# 含能材料 QSAR（爆热 DH / 热分解温度 TDT）

> 主仓库（Gitee）：<https://gitee.com/peach_moon/chem_project>

> GitHub 镜像：<https://github.com/KaltsitDog/ChemProject>

含能材料（炸药 / 高能化合物）的 QSAR 回归项目：用分子结构（SMILES）预测爆热 Q 和热分解温度 Td。特征由 RDKit / Mordred 的 2D 描述符与 xTB 半经验量化算出的 WBO、BDE 拼接而成。

技术栈：RDKit、Mordred、xTB GFN2、scikit-learn、XGBoost。

## 数据

| 模块 | 数据 | 任务 |
| --- | --- | --- |
| DH | `DH/data/test.xlsx`（88 条） | 爆热 Q（cal/g） |
| TDT | `TDT/data/fixed.xlsx`（1426 条） | 热分解温度 Td（°C） |

## 结果

| 模块 | 口径 | R² | MAE |
| --- | --- | ---: | ---: |
| DH | 随机 10 折 CV | **0.791 ± 0.059** | 132.9 |
| DH | Murcko 骨架 8 : 2 留出（70 / 18） | 0.787 | 190.6 |
| TDT | 随机 10 折（3 个种子平均，bag3） | **0.7073** | 26.81 |
| TDT | 骨架 8 : 2 × 5 种子 | 0.6559 ± 0.0268 | 30.34 |
| TDT | 骨架分组 10 折 | 0.6104 ± 0.1376 | 29.48 |

## 目录

```
chem_project/
├── config.py                    # 唯一的路径出口
├── requirements.txt
├── DH/
│   ├── data/test.xlsx
│   └── notebook/                # RandomForestRegressor 等文件
└── TDT/
    ├── data/                    # fixed.xlsx（主表）/ source/（两篇原始表）
    └── notebook/
        ├── data_prep/           # fixed_provenance / source_vs_td / unique
        └── modeling/            # Features_Producer / test / 3D_try / BDE_Producer
```

## 快速开始

```bash
conda create -n chem python=3.11 -y
conda activate chem
pip install -r requirements.txt
python config.py
```

- **数据清洗**：`TDT/notebook/data_prep/fixed_provenance.ipynb` → `source_vs_td.ipynb`
- **DH 模型**：`DH/notebook/RandomForestRegressor.ipynb`
- **TDT 模型**：`TDT/notebook/modeling/Features_Producer.ipynb` → `TDT/notebook/modeling/test.ipynb`

跑 TDT 模型需要仓库外的 `Parents/`（1426 个 `parent_XXXX/`，含 `conf.xyz`、`wbo`）和 `xtb_work/BDE/`，用 `CHEM_PARENTS` / `CHEM_XTB_WORK` 指过去。

从零重算几何 / BDE 另需 xTB，设 `CHEM_XTB`。

`DH/notebook` 的 5 本要在 `DH/notebook` 目录下打开（它们用 `Path.cwd().parent`），其余 notebook 从仓库根打开即可。

## 数据说明

- `TDT/data/fixed.xlsx`：主表，1426 行，`Td(°C)` + `SMILES`。
- `TDT/data/source/`：两篇来源文献的原始表。
- `TDT/data/unique_random.xlsx`、`random.xlsx`、`test.xlsx` 是清洗中间产物。

本项目仅供学习和研究使用。