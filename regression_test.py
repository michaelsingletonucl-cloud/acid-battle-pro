from acid_data import WATER_ACIDS, CORE_25_IDS, EXTENDED_50_IDS, DMSO_ACIDS
from rdkit import Chem

assert len(WATER_ACIDS) == 63
assert len(CORE_25_IDS) == 25
assert len(EXTENDED_50_IDS) == 50
assert len(DMSO_ACIDS) == 24

water_ids = [x['id'] for x in WATER_ACIDS]
dmso_ids = [x['id'] for x in DMSO_ACIDS]
assert len(water_ids) == len(set(water_ids))
assert len(dmso_ids) == len(set(dmso_ids))
assert set(CORE_25_IDS).issubset(water_ids)
assert set(EXTENDED_50_IDS).issubset(water_ids)

assert next(x for x in WATER_ACIDS if x['id']=='triflic_acid')['pka'] == -16.0
assert next(x for x in WATER_ACIDS if x['id']=='water')['pka'] == 15.7
assert next(x for x in WATER_ACIDS if x['id']=='methane')['pka'] == 50.0
assert next(x for x in WATER_ACIDS if x['id']=='pyridinium')['ref'] == 'pyridine'

assert next(x for x in DMSO_ACIDS if x['id']=='acetic_acid')['pka'] == 11.6
assert next(x for x in DMSO_ACIDS if x['id']=='water')['pka'] == 31.4
assert next(x for x in DMSO_ACIDS if x['id']=='toluene')['estimated'] is True
assert next(x for x in DMSO_ACIDS if x['id']=='methane')['pka'] == 55.0

for row in WATER_ACIDS + DMSO_ACIDS:
    if row.get('smiles'):
        assert Chem.MolFromSmiles(row['smiles']) is not None, (row['id'], row['smiles'])

print('Acid Battle regression: PASS')

app_source = __import__('pathlib').Path('app.py').read_text(encoding='utf-8')
for marker in ['id="sound"', 'function sfxFlip', 'function sfxCorrect', 'function sfxWrong', '@keyframes cardFlip', "localStorage.setItem('acidBattleMuted'"]:
    assert marker in app_source, marker
