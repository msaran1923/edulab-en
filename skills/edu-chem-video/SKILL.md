---
name: edu-chem-video
description: >-
  Use when asked to make an explainer / walkthrough video for a chemistry problem (redox balancing and double-line bridge, amount of substance calculations, chemical equilibrium ICE table, equilibrium constant, conversion rate, reaction rate, ionic reactions, electrochemistry, titration, industrial processes), from a problem screenshot or text, with English (or Turkish) voice-over (edge-tts or GLM-TTS), bilingual en+tr subtitles and chalkboard-style canvas animation built around the chemical equation, rendered to MP4.
  Trigger words: chemistry explainer video, redox, electron conservation, double-line bridge, amount of substance, chemical equilibrium, ICE table, titration; kimya açıklayıcı video, redoks.
---

# Chemistry Problem Explainer Video (edu-chem-video)

Turns one chemistry problem into a 16:9, 1920×1080 MP4 with English/Turkish voice-over + bilingual subtitles + **green chalkboard** style animation. Pipeline is the same as the other video skills; differences are the solving method and the picture:
- Solving: the main line is "**conservation + amount of substance as the center**": write and balance the equation correctly (electron conservation → atom conservation → charge conservation) → find relationships (coefficient ratios, conservation, relations) → calculate centered on n / ICE table → re-check conservation.
- Picture: dark green blackboard + chalk lines; **top pinned equation strip**, demo on the left, slate on the right. Oxidation numbers rise/fall on a number line, electrons group until counts match, coefficients fly from the electron row into the equation, atom tallies check off, double-line bridge shows electron flow, molecule boxes react in the coefficient ratio, ICE table fills row by row. Visually distinct from math (beige notebook) and physics (dark blue blueprint).

**Core principle: the equation explains the problem, and conservation is counted on screen.** Every narration line has an action that enacts that chemical reasoning; all proportions and quantities come from the balanced equation; every animation is timed with `S.at(k, f)`.

The skill contains all code (template with copper + dilute nitric acid example, chem.js prop library for equation/valence/bridge/eFlow/tally/molMap/iceTable/molecule/beaker/graph, examples/equilibrium, chem_check.py for zero-dependency balancing verification, shared pronunciation with chemistry terms, scripts).

## Rules that must be followed
Same 11-step discipline, plus:
- First solve with the chemistry method and write a solution card. Equations must be verified with `chem_check.py`.
- `tts` uses names instead of formulas (`HNO3` → nitric acid, `SO4^{2-}` → sulfate ion, units spoken).
- Chemical correctness: oxidation numbers, coefficients, bridge endpoints and electron counts, molecule counts all match the solution card. Color convention: lost electrons / oxidation blue, gained electrons / reduction red.
- Layout: equation strip y 140~300, demo area x 60~900 y 310~860, slate with `board()` + `bm()`.

## 11 Steps
1. Solve with chemistry method, write solution card (read chemistry-solving reference). Run `chem_check.py balance` and `check`.
2. Create project + setup check.
3. Test TTS.
4. Prepare problem image + boxes.
5. Write episode.json + script.json (scenes follow solving flow: intro → equation/oxidation numbers → balancing → (double-line bridge) → calculation/ICE → (re-check, common mistakes) → outro).
6. Write storyboard.md (solution card + figure list at top; point/move/leave; choose from chemistry action table).
7. Pronunciation & script check to 0.
8. Write anim.js (chemical constants area with equation spec and coefficients, eqDraw, SC.<id> per scene).
9. Free preview: motion + stills. Check chemical correctness on screenshots.
10. Real TTS + ASR + re-check.
11. Render and deliver.

## Common mistakes
Do not start calculating with an unbalanced equation, do not only say "observation method" for balancing (show oxidation numbers → electron conservation → atom conservation), do not write formulas in tts, do not connect double-line bridge between different elements, do not confuse "nitric acid reduced" with "nitric acid that reacted", always use concentrations (not amounts) for K, always check screenshots, etc.

## Reference files
chemistry-solving.md, visual-design.md, animation.md, script-writing.md, pronunciation.md, glm-tts-setup.md, troubleshooting.md.
