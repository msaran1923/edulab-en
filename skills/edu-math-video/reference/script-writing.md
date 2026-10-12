# Writing the narration script: episode.json + script.json

## episode.json

```json
{
  "title": "Median to the hypotenuse of a right triangle: find the length of CD",
  "output_name": "Median_to_Hypotenuse",
  "pop_scenes": ["key", "solve"]
}
```
- `title`: written into the mp4 metadata.
- `output_name`: outputs `WS/<output_name>.mp4` and `.srt`. Format `Short_English_Name`; no spaces or `/`.
- `pop_scenes`: add a light "pop" sound effect at the start of each narration line in these scenes (use for key conclusions and equation scenes). The "whoosh" on scene transitions is automatic.

## script.json format

```json
[
  {"scene": "intro", "lines": [
    {"zh": " AC = 3，BC = 4。",
     "tts": "The legs are AC equals three, BC equals four.",
     "en": "The legs are AC = 3 and BC = 4."}
  ]},
  {"scene": "solve", "lines": [ ... ]}
]
```

| Field | Purpose | Rules |
|---|---|---|
| `scene` | Scene id | English identifier (`intro`, `figure`, `key`, `solve`, `check`, `outro`…), unique; anim.js must have a matching `SC.<id>` and `TAGS.<id>` |
| `zh` | Chinese subtitle | Normal mathematical notation: `AB = 5`, `∠C = 90°`, `AB^2` (`^2` displays as ², `_2` as ₂). May contain pronunciation annotations, which are automatically stripped from the subtitle |
| `tts` | Text actually spoken | **Only speakable text** (see table below). If omitted, `zh` is spoken, so you must write `tts` whenever `zh` contains numbers or symbols |
| `en` | English subtitle | Corresponding meaning, ≤ 95 characters |

**Write `tts` for every line**, even if it matches the subtitle, so nothing is missed.

## Scene structure (standard 5–7 scenes)

| Scene id (example) | Content | Picture |
|---|---|---|
| `intro` | Title + **read the problem line by line**: one condition per sentence, last sentence reads "what is asked" | Problem image card; box each condition as it is read; small condition chips appear below |
| `figure` / `setup` | Draw the figure, mark known quantities, clarify what is asked | Left side draws the figure step by step; right board lists "given / find" |
| `key` | Key idea / theorem, **and show why with animation** | Add auxiliary lines, coloring, correspondences on the figure |
| `solve` / `equation` | Write equations, one step per sentence | Board writes formulas line by line; finally `stamp` the answer |
| `check` (recommended) | Substitute back to verify, check the range | Mark actual values on the figure |
| `outro` | Method review (3 cards) + state the answer + closing | Cards → mascot + answer bubble |

Multiple parts (question (1)(2)): one key/solve pair per part, ids such as `key1`, `solve1`, `key2`, `solve2`.

## Rules for good narration

1. **One point per sentence**, 15–30 characters is best; > 36 character widths (`--check` will warn) causes the subtitle to wrap to two lines, and the subtitle box top rises to y≈860.
2. Conversational, like a teacher: "Let's look at this problem", "Why?", "The key is…".
3. Speak in the order of the picture: first say "look at this auxiliary line", then the auxiliary line appears.
4. Numbers must match the solution exactly; the check scene must actually substitute back.
5. Reading sentences must correspond to the original problem text, because each sentence needs a highlight box.
6. The whole video is 1.5–3.5 minutes, about 15–30 sentences.

## Spoken form of mathematical expressions (tts field)

`--check` blocks Arabic numerals and symbols in tts. Reference table:

| Written | Write in tts |
|---|---|
| `AC = 3` | AC equals three |
| `60 m`, `7.5 s`, `4 m/s` | sixty meters, seven point five seconds, four meters per second |
| `1200`, `4800` | one thousand two hundred, four thousand eight hundred |
| `-3` | negative three |
| `x²`, `x³`, `xⁿ` | x squared, x cubed, x to the n |
| `√3`, `2√3` | square root of three, two times square root of three |
| `3/4`, `a/b` | three over four, a over b |
| `(60 − 7t)/60` | sixty minus seven t, over sixty |
| `a(b + c)` | a times the quantity b plus c |
| `a × b`, `a ÷ b`, `a · b` | a times b, a divided by b, a dot b (vector) |
| `a ≥ b`, `a ≤ b`, `a ≠ b`, `≈` | a greater than or equal to b, a less than or equal to b, a not equal to b, approximately equal to |
| `∠ABC = 90°` | angle ABC equals ninety degrees |
| `△ABC ∽ △DEF`, `≌` | triangle ABC is similar to triangle DEF, congruent to |
| `AB ∥ CD`, `AB ⊥ CD` | AB parallel to CD, AB perpendicular to CD |
| `x ∈ [0, 1]` | x belongs to the closed interval zero to one |
| `f(x) = 2x + 1` | f of x equals two x plus one |
| `f'(x)` | the derivative of f of x |
| `sin α`, `cos 2x`, `tan θ` | sine alpha, cosine of two x, tangent theta (do not write sin/cos; TTS will misread) |
| `log₂8` | log base two of eight |
| `π` | pi |
| Coordinates `(2, −1)`, `A(1, 0)` | point two, negative one / x-coordinate two, y-coordinate negative one / point A one, zero (do not say "open parenthesis… close parenthesis") |
| Interval `1 < x < 3`, `(1, 3)` | one less than x less than three / open interval one to three |
| `a₁`, `aₙ`, `Sₙ` | a one, a n, S n |
| `{aₙ}` | sequence a n |
| `P(A)` | the probability of A / P A |
| `%` | percent |
| `∴`, `∵` | therefore, because |
| `Rt△ABC` | right triangle ABC |
| Capital letter point names `AB`, `BPQ` | write `AB` directly (pron.py automatically splits into `A B` and reads them one by one; do not write `A, B`) |
| A single character before a letter (`arc AC`, `T is…` at the start) | Prefix with a category noun: `arc AC`, `point T is…`, `segment CM equals…` |

Tips:
- When parentheses or fractions are long, split into two sentences, or use a comma to give TTS a pause: "sixty minus seven t, over sixty".

**Phrasing**: GLM-TTS has no pause markers; the only way to control pauses is punctuation.
- Place commas where a natural breath occurs when speaking: after a long subject, before "so / therefore / thus", before each "equals" in a chain of equalities (`OB equals square root of two plus one, equals square root of three`).
- A clause (between two punctuation marks) should not exceed 18 characters, otherwise TTS will find its own place to pause, often in the middle of a word; `--check` will warn.
- Do not split a noun with a comma: do not write `plane, P A D`, `angle, O C B`.
- Colons and semicolons also produce pauses; use them only where you truly want a pause.
- Single lowercase letters are fine (`t`, `x`); consecutive lowercase words (sin, log, max) will be warned; replace them with English words.
- Years and numbers follow customary reading: "two thousand twenty five".

## Self-check after writing
- [ ] Every `tts` has no digits or symbols (`--check` has no ERROR)
- [ ] Every intro sentence corresponds to a highlight box on the problem image
- [ ] The final answer matches what you calculated yourself in Step 1
- [ ] The last sentence of the outro states the answer
