---
name: edu-analytic-geometry
description: >-
  Turns one analytic geometry (conic sections) problem into a self-contained interactive lesson web page: left panel shows the problem statement + dynamic console (a variable parameter slider drives live recalculation of geometric quantities + theoretical range / fixed-value indicator), middle panel shows KaTeX step-by-step solution, right panel shows a 2D Canvas dynamic geometry board (ellipse/hyperbola/parabola/circle + moving line/point + vectors + labels + drawing tools). Supports three entry points — given text problem, random problem, or image upload for recognition then solving. Covers standard equations, chord length, vector dot-product range/fixed value, triangle-area extremum, fixed point, fixed value (slope product), locus, eccentricity, etc. Unified method of "parametrized line x=my+c + system + Vieta + substitution", driven by exact sympy computation (answer, coordinates, step values, and the interactive engine's theoretical range all share the same source). Other agents can also call this skill to generate such pages. Parallel in form to edu-solid-geometry, but uses Canvas-2D + KaTeX (not Three.js).
  Trigger words: analytic geometry, conic sections, ellipse, hyperbola, parabola, line and conic, focal chord, chord length, dot product range, vector dot product, fixed point, fixed value, slope product, triangle area maximum, locus equation, eccentricity, solve this analytic geometry problem, random conic problem, analytic geometry in this image; interactive analytic geometry solution page.
---

# Analytic Geometry Problem → Interactive Web Page

## What this skill produces
A single HTML page that opens directly in the browser (three columns):
- **Left column**: problem statement + dynamic console — a variable parameter slider (e.g. line inclination angle θ / moving point parameter t) drives live recalculation of geometric quantities (intersection coordinates, slopes, dot products, chord lengths, areas…), plus a "theoretical range bar" or "fixed-value indicator".
- **Middle column**: step-by-step solution (formulas with **KaTeX**), which can be collapsed with one click to give more space to the board.
- **Right column**: 2D Canvas dynamic geometry board (conic + moving line/point + vectors + point labels + grid axes), with an overlaid drawing/doodle toolbar.

## Dependencies (important)
The compute core `lib/analytic_kernel.py` depends on **sympy**. Before running scripts, confirm a `python3` that can import sympy: `python3 -c "import sympy"`.

**When missing**: If import fails (sympy or any later library), **first ask the user if they want to install**, then install after consent (`python3 -m pip install <package>`) or switch to an interpreter that already has it; **do not install without asking**.
All `python3` below refers to an interpreter that can run the dependencies.

## Workflow

### Step 1: Obtain the problem spec (unify three entry points)
Organize the problem into a structured spec (curve type and parameters, given points/conditions, requested type and objects, language).
- **Text problem**: extract directly.
- **Image**: use vision to extract, and **echo the recognized problem back to the user for confirmation** (statement/curve/parameters/requested/language) before continuing.
- **Random problem**: choose curve + problem type, random parameters → kernel solve, use `analytic_kernel.is_clean(...)` to judge if the answer is clean; re-roll if not.

> **Output language follows prompt language**: English prompt → English page, etc. Record `language` in the spec.

### Step 2: Exact computation with the kernel (do not calculate by hand)
Follow the solution recipes in `references/conventions.md`, call `lib/analytic_kernel.py` and `lib/conics.py`:
- `conics.ellipse/hyperbola/parabola/circle(...)` yields the curve object (exact a,b,c, foci, vertices, directrices, asymptotes, `eq_latex`, and the `board` dict for the frontend engine).
- `chord_setup(conic, through)` sets up the system of the parametrized line `x=my+c` to obtain the quadratic in y + Vieta quantities (exact).
- Target quantities: `dot_product_expr` / `chord_len_sq_expr` / `triangle_area_expr` / `slope_product_central` …
- Range: `range_over_m(expr, horizontal_valid=?)` — **includes open/closed endpoint decision** (critical correctness point, see below).
- Fixed value: `is_constant_in_m(expr)`.

You can self-check the kernel from the command line:
```bash
python3 lib/analytic_kernel.py      # built-in assertion self-check for flagship problems
```

> ⚠️ **Open/closed endpoints = correctness critical**: For a chord through a focus, both the horizontal line (x-axis, θ=0) and the vertical line (θ=90) are valid lines; the endpoints they attain must be included. Example: ellipse MA·MB problem, x-axis attains −3, vertical line attains 7/4, so the answer is the **closed interval** `[-3, 7/4]` (many textbooks wrongly write the open `(-3, 7/4]`). `range_over_m` decides accordingly, and the answer matches the interactive tool — drag the slider to 0° and you read exactly −3. For a parabolic focal chord the "axial direction" is a degenerate line (intersects at only one point); its limiting endpoint is not counted (`horizontal_valid=False` or restrict the param range).

### Step 3: Assemble data and inject into the template

> 📍 **Output location & sole deliverable (most important)**: The **only** thing delivered to the user is one `.html` file, written to the **current working directory (`Path.cwd()`)** (unless the user explicitly specifies a path). **Do not leave any other files** in cwd — build scripts (`.py`), `__pycache__`, self-check screenshots (`.png`), temporary files are **not deliverables**; put them in `/tmp` or delete them after use.
> Also **never** write into the skill's own directory (`skills/edu-analytic-geometry/output/` is the skill's internal sample directory).

Write the "assemble data + inject template" **build script into a temporary directory** (e.g. `/tmp/ag_build.py`), and make it **write only the `.html` to cwd**; the script assembles `lesson` / `steps` / `board` data (schema in `references/problem-schema.md`), calls `generate.render_html(data, out)` to inject `template/board.html`, **then delete the script**:

