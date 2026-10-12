# Explainer animation design (read before writing storyboard.md and anim.js)

## Goal: the figure "explains the problem", not a gradually filled illustration

Bad practice (has happened): the figure is drawn completely once, then each sentence only adds a line or a label, and all explanation lives on the right board. Viewers can only stare at the board; the figure is just background. `render.mjs motion` marks such sentences as `STATIC` / `POP`.

Good practice: **for every narration line, the figure has an action that "acts out" that reasoning**. When you say "CD equals half of AB", slide a copy of CD onto DA and DB until they coincide; when you say "arc length divided by radius gives the central angle", roll the radius along the arc; when you say "back to the space figure", rotate the top view back into the 3D view. The board only records the conclusions.

## Four actions per narration line: point → move → leave → link

| | What | How |
|---|---|---|
| **Point** | The element mentioned by the narration lights up; irrelevant elements fade | `glow(pts, col, bump(lt, at(k, f)))` draws a highlighter under the segment; `grp(0.3, ...)` draws secondary elements; intro uses `hiBox` |
| **Move** | One action that embodies the reasoning, 0.6–1.5 s, finished in the middle of the sentence | See the action table below: `slideSeg`, `movePoly`, `camTween`, moving point, `countTo`, growing auxiliary line… |
| **Leave** | After the action, leave a mark that later sentences can refer to | `rightM` right angle, `tickM` equal length, `paraM` parallel, `angM` angle, numeric labels, translucent fill |
| **Link** | Formulas on the board and quantities on the figure use **the same color**; for complex cases use a `callout` arrow from the figure to the board line | Given quantities blue, sought/answer red, auxiliary/conclusion green, emphasis yellow |

Do **one main action** per sentence. Multiple actions crammed into one sentence are hard to follow.

## Action table: reasoning → animation

| Reasoning / statement | Action on the figure | Code |
|---|---|---|
| Given an edge or a quantity | The edge glows once, the number pops | `glow` + `bump`; `txt(..., {pop: P(...)})` |
| Take a midpoint / a point | A point slides along the segment and stops there, then equal-length marks appear | `mix2(A, M, eio(P(...)))` + `dot`; `tickM` |
| Draw an auxiliary line | A dashed line "grows" from the start | `draw([P, Q], {dash: [12, 10], p: P(...)})` |
| Two segments equal | A copy of one translates + rotates onto the other until they coincide | `slideSeg(a, b, c, d, eio(P(...)))` |
| Two lines parallel | A copy of one translates onto the other; then draw parallel marks | `slideSeg` + `paraM` |
| Two angles equal (alternate / corresponding) | An angle arc + colored sector is copied and moved onto the other angle | `angM` drawn on the three points after `movePoly` |
| Perpendicular | Right-angle mark is drawn, segment glows | `rightM` |
| Congruent | A colored copy of a triangle translates/rotates (flip if needed) onto the other | `fillPts(movePoly(tri, dx, dy, rot))` |
| Similar / midline | Small triangle colored, scaled by k and overlaid on the large one (or vice versa) | `movePoly(tri, dx, dy, 0, k)` |
| Pythagoras / area | Squares or area blocks on the sides are colored and counted; for dissection, move the area blocks | `fillPts` + `movePoly` + `countTo` |
| Find a length | The line glows from one end to the other, the number counts from 0 to the result | `glow(pts, col, 1)` with `draw(..., {p})`; `countTo(0, v, e, 1)` |
| Central angle / arc length | The arc grows along the circumference while the radius sweeps | `ellPts` + `draw({p})`; radius endpoint `[cx + r cos a, cy + r sin a]`, a changes with time |
| Cone lateral area / net | Lateral surface cut along a generatrix and unfolded into a sector (see code below) | `unrollCone` recipe |
| Line-plane perpendicular, projection | A dashed line "drops" from the point to the base, right-angle mark appears at the foot | `L3(P, foot, {dash, p})` + `rightM(pr(...))` |
| Solid → base top view | **The same 3D model** rotates the camera to directly above; do not hard-switch to another picture | `camTween({pitch: .52, yaw: .2}, {pitch: PI / 2, yaw: 0}, e)` |
| Parallel planes | Two planes colored translucent, a copy of one translates onto the other | `fillPts` for the four plane points; 3D points use `mix3` translation |
| Line in plane / moving point | Point moves back and forth on the segment, related lines follow, properties preserved (colors and marks stay) | `const u = 0.5 + 0.5 * Math.sin(...)` or `eio(P(...))` |
| Function monotonicity / extremum | Moving point travels along the graph, readout `(x, y)` updates; stops and flashes at the extremum | `fnPts` + `ax.S` + `countTo` |
| Parameter change | Graph deforms with the parameter (parameter value written beside and counted) | Recompute `fnPts` each frame with the interpolated parameter |
| Inequality / range | Corresponding interval colored on the number line or graph, endpoints hollow/solid | `fillPts` + `circ` |
| Motion / pursuit | "Problem time" drives character movement, clock and distance readouts update live | `token` + `countTo`; position = distance function(time) |
| Set up equation / algebraic manipulation | Corresponding quantity on the figure glows and is written in the same color on the board; when moving a term, the text slides from left to right and changes sign | `txt` position uses `lerp` |
| Case discussion | Same figure shows two cases: switch sequentially, or small figures side by side | `grp` fade in/out / `scaleAt` shrink |
| Check | Substitute the answer back: numbers on the figure update to the answer, property marks (parallel, equal) light up | `countTo` + `bump` |

