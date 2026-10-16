# Jev Vision v0.5 — bisettrice versus mediana (pairwise)

Test isolato della capacità di Jev di selezionare la costruzione che divide un angolo in **due angoli uguali**, a parità di figura scalena e con due sole opzioni visive.

## Metodo

- Due triangoli scaleni (apice a sinistra e a destra).
- Due candidate per figura: congiungente dall'apice al punto di divisione **angolare** e congiungente dall'apice al **punto medio** della base.
- Due ordini delle immagini per figura (K1/K2 invertiti) → **quattro chiamate live**.
- Colore, tratto e marcatori identici; nessuna etichetta di costruzione o proposizione nelle immagini inviate.
- Non chiediamo di dimostrare Euclide I.10, non mostriamo una proof trace e non forniamo il frame LAL.
- L'oracolo di correttezza deriva dal calcolo indipendente della differenza tra gli angoli in C.

Jev riceve il focus sullo spazio mentale angolare; senza questo riferimento non c'è un'unica costruzione "migliore" in senso assoluto.

## Esecuzione

Il workflow `.github/workflows/jev-pairwise-v05.yml` parte sul branch sperimentale e usa il secret GitHub Actions `TYPESAFE_API_KEY`. Scaricare `pairwise_results.json` dagli artifact. Non riportare chiavi nei log.

## Interpretazione

4/4 indica riconoscimento nel test binario su due figure e due ordini, **non** capacità generale di proof search. Un fallimento suggerisce confusione tra divisione di un angolo e divisione di un segmento, oppure problemi di attenzione visiva o di formato dell'input. Serve un benchmark più ampio e controls prima di concludere.

I test locali verificano la geometria, la randomizzazione della posizione e la mancanza di leakage nei campi testuali.
