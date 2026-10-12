---
name: edu-physics-video
description: >-
  Use when asked to make an explainer / walkthrough video for a physics problem (mechanics: force analysis, Newton's laws, incline, conveyor, projectile, circular motion, energy, momentum; optics: refraction; electromagnetism: charged particles), from a problem screenshot or text, with English (or Turkish) voice-over (edge-tts or GLM-TTS), bilingual en+tr subtitles and blueprint-style canvas animation where the motion follows the real analytic solution, rendered to MP4.
  Trigger words: physics explainer video, force diagram, Newton's laws, incline, projectile, circular motion, energy, momentum, refraction; fizik açıklayıcı video, kuvvet diyagramı.
---

# Physics Problem Explainer Video (edu-physics-video)

Turns one physics problem into a 16:9, 1920×1080 MP4 with English/Turkish voice-over + bilingual subtitles + blueprint-style animation. The pipeline is the same as edu-math-video; what changes is the solving method and the picture: first solve correctly following the physics workflow (model → segment → forces → choose law → solve → verify), then make the picture truly enact the physical process — force arrows grow from the point of application on a consistent scale, the object moves according to the analytic solution `x(t)` via linear `simT()`, the v–t graph grows in sync, friction reverses when relative motion does.

**Core principle: the picture follows the narration, and the physical process really happens on the figure.** Every narration line has an action that enacts that physics; every animation is timed with `S.at(k, f)`; object position comes only from the analytic solution.

The skill contains all code (template with incline example, phys.js prop library, examples/laser-curvature for optics, shared pronunciation, scripts). Do not copy from other projects. WS = user's current directory.

## Rules that must be followed
Same 11-step discipline as math-video, plus:
- First solve with the physics method and write a solution card (object of study, process segments, forces per segment, laws used, answer, verification).
- `tts` must be speakable (units read aloud: "ten meters per second", Greek letters as "theta", etc.).
- Physical correctness: force directions (friction opposite relative motion), consistent scale `FS` for force arrows, positions from analytic solution, textbook approximations for special angles (sin37° = 0.6).
- All content within y ≤ 860. Graphics left, derivation on right `board()` with `bm()` for subscripts.

## 11 Steps
1. Solve with physics method, write solution card (read physics-solving reference). Use sympy for multi-segment or symbolic answers.
2. Create project + setup check (`new_video.sh` + `setup_check.sh`). Handle missing GLM_API_KEY by guiding user or using edge-tts fallback.
3. Test TTS with a short English/Turkish sentence.
4. Prepare `problem.png` + highlight boxes.
5. Write `episode.json` + `script.json` (scenes follow solving flow: intro → forces/modeling → each process segment → critical judgment → verification → outro).
6. Write `storyboard.md` (solution card + figure list at top; point/move/leave for each line; choose actions from the physics action table).
7. Pronunciation & script check to 0.
8. Write `anim.js` (PROBLEM, TAGS, physics constants, analytic solutions `sPos(t)`, `vel(t)`, scale constants `FS`/`VS`, `SC.<id>` per scene).
9. Free preview: motion + stills + contact sheet. Fix any STATIC.
10. Real TTS + ASR + re-check stills.
11. Render video (`node render.mjs video 6`) and deliver paths, duration, scene contents, answer. Remind user to listen for pronunciation.

## Common mistakes
Do not skip modeling/segmentation, do not draw friction only opposite velocity (must reverse on direction change), do not lerp object positions (use analytic solution + linear time), do not invent force arrow lengths (use consistent FS), do not hard-code times, always check screenshots, etc.

## Reference files
physics-solving.md, visual-design.md, animation.md, script-writing.md, pronunciation.md, glm-tts-setup.md, troubleshooting.md.
