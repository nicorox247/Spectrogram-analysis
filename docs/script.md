# Script — Full Draft (Revised)

Target: ~20 minutes total. Voice ~150 wpm.

Conventions:
- `[VISUAL: ...]` — what's on screen
- `[AUDIO: ...]` — audio examples (under 2 min total across the whole video)
- `[SOURCE: ...]` — citation placeholder, fill with specific page numbers when sourced
- `[B-ROLL: ...]` — visual filler (images, archival footage, etc.)

Voiceover text is written to be spoken aloud. Lines in **bold** are the load-bearing claims of each section.

**Narrative arc:** Hook → Establish what the FT is, as a tool for *analysis* only → Use it as a microscope on acoustic instruments → Pivot moment: the FFT arrives, and you can run the process in reverse → Cascade of consequences (synthesis, sampling, Auto-Tune) → Reflection → Close.

---

## Section 1: Cold Open with Hook (1 min, ~150 words)

`[VISUAL: Title card — black background, white text — "What does..."]`
`[B-ROLL: Portrait of Joseph Fourier, the famous 1820s lithograph, fades in]`

VOICEOVER:
> What does this French mathematician from the 1820s...

`[VISUAL: Cuts to a montage — Future, Drake, Migos, performance footage or album art]`
`[AUDIO: ~5 seconds of an obviously Auto-Tuned hip-hop hook, full volume]`

VOICEOVER:
> ...have to do with these guys?

`[VISUAL: Slight pause, hold on the contrast. Then text appears: "more than you'd think."]`

VOICEOVER:
> A lot, actually. Joseph Fourier was studying heat. How it flows through metal bars. The math he invented to do that — almost two hundred years ago — turns out to be the same math behind Auto-Tune. And synthesizers. And the 808 drum machine. And sampling. And basically every digital sound you've heard today.

`[VISUAL: Title card — final project title]`

VOICEOVER:
> This is the story of how a heat equation became the secret foundation of modern music.

---

## Section 2: What the Fourier Transform Is (3.5 min, ~525 words)

### 2a — The intuitive math (~2 min)

`[VISUAL: A simple sine wave drawn on screen, oscillating]`

VOICEOVER:
> Let's start with the simplest possible sound: a pure tone. A single frequency. Visually, it looks like this — a sine wave. Mathematically, it's the cleanest sound that exists.

`[AUDIO: 1 second of a 440 Hz sine tone]`

VOICEOVER:
> But almost no real sound is this simple. A violin playing the exact same note...

`[AUDIO: 2 seconds of a violin playing A4]`
`[VISUAL: Waveform of the violin, much more complex than the sine]`

VOICEOVER:
> ...looks like this. Same note. Vastly more complex shape. That complexity is what makes a violin sound like a violin and not a sine wave generator.

`[VISUAL: animate_resynthesis.py — violin_A4, progressive version reveal. Start at v1 (fewest components, ~6). The individual sine waves scroll left as oscillating lines, each at a different frequency and speed. The cyan sum wave shows below. Cut between versions as voiceover progresses, ending on the full reconstruction closing.]`

**VOICEOVER:**
> **Here's Fourier's insight: every complex sound, no matter how messy it looks, can be broken down into a sum of pure sine waves at different frequencies and intensities.** A violin note isn't one sound. It's many sine waves layered together — a fundamental tone plus its harmonics plus a little noise from the bow on the string.

`[VISUAL: Transition to a spectrogram of the violin note]`

VOICEOVER:
> A spectrogram is a tool that shows you those component frequencies directly. Time goes left to right. Frequency goes bottom to top. Brightness shows intensity. When you see horizontal lines stacked on top of each other, you're seeing the harmonics that make up a single musical note.

`[VISUAL: Highlight the harmonic stack with frequency labels]`

VOICEOVER:
> The Fourier transform is the math that takes a sound and gives you this picture. It's the bridge between what we hear and what's actually inside the sound.
> [SOURCE: Sethares, *Tuning, Timbre, Spectrum, Scale*, intro chapters]

### 2b — A little history (~1.5 min)

`[B-ROLL: Portrait of Joseph Fourier, image of his 1822 treatise]`

VOICEOVER:
> Fourier published this idea in 1822. He wasn't thinking about music at all. He was a French mathematician trying to understand how heat propagates through solid objects — how a hot metal bar cools down over time.

