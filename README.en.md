# Chem Project — QSAR for Energetic Materials (Heat of Detonation DH / Thermal Decomposition Temperature TDT)

> Main repository (Gitee): <https://gitee.com/peach_moon/chem_project>
> GitHub mirror: <https://github.com/KaltsitDog/ChemProject>

A QSAR regression project for energetic materials (explosives / high-energy compounds): it predicts heat of detonation Q and thermal decomposition temperature Td from molecular structure (SMILES). Features combine RDKit / Mordred 2D descriptors with WBO and BDE from xTB semi-empirical calculations.

Stack: RDKit, Mordred, xTB GFN2, scikit-learn, XGBoost.

## Data

| Module | Data | Task |
| --- | --- | --- |
| DH | `DH/data/test.xlsx` (88 rows) | heat of detonation Q (cal/g) |
| TDT | `TDT/data/fixed.xlsx` (1426 rows) | thermal decomposition temperature Td (°C) |

## Results

| Module | Setting | R² | MAE |
| --- | --- | ---: | ---: |
| DH | random 10-fold CV | **0.791 ± 0.059** | 132.9 |
| DH | Murcko-scaffold 8:2 hold-out (70 / 18) | 0.787 | 190.6 |
| TDT | random 10-fold (3 seeds averaged, bag3) | **0.7073** | 26.81 |
| TDT | scaffold 8:2 × 5 seeds | 0.6559 ± 0.0268 | 30.34 |
| TDT | scaffold-grouped 10-fold | 0.6104 ± 0.1376 | 29.48 |

## Layout

```
chem_project/
├── config.py                    # the single exit point for paths
├── requirements.txt
├── DH/
│   ├── data/test.xlsx
│   └── notebook/                # RandomForestRegressor etc.
└── TDT/
    ├── data/                    # fixed.xlsx (main table) / source/ (raw tables of the two papers)
    └── notebook/
        ├── data_prep/           # fixed_provenance / source_vs_td / unique
        └── modeling/            # Features_Producer / test / 3D_try / BDE_Producer
```

## Quick start

```bash
conda create -n chem python=3.11 -y
conda activate chem
pip install -r requirements.txt
python config.py
```

- **Data cleaning**: `TDT/notebook/data_prep/fixed_provenance.ipynb` → `source_vs_td.ipynb`
- **DH model**: `DH/notebook/RandomForestRegressor.ipynb`
- **TDT model**: `TDT/notebook/modeling/Features_Producer.ipynb` → `TDT/notebook/modeling/test.ipynb`

Running the TDT model needs the external `Parents/` (1426 `parent_XXXX/` folders with `conf.xyz` and `wbo`) and `xtb_work/BDE/`; point `CHEM_PARENTS` / `CHEM_XTB_WORK` at them.

Recomputing geometries / BDE from scratch also needs xTB (`CHEM_XTB`).

The 5 notebooks under `DH/notebook` must be opened from that directory (they use `Path.cwd().parent`); all other notebooks can be opened from the repository root.

## Data notes

- `TDT/data/fixed.xlsx`: main table, 1426 rows, `Td(°C)` + `SMILES`.
- `TDT/data/source/`: raw tables of the two source papers.
- `TDT/data/unique_random.xlsx`, `random.xlsx`, `test.xlsx` are intermediate cleaning products.

The project is for study and research use only.
