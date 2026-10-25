# Merovingio v9 · Attrazione competitiva dei frame LAL e LLL

## Ipotesi sperimentale

Continuando la v8, non moltiplichiamo le forme geometriche. La stessa costruzione prospettica (TRIANGLE × DIVISION → due sottotriangoli) viene interpretata attraverso **due possibili frame di congruenza**, LAL (lato–angolo–lato; SAS) e LLL (lato–lato–lato; SSS).

I frame sono entrambi presenti in memoria dall'inizio e contengono tre *slot relazionali astratti*. La competizione dipende dall'evidenza realmente disponibile, dal completamento dei ruoli e da una prior categoriale eventualmente concorrente. La scelta cognitiva NON è di per sé una certificazione.

## Premesse della proposizione I.10

L'equilatero ABC dà AC = BC, prima di tracciare CD. Una volta costruita la bisettrice da C, i due sottotriangoli ACD e BCD forniscono anche:

- CD = CD, il segmento materiale comune.
- ∠ACD = ∠DCB, uguaglianza garantita dalla costruzione; è proprio l'angolo COMPRESO fra le due coppie di lati uguali.

Il frame LAL è quindi completo con 3/3 witness.

Il frame LLL resta a 2/3 perché richiederebbe AD=DB come terzo witness: proprio la relazione che I.10 intende dimostrare. **Non è ammesso importare un candidato analogico come premessa verificata**.

La condizione controfattuale inserisce invece esplicitamente AD=DB come nuova premessa, per mostrare che LLL può legittimamente diventare completo e vincere la competizione se è favorito: questo esperimento NON equivale alla dimostrazione originaria.

## Implementazione

- Riusa la v8 per costruire la bisettrice: il workspace materiale precedente contiene soltanto il triangolo, l'obiettivo e un blend prospettico non ancora realizzato.
- La corrispondenza fra i due nuovi triangoli deriva dal carrier costruito e dal confronto delle nuove facce, senza istanze LAL/LLL hard-coded su AD/CD.
- I due frame astratti hanno liste distinte di tre prerequisiti; il motore riempie i binding dai **witness** con provenienza:
  - uguaglianza dei lati originali: dato dell'equilatero / isoscele;
  - lato condiviso: identità del segmento materiale;
  - uguaglianza degli angoli compresi: conseguenza data dalla bisettrice;
  - uguaglianza delle due porzioni della base: assente salvo la condizione controfattuale.
- L'ordine in cui la memoria cognitiva ispeziona il lato comune e l'angolo compreso è randomizzato con seed. I punteggi dei due frame vengono aggiornati in ogni fase e sono separati dai prerequisiti strettamente verificati.
- Un piccolo verificatore SAS controlla separatamente il posizionamento dell'angolo fra i due lati corrispondenti; solo se LAL è completo può certificare AD=DB mediante quella regola.
- Il verificatore non viene influenzato dal frame scelto per preferenza cognitiva. Può identificare un certificato SAS valido anche in una simulazione che ha preferito provvisoriamente LLL.

## Condizioni confrontate

1. balanced: prior uniformi fra frame.
2. LLL_initially_favored: LLL attraente prima della costruzione, ma non autorizzato ad assumere la conclusione.
3. without_prospection: elimina la disposizione prospettica v8; la costruzione resta identica.
4. angle_witness_masked: la lettura cognitiva non vede temporaneamente l'uguaglianza fra i settori; nessuna prova per LAL senza quel witness.
5. counterfactual_base_given: introduce come premessa indipendente l'uguaglianza segmentale, e la segnala chiaramente come aggiunta NON appartenente a I.10.

Geometrie: triangolo equilatero, triangolo isoscele non equilatero, triangolo scaleno. Nell'equilatero si varia il vertice da dividere. Per gli altri casi si prende il vertice C. La condizione controfattuale è esclusa dallo scaleno per non imporre una premessa incompatibile con la geometria costruita.

## Misure ed epistemologia

Disponibilità delle relazioni a ogni fase, cambiamento della probabilità di selezione del frame, quote di scelte LAL/LLL, completamento delle condizioni LAL/LLL, certificati SAS validi, nessun utilizzo circolare della conclusione come premessa.

I coefficienti di attenzione sono **progettati** per lo studio e NON rappresentano una validazione della cognizione umana. La scelta di frame è distinta dalla verifica deduttiva. Questo test studia come si comporta il software progettato con questi vincoli, non come Euclide abbia storicamente trovato la dimostrazione.

## Esecuzione

    python -m unittest discover -s NMerovingio/experiments/congruence_frame_v9 -p 'test_*.py' -v
    python NMerovingio/experiments/congruence_frame_v9/frame_competition.py --seeds 48
    python NMerovingio/experiments/congruence_frame_v9/viewer.py

Artifacts: results/traces.json, results/aggregates.json, results/REPORT.md, results/viewer.html.