```python
# Build script goes in /tmp (not cwd): /tmp/ag_build.py
import sys; sys.dont_write_bytecode = True            # do not generate __pycache__
sys.path.insert(0, "<skill-dir>/scripts")
import generate
from pathlib import Path
data = {"lesson": {...}, "steps": [...], "board": {...}}
out = Path.cwd() / "solution-<short-description>.html"   # sole deliverable, lands in user's current directory
generate.render_html(data, out)
```

```bash
python3 -B /tmp/ag_build.py && rm -f /tmp/ag_build.py   # -B no bytecode; delete temp script after run, cwd has only .html
```

- Numerical values in `steps[*].content` **directly reference kernel results** (use `K.tex(...)` for LaTeX); the model only organizes the explanatory text (in the target language).
- `board` uses the curve `board` dict from the kernel, exact point coordinates, `param`, `derived` construction sequence, `readouts`, `rangeBar` (range problems) / `constant` (fixed-value problems) / `answerBand` (**shape-parameter problems**, e.g. eccentricity range).
- **Shape-parameter problems (slider = eccentricity e, etc.)**: When the natural dynamic quantity is the shape of the curve itself rather than a moving line/point, let the slider = that parameter, write the curve's `a/b/c`, foci, and moving-point coordinates as **expression strings** of `@param` (the engine redraws the curve/foci/asymptotes every frame), pair with a `status` readout showing inequality state, and `answerBand` highlighting the answer interval on the parameter axis. See conventions "shape-parameter problems".
- **Directly copyable examples**: The 6 `build_*` in `scripts/generate.py` cover the various interaction paradigms:
  `ellipse_dot_range` (range bar), `ellipse_chord_range`, `ellipse_area_max`,
  `ellipse_slopeprod_const` (fixed value · central symmetry), `parabola_dot_const` (fixed value · parabola),
  `hyperbola_ecc_range` (**shape parameter**: slider=e, curve redraws + `status` + `answerBand`).

Registered problems can be generated directly (`-B` no bytecode; no path defaults to skill output — when delivering to the user always change to a `.html` under cwd):
```bash
python3 -B scripts/generate.py list                      # list problem types
python3 -B scripts/generate.py ellipse_dot_range ./sol.html
python3 -B scripts/generate.py all ./out_dir             # all types
```

### Step 4: Self-check (correctness plan)
- kernel answer == answer card `lesson.answer` == final value shown in the last step == **JS standard-position / sweep-segment recalculated value**, all four consistent (`assert` already present inside `build_*`).
- `rangeBar` endpoints come from the kernel's `range_over_m`; `constant` value comes from the kernel's fixed value.
- Start a local static server (serving the **directory of the output file**, i.e. cwd) and preview-check: no console errors, KaTeX renders correctly, slider live recalculation is correct, range bar / fixed value / fixed point / locus behavior matches, drawing tools and collapse panel work.
  (When developing inside the skill repo, `.claude/launch.json`'s `ag-preview` can be used, port 4601; elsewhere start a temporary static server on cwd.)
- **Self-check screenshots are only for you**: the preview tool returns the image directly, **do not save `.png` to cwd**; the local static server is read-only and produces no files. Any temporary files produced by the self-check (build script `.py`, screenshots `.png`, `__pycache__`, etc.) must be cleaned up before delivery.

> ⚠️ **Must close any ports/services you opened**: Immediately stop the local server after the preview, **never leave processes occupying ports**.
> - Opened with preview tool: `preview_stop` (pass serverId).
> - Direct `http.server`: `kill` it when done, or check `lsof -nP -iTCP:<port> -sTCP:LISTEN` to confirm released.
> - Before delivery confirm the port is released, then tell the user. Opening without closing = incomplete self-check.

### Step 5: Delivery
The finished product is written in the **user's current working directory (cwd)**, named like `solution-<short-description>.html`, tell the user the path, can be opened directly in the browser.
Before delivery confirm: **(1)** finished product is in cwd, not in the skill directory; **(2)** no local services/ports left open from this preview; **(3)** cwd has **only this one new `.html`** — no `.py` / `.png` / `__pycache__` / temporary files (check with `git status` or `ls` and delete if present).

## Extension
- **Add problem types**: Add target-quantity functions in `analytic_kernel.py` (written as expressions in m) + reuse `range_over_m` / `is_constant_in_m`; add a `build_*` in `generate.py`, choosing an interaction paradigm (range bar / fixed value / fixed point / locus trace / shape-parameter answerBand). See the recipe table in `references/conventions.md`.
- **Add curves**: `conics.py` already has ellipse/hyperbola/parabola/circle; the frontend `board.html` engine already supports four types of rendering, asymptotes, and directrix directions. Add one copy in each place for a new curve.
- **Add interactive constructions**: The `buildScene` switch in `board.html` is the construction library (`line_through_angle`, `intersect_line_conic`, `point_on_conic`, `point_reflect`, `tangent_at`, `foot_perp`…); extend as needed and register in the schema document.

## Directory
- `template/board.html` — data-driven template (generic 2D renderer + parameter engine + data island `__LESSON_DATA__`)
- `lib/conics.py` — conic sympy definition library (special points / LaTeX / board dict)
- `lib/analytic_kernel.py` — sympy exact solver core (system · Vieta · range · fixed value)
- `scripts/generate.py` — template injection + 5 build_* examples + batch/single problem generation
- `references/problem-schema.md` — data format (board engine schema)
- `references/conventions.md` — standard forms, solution recipe table, Vieta/substitution routines, open/closed endpoints, self-check
