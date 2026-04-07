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
- 已补齐 attribute inference 实验并扩展 multivariate tabular attack 面；修改说明：新增 `src/experiments/run_tabular_synth_benchmark.py`，在 Home Credit 上以 quasi-identifier 预测 income bin，结果写入 `src/data/tabular_synth_results.csv` 并生成 `paper/figs/fig_tabular_synth.png`；主文已不再把 attribute inference 写成“仅属于 threat model 但未实测”。
- 已加入更成熟且可解释的 tabular synthesizer baseline；修改说明：新增 `src/algorithms/tabular_synthesizers.py` 与兼容导入 `src/reaedp/tabular_synthesizers.py`，实现离散 tabular 的 DP Gaussian copula，并与 independent private marginals 做 utility / privacy 对比；正文已把 synthetic-data 竞争力叙事从单纯 MWEM reference 扩展到 multivariate tabular benchmark。
- 已重做 supplementary functional-release mechanism；修改说明：`src/algorithms/wiener_kernel.py` 已从旧的离散 smoothing-operator/$\rho$ 版本改为 Wiener KL spectral coefficient release，`src/experiments/run_wiener_figures.py` 已改为 rank-based 图和 summary；正文与附录已同步改写为 spectral rank 的 approximation--noise tradeoff，不再沿用旧的 $\rho$ 叙述。
- 已完成一轮定向版式清理；修改说明：`paper/main.tex` 与 `paper/appendix.tex` 已处理数学标题导致的 `hyperref` warning，并压缩附录 figure/table 描述表；当前构建日志中已不再有这类 token warning。

## 未修改或部分修改

- 更贴近真实发布流程的 record-level inference / linkage protocol 仍可继续加强；修改说明：本轮已补齐 attribute inference，并保留原有更强 MIA 与 linkage-style 攻击；未全部修改原因：当前新增攻击仍主要基于 tabular synthetic release 上的 supervised inference，而不是更复杂的 auxiliary-record matching protocol；后续准备如何修改：若继续扩展攻击面，可围绕固定辅助信息、部分记录可见、目标记录重识别等协议再加一层评测。
- LaTeX 版式警告仍未完全清理；修改说明：当前 `paper/build.bat` 可以稳定生成最新 PDF，且数学标题造成的 `hyperref` warning 已清掉；未全部修改原因：还残留少量 underfull / overfull box 与 `dwork2014algorithmic` 的 multiply-defined label 提示；后续准备如何修改：投稿前单独做一次版式精修，重点压缩 related-work 表格、长公式与少量双栏断词位置，并定位该重复 label 的根源。
