# NMerovingio

A deliberately tiny research reasoner for Euclid Book I, restricted to the **isosceles workspace** and propositions **I.5, I.6, I.7, I.18, I.19**.

This introduction describes the existing executable prototype and its original experiment. The [Panoptikon v0.3 research specification](docs/Merovingio_Panoptikon_Fondamenti_v0_3.md) develops the cognitive process separately, including perception of the current graph, construction history and probabilistic grouping. Its I.10 fixture is illustrative and is not yet consumed by the engine.

The goal is not theorem proving by broad search. The goal is to test whether a reasoner can **generate useful analogies and disanalogies from a single stabilized Gestalt**, especially the counterfactual pattern made explicit by I.6.

## Core hypothesis

Use the isosceles triangle as a base Gestalt:

- equal sides <-> equal base angles
- a counterfactual is created by minimally breaking one correspondence
- preserved correspondences become epistemic contacts
- the break is run through the workspace until it propagates, closes coherently, or produces an incompatible Gestalt
- a stabilized counterfactual may become a new base case for later reasoning

The first target is not to reproduce Euclid's proofs verbatim. It is to reconstruct a **visual-inferential grammar** capable of rediscovering relations among I.5, I.6, I.7, I.18 and I.19.

## Allowed primitives

Construction / visual operators:

- `OVERLAY`
- `BREAK_SIDE_EQUALITY`
- `BREAK_ANGLE_EQUALITY`
- `PRESERVE_CONTACT`
- `EXTEND_COLLINEAR`
- `PART_WHOLE`
- `JOIN`
- `RUN`
- `ELIMINATE_INCOMPATIBLE`
- `STABILIZE`

The engine should prefer **minimal breaks**: preserve as much of the base mapping as possible and perturb exactly one relation first.

## Proposition roles

- **I.5**: forward equality pattern: equal sides -> equal base angles.
- **I.6**: counterfactual / converse pressure: equal base angles resist a side-inequality break.
- **I.7**: uniqueness / no-second-closure constraint for a fixed side configuration.
- **I.18**: propagate an ordered side disanalogy into an ordered opposite-angle disanalogy.
- **I.19**: propagate the ordered angle disanalogy back toward the opposite side; can be read as residual elimination once equality and reverse-order cases are blocked.

## Minimal experiment

1. Instantiate the isosceles base Gestalt.
2. Generate only two one-break counterfactuals:
   - one side becomes greater / smaller;
   - one base angle becomes greater / smaller.
3. Retrieve only proposition-patterns whose inferential role matches the active tension.
4. Run candidate continuations.
5. Record:
   - preserved contacts,
   - broken correspondences,
   - eliminated states,
   - newly inferred relations,
   - whether a new Gestalt stabilizes.
6. Do **not** inject a visual analogy to the target theorem.

## Research success criterion

A run is interesting when NMerovingio reaches a useful proposition path because the **inferential tension** of the counterfactual recalls a previous Gestalt, not because the target theorem or its diagram was supplied.

In particular, we want to observe paths such as:

`isosceles base -> minimal break -> counterfactual run -> contact with known equality/disquality regime -> elimination / propagation -> I.18 or I.19-like relation`

## Files

### Panoptikon v0.3 — processo cognitivo

- [Fondamenti v0.3](docs/Merovingio_Panoptikon_Fondamenti_v0_3.md) — spazi di premessa e conclusione, role binding ipotetico, apertura delle Gestalt e propagazione di plausibilità; §7.4 include `target_instantiation_line` e l'obiettivo dell'istanziazione.
- [Fixture cognitiva I.10 v0.3](tests/fixtures/Merovingio_I10_CognitiveProcess_Fixture_v0_3.yaml) — input W1 con alternative di binding, traccia illustrativa dei Generic Spaces e riferimento di certificazione distinto.

La costruzione, il grafo e la loro genealogia alimentano la scelta cognitiva. SAS può emergere come framing conclusivo; il controllo formale certifica la relazione proposta. Pesi delle bolle, regole di apertura/disassemblaggio e integrazione Jev restano da progettare. La fixture non va inviata integralmente al modello: `cognitive_input` è l'input iniziale, mentre le sezioni `*_do_not_submit` sono riferimenti d'autore per la valutazione.

La v0.3 rivede il nucleo cognitivo della v0.2 conservandone i file originali, senza modificare il reasoner o attestare esperimenti Jev.

Il §5.4bis segue anche la prosecuzione dalle partizioni in C e D: i Generic Spaces generati portano all'attenzione nuove domande e proposizioni, e possono orientare l'esplorazione oltre il goal iniziale.

### Panoptikon v0.2 — bridge planning

- [Fondamenti del modello teorico v0.2](docs/Merovingio_Panoptikon_Fondamenti_v0_2.md) — ontologia, BridgePotential e ranking congiunto Frame + Bridge + RoleMap; capitoli 5 e 7 per I.10.
- [Fixture I.10 pre-costruzione v0.2](tests/fixtures/Merovingio_I10_BridgePlanning_Fixture_v0_2.yaml) — stato W1, piano bisettrice + I.4/LAL, negativo circolare I.8/LLL e piano incompleto.

I due file conservano i contenuti della Library. La fixture è una specifica del testbed, non un test già eseguito dal motore: D e CD sono output proposti, e AD=DB va certificato solo dopo costruzione e verifica. Jev ordina i candidati; costruzione e certificazione restano deterministiche.

La v0.2 affianca [Panoptikon v0.1](PANOPTIKON_V01.md) e il suo [schema](graph/panoptikon_v0_1.json), senza sostituirli né cambiare la versione dell'architettura cognitiva.

Nomi equivalenti fra documento e fixture: I.4/LAL (`EUCLID_I_4_LAL`) = `EUCLID_I4_SAS`; I.8/LLL = `EUCLID_I8_SSS`; I.9 = `EUCLID_I9_ANGLE_BISECTOR`. Le uguaglianze AC=BC e AB=BC della fixture implicano AC=AB, riportata nello stato W1 del documento.

- `SPEC.md` — conceptual and computational contract.
- `data/propositions.json` — tiny proposition memory.
- `src/reasoner.py` — minimal executable prototype.
- `tests/test_reasoner.py` — sanity checks for counterfactual generation and proposition retrieval.
