# Claude Code Prompt: Project Pivot

Paste the text below into Claude Code from the root of your `spectral-history/` project directory.

---

I'm pivoting this project. Please read CLAUDE.md first to understand the current state, then update the project documents to reflect the new direction.

## The new project

**Same title family, new thesis.** Instead of arguing that bass frequencies descended an octave in 50 years, the project is now a historical narrative video essay about how the Fourier transform — a piece of 19th-century mathematics — quietly reshaped what music can sound like.

**New thesis:** Joseph Fourier's early-1800s work on heat conduction, made computationally practical by the Cooley-Tukey FFT algorithm in 1965, became the mathematical foundation for nearly every form of modern sound manipulation: synthesizers, samplers, Auto-Tune, MP3 compression, drum machines, digital audio workstations. The video traces this lineage by analyzing the spectrograms of acoustic instruments and contrasting them with synthesized and digitally processed sounds.

**Tone:** Pedagogical and warm, not densely argumentative. A narrative with a clear through-line, not a tight thesis with a sharp claim. Closer in spirit to a 3Blue1Brown video than an academic essay.

**Cold open hook:** Opens with "What does this 1800s French mathematician have to do with these guys?" — Joseph Fourier's portrait followed by images of contemporary hip-hop artists (Future, Drake, Migos) with an Auto-Tune audio clip. Then a teaser list: "This video shows how a heat equation became the foundation of synthesizers, Auto-Tune, 808s, sampling, and more."

## Narrative structure (~20 minutes total)

The narrative is staged so the dramatic reveal — that the Fourier transform can be run in reverse to *manufacture* sound, not just analyze it — lands at the historical pivot point, not at the start. Sections 2-3 treat the FT as an analytical microscope only. Section 4 opens with the FFT (1965) arrival and the reverse-the-process insight, then cascades into synthesis, sampling, and digital manipulation.

1. **Cold open with the hook** (1 min) — Fourier portrait + hip-hop images + Auto-Tune clip + teaser
2. **What the Fourier transform is** (3.5 min) — Intuitive math: any sound decomposes into sine waves; spectrograms visualize this. Plus a little history: Fourier 1822, studying heat. The FT is presented purely as an *analytical* tool here. We do NOT mention synthesis or the reverse process yet.
3. **Acoustic timbre** (4 min) — Use the FT as a microscope on violin, flute, piano. Establish the concept of spectral fingerprint and the centuries-long stability of the acoustic palette. Subtle artist nods (Beethoven/Mahler for violin, Debussy for flute, Gould/Horowitz for piano). Ends with the cliffhanger: "Then in the 1960s, that started to change."
4. **The pivot and synthesis** (5.5 min) — Opens with the 1965 FFT arrival (Cooley & Tukey) and the dramatic reveal: if the FT can decompose sound, you can run it in reverse to build new sounds. Then Moog → DX7/FM synthesis → contemporary synths.
5. **Sampling and digital manipulation** (3 min) — Samplers, hip-hop, Auto-Tune, the modern Fourier-domain production environment
6. **How this changed what we hear** (2 min) — Cultural/aesthetic payoff
7. **Conclusion** (1 min) — Short, lyrical close on Fourier's unintended legacy

The key structural choice: the viewer EARNS the insight that synthesis is "running the FT in reverse" at the moment it becomes historically relevant. Sections 2-3 set up; Section 4 detonates the reveal.

## What I need you to do

Please update these files to reflect the new direction. Keep the structure of the documents (sections, headers) similar to what's there — just rewrite the content. Don't rebuild the whole repo from scratch.

1. **`CLAUDE.md`** — Update the project summary, thesis, "what done looks like," and structure sections. Note that the toolchain, file structure, and conventions stay the same — the pipeline still works as-is.

2. **`docs/tracks.md`** — Replace the genre-organized track list with an example-organized list reflecting the new sections:
   - Section 1: Auto-Tune clip (contemporary hip-hop, e.g. Future/Migos/Travis Scott)
   - Section 2: 440 Hz sine tone, sustained violin note for waveform/spectrogram demo
   - Section 3: Acoustic violin, flute, piano sustained notes (isolated samples ideal)
   - Section 4: Early Moog example (Wendy Carlos), DX7 patch (recognizable 80s pop), contemporary synth (Daft Punk/The Weeknd/similar)
   - Section 5: Sampled hip-hop track, clean vocal + Auto-Tuned vocal pair
   - The bar is "clearly illustrates the point" rather than "canonically iconic"

3. **`docs/script.md`** — REPLACE THE ENTIRE FILE with the revised script that I will paste in a follow-up message. Don't try to regenerate it; I have the final version. Just make sure `docs/script.md` is ready to receive it.

4. **`docs/sources.md`** — Adjust which sources are foregrounded:
   - **Sethares** becomes central (timbre and spectrum is the core concept now)
   - **Pinch & Trocco** (Moog history) becomes central (synthesis section)
   - **Chowning, "The Synthesis of Complex Audio Spectra by Means of Frequency Modulation" (1973)** — ADD this for the FM synthesis claim in Section 4
   - **Heideman, Johnson, Burrus, "Gauss and the History of the Fast Fourier Transform" (1985)** — ADD this for the FFT history in Section 4
   - **Sterne, *The Audible Past*** remains relevant (cultural reception of recorded sound, Section 6)
   - **Schloss, *Making Beats*** stays relevant (sampling and hip-hop production, Section 5)
   - **Veal, *Dub*** becomes optional (no longer the focus)
   - **Henriques, *Sonic Bodies*** becomes optional (no longer the focus)

5. **`docs/schedule.md`** — Keep the week-long structure but note that the new sequencing is: script first (mostly done), then targeted source-gathering, then analysis and animation. Source-gathering is now simpler because the bar is "clearly illustrates the point" rather than "canonically iconic."

Please don't change `analysis/`, `animations/`, or `requirements.txt`. The technical pipeline is unaffected.

After making the changes, give me a brief summary of what you updated so I can verify it matches the pivot. Then ask me to paste in the new script content for `docs/script.md`.
