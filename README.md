# Acid Battle v0.0.7

Standalone physical-organic-chemistry Acid Battle game.

## v0.0.7 fixes

- Restores the balanced dealing model from the original Organic Chemistry Trainer Acid Battle.
- A deck choice counts **unique acid types**, not total physical cards.
- Each selected acid is duplicated once: one copy begins on the player side and one on the computer side.
  - 25 acids = 50 physical cards (25 per side)
  - 50 acids = 100 physical cards (50 per side)
  - Whole H2O list = 126 physical cards (63 per side)
  - Whole DMSO list = 48 physical cards (24 per side)
- This prevents one player from being randomly dealt the only copy of the strongest acid.
- Reworked home-screen solvent/deck controls to use direct in-iframe state rather than Streamlit render-message state.
- Setup controls now use robust delegated click handling and explicit pressed/disabled states.
- Retains sound effects, mute, card animation, mobile layout, H2O/DMSO reference scales, and Streamlit Cloud Linux packages.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```


## v0.0.7
- Fixed molecular structure images being squeezed into narrow vertical strips on cards.
- Structures now render inside an absolutely positioned viewport, independent of card flex sizing.
- RDKit depictions use `fitImage=True` and a larger source canvas for improved readability.
- Mobile card structure sizing updated to use the same robust viewport layout.
