# Score sulle classi certificate: confronto con i singoli bridge

Valutare direttamente le classi recupera quattro insiemi utili su sei, contro tre su sei degli Score individuali archiviati. La media aritmetica dei vecchi Score dentro ciascuna classe recupera però gli stessi quattro casi, senza nuove chiamate. Questa prova non mostra un vantaggio aggiuntivo della valutazione JEV per classe rispetto all'aggregazione già disponibile in codice.

Fonte: [Actions 39943364725](https://github.com/clarismetaverse/merovingio/actions/runs/39943364725), commit live `531ec29c3eaac95bfa8b175b948b93a94b7b33f5`, branch `codex/equivalence-class-relevance`. Completati 124 test offline, build standard e audit in pipeline. Sei chiamate da quattro domande, 24 nuovi Score; modello richiesto e restituito `jev-1.14.0`. Nessun errore API, retry o domanda di riparazione. I 36 Score del confronto provengono esclusivamente dal precedente run 39940956209 e non sono stati rieseguiti.

## Due classi fisse, obiettivi invariati

Il codice raggruppa i due tagli dai vertici della base del triangolo isoscele, collegati dalla riflessione della stessa figura ospite. Il taglio dall'apice è una classe singola. La partizione viene costruita usando isometrie e verifiche dei due contratti materiali storici, senza consultare utilità, risposte attese, vecchi Score o gruppi preferiti. Si controlla inoltre l'invarianza dei riferimenti attivi sotto lo scambio degli estremi della base per questi tre obiettivi noti e congelati.

Le stesse due classi compaiono in tutti i casi. Nell'obiettivo di decomposizione senza ancoraggio sono entrambe utili ed equivalenti rispetto allo scopo: le classi isometriche sono una partizione più fine di quell'equivalenza funzionale. Non si costruisce una singola classe all-useful che risolva preventivamente il confronto. Per ogni presentazione solo active_objective cambia; classi, domande, ordine, immagini e fatti rimangono fissi. Fra le due presentazioni sono controbilanciate le posizioni delle classi e l'ordine dei due membri.

Sono riusati esattamente gli stati e gli obiettivi archiviati, i livelli descrittivi, i carrier, le regioni, le metriche, i Mental Spaces e i Generic Spaces. Le otto immagini sono congelate e verificate byte per byte. L'intervento consiste nell'aggiunta delle classi certificate e nelle domande riferite alla classe, invece che al bridge. Il modello non riceve utilità, cardinalità attese degli insiemi, graduatorie o Score storici. La cardinalità della classe non dà un premio.

Un solo Score per classe e asse viene propagato dal codice a tutti i membri. **L'uguaglianza interna alla classe è quindi garantita dal codice, non riconosciuta autonomamente da JEV.** Il vero confronto di equivalenza del modello riguarda le due classi nell'obiettivo aperto.

## Risultati sugli stessi obiettivi

Il composito resta 0,5 Mental Spaces e 0,5 Generic Spaces, dopo normalizzazione per tre. La policy invariata conserva ogni classe con score almeno 2/3 e distante non più di 0,10 dal massimo, quindi espande le classi selezionate a tutti i membri. Sono ammessi insiemi vuoti e multipli.

| Obiettivo | Vecchi Score individuali | Media dei vecchi Score per classe | Nuovi Score JEV per classe |
| --- | ---: | ---: | ---: |
| Conservare un lato intatto: due bridge utili | 0/2 | 0/2 | 0/2 |
| Decomposizione senza ancoraggio: tre bridge utili | 1/2 | 2/2 | 2/2 |
| Sottofigure scambiabili: solo il taglio dall'apice | 2/2 | 2/2 | 2/2 |
| Totale degli insiemi esatti | 3/6 | 4/6 | 4/6 |

L'unico caso recuperato rispetto ai singoli Score è la decomposizione aperta nella presentazione trasformata, recuperata anche dalla semplice media. Non ci sono casi esatti nuovi esclusivi rispetto alla baseline aggregata.

| Lettura dei nuovi Score | Risultato |
| --- | ---: |
| Equivalenza fra le due classi nel caso aperto, entro fascia 0,10 | 2/2 |
| Preferenze strette fra classi col segno corretto | 2/4 |
| Preferenze strette con margine oltre 0,10 | 2/4 |
| Appartenenze corrette / aggiunte errate / omissioni dopo espansione | 10 / 2 / 2 |
| Insiemi erroneamente ridotti a un solo membro nei casi multipli | 1/4 |

Le due preferenze corrette sono il controllo selettivo delle sottofigure scambiabili. Sul lato da conservare la classe meno pertinente ottiene un punteggio superiore in entrambe le presentazioni. Non è solo un problema della fascia: anche l'ordine fra classi è invertito.

## Punteggi e baseline aritmetica

P indica la classe dei due tagli dalla base; S il singolo taglio dall'apice. Sono nomi di lettura per l'audit, non label di risposta nelle immagini. I compositi sono normalizzati e qui arrotondati a tre decimali; gli originali sono conservati nel JSON.

| Presentazione | Obiettivo | JEV classe P | JEV classe S | Media vecchia P | Media vecchia S | Classi selezionate da JEV |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Originale | Lato intatto | 0,753 | 0,785 | 0,770 | 0,743 | P e S, attesa P |
| Ruotata/riflessa | Lato intatto | 0,637 | 0,672 | 0,724 | 0,668 | S, attesa P |
| Originale | Senza ancoraggio | 0,872 | 0,908 | 0,881 | 0,918 | P e S, corretto |
| Ruotata/riflessa | Senza ancoraggio | 0,743 | 0,805 | 0,766 | 0,830 | P e S, corretto |
| Originale | Sottofigure scambiabili | 0,475 | 0,943 | 0,422 | 0,955 | S, corretto |
| Ruotata/riflessa | Sottofigure scambiabili | 0,487 | 0,870 | 0,439 | 0,877 | S, corretto |

Nel caso del lato intatto originale vengono inclusi tutti e tre i bridge. In quello trasformato P scende sotto il livello minimo e viene selezionato soltanto il bridge meno pertinente S, perdendo entrambi i membri utili. La media storica assegna invece P sopra S in entrambi i casi, ma con margini troppo piccoli per escludere S con la stessa fascia. Quindi anch'essa fallisce l'insieme esatto, pur mantenendo tutti i membri utili.

| Policy | Appartenenze utili mantenute | Aggiunte errate | Membri utili omessi |
| --- | ---: | ---: | ---: |
| Vecchi Score individuali | 10 | 2 | 2 |
| Media storica per classe | 12 | 2 | 0 |
| Nuovi Score per classe | 10 | 2 | 2 |

Anche la parità 4/6 nasconde dunque una differenza: sui membri la nuova valutazione per classe non migliora la media aritmetica e ne omette due. I due assi separati producono entrambi quattro insiemi esatti su sei; scegliere un asse a posteriori non risolve il lato da conservare.

## Sensibilità e interpretazione

Con le tre fasce previste prima della prova, i nuovi Score danno 3/6 insiemi esatti a 0,05, 4/6 a 0,10 e 4/6 a 0,15. Il caso aperto ha scarti fra classi di 0,037 e 0,062, entrambi nella fascia principale; quella più stretta ne esclude una nella presentazione trasformata. Non sono stati cambiati pesi, soglie, aggregazioni o Score nativi per migliorare il risultato.

Il raggruppamento rende coerenti i membri per costruzione e in questo test permette di mantenere le due classi nel compito aperto. Non risolve però la pertinenza rispetto allo scopo del lato intatto. Non emerge un valore aggiunto osservato delle nuove chiamate sulle classi rispetto alla media degli Score già disponibili. Non si può attribuire il problema a un particolare meccanismo interno: interpretazione dello scopo e composizione delle relazioni rimangono da distinguere.

Il confronto è storico, non un esperimento contemporaneo randomizzato fra unità individuali e classi. Cambiano insieme membership visibile e istruzioni dell'unità. Sono solo due presentazioni correlate di una figura e tre obiettivi espliciti; i risultati non stimano una capacità generale né dimostrano utilità matematica aperta, creatività, scoperta autonoma di Generic Spaces, estrazione dai pixel o prova geometrica.

## Usage e audit

Le 24 nuove risposte dichiarano 30.759 token input e 408 output, contro 31.341 input e 600 output delle 36 risposte individuali archiviate: un terzo di domande in meno ma circa l'1,9% di input in meno. La membership e i certificati aumentano lo state comune; il numero di domande da solo non misura il costo. La media storica per classe non ha generato alcun nuovo consumo API.

Confidenza media dichiarata 0,411; 0,420 per Mental Spaces e 0,402 per Generic Spaces. Affidabilità numerica e total_tokens non forniti, conservati null. Deviazione massima delle probabilità arrotondate dalla somma uno 0,01; scarto massimo fra score e attesa delle probabilità 0,02. Nessun dato è rinormalizzato o sostituito.

Audit indipendente di tutte le sei richieste, 24 Score, immagini congelate esatte, 36 controlli materiali ripetuti, sei ricostruzioni delle partizioni isometriche, due gruppi di controfattuali e di entrambe le baseline. Gli hash registrati restano esatti; per la sola ricostruzione scalare da sorgente si conserva la tolleranza 1e-12 già documentata. Il viewer e il pacchetto contengono matrici, Score separati, espansione ai membri, valori storici, protocollo e provenienza.

Solo Actions usa TYPESAFE_API_KEY secret e TypeSafe-Danger-Zone-Images: true. Nessun long context, chiave esposta o risposta grezza d'errore. Branch dedicato, main e v0.9/v1.0 preservati. Le immagini sono alternative prospettiche e non attestano ragionamento sequenziale interno.
