# Style guide

## Indice
1. Palette e classDef canonici
2. Forme dei nodi
3. Come classificare un box
4. Naming e label
5. Sintassi sicura (cosa rompe Mermaid)
6. Layout e leggibilità

## 1. Palette e classDef canonici

Copia **sempre** questo blocco in fondo ai flowchart/swimlane (togli solo le classi non usate, mai quelle usate).

```text
classDef status fill:#FFF9C4,stroke:#F9A825,stroke-width:1.5px,color:#3E2723
classDef action fill:#FFE0B2,stroke:#FB8C00,stroke-width:1.5px,color:#3E2723
classDef decision fill:#424242,stroke:#212121,stroke-width:1.5px,color:#FFFFFF
classDef terminator fill:#ECEFF1,stroke:#607D8B,stroke-width:1.5px,color:#263238
```

| Classe | Significato | Colore | Richiesto dall'utente? |
|---|---|---|---|
| `status` | Aggiornamento di stato | giallo chiaro `#FFF9C4` | Sì |
| `action` | Azione / operazione | arancione chiaro `#FFE0B2` | Sì |
| `decision` | Decisione / branching | grigio scuro `#424242`, testo bianco | Sì |
| `terminator` | Start / End | grigio-azzurro neutro `#ECEFF1` | No: scelta neutra per non competere con i 3 colori semantici |

Opzionale, solo se il processo ha sistemi esterni da evidenziare:

```text
classDef external fill:#E3F2FD,stroke:#1E88E5,stroke-width:1.5px,color:#0D47A1,stroke-dasharray:4 3
```

Opzionale per i subgraph (lane/gruppi), applicata con `class laneId lane`:

```text
classDef lane fill:#FAFAFA,stroke:#BDBDBD,stroke-width:1px,color:#424242
```

Non aggiungere altri colori senza che l'utente li chieda: il codice colore è parte del significato.

## 2. Forme dei nodi

Colore **e** forma portano significato (utile in stampa e in b/n).

| Tipo | Forma Mermaid | Esempio |
|---|---|---|
| Start / End | stadium `([ ])` | `start(["Process starts"]):::terminator` |
| Action | rettangolo `[ ]` | `send["Send invoice"]:::action` |
| Status update | rettangolo arrotondato `( )` | `stPaid("Status: PAID"):::status` |
| Decision | rombo `{ }` | `ok{"Approved?"}:::decision` |
| External system | rettangolo `[ ]` + classe `external` | `crm["CRM"]:::external` |

## 3. Come classificare un box

Domanda guida: **cosa fa questo box all'entità di business?**

- **Status** = scrive/cambia il *valore di stato* di un'entità (Consultancy, Order, Ticket…). Etichetta `Status: VALUE`. Esempi: `Status: DELIVERED`, `Set status to CLOSED`.
- **Action** = compie lavoro: calcola, invia, crea, notifica, valida, chiama un servizio, aggiorna dati che *non* sono lo stato. Esempi: `Generate invoice`, `Notify client`.
- **Decision** = valuta una condizione e sceglie un ramo. Sempre rombo, sempre domanda o condizione, archi etichettati.

Casi dubbi:
- "Update CRM" → **action** (aggiorna dati). "Set CRM opportunity to Won" → **status**.
- Un'action che *come effetto collaterale* cambia stato → due box: prima l'action, poi lo status. Mai fondere.
- "Check if X" senza ramo → è un'action. Con ramo → decision.
- "Wait for client reply" → action (attesa), seguita da decision se c'è esito.

## 4. Naming e label

- **Inglese**, sempre.
- **ID dei nodi**: camelCase breve e parlante (`sendInvoice`, `stClosed`, `chkComplete`). Prefisso `st` per status, `chk` per decision aiuta la leggibilità del codice.
- **Action**: verbo all'imperativo + oggetto (`Send final invoice`).
- **Status**: `Status: VALUE` in maiuscolo per il valore.
- **Decision**: domanda breve che termina con `?` (`Deliverable complete?`).
- **Archi dalle decision**: `Yes` / `No`, oppure valori espliciti se >2 rami (`Approved`, `Rejected`, `Escalate`).
- Max ~6 parole per label. Più lungo → `<br/>` per andare a capo.
- Archi fuori dalle decision: di norma senza etichetta, salvo serva chiarire (`on timeout`).

## 5. Sintassi sicura

- **Metti sempre le label tra doppi apici**: `a["Label (with parens)"]`. Evita rotture con `()`, `[]`, `{}`, `:`, `#`, `;`.
- Dentro le label non usare `"`; usa `#quot;`. Per `#` usa `#35;`.
- **ID riservati da evitare**: `end`, `graph`, `subgraph`, `class`, `classDef`, `style`, `click`, `default`. Un nodo chiamato `end` rompe il parser (usa `finish`).
- Un ID che inizia con `o` o `x` dopo `---` viene letto come terminatore di freccia (`A---oB`): usa ID che non iniziano così, oppure spazia (`A --- oB`).
- Applica le classi con `:::` alla definizione del nodo: `a["Text"]:::action`. Una sola classe per nodo.
- Dichiara prima tutti i nodi (con classe), poi gli archi: codice più pulito e diff più facile.
- `classDef` in fondo, uno per riga.
- Commenti con `%%` su riga propria.
- Direzione: `flowchart TD` per processi verticali; `flowchart LR` per pipeline ampie. Usa `flowchart`, non `graph` (più moderno, stessi stili).

## 6. Layout e leggibilità

- Flusso principale ("happy path") dritto, eccezioni e rework ai lati.
- Cicli di rework: un solo arco di ritorno verso un nodo già presente, non duplicare nodi.
- Oltre ~20 nodi: dividi in un diagramma *overview* (macro-fasi) + diagrammi di dettaglio per fase.
- Incrocio di archi frequente → ripensa l'ordine delle dichiarazioni o passa a swimlane.
- Titolo opzionale via frontmatter:
  ```
  ---
  title: Consultancy completion
  ---
  ```
  (solo se il visualizzatore dell'utente lo supporta; in dubbio, omettilo).
