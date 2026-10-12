---
name: edu-chem-reaction
description: >-
  Turns one chemical reaction into a self-contained microscopic 3D interactive demonstration web page: left/top is a Three.js interactive molecular animation (drag the slider to watch bonds break · form · atoms recombine, with step highlighting), right is the KaTeX reaction equation + step-by-step explanation + atom conservation counter + optional energy–reaction-progress curve. Supports three entry points — given text reaction/equation, random problem, or image upload for recognition then demonstration. Covers combustion, combination/decomposition/displacement/double displacement, redox (electron transfer visualization), organic mechanisms (esterification etc. with catalyst · transition state). Unified exact drive by sympy: auto-balances the equation, validates atom conservation and atom map, derives which bonds break/form; answer and geometry share the same source. Built-in dual engines with automatic selection: morph (atom morphing, shows atom conservation) and mechanism (mechanism keyframes, shows catalysis/transition state). Hybrid geometry: default built-in VSEPR molecule library; if RDKit is installed it can generate conformers from SMILES (never installs automatically). Other agents can also call this skill to generate such pages. Parallel in form to edu-solid-geometry / edu-analytic-geometry, but uses Three.js + KaTeX to demonstrate molecular reactions.
  Trigger words: chemistry reaction, microscopic demonstration, molecular animation, combustion, methane combustion, hydrogen combustion, water electrolysis, redox, electron transfer, esterification, reaction mechanism, bond breaking and forming, atom conservation, mass conservation, chemical equation balancing, solve this chemical reaction, random chemical reaction, chemical reaction in this image; interactive chemistry reaction page.
---

# Chemical Reaction Microscopic Demonstration → Interactive Web Page

## What this skill produces
A single HTML page that opens directly in the browser: one side is the **3D molecular animation** corresponding to the reaction (Three.js, rotatable/zoomable, drag the "reaction progress" slider to watch frame-by-frame **chemical bonds break/form and atoms recombine**, with step highlighting + floating molecule labels), the other side is the **KaTeX reaction equation + step-by-step explanation + atom conservation counter**, and optionally an **energy–reaction-progress curve**, flame, catalyst protons, electron transfer overlays, etc. Matches the structure of `template/reaction.html`.

## Dependencies (important)
The compute core `lib/reaction_kernel.py` depends on **sympy** (for balancing). Before running scripts, confirm a `python3` that can import sympy: `python3 -c "import sympy"`.

**When missing**: If import fails (sympy or any later library), **first ask the user if they want to install**, then install after consent (`python3 -m pip install <package>`) or switch interpreters; **do not install without asking**.
**RDKit is optional**: if installed, hybrid geometry uses it to generate real conformers from SMILES; if not, the built-in VSEPR library is used — both work, and **this skill never automatically installs RDKit**.

## Workflow

### Step 1: Obtain the reaction spec (unify three entry points)
Organize the reaction into a structured spec (format in `references/problem-schema.md`): reactants/products, atom map or explicit atoms, conditions (ignition/electrification/catalysis/reversible), category, step-by-step explanation, **language**.
- **Text reaction/equation**: extract reactants and products directly, call the kernel to auto-balance.
- **Image**: use vision to extract the equation, and **echo the recognized reaction back to the user for confirmation** (equation/conditions/category/language) before continuing.
- **Random problem**: pick a reaction from the registry, or combine species within the library and balance with `balanced_coefficients`, use only if the answer is clean.

> **Output language follows prompt language**: English prompt → English page, etc. Record `meta.language` in the spec.

### Step 2: Exact computation with the kernel (do not calculate by hand)
Follow the modeling conventions in `references/conventions.md`, call `lib/reaction_kernel.py`:
- `balanced_coefficients(...)` uses sympy null space to **auto-balance** (equation coefficients are guaranteed);
- `assemble_data(spec)` expands molecule instances, **validates atom conservation and atom-map bijection**, **derives which bonds break/form (difference set)**, calculates each atom's world coordinates in reactant/product states, and produces the `data` to inject into the template.

You can self-check from the command line first:
```bash
python3 lib/reaction_kernel.py     # balancing + conservation + bond-diff self-check
python3 lib/molecules.py           # molecule library self-check
```

### Step 3: Write build_* to assemble spec and inject into template

