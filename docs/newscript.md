# Script — Full Draft (Revised)

Target: ~20 minutes total. Voice ~150 wpm.

Conventions:
- `[VISUAL: ...]` — what's on screen
- `[AUDIO: ...]` — audio examples (under 2 min total across the whole video)
- `[SOURCE: ...]` — citation placeholder, fill with specific page numbers when sourced
- `[B-ROLL: ...]` — visual filler (images, archival footage, etc.)
- `[NEW ADDITION: ...]` — newly added content not yet recorded
- `[EDIT: ...]` — a small modification to existing content

Voiceover text is written to be spoken aloud. Lines in **bold** are the load-bearing claims of each section.

**Narrative arc:** Hook → Establish what the FT is, as a tool for *analysis* only → Use it as a microscope on acoustic instruments → Pivot moment: the FFT arrives, and you can run the process in reverse → Cascade of consequences (synthesis, sampling, Auto-Tune) → Reflection → Close.

---

## Section 1: Cold Open with Hook (1 min, ~150 words)

[unchanged — no edits to this section]

---

## Section 2: What the Fourier Transform Is (~4.5 min, ~675 words)

### 2a — A little history (~1 min)

[unchanged — no edits to this section]

### 2b — The math (~2 min)

[unchanged — no edits to this section]

### 2c — Microscope framing + new framing addition (~1.5 min)

**VOICEOVER:**
> **For now, let's just use it as a microscope. Let's use the Fourier transform to look at what acoustic music actually sounds like.**

`[NEW ADDITION — record this as an insert at end of section 2]`

`[VISUAL: Hold on a simple frame — maybe a still of the Fourier transform equation, or fade back to the portrait briefly]`

NEW VOICEOVER:
> One thing worth flagging before we go further. The Fourier transform is a specific mathematical procedure — a way of *computing* the breakdown of a signal into sine waves. But Fourier's deeper contribution wasn't really the procedure. It was the *idea* — the claim that every complex sound has a hidden additive structure, that anything you hear is some combination of pure tones layered together.

> That idea turned out to matter even more than the procedure itself. Because once engineers and composers internalized it, they didn't just want to *analyze* sounds — they wanted to *build* them. They wanted to design filters that shaped frequencies on purpose. They wanted to construct timbres from scratch. Some of what comes next in this video uses the Fourier transform directly. Some of it uses Fourier's idea as a way of thinking, implemented in circuits and oscillators rather than in code. Both are part of the same story.

`[END NEW ADDITION]`

---

## Section 3: Acoustic Timbre (4 min, ~600 words)

[unchanged — no edits to this section]

---

## Section 4: The Pivot and Synthesis (~6.5 min, ~975 words)

### 4a — The Pivot (~1.25 min)

[unchanged — no edits to this section]

### 4b — Moog and early synthesis (~2 min)

[unchanged — no edits to this section]

### 4c — DX7 and FM synthesis (~1.5 min)

`[B-ROLL: Photos of the Yamaha DX7, 80s pop production]`

VOICEOVER:
> If the Moog sculpted sound by *removing* harmonics from a rich waveform, the next generation of synthesizers did the opposite: they generated complex spectra directly, starting from nothing but pure sine waves. The breakthrough came in the early 1970s at Stanford, where a composer named John Chowning was experimenting with vibrato. He'd take a sine wave and modulate its pitch with another sine wave to produce a wobble — and he noticed that when he pushed the modulation rate up into the audio range, fast enough that you couldn't hear the individual wobbles anymore, the sound stopped wobbling and started transforming. New frequencies appeared. Bright, metallic, bell-like tones that no acoustic instrument could produce.

> Chowning had stumbled onto something the math of Fourier analysis predicts exactly. When you modulate one sine wave with another, the result isn't a wobble — it's a precise, calculable series of new frequencies arranged around the original tone, with amplitudes determined by the modulation depth. Push the depth harder and you summon more harmonics. Change the ratio between the two sine waves and you change which harmonics appear. You can design a target spectrum with pencil and paper, then dial up the parameters that produce it. This technique became known as FM synthesis — frequency modulation — and it's one of the most direct musical applications of Fourier thinking in any consumer technology ever built.
> [SOURCE: Chowning, "The Synthesis of Complex Audio Spectra by Means of Frequency Modulation," 1973]

