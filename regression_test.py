from pathlib import Path
from acid_data import WATER_ACIDS, DMSO_ACIDS, CORE_25_IDS, EXTENDED_50_IDS

assert len(WATER_ACIDS) == 63
assert len(DMSO_ACIDS) == 24
assert len(CORE_25_IDS) == 25
assert len(EXTENDED_50_IDS) == 50
assert len(set(CORE_25_IDS)) == 25
assert len(set(EXTENDED_50_IDS)) == 50

# Correct aromatic imidazolium representation.
imid = next(a for a in WATER_ACIDS if a['id'] == 'imidazolium')
assert imid['smiles'] == '[nH]1cc[nH+]c1'

app_source = Path('app.py').read_text(encoding='utf-8')
sql_source = Path('supabase_leaderboard_setup.sql').read_text(encoding='utf-8')

for marker in [
    'YOUR HAND — CHOOSE ONE CARD',
    'LOWER pKa WINS • CAPTURE THE WHOLE DECK',
    'function refillHand()',
    'function prepareCpu()',
    'function playCard(',
    'function advance(',
    'warPot.push(player,opp)',
    "p.push(makeInstance(card,'P',i))",
    "c.push(makeInstance(card,'C',i))",
    "components.html(html, height=1080, scrolling=False)",
    "$('setup').addEventListener('click'",
    'playerWon.push(...warPot.splice(0),player,opp)',
    'cpuWon.push(...warPot.splice(0),player,opp)',
    'function sfxFlip',
    'function sfxWin',
    'function sfxLoss',
    'function toggleSound',
    "localStorage.setItem('acidBattleMuted'",
    '@media(max-width:680px)',
    'overflow-x:auto',
]:
    assert marker in app_source, marker

# Balanced and randomized pools: same acid types for both players, independently shuffled.
assert "pool=shuffle(list.slice()).slice(0,n)" in app_source
assert "return[shuffle(p),shuffle(c)]" in app_source

# v0.0.10+ account / leaderboard / strategy features.
for marker in [
    'PLAY AS GUEST',
    'SIGN IN / CREATE PLAYER',
    'Remember your nickname and 4-digit PIN',
    'There is no PIN recovery',
    'function analyzeOptimal(',
    "rpc('acid_record_move'",
    "rpc('acid_finish_game'",
    'STRATEGY_MIN=20',
    'Acid Battle Leaderboards',
    '🏆 WINS',
    '🎯 STRATEGY',
    'SUPABASE_PUBLISHABLE_KEY',
    'SUPABASE_ANON_KEY',
]:
    assert marker in app_source, marker

# The browser payload must never use the service/secret key.
assert '_secret_value("SUPABASE_SECRET_KEY")' not in app_source

for marker in [
    'create table if not exists public.acid_sessions',
    'create or replace function public.acid_create_player',
    'create or replace function public.acid_login_player',
    'create or replace function public.acid_start_game',
    'create or replace function public.acid_record_move',
    'create or replace function public.acid_finish_game',
    'create or replace function public.acid_leaderboard',
    'revoke all on table public.acid_players from anon, authenticated',
    'grant execute on function public.acid_leaderboard(text) to anon',
]:
    assert marker in sql_source, marker

# v0.0.13 accessibility + animation defaults.
for marker in [
    '♿ Accessibility',
    'aria-live="polite"',
    'aria-modal="true"',
    "setAttribute('role','button')",
    "e.key==='Enter'||e.key===' '",
    'focus-visible',
    'Reduce motion',
    'Manual result advance',
    'NEXT TRICK',
    'function announce(',
    'function loadAccessibilityPrefs(',
    'user-scalable=no',
]:
    if marker == 'user-scalable=no':
        assert marker not in app_source, marker
    else:
        assert marker in app_source, marker

assert '@media(prefers-reduced-motion:reduce)' not in app_source
assert "function sparks(card){if(reduceMotion)return;" in app_source
assert '⚠ NOT OPTIMAL' in app_source
assert "reduceMotion=r==='1'" in app_source
assert 'Reduce motion is OFF by default' in app_source
print('Acid Battle v0.0.13 regression: PASS')
