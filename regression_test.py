from pathlib import Path
from acid_data import WATER_ACIDS, DMSO_ACIDS, CORE_25_IDS, EXTENDED_50_IDS

assert len(WATER_ACIDS) == 63
assert len(DMSO_ACIDS) == 24
assert len(CORE_25_IDS) == 25
assert len(EXTENDED_50_IDS) == 50
assert len(set(CORE_25_IDS)) == 25
assert len(set(EXTENDED_50_IDS)) == 50
assert {a['id'] for a in DMSO_ACIDS}.issubset({a['id'] for a in WATER_ACIDS} | {
    'phenylthio_methyl_phenyl_sulfone','phenylthio_acetonitrile','phenylacetonitrile',
    'benzyl_phenyl_sulfide','methyl_phenyl_sulfone','nn_diethylacetamide','phenylacetylene'
})

app_source = Path('app.py').read_text(encoding='utf-8')
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

print('Acid Battle v0.0.5 regression: PASS')

# The standalone game must deal one physical copy of every selected acid to
# each side, matching the original trainer Acid Battle model.
assert "const physical=shuffle(pool.map" not in app_source
assert "streamlit:render" not in app_source
assert "Each selected acid appears once in your starting deck" in app_source
print('Acid Battle v0.0.6 balanced-deck/control regression: PASS')