> But the math turned out to be so general that it applied to almost anything that oscillates or varies. Light, sound, electricity, waves of any kind. For most of the next century, it lived in math textbooks and physics labs. Beautiful, useful, but not exactly fast — these calculations were done by hand, and they took forever.

**VOICEOVER:**
> **For now, let's just use it as a microscope. Let's use the Fourier transform to look at what acoustic music actually sounds like.**

---

## Section 3: Acoustic Timbre (4 min, ~600 words)

`[VISUAL: Section title — "Part 1: The Sound of Things"]`

VOICEOVER:
> For most of music history, the sounds available to us were the sounds of physical objects. Wood, strings, metal, breath. Let's look at three of them.

`[AUDIO: 3 seconds of a violin sustaining a note]`
`[VISUAL: animate_spectrogram.py — violin_A4, full duration. Spectrogram sweeps in real time showing the bright harmonic stack.]`

VOICEOVER:
> A violin playing a sustained A — 440 Hz. The kind of note that anchors a Beethoven slow movement, or a Mahler symphony. Watch the spectrogram. There's a bright line at the bottom — that's the fundamental, the 440. But look above it. 880 Hz. 1320. 1760. 2200. 2640. These are the violin's *harmonics* — integer multiples of the fundamental, all sounding at once.

`[VISUAL: Highlight a few harmonic lines with their frequency values]`
`[VISUAL: Cut to animate_resynthesis.py — violin_A4, closing segment only (150 components, sum wave). Shows the reconstructed waveform scrolling — this is what those stacked harmonics sound like when reassembled.]`

VOICEOVER:
> The pattern of which harmonics are loud and which are quiet — that's what makes a violin sound like a violin and not a flute or a trumpet.

`[AUDIO: 3 seconds of a flute playing A4]`
`[VISUAL: Spectrogram of the flute note]`

VOICEOVER:
> Here's a flute. Same note, completely different fingerprint. The higher harmonics are much weaker — flutes are nearly pure tones compared to violins. And see this fuzzy haze across the whole spectrogram? That's breath noise — air rushing past the embouchure hole. It's part of why a flute sounds airy and a violin doesn't. Debussy knew this. So did every composer who ever wrote a flute solo.

`[AUDIO: 3 seconds of a piano playing A4]`
`[VISUAL: Spectrogram of the piano note]`

VOICEOVER:
> And here's a piano. Sharp attack — see how everything lights up the moment the hammer strikes. Then a long, slow decay. Pianos also have what's called inharmonic content — small frequencies that aren't part of the perfect harmonic series, caused by the stiffness of the steel strings. That slight imperfection is part of what gives the piano its characteristic warmth. It's part of why the same notes feel different in the hands of Glenn Gould versus Vladimir Horowitz.

`[VISUAL: Three spectrograms side by side — violin, flute, piano — all playing the same note]`

**VOICEOVER:**
> **Same note. Three completely different spectral fingerprints. This is what we mean by *timbre* — the unique pattern of frequencies that distinguishes one instrument from another.**
> [SOURCE: Sethares on the harmonic series and timbre]

VOICEOVER:
> Every instrument in the orchestra has a fingerprint like this. The buzzy edge of an oboe. The mellow round of a French horn. The metallic ping of a triangle. And for thousands of years, this palette of timbres was *fixed*. It was determined by the physics of vibrating strings, columns of air, stretched membranes. Stradivari refined the violin in the 1700s. Sébastien Érard refined the piano in the 1800s. Every composer who ever wrote for orchestra — Bach, Mozart, Brahms, Stravinsky — worked within the available palette of physical objects.

> The available timbres were the available materials. You couldn't *make* a new instrument any more than you could make a new color out of thin air.

> Then in the 1960s, that started to change.

`[VISUAL: Hold on the silence for a beat before transitioning]`

---

## Section 4: The Pivot and Synthesis (5.5 min, ~825 words)

### 4a — The Pivot (~45 sec)

`[VISUAL: Section title — "Part 2: Making Sound from Math"]`

`[B-ROLL: Photos of early IBM computers, the kind Cooley and Tukey would have worked with]`

VOICEOVER:
> In 1965, two mathematicians named James Cooley and John Tukey published an algorithm called the Fast Fourier Transform — the FFT. They didn't change Fourier's math. They just made it dramatically faster. Fast enough to run on a computer in real time.
> [SOURCE: Heideman, Johnson, Burrus, "Gauss and the History of the Fast Fourier Transform," 1985]