`[EDIT: previous phrase was "one of the most direct applications of Fourier theory" — now says "one of the most direct musical applications of Fourier thinking". One-word swap of "theory" → "thinking" and added "musical" to align with the new section 2c framing. Re-record this sentence only, or paste over the original if convenient.]`

`[B-ROLL: The Yamaha DX7, close-up shots of its interface]`

VOICEOVER:
> Stanford licensed Chowning's work to Yamaha. And in 1983, Yamaha released the DX7 — the first commercially successful digital synthesizer, built around six sine-wave operators that could modulate each other in different configurations. It sold over 200,000 units, which for a synthesizer is astonishing.

`[AUDIO: 5 seconds of a recognizable DX7 patch — the famous "electric piano" or "bass" sound]`
`[VISUAL: Spectrogram of the DX7 patch, showing the characteristic non-harmonic frequency content]`

VOICEOVER:
> If you grew up listening to 80s pop, this is the sound of your childhood. Whitney Houston's "Greatest Love of All." The electric piano in nearly every power ballad of the decade. The slap-bass synths on countless TV themes. That distinctive bright, glassy shimmer — that's FM synthesis. That's Fourier thinking, shipped as a piece of consumer hardware, played by every keyboard player from Tokyo to Nashville.

`[EDIT: previous phrase was "That's pure Fourier mathematics, shipped as a piece of consumer hardware" — now says "That's Fourier thinking, shipped as a piece of consumer hardware". Two-word swap. Re-record this sentence only.]`

### 4d — Contemporary synths (~1.25 min)

[unchanged — no edits to this section]

---

## Section 5: Sampling and Digital Manipulation (3 min, ~450 words)

[unchanged — no edits to this section]

---

## Section 6: How This Changed What We Hear (2 min, ~300 words)

[unchanged — no edits to this section]

---

## Section 7: Conclusion (1 min, ~150 words)

[unchanged — no edits to this section]

---

## Timing Summary

| Section | Duration | Word target |
|---------|---------:|------------:|
| 1. Cold open | 1.0 min | 150 |
| 2. What the FT is | 4.5 min | 675 (was 3.5 / 525 — added ~150 words of new framing at end of 2c) |
| 3. Acoustic timbre | 4.0 min | 600 |
| 4. Pivot + Synthesis | 6.5 min | 975 (was 5.5 / 825 — Cold War / FFT expansion already incorporated in 4a) |
| 5. Sampling & manipulation | 3.0 min | 450 |
| 6. What it means | 2.0 min | 300 |
| 7. Conclusion | 1.0 min | 150 |
| **Total** | **22.0 min** | **~3,300** |

Audio examples used: ~8 short clips totaling under 2 minutes per rubric.

---

## Summary of Changes (what you actually need to do)

**Three things changed in this revision:**

1. **NEW ADDITION at end of section 2c** — ~150 words of new voiceover explaining the distinction between the Fourier transform (the procedure) and Fourier's idea (the conceptual framework). This is a fresh insert you'll need to record. Goes immediately after the existing "microscope framing" bold line.

2. **EDIT in section 4c, first paragraph, final sentence** — one phrase swap from "one of the most direct applications of Fourier theory" to "one of the most direct musical applications of Fourier thinking". Re-record this single sentence.

3. **EDIT in section 4c, last paragraph, second-to-last sentence** — one phrase swap from "That's pure Fourier mathematics, shipped as a piece of consumer hardware" to "That's Fourier thinking, shipped as a piece of consumer hardware". Re-record this single sentence.

**Total new recording needed:** ~150 words for the section 2c insert + two sentence-level pickups in section 4c. Maybe 90 seconds of new voiceover.

---

## Existing issues in your draft (separate from this revision)

I noticed a few things in the script you pasted that look like editing artifacts. Flagging them in case you want to clean them up while you're in there:

- Section 2a header is duplicated three times in your file (lines for "### 2a — A little history" appear consecutively before the actual content). Only one is needed.
- Section 4a header is duplicated three times with different time estimates (45 sec / 1 min / 1.25 min). The 1.25 min version is the current one — the other two are old versions that should be deleted.
- Section 4a contains a paragraph that starts "Now that the computational aspect of fourier transforms had been made trivial, this allowed for innovation in real-time digital applications. The analog version of the spectrogram we were using earlier became digitized. But another very interesting idea came up. What happens when we reverse the transform?" — this paragraph appears *after* the analysis/synthesis explanation, which makes it redundant. You probably want to either delete it or move it earlier and cut the duplicate explanation.

None of these affect the new additions, just worth cleaning up.