> 📍 **Output location (important)**: Finished HTML is always written to the **user's current working directory (`Path.cwd()`)**, unless the user explicitly specifies a path.
> **Never** write into the skill's own directory (`skills/edu-chem-reaction/output/` etc.) — that is the skill's internal development sample directory.

Adapt the `build_*` in `scripts/generate.py`, then `render_html(K.assemble_data(spec), out)`:
```python
from pathlib import Path
out = Path.cwd() / "reaction-<short-description>.html"   # lands in user's current directory
render_html(K.assemble_data(spec), out)
```
**Examples (copy and adapt)**:
- `build_combustion_ch4` (methane combustion · morph · flame · energy) — high-level `species + atom_map` template;
- `build_redox_na_cl2` (sodium + chlorine · redox · electron transfer) — overlay `electrons`;
- `build_esterification` (esterification · mechanism · catalyst · transition state) — low-level `atoms + fragments + keyframes` template.

`generate.py` can directly output registered reactions; **no path defaults to cwd**:
```bash
python3 <skill-dir>/scripts/generate.py combustion_ch4 ./reaction.html
python3 <skill-dir>/scripts/generate.py list
```

### Step 4: Self-check (corresponding to correctness plan)
- sympy balancing coefficients == displayed equation coefficients == number of each molecule instance (`assert` already inside `assemble_data`).
- Atom map is a **bijection** between reactant ↔ product atoms, elements match; bond endpoints all exist (kernel has validated).
- Atom conservation counter is unchanged before and after the reaction (catalyst not counted).
- Start a local static server (serving the **directory of the output file**) and preview-check: no console errors, KaTeX equation renders correctly, bond break/form highlighting matches the step-by-step explanation when dragging the slider.

> ⚠️ **Must close any ports/services you opened**: Immediately stop the local server after the preview check, **never leave processes occupying ports**.
> Opened with preview tool: call `preview_stop` right after checking. Before delivery confirm the port is released, then tell the user the result.

### Step 5: Delivery
The finished product is written in the **user's current working directory (cwd)**, named like `reaction-<short-description>.html`, tell the user the path, can be opened directly in the browser.
Before delivery confirm: **(1)** finished product is in cwd, not in the skill directory; **(2)** no local services/ports left open from this preview.

## Dual engines and automatic selection
The template has one unified renderer with two per-frame position resolvers (sharing bond-diff drawing / labels / overlays / UI):
- **morph** (atom morphing): each atom interpolates from reactant state to product state, naturally showing **atom conservation/recombination**, suitable for any reaction.
- **mechanism** (mechanism keyframes): atoms belong to rigid fragments, move as a whole according to K0/K1/K2 keyframes, groups do not deform, suitable for **catalyst / transition state / leaving group** organic mechanisms.

`assemble_data` selects according to `meta.engine` (`auto`/`morph`/`mechanism`): when `auto`, category `organic` or presence of `fragments` selects mechanism, otherwise morph. Overlays are all data switches (see schema):
`flame` (combustion/strong exothermic), `catalyst` (catalyst protons + switch), `transitionGlow` (transition-state energy glow),
`electrons` (redox electron transfer), `energy` (energy–reaction-progress curve), atom conservation counter (on by default).

**Color scheme**: overall bright (textbook ball-and-stick style: atoms with dark outline + soft shadow + white panel), each reaction uses `meta.accent` to distinguish accent color (combustion amber, esterification indigo, sodium-chlorine violet…).

## Extension
- **Add reactions**: Add a `build_*` in `generate.py` (high-level `species+atom_map` or low-level `atoms+fragments`), register in `REGISTRY`.
- **Add molecules/ions**: Add an entry to `_LIBRARY_BUILDERS` in `lib/molecules.py` (VSEPR geometry + display metadata + internal bonds).
- **Add overlays**: Add an optional module driven by a `data` field in `template/reaction.html`.

## Directory
- `template/reaction.html` — data-driven template (unified renderer + dual engine + data island `__REACTION_DATA__`)
- `lib/molecules.py` — VSEPR ideal molecule geometry library (includes element table/colors/radii)
- `lib/reaction_kernel.py` — sympy balancing + conservation/map validation + bond-diff + scene assembly + optional RDKit probe
- `scripts/generate.py` — template injection + example build_* (includes REGISTRY and CLI)
- `references/problem-schema.md` — data format for reaction spec and data
- `references/conventions.md` — modeling conventions, engine selection, overlays, balancing and self-check
