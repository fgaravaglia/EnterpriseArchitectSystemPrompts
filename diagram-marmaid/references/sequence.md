# Sequence diagram

## Scopo
Mostrare **l'ordine temporale dei messaggi** tra attori e sistemi: chi chiama chi, cosa risponde, cosa succede in caso di errore o timeout.

## Quando usarlo
- Integrazioni API, orchestrazione tra servizi, protocolli
- Debug o design di flussi dove l'ordine e le risposte contano
- Dettaglio di *un singolo passo* di un flowchart più grande

## Quando NON usarlo
- Logica di business con molti rami: diventa illeggibile → flowchart.

## Come costruirlo
1. `participant` con alias in inglese, nell'ordine in cui compaiono.
2. `autonumber` per riferirsi ai passi.
3. Frecce `->>` per richieste, `-->>` per risposte.
4. Rami con `alt / else / end`, cicli con `loop`, parallelismo con `par`.
5. **Colori**: le sequence non supportano `classDef`. Adatta la palette con blocchi `rect rgb(...)`:
   - status update → `rect rgb(255, 249, 196)` (giallo chiaro)
   - action/operazione di business → `rect rgb(255, 224, 178)` (arancione chiaro)
   - decision → il blocco `alt` stesso (nota: non è colorabile in modo portabile; usa `Note over` con testo `Decision: ...` se serve enfasi)
6. Dichiara il mapping dei colori in un commento `%%` in testa.

## Esempio finito
```mermaid
sequenceDiagram
    %% Colors: yellow = status update, orange = business action
    autonumber
    participant C as Consultant
    participant P as Portal
    participant Q as Quality Service
    participant B as Billing Service
    participant CL as Client

    C->>P: Mark consultancy as delivered
    rect rgb(255, 249, 196)
        P->>P: Set status DELIVERED
    end
    P->>Q: Request completeness check
    Q-->>P: Check result

    alt Deliverable incomplete
        rect rgb(255, 249, 196)
            P->>P: Set status IN REWORK
        end
        P-->>C: Notify rework required
    else Deliverable complete
        rect rgb(255, 224, 178)
            P->>CL: Send deliverable
        end
        CL-->>P: Accept or request changes
        alt Client accepts
            rect rgb(255, 249, 196)
                P->>P: Set status ACCEPTED
            end
            P->>B: Create invoice
            B-->>P: Invoice created
            rect rgb(255, 249, 196)
                P->>P: Set status INVOICED
            end
        else Client requests changes
            rect rgb(255, 249, 196)
                P->>P: Set status REVISION REQUESTED
            end
            P-->>C: Notify change request
        end
    end
```
