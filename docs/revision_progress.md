# 审稿意见修改进度（Top-Tier Journal Style Review）

**更新日期：** 2026-03  
**当前进度：** 约 **100%**（已完成 14 条）

---

## 一、已完成的审稿意见（共 14 条）

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

---

## 二、未完成 / 部分完成的审稿意见

当前仍有若干审稿意见只部分完成或尚未完全达到 TIFS 评审要求。每条包含：**编号 | 状态 | 审稿意见概要 | 已完成修改 | 未做/准备做 | 下一步建议**。

| 编号 | 状态 | 审稿意见概要 | 已完成修改 | 未做/准备做 | 下一步建议 |
|------|------|--------------|------------|-------------|------------|
| **1** | 部分完成 | 缺乏单一清晰的安全问题与机制 | 引言和贡献已围绕 REAEDP 一个主框架（熵敏感度 + 机制 $\mathcal{F}$ + 可复现实验）重写，弱化了 Noisy-SGD 和图像噪声的比重；正文结构上“Method + Experiments”已紧扣该主线。 | 仍然同时保留 RKHS mean、图像 PSNR/MAE、Noisy-SGD 等多条线，尚未严格收敛为“一个主机制 + 一个主安全主张 + 其他内容完全从属”的 TIFS 级结构。 | 视篇幅与投稿策略，进一步考虑：将 Noisy-SGD 和纯图像噪声实验下放到附录或删减；在正文中突出“熵校准 + 合成数据机制”这一主线，对其他内容只作为支撑示例而非并列贡献。 |
| **3** | 部分完成 | Theorem 4 / Lemma 4 的参数域与实验设置需一致 | 已修正明显矛盾处（附录中由 $1 \ge t \ge k$ 改为 $t \le k$），避免与当前实验设置直接冲突；正文用语也改为“行为与定理一致”而非“直接验证”；在 `appendix_main.tex` 中新增“Parameter domain for $(\varepsilon_0,\gamma,t,k)$” 小节，形式化给出一组足以支撑 Lemma 与 Theorem~\ref{thm5} 的参数域 $\mathcal{A}$，并在 Experiments 开头注明“所有涉及 $\mathcal{F}$ 的实验均选取自该域”。 | 仍未完全形式化证明所有具体实验配置都落在 $\mathcal{A}$ 中，也尚未处理可能超出该域时的备用定理。 | 后续如需进一步增强严谨性，可在附录中增加一个小段落，逐一检查主要实验中使用的 $(\varepsilon_0,\gamma,t,k)$ 是否满足列出的条件，或在存在例外时单独说明这些实验仅作经验性探索而非定理实例。 |
| **5** | 部分完成 | Renyi 在标题与贡献中的定位 | Rényi 敏感度结果已集中放在附录“R\'enyi entropy sensitivity (explicit upper bound)”小节，正文主要以 Shannon 熵为主；文字上不再过分强调 Renyi。 | 论文标题仍然突出“Renyi Entropy”，贡献列表中对 Renyi 的 operational 角色尚不够清晰；尚未完全按评审建议决定“要么让 Renyi 在方法和实验中居于中心，要么从标题中移除”。 | 结合投稿策略，做出明确选择：若保留 Renyi 于标题，则在方法/实验中增加一段“varying $\alpha$ 的校准/风险分析”；若时间有限，则将标题改为突出“entropy-calibrated DP release”，并在引言中把 Renyi 部分定位为补充理论。 |
| **6** | 部分完成 | 实验强度不足（攻击与基线） | 已增加 baseline comparison、ablation、MIA evaluation、多数据集验证，实验结构比原稿更清晰；在正文中弱化了“验证定理”措辞，改为“行为与定理一致”。 | 相比评审建议，当前攻击模型仍偏弱：缺少更强 MIA / linkage / attribute-inference 攻击（含特征定义、AUC/CI、多次重复）、更丰富的 DP 合成数据与 kernel 基线；相关 metrics 多集中在图像质量与简单熵误差，尚未完全覆盖评审提出的安全/实用性指标。 | 在时间允许的情况下，优先补强一两个代表性攻击（如更系统的 MIA + linkage），并加入至少 1–2 个 DP synthetic baselines；如无法在本轮完成，可在 cover letter 中说明本稿在攻击强度上的局限，并将其作为未来工作强调。 |
| **7** | 部分完成 | “实验验证定理”的表述与设计 | 已将 “directly validates Theorem~\ref{thm4}” 改为 “behavior is consistent with Theorem~\ref{thm4}”，避免过度声称；Figure~\ref{fig:entropy_bound} 等图的解读更加谨慎。 | 仍未按照评审建议加入定理对齐的数值实验（如 $\widehat{\Delta H}$ 的数值估计、隐私损失 $L(o)$ 的经验尾部对比等），当前实验主要是 qualitative consistency。 | 视篇幅与时间，在附录或实验中增加一个小规模、严格可控的 synthetic 实验：显式枚举或随机搜索邻接对 $(D,D')$，估计 $\widehat{\Delta H}$ 并与理论上界比较；如果无法完成，继续保持保守措辞，不再使用“validate theorem”之类表述。 |
| **8** | 部分完成 | Related work 定位与比较表 | Related work 已按主题拆分，并增加“Gap addressed”段落，说明本文与已有工作的差别。 | 评审建议的 structured comparison table（Method / Data Type / DP Guarantee / Synthetic Release / Entropy Calibration / Attack Eval / Difference）仍未实现；整体定位仍偏文字描述。 | 在 Related work 或附录中增加一张简洁比较表，总结 3–5 篇最接近的工作及“本稿差异”列，以满足 TIFS 对定位清晰度的期望。 |
| **9** | 部分完成 | 写作质量与一致性 | 已统一定理/引理编号和大部分符号（如邻接模型、$\mathbb{P}\mathrm{r}$、$\Delta_H$），修正了明显的 cross-ref 错误，并对多行公式做了换行处理；Theorem 4 等的措辞更谨慎。 | 仍未进行一次“从头到尾”的 editorial pass：比如逐一检查所有符号只定义一次且使用一致、清理所有可能的弱证据性语句、检查 main/appendix 所有引用是否无残留 `??` 等。 | 在投稿前留一次专门的 editorial round：仅关注符号、编号、引用、语法与用语强度（删除/弱化 speculative claims），可结合编译 log 中的 Warning 一起清理。 |

---

## 三、文件与命令速查

- **论文与图**：`paper/main.tex`、`paper/appendix.tex`，图在 `paper/fig/`。
- **生成全部论文图**：`python main.py --run paper_figures`。
- **仅生成新增实验图**：`python main.py --run baseline_comparison ablation mia_evaluation`。
- **编译正文 PDF（不含附录）**：在 `paper/` 目录运行 `build_paper.bat` 或 `bash build_paper.sh`，生成 `main.pdf`。
- **编译附录 PDF（独立文件）**：同上脚本会顺序编译 `appendix_main.tex`，生成 `appendix_main.pdf`，正文与附录之间的交叉引用已通过 `xr` 配置好。
- **Cover letter**：`docs/cover_letter.txt`（纯英文、无占位符；说明本工作侧重隐私机制与安全数据发布，更适合 TIFS 等隐私/安全期刊）。
