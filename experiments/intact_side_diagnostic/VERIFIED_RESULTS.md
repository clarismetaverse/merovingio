# Controllo sul lato intatto: risultato verificato

**La formulazione esplicita basta a correggere entrambi i casi negativi di questo piccolo controllo.** La copertura certificata mantiene tutte le risposte corrette e rende le probabilità molto più separate. Non dimostra che tutti i precedenti errori di binding dipendessero dal testo.

Tre bridge individuali già verificati, due presentazioni archiviate dello stesso host, tre condizioni. Immagini, ID, ordine, Mental Spaces, Generic Spaces e fatti preesistenti invariati. Una domanda binaria nativa Noul per candidato/versione, tre per richiesta, **18 risposte in sei richieste**, senza Score o composito. Soglia fissata prima delle chiamate: p>.5 sì, p<.5 no; p=.5 astensione, contata errata.

| Versione | Corretti | TP | FN | TN | FP | Astensioni | Brier medio |
|---|---:|---:|---:|---:|---:|---:|---:|
| Testo attuale | 4/6 | 4 | 0 | 0 | 1 | 1 negativa | 0.166317 |
| Richiesta esplicita | 6/6 | 4 | 0 | 2 | 0 | 0 | 0.100500 |
| Esplicita + copertura certificata | 6/6 | 4 | 0 | 2 | 0 | 0 | 0.001050 |

“Sempre sì” darebbe 4/6: il baseline attuale non mostra una corretta discriminazione dei negativi. Esplicitare che il lato deve appartenere per intero al bordo di **UNA DELLE DUE NUOVE REGIONI**, e che la conservazione nell'host o l'unione di pezzi di regioni diverse non basta, corregge due giudizi senza peggiorarne altri. Aggiungere la tabella di copertura non cambia nessuna decisione a .5. I valori Noul diventano .97–.98 sui positivi e .04 sui negativi. Questa è maggiore separazione delle probabilità restituite in questo campione, non una calibrazione statistica o una confidenza indipendente.

| Presentazione | Candidato | Riferimento | P(sì), attuale | P(sì), esplicita | P(sì), copertura |
|---|---|---|---:|---:|---:|
| 0 | C897 | sì | .88 | .84 | .97 |
| 0 | C306 | no | .79 | .27 | .04 |
| 0 | C646 | sì | .94 | .84 | .97 |
| 1 | C843 | sì | .77 | .67 | .97 |
| 1 | C176 | sì | .77 | .56 | .98 |
| 1 | C415 | no | .50 | .42 | .04 |

La richiesta esplicita conserva anche giudizi vicini alla soglia (.56 e .42 nella presentazione 1). Non è quindi equivalente a una classificazione robusta su nuove figure. Il Brier è descrittivo; il campione non supporta una stima di calibrazione.

## Che cosa possiamo concludere

Questo esito è compatibile con un'ambiguità della formulazione precedente: “intact anchor” non specificava quanto esplicitamente il bordo della nuova sottofigura dovesse contenere tutto il lato. Non serve la tabella per arrivare a 6/6 qui. Non emerge un limite irriducibile nel confronto degli ID in questi sei giudizi, ma non abbiamo misurato il processo interno del modello né isolato tutte le possibili cause.

La copertura fornisce intenzionalmente le premesse geometriche mancanti in forma uniforme: per ogni candidato, per ogni regione e per tutti i lati originali. Nessun verdetto complessivo sul candidato viene inviato. Le risposte con tabella misurano l'applicazione della richiesta a fatti già forniti, non l'estrazione autonoma dai pixel. Tutte le condizioni mantengono le immagini: il test non separa capacità visiva e testuale pura.

Il confronto è fra tre formulazioni binarie nuove. I precedenti esperimenti usavano due assi Score, classi e politiche di selezione: non attribuiamo a questo controllo una dimostrazione causale che lo scoring nativo funzionasse male. Le due viste sono correlate e derivano da un unico host e tre tagli. Non generalizziamo ai 28 binding storici, alla scoperta libera di Generic Spaces o alla pertinenza matematica aperta.

## Esecuzione e audit

- Branch dedicato: `codex/intact-side-diagnostic`, derivato da `9b2590393b7b9672861bef4ac5719f9b51dd2456`. `main` e il lavoro precedente restano preservati.
- [Run iniziale 39946481728](https://github.com/clarismetaverse/merovingio/actions/runs/39946481728), commit `53fc9b76589606caca61214460d51e3d2d2685a0`: una richiesta, tre risposte coverage/presentazione 0, salvate prima di un errore del viewer sulle condizioni ancora vuote.
- [Ripresa completata 39946781738](https://github.com/clarismetaverse/merovingio/actions/runs/39946781738), commit `cf257d39b6af8ff1cc0fcea8c6d4173b5f1d54cf`: riusa quell'unica richiesta verificandone input/hash/risposte, esegue solo le cinque mancanti. Nessuna domanda ripetuta o risposta selezionata. Tutte le fasi, inclusa la build del viewer e 138 test, sono riuscite.
- Il runner registra per ogni richiesta il run/commit di effettiva esecuzione. La correzione riguarda solo reporting e ripresa; le domande e gli input del protocollo originario restano identici.
- Audit offline: sei richieste ricostruite, 18 Noul verificati, 36 righe di copertura ricalcolate, due triplette appaiate, hash di richieste e byte PNG esatti. Le sole somme rigenerate ammettono tolleranza 1e-12 per differenze Python 3.11/3.12; valori nativi e hash non vengono arrotondati o corretti.
- Usage complessivo delle sei richieste: **27,929 input token, 366 output token**; total_tokens non restituito, lasciato null. Nessun errore API. Affidabilità e confidenza separata non restituite, lasciate null. Noul normalmente non ha confidenza separata.
- Chiamate esclusivamente via Actions con secret del repository e header immagini abilitato. Nessuna chiave o corpo d'errore nei risultati.

`live_results.json` conserva i risultati sanificati effettivi. Il viewer offline mostra immagini e probabilità affiancate; protocollo, artifact e manifest permettono di ricostruire il confronto. Il problema del viewer non è un fallimento Jev: è documentato separatamente dall'esito empirico e ha richiesto una ripresa senza nuove domande.

Riferimento tecnico: [Noul nativo TypeSafe](https://docs.typesafe.ai/primitives/noul). Noul è probabilità di sì, non un punteggio di pertinenza. Non si ricavano prove geometriche né ragionamento sequenziale interno da questo esperimento.
