# Swimlane (flowchart per attore)

## Scopo
Mostrare **chi** fa cosa e dove avvengono gli handoff tra attori/team/sistemi.

## Quando usarlo
- ≥3 attori e le responsabilità sono il punto della discussione
- Audit, compliance, RACI impliciti (utile in contesti regolamentati)
- Si vogliono individuare colli di bottiglia negli handoff

Con un solo attore usa il process flowchart.

## Come costruirlo
1. Un `subgraph` per attore, con ID e titolo in inglese (`subgraph consultant["Consultant"]`).
2. Dentro ogni lane, **solo i nodi** di quell'attore; gli archi tra lane si dichiarano **fuori** dai subgraph.
3. Applica `class laneId lane` per lo stile neutro delle lane (non usare i 3 colori semantici sulle lane).
4. Direzione `flowchart LR` se le lane sono pochissime e il flusso lungo; `TD` come default.
5. Mantieni stesse regole di colore/forma/classDef del process flowchart.

## Esempio finito
```mermaid
flowchart TD
    start(["Consultancy marked as delivered"]):::terminator

    subgraph consultant["Consultant"]
        submit["Submit final deliverable"]:::action
        fixIssues["Fix reported issues"]:::action
    end

    subgraph quality["Quality Team"]
        chkComplete{"Deliverable<br/>complete?"}:::decision
        stRework("Status: IN REWORK"):::status
        stDelivered("Status: DELIVERED"):::status
    end

    subgraph client["Client"]
        chkAccept{"Accepts<br/>deliverable?"}:::decision
        reqChange["Submit change request"]:::action
    end

    subgraph finance["Finance"]
        stAccepted("Status: ACCEPTED"):::status
        invoice["Issue invoice"]:::action
        stClosed("Status: CLOSED"):::status
    end

    finish(["Consultancy completed"]):::terminator

    start --> submit --> chkComplete
    chkComplete -->|No| stRework --> fixIssues --> submit
    chkComplete -->|Yes| stDelivered --> chkAccept
    chkAccept -->|No| reqChange --> fixIssues
    chkAccept -->|Yes| stAccepted --> invoice --> stClosed --> finish

    classDef status fill:#FFF9C4,stroke:#F9A825,stroke-width:1.5px,color:#3E2723
    classDef action fill:#FFE0B2,stroke:#FB8C00,stroke-width:1.5px,color:#3E2723
    classDef decision fill:#424242,stroke:#212121,stroke-width:1.5px,color:#FFFFFF
    classDef terminator fill:#ECEFF1,stroke:#607D8B,stroke-width:1.5px,color:#263238
    classDef lane fill:#FAFAFA,stroke:#BDBDBD,stroke-width:1px,color:#424242
    class consultant,quality,client,finance lane
```

## Note
- Mermaid non ha vere "corsie" orizzontali: i subgraph sono raggruppi. In `TD` le lane si impilano in base al flusso; è normale e leggibile.
- L'assegnazione di un box a una lane è un'**assunzione di responsabilità**: se la descrizione non la dice, dichiarala in *Assumptions*.
