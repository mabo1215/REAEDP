# 进度日志

## 已全部修改

- 已根据当前仓库状态重写 `docs/progress.md` 的整体结构；修改说明：现已对齐 `C:\source\JDCNET\docs\progress.md` 的格式，采用“已全部修改 / 未修改或部分修改”的两段式中文进度日志，不再保留旧版 60+ 条表格台账。
- 已完成当前 revision cycle 中面向 REAEDP 主线的文稿收口；修改说明：`paper/main.tex` 与 `paper/appendix.tex` 已统一到以熵校准直方图发布、机制 $\mathcal{F}$、baseline comparison 与 attack-based evaluation 为主线的叙述，弱化了与当前证据不匹配的过强表述。
- 已完成更强的 MIA 实验闭环；修改说明：`src/experiments/run_mia_evaluation.py` 已补强为 summary-feature logistic regression、histogram-feature random forest、likelihood-ratio attacker 与 linkage-style attacker 四类攻击，重复次数已提升到 20，结果已写入 `src/data/mia_results.csv` 并更新 `paper/figs/fig_mia.png`。
- 已加入一个真正的 DP synthetic baseline；修改说明：`src/experiments/run_baseline_comparison.py` 已新增 MWEM-style DP synthetic baseline，结果已写入 `src/data/baseline_results.csv` 并更新 `paper/figs/fig_baseline.png`；正文与附录已同步改为“真实 synthetic reference point，而非当前任务下最强 utility baseline”的谨慎定位。
- 已完成 Wiener-kernel 部分的机制梳理和定位调整；修改说明：`src/algorithms/wiener_kernel.py` 已显式引入 smoothing operator，并输出 sensitivity / Gaussian $\sigma$；`src/experiments/run_wiener_figures.py` 新增 `src/data/wiener_summary.csv` 与 `paper/figs/fig8.png`。根据真实结果，Wiener-kernel 已从主文强结论降格为 supplementary diagnostic / structured example。
- 已将新的实验结果写回论文；修改说明：`paper/main.tex` 与 `paper/appendix.tex` 已改写 MIA、baseline comparison 与 Wiener-kernel 相关段落，不再声称当前结果未支持的结论，例如“所有攻击都接近随机”或“更大的 $\rho$ 单调提升 Wiener utility”。
- 已重新编译并验证论文当前可构建；修改说明：`paper/build.bat` 已成功生成 `paper/main.pdf` 与 `paper/appendix.pdf`，实验更新后的图和文本均已进入 PDF，没有新增构建失败。
- 已完成当前 `docs/revision_suggestions.tex` 下的强制修改项；修改说明：当前主文与附录的理论表述、baseline、攻击实验、supplementary 定位和 progress 记录已经同步到同一状态，不再存在必须继续挂在“未修改”名下的强制条目。

## 未修改或部分修改

- 更强的 attribute inference 或更贴近 release 语义的 record-level attack 仍未完成；修改说明：本轮已经把 MIA 与 linkage-style 攻击补强，并加入 likelihood-ratio attacker；未修改原因：当前仓库中还没有与现有 release pipeline 对齐、且能低成本补进主文的 attribute inference 实验实现；后续准备如何修改：若继续扩展攻击面，优先补 attribute inference，或设计更贴近发布对象的 record-level inference protocol。
- 更成熟的 tabular DP synthesizer baseline 仍未补入；修改说明：这轮已经加入 MWEM-style baseline，使“真正的 DP synthetic baseline”不再缺位；未全部修改原因：当前一维 histogram workload 下，继续补更复杂 synthesizer 的解释收益有限，且容易把论文重心从 theorem-aligned release 拉偏；后续准备如何修改：只有在需要显著强化 synthetic-data 竞争力叙事时，再补一个更成熟且可解释的 tabular synthesizer。
- Wiener-kernel 部分尚未重做为更强的 functional-release 结果；修改说明：当前已根据真实结果把它降格为 supplementary diagnostic，避免过强 claim；未全部修改原因：现有离散化实现下，$\rho$ 与 utility 的关系仍不够理想，直接重写需要新的机制设计而不是小修小补；后续准备如何修改：若后续要重新升格这一部分，需要先重做 functional-release mechanism 与相应实验，而不是继续沿用当前实现做表述优化。
- LaTeX 版式警告仍未完全清理；修改说明：当前 `paper/build.bat` 可以稳定生成最新 PDF；未全部修改原因：还残留少量 underfull / overfull box、multiply-defined labels 与 hyperref token warning，但这些属于投稿前的版式清理，不影响当前 revision cycle 完成；后续准备如何修改：投稿前单独做一次版式清理，优先处理附录表格和含数学的标题/图注。