`[VISUAL: animate_resynthesis.py — violin_A4, full video. Begin with v1 (fewest components — thin, ghostly sound). Progress through versions as voiceover builds. The viewer watches and hears the violin emerge from pure sine waves. End on the closing (150-component sum). This IS the dramatic reveal — the same animation from Section 2 is now reframed as construction, not just decomposition.]`

**VOICEOVER:**
> **And here's the moment everything changes. If the Fourier transform can take a sound and break it down into pure sine waves — then in principle, you can run the process in reverse. You can start with sine waves, combine them in whatever amounts you want, and *build* a sound that's never existed before.**

> Timbre stops being a property of physical objects. It becomes something you can design.

### 4b — Moog and early synthesis (~2 min)

`[B-ROLL: Photos of early Moog synthesizers, Robert Moog at the controls, Wendy Carlos "Switched-On Bach" album cover]`

VOICEOVER:
> Robert Moog was one of the first people to build a machine that did exactly this. Starting in the mid-1960s, the Moog synthesizer let you generate pure sine waves and other simple waveforms, shape their envelopes, layer them, filter them. You weren't recording vibrating objects anymore. You were *designing* sound from scratch, the way a sculptor works clay.
> [SOURCE: Pinch and Trocco, *Analog Days*]

`[AUDIO: 5 seconds of an early Moog sound — Wendy Carlos's "Switched-On Bach" or a classic Moog patch]`
`[VISUAL: Spectrogram of the Moog sound]`

VOICEOVER:
> Listen to what a Moog sounds like. And look at the spectrogram. Compare it to the violin from a few minutes ago. Notice how *clean* it is. The frequencies are bright, sharp, almost mathematically precise. There's no breath noise, no bow scratch, no inharmonic warmth from a vibrating physical object. This is sound built directly from equations.

### 4c — DX7 and FM synthesis (~1.5 min)

`[B-ROLL: Photos of the Yamaha DX7, 80s pop production]`

VOICEOVER:
> By 1983, the Yamaha DX7 took this idea mainstream. The DX7 used a technique called FM synthesis — short for frequency modulation — which is, no exaggeration, *literally* Fourier mathematics applied to making sounds. You take one sine wave and use it to modulate the frequency of another sine wave, and out pops a complex spectrum you can shape with precision.
> [SOURCE: Chowning, "The Synthesis of Complex Audio Spectra by Means of Frequency Modulation," 1973]

`[AUDIO: 5 seconds of a recognizable DX7 patch — the famous "electric piano" or "bass" sound]`
`[VISUAL: Spectrogram of the DX7 patch]`

VOICEOVER:
> If you grew up listening to 80s pop, this is the sound of your childhood. Whitney Houston's "Greatest Love of All." The keyboard riffs in countless ballads. That distinctive bright, glassy, slightly artificial shimmer. That sound *is* Fourier math.

### 4d — Contemporary synths (~1.25 min)

`[AUDIO: 5 seconds of a contemporary track with prominent synth — Daft Punk, The Weeknd, or similar]`
`[VISUAL: Spectrogram with annotations highlighting the synthesized elements]`

VOICEOVER:
> And it kept going. Today, almost every pop song you hear contains timbres that have no acoustic origin. The bass in trap music, the leads in EDM, the pads in pop ballads — these aren't recordings of instruments. They're mathematical constructs, generated by software synthesizers that descend directly from Moog and the DX7, descending directly from Fourier.

**VOICEOVER:**
> **Timbre, which used to be a property of physical objects, became a property of mathematical manipulation. You can edit it. You can copy it. You can save it as a file.**

---

## Section 5: Sampling and Digital Manipulation (3 min, ~450 words)

`[VISUAL: Section title — "Part 3: The Sound of Other Sounds"]`

VOICEOVER:
> Synthesis was one revolution. Sampling was the other.

`[B-ROLL: Photos of early samplers — the Fairlight CMI, the E-mu SP-1200, the Akai MPC]`

VOICEOVER:
> Starting in the late 1970s, digital samplers let producers do something equally radical: take any existing sound — a drum hit, a vocal phrase, a horn stab from an old jazz record — and treat it as raw material. You could chop it up, pitch-shift it, time-stretch it, layer it with other samples. Every transformation depended on Fourier-based digital signal processing.

