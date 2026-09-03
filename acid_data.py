"""Reference pKa data for Acid Battle.

Water values are the course reference values supplied by the user.  Asterisks
in the original table are retained via estimated=True.  The DMSO values are the corresponding physical-organic course reference values
supplied by the user.
"""

WATER_ACIDS = [
    # id, display name, reference label, pKa value, display, estimated, smiles
    dict(id='hf_sbf5', name='HF–SbF₅', ref='HF-SbF5', pka=None, pka_text='> CH₅⁺ in acid strength', estimated=False, smiles=None),
    dict(id='triflic_acid', name='Triflic acid', ref='CF3SO3H', pka=-16.0, pka_text='−16*', estimated=True, smiles='OS(=O)(=O)C(F)(F)F'),
    dict(id='perchloric_acid', name='Perchloric acid', ref='HClO4', pka=-10.0, pka_text='−10', estimated=False, smiles='OCl(=O)(=O)=O'),
    dict(id='hydroiodic_acid', name='Hydroiodic acid', ref='HI', pka=-10.0, pka_text='−10', estimated=False, smiles='[H]I'),
    dict(id='sulfuric_acid', name='Sulfuric acid', ref='H2SO4', pka=-9.0, pka_text='−9', estimated=False, smiles='OS(=O)(=O)O'),
    dict(id='hydrobromic_acid', name='Hydrobromic acid', ref='HBr', pka=-9.0, pka_text='−9', estimated=False, smiles='[H]Br'),
    dict(id='hydrochloric_acid', name='Hydrochloric acid', ref='HCl', pka=-7.0, pka_text='−7', estimated=False, smiles='[H]Cl'),
    dict(id='benzenesulfonic_acid', name='Benzenesulfonic acid', ref='PhSO3H', pka=-6.0, pka_text='−6', estimated=False, smiles='O=S(=O)(O)c1ccccc1'),
    dict(id='protonated_alcohol', name='Protonated alcohol', ref='ROH2+', pka=-3.0, pka_text='−3', estimated=False, smiles=None),
    dict(id='hydronium', name='Hydronium', ref='H3O+', pka=-1.7, pka_text='−1.7', estimated=False, smiles='[OH3+]'),
    dict(id='nitric_acid', name='Nitric acid', ref='HNO3', pka=-1.4, pka_text='−1.4', estimated=False, smiles='O[N+](=O)[O-]'),
    dict(id='bisulfate', name='Bisulfate', ref='HSO4−', pka=2.0, pka_text='2.0', estimated=False, smiles='OS(=O)(=O)[O-]'),
    dict(id='hydrofluoric_acid', name='Hydrofluoric acid', ref='HF', pka=3.18, pka_text='3.18', estimated=False, smiles='[H]F'),
    dict(id='acetic_acid', name='Acetic acid', ref='MeCO2H', pka=4.74, pka_text='4.74', estimated=False, smiles='CC(=O)O'),
    dict(id='carbonic_acid', name='Carbonic acid', ref='H2CO3', pka=6.35, pka_text='6.35', estimated=False, smiles='O=C(O)O'),

    dict(id='triphenylammonium', name='Triphenylammonium', ref='Ph3NH+', pka=-5.0, pka_text='−5', estimated=False, smiles='[NH+](c1ccccc1)(c2ccccc2)c3ccccc3'),
    dict(id='diphenylammonium', name='Diphenylammonium', ref='Ph2NH2+', pka=1.0, pka_text='1', estimated=False, smiles='[NH2+](c1ccccc1)c2ccccc2'),
    dict(id='anilinium', name='Anilinium', ref='PhNH3+', pka=4.6, pka_text='4.6', estimated=False, smiles='[NH3+]c1ccccc1'),
    # The source list gives the base name; Acid Battle displays the acidic conjugate-acid species.
    dict(id='pyridinium', name='Pyridinium', ref='pyridine', pka=5.3, pka_text='5.3', estimated=False, smiles='[nH+]1ccccc1', note='pKa of the conjugate acid of pyridine'),
    dict(id='imidazolium', name='Imidazolium', ref='imidazole', pka=7.0, pka_text='7', estimated=False, smiles='[nH]1cc[nH+]c1', note='pKa of the conjugate acid of imidazole'),
    dict(id='dmaph', name='DMAPH⁺', ref='4-dimethylaminopyridine', pka=10.0, pka_text='10', estimated=False, smiles='CN(C)c1cc[nH+]cc1', note='pKa of the conjugate acid of DMAP'),
    dict(id='thiophenol', name='Thiophenol', ref='PhSH', pka=8.0, pka_text='8', estimated=False, smiles='Sc1ccccc1'),
    dict(id='phenol', name='Phenol', ref='PhOH', pka=10.0, pka_text='10', estimated=False, smiles='Oc1ccccc1'),
    dict(id='alkanethiol', name='Alkanethiol', ref='RSH', pka=12.0, pka_text='12', estimated=False, smiles=None),
    dict(id='ammonium', name='Ammonium', ref='NH4+', pka=9.24, pka_text='9.24', estimated=False, smiles='[NH4+]'),
    dict(id='ethylammonium', name='Ethylammonium', ref='EtNH3+', pka=10.6, pka_text='10.6', estimated=False, smiles='CC[NH3+]'),
    dict(id='hydrogen_peroxide', name='Hydrogen peroxide', ref='HOOH', pka=11.6, pka_text='11.6', estimated=False, smiles='OO'),
    dict(id='trifluoroethanol', name='2,2,2-Trifluoroethanol', ref='CF3CH2OH', pka=12.4, pka_text='12.4', estimated=False, smiles='OCC(F)(F)F'),
    dict(id='methanol', name='Methanol', ref='MeOH', pka=15.2, pka_text='15.2', estimated=False, smiles='CO'),
    dict(id='water', name='Water', ref='H2O', pka=15.7, pka_text='15.7', estimated=False, smiles='O'),
    dict(id='ethanol', name='Ethanol', ref='EtOH', pka=16.0, pka_text='16', estimated=False, smiles='CCO'),
    dict(id='isopropanol', name='Isopropanol', ref='iPrOH', pka=16.5, pka_text='16.5', estimated=False, smiles='CC(O)C'),
    dict(id='tert_butanol', name='tert-Butanol', ref='t-BuOH', pka=18.0, pka_text='18', estimated=False, smiles='CC(C)(C)O'),
    dict(id='amide_nh', name='Amide N–H', ref='RCONH2', pka=17.0, pka_text='17', estimated=False, smiles=None),
    dict(id='ammonia', name='Ammonia', ref='NH3', pka=35.0, pka_text='35', estimated=False, smiles='N'),
    dict(id='diethylamine', name='Diethylamine', ref='Et2NH', pka=36.0, pka_text='36', estimated=False, smiles='CCNCC'),

    dict(id='tricyanomethane', name='Tricyanomethane', ref='CH(CN)3', pka=-5.0, pka_text='−5*', estimated=True, smiles='N#CC(C#N)C#N'),
    dict(id='triacetylmethane', name='Triacetylmethane', ref='CH(COCH3)3', pka=6.0, pka_text='6', estimated=False, smiles='CC(=O)C(C(C)=O)C(C)=O'),
    dict(id='dinitromethane', name='Dinitromethane', ref='CH2(NO2)2', pka=3.6, pka_text='3.6*', estimated=True, smiles='C([N+](=O)[O-])([N+](=O)[O-])'),
    dict(id='acetylacetone', name='Acetylacetone', ref='CH2(COCH3)2', pka=9.0, pka_text='9', estimated=False, smiles='CC(=O)CC(C)=O'),
    dict(id='phosphonium_ester', name='Ethoxycarbonylmethyltriphenylphosphonium', ref='Ph3P+CH2CO2Et', pka=9.2, pka_text='9.2', estimated=False, smiles='CCOC(=O)C[P+](c1ccccc1)(c2ccccc2)c3ccccc3'),
    dict(id='beta_keto_ester', name='β-Keto ester', ref='CH3COCH2COOR', pka=11.0, pka_text='11', estimated=False, smiles='CCOC(=O)CC(C)=O'),
    dict(id='malononitrile', name='Malononitrile', ref='CH2(CN)2', pka=11.2, pka_text='11.2', estimated=False, smiles='N#CCC#N'),
    dict(id='diethyl_malonate', name='Diethyl malonate', ref='CH2(COOEt)2', pka=13.0, pka_text='13', estimated=False, smiles='CCOC(=O)CC(=O)OCC'),
    dict(id='bis_methylsulfonyl_methane', name='Bis(methylsulfonyl)methane', ref='CH2(SO2Me)2', pka=13.0, pka_text='13', estimated=False, smiles='CS(=O)(=O)CS(=O)(=O)C'),
    dict(id='hydrogen_cyanide', name='Hydrogen cyanide', ref='HCN', pka=9.2, pka_text='9.2', estimated=False, smiles='C#N'),
    dict(id='acetylene', name='Acetylene', ref='HC≡CH', pka=25.0, pka_text='25', estimated=False, smiles='C#C'),
    dict(id='cyclopentadiene', name='Cyclopentadiene', ref='cyclopentadiene', pka=16.0, pka_text='16', estimated=False, smiles='C1C=CC=C1'),
    dict(id='indene', name='Indene', ref='indene', pka=20.0, pka_text='20', estimated=False, smiles='c1ccc2c(c1)CC=C2'),
    dict(id='fluorene', name='Fluorene', ref='fluorene', pka=23.0, pka_text='23*', estimated=True, smiles='c1ccc2c(c1)Cc1ccccc1-2'),
    dict(id='nitromethane', name='Nitromethane', ref='CH3NO2', pka=10.2, pka_text='10.2', estimated=False, smiles='C[N+](=O)[O-]'),
    dict(id='acetophenone', name='Acetophenone', ref='PhCOCH3', pka=16.0, pka_text='16', estimated=False, smiles='CC(=O)c1ccccc1'),
    dict(id='acetone', name='Acetone', ref='CH3COCH3', pka=20.0, pka_text='20', estimated=False, smiles='CC(=O)C'),
    dict(id='dimethyl_sulfone', name='Dimethyl sulfone', ref='CH3SO2CH3', pka=23.0, pka_text='23', estimated=False, smiles='CS(C)(=O)=O'),
    dict(id='ethyl_acetate', name='Ethyl acetate', ref='CH3CO2Et', pka=25.0, pka_text='25', estimated=False, smiles='CCOC(C)=O'),
    dict(id='acetonitrile', name='Acetonitrile', ref='CH3CN', pka=25.0, pka_text='25', estimated=False, smiles='CC#N'),
    dict(id='dmso', name='Dimethyl sulfoxide', ref='CH3SOCH3', pka=35.0, pka_text='35', estimated=False, smiles='CS(C)=O'),
    dict(id='dithiane', name='1,3-Dithiane', ref='1,3-dithiane', pka=31.0, pka_text='31', estimated=False, smiles='S1CSCCC1'),
    dict(id='triphenylmethane', name='Triphenylmethane', ref='Ph3CH', pka=33.0, pka_text='33', estimated=False, smiles='C(c1ccccc1)(c2ccccc2)c3ccccc3'),
    dict(id='toluene', name='Toluene', ref='PhCH3', pka=41.0, pka_text='41*', estimated=True, smiles='Cc1ccccc1'),
    dict(id='benzene', name='Benzene', ref='benzene', pka=43.0, pka_text='43*', estimated=True, smiles='c1ccccc1'),
    dict(id='propene', name='Propene', ref='propene', pka=43.0, pka_text='43*', estimated=True, smiles='CC=C'),
    dict(id='methane', name='Methane', ref='CH4', pka=50.0, pka_text='50*', estimated=True, smiles='C'),
]

