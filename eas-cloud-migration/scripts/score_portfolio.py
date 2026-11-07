#!/usr/bin/env python3
"""Deterministic Fit Score + R assignment for the eas-cloud-migration skill.

Usage:  python score_portfolio.py inventory.csv [--driver dc_exit_speed|cost|agility|resilience] [--md]
Output: CSV (default) or Markdown table on stdout. Gates mirror
references/scoring-and-decision-gates.md; keep the two in sync.
Unknown scores ("?" or blank) are never guessed: the row is flagged NEEDS_DATA.
"""
import argparse, csv, sys

WEIGHTS = {"BV": 5, "TT": 4, "CR": 3, "CH": 5, "TL": 3}


def num(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def yes(v):
    return str(v or "").strip().lower() in ("yes", "y", "true", "1")


def fit_score(s):
    tot_w = sum(WEIGHTS.values())
    # integer math + round-half-up: avoids float artefacts (57.4999 vs 57.5)
    return (2 * (sum(s[k] * w for k, w in WEIGHTS.items()) - tot_w) * 100 + 4 * tot_w) // (8 * tot_w)


def assign(row, s, driver):
    """Return (R, rationale, adjacent_R). First matching gate wins."""
    usage = (row.get("usage") or "").strip().lower()
    saas = num(row.get("saas_fit_pct")) or 0
    if usage == "none" or (row.get("duplicate_of") or "").strip():
        return "Retire", "Unused or duplicate (gate 1)", "Retain"
    if s["CH"] == 1 or yes(row.get("hw_dependency")) or yes(row.get("vendor_unsupported_in_cloud")):
        return "Retain", "Hard block: compliance/hardware/vendor (gate 2)", "Rehost"
    if s["TL"] <= 2 and s["BV"] <= 3:
        return "Retain", "Short remaining life, low value: keep until EoL (gate 3)", "Retire"
    if saas >= 80 and s["BV"] <= 4:
        return "Repurchase", f"Commodity, SaaS fit {saas}% (gate 4)", "Retire"
    if (row.get("source") or "").lower() == "vmware" and driver == "dc_exit_speed" and s["CR"] <= 2:
        return "Relocate", "VMware source + fast DC exit (gate 5)", "Rehost"
    if (s["BV"] >= 4 and s["TL"] >= 4 and (s["TT"] <= 3 or s["CR"] <= 3)
            and (row.get("refactor_case") or "").lower() == "positive"):
        return "Refactor", "Strategic, long-lived, positive business case (gate 6)", "Replatform"
    if 2 <= s["CR"] <= 4 and s["BV"] >= 3 and yes(row.get("managed_alternative")):
        return "Replatform", "Managed-service gain, medium readiness (gate 7)", "Rehost"
    return "Rehost", "Default (gate 8)", "Replatform"


def compliance_overlay(row, s, r, threshold):
    """Overlay (does NOT change the R): mandatory conditions for apps with low
    Compliance Headroom. CH=1 is already handled by gate 2 (Retain)."""
    if r in ("Retire", "Retain") or s["CH"] > threshold:
        return "-"
    conds = ["compliance sign-off before wave entry", "tested exit plan",
             "resilience design (tier-1: multi-AZ/region)", "not in Wave 1"]
    if r in ("Repurchase", "Replatform", "Refactor"):
        conds.append("ICT provider risk assessment + register entry")
    return "; ".join(conds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--driver", default="cost")
    ap.add_argument("--md", action="store_true")
    ap.add_argument("--ch-threshold", type=int, default=2,
                    help="apps with CH <= threshold get compliance conditions (default 2)")
    a = ap.parse_args()

    out = []
    with open(a.csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = {k: num(row.get(k)) for k in WEIGHTS}
            if any(v is None for v in s.values()):
                out.append([row["app_name"], "?", "NEEDS_DATA", "Missing scores", "-", "-"])
                continue
            r, why, adj = assign(row, s, a.driver)
            out.append([row["app_name"], fit_score(s), r, why, adj,
                        compliance_overlay(row, s, r, a.ch_threshold)])

    head = ["app_name", "fit_score", "recommended_R", "gate_rationale", "adjacent_R", "compliance_conditions"]
    if a.md:
        print("| " + " | ".join(head) + " |")
        print("|" + "---|" * len(head))
        for r in out:
            print("| " + " | ".join(map(str, r)) + " |")
    else:
        w = csv.writer(sys.stdout)
        w.writerow(head)
        w.writerows(out)


if __name__ == "__main__":
    main()