`[AUDIO: 5 seconds of a clearly sampled hip-hop track — early De La Soul, A Tribe Called Quest, or contemporary trap]`
`[VISUAL: Spectrogram with sampled elements identified]`

VOICEOVER:
> Hip-hop is, in a sense, the first genre built entirely around this idea. The drum break from an old funk record, isolated, looped, manipulated, becomes the backbone of a new song. The history of recorded music gets recycled into new music. And the tool that makes this possible — that lets you cleanly cut, stretch, and pitch-shift digital audio — is Fourier analysis.
> [SOURCE: Schloss, *Making Beats*]

`[AUDIO: 3 seconds of an unprocessed vocal]`
`[VISUAL: Spectrogram of clean vocal]`
`[AUDIO: 3 seconds of the same or similar vocal with obvious Auto-Tune]`
`[VISUAL: Spectrogram with Auto-Tune artifacts visible — quantized pitch transitions]`

VOICEOVER:
> Or take Auto-Tune. Released in 1997, it does exactly what you'd expect from a piece of Fourier-derived software: it analyzes the frequency of a voice in real time, and shifts that frequency to land exactly on the nearest note in a chosen scale. You can hear the effect. You can see it on the spectrogram — pitch movements that snap rather than slide.

> Auto-Tune was originally meant to fix small mistakes invisibly. But T-Pain in the mid-2000s, and then a generation of hip-hop and pop artists, used it as an effect. The artificial quality became the aesthetic.

**VOICEOVER:**
> **Every modern music production environment is a Fourier-domain workspace. Pitch correction, time-stretching, noise reduction, compression, EQ, reverb — almost everything a producer does involves manipulating the frequency content of a signal.**

---

## Section 6: How This Changed What We Hear (2 min, ~300 words)

`[VISUAL: Section title — "What it means"]`
`[B-ROLL: Quick montage of contemporary music videos, streaming app interfaces, production software, headphones]`

VOICEOVER:
> Step back for a moment. What does all of this add up to?

> Two hundred years ago, music was made by physical objects. Wood, strings, breath, hands. Every sound had a body. Every timbre was the signature of a specific material thing vibrating in a specific way.

> Today, an enormous fraction of the music we listen to contains sounds that have no physical body at all. Synthesizers produce timbres that no instrument could produce. Samplers fragment and recombine sounds from across history. Auto-Tune turns the human voice into a quantized object. Digital effects reshape sound in ways no acoustic process could.
> [SOURCE: Sterne, *The Audible Past*, on reproduction and cultural reception]

> And we don't really notice. We've grown up listening to this. The line between "real" and "synthetic" sound has eroded to the point of being almost invisible. A pop song today might contain dozens of sounds that exist only as mathematical objects — Fourier components combined into something we hear as music.

**VOICEOVER:**
> **The instruments are now mathematical. The voices are processed. The music is, in a very real sense, made of numbers.**

---

## Section 7: Conclusion (1 min, ~150 words)

`[VISUAL: Slow fade back to the Fourier portrait from the opening]`

VOICEOVER:
> Joseph Fourier died in 1830. He never heard a synthesizer. He never heard a recording. He probably never imagined that his work on heat conduction would, two centuries later, be running inside every phone, every speaker, every streaming service on the planet.

> Cooley and Tukey, who built the algorithm that made it all practical, were doing applied math for the Cold War. They weren't thinking about music either.

> But every sound from a screen, every drop in a club, every Auto-Tuned hook, every sampled breakbeat — passed through their math. The Fourier transform wasn't designed to change music. It just happened to be the right idea, sitting around for the right amount of time, until the technology caught up and people figured out what it was actually good for.

`[VISUAL: Final card with a short tagline]`

VOICEOVER:
> Not bad for a guy studying hot metal bars.

`[VISUAL: Fade to credits / sources card]`

---

## Timing Summary

| Section | Duration | Word target |
|---------|---------:|------------:|
| 1. Cold open | 1.0 min | 150 |
| 2. What the FT is | 3.5 min | 525 |
| 3. Acoustic timbre | 4.0 min | 600 |
| 4. Pivot + Synthesis | 5.5 min | 825 |
| 5. Sampling & manipulation | 3.0 min | 450 |
| 6. What it means | 2.0 min | 300 |
| 7. Conclusion | 1.0 min | 150 |
| **Total** | **20.0 min** | **~3000** |

Audio examples used: ~8 short clips totaling under 2 minutes per rubric.
