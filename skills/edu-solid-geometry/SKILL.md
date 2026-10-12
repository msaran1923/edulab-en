---
name: edu-solid-geometry
description: >-
  Turns one solid geometry problem into a self-contained interactive lesson web page:
  left side MathJax step-by-step solution, right side Three.js interactive 3D model
  (step highlighting + camera switches). Supports three entry points — given text problem,
  random problem generation, or image upload for recognition then solving. Covers cubes/cuboids,
  pyramids/prisms, cylinders/cones with line-plane angles, dihedral angles, skew line angles,
  point-to-plane distances, volumes, etc. Unified "coordinate system + vector method", driven by
  exact sympy computation (answer, 3D coordinates, step values all consistent). Other agents can
  also call this skill to generate such pages.
  Trigger words: solid geometry, line-plane angle, dihedral angle, angle between skew lines,
  distance to plane, regular square pyramid, cube angle, solve this geometry problem,
  random solid geometry problem, solid geometry in this image; interactive geometry solution page.
---

# Solid Geometry Problem → Interactive Web Page

## What this skill produces
A single HTML page that opens directly in the browser: left side problem/answer/step-by-step solution (MathJax formulas),
right side corresponding 3D model (Three.js, rotatable/zoomable, step highlighting of key elements and camera switches).
Matches the structure of `template/lesson.html`.

## Dependencies (important)
Compute core `lib/geometry_kernel.py` depends on **sympy**. Before running scripts, confirm a `python3` that can import sympy:
`python3 -c "import sympy"`.

**When missing**: If import fails (sympy or any later library), **first ask the user if they want to install**, then install after consent
(`python3 -m pip install <package>`), or switch to an interpreter that already has it; **do not install without asking**.
All `python3` below refers to an interpreter that can run the dependencies.

## Workflow

### Step 1: Obtain the problem spec (unify three entry points)
Organize the problem into a structured spec (format in `references/problem-schema.md`): solid type and dimensions,
given construction points/conditions, requested type and objects, **language**.
- **Text problem**: extract directly.
- **Image**: use vision to extract, and **echo the recognized problem back to the user for confirmation** (statement/solid/dimensions/requested/language) before continuing.
- **Random problem**: choose solid and type, use kernel with random parameters, re-roll if answer is not clean.

> **Output language follows prompt language**: English prompt → English page, etc. Record `language` in the spec.

### Step 2: Exact computation with the kernel (do not calculate by hand)
Follow coordinate conventions and solution recipes in `references/conventions.md`, call `lib/geometry_kernel.py`:
get exact coordinates, key vectors, normals, final answer, and intermediate values for each step (all as LaTeX strings).
Three.js coordinates of vertices via `kernel.to_three(points, scale)`.

You can verify the kernel from the command line first:
```bash
python3 lib/geometry_kernel.py    # built-in sample self-check
```

### Step 3: Assemble lesson data and inject into template

> 📍 **Output location (important)**: Finished HTML is always written to the **user's current working directory (`Path.cwd()`)**, unless the user explicitly specifies a path.
> **Never** write into the skill's own directory (`skills/edu-solid-geometry/output/` etc.) — that is the skill's internal development sample directory.
> Temporary build scripts also go to cwd or a temp directory (e.g. `/tmp`), and can be deleted after use.

Write a **temporary build script** that imports kernel, bodies, generate, assembles `lesson` / `steps` / `model` data
(schema in `references/problem-schema.md`), then calls `generate.render_html(data, out)` to inject the template and produce HTML.
`out` uses an **absolute path under cwd**:

```python
from pathlib import Path
out = Path.cwd() / "solution-<short-description>.html"   # lands in user's current directory, not the skill directory
generate.render_html(data, out)
```

- All numerical values in `steps[*].content` **directly reference kernel results**; the model only organizes the explanatory text (written in the target language).
- `model.points` use results from `kernel.to_three(...)`; `model.spheres`/`edges` use topology from `lib/bodies.py`
  (`quad_pyramid` / `tri_pyramid` / `cuboid` / `cube` / `prism`), rare solids can have edges written by hand.
- Each step has `highlight` (absolute set of visible elements for that step) and `cameraPos`.
- **When the problem gives segment lengths**: add a `measure` element for the corresponding edge (`label` in LaTeX, e.g. `2\sqrt{2}`),
  and put it in the `highlight` of the "establish coordinate system / list known conditions" step, marking the length in the 3D figure (see problem-schema).
- For English output, fill `lesson.ui` with English copy and set `lesson.language="en"`.

**Directly referenceable examples**: `build_data()` (regular square pyramid · line-plane angle),
`build_cube_data()` (cube · line-plane angle), `build_box_volume_data()` (cuboid · volume) in `scripts/generate.py` are complete templates — adapt them.

`generate.py` can directly output registered problems; **when no path is passed it defaults to the current working directory (cwd)**, or you can explicitly give a filename under cwd
(using the skill directory's `scripts/generate.py`, output lands in cwd):
```bash
python3 <skill-dir>/scripts/generate.py cube ./cube.html
python3 <skill-dir>/scripts/generate.py box  ./box.html
```

**Random problems**: `generate.py random <seed> [output.html]`, internally uses `kernel.is_clean(...)` to judge if the answer is clean, re-rolls if not:
```bash
python3 <skill-dir>/scripts/generate.py random 7 ./random.html   # no path defaults to ./random.html (cwd)
```
When extending random problem types, follow "random parameters → solve → re-roll if not is_clean".

### Step 4: Self-check (corresponding to correctness plan)
- kernel answer == answer card `answerValue` == final value shown in the last step (generate.py has assert examples).
- 3D vertex coordinates come from `kernel.to_three` (same source as the solution).
- Start a local static server (serving the **directory of the output file**, i.e. cwd) and preview-check: no console errors, formulas render correctly, step highlighting/camera matches expectations.
  (When developing inside the skill repo, `.claude/launch.json`'s `geom-preview` can be used; elsewhere start a temporary static server on cwd.)

> ⚠️ **Must close any ports/services you opened**: Immediately stop the local server after the preview check, **never leave processes occupying ports**.
> - Opened with preview tool: call `preview_stop` right after checking (pass the corresponding serverId).
> - Direct `http.server`: `kill` it when done, or check `lsof -nP -iTCP:<port> -sTCP:LISTEN` to confirm released.
> - Before delivery, confirm the port is released, then tell the user the result. Opening without closing = incomplete self-check.

### Step 5: Delivery
The finished product is written in the **user's current working directory (cwd)**, named like `solution-<short-description>.html`, tell the user the (cwd) path, can be opened directly in the browser.
Before delivery confirm: **(1)** finished product is in cwd, not in the skill directory; **(2)** no local services/ports left open from this preview.

## Extension
- **Add problem types**: Add solving functions in `geometry_kernel.py` (see conventions recipe table), add a `build_*` in `generate.py`.
- **Add solids**: Add coordinate construction functions in `geometry_kernel.py`, add edge topology in `bodies.py`.

## Directory
- `template/lesson.html` — data-driven template (generic 3D renderer + data island `__LESSON_DATA__`)
- `lib/geometry_kernel.py` — sympy exact computation core
- `lib/bodies.py` — solid edge topology library
- `scripts/generate.py` — template injection + example build functions
- `references/problem-schema.md` — data format
- `references/conventions.md` — coordinate conventions, solution recipes, self-check
