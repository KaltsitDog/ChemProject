# 复现检查点、口径与排错

> 这是 [README](../README.md) 的补充：README 只留简要介绍，检查点、版本和排错放这里。

## 1. 环境自检

- Python 3.11（实测 3.11.15），依赖见 `requirements.txt`。
- `scikit-fingerprints` 至少 **1.8.0**：`scaffold_train_test_split` 从 1.8.0 才开始有。
- 仓库根跑 `python config.py`，会逐条打印 `ROOT` / `DATA_TDT` / `SOURCE` / `OUT` / `PARENTS` / `XTB` / `XTB_WORK` 是否存在，它不打印 `DATA_DH`。

## 2. 数据清洗

### 输入

- `TDT/data/fixed.xlsx`：主表，1426 行，`Td(°C)` + `SMILES`
- `TDT/data/source/`：两篇来源文献的原始表，`datasetwithheader.csv`（1022 行）、`Td_zcy.csv`（886 行）

### 第 1 本 `fixed_provenance.ipynb`

| 检查点    | 期望值                                          |
| ------ | -------------------------------------------- |
| 读表     | `fixed (1426, 2)`、A `(1022, 4)`、B `(886, 2)` |
| 解析失败   | `0 / 0 / 0`                                  |
| 来源分布   | `-1`: 10、`0`: 560、`1`: 450、`2`: 406          |
| 要剔的行   | **10 行**，原因都是「来源 = A，修复后 InChIKey 变化导致匹配失败」  |
| 保留行数   | 1426 − 10 = **1416**                         |
| 两篇温度冲突 | **106 条**，其中 `\|Δ\| > 5` 的 **34 条**          |

产出 `fixed_去10行_带来源.xlsx`（3 个表：`fixed_去10行带来源` / `剔除的10行` / `两篇温度冲突`）。

### 第 2 本 `source_vs_td.ipynb`

| 检查点 | 期望值 |
| --- | --- |
| 样本量 | `n = 1416`；两组对比时 `n = 1010` |
| 描述符维度 | `(1416, 13)` |
| 二元组别 vs Td（Q1） | `r = +0.1614`、`p(公式) = 2.523e-07`、`置换 p = 0.000000`，落点范围 `[-0.1373, +0.1307]` |
| 三组 vs Td（Q1） | `η² = 0.0188`（1.88%）、ANOVA p = 1.525e-06 |
| 控制组成后的残差（Q2） | `RF 5 折 CV R² = 0.411`、残差均值差 `+2.20 °C`、`置换 p = 0.5030` |

产出 `实验组别与Td关系.xlsx`（5 个表：`汇总` / `各组Td分布` / `置换落点分布` / `Q1与Q2对照` / `两篇分子组成对比`）。

## 3. DH（爆热）

`DH/data/test.xlsx`：88 行 × 3 列（`Num` / `Q(cal/g)` / `SMILES`）。

5 本 notebook 是 3 条独立的线：

- `RandomForestRegressor.ipynb`：11 个写死的 Mordred 2D 特征；RF 300 树，**shuffled 10 折**（`KFold(10, shuffle=True, random_state=323922)`）；另做 Murcko 骨架 8 : 2。
- `XGBoost.ipynb`：另一套 6 特征；CV 先在全部 X 上 fit scaler 再切折（轻微泄漏）。
- `contrast.ipynb` / `test.ipynb`：6 个手工特征，基线和特征试探。
- `DataSelector.ipynb`：Mordred 1613 → 70 → GA 选 21 个。**没设 `random_seed`**，且 RF 不读它的结果。

主结果（2026-11-10 重跑，n = 88）：

| 口径 | R² | RMSE | MAE |
| --- | ---: | ---: | ---: |
| shuffled 10 折 CV | **0.7765 ± 0.1305** | 165.46 | 133.73 |
| Murcko 骨架 8 : 2 留出（70 / 18） | 0.7867 | 241.94 | 190.60 |

跑法：必须在 `DH/notebook` 目录下打开（5 本都用 `Path.cwd().parent`，不 `import config`）。DH notebook 只打印，不落盘。

## 4. TDT（热分解温度）

先跑 `Features_Producer.ipynb`（约 1 分钟）：`fixed.xlsx` → `max_wbo` + 三列 BDE + Mordred 全量，存 `TDT/out/features_1426.npz`（`mmat` 1426 × 1449、`qx` 1426 × 4、`y`）。

- 4 个量化列的 NaN 是结构性的：C-NO₂ 463、N-NO₂ 1008、O-NO₂ 1346 = 1426 − 963 / 418 / 80。
- 缺 `Parents/` 或 `BDE/` 时会报错。
- `test.ipynb`：每折训练折内选 120 个 Mordred + 4 个量化列 = 124 维 → ens4（XGB 800 / ExtraTrees 500 / HistGB 500 / MLP (64, 32)）→ 随机 10 折。接着再换 2024 / 777 两个折种子做 bag3。

| 口径 | R² | MAE |
| --- | ---: | ---: |
| 随机 10 折（seed 114514） | 0.6996 | 27.18 |
| 随机 10 折（seed 2024） | 0.7013 | 27.10 |
| 随机 10 折（seed 777） | 0.7022 | 27.06 |
| 随机 10 折 bag3 | **0.7073** | **26.81** |

骨架口径：

8 : 2 × 5 种子 **0.6559 ± 0.0268**（MAE 平均 30.34）；

GroupKFold 10 折 **0.6104 ± 0.1376**（MAE 平均 29.48）。

随机折会让同骨架分子跨折，**泛化请用骨架数字**。

## 5. 版本

| 包 | 实测版本 |
| --- | --- |
| Python | 3.11.15 |
| pandas | 3.0.5 |
| numpy | 2.4.6 |
| scipy | 1.17.1 |
| scikit-learn | 1.9.0 |
| rdkit | 2026.3.5 |
| openpyxl | 3.1.5 |
| mordredcommunity | 2.0.7 |
| scikit-fingerprints | 2.1.0 |
| xgboost | 3.2.0 |
| pygad | 3.7.0 |
| matplotlib | 3.11.1 |
| requests | 2.34.2 |
| joblib | 1.5.3 |
