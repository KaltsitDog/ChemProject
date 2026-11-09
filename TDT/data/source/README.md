# 两篇原始文献的数据集

`TDT/data/fixed.xlsx`（主表，1426 条）不是从零测的：它是两篇文献的数据拼起来、再去重清洗后得到的。
这个目录放那两篇的原始表，`TDT/notebook/data_prep/fixed_provenance.ipynb` 靠它们做逐条溯源。

| 文件 | 来源 | 行数 | 列 | 唯一 InChIKey |
|---|---|---|---|---|
| `datasetwithheader.csv` | 来源 A：2025 那篇（筛选/建模论文） | 1022 | `idx`, `smiles`, `temp`, `canonical_smiles` | 997 |
| `Td_zcy.csv` | 来源 B：2023 那批 | 886 | `smiles`, `Td` | 880 |

- 两篇的 `temp` / `Td` 都是热分解温度（°C），但**测定方法没有统一**，所以溯源之后还要做"来源与 Td 的关系"分析（`source_vs_td.ipynb`）：原始差显著（r = +0.1614），控制分子组成后归零（置换 p = 0.5030）。
- 匹配键用 **InChIKey**，不用 SMILES 字符串 —— 同一分子有多种写法（A 里同时给了带显式 H 的 `smiles` 和规整过的 `canonical_smiles`），字符串直接比会漏（实测命中 947 vs 966）。
- ⚠️ 来源 B 的文献出处**尚未最终确认**（按"温度基本都对得上"认作 2023 那篇），引用前请核对原文。
