# Tracks

This file tracks candidate recordings, testing decisions, and final selections. Update as you go.

## Selection Criteria

A canonical track for this project must:
1. Be spectrally **iconic** of its tradition (not just a track you happen to like)
2. Produce a spectrogram that **clearly visualizes** the argument for that section
3. Be available as **lossless audio** (WAV or FLAC, ideally from the original master rather than a streaming rip)
4. Have a **clean representative segment** of 15-30 seconds you can isolate for animation

## Section 3: Acoustic Baseline

### Candidates

| Track | Composer/Performer | Notes |
|-------|---------|-------|
| Passacaglia and Fugue in C minor (BWV 582) | J.S. Bach | Pipe organ, ideally a modern recording on a large instrument |
| Symphony No. 5, opening | Beethoven | Strong contrabass writing, well-known reference |
| Symphony No. 9, scherzo | Beethoven | Heavy use of low strings and timpani |
| Symphony No. 3 ("Eroica"), funeral march | Beethoven | Sustained low writing |

### Selection Status

- [x] Bach organ piece selected: Passacaglia and Fugue in C minor (BWV 582) — `Bach_Fugue_in_C-minor.wav` acquired, spectrogram generated
- [ ] Beethoven excerpt selected: _____
- [ ] Source files acquired and verified lossless

### Argument from this section

There IS bass here, but it floors out around 30-40 Hz, lives in specialized instruments (organ, contrabass), and is structurally subordinate to the harmony rather than centrally foregrounded.

---

## Section 4: Rock

### Candidates

| Track | Artist | Year | Notes |
|-------|--------|------|-------|
| When the Levee Breaks | Led Zeppelin | 1971 | Iconic kick drum sound, foundational reference |
| Kashmir | Led Zeppelin | 1975 | Heavy bass and drum production |
| War Pigs | Black Sabbath | 1970 | Heavy low end |
| Another Brick in the Wall Pt. 2 | Pink Floyd | 1979 | Stadium-era production |

### Selection Status

- [ ] Primary track selected: _____
- [ ] Optional contrast track (early 60s rock with quieter bass): _____
- [ ] Source files acquired and verified lossless

### Argument from this section

Rock takes the existing acoustic-instrument frequency range and makes it LOUD and CENTRAL through amplification and recording practice. The floor doesn't move down, but the bass becomes a felt physical presence rather than harmonic support.

---

## Section 5: Dub / Electronic

### Candidates

| Track | Artist | Year | Notes |
|-------|--------|------|-------|
| King Tubby Meets Rockers Uptown | Augustus Pablo / King Tubby | 1976 | Canonical early dub |
| Heavyweight Dub Champion | Scientist | 1980 | Pure dub showcase |
| Tracks from "Super Ape" | Lee "Scratch" Perry | 1976 | Classic Black Ark production |
| Untrue (album cuts) | Burial | 2007 | Modern descendant for lineage gesture |

### Selection Status

- [ ] Primary dub track selected: _____
- [ ] Optional descendant track (techno or dubstep) for forward-gesture: _____
- [ ] Source files acquired and verified lossless

### Argument from this section

The aesthetic break: synthesizer/electronic processing and sound system culture push the floor BELOW the acoustic limit, into sub-30 Hz territory, and treat that territory as primary content rather than support. The bass is the song.

---

## Section 6: Hip-Hop

### Candidates

| Track | Artist | Year | Notes |
|-------|--------|------|-------|
| Mask Off | Future | 2017 | Iconic 808, prominent sub-bass |
| Fuck Up Some Commas | Future | 2014 | Clean 808 signature |
| March Madness | Future | 2015 | DS2-era spectral aggression |
| Tracks from DS2 | Future | 2015 | Album-level option |

### Selection Status

- [x] Primary Future track selected: Mask Off (2017) — `Future_Mask_off.wav` acquired, spectrogram generated, bimodal signature confirmed
- [ ] Optional historical 808 reference (early hip-hop): _____
- [ ] Source files acquired and verified lossless

### Argument from this section

Hip-hop inherits dub's low-end aesthetic via the drum machine and develops it into a genre-defining bimodal spectral signature: heavy sub-bass (the 808) + vocal range, with relatively empty space between. This shape is genuinely new in music history.

---

## Acquisition Notes

You mentioned access through Columbia. Some likely sources:
- **Columbia Music Library** (Dodge Hall) — physical collections including LPs
- **Naxos Music Library** (via Columbia subscription) — strong on classical
- **Alexander Street Press** (via Columbia subscription) — has jazz, popular, and world music
- **Smithsonian Folkways** (via Columbia subscription) — possibly relevant for dub/reggae

For tracks not available through institutional access, purchasing from Bandcamp or HDtracks gets you actual lossless files rather than streaming derivatives.

## Testing Workflow

Once you have candidate WAVs in `audio/raw/`:

```bash
# Normalize all candidates
python analysis/normalize_loudness.py

# Compute spectrograms for all candidates
python analysis/compute_spectrograms.py

# Generate side-by-side preview PNGs
python analysis/generate_previews.py

# Look at the previews in analysis/previews/ and decide
```

After selection, copy or symlink the chosen tracks into `audio/canonical/` and update this document with final choices.
