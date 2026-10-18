# ER diagram

## Scopo
Mostrare **entità, attributi e relazioni** (cardinalità) di un modello dati.

## Quando usarlo
- Design o documentazione di schema
- Chiarire "cosa è legato a cosa" prima di scrivere codice (partire dal domain model)

## Quando NON usarlo
- Serve il comportamento nel tempo → flowchart / sequence / state.

## Come costruirlo
1. Entità al singolare, MAIUSCOLO (`CONSULTANCY`), attributi in inglese.
2. Dichiara tipo, nome, e chiave (`PK`, `FK`) per ogni attributo.
3. Cardinalità: `||--o{` (uno a molti opzionale), `||--||` (uno a uno), `}o--o{` (molti a molti, da risolvere con entità ponte).
4. Etichetta ogni relazione con un verbo (`"has"`, `"produces"`).
5. **Colori**: l'ER non ha un equivalente portabile di status/action/decision; non forzarlo. Lascia lo stile di default per massimizzare la portabilità e dichiaralo come scelta.

## Esempio finito
```mermaid
erDiagram
    CLIENT ||--o{ CONSULTANCY : orders
    CONSULTANT ||--o{ CONSULTANCY : delivers
    CONSULTANCY ||--o{ DELIVERABLE : produces
    CONSULTANCY ||--o{ INVOICE : "is billed by"

    CLIENT {
        uuid id PK
        string name
        string billing_email
    }
    CONSULTANT {
        uuid id PK
        string full_name
    }
    CONSULTANCY {
        uuid id PK
        uuid client_id FK
        uuid consultant_id FK
        string status
        date delivered_on
    }
    DELIVERABLE {
        uuid id PK
        uuid consultancy_id FK
        string version
        string review_result
    }
    INVOICE {
        uuid id PK
        uuid consultancy_id FK
        decimal amount
        date due_date
        string payment_status
    }
```
