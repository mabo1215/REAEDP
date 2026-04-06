# 审稿意见修改进度（Top-Tier Journal Style Review）

**更新日期：** 2026-03  
**当前进度：** 约 **100%**（已完成 62 条）

---

## 一、已完成的审稿意见（共 62 条）

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
| **21** | 已改 | **P1 全局邻接表述** | Section III-A 改为明确两种邻接：Theorem~\ref{thm4}（熵敏感度）用 replacement；Theorem~\ref{thm5}（机制 $\mathcal{F}$）用 add/remove；每处定理写明所用邻接。 |
| **22** | 已改 | **P2 Table II** | Table~\ref{tab:notation} 中 $D,D'$ 一行改为：Theorem~\ref{thm4} 用 replacement；Theorem~\ref{thm5} 用 add/remove。 |
| **23** | 已改 | **P3 Theorem 4 限定 replacement** | 定理标题改为 “Shannon entropy sensitivity under replacement adjacency”；陈述中写明 assume $D,D'$ adjacent under replacement (Section III-A)。 |
| **24** | 已改 | **P4 Theorem 5 限定 add/remove** | 定理标题改为 “Differential privacy of $\mathcal{F}$ under add/remove adjacency”；陈述中写明 $D'=D\cup\{d'\}$ or $D=D'\cup\{d'\}$ 及 Appendix 假设。 |
| **25** | 已改 | **P5 威胁模型与实验范围** | 威胁模型段落明确：形式分析约束一般泄漏；显式实验仅针对 MIA 与 linkage-style；attribute inference 不在本版做 benchmark。 |
| **26** | 已改 | **P6 弱化过度声称** | 摘要/引言/结论：“unified”→“differential privacy framework”，“reproducible”→“algorithmic implementation/pipeline”；讨论中 “consistent with $(\varepsilon,\delta)$-DP”→“consistent with the expected privacy behavior under the tested attack setting”。 |
| **27** | 已改 | **P7 附录去遗留** | 附录中 Noisy-SGD 与 performance measurement 改为一句概念性提及；图像实验标为 “Supplementary: Image noise utility”。 |
| **28** | 已改 | **P8 去掉 rebuttal 式叙述** | 实验开头 “figures directly support contributions (i)(ii)(iii)” 改为四部分结构描述（privacy-test, utility comparison, theorem-oriented validation, attack-based evaluation）。 |
| **29** | 已改 | **P9 弱化 Figure 1/4/7 解读** | Fig 1（generalpic）：强调隐私检验行为，正式保证由 Theorem 5 给出；Fig 4（entropy_bound/delta_h_empirical）：表述为 below the bound in the tested regime；Fig 7（mia）：表述为 consistent with stronger privacy at smaller $\varepsilon$。 |
| **30** | 已改 | **P10 Table I 措辞** | Related work 比较表 This work 行 “repro.\ algorithm”→“algorithmic implementation + baselines + attack evaluation”。 |
| **31** | 已改 | **P11 附录标题与结构** | 参数域小节标题改为 “Sufficient parameter domain for Theorem~\ref{thm5}”；Noisy-SGD/图像移入 “Supplementary material” 并标注。 |
| **32** | 已改 | **P1 威胁模型与熵敏感度** | 将“one record is added or removed”改为“under the adjacency model used in Theorem~4”，并改为“noise scales can be calibrated to the target privacy level”，避免暗示 Theorem 3 使用 add/remove 邻接。 |
| **33** | 已改 | **P2 Definition 1 邻接** | “differing in at most one record”改为“where adjacency is defined according to the mechanism or theorem under consideration (Section~III-A and each theorem statement)”。 |
| **34** | 已改 | **P3 Related Work MIA 表述** | “we add MIA evaluation … to show that our release limits inference in practice”改为“we add MIA and linkage-style attack evaluation … to assess privacy behavior empirically under the tested release setting”。 |
| **35** | 已改 | **P4 问题形式化隐私目标** | Privacy goal 改为强调“output-side information leakage is formally constrained”，并写明实验通过 membership-inference 与 linkage-style attacks 评估。 |
| **36** | 已改 | **P5 Section IV-B 标题** | “Reproducible algorithm”改为“Algorithmic implementation”，保留 \label{sec:algorithm}。 |
| **37** | 已改 | **P6 图表解读弱化** | Baseline：改为“For the tested values of $\varepsilon$, the observed entropy error … remains below the theoretical bound $\Delta_H$ from Theorem~4”；Ablation：clarify/control/confirm/stable → illustrate/affect/show/remains informative across tested values of $m$；MIA：增加“in the tested setting”。 |
| **38** | 已改 | **P7 Figure 3 图注** | 熵敏感度图注由“abstract contribution (i): calibrates…”改为“Entropy sensitivity bound $\Delta_H$ vs. dataset size $n$, illustrating the decrease of the theoretical bound used for calibrated histogram release.” |
| **39** | 已改 | **P8 附录结构 I/J/K** | 附录明确为：I. Sufficient parameter domain for Theorem~5；J. Supplementary conceptual background（Noisy SGD）；K. Supplementary image-noise and additional experiments。 |
| **40** | 已改 | **P9 Discussion 结构** | 讨论首段改为“观察→解读→局限”：先陈述 Fig 5/7 现象（bound 以下、MIA/linkage 趋近 random-guess），再写与隐私–效用权衡一致，最后写明“empirical evaluation limited to tested attack models, does not yet include attribute inference”。 |
| **41** | 已改 | **P10 Conclusion 强化** | 结论保留两条定理级贡献；Limitations 中明确 (iii) Wiener/图像为 secondary，(iv) 仅 MIA/linkage、无 attribute inference；并增加收尾句：Future work includes attribute inference 覆盖、多模态/联邦、RKHS 有限维近似更紧分析。 |
| **42** | 已改 | **Final P1 全局邻接句** | Section III-A 已为两种邻接分开表述（Theorem~4 replacement、Theorem~5 add/remove），且无“All mechanisms and bounds are stated for this adjacency model”之误；保持“The relevant adjacency model is stated explicitly in each theorem.” |
| **43** | 已改 | **Final P2 Related Work 弱化** | Related Work 中 MIA 表述已为“assess privacy behavior empirically under the tested release setting”（此前已改）。 |
| **44** | 已改 | **Final P3 Section IV-B 标题** | 已为“Algorithmic implementation”（此前已改）。 |
| **45** | 已改 | **Final P4 问题形式化隐私目标** | 已为“output-side information leakage formally constrained”+ 实验通过 MIA 与 linkage-style 评估（此前已改）。 |
| **46** | 已改 | **Final P5 Discussion 弱化** | 将“Overall, the proposed framework---…is both theoretically grounded and practically evaluable”改为“Overall, the reported results support the main entropy-calibrated release framework…; The RKHS/Wiener and image-noise components should be interpreted as supporting or supplementary analyses.” |
| **47** | 已改 | **Final P6 Conclusion TIFS 版** | 结论全文替换为 TIFS 风格：强调两点定理贡献（熵敏感度 Theorem~4、机制 F Theorem~5）、实验结论（bound 以下、baseline 可比、MIA/linkage 趋近 random-guess）、REAEDP 作为 algorithmic release pipeline；Limitations 重写为四条（离散化、可扩展性、RKHS 有限维近似、MIA/linkage 评估与未来 attribute inference/多模态/联邦）。 |
| **48** | 已改 | **Final P7 附录图像噪声定位** | 正文中所有引用 Appendix image-noise 处改为“Supplementary image-noise utility…included only as supporting evidence, not as a central part of the main theorem-to-mechanism evaluation pipeline”；实验开头与 Discussion (4) 同步弱化图像噪声为 supporting only。 |
| **49** | 已改 | **Final P8 Cover Letter 更新** | 标题改为与正文一致“REAEDP: Entropy-Calibrated Differentially Private Data Release with Formal Guarantees and Attack-Based Evaluation”；Scope 段采用审稿建议段落（Theorem 4/5、无 unified/reproducible）；Why TIFS 中“reproducible experiments”改为“algorithmic implementation”。 |
| **50** | 已改 | **Final P9 全局措辞** | 全文已无“unified framework”“reproducible algorithm”“limits inference in practice”“confirming that the release limits membership inference”；保持“differential privacy framework”“algorithmic implementation”“assess privacy behavior empirically”“consistent with stronger privacy in the tested setting”。 |
| **51** | 已改 | **Final-Check P1 附录引用统一** | 正文不再出现泛泛的 “Appendix A”；Theorem 1–2、Lemma 与 Theorem 5 等处统一改为 “See/Proof is in Appendix~\\ref{app:proofs}”，与 `appendix_main.tex` 中 `\\section{Proofs}` 对应。 |
| **52** | 已改 | **Final-Check P2 附录 Theorem 4 标题** | `appendix_main.tex` 中小节标题由 “Proof of Theorem 4 (Sensitivity of $H$)” 改为 “Proof of Theorem 4 (Shannon entropy sensitivity under replacement adjacency)”，与正文中 Theorem 4 的最终表述完全一致。 |
| **53** | 已改 | **Final-Check P3 Figure 4 图注弱化** | Figure~\\ref{fig:delta_h_empirical} 图注改为 “mean and maximum over adjacent pairs. The ratio remains below 1 in the tested regime, indicating that the empirical entropy sensitivity stays below the theoretical bound.”，不再用 “confirms bound holds” 这类过强措辞。 |
| **54** | 已改 | **Final-Check P4 Discussion 结构核对** | Discussion 开头段已按“观察→解读→局限”结构改写（Figures 5/7 现象、与隐私–效用权衡一致、局限于当前攻击模型且无 attribute inference benchmark），与审稿建议风格一致。 |
| **55** | 已改 | **Final-Check P5 附录 K 表格措辞** | `Figure and table data descriptions` 中 Table~\\ref{tab:figures_theory} 改为 “Supplementary figures and their experimental role (data shown and connection to the theory)”，列名由 “Theory supported” 改为 “Experimental role”，去掉 “abstract contribution(s)” 等内部起稿式措辞，仅保留技术性描述。 |
| **56** | 已改 | **Final-Check P6 附录结构角色说明** | 附录已按 proofs/parameter 域 + J（Supplementary conceptual background）+ K（Supplementary image-noise and additional experiments）结构划分，并在 `Figure and table data descriptions` 中用中性语言描述各图角色，强化 theorem-critical 与 supplementary 的分界。 |
| **57** | 已改 | **Final-Check P7 实验写作微调** | “All experiments were run with fixed random seed …” 改为 “Unless otherwise stated, experiments were run with a fixed random seed … to reduce variability across repeated trials”；Real-data 段 “This illustrates that entropy-based DP release applies …” 改为 “illustrates the applicability of the entropy-based DP release pipeline … in the tested setting”。 |
| **58** | 已改 | **Final-Check P8 结论最终核对** | 结论第一段仅强调两条定理级贡献（熵敏感度上界、机制 $\\mathcal{F}$ 的 $(\\varepsilon,\\delta)$-DP 保证）与实验结果；RKHS/Wiener 与 image-noise 仅在 Limitations 中作为 secondary/supplementary 出现，并以审稿建议的 closing sentence 收尾。 |
| **59** | 已改 | **编号 9 全稿 editorial pass** | 弱证据句弱化（Discussion 中 shows→indicates、confirms→indicates；(6) 补 “in the tested setting”）；main.tex 与 appendix_main.tex 均加入 hyperref 以稳定交叉引用并避免 PDF 出现 ??；符号与 \\ref/\\label 已核对；编译顺序说明已纳入“未完成”转“已改”说明。 |
| **60** | 已改 | **revision_suggestions.tex 附录引用与版式** | 正文 image-noise 附录引用统一为 Appendices~J--L（非 I--L），Noisy-SGD 为 Appendix~I；Table~III 合成图像行改为 Supplementary appendix (Appendices~J--L)；详细 metric 比较处用 Appendix~L；附录 mechanism $\\mathcal{F}$ 已为 \\subsection* 形式（Domain and range, Input, Seed selection 等）；引用处使用非断行空格（~）。 |
| **61** | 已改 | **Final TeX fixes (revision_suggestions.tex)** | 附录图/表编号改为 Supplementary 序列：在 \\appendix 后增加 \\thefigure=S\\arabic{figure}、\\thetable=S\\arabic{table} 及计数器归零，附录中图为 Fig.~S1、S2…，表为 Table~S1…；附录 image-noise 小节措辞改为 “The following image-noise experiments are included as supporting material; the main text focuses on entropy calibration and the synthetic-data mechanism $\\mathcal{F}$.”；mechanism $\\mathcal{F}$ 小标题已为 \\subsection* 形式。 |
| **62** | 已改 | **Final Review (revision_suggestions.tex)** | 最终核对：正文附录引用（Appendix~I / Appendices~J--L）、Table~III 合成图像指向、去重段落、无 H0a/??、build 脚本均已就绪；附录 mechanism $\\mathcal{F}$ 八处小标题已全部使用 \\subsection*（Domain and range, Input, Seed selection, Candidate generation, Partition rule, Privacy-test random variable, Acceptance rule, Output and termination）；附录 Fig.~S1/Table~S1 编号已生效。无新增强制修改。 |

