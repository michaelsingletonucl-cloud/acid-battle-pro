# Acid Battle v0.0.14

Standalone physical-organic-chemistry Acid Battle game for Streamlit.

## New in v0.0.14 — full motion by default

- **Reduce motion now defaults to OFF**, so card flips, shakes, sparks, and transitions are enabled for new users.
- A user who explicitly turns Reduce motion ON still keeps that preference in the browser for later visits.
- The Accessibility panel continues to provide the motion toggle and manual result advance option.
- Card flips, brighter sparks, and high-contrast **NOT OPTIMAL** feedback from v0.0.12 are retained.

## Accessibility features retained from v0.0.11

This release adds an accessibility layer targeting the practical requirements of **WCAG 2.1 AA** for the game interface. It is not a formal accessibility certification.

- All playable acid cards are keyboard-focusable controls.
- **Tab / Shift+Tab** moves through controls and cards; **Enter / Space** plays a focused card.
- High-visibility `:focus-visible` outlines are provided for buttons, inputs, cards, and dialog controls.
- Playable cards have explicit accessible names stating the acid name, whether pKa is hidden/revealed, and the keyboard action.
- Decorative molecular PNGs are hidden from screen readers to avoid duplicate announcements; the card itself carries the accessible name.
- Live regions announce CPU plays, trick outcomes, strategy feedback, login errors, and game-over results.
- Correct/loss/tie/optimal outcomes are always written in text; color and sound are never the only cues.
- Nickname and PIN fields use explicit labels and descriptive error/status messaging.
- Leaderboard and Accessibility overlays are marked as modal dialogs and restore focus when closed.
- Leaderboard tabs expose selected state to assistive technology.
- Browser pinch-to-zoom is enabled; the mobile layout was retested at 200% zoom without page-level horizontal overflow.
- A new **♿ Accessibility** panel is available from the top bar.
- **Reduce motion** can disable card flips, shakes, sparks, and most transitions; it is OFF by default.
- **Manual result advance** can turn off the automatic result timer so each trick result remains visible until the player chooses **Next trick**.
- Sound remains optional and independently mutable with the existing sound toggle.
- Mobile top controls now use a two-column touch-friendly layout so Accessibility and Leaderboards remain reachable on narrow screens.

## Player / leaderboard features retained from v0.0.10

- Entry screen: **Play as Guest** or **Sign in / Create Player**.
- Player profiles use only a **nickname + 4-digit PIN**.
- Clear reminder that students must remember both; there is no PIN recovery.
- Nickname screening for length/characters and common inappropriate names.
- Persistent Supabase records scoped automatically to the hidden `COURSE_CODE`.
- Every signed-in move is recorded as it is played.
- **Optimal move** rule:
  - if a winning card exists, use the least acidic card that still wins;
  - if no card can win, sacrifice the least acidic card in the hand.
- **Wins leaderboard**: total completed game wins.
- **Strategy leaderboard**: optimal-move percentage, minimum **20 recorded moves**.
- Unfinished games do not count as wins, but already-recorded moves still count toward strategy.
- Randomized balanced decks, H2O/DMSO scales, card sounds, animations, fullscreen, and smartphone layout are retained.

## Supabase

No new database migration is required when upgrading from v0.0.10. Continue using the same `supabase_leaderboard_setup.sql` and Streamlit Secrets.

```toml
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_PUBLISHABLE_KEY = "sb_publishable_..."
COURSE_CODE = "TAMU610"
```

Do not put a Supabase secret/service-role key in GitHub or browser code.

## Deploy

Upload/replace the repository contents in GitHub. Streamlit Community Cloud should redeploy automatically.

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Guest mode works even when Supabase is not configured.


## v0.0.14 feedback changes
- Trick outcome is now the dominant feedback: TRICK WON, TRICK LOST, or TIE — WAR POT.
- Result panel is visually keyed to win/loss/tie independently of strategy quality.
- Strategy feedback is shortened to OPTIMAL MOVE or STRATEGY: NOT OPTIMAL.
- Non-optimal feedback no longer reveals the best card.
