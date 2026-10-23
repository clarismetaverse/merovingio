# Gestalt Propagation v3 — costruzione polisemica e co-generazione porismatica

## Ipotesi da preservare

La costruzione non è un semplice "passo" della dimostrazione. Può comportarsi come un **dispositivo cognitivo polisemico**: un unico termine medio materiale (CD, con l'incidenza in D) rende visibili simultaneamente più registri di organizzazione (partizione di ∠ACB, partizione di AB, due triangoli con lato comune, nuove opposizioni fra angoli e lati). In analogia *funzionale* a un porisma, l'operazione dice più cose contemporaneamente e facilita il passaggio da una lettura all'altra. Non affermiamo che "porisma" fosse storicamente definito così.

La macro-tensione ANGLE SPACE ↔ SIDE SPACE non deve aspettare la stabilizzazione completa dei raggruppamenti: può **propagarsi verso i sottogruppi ancora in formazione**. La co-origine di due partizioni legate allo stesso gesto costruttivo genera una via addizionale di salienza, che torna a modificare la tensione macro. Non trattiamo la somiglianza fra bisettrice, mediana e perpendicolare come uguaglianza dei loro significati.

Il trasferimento cognitivamente cercato nel caso bisettrice è:

    angoli ∠ACD = ∠DCB  (relazione data dalla costruzione)
        ↓ opposizioni angolo-lato, termine medio, sottotriangoli
    segmenti AD = DB ? (ipotesi di slippage NON provata)

Nel triangolo scaleno tale uguaglianza delle porzioni della base è generalmente falsa. Una trasversale generica che non sia bisettrice continua a creare i due sottosistemi, ma non fornisce il dato sorgente di uguaglianza angolare.

## Differenza dalla v2

La v2 genera SEED / EXTEND / ALIGN da un grafo geometrico. La v3 mantiene tutti i candidati della v2 e introduce, via analisi del grafo materiale:

1. *PARTITION FAMILY*: individua relazioni PART_OF aventi un genitore e due figli nello stesso dominio.
2. *COMMON MEDIAL TERM*: identifica i punti di contatto condivisi dai due segmenti e il raggio comune ai due angoli; verifica l'esistenza del carrier materiale che unisce i due estremi.
3. *CO-GENERATION PACKET*: associa le partizioni ai triangoli adiacenti, ai due ruoli di opposizione angolo-lato, e alla relazione angolare data, se presente. Non contiene un esito metrico finale predeterminato.
4. *COFRAME codelet*: raggruppamento multi-dominio stabilizzato a partire dal pacchetto.
5. *REBASE codelet*: dopo COFRAME, tenta una lettura per opposizioni lato-angolo, individuando il *verso* del trasferimento solo se esiste una relazione sorgente di uguaglianza.
6. *GENEALOGY PRESSURE*: la discendenza condivisa dall'evento di costruzione aumenta la salienza di COFRAME/REBASE; i raggruppamenti restituiscono attivazione macro.

**Heat** è la temperatura della scelta stocastica; **activation** è la salienza che si diffonde. Il motore conserva entrambe e registra score, origine del punteggio, evento e genealogia dei sottogruppi.

## Ablazioni a grafi materialmente identici

| Condizione | Macro opp. | Co-origine come prior | Micro→macro |
|---|---|---|---|
| no_macro | no | no | no |
| macro_only | sì | no | no |
| cogeneration_only | no | sì | no |
| coupled | sì | sì | sì |
| genealogy_blinded | sì | no | sì |

La quinta condizione mantiene la figura e i gruppi disponibili, ma nasconde **solo il peso attribuito alla loro origine costruttiva**. È un controllo dell'utilità della genealogia, non un disegno diverso.

Tre geometrie: triangolo isoscele con bisettrice; scaleno con bisettrice; scaleno con trasversale arbitraria senza uguaglianza degli angoli. Quest'ultima deve ancora generare il pacchetto strutturale, ma non può autorizzare l'ipotesi di uguaglianza segmentale partendo dagli angoli.

## Epistemologia

Il sistema non conclude AD = DB e non applica LAL: anche se nel caso isoscele tale uguaglianza è dimostrabile, la proiezione analogica è **HYPOTHESIS_ONLY**. La co-generazione è un fatto sulla genealogia topologica delle partizioni; i Generic Spaces sono ipotesi di allineamento, non certificazioni metriche.

Questa è una simulazione esplicita dei principi teorici proposti, non uno studio della cognizione reale, né evidenza sul processo storico di scoperta di Euclide. Le primitive percettive, la grammatica, il ranking e il meccanismo di attivazione sono ancora definiti da noi. L'esperimento valuta se il software soddisfa le invarianti e quali differenze producono le ablazioni.

## Esecuzione

    python -m unittest discover -s NMerovingio/experiments/gestalt_heat_v3 -p 'test_*.py' -v
    python NMerovingio/experiments/gestalt_heat_v3/poristic.py --seeds 32 --budget 18
    python NMerovingio/experiments/gestalt_heat_v3/viewer.py

Output: results/traces.json, results/aggregates.json, results/REPORT.md, results/viewer.html. I fixture e la memoria precedenti rimangono invariati; si importano il grafo v2 e il generatore di geometria v1.

## Futuro

Trasferire questa stessa grammatica a **nuove costruzioni non prefigurate dal triangolo I.10** (una trasversale fra rette parallele, una perpendicolare che divide un angolo piatto, un quadrilatero con diagonale) e misurare se il codice scopre veri pacchetti di co-origine senza assumere i loro nomi. Successivamente, apprendere salienza e dinamica invece di fissarne manualmente i pesi.
