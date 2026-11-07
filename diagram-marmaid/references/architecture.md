# Architecture / component diagram

## Scopo
Mostrare **componenti, layer, integrazioni e confini** di un sistema (cosa c'è, cosa parla con cosa).

## Quando usarlo
- Overview tecnica per stakeholder, ADR, onboarding
- Confini tra sistemi interni ed esterni, flussi di dati principali

## Quando NON usarlo
- Serve l'ordine temporale delle chiamate → sequence.

## Come costruirlo
1. `flowchart LR` con un `subgraph` per layer/boundary (es. *Channels*, *Core Services*, *Data*, *External*).
2. **Palette propria**: la semantica status/action/decision NON si applica qui (i componenti non sono azioni). Usa:
   - `component` → azzurro chiaro (servizi interni)
   - `datastore` → verde chiaro, forma cilindro `[( )]`
   - `external` → grigio chiaro tratteggiato (sistemi di terzi)
3. Esporta sempre i `classDef`, come per i flowchart.
4. Etichetta gli archi con il tipo di integrazione (`REST`, `Event`, `Batch`), non con frasi lunghe.
5. Un solo livello di dettaglio per diagramma; per scendere di livello fai un secondo diagramma.

## Esempio finito
```mermaid
flowchart LR
    subgraph channels["Channels"]
        portal["Consultant Portal"]:::component
    end

    subgraph core["Core Services"]
        workflow["Consultancy Workflow Service"]:::component
        quality["Quality Check Service"]:::component
        billing["Billing Service"]:::component
    end

    subgraph data["Data"]
        db[("Consultancy DB")]:::datastore
        bus[("Event Bus")]:::datastore
    end

    subgraph ext["External"]
        crm["CRM"]:::external
        erp["ERP"]:::external
    end

    portal -->|REST| workflow
    workflow -->|REST| quality
    workflow --> db
    workflow -->|Event| bus
    bus -->|Event| billing
    billing -->|REST| erp
    workflow -->|REST| crm

    classDef component fill:#E3F2FD,stroke:#1E88E5,stroke-width:1.5px,color:#0D47A1
    classDef datastore fill:#E8F5E9,stroke:#43A047,stroke-width:1.5px,color:#1B5E20
    classDef external fill:#F5F5F5,stroke:#757575,stroke-width:1.5px,color:#424242,stroke-dasharray:4 3
```
