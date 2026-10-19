# Tabelle esplicite delle incidenze: risultati verificati

Il formato tabellare non risolve il binding materiale nel campione provato: 11/24 risposte corrette contro 12/24 del grafo ridotto. Jev supera tutti e quattro i controlli separati di identità letterale. Il risultato distingue il confronto elementare fra due stringhe mostrate dalla selezione di un binding che richiede recuperare e combinare riferimenti nel workspace; non identifica da solo il meccanismo interno dell'errore.

Fonte: [run Actions 39286026262](https://github.com/clarismetaverse/merovingio/actions/runs/39286026262), commit live `28fe93ad8aa253fcfe92ed7de63de2107abb35a2`, branch `codex/explicit-incidence-tables`, Jev `1.14.0`. Il job evaluate ha completato 89 test offline, build standard del viewer e 26 richieste live senza errori API: 48 risposte principali e quattro controlli, due domande per richiesta. La conclusione del job e l'artifact scaricato sono verificati direttamente.

## Confronto controllato

Stesse due repliche, sei casi, ID, contratti, domande, opzioni e immagini del precedente esperimento a contesto ridotto. Per ogni coppia cambia soltanto la rappresentazione degli stessi fatti: dizionario di oggetti oppure quattro tabelle con colonne e righe esplicite per punti, carrier, poligoni e usi di bordo. La trasformazione è reversibile: ricostruisce esattamente tutti gli oggetti, endpoint, cicli, ID materiali e usi originari. Nessun flag di uguaglianza, validità o risposta è aggiunto. L'ordine grafo/tabelle è bilanciato; i quattro controlli letterali sono in richieste separate, senza immagini o grafo.

| Misura | Grafo ridotto | Tabelle esplicite |
| --- | ---: | ---: |
| Risposte corrette | 12/24 | 11/24 |
| Binding validi riconosciuti | 4/8 | 7/8 |
| None corretti sui negativi | 8/16 | 4/16 |
| Binding invalidi accettati, inclusi positivi con alternativa errata | 8 | 13 |
| Astensioni errate sui positivi | 4 | 0 |
| Coppia base/identità distinta interamente corretta | 1/4 | 1/4 |

Le tabelle aumentano i positivi riconosciuti ma fanno accettare più alternative invalide. Su otto positivi selezionano sette binding corretti e uno sbagliato; sui sedici negativi accettano dodici binding invalidi. Rispondere sempre none darebbe 16/24: nessuno dei due formati costituisce una policy di binding affidabile.

| Caso | Grafo | Tabelle |
| --- | ---: | ---: |
| Caso base | 4/4 | 4/4 |
| Carrier coincidenti con ID materiali distinti | 1/4 | 1/4 |
| Uso parziale del carrier | 3/4 | 1/4 |
| Triangolo più quadrilatero | 2/4 | 2/4 |
| Figura ospite diversa | 2/4 | 3/4 |
| Binding valido escluso dalle opzioni | 0/4 | 0/4 |

L'aggregato triangolo/quadrilatero nasconde una completa inversione: il grafo rifiuta i due negativi ma manca i due positivi; le tabelle riconoscono i positivi e accettano entrambi i negativi. Nei 24 confronti appaiati, sette risposte sono corrette in entrambi i formati, quattro solo nelle tabelle, cinque solo nel grafo e otto errate in entrambi. La baseline grafo ripete esattamente le 24 scelte storiche: nessuna scelta cambiata rispetto alla precedente condizione relevant_state. Questo non misura né esclude caching lato fornitore.

## Cosa separano i quattro controlli

Per ciascuna replica sono confrontati due veri ID del workspace: una coppia S/S e una coppia S/T. Jev distingue correttamente tutte e quattro le coppie, con confidenza dichiarata 1. Nei problemi completi, invece, sbaglia tre dei quattro controesempi di carrier coincidenti in entrambi i formati.

Il campione non sostiene l'ipotesi semplice che Jev non sappia confrontare due stringhe esplicite. La difficoltà osservata emerge quando deve individuare i riferimenti pertinenti e applicare congiuntamente identità, uso completo, tipo di regione, ospite e scelta fra alternative. Il test non separa ancora recupero, integrazione dei vincoli e politica di risposta. Quattro controlli non dimostrano una capacità generale sugli ID; il mancato miglioramento non esclude ogni possibile rappresentazione tabellare. Raggruppamento, lunghezza e disposizione sono parte dello stesso intervento; le immagini restano presenti nei due formati principali.

Il passo diagnostico successivo consigliato è chiedere pochi recuperi atomici dei carrier usati dalle due regioni, seguiti dal confronto dei due ID recuperati, mantenendo questi stessi controesempi. Non è stato eseguito in questa prova. Per l'uso pratico resta necessario verificare in codice il binding materiale; tale verifica non corregge retroattivamente i conteggi nativi riportati qui.

## Usage e audit

| Richieste | Token input dichiarati | Token output dichiarati |
| --- | ---: | ---: |
| Grafo, 12 chiamate | 68.188 | 1.848 |
| Tabelle, 12 chiamate | 66.072 | 1.872 |
| Controlli ID, 2 chiamate | 1.152 | 194 |
| Totale, 26 chiamate | 135.412 | 3.914 |

Le tabelle riducono di circa il 3,1% i token input del confronto principale. Confidenza media dichiarata: grafo 0,557, tabelle 0,462, controlli 1; sulle 52 risposte 0,547. Affidabilità numerica e total_tokens non forniti, mantenuti null. Le probabilità native sommano a uno nei dati ricevuti, senza rinormalizzazione. La confidenza non è una misura di correttezza.

Audit indipendente: 26 hash delle richieste ricostruiti, 52 risposte typed verificate, dodici coppie appaiate, dodici conversioni tabella/grafo reversibili, tutte le immagini e 240 witness candidati ricontrollati; analisi e matrici ricalcolate dalle risposte. Dati sanitizzati, usage e immagini conservati nel viewer offline e nel pacchetto Library. Gli input non contengono gold, diagnosi del verificatore o risposte storiche. Live soltanto via Actions con TYPESAFE_API_KEY secret e TypeSafe-Danger-Zone-Images: true; nessun retry, long context o nuovo Score. Main, v0.9/v1.0 e gli esperimenti precedenti restano preservati.

È selezione fra witness finiti su fatti strutturali forniti, non estrazione visiva autonoma, prova geometrica o generazione libera di Generic Spaces. Più immagini non dimostrano ragionamento sequenziale interno.
