# Colori e associazione agli ID: nessun recupero del negativo in questo run

**I colori non migliorano la correttezza della coppia in questa prova.** Il nuovo replay monocromatico fa 2/2, i colori soli 1/2 e gli stessi colori con legenda 1/2. Le probabilità restano vicine alla soglia sul negativo. Il risultato non prova che i colori siano inutili in generale e non giustifica una soglia scelta dopo aver visto i dati.

Il [run live 39999505442](https://github.com/clarismetaverse/merovingio/actions/runs/39999505442) è concluso con successo, commit `2b12ec67791a683134a297351e54dff3044437b2`: **tre richieste di due Noul, sei giudizi nuovi**. Nessun retry automatico, Score, composito o tabella di copertura. Stessi bridge C914 positivo e C850 negativo, geometria, orientazione/riflessione, ID, richiesta esplicita, ordine, contratti e fatti metrici.

| Versione | P(sì), positivo | P(sì), negativo | Margine | Corretti | Brier medio |
|---|---:|---:|---:|---:|---:|
| Replay monocromatico | .54 | .48 | +.06 | 2/2 | .22100 |
| Solo colori | .68 | .51 | +.17 | 1/2 | .18125 |
| Colori + legenda degli ID | .70 | .56 | +.14 | 1/2 | .20180 |

Soglia preregistrata invariata: p>.5 sì, p<.5 no, p=.5 astensione contata errata. Monocromatico: TP=1, TN=1, FP=FN=0. Ciascuna versione a colori: TP=1, FP=1, TN=FN=0. Nessuna astensione. Totale descrittivo 4/6, contro 3/6 sempre sì; sono tre versioni della stessa coppia, non sei geometrie indipendenti.

## Cosa cambia e cosa non possiamo attribuire ai colori

Il replay monocromatico ha **lo stesso hash del corpo completo** della precedente richiesta isolata originale del run 39996906771. Quella volta P(sì) era .67/.51; ora è .54/.48. Cambiano quindi i valori e la decisione sul negativo anche senza cambiare alcun byte di input, contesto o numero di domande. È un'osservazione di variazione fra due chiamate, non una stima statistica del rumore o la diagnosi del meccanismo interno.

Mono→color: il positivo sale di .14 e il negativo di .03; il margine cresce di .11. Color→color_legend: il positivo sale di .02, il negativo di .05; il margine cala di .03. Tutte le versioni ordinano il positivo sopra il negativo, ma il recupero del margine non equivale a un rifiuto corretto del negativo.

Il Brier è inferiore con i colori soli (.18125 contro .22100): l'aumento della probabilità sul positivo compensa, nella media di questi due casi, il piccolo incremento sul negativo. Non si omette questo dato favorevole, ma non lo si presenta come calibrazione o miglioramento affidabile. Alla soglia fissata il negativo a .51 resta un falso positivo. La legenda non recupera quel caso e lo porta a .56. Una sola chiamata per variante non separa questi spostamenti dalla variabilità osservata sul replay identico.

## Presentazione controllata

I tre lati originali hanno colori distinti per identità: AB ambra, BC blu, CA verde acqua. I tre vertici originali hanno colori stabili per punto. Entrambi i nuovi carrier sono viola ed entrambi i nuovi punti di contatto sono magenta. I colori dipendono da identità o tipo di elemento, mai dal riferimento positivo/negativo o dalla soddisfazione dell'obiettivo. Non si colorano le risposte giuste/sbagliate e non si riempiono regioni.

Le lettere rimangono scure e uguali. Canvas 320×320, coordinate, linee da 3 px, punti di raggio 3 px, font, dimensione e posizione delle etichette sono identici. I test verificano la stessa maschera dei pixel diversi dal bianco: soltanto i valori RGB dell'inchiostro cambiano. Il renderer monocromatico riproduce i pixel storici.

Il confronto color→color_legend usa **PNG pixel-identici e gli stessi file**, aggiungendo soltanto la legenda testuale. La legenda elenca tutti e tre i lati originali, tutti e cinque i punti visibili e i due nuovi carrier con i rispettivi ID già presenti. Un colore condiviso non fonde materiali distinti di candidati alternativi. Nessuna nuova appartenenza di punti a lati, ciclo, frazione/intervallo di copertura, risposta o verdetto di utilità viene aggiunto.

## Portata dell'esito

Il colore può rendere gli oggetti più distinguibili per chi guarda, ma questo test misura la risposta alla specifica richiesta sul lato intatto con immagini e state strutturato insieme. Non misura separatamente il riconoscimento dei colori o il binding visivo di ogni ID. Non possiamo affermare che Jev abbia usato, ignorato o interpretato correttamente la legenda internamente.

La coppia è stata preselezionata perché aveva prodotto errori; c'è una sola palette e una sola risposta per condizione. Non è una verifica generale su nuove figure né una misura di calibrazione. Il negativo resta formalmente ammissibile per entrambi i GS e manca soltanto lo specifico requisito dell'obiettivo. Nessuna prova geometrica, scoperta autonoma di Generic Spaces, estrazione autonoma dai pixel o ragionamento sequenziale interno viene dimostrato.

## Esecuzione e audit

- Branch `codex/right-pair-color-binding`, derivato da `e9ed7abd22bda84bc6d77bd4f2bdf033452fb4b8`; `main` e tutti gli esperimenti precedenti preservati.
- Pipeline live: **176 test e build riusciti**. Tre richieste esclusivamente da GitHub Actions con jev-1.14.0, secret del repository e header TypeSafe-Danger-Zone-Images: true. Il baseline è un replay sperimentale intenzionale; nessuna richiesta è stata ripetuta automaticamente per riparare un risultato.
- Audit offline: tre richieste ricostruite, sei risposte native verificate, 12 controlli dei contratti materiali e sei riferimenti verificati. Replay monocromatico esatto, soli PNG modificati in color, stessa immagine con/senza legenda, solo legenda aggiunta nel terzo state. Hash dei corpi e byte PNG congelati esatti.
- Sei PNG unici (tre mono, tre colorati), riutilizzati nei nove riquadri del viewer. Fixture manifest con palette e legenda fissate prima del live. Nessuna etichetta di risposta nelle immagini model-visible.
- Usage: **10,561 input token e 126 output token**. Total_tokens non restituito e lasciato null; nessuna confidenza separata o affidabilità numerica restituita, campi null. Noul è la probabilità nativa di sì. Nessuna chiave o corpo d'errore negli artifact, nessun errore API.

`live_results.json` conserva i sei giudizi effettivi. Il viewer offline mostra le immagini colorate e il confronto con il nuovo replay monocromatico; la legenda inviata a Jev è ispezionabile separatamente. Nessuna soglia o palette è stata modificata dopo i risultati.