---

## 二、未完成 / 部分完成的审稿意见（共 0 条）

当前未完成项已清零；以下为历史记录。

| 编号 | 状态 | 审稿意见概要 | 已完成修改 | 未做/准备做 | 下一步建议 |
|------|------|--------------|------------|-------------|------------|
| **9** | 已改 | **写作质量与一致性** | 已完成全稿 editorial pass：正文与附录交叉引用已核对（\ref{thm4},\ref{thm5},\ref{app:proofs} 等与 \label 一致）；Discussion 中弱证据句已弱化（“shows”→“indicates”、“confirms”→“indicates”，(6) 补“in the tested setting”）；main.tex 与 appendix_main.tex 均加入 hyperref，交叉引用与 URL 可点击、利于检查 ??；符号 \mathbb{P}\mathrm{r}、\Delta_H、\mathcal{F} 等全文一致。编译顺序建议：先编 main.tex 再编 appendix_main.tex，以保证附录引用正文时无 ??。 | — | 后续若增删图/表/定理，请补全 \label 并重新双遍编译。 |

---

## 三、文件与命令速查

- **论文与图**：`paper/main.tex`、`paper/appendix_main.tex`，图在 `paper/figs/`。
- **生成全部论文图**：`python main.py --run paper_figures`。
- **仅生成新增实验图**：`python main.py --run baseline_comparison ablation mia_evaluation delta_h_empirical`。
- **编译正文与附录 PDF**：在 `paper/` 目录运行 `build.bat`，中间文件写入 `paper/build/`，并将 `main.pdf` 与 `appendix_main.pdf` 复制回 `paper/`。
- **编译附录 PDF（独立文件）**：同上脚本会顺序编译 `appendix_main.tex`，生成 `appendix_main.pdf`，正文与附录之间的交叉引用已通过 `xr` 配置好。
- **Cover letter**：`docs/cover_letter.txt`（纯英文、无占位符；说明本工作侧重隐私机制与安全数据发布，更适合 TIFS 等隐私/安全期刊）。
