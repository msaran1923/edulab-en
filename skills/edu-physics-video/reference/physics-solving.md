# Physics problem-solving method (must read for Step 1)

The quality ceiling of the explainer video = the quality of your solution. For math problems "getting the calculation right is enough"; for physics problems you must also **explain the model and the process clearly**. Students most often fail not on calculation, but on choosing the wrong object of study, missing a force, failing to segment the process, or not fixing the direction. The scene structure of the video should follow the solving flow below.

## 1. Standard six steps (write into the "solution card" at the top of storyboard.md)

| Step | Ask yourself | Write down |
|---|---|---|
| 1. Read and model | Who is the object of study (single body / system / isolate)? Idealizations (smooth, long enough, light string, point mass, small angle)? | Object, model name (incline, conveyor, block-slab, spring, circular motion, projectile, charged particle in a field, parallel glass block…) |
| 2. Segment the process | Where does the motion / state change abruptly (velocity zero, common velocity, leaves surface, collision, enters/exits field, friction reverses)? | Stage list ①②③, start and end conditions of each stage |
| 3. Force / state analysis | Each stage: gravity → normal force (contact surfaces) → friction (by direction of relative motion) → other forces (electric, magnetic, tension); optics: point of incidence, normal, interface | One force diagram per stage (magnitude and direction of forces), state quantities |
| 4. Choose the law | Acceleration / time → Newton's laws + kinematics; only care about initial and final states → work-energy theorem / mechanical energy conservation; collision, explosion, recoil → momentum conservation; circular → centripetal force equation; light → Snell's law + geometry | Which law for each stage (one-sentence reason) |
| 5. Write equations and solve | Define positive direction; one set of equations per stage; connect stages with continuity quantities (final velocity of one = initial velocity of next) | Equations and numbers, **symbolic solution before numerical** |
| 6. Check | Dimensions, limits (μ→0, θ→0, n₂→n₁), order of magnitude, solve again with another law (energy ↔ dynamics) | Check method and result |

**State the segmentation criteria out loud** (this is the most valuable part of the video):
- "Can it slide back?" Compare mg sinθ with maximum static friction μmg cosθ (usually take maximum static ≈ kinetic).
- "When do they reach common velocity?" Conveyor / block-slab: after common velocity, re-judge whether they move together or continue relative sliding.
- "Does it leave the surface?" At the highest point of a circle, compare required centripetal force with mg; normal force N = 0 is the critical case.
- "Total internal reflection?" Compare angle of incidence with critical angle.
- Direction of friction: look at the direction of **relative** motion (or tendency), not the velocity direction. Motion reverses ⇒ friction reverses.

## 2. Verify with sympy (strongly recommended, especially for multi-stage processes)

The default `python3` may lack packages; use the PY reported by `setup_check.sh` or an interpreter that has sympy. Write the equations from the solution card as a script; numerical answers, stage times, and critical conditions all come from it, then copy them into the constants area of anim.js:

```python
from sympy import *
g, th, mu, v0 = 10, Rational(3, 5), Rational(1, 2), 10   # textbook approximations: sin37°=3/5, cos37°=4/5
s, c = th, Rational(4, 5)
a1 = g*s + mu*g*c;  t1 = v0/a1;  x = v0**2/(2*a1)
a2 = g*s - mu*g*c;  v = sqrt(2*a2*x);  t2 = v/a2
print(a1, t1, x, a2, v, t2)       # 10 1 5 2 2*sqrt(5) sqrt(5)
# energy check: ½mv0² − f·2x = ½mv²
```

- Use textbook approximations for special angles (37°/53° → 0.6/0.8), and **use the same values in anim.js** (`const SIN = 0.6, COS = 0.8`); do not use `Math.sin(37°)`, otherwise the on-screen numbers will not match the answer.
- For symbolic answers (e.g. optics R = (n₂ − n₁) s l / [n₂ (d_A cos θ_A + d_B cos θ_B)]), simplify with sympy `simplify` and substitute a set of numbers to check the limits.

## 3. Turning the solution into animation (special requirements for physics problems)

1. **Motion must follow the true analytic solution**: write `x(t)`, `v(t)` at the top of anim.js (piecewise functions matching the sympy results); the picture uses `simT()` to map narration time **linearly** onto physical time. You may slow it down (note "slow motion ×0.2" on screen); do not use easing functions (eio) to drive object position — that fabricates acceleration.
2. **Graphs synchronized with motion**: the v-t / x-t curve is only drawn up to the current physical time; the cursor follows the object; when displacement = area, color it with `graph().area()`.
3. **Draw forces to scale**: within the same scene, force arrow length ∝ magnitude (one constant `FS` px/N). A 12 N arrow must be 1.5× longer than an 8 N arrow so viewers can "see" which is larger. Same for velocity arrows (`VS` px per m/s).
4. **Declare schematic exaggeration**: when drawing small angles or small displacements enlarged, write `notToScale()` in the corner ("angle exaggerated").
5. **Stage times must have visual events**: when velocity is zero the object pauses and the v arrow disappears; when friction reverses the arrow rotates 180° about the point of application; at common velocity the two velocity arrows merge.

## 4. Common problem types → suggested scene structure

| Type | Scenes (scene id) | Core visuals |
|---|---|---|
| Incline / horizontal back-and-forth (template) | intro → force → up → back → down → outro | Force decomposition, resultant head-to-tail, true deceleration/acceleration, two-segment v-t, friction reverses |
| Conveyor | intro → model → phase1 → together (common-velocity judgment) → phase2 → outro | Block + belt two sets of velocity arrows, relative-motion arrow, v-t area difference = skid mark |
| Block-slab model | intro → force (isolate both objects) → slip → common (common velocity) → outro | Separate force diagrams for the two objects (same friction equal and opposite), relative displacement |
| Projectile / angled throw | intro → split (decompose) → time → landing → outro | Strobe trail `trail({dots})`, horizontal/vertical velocity components changing with time |
| Circular motion | intro → force → critical (critical) → solve → outro | Centripetal force arrow pointing to center, critical picture of N→0 at the highest point |
| Energy / momentum conservation | intro → process → conserve → solve → check | `bars()` energy bars / momentum bars updating live, total unchanged |
| Charged particle in a field | intro → field → trajectory → geometry (find center/radius) → outro | `bField` / `eField`, Lorentz force always pointing to center, constructing the trajectory center |
| Geometric optics (examples/laser-curvature) | problem → setup → one scene per law → geometry relations → outro | `ray` light propagation, normal, angle arcs, "angle exaggerated" |
