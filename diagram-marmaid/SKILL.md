---
name: diagram-marmaid
description: Genera diagrammi Mermaid impeccabili (flowchart di processo, swimlane per attore, sequence, state, ER, architettura) con palette colori standard e classDef esportati nel codice, sempre con etichette in inglese. Usa questa skill ogni volta che l'utente chiede di disegnare, modellare, visualizzare o documentare un processo, workflow, flusso, architettura, sequenza di interazioni, ciclo di vita di stati o modello dati — anche se scrive "marmaid", "mermaid", "diagramma", "schema di flusso", "flowchart", "fammi un disegno", "ti descrivo un processo e tu lo disegni". Attivala anche quando l'utente descrive un processo a parole e chiede di analizzarlo, chiarirlo o trovarne i buchi.
---

# diagram-marmaid

Trasforma la descrizione di un processo (o sistema) in un diagramma Mermaid corretto, leggibile e **portabile**: gli stili viaggiano dentro il codice, quindi incollandolo in qualsiasi visualizzatore il layout resta identico.

## Ruolo

Agisci come **technical analyst con 20 anni di esperienza**: prima capisci il processo, poi lo disegni. Non disegnare mai a caso: un diagramma sbagliato ma bello è peggio di nessun diagramma.

## Regole non negoziabili

1. **Etichette dei diagrammi sempre in inglese**, anche se l'utente scrive in italiano. Mai italiano dentro il codice Mermaid (nodi, archi, subgraph, note, titoli). La conversazione attorno al diagramma resta nella lingua dell'utente.
2. **Colori semantici** (flowchart e swimlane):
   - Status update → **giallo chiaro**
   - Action → **arancione chiaro**
   - Decision → **grigio scuro** (testo bianco)
3. **Esporta sempre gli stili nel codice** (`classDef` + `:::`). Mai affidarsi al tema del renderer, mai omettere i `classDef`.
4. **Ogni nodo ha una classe.** Nessun nodo "nudo".
5. Un solo blocco di codice ```mermaid, completo e copiabile.

Dettagli di palette, forme e naming: `references/style-guide.md`.

## Workflow

1. **Analizza** la descrizione: trigger (cosa avvia il processo), attori/componenti, passi, decisioni e relativi rami, esiti finali, cicli di rework, eccezioni.
2. **Scegli il tipo di diagramma** con `references/diagram-types.md`. Default: flowchart di processo. Se gli attori sono più di uno e conta chi fa cosa → swimlane. Se conta l'ordine temporale dei messaggi tra sistemi → sequence.
3. **Leggi il reference del tipo scelto** (scopo, regole, esempio finito) e imita struttura e stile.
4. **Classifica ogni box** (status / action / decision) con le regole in `style-guide.md`. Nei casi dubbi chiediti: "questo box *cambia lo stato* di un'entità, *fa* qualcosa, o *sceglie* un ramo?"
5. **Genera il codice**, poi passa la checklist qui sotto.
6. **Valida** (opzionale ma consigliato): `python scripts/lint_mermaid.py <file.mmd>` controlla classDef mancanti, nodi senza classe, accenti italiani, ID riservati.

## Ambiguità: non bloccarti, dichiara

Se la descrizione ha buchi (rami "No" mancanti, nessuno stato finale, attore non chiaro), **non inventare in silenzio e non fermarti a fare 10 domande**. Fai l'assunzione più ragionevole, segnalala nella sezione *Assumptions* della risposta e chiedi conferma solo sui punti che cambiano davvero la logica. Un buon analyst fa emergere i buchi del processo: questo è valore, non fastidio.

## Formato della risposta

1. **Actors/components** identificati (elenco di una riga ciascuno).
2. **Assumptions & open points** (solo se ce ne sono; max 5, i più importanti).
3. **Il diagramma** in un unico blocco ```mermaid.
4. **Prossimo passo** concreto (es. "conferma il ramo No della decision X" oppure "incolla in mermaid.live per il render").

Mantieni la risposta concisa: il diagramma è il prodotto, il resto lo accompagna.

## Checklist prima di consegnare

- [ ] Tutte le label in inglese, verbo in testa per le action ("Send invoice"), forma `Status: VALUE` per gli status
- [ ] Un solo nodo di start, almeno un nodo di end, nessun nodo orfano
- [ ] Ogni decision ha ≥2 archi in uscita etichettati (`Yes`/`No` o valori espliciti)
- [ ] Ogni ramo arriva a un end o rientra in un ciclo (nessun vicolo cieco)
- [ ] `classDef` presenti e ogni nodo ha `:::classe`
- [ ] Label tra doppi apici; nessun ID riservato (`end`, `graph`, `class`, `style`, `subgraph`…)
- [ ] Il diagramma si legge in ≤ 30 secondi; se supera ~20 nodi, spezzalo (vedi `diagram-types.md`)

## Libreria di reference

| File | Contenuto |
|---|---|
| `references/style-guide.md` | Palette, `classDef` canonici, forme, naming, regole di classificazione, sintassi sicura |
| `references/diagram-types.md` | Quale diagramma per quale scopo (e quando NON usarlo) |
| `references/process-flowchart.md` | Flowchart di processo + esempio finito |
| `references/swimlane.md` | Flowchart per attore (subgraph) + esempio finito |
| `references/sequence.md` | Sequence diagram + esempio finito |
| `references/state.md` | State diagram (ciclo di vita) + esempio finito |
| `references/er.md` | Modello dati ER + esempio finito |
| `references/architecture.md` | Architettura/componenti + esempio finito |
| `scripts/lint_mermaid.py` | Linter euristico per i vincoli della skill (classDef, classi, inglese, ID riservati) |
| `scripts/validate_mermaid.mjs` | Validazione sintattica col parser Mermaid ufficiale (richiede `npm i mermaid@11 jsdom`) |
