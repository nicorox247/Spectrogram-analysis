# Working Schedule

Deadline: **May 13, 2026.**

The schedule below reflects the revised project. Key sequencing change: the script is largely done, so source-gathering and audio acquisition are now the priority. The bar for audio examples is "clearly illustrates the point" — isolated single notes are often better than famous records for spectrogram work.

## Day 0: May 6 ✓

- [x] Set up project folder, install dependencies, verify manim renders the smoke test
- [x] Begin gathering source materials — Bach Fugue in C minor and Future - Mask Off acquired
- [ ] Email professor with project proposal for explicit approval

## Day 1: May 7

- [x] `violin_A4.wav` acquired from UIOWA, trimmed to sustained note, normalized, spectrogram computed
- [x] Resynthesis animation pipeline built (`animate_resynthesis.py`) — scrolling window, progressive component reveal, high-fidelity closing
- [ ] Acquire flute A4 and piano A4 from UIOWA
- [ ] Acquire synthesis examples: one Moog/Wendy Carlos clip, one DX7 patch clip
- [ ] Read Sethares chapters 1–3 and Chowning (1973) paper

## Day 2: May 8

- [x] Run normalization pipeline (skip logic in place)
- [x] Run spectrogram computation (skip logic in place)
- [x] Generate matplotlib preview PNGs (skip logic in place)
- [ ] Run pipeline on all new instrument samples and synthesis examples
- [ ] Review previews — confirm violin/flute/piano harmonic stacks are clearly visible
- [ ] **Commit to final audio examples for all sections — no second-guessing after today**
- [ ] Update `docs/tracks.md` with final selections

## Day 3: May 9

- [ ] Build the manim Section 2 animation: waveform → FFT → spectrogram explainer (this is the most complex scene — do it early)
- [x] Spectrogram animation template complete (`animate_spectrogram.py` — cividis colormap, reveal effect, CLI args, QuickTime H.264, audio baked in)
- [x] Resynthesis animation template complete (`animate_resynthesis.py` — scrolling window, plasma red→yellow colormap, progressive versions, sum-only closing)
- [x] Violin A4 spectrogram + resynthesis animations rendered
- [ ] Render spectrogram + resynthesis animations for flute A4 and piano A4
- [ ] Render spectrogram animations for Section 4 (Moog, DX7, contemporary synth)

## Day 4: May 10

- [ ] Render spectrogram animations for Section 5 (sampled hip-hop, Auto-Tune vocal pair)
- [ ] Build manim reverse-FT animation for Section 4a pivot moment (violin spectrogram → arrows → new waveform)
- [ ] Read Pinch & Trocco (Moog chapters), Heideman et al. (FFT history), Schloss (sampling chapters)
- [ ] First full read-through of complete script with stopwatch

## Day 5: May 11

- [ ] Final script polish — tighten any sections running long
- [ ] Record voiceover (use a closet, hang clothes for sound dampening)
- [ ] Edit voiceover audio (cut long pauses, breaths, mistakes)
- [ ] Re-render any animations at high quality (higher dpi for matplotlib)

## Day 6: May 12

- [ ] Assemble in video editor (DaVinci Resolve recommended)
  - Place voiceover on timeline
  - Sync spectrogram animation MP4s (audio already baked in)
  - Insert remaining audio examples (verify total under 2 minutes)
  - Add title cards and section headers
  - Add source citations on screen where indicated
- [ ] Watch through end-to-end
- [ ] Fix the 3–5 things that nag you most
- [ ] Compile sources PDF with bibliography in Chicago Notes-Bibliography style

## Day 7: May 13

- [ ] Final watch-through
- [ ] Export final MP4 (1080p, 8–12 Mbps)
- [ ] Upload to Google Drive or Vimeo as private/unlisted
- [ ] Add link to top of sources PDF
- [ ] **Submit to Canvas before deadline**

## Things That Tend to Eat Time

1. **Instrument sample hunting.** UIOWA has clean isolated notes for free — go there first, don't spend more than 30 minutes on this.
2. **Manim render times.** If the Section 2 or 4a scene takes more than ~10 minutes at low quality, simplify. The narrative matters more than the animation.
3. **Voiceover perfectionism.** Your voice will sound weird to you. It sounds normal to everyone else. Record, lightly edit, move on.
4. **Reading too much.** You need Sethares ch. 1–3, Chowning, Heideman, and selective Schloss. That's it. Don't read Pinch & Trocco cover to cover.

## Fallback Triggers

If by **end of Day 3** the manim scenes aren't working, switch entirely to matplotlib for all visualizations and use static title cards for the pivot moment. The argument still lands.

If by **end of Day 5** you don't have a complete assembled edit, cut Section 4d (contemporary synths) to a brief mention rather than a full spectrogram segment. The Moog → DX7 sequence carries the argument; 4d is supporting material.

If by **end of Day 6** the video isn't assembled, submit what you have. A submitted project at 80% gets graded; an unsubmitted project at 100% does not.

## Reminders

- The narrative is the project. Spectrograms are evidence. Animations are presentation.
- The professor will appreciate ambition tempered by execution.
- Sleep is not optional.
