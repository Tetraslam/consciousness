# Demo Guide – Consciousness as Error Correction

*A concise, no-fluff walkthrough of exactly what to show judges & visitors.*

---

## 0. Prep (2 min before demo)
1. Clone repo & install deps:
   ```bash
   git clone <repo>
   cd consciousness
   uv sync   # or: pip install -r requirements.txt
   ```
2. **Open two terminals**:
   - **Term A** – for the live interactive demo  
   - **Term B** – ready to cat / open static figures if asked

---

## 1. Live Interactive Demo (core – 90 s)
Run once, keep on projector while you talk:
```bash
uv run demo/interactive_consciousness_demo.py
```

### What the audience sees
| Area | What to point out | Citation |
|------|------------------|----------|
| Neural Activity heat-map | 10 modules × 100 neurons. Red/blue = firing rate.| Fiete et al., 2011 – grid cells as error-correcting code. |
| Consciousness plot | Sharp jump > 0.3 error-correction (EC) | Zlokapa et al., 2024 – fault-tolerant phase transition. |
| Phase-space scatter | Trajectory stabilises only when EC > 0.3 | Hardcastle et al., 2015 – error accumulation ↔ correction. |
| Metric bars | Noise-suppression, integration… show objective scores | qCON & BIS monitors use similar EEG metrics (Harsha 2022). |

### Scripted Flow (speak + click)
1. **Start** (press *Start*). Leave EC ≈ 0.0 → chaotic heat-map, low consciousness (< 0.05).
2. **Slide EC ➔ 0.4**. Point at instant jump on blue curve; scatter collapses to tight loop ⇒ *"This is the moment consciousness emerges"*.
3. **Toggle Noise slider** high/low – show robustness plateau after EC threshold.
4. **Reset** – quick repeat if judges want.

*Total time: ≤ 90 seconds.*

---

## Need the figures afterwards?
Run the gallery script:
```bash
uv run scripts/view_gallery.py
```

This cycles through all PNGs in `visualizations/` one after another.

---

## Key Citations (quick list)
1. Fiete, I. et al. 2011. *Grid cells generate an analog error-correcting code.* Nature Neuroscience.
2. Hardcastle, K. et al. 2015. *Environmental Boundaries as an Error Correction Mechanism for Grid Cells.* Neuron.
3. Zlokapa, A. et al. 2024. *Biological error correction codes generate fault-tolerant neural networks.* arXiv.
4. Rolls, E.T. 2020. *Higher Order Syntactic Thought Theory.* Frontiers in Psychology.
5. Harsha, M.S. et al. 2022. *Quantium Consciousness Index in ICU Patients.* Indian J Crit Care Med.

---

## That's it
*"Consciousness is what error correction feels like."* Run the live demo, slide EC above 0.3, drop the mic. 