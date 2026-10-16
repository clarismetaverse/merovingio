# Jev Vision v0.4 — test scaleno

Questo test valuta se Jev sa discriminare **ruoli di costruzione** e non solo simmetria visiva.

- Due triangoli scaleni con vertice a sinistra/destra.
- Cinque ceviane candidate: bisettrice, mediana, altezza, due scelte generiche.
- Quattro contesti per ciascuna figura: esplorazione libera, divisione angolare, divisione metrica della base, ortogonalità.
- Identità delle candidate randomizzate a ogni trial; immagini in bianco e nero.
- Le condizioni guidate hanno una risposta verificabile con calcoli geometrici; la ricerca libera **non ha una soluzione unica**.
- Il prompt NON contiene I.10, teoremi, dimostrazioni, nomi delle candidate o etichette dell'opzione corretta.
- Il secret `TYPESAFE_API_KEY` viene usato soltanto dal runner GitHub Actions; il risultato pubblicato non contiene credenziali.

Esegui il workflow `.github/workflows/jev-scalene-stress.yml`, poi consulta il file `scalene_results.json` negli artifact.

Un match nelle condizioni guidate dimostra soltanto *role-conditioned visual selection*, non capacità autonoma di dimostrazione.
