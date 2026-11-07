# Quale diagramma per quale scopo

## Albero decisionale rapido

1. Devo mostrare **passi e decisioni** di un processo? → **Process flowchart**
2. …e conta **chi** fa cosa (≥3 attori/team)? → **Swimlane**
3. Devo mostrare **messaggi nel tempo** tra sistemi/persone (chiamate, risposte, timeout)? → **Sequence**
4. Devo mostrare **gli stati** di un'entità e le transizioni permesse? → **State**
5. Devo mostrare **entità dati e relazioni**? → **ER**
6. Devo mostrare **componenti, layer, integrazioni**? → **Architecture**

## Tabella di scelta

| Tipo | Scopo | Domanda a cui risponde | Usalo quando | Non usarlo quando | Palette status/action/decision |
|---|---|---|---|---|---|
| Process flowchart | Descrivere un processo end-to-end | "Cosa succede, in che ordine, con quali scelte?" | Processo con decisioni, rework, esiti multipli | Il tempo/messaggistica tra sistemi è il punto centrale | Sì, piena |
| Swimlane | Assegnare responsabilità | "Chi fa cosa, e dove avvengono gli handoff?" | ≥3 attori, handoff critici, audit/compliance | Un solo attore (rumore inutile) | Sì, piena |
| Sequence | Interazioni ordinate nel tempo | "Chi chiama chi, in che ordine, cosa torna?" | Integrazioni API, protocolli, debug di flussi tra sistemi | Servono rami di business complessi (diventa illeggibile) | Adattata (`rect` colorati) |
| State | Ciclo di vita di un'entità | "Quali stati esistono e quali transizioni sono lecite?" | Definire/validare un modello di stato (ordine, pratica, ticket) | Interessa la sequenza di attività, non lo stato | Solo `status` |
| ER | Modello dati | "Quali entità, attributi, cardinalità?" | Design/documentazione di schema | Serve il comportamento, non la struttura | Nessun colore semantico |
| Architecture | Struttura del sistema | "Quali componenti, layer, dipendenze?" | Overview tecnica, integrazioni, confini | Serve il flusso temporale (→ sequence) | Palette propria (component/datastore/external) |

## Combinazioni utili

- **Overview + dettaglio**: un flowchart macro-fasi (≤10 nodi) + un flowchart per ogni fase complessa.
- **Processo + stati**: flowchart di processo (cosa si fa) + state diagram (come cambia lo stato). I nodi `Status: X` del flowchart devono corrispondere esattamente agli stati dello state diagram: verifica la coerenza dei nomi.
- **Processo + sequence**: flowchart per la logica di business, sequence per il dettaglio d'integrazione di un singolo passo.

## Segnali che il diagramma è sbagliato

- Troppe frecce che si incrociano → prova swimlane o dividi.
- Decision con un solo ramo disegnato → manca un esito.
- Nessun nodo end raggiungibile da un ramo → vicolo cieco.
- Più nodi start → il trigger è ambiguo: chiedi all'utente.
- Label in italiano → violazione della regola n.1.