## Two complete examples (learn from these)
- `template/` (anim.js + storyboard.md): plane geometry. Segment copies slide to prove equality, circumcircle, extend to rectangle, diagonal rotates to coincide, number counting.
- `examples/cone-parallel/`: solid geometry. Projection (P drops to O, PA is pressed onto AO), two segments of OA cover PA, lateral surface unfolds into a semicircle, same model rotates to top view, 60° sector rotates half a turn around the midpoint of OC (alternate interior angles), △AOQ scales up to △APB (midline), plane QOC translates along OB into plane PBD, moving point T.
  Usage: when the new problem is solid geometry, copy the `cone()` / `camTween` / `unrollCone` patterns from this example instead of writing from scratch.

## Easy to gloss over (motion check cannot catch these; you must guard them yourself)
- **Just making a line flash does not count as "move".** glow/bump is "point". If the storyboard "move" only writes glow/flash/highlight/appear, `--check` will reject it.
- **Calculation scenes also need actions on the figure**:
  - "Substitute the known number" → the corresponding numeric label on the figure flies into the formula on the board: `flyText('2', position_of_2_on_figure, blPos(1, 180), eio(P(at(0, 0.2), 1.0)))`
  - "Find BC = 10" → the number beside BC counts from 0 to 10 (`countTo`), while BC glows from one end to the other
  - "Ratio AD/AB = DE/BC" → the sides of the small triangle scale and land on the corresponding sides of the large triangle (`slideSeg`), appearing in same-color pairs
- **Every object in the problem must be drawn.** Before writing the storyboard, list the "figure inventory": all points, segments, parallel/perpendicular relations, given lengths. When checking screenshots, verify item by item. Missing a drawing (e.g. the problem says DE∥BC but DE is not drawn) is a serious error, worse than a mediocre animation.
- Point positions must match the data: AD = 2, DB = 3 → D is at 2/5 of AB; parallel lines must actually be parallel. Compute coordinates with `mix2(A, B, 2 / 5)`, do not eyeball.

## Common patterns

```js
SC.key = (lt, S) => {
  const { P, at } = S;
  // Point: this sentence (sentence 0) mentions CD → highlighter under CD flashes; bump goes 0→1→0 within 1.2 s after at(0)
  glow([Cp, Dp], C.red, bump(lt, at(0)));
  // Secondary elements fade: during the "move", draw the rest at 0.3 opacity
  const focus = P(at(0, 0.15), 0.4) * (1 - P(at(1), 0.4));
  grp(1 - 0.7 * focus, () => drawRest());
  // Move: copy of CD rotates onto DA (eio makes it slow-fast-slow)
  slideSeg(Cp, Dp, Dp, Ap, eio(P(at(0, 0.25), 1.0)));
  // Leave: draw equal-length marks after the action
  tickM(Dp, Ap, 1, C.red, P(at(0, 0.6), 0.4));
  // Link: same color on the board
  bl(1, 'CD = DA = DB', at(0, 0.5), lt, { c: C.red });
};
```