# Curated teaching pools.  The 25-card deck emphasizes functional-group scale
# and familiar physical-organic comparisons; the 50-card deck adds most of the
# carbon-acid and stronger-acid examples.  The full deck always contains all 63.
CORE_25_IDS = [
    'hydrochloric_acid', 'hydronium', 'nitric_acid', 'bisulfate', 'hydrofluoric_acid',
    'acetic_acid', 'anilinium', 'pyridinium', 'imidazolium', 'dmaph',
    'thiophenol', 'phenol', 'ammonium', 'ethylammonium', 'hydrogen_peroxide',
    'trifluoroethanol', 'methanol', 'water', 'ethanol', 'tert_butanol',
    'hydrogen_cyanide', 'acetylacetone', 'cyclopentadiene', 'acetylene', 'methane',
]

EXTENDED_50_EXCLUDE_IDS = {
    'hf_sbf5', 'perchloric_acid', 'hydroiodic_acid', 'protonated_alcohol',
    'triphenylammonium', 'diphenylammonium', 'alkanethiol', 'amide_nh',
    'triacetylmethane', 'phosphonium_ester', 'bis_methylsulfonyl_methane',
    'dimethyl_sulfone', 'propene',
}
EXTENDED_50_IDS = [a['id'] for a in WATER_ACIDS if a['id'] not in EXTENDED_50_EXCLUDE_IDS]

