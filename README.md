# Acid Battle v0.0.10

Standalone physical-organic-chemistry Acid Battle game for Streamlit.

## New in v0.0.10

- Entry screen: **Play as Guest** or **Sign in / Create Player**.
- Player profiles use only a **nickname + 4-digit PIN**.
- Clear reminder that students must remember both; there is no PIN recovery.
- Nickname screening for length/characters and common inappropriate names.
- Persistent Supabase records scoped automatically to the hidden `COURSE_CODE`.
- Every signed-in move is recorded as it is played.
- **Optimal move** rule:
  - if a winning card exists, use the least acidic card that still wins;
  - if no card can win, sacrifice the least acidic card in the hand.
- Strategy feedback appears after every move in both Guest and Player modes.
- **Wins leaderboard**: total completed game wins.
- **Strategy leaderboard**: optimal-move percentage, minimum **20 recorded moves**.
- Unfinished games do not count as wins, but already-recorded moves still count toward strategy.
- Existing randomized balanced decks, H2O/DMSO scales, card sounds, mute, animations, fullscreen, and smartphone layout are retained.

## One-time Supabase migration

The original three tables (`acid_players`, `acid_games`, `acid_moves`) should already exist.

Open **Supabase → SQL Editor → New query**, paste the entire contents of:

`supabase_leaderboard_setup.sql`

and press **Run** once. The script is written to be safe to run again if needed.

It adds the short-lived session table and restricted RPC functions used by the browser while leaving the underlying tables protected by RLS.

## Streamlit Secrets

The browser must use a **publishable** Supabase key. Do **not** expose the secret/service-role key in the app or GitHub.

Keep your existing settings and add the publishable key:

```toml
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_PUBLISHABLE_KEY = "sb_publishable_..."
COURSE_CODE = "TAMU610"
```

A legacy Supabase anon JWT can be used instead with:

```toml
SUPABASE_ANON_KEY = "eyJ..."
```

If you already stored `SUPABASE_SECRET_KEY` in Streamlit Secrets, it can remain there, but Acid Battle v0.0.10 deliberately never sends or uses it in browser code.

## Deploy

Upload/replace the repository contents in GitHub. Streamlit Community Cloud should redeploy automatically.

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Guest mode works even when Supabase is not configured.
