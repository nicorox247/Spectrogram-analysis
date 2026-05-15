# Tracks

This file lists audio examples needed per section. The bar is **"clearly illustrates the point"** — not canonically iconic. Isolated samples and clean single-note recordings are often better than famous records for spectrogram work.

## Selection Criteria

A good example for this project must:
1. **Clearly visualize the claim** being made in that section of the script
2. Be available as **lossless audio** (WAV or FLAC — no streaming rips)
3. Have a **clean representative segment** of 5–15 seconds that works in isolation

---

## Section 1: Cold Open

| Purpose | Example | Notes |
|---------|---------|-------|
| Auto-Tune clip (hook) | Future – Mask Off, or Travis Scott, or Migos | ~5 seconds, obviously Auto-Tuned hook |

### Status
- [x] `Future_Mask_off.wav` acquired — usable for cold open Auto-Tune clip

---

## Section 2: What the Fourier Transform Is

| Purpose | Example | Notes |
|---------|---------|-------|
| Pure sine tone | Generate with Python/librosa | 440 Hz, 1–2 seconds |
| Complex waveform demo | Violin sustaining A4 | For contrast with sine |

### Status
- [ ] Sine tone — can be generated programmatically, no file needed
- [ ] Violin A4 isolated sample — search freesound.org or university sample libraries

---

## Section 3: Acoustic Timbre

| Purpose | Example | Notes |
|---------|---------|-------|
| Violin sustained note | Violin playing A4 or similar | Need clean, isolated note |
| Flute sustained note | Flute playing A4 or similar | Need clean, isolated note |
| Piano sustained note | Piano playing A4 | Need clean, isolated note |

### Status
- [ ] Violin sample acquired: _____
- [ ] Flute sample acquired: _____
- [ ] Piano sample acquired: _____

### Notes
University sample libraries (UIOWA Musical Instrument Samples) are ideal here — they have clean isolated notes for every instrument, free to use.

---

## Section 4: The Pivot and Synthesis

| Purpose | Example | Notes |
|---------|---------|-------|
| Early Moog sound | Wendy Carlos – *Switched-On Bach* excerpt | ~5 seconds of any recognizable Moog patch |
| DX7 / FM synthesis | 80s pop with obvious DX7 — Whitney Houston, A-ha, Hall & Oates | The electric piano or bass patch |
| Contemporary synth | Daft Punk, The Weeknd, or similar | Shows lineage continues |

### Status
- [ ] Moog example acquired: _____
- [ ] DX7 example acquired: _____
- [ ] Contemporary synth example acquired: _____

---

## Section 5: Sampling and Digital Manipulation

| Purpose | Example | Notes |
|---------|---------|-------|
| Sampled hip-hop track | De La Soul, A Tribe Called Quest, or contemporary trap | Shows sampling in use |
| Clean vocal | Any clean unprocessed vocal phrase | For before/after Auto-Tune contrast |
| Auto-Tuned vocal | Same or matching phrase with heavy Auto-Tune | T-Pain era or contemporary |

### Status
- [ ] Sampled hip-hop example acquired: _____
- [ ] Vocal pair (clean + Auto-Tuned) acquired: _____

---

## Acquisition Notes

- **UIOWA Musical Instrument Samples** (freemiva.org) — best source for isolated acoustic instrument notes (violin, flute, piano)
- **Freesound.org** — community samples, check licenses
- **Columbia Music Library / Naxos** — for Wendy Carlos and classical recordings
- **Bandcamp / HDtracks** — lossless purchases for pop/electronic examples where needed

## Testing Workflow

Once WAVs are in `audio/raw/`:

```bash
# Normalize and compute spectrograms
python analysis/normalize_loudness.py
python analysis/compute_spectrograms.py

# Generate preview PNGs
python analysis/generate_previews.py

# Animate a segment
python matplotlib_fallback/animate_spectrogram.py <track_name> <start_sec> <end_sec>
```
