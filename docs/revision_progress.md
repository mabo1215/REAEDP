# 审稿意见修改进度（Top-Tier Journal Style Review）

**更新日期：** 2026-03  
**当前进度：** 约 **100%**（已完成 20 条）

---

## 一、已完成的审稿意见（共 20 条）

每条包含：**序号 | 状态 | 审稿意见概要 | 修改说明**

| 序号 | 状态 | 审稿意见概要 | 修改说明 |
|------|------|--------------|----------|
| **1** | 已改 | **核心贡献不够聚焦**：多点多线并行，缺少“一句话能说清的主方法”。 | 摘要和引言围绕“REAEDP 一个主方法”重写；贡献收敛为三条（熵敏感度上界、机制 F+隐私检验、实验验证）；明确“主方法”为熵校准 + 合成数据机制 + 可复现算法；同时按 `docs/revision_suggestions.tex` 中 C1–C3 的建议，对标题、摘要和引言结构做了整体重构，避免在正文中出现诸如 RQ1 等内部标记。 |
| **2** | 已改 | **理论严谨性不足**：邻接模型、假设、证明步骤与 Rényi 熵表述不够清晰。 | Preliminaries 中增加并统一“邻接数据集”定义（采用 replacement adjacency，一致用于定理与证明）；Theorem 4 前写明 Assumption 与 Claim（上界），并改写叙述为“具有正确的 $1/n$ 阶”而不再声称“tight up to constants”；附录证明改为标准定理–证明表述并统一符号。Rényi 熵正文已有定义，附录已补充“Rényi entropy sensitivity”显式上界。 |
| **3** | 已改 | **方法不可复现**：缺少完整算法与输入/输出/复杂度说明。 | Method 中增加“Reproducible algorithm”小节与 Algorithm 1 伪代码，写明输入（D, ε, δ, m, k, t, γ, ε₀）、输出（噪声直方图/熵或合成记录）、复杂度说明，并与正文定理对应；在 `paper/appendix_main.tex` 中新增“Mechanism $\mathcal{F}$: formal specification”小节，给出 $\mathcal{F}$ 的完整形式化定义（输入、种子选择、候选分布 $p_s(y)$、划分规则 $I_s(y)$、隐私测试随机变量 $L$ 及接受/重采样逻辑），使 DP 定理的 Proof 附录与正文算法严格对齐、可复现。 |
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
| **15** | 已改 | **Related work 比较表** | 在 Related work “Gap addressed” 后增加 Table~\ref{tab:related}（Method / Data Type / Formal DP / Synthetic / Entropy Calibration / Attack Eval / Difference），对比 Dwork、Noisy-SGD、DP histogram、Kernel prior 与 This work（REAEDP），满足 TIFS 对定位清晰度的期望。 |
| **16** | 已改 | **Rényi 在标题与贡献中的定位（varying $\alpha$）** | 在附录 “Rényi entropy sensitivity” 后增加 “Varying $\alpha$: calibration and risk” 段落及 Table~\ref{tab:varying_alpha}（$C_\alpha = 2|\alpha|/(|1-\alpha|\ln 2)$ 随 $\alpha$ 变化），说明 Rényi 熵在校准中的 operational 角色，与保留 Rényi 于标题的选择一致。 |
| **17** | 已改 | **缺乏单一清晰的安全问题与机制（主线收敛）** | 将 Noisy-SGD 与纯图像噪声实验下放到附录：正文删除 “Traditional Noisy-SGD” 与 “Performance measurement” 小节，删除 “Privacy--utility tradeoff (image noise)” 与 “Metrics comparison: Laplace vs.\ Gaussian” 小节及对应图，上述内容迁至 `appendix_main.tex`（Appendix~\ref{app:noisy_sgd}、Appendix~\ref{app:image_noise}）；Related Work 与 Motivation 中 Noisy-SGD 仅保留一句并指向附录；实验开头与讨论中明确主线为“熵校准 + 合成数据机制 $\mathcal{F}$”，图像 PSNR/MAE 仅以附录支撑形式提及。 |
| **18** | 已改 | **Theorem 4 / Lemma 4 的参数域与实验设置需一致** | 在 `appendix_main.tex` 的 “Parameter domain for $(\varepsilon_0,\gamma,t,k)$” 小节末尾增加 “Verification that reported experiments use parameters in $\mathcal{A}$” 段落：逐一说明 Figure~\ref{fig:generalpic} 使用的 $t=2$、$k \in \{10,20,30,50\}$、$\gamma>1$ 及 $|D| \ge 50$ 满足 $\gamma>1$、$t \le k$、$k \le |D|$ 与 Lemma 要求，故落在 $\mathcal{A}$ 内；并注明其余未列出的 $\mathcal{F}$ 配置仅作经验性探索、不声称实例化 Theorem~\ref{thm5}。 |
| **19** | 已改 | **实验强度不足（攻击与基线）** | 补强 MIA：在 `run_mia_evaluation.py` 中增加 AUC、5 次重复运行及 95\% CI、linkage-style 攻击（基于 L2 距离的“哪个参考发布更近”猜测）；图中报告 MIA accuracy（带 CI）、MIA AUC、linkage accuracy。增加 2 个 DP synthetic 基线：在 `run_baseline_comparison.py` 中增加 “DP synthetic (Laplace)” 与 “DP synthetic (Gaussian)”（对 count 加噪后归一化再 multinomial 抽样得到合成直方图），与 Laplace、Gaussian 一起画熵误差与 MAE；正文 Baseline 与 Discussion 已更新。 |
| **20** | 已改 | **“实验验证定理”的表述与设计** | 在实验中增加小规模、严格可控的 synthetic 实验：新增 `run_delta_h_empirical.py`，对相邻直方图对 $(D,D')$ 显式枚举或随机采样，估计 $\widehat{\Delta H} = \max_{D\sim D'} |H(D)-H(D')|$，与理论上界 $\Delta_H$ 比较；输出 `fig_delta_h_empirical.png` 与 `data/delta_h_empirical.csv`。正文新增 “Empirical entropy sensitivity ($\widehat{\Delta H}$ vs.\ bound)” 小节与 Figure~\ref{fig:delta_h_empirical}，说明比值 $<1$、行为与 Theorem~\ref{thm4} 一致；Discussion 中补充 (1b) 对应结论。 |

---

## 二、未完成 / 部分完成的审稿意见（共 1 条）

当前仍有若干审稿意见只部分完成或尚未完全达到 TIFS 评审要求。每条包含：**编号 | 状态 | 审稿意见概要 | 已完成修改 | 未做/准备做 | 下一步建议**。

| 编号 | 状态 | 审稿意见概要 | 已完成修改 | 未做/准备做 | 下一步建议 |
|------|------|--------------|------------|-------------|------------|
| **9** | 部分完成 | 写作质量与一致性 | 已统一定理/引理编号和大部分符号（如邻接模型、$\mathbb{P}\mathrm{r}$、$\Delta_H$），修正了明显的 cross-ref 错误，并对多行公式做了换行处理；Theorem 4 等的措辞更谨慎。 | 仍未进行一次“从头到尾”的 editorial pass：比如逐一检查所有符号只定义一次且使用一致、清理所有可能的弱证据性语句、检查 main/appendix 所有引用是否无残留 `??` 等。 | 在投稿前留一次专门的 editorial round：仅关注符号、编号、引用、语法与用语强度（删除/弱化 speculative claims），可结合编译 log 中的 Warning 一起清理。 |

---

## 三、文件与命令速查

- **论文与图**：`paper/main.tex`、`paper/appendix_main.tex`，图在 `paper/fig/`。
- **生成全部论文图**：`python main.py --run paper_figures`。
- **仅生成新增实验图**：`python main.py --run baseline_comparison ablation mia_evaluation delta_h_empirical`。
- **编译正文 PDF（不含附录）**：在 `paper/` 目录运行 `build_paper.bat` 或 `bash build_paper.sh`，生成 `main.pdf`。
- **编译附录 PDF（独立文件）**：同上脚本会顺序编译 `appendix_main.tex`，生成 `appendix_main.pdf`，正文与附录之间的交叉引用已通过 `xr` 配置好。
- **Cover letter**：`docs/cover_letter.txt`（纯英文、无占位符；说明本工作侧重隐私机制与安全数据发布，更适合 TIFS 等隐私/安全期刊）。
