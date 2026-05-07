# Working Schedule

Deadline: **May 13, 2026** (today is May 6).

The schedule below is aggressive but workable. The key is sequencing: do the things that *unblock* other things first, and don't get stuck on polish before the structure is in place.

## Day 0: May 6 (today)

- [ ] Email professor with project proposal for explicit approval (note: rubric says "involving music that I have approved")
- [x] Set up project folder, install dependencies, verify manim renders the smoke test
- [x] Begin gathering source materials — Bach Fugue in C minor and Future - Mask Off acquired

## Day 1: May 7

- [ ] Acquire 3-4 candidate WAVs per genre (12-16 tracks total)
- [ ] Read Sterne, *Audible Past* introduction; Veal, *Dub* introduction; Schloss, *Making Beats* introduction. This is the bare minimum to start writing with grounding.
- [ ] Draft script section 1 (cold open) and section 2 (spectrogram explainer)

## Day 2: May 8

- [x] Run normalization pipeline on all candidates (skip logic added — won't re-process existing files)
- [x] Run spectrogram computation on all candidates (skip logic added)
- [x] Generate matplotlib preview PNGs side by side (skip logic added)
- [ ] **Pick canonical tracks for each section** (commit and don't second-guess)
- [ ] Update `docs/tracks.md` with final selections
- [ ] Draft script sections 3 and 4

## Day 3: May 9

- [ ] Build the manim spectrogram explainer scene (section 2 of video). This is the most complex animation, get it done early.
- [x] Build matplotlib animation template for per-track spectrograms with sweeping playhead (reveal effect, CLI args, QuickTime-compatible H.264)
- [ ] Render preview MP4s for sections 3-4
- [ ] Draft script sections 5 and 6

## Day 4: May 10

- [ ] Render preview MP4s for sections 5-6
- [ ] Build manim final comparison scene (section 7 of video)
- [ ] Draft script section 7
- [ ] Read remaining priority chapters from sources
- [ ] First full read-through of complete script with stopwatch

## Day 5: May 11

- [ ] Final script polish
- [ ] Record voiceover (use a closet, hang clothes around for sound dampening)
- [ ] Edit voiceover audio (cut long pauses, breath sounds, mistakes)
- [ ] Re-render any animations at high quality (`-qh` for manim, higher dpi for matplotlib)

## Day 6: May 12

- [ ] Assemble in video editor (DaVinci Resolve recommended)
  - Place voiceover on timeline
  - Sync animation MP4s
  - Insert audio examples (verify total under 2 minutes)
  - Add title cards and section headers
  - Add citations on screen as appropriate
- [ ] Watch through end-to-end
- [ ] Fix the 3-5 things that nag you most
- [ ] Compile sources PDF with bibliography in chosen citation style

## Day 7: May 13

- [ ] Final watch-through
- [ ] Export final MP4 (1080p, reasonable bitrate — 8-12 Mbps is plenty)
- [ ] Upload to Google Drive or Vimeo as private/unlisted
- [ ] Add link to top of sources PDF
- [ ] **Submit to Canvas before deadline**
- [ ] Take a breath

## Things That Tend to Eat Time

If you find yourself behind schedule, these are the time sinks to watch for:

1. **Manim installation problems on the first day.** If smoke test fails, fix it now or commit to matplotlib-only and don't come back.
2. **Track indecision.** Allowing yourself to keep "testing one more track" past day 2 is fatal. Commit at end of day 2, no exceptions.
3. **Voiceover perfectionism.** Your voice will sound weird to you. It sounds normal to everyone else. Record, lightly edit, move on.
4. **Manim render times.** If a scene takes more than ~10 minutes to render at low quality, simplify the scene. Don't let render times eat your day.
5. **Reading too much from sources.** You need to engage with sources, not master them. Read introductions and the chapters you'll directly cite. That's enough.

## Fallback Triggers

If by **end of Day 3** you don't have working manim animations, switch entirely to matplotlib for all visualizations. The video can still be excellent without manim — manim is craft, not substance.

If by **end of Day 5** you don't have a complete script, cut Section 5 (dub/electronic) down to 2 minutes as a transition rather than a full section. The argument still holds; you just lose some historical depth.

If by **end of Day 6** you don't have a complete assembled video, submit what you have with a brief note acknowledging incomplete polish. A submitted project at 80% completion gets graded; an unsubmitted project at 100% does not.

## Reminders

- The argument matters more than the polish.
- The professor will appreciate ambition tempered by execution. They will not appreciate ambition that didn't ship.
- Sleep is not optional. Do not pull all-nighters; you will make worse decisions.