assert len(WATER_ACIDS) == 63
assert len(CORE_25_IDS) == 25
assert len(EXTENDED_50_IDS) == 50
assert len(set(CORE_25_IDS)) == 25
assert len(set(EXTENDED_50_IDS)) == 50

DMSO_ACIDS = [
    dict(id='acetic_acid', name='Acetic acid', ref='MeCOOH', pka=11.6, pka_text='11.6', estimated=False, smiles='CC(=O)O'),
    dict(id='phenol', name='Phenol', ref='PhOH', pka=16.4, pka_text='16.4', estimated=False, smiles='Oc1ccccc1'),
    dict(id='methanol', name='Methanol', ref='MeOH', pka=29.0, pka_text='29', estimated=False, smiles='CO'),
    dict(id='water', name='Water', ref='H2O', pka=31.4, pka_text='31.4', estimated=False, smiles='O'),
    dict(id='ethanol', name='Ethanol', ref='EtOH', pka=29.8, pka_text='29.8', estimated=False, smiles='CCO'),
    dict(id='tert_butanol', name='tert-Butanol', ref='t-BuOH', pka=32.2, pka_text='32.2', estimated=False, smiles='CC(C)(C)O'),
    dict(id='ammonia', name='Ammonia', ref='NH3', pka=41.0, pka_text='41', estimated=False, smiles='N'),
    dict(id='phenylthio_methyl_phenyl_sulfone', name='(Phenylthio)methyl phenyl sulfone', ref='PhSCH2SO2Ph', pka=20.3, pka_text='20.3', estimated=False, smiles='c1ccccc1SCS(=O)(=O)c2ccccc2'),
    dict(id='phenylthio_acetonitrile', name='(Phenylthio)acetonitrile', ref='PhSCH2CN', pka=20.8, pka_text='20.8', estimated=False, smiles='N#CCSc1ccccc1'),
    dict(id='phenylacetonitrile', name='Phenylacetonitrile', ref='PhCH2CN', pka=21.9, pka_text='21.9', estimated=False, smiles='N#CCc1ccccc1'),
    dict(id='benzyl_phenyl_sulfide', name='Benzyl phenyl sulfide', ref='PhCH2SPh', pka=30.8, pka_text='30.8', estimated=False, smiles='c1ccccc1CSc2ccccc2'),
    dict(id='nitromethane', name='Nitromethane', ref='CH3NO2', pka=17.2, pka_text='17.2', estimated=False, smiles='C[N+](=O)[O-]'),
    dict(id='acetophenone', name='Acetophenone', ref='PhCOCH3', pka=24.7, pka_text='24.7', estimated=False, smiles='CC(=O)c1ccccc1'),
    dict(id='acetone', name='Acetone', ref='CH3COCH3', pka=26.5, pka_text='26.5', estimated=False, smiles='CC(=O)C'),
    dict(id='methyl_phenyl_sulfone', name='Methyl phenyl sulfone', ref='PhSO2CH3', pka=29.0, pka_text='29', estimated=False, smiles='CS(=O)(=O)c1ccccc1'),
    dict(id='ethyl_acetate', name='Ethyl acetate', ref='CH3CO2Et', pka=30.5, pka_text='30.5', estimated=False, smiles='CCOC(C)=O'),
    dict(id='dimethyl_sulfone', name='Dimethyl sulfone', ref='CH3SO2CH3', pka=31.0, pka_text='31', estimated=False, smiles='CS(C)(=O)=O'),
    dict(id='acetonitrile', name='Acetonitrile', ref='CH3CN', pka=31.3, pka_text='31.3', estimated=False, smiles='CC#N'),
    dict(id='nn_diethylacetamide', name='N,N-Diethylacetamide', ref='CH3CONEt2', pka=34.5, pka_text='34.5', estimated=False, smiles='CC(=O)N(CC)CC'),
    dict(id='dmso', name='Dimethyl sulfoxide', ref='CH3SOCH3', pka=35.1, pka_text='35.1', estimated=False, smiles='CS(C)=O'),
    dict(id='phenylacetylene', name='Phenylacetylene', ref='phenylacetylene', pka=28.8, pka_text='28.8', estimated=False, smiles='C#Cc1ccccc1'),
    dict(id='triphenylmethane', name='Triphenylmethane', ref='Ph3CH', pka=30.6, pka_text='30.6', estimated=False, smiles='C(c1ccccc1)(c2ccccc2)c3ccccc3'),
    dict(id='toluene', name='Toluene', ref='PhCH3', pka=42.0, pka_text='42*', estimated=True, smiles='Cc1ccccc1'),
    dict(id='methane', name='Methane', ref='CH4', pka=55.0, pka_text='55*', estimated=True, smiles='C'),
]

assert len(DMSO_ACIDS) == 24
assert len({a['id'] for a in DMSO_ACIDS}) == 24
