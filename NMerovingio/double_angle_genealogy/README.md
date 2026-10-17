# Panoptikon v1.1 — Genealogia delle due coppie di angoli

## Ipotesi concettuale

Due Mental Spaces possono rappresentare **due settori angolari al vertice** generati da una bisettrice e **due angoli retti alla base** generati da una perpendicolare.

I due angoli retti sono uguali **fra loro**, così come le due metà dell'angolo al vertice sono uguali **fra loro**. Gli angoli retti **non** sono in generale uguali agli angoli al vertice! La nostra ipotesi riguarda corrispondenze di ruoli e partizioni left/right, non uguaglianze incrociate di misura.

In un triangolo isoscele con apice sulla mediatrice, bisettrice e perpendicolare coincidono fisicamente: le due coppie di angoli possono essere reinterpretate come strutture prodotte da un unico segmento CD. In un triangolo scaleno, la bisettrice CE e la perpendicolare CH sono due segmenti diversi: un'**analogia astratta** fra due partizioni binarie rimane plausibile, ma non il legame forte attraverso lo stesso carrier.

## Due genealogie della stessa figura finale

- **Apex-first:** emerge prima lo spazio dei due angoli alla sommità; successivamente quello dei due angoli retti al piede.
- **Base-first:** emerge prima la coppia dei retti; successivamente la coppia degli angoli al vertice.

Il motore conserva origine, sequenza, verifiche, coincidenza dei carrier e il Generic Space candidato. **L'ultima figura è identica** nelle due storie; soltanto la prima comparsa degli spazi e la provenienza divergono.

## Esperimento controllato

- 2 triangoli isosceli con diversa altezza (figure condivise dalle due genealogie).
- 2 controlli scaleni nei quali la coincidenza del carrier è falsa.
- **24 chiamate Jev 1.14**: condizioni final-only, history-aware e inversione dell'ordine di presentazione degli eventi; diagramma semplice non annotato o sole informazioni simboliche (nessun diagramma).
- Tre domande per ogni chiamata:
  1. `noul`: le due coppie sono organizzate fisicamente sullo stesso segmento?
  2. `noul`: esiste davvero uguaglianza metrica incrociata fra angoli al vertice e angoli retti? (controllo falso).
  3. `choice`: quale interpretazione sarebbe più interessante esplorare? (nessuna risposta oggettivamente unica).

Ogni richiesta è indipendente e non include il verdetto dell'oracolo. Le valutazioni geometriche sono svolte separatamente in Python. Nel caso genealogia finale la rappresentazione è identica per entrambe le storie; invertire l'ordine degli elementi **nella lista** senza invertire gli indici temporali è un controllo di recency bias.

**Attenzione:** l'uso della parola 'corrispondenza' è volutamente distinto da congruenza e somiglianza metrica. L'eventuale scelta di Jev per la corrispondenza con carrier condiviso è una priorità cognitiva, non un nuovo teorema.

## Limiti metodologici

La grammatica dei Mental Spaces viene costruita deterministicamente; Jev valuta e priorizza interpretazioni, non le inventa. Le parole 'bisettrice' e 'perpendicolare' nella storia possono influenzare direttamente la selezione per semplice priming semantico. I controlli con ordine di presentazione e genealogia omessa aiutano ma non eliminano questo problema. Con soli due triangoli isosceli non possiamo inferire una legge generale. In una prossima versione, usare descrizioni di operatori anonimi e più famiglie geometriche.

## Esecuzione

Workflow: `.github/workflows/panoptikon-double-angle-v11.yml`.

Il secret GitHub Actions `TYPESAFE_API_KEY` è letto esclusivamente nel passo API. Il codice non registra né stampa la chiave.

Il report `output/jev_double_angle_results.json` include distribuzioni, probabilità, uso token; `output/double_angle_geometry.json` contiene verifiche e genealogie. Entrambi sono pubblicati negli artifact.
