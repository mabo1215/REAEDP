# 审稿意见修改进度（Top-Tier Journal Style Review）

**更新日期：** 2026-03  
**当前进度：** 约 **100%**（已完成 14 条）

---

## 一、已完成的审稿意见（共 14 条）

每条包含：**序号 | 状态 | 审稿意见概要 | 修改说明**

| 序号 | 状态 | 审稿意见概要 | 修改说明 |
|------|------|--------------|----------|
| **1** | 已改 | **核心贡献不够聚焦**：多点多线并行，缺少“一句话能说清的主方法”。 | 摘要和引言围绕“REAEDP 一个主方法”重写；贡献收敛为三条（熵敏感度上界、机制 F+隐私检验、实验验证）；明确“主方法”为熵校准 + 合成数据机制 + 可复现算法；同时按 `docs/revision_suggestions.tex` 中 C1–C3 的建议，对标题、摘要和引言结构做了整体重构，避免在正文中出现诸如 RQ1 等内部标记。 |
| **2** | 已改 | **理论严谨性不足**：邻接模型、假设、证明步骤与 Rényi 熵表述不够清晰。 | Preliminaries 中增加“邻接数据集”定义（add/remove）；Theorem 4 前写明 Assumption 与 Claim（上界），并注明“tight up to constants”；附录证明改为标准定理–证明表述并统一符号。Rényi 熵正文已有定义，附录已补充“Rényi entropy sensitivity”显式上界。 |
| **3** | 已改 | **方法不可复现**：缺少完整算法与输入/输出/复杂度说明。 | Method 中增加“Reproducible algorithm”小节与 Algorithm 1 伪代码，写明输入（D, ε, δ, m, k, t, γ, ε₀）、输出（噪声直方图/熵或合成记录）、复杂度说明，并与正文定理对应。 |
| **4** | 已改 | **实验与理论脱节**：实验未充分体现“所提机制优于基线/在何条件下更好”。 | 实验按 RQ1–RQ4 组织；新增“Baseline comparison”“Ablation”“MIA evaluation”三个子节及对应图（fig_baseline, fig_ablation, fig_mia），直接回答与基线对比、参数/模块贡献、攻击评估。 |
| **5** | 已改 | **缺少强基线与消融**：未与标准 Laplace/Gaussian、DP 直方图/合成数据基线系统对比，无消融。 | 新增 baseline_comparison（Laplace vs Gaussian，熵误差与 MAE vs ε，并标 Δ_H 上界）、ablation（熵误差 vs bins，与上界对比）；Wiener 的 ρ、隐私检验的 k 已有 fig2–4 与 fig1 支撑。 |
| **6** | 已改 | **隐私攻击评估不足**：引言提到 MIA/属性推断/链接，但实验未做攻击评估。 | 新增 MIA 实验（run_mia_evaluation），在 DP 直方图发布上做成员推断，画 MIA 准确率 vs ε，“Membership inference attack evaluation” 小节与 fig_mia，讨论随 ε 降低趋近随机猜测。 |
| **7** | 已改 | **写作与定理呈现需打磨**：附录证明、记号一致性、数学英文与语法。 | 已对 `paper/main.tex` 与 `paper/appendix.tex` 通篇校对数学英文与语法，统一符号（如 $\mathbb{P}\mathrm{r}$、$\Delta_H$）、定理/引理编号与引用；对 Lemma、Theorem~5 等长公式和证明进行了多行对齐与换行，避免双栏越界；同时保证正文与附录在邻接模型、参数符号和交叉引用上的一致性。 |
| **8** | 已改 | **摘要**：信息过载，应突出“一个问题、一个方法、一个保证、一个结果、意义”。 | 摘要按“问题→方法→关键理论保证→关键实验结果→实际意义”五部分重写，主方法统一为 REAEDP。 |
| **9** | 已改 | **引言**：区分“实际问题 / 文献缺口 / 本文贡献”，贡献收紧为三条。 | 增加“Practical privacy problem”“Technical gap”“Contribution”三段，贡献明确为三条并对应算法与实验。 |
| **10** | 已改 | **Related Work**：按主题分小节，结尾明确“本文填补的缺口”。 | 拆分为 DP 与合成数据、熵与信息论隐私、核/函数空间机制、隐私审计与攻击、Noisy SGD；文末增加“Gap addressed”段落。 |
| **11** | 已改 | **问题形式化**：明确 M: D↦D̃、隐私目标、效用目标、攻击模型。 | Preliminaries 末增加“Problem formulation”小节，显式写出机制 $\mathcal{M}: D \mapsto \widetilde{D}$、隐私目标、效用目标、攻击模型（并指向 MIA 实验）。 |
| **12** | 已改 | **实验**：按 RQ1–RQ4 组织（隐私–效用、与基线、模块贡献、攻击鲁棒性）。 | 实验开头给出 RQ1–RQ4，并新增基线、消融、MIA 三个子节及对应图与讨论。 |
| **13** | 已改 | **结论**：除总结外需写“局限与未来工作”。 | 结论末增加“Limitations and future work”（离散化/高维、可扩展性、RKHS 近似、联邦与更强攻击等）。 |
| **14** | 已改（cover letter） | **期刊定位**：当前更适合 TIFS 等隐私/安全期刊，若强化 ML 方法创新可考虑 TNNLS。 | 在 `docs/cover_letter.txt`（纯英文、无占位符）中写明本工作侧重隐私机制与安全数据发布、更适合 TIFS 等隐私/安全期刊；正文不写该表述。投稿时使用该 cover letter 即可。 |

---

## 二、未完成 / 部分完成的审稿意见

当前暂无未完成或部分完成的审稿意见。

---

## 三、文件与命令速查

- **论文与图**：`paper/main.tex`、`paper/appendix.tex`，图在 `paper/fig/`。
- **生成全部论文图**：`python main.py --run paper_figures`。
- **仅生成新增实验图**：`python main.py --run baseline_comparison ablation mia_evaluation`。
- **编译正文 PDF（不含附录）**：在 `paper/` 目录运行 `build_paper.bat` 或 `bash build_paper.sh`，生成 `main.pdf`。
- **编译附录 PDF（独立文件）**：同上脚本会顺序编译 `appendix_main.tex`，生成 `appendix_main.pdf`，正文与附录之间的交叉引用已通过 `xr` 配置好。
- **Cover letter**：`docs/cover_letter.txt`（纯英文、无占位符；说明本工作侧重隐私机制与安全数据发布，更适合 TIFS 等隐私/安全期刊）。
