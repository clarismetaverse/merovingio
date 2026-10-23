# Più bridge utili: equivalenze e pertinenza meno ovvia

Il risultato è parziale: con la policy fissata prima del test vengono recuperati esattamente tre insiemi utili su sei. JEV riconosce bene il controllo selettivo, ma non mantiene sempre le equivalenze previste né esclude tutte le alternative meno pertinenti. Evitare un vincitore unico è possibile nella policy; questo da solo non rende corretto l'insieme selezionato.

Fonte: [Actions 39940956209](https://github.com/clarismetaverse/merovingio/actions/runs/39940956209), commit live `f9ad26d332ae50e1d1ebf804ece343f965413f8b`, branch `codex/multi-bridge-relevance`, modello richiesto e restituito `jev-1.14.0`. Il run ha completato 111 test offline, build standard, sei richieste da sei Score e audit in pipeline. Sono 36 risposte native, senza errori API, retry o riparazioni a pagamento. Gli input e gli Score di questo run restano immutati.

## Obiettivi, equivalenze e verificatore

Tre mediane di un unico triangolo isoscele, in due presentazioni con rotazione/riflessione e alias/ordine diversi. Tutte passano entrambi i contratti locali dei Generic Spaces storici: due triangoli con carrier comune e carrier con più partecipazioni nella partizione dell'ospite. Il codice verifica identità, uso completo del bordo, contenimento, disgiunzione e partizione. Metriche e riflessioni sono calcolate dalla geometria esplicita, con tolleranze numeriche dichiarate.

Le trasformazioni del workspace aggiungono un carrier, due regioni e i rispettivi usi di bordo. La riflessione della figura ospite scambia i due tagli dai vertici della base; lascia invariato il taglio dall'apice, scambiandone le due regioni. È equivalenza di trasformazioni rispetto allo scopo, non fusione degli ID materiali.

| Obiettivo | Insieme utile di riferimento | Recupero esatto con la policy |
| --- | --- | ---: |
| Conservare tutto il lato designato in una sottofigura, senza preferire un estremo | Due tagli dai vertici della base | 0/2 |
| Organizzare due viste triangolari senza privilegiare vertice, lato, orientamento o dimensione | Tutti e tre i tagli | 1/2 |
| Scambiare le sottofigure mediante una simmetria dell'ospite, preservandone la forma metrica | Solo il taglio dall'apice | 2/2 |

Le tre mediane producono tutte aree uguali, ma solo quella dall'apice produce due sottofigure congruenti e scambiabili nella figura ospite. I due tagli dalla base sono riflessioni reciproche. Nel caso senza ancoraggio tutti e tre sono equivalenti soltanto sotto la politica strutturale dichiarata, che ignora le differenze metriche. La validità formale è identica; la pertinenza dipende dallo scopo.

Il caso con tre alternative utili è un controllo ampio, non un obiettivo semanticamente difficile. Quello selettivo riceve fatti metrici già certificati. Conservare un lato come riferimento richiede invece combinare lo scopo con le relazioni e i cicli delle regioni forniti. Gli errori non isolano interpretazione dello scopo, composizione delle evidenze e politica degli Score.

## Score nativi e insiemi, senza top-1 obbligatorio

Due Score descrittivi per candidato, su Mental Spaces e Generic Spaces. Sono due viste correlate. Ogni Score è conservato, diviso per tre e combinato con pesi prefissati 0,5/0,5. JEV non restituisce un insieme: il codice applica una policy dichiarata prima del run, mantenendo ogni candidato con score composito almeno 2/3 e distante al massimo delta=0,10 dal massimo. Insiemi vuoti e multipli sono ammessi. La tolleranza non è una prova statistica di equivalenza o una soglia calibrata per l'uso reale.

| Misura, con delta=0,10 | Risultato |
| --- | ---: |
| Insiemi della policy esattamente coincidenti col riferimento | 3/6 |
| Coppie equivalenti fra bridge utili entro la fascia | 5/8 |
| Tutte le coppie equivalenti, incluse due coppie di alternative inferiori | 6/10 |
| Preferenze strette col segno corretto | 7/8 |
| Preferenze strette con margine superiore alla fascia | 4/8 |
| Insiemi ridotti a un solo candidato nei quattro casi con più alternative utili | 0/4 |
| Appartenenze corrette / aggiunte errate / omissioni | 10 / 2 / 2 |

I quattro margini nettamente separati provengono tutti dal controllo selettivo. Sullo scopo meno ovvio del lato intatto, una preferenza su quattro è invertita e le altre hanno margini piccoli. Le graduatorie grezze hanno un massimo numerico unico in tutti e sei i casi; questo non è interpretato come obbligo di scegliere un solo elemento. La policy principale conserva più elementi in tutti i casi che li prevedono, ma può conservarne di sbagliati o perderne uno equivalente.

## Dove fallisce

Si indicano con K_A, K_B e K_C i tagli dai tre vertici canonici dell'audit; questi nomi non erano nelle immagini come etichette di risposta. Gli alias effettivi sono conservati nel viewer. Valori compositi normalizzati, arrotondati qui a tre decimali.

| Presentazione | Obiettivo | K_A | K_B | K_C | Insieme della policy | Riferimento |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Originale | Lato intatto | 0,718 | 0,822 | 0,743 | K_B, K_C | K_A, K_B |
| Ruotata/riflessa | Lato intatto | 0,687 | 0,762 | 0,668 | Tutti | K_A, K_B |
| Originale | Senza ancoraggio | 0,862 | 0,900 | 0,918 | Tutti | Tutti |
| Ruotata/riflessa | Senza ancoraggio | 0,833 | 0,698 | 0,830 | K_A, K_C | Tutti |
| Originale | Sottofigure scambiabili | 0,402 | 0,442 | 0,955 | K_C | K_C |
| Ruotata/riflessa | Sottofigure scambiabili | 0,497 | 0,382 | 0,877 | K_C | K_C |

Nel primo caso il taglio meno pertinente K_C supera K_A di 0,025 e K_A dista 0,103 dal massimo: una piccola differenza basta a escluderlo con la fascia principale. Nella seconda presentazione tutti e tre superano il livello minimo e rientrano nella fascia, includendo K_C senza giustificazione nello scopo dichiarato. Nell'obiettivo senza ancoraggio, K_B viene escluso nella presentazione trasformata pur essendo utile ed equivalente: il divario dal massimo è 0,135.

Entrambi gli assi separati producono lo stesso conteggio per obiettivo: 0/2, 1/2, 2/2. La difficoltà non viene risolta scegliendo a posteriori uno dei due assi al posto del composito.

## Sensibilità preregistrata

| Fascia delta | Insiemi esatti | Tutte le coppie equivalenti nella fascia | Riduzioni spurie a un solo candidato |
| --- | ---: | ---: | ---: |
| 0,05 | 2/6 | 4/10 | 2 |
| 0,10, principale | 3/6 | 6/10 | 0 |
| 0,15 | 4/6 | 10/10 | 0 |

Tutte e tre le fasce erano previste prima delle chiamate. La fascia più ampia tiene vicine tutte le equivalenze ma non risolve il lato intatto: include ancora tutti e tre i bridge in entrambe le presentazioni. Non viene quindi scelta dopo il test per dichiarare riuscita la prova. Una policy che selezionasse sempre tutto farebbe 2/6; un singolo vincitore obbligatorio non potrebbe recuperare nessuno dei quattro insiemi multipli.

## Interpretazione e prossimo passo possibile

Lo scoring può essere usato senza imporre top-1, ma le equivalenze verificate dal codice non sono rispettate stabilmente da Score indipendenti per candidato. Questo ridimensiona il segnale della precedente prova a obiettivi univoci: il buon risultato del controllo selettivo non basta per una prioritizzazione affidabile fra più alternative utili.

Un seguito possibile sarebbe presentare classi di equivalenza già certificate come unità di valutazione e confrontare classi rispetto allo scopo. Tale raggruppamento cambierebbe il compito e non correggerebbe retroattivamente gli Score qui osservati. Non è stato eseguito né applicato ai conteggi di questa prova.

Il test resta limitato a una figura sintetica, due presentazioni correlate, scopi espliciti e fatti strutturali/metrici già forniti. Il riferimento è una politica operativa del benchmark, senza giudizi indipendenti di utilità matematica. Non dimostra creatività, scoperta autonoma di Generic Spaces, prova geometrica, estrazione dai soli pixel o generalizzazione a Euclide.

## Usage e audit

Usage dichiarato: 31.341 input e 600 output. Confidenza media 0,464; 0,474 per Mental Spaces e 0,453 per Generic Spaces. Affidabilità numerica e total_tokens non forniti, conservati null. Le probabilità native arrotondate hanno deviazione massima dalla somma uno di 0,01; la differenza massima fra score e attesa delle probabilità è 0,03. Nessuno Score o distribuzione viene sostituito o rinormalizzato.

Verificati i sei hash delle richieste ricostruite dagli input registrati e dagli asset, tutte le 36 risposte, 36 controlli di contratto ripetuti, due gruppi di controfattuali con solo active_objective variabile, riflessioni, ordini parziali e matrici. L'audit Linux della pipeline è passato. Ricostruendo su Windows, un valore d'area differiva di 9,1e-13: il controllo locale inizialmente troppo stretto è stato corretto con tolleranze scalari relative e assolute 1e-12, mantenendo esatti hash registrati, stringhe, booleani e struttura. Un tredicesimo test controlla sia il roundoff ammesso sia il rifiuto di fatti metrici o tipi modificati. Gli input inviati e le risposte non sono cambiati e non sono state ripetute chiamate JEV.

Il branch conserva protocollo, risultati nativi sanitizzati, immagini, viewer offline, sorgenti e audit, con artifact in outputs e Library. Main e il lavoro precedente restano preservati. Solo Actions usa TYPESAFE_API_KEY secret e TypeSafe-Danger-Zone-Images: true. Più immagini qui sono alternative prospettiche, non una sequenza temporale né evidenza di ragionamento sequenziale interno.
