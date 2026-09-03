# Acid Battle v0.0.3

Standalone Streamlit physical-organic chemistry game.

## Reference decks
- **H2O:** 63 reference acids. Curated 25-card and 50-card pools plus All 63.
- **DMSO:** 24 reference acids from the supplied course table. Because this scale currently contains fewer than 25 entries, the UI automatically selects **All 24** and disables 25/50. Those options enable automatically if the DMSO dataset is later expanded.
- Asterisks from the supplied reference tables are preserved as `estimated=True`.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

The interface is responsive for desktop and portrait smartphone use.


## v0.0.3 interaction polish
- Browser-synthesized card/deal flip sound, correct cue, wrong cue, tie cue, and a stronger cue every 5-answer streak.
- No bundled third-party audio assets and no sound licensing/attribution dependency.
- Synchronized 3D card-flip reveal animation plus deal-in motion for each new battle.
- Persistent **Sound on / Muted** control using browser local storage; on phones it collapses to a large touch-friendly speaker icon.
- Sound is initialized from a user gesture so it behaves correctly with normal mobile browser autoplay restrictions.
