# Process flowchart

## Scopo
Descrivere un processo end-to-end: trigger, azioni, aggiornamenti di stato, decisioni, rework ed esiti finali. È il tipo **di default** di questa skill.

## Quando usarlo
- L'utente descrive "il processo parte quando… poi… se… altrimenti…"
- Servono decisioni con rami e cicli di rework
- Un solo attore principale, o attori non rilevanti per la lettura

## Come costruirlo
1. Un solo `terminator` di start (il trigger) e ≥1 di end.
2. Disegna prima l'happy path, poi rami d'errore/rework.
3. Ogni "set status" è un box `status` separato dall'action che lo causa.
4. Decision con archi `Yes`/`No` (o valori espliciti).
5. `classDef` in fondo; ogni nodo con `:::classe`.

## Esempio finito
Input utente (riassunto): *"Il processo si avvia quando il consulente segna la consulenza come consegnata. Il team qualità verifica la completezza; se manca qualcosa, rework. Poi il deliverable va al cliente, che accetta o chiede modifiche. Dopo l'accettazione si fattura; se non pagata entro 30 giorni, sollecito. Alla fine la pratica si chiude."*

```mermaid
flowchart TD
    %% --- Nodes ---
    start(["Consultancy marked as delivered"]):::terminator
    submit["Submit final deliverable<br/>to quality review"]:::action
    chkComplete{"Deliverable<br/>complete?"}:::decision
    reqRework["Request rework<br/>from consultant"]:::action
    stRework("Status: IN REWORK"):::status
    stDelivered("Status: DELIVERED"):::status
    sendClient["Send deliverable to client"]:::action
    chkAccept{"Client<br/>accepts?"}:::decision
    logChange["Log client change request"]:::action
    stRevision("Status: REVISION REQUESTED"):::status
    stAccepted("Status: ACCEPTED"):::status
    invoice["Generate and send invoice"]:::action
    chkPaid{"Paid within<br/>30 days?"}:::decision
    remind["Send payment reminder"]:::action
    stClosed("Status: CLOSED"):::status
    finish(["Consultancy completed"]):::terminator

    %% --- Flow ---
    start --> submit --> chkComplete
    chkComplete -->|No| reqRework --> stRework --> submit
    chkComplete -->|Yes| stDelivered --> sendClient --> chkAccept
    chkAccept -->|No| logChange --> stRevision --> submit
    chkAccept -->|Yes| stAccepted --> invoice --> chkPaid
    chkPaid -->|No| remind --> chkPaid
    chkPaid -->|Yes| stClosed --> finish

    %% --- Styles (exported for portability) ---
    classDef status fill:#FFF9C4,stroke:#F9A825,stroke-width:1.5px,color:#3E2723
    classDef action fill:#FFE0B2,stroke:#FB8C00,stroke-width:1.5px,color:#3E2723
    classDef decision fill:#424242,stroke:#212121,stroke-width:1.5px,color:#FFFFFF
    classDef terminator fill:#ECEFF1,stroke:#607D8B,stroke-width:1.5px,color:#263238
```

## Perché funziona
- Ogni cambio di stato ha il suo box giallo, quindi si vede *dove* il sistema scrive lo stato.
- I tre cicli di rework rientrano su `submit` invece di duplicare nodi.
- Le decision sono scure: l'occhio trova subito i punti di branching.