**Solid ↔ top view (continuous transition)**
```js
const e = eio(P(at(0), 1.5));                        // Entering this scene: 1.5 s rotate to top view
camTween({ pitch: 0.52, yaw: 0.2, s: 160 }, { pitch: PI / 2, yaw: 0, s: 220 }, e);
cone(st);                                            // Same drawing function; in top view z is ignored, base circle is a true circle
```
When leaving the top view, reverse `camTween(top, oblique, eio(P(at(k), 1.5)))`.

**Cone lateral surface unfolds into a sector (unrollCone recipe)**: generatrix length l, base radius r, unfolded sector central angle = 2πr / l.
```js
// e: 0 = solid cone lateral surface, 1 = plane sector; apex2D is the sector center on screen, Ls is the generatrix length on screen
function unrollCone(e, apex2D, Ls, r, l, col = C.blue) {
  const n = 60, theta = 2 * PI * r / l, pts3 = [], pts2 = [];
  for (let i = 0; i <= n; i++) {
    const a = i / n * 2 * PI;                                    // point on base circumference (3D)
    pts3.push(pr([r * Math.cos(a), r * Math.sin(a), 0]));
    const b = -PI / 2 - theta / 2 + theta * i / n;               // corresponding point on sector arc (2D)
    pts2.push([apex2D[0] + Ls * Math.cos(b), apex2D[1] + Ls * Math.sin(b)]);
  }
  const rim = tween(pts3, pts2, e), top = mix2(pr(G.P), apex2D, e);
  fillPts([top, ...rim], col, 0.15);
  draw(rim, { c: col, w: 4 }); draw([top, rim[0]], { c: col, w: 4 }); draw([top, rim[n]], { c: col, w: 4 });
}
```
(Schematic is fine: the intermediate process does not need to be a strict geometric unfolding; viewers understand "cut open — flatten".)

**Moving point preserves properties**
```js
const u = 0.5 + 0.45 * Math.sin(PI * 2 * P(at(5), S.dur(5)));   // one back-and-forth in this sentence
const T = mix3(G.O, G.C, u);
L3(G.Q, T, { c: C.red, w: 6 });                                  // QT follows
glow([pr(G.Q), pr(T)], C.red, 0.6);                              // always inside the colored region of plane QOC
```

## Layout and pacing
- The figure occupies the left half and is as large as possible (leave room for labels); when two views are needed, use `camTween` or `scaleAt` transitions, do not cram two pictures together.
- At the start of each scene, continue from the end state of the previous scene (same drawing function, parameters set to 1), then begin the new actions of this scene.
- Place actions between 15% and 80% of the sentence: the beginning is for "point", the end for "leave".
- Do not change the meaning of colors used within the same scene.
- When emphasizing the answer: `stamp` a seal + glow the corresponding elements on the figure.

## storyboard.md (must be written before anim.js)

Format see `template/storyboard.md`: one row per sentence, `| scene_id sentence_no | narration point | point | move | leave | board |`.
- Except for the first scene (read the problem) and the last scene (review), **every row's "move" must be filled**, and it must be an action from the table above, not words that only mean appearance such as "show", "appear", "mark" (appearance can go in "leave").
- At least one sentence per scene must have a continuous motion in "move" (slide, rotate, translate, unfold, camera rotate, moving point, number counting).
- `build_audio.py --check` checks that every sentence has a row and that "move" is not empty.

After writing anim.js, `node render.mjs motion` automatically checks:
- `STATIC`: the figure has no change at all in this sentence → must fix (add a glow/bump point, or add an action).
- `POP`: something only appeared → acceptable, but every scene must have at least one `MOVE`.
- `MOVE`: the figure is moving throughout this sentence.
The report is in `build/motion_report.txt`; exit code is 1 if it fails. For sentences that truly do not need motion (rare), list them in `episode.json` under `"static_ok": ["scene_id sentence_no"]` and explain the reason on delivery.
