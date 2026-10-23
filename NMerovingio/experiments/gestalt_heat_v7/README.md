# Merovingio · v7 — Flat-angle construction and medial regrouping

## Obiettivo

Primo test di generalizzazione fuori dal triangolo I.10, senza modificare i pesi di produttività della v6: verificare se una costruzione (retta AB, punto d'incidenza O, nuova semiretta OC) induce due partizioni primitive in ANGLE SPACE e SIDE SPACE che un REBASE può collegare attraverso un Generic Space con origine costruttiva comune.

La rappresentazione contiene linee/semirette, settori angolari, segmenti e partizioni orientate PART_OF, ma **non** istanze di triangoli, criteri di congruenza o deduzioni metriche.

## Scene geometriche

- flat_ray (W1): OC divide l'angolo piatto superiore AOB; O divide il segmento AB in AO e OB. Entrambi i raggruppamenti hanno la stessa radice costruttiva EV:O:INCIDENCE.
- crossed_lines (W2): prolungando OC in OD emerge una seconda partizione dell'angolo piatto inferiore, con stessa discendenza mediale; nascono anche due coppie di angoli opposti al vertice. Queste opposizioni NON sono automaticamente relazioni metriche certificate.
- independent_partitions: il primo gruppo angolare nasce dall'incidenza in O sulla retta di supporto AB, ma la divisione segmentale appartiene a EF nel punto P (e JRK come seconda alternativa). Sono partizioni strutturalmente analoghe, ma non co-generate dallo stesso punto/evento.

Tutte le scene includono famiglie indipendenti/distrattrici per impedire un successo puramente deterministico.

## Grammatica v7

- PART_OF: orienta il rapporto figlio→genitore e conserva il root_event.
- PARTITION FAMILY: deriva runtime una coppia di elementi dello stesso dominio sotto un genitore, con ancoraggio geometrico inferito dal grafo.
- PROSPECTIVE GS: può collegare una famiglia ANGLE e una SIDE solo quando hanno una radice costruttiva e un ancoraggio materiale comuni.
- REBASE: cambia il fuoco ANGLE→SIDE o SIDE→ANGLE scegliendo stocasticamente una nuova partizione ancora inesplorata.
- PRODUCTIVITY: completare uno slot di un Generic Space riattiva i ruoli mancanti; soltanto un GS effettivamente istanziato emette feedback. Punteggi frozen della v6: +.19 primo binding, +1.08 completamento previsto, +.73 feedback slot mancante, .72 prior co-origine, temperatura .59.

Un GS completato non asserisce α=β, AO=OB, né un teorema sugli angoli opposti al vertice.

## Esperimento

Cinque condizioni sulle stesse figure e budget:

- fixed_initial: ordinamento iniziale congelato per ciascun dominio;
- topology_only: attivazione locale delle relazioni, nessuna genealogia, nessun macroconcept;
- predictive_only: produttività prospettica senza retroazione;
- productivity_feedback: produttività prevista più feedback dai GS che emergono;
- genealogy_blind: genealogia disattivata come prior e feedback genealogico attenuato, mantenendo stesse candidate e struttura.

Due condizioni di attenzione: clean e competing (prime iniziale di partizioni SIDE con un'altra origine costruttiva).

Per ciascun trial: 3 REBASE a partire da una lettura angolare in O, su tutti i tipi di scenario, con 32 seed. I controlli indipendenti NON devono generare generic mediali con falsa radice condivisa.

La v7 include un viewer offline che mostra i gruppi realmente selezionati e i Generic Spaces parziali/completi.

## Riprodurre

    python -m unittest discover -s NMerovingio/experiments/gestalt_heat_v7 -p 'test_*.py' -v
    python NMerovingio/experiments/gestalt_heat_v7/flat_angle.py --seeds 32 --budget 3
    python NMerovingio/experiments/gestalt_heat_v7/viewer.py

L'esperimento è un modello cognitivo ingegnerizzato con regole fissate a mano, **non** prova una teoria psicologica e non ricostruisce la scoperta storica di Euclide.
