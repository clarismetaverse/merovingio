# Continuazione del segmento: risultati verificati

[Live 40007031575](https://github.com/clarismetaverse/merovingio/actions/runs/40007031575) completato sul commit `cf0daca85d53ec0fe81fecdf99359bf1a4256ae9`. **Otto richieste indipendenti, una Choice nativa ciascuna, otto risposte, zero failure e zero retry.** Protocollo, sette PNG unici e manifest erano congelati in quel commit prima delle chiamate. Branch `codex/segment-continuation`, derivato da `90083c9`; main e tutti i lavori precedenti preservati.

## Risultato principale

| Evidenza sulla storia | JEV: passo successivo corretto | Insufficienza dichiarata | Baseline abbinata |
|---|---:|---:|---|
| Solo immagine finale comune | **Non identificabile** | 2/2 | 2/2 astensioni |
| Tre immagini cronologiche | **1/2** | 0/2 | Tracker raster 2/2 |
| Tre record testuali di coordinate | **2/2** | 0/2 | Tracker di coordinate 2/2 |
| Immagini + stessi record | **2/2** | 0/2 | Entrambi i tracker 2/2, concordi |

Le alternative sono sempre immagini: la cronologia testuale non è un controllo completamente privo di immagini. Nei due controlli finali il modello ha restituito informazioni insufficienti, senza proporre un estremo arbitrario. Le due richieste sono identiche per hash e pianificate prima del live, non tentativi ripetuti fino alla risposta voluta. Non esiste un gold unico di continuazione in quel controllo, quindi accuratezza geometrica e riferimento dell’azione restano null.

**Con le sole immagini JEV propone extend_A in entrambe le storie.** Risolve la crescita da A e sbaglia la crescita da B: non distingue correttamente entrambe le storie con la stessa immagine finale. Il passo sbagliato è comunque un prolungamento geometrico valido; fallisce la continuazione del movimento dimostrato, non la collinearità. Questo separa validità dell’operazione e coerenza con la storia.

## Scelte, probabilità e confidenza native

| Storia | Condizione | Scelta | P(scelta) | Confidenza nativa |
|---|---|---|---:|---:|
| Cresce A | final_only | insufficient | .98 | .98 |
| Cresce B | final_only | insufficient | .96 | .95 |
| Cresce A | images | extend_A | .60 | .52 |
| Cresce B | images | extend_A, **errato** | .69 | .63 |
| Cresce A | text_history | extend_A | .82 | .78 |
| Cresce B | text_history | extend_B | .29 | .15 |
| Cresce A | combined | extend_A | .71 | .65 |
| Cresce B | combined | extend_B | .59 | .51 |

Il successo text_history/B è fragile: P(extend_B)=.29, hold=.26 e extend_A=.25, con confidenza .15. Non trasformiamo il 2/2 in robustezza dimostrata. Nell’errore visivo la confidenza è invece .63: la confidenza nativa non è una certificazione di correttezza. Nessuna soglia è stata applicata o aggiustata dopo i risultati. Affidabilità numerica separata non restituita: null. Distribuzioni complete e matrici sono nel JSON.

Nel confronto appaiato, testo e combined correggono entrambi il caso B sbagliato dalle sole immagini e mantengono corretto A. Combined non aggiunge un successo rispetto alla cronologia testuale; aumenta la probabilità dell’opzione corretta per B e la riduce per A. Sono due casi, senza repliche: non è isolato un contributo causale dell’immagine o una stima di variabilità.

## Verifica e baseline

Il codice controlla che le alternative siano segmenti non degeneri sulla retta corrente; per i prolungamenti controlla contenimento del segmento precedente, un solo estremo modificato e passo di 25 pixel. Il target è estrapolato dalla cronologia sotto la regola esplicita “stesso estremo, stesso spostamento per passo”. Non è una previsione dell’intenzione umana senza assunzioni.

Il tracker raster estrae gli estremi dai pixel blu/ambra delle effettive immagini inviate, calcola gli spostamenti e confronta il passo previsto con i PNG delle alternative. Non riceve nome della storia, coordinate del renderer, target o diagnosi JEV. Risolve entrambi i casi visivi e si astiene senza storia. Il tracker testuale usa le coordinate rese disponibili al modello e le stesse opzioni visive. Questa baseline è specializzata per disegni puliti e palette nota, non visione generale; qui **non emerge un vantaggio di JEV rispetto al tracciamento degli estremi**. Non abbiamo misurato un vantaggio di costo o latenza.

## Interpretazione strutturale e limiti

`SAME_FINAL_SEGMENT != SAME_NEXT_EDIT`, a parità della regola di continuazione e con storie diverse. Per uno stato S=(A,B), una trasformazione candidata ha forma S'=(A+ΔA,B+ΔB), con un solo Δ non nullo; collinearità e contenimento distinguono un prolungamento da altri cambiamenti. La storia fornisce quale Δ proseguire. Il codice verifica tali proprietà; il modello sceglie una trasformazione fra immagini già generate.

Questa prova non mostra ancora un uso affidabile della sola sequenza visiva per proporre l’estensione. Mostra che il modello può scegliere i passi corretti quando riceve le coordinate della storia, con bassa confidenza in uno dei due casi. Non è generazione libera di coordinate o costruzioni, induzione di Generic Spaces, prova geometrica o ragionamento sequenziale interno dimostrato.

Un’unica scala, una rotazione/riflessione condivisa, stessa assegnazione di lettere/colori e opzioni fisse: non possiamo attribuire l’errore a colore, lettera, posizione, ordine o rappresentazione delle opzioni. Non ci sono test live di ordine inverso/shuffle o immagini isolate aggiuntive. Due osservazioni distinte basterebbero al tracker: il confronto col finale non prova necessità di tre frame. Le otto domande sono due template sotto quattro presentazioni, non otto problemi geometrici indipendenti.

## Integrità e conservazione

Actions ha superato **204 test, build del viewer esistente e audit degli otto corpi e risposte**. Manifest canonico SHA256 `fc44b4971e9e2ddd75d6a0f62bfddba57f0134a17bb75a18cbb8b18aa7db990a`. Audit ricostruisce ogni richiesta e ricontrolla byte dei PNG, controlli finali identici, opzioni comuni, entrambe le baseline, matrici e valori sanificati. `live_results.json` preserva il JSON originale scaricato, senza riscrittura.

Usage: **28372 input token, 640 output token**; totale non restituito, null. Otto confidenze native presenti, nessuna affidabilità numerica separata. Solo chiamate tramite Actions con secret `TYPESAFE_API_KEY` e header `TypeSafe-Danger-Zone-Images: true`; nessuna chiave o risposta libera di errore esposta. La verifica finale del branch e il pacchetto in Library sono documentati nei metadati CI e nel manifest del pacchetto, senza nuove chiamate JEV.
