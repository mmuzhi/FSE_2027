# FSE 转投修改计划（精简版）

本计划根据三份 ICSE review 对当前稿件进行核查，重点保留会影响 FSE 接收的构念有效性、实验归因、跨模型主张和可复现性问题。原始评审意见仍保存在 `review.md`，本文件只作为执行清单，不重复抄录评审全文。

## 总体判断

当前稿件已经补充了 RQ3.2 的组件消融、RQ3.3 的在线规则 mapper 和额外目标模型结果，但仍有四个主要风险：

1. RQ2 的 validity 标签与 action patterns 来自同一 reasoning trace，仍存在构念循环性。
2. RQ3.2 的现有消融尚不能排除 generic advice 或 prompt 长度带来的收益。
3. RQ3.3 已说明在线实现，但 API token reduction 不能直接等同于端到端延迟或费用节省。
4. GLM、DS-V4-F 和两个 R1 模型提供的是不同层次的证据，不能统称为完整的跨模型泛化。

## 修改状态与 Review 对照（2026-09-30）

**核查范围：**当前 `main.tex`、相关结果表和三份 `review.md` 意见。以下“已完成”指可在稿件中核实的修改，不代表底层数据已复算或 reviewer 的全部疑问已解决。本轮未审计完整 artifact；“正文未报告”不等于实验未做。

**状态：**已完成＝该文字/呈现项已落实；部分回应＝已有修改但仍缺证据或细节；待补＝当前稿件尚未覆盖；待核查＝需要查实验记录。

| Review 意见 | 状态 | 已完成与剩余事项 |
|---|---|---|
| A：teacher/distillation 不能支持独立模型家族泛化；B：transfer 独立性不足 | 部分回应 | RQ1/RQ2 正文及可见表格仅保留 R1 两模型；GLM 原表内容注释保留，暂不加附录。RQ3 保留额外目标模型；Threats 明确同源关系及 GLM judge 角色。仍需补模型选择理由与实际开发/评估隔离说明。 |
| A：大模型与 8B 比较的动机及规模差异 | 待补 | 已承认同源、不同规模，但未说明为何选择这组模型，以及如何避免将能力/规模差异直接解释为模式效应。 |
| A/B：validity 构念循环性；B：valid 是否要求答案正确 | 部分回应 | 已区分 trace validity 与 oracle correctness，并清理 RQ2/Discussion/Threats 的混用。仍缺 validity×correctness 四格表、oracle pass/fail 模式对照或其他外部验证。 |
| A/B：judge 使用方式及验证不足 | 部分回应 | 已描述 3 个 judge×3 次、置信度加权、0.8 阈值和人工裁决；仍缺 judge 选择理由、rubric 摘要、agreement/覆盖率、人工裁决数量。 |
| A/B：action annotation 合并及 human validation 不清楚 | 部分回应 | 已列 annotator 名称、标注流程和 κ=0.816；仍缺两个 annotator 分歧合并规则、人工子集规模及 κ 的具体计算对象。不能把 action annotation κ 当成 validity judge 的验证。 |
| A/B：prompting 缺 generic/mismatched control | 部分回应 | 已有 16 个设置的 Pattern-only / Anti-pattern-only 消融，且明确不能排除 generic advice；未报告 generic-advice 或 mismatched-task 对照。组件消融不等于归因问题已解决。 |
| B/C：prompting 提升与泛化表述过强 | 已完成（文字） | 按作者最新更正的 GLM generation 90.06/90.74/91.17，同步表格、+0.88 pp、摘要和 Finding 3.2；结论限定为 16/16 的平均 pass@1 数值提升，去掉 comparable token cost 和 model-agnostic。原始实验汇总仍待复算。 |
| C：direct 设置是否有信息泄漏 | 待核查 | 已明确 same-source 与 transferred 的模式来源，但未报告实例级 discovery/evaluation 重叠、提示词选择或调参是否使用目标结果；需根据真实实验流程说明，不能仅凭同模型判定泄漏。 |
| A/B：在线 action mapping 不可复现、monitor 成本不清楚 | 部分回应 | 已说明本地规则 mapper、分段和触发逻辑、第二次 finalizer 请求，并报告离线本地处理微基准。仍缺具体规则/阈值的可定位复现信息；online/offline 一致性未测已明确承认。 |
| C：早停模式来源与迁移是否成立 | 部分回应 | 已包含 R1-Qwen3-8B、DS-V4-F、GLM-5.1 的早停结果；仍需明确每个目标模型使用哪套源模式/参数，是否固定或重新调参。有额外模型结果不自动等于冻结策略迁移。 |
| C：早停是否值得准确率损失 | 已完成（定位） | Finding 3.3、摘要和结论统一为 accuracy–token trade-off，不声称无损或普遍最优。若要证明模式策略优于简单截断，还需预算匹配 baseline/消融。 |
| A/B：mining 阈值手选且缺敏感性分析 | 待补 | 已列阈值及专家查看 preliminary results 的选择方式；没有敏感性结果，也未明确开发数据与评估数据的分离。 |
| A/C：创新性增量、first 主张 | 部分回应 | 已去掉 first empirical study，贡献聚焦跨任务和宏观/微观分析；与最接近工作的具体差异仍可加强，文字调整本身不增加方法创新。 |
| B：多任务设计没有充分用于研究问题 | 待补 | 已描述四任务差异，但尚无专门论证哪些发现只有跨任务比较才能获得；可先补讨论，不预设必须新增实验。 |
| C：任务分类的用途不明确 | 部分回应 | 已使用 supervised/task recovery probe，并改为 evaluation dataset；仍需一句明确其是表示诊断而非用户功能。未新增 length-only/action-only baseline。 |
| A：现实 SE 外部效度 | 待补 | 已有一般性的任务/模型局限，仍未明确 algorithmic/class-level benchmark 与 repo-level/agentic 工作流的范围差异。 |
| B：SD/AUX 定义冲突、closure/drift 抽象 | 已完成（文字） | SD 保持 solution design；AUX 保持 auxiliary，不再等同 finalization；closure share 明确为 VV+CC+AUX 占比代理。动作占比不再在关键定量描述中混称成本或资源投入。代理指标的有效性仍非已验证结论。 |
| A/B：数学与流程呈现难读 | 部分回应 | 已将简单占比/转移/support 公式简化为文字，保留投票和熵公式；仍缺完整 worked example，投票符号可补一行定义。 |
| A：action taxonomy 各动作的文献来源 | 待补 | 当前只有整体引用，未提供每类动作的来源或整合依据；属于可用简短说明解决的低成本项。 |
| B：action trace 更长是否必然 token 更多 | 部分回应 | 表中并列报告 token、raw/collapsed action 数，正文仅陈述两者在 invalid 组均更高；尚未报告二者相关性，也不应声称必然对应。 |
| A：调用配置、checkpoint、serving 信息 | 部分回应 | 已写 temperature/top-p 和 think trace 提取；仍缺精确 model ID/checkpoint、调用方式、输出上限等最小复现信息。 |
| A：表格风格不统一、图表密集 | 部分回应 | 已有统一表格样式宏和部分布局调整，RQ2 表题去掉 Cost；仍有个别表独立样式，需最终 PDF 视觉检查。 |

**额外核查项（不是原 review 的逐字要求）：**RQ3 均值的跨运行不确定性、prompt-token overhead 数量、GLM 更正值与原始汇总的对应、RQ3.3 usage 复算、早停预算匹配对照/组件消融。当前正文的消融是 **RQ3.2 prompting 消融**，尚未报告 **RQ3.3 early-stopping 消融**。

## P0：投稿前优先处理

### P0-1：补齐 RQ2 协议的可复现性说明并验证 validity 的外部关系

**当前判断：协议本身可以保留；需要补充证据和边界说明。**

3×3 judge、confidence-weighted voting 和低置信度人工裁决如果确实按当前正文执行，则无需因为原始数据未公开而改写协议。需要避免把“原始 judge 记录未放入代码库”误写成“协议未执行”。但 valid/invalid 标签和 action features 仍然来自同一 trace 的不同 LLM 分析，因此构念循环性问题仍需通过 correctness oracle 和措辞边界来缓解。

**必须完成：**

- 报告 validity 与 objective correctness oracle 的关系，至少给出总体四格表（correct-valid、correct-invalid、incorrect-valid、incorrect-invalid）。
- 在方法或附录中明确 3×3 judge、置信度聚合、0.8 阈值和人工裁决的实际执行流程；若原始 judge 记录不公开，至少报告各 judge 覆盖率、低置信度样本数和最终纳入分析的样本数。
- 给出 validity judge rubric 的摘要，说明 rubric 没有直接把待发现的 anti-pattern 名称当作判断标准。

**推荐增强：**不使用 validity label，直接按 oracle pass/fail 重做 RQ2 的核心 pattern/anti-pattern 对比，作为 robustness analysis。控制 task、model 和 trace length 的回归/分层分析，以及完整的 judge agreement 表可放入附录；如果数据成本过高，不作为投稿阻断项。

### P0-2：明确 RQ3.2 的归因边界

**当前判断：部分解决。**

Pattern-only 与 Anti-pattern-only 消融说明两个组件单独并不稳定，但不能排除通用建议、prompt 长度或任务错配等替代解释。

**必须完成：**

- 增加一个长度和格式匹配的 generic-advice control，或明确承认当前数据不能区分 pattern-specific effect 与 generic instruction effect。
- 报告额外 guidance 的 prompt-token overhead；不能只比较 generated-output tokens。
- 将 direct 结果定位为 within-source intervention，将 transferred 结果定位为 R1-derived guidance 在 DS-V4-F/GLM-5.1 上的迁移测试。
- Finding 3.2 按更正后的 GLM generation 结果（Pattern-only 90.06、Anti-pattern-only 90.74、Pattern+Anti 91.17）统一为：组合方案在全部 16 个 task--model 设置中提高平均 pass@1，且均优于单独组件。保留收益幅度和 token 用量差异，不将数值提升表述为统计显著或普适的 model-agnostic 效果。

**可选增强：**mismatched-task pattern control。如果无法补做，至少在 limitations 中明确该替代解释未被排除；randomized-pattern control 不作为必做项。

### P0-3：收缩跨模型泛化主张并统一 GLM 的角色

**当前判断：正文范围及泛化措辞已调整；模型选择理由和冻结策略/数据隔离仍需核查。**

- R1-0528 与 R1-Qwen3-8B 是 teacher/distillation，属于 within-lineage、cross-scale comparison，不是两个独立模型家族。
- [x] RQ1/RQ2 正文不再报告 GLM 补充模式分析；原表内容已注释保留，暂不新增附录。
- [x] RQ3 保留 GLM 迁移结果，同时保留其参与 validity judging 的实际角色说明。
- RQ3.2/RQ3.3 中将固定的 R1-derived guidance/policy 应用于 DS-V4-F 和 GLM-5.1，才是当前最清楚的跨家族迁移证据。
- GLM-5.1 参与过 primary R1 traces 的 validity judging，因此 RQ3 结果不能称为完整、完全独立的 discovery-to-intervention replication。

**必须完成：**

- [x] 统一当前 Abstract、Findings、Threats 和 Conclusion 中的主要泛化措辞。
- [x] 删除或改写当前正文中的 “model-agnostic”“generalizes across unseen models”等过强表述。
- [x] 移除 RQ1/RQ2 中 GLM 的补充分析文字及可见表格内容，注释保留原表数据。

## P1：显著提升 FSE 说服力

### P1-1：重新定位创新性

删除无法严格证明的 “first empirical study” 表述。贡献重点改为：

- 四类 coding tasks 的统一 reasoning-action 表征和比较；
- macro/micro patterns 的统一分析；
- 从描述性 pattern 到 prompting 和 streaming control 的连接；
- 明确 transfer 的适用边界，而不是声称普适泛化。

Related Work 只需补充与最近工作的直接差异：task scope、representation、pattern mining 和 intervention。无需扩展成完整文献综述。

### P1-2：明确 RQ3.1 的用途

RQ3.1 更适合称为 representation probe 或 diagnostic probe，用来检验 action representation 是否保留 task-discriminative structure，而不是直接的用户功能。

正文应说明这一定位，并避免把高分类准确率包装成实际生产收益。trace-length-only、action-only 等 baseline 属于有余力时的增强项；若不补做，就减少 RQ3.1 篇幅。

### P1-3：限定现实软件工程外部效度

当前四类任务主要是 benchmark-based、algorithmic 或 class-level tasks。若不新增 repo-level/agentic 实验，应在 Introduction、Discussion、Threats 和 Conclusion 中明确：结论限于带 objective oracle 的代码推理任务，不直接推广到真实 repo-level coding agents 或生产工作流。

不把新增 repo-level 实验列为 FSE 投稿前硬性要求，避免无关的范围扩张。

### P1-4：补充必要的稳健性和统计信息

优先补充以下最直接影响可信度的内容：

- 主要比较的 effect size 和不确定性（例如跨三次运行的均值与区间）；
- mining/stopping threshold 的来源，是预设、开发集选择还是事后选择；
- 对 early stopping 至少说明当前工作点的 trade-off，不把单点结果写成普遍最优。

全面 threshold grid、Jaccard stability 和复杂多重比较校正可放入附录或 artifact；如果没有足够数据，不作为单独的投稿阻断项。

## P2：复现性与表达

### P2-1：补齐 judge 和 annotation 的最小必要信息

方法或附录中应说明：

- judge/annotation 模型及其用途；
- validity judge 的投票、置信度和人工裁决流程；
- action annotation 中两个自动 annotator 不一致时的合并规则；
- human validation subset 的规模、抽样方式和 kappa 的具体计算对象。

per-judge 全部分布、所有 pairwise agreement 和额外 alpha/F1 指标可放在 artifact，不必全部塞入正文。

### P2-2：补齐模型调用与数据复现信息

至少列出实际使用的 model ID/checkpoint、调用方式、关键 decoding 配置、最大输出限制和 reasoning trace 获取方式。只有在确实使用 self-hosted 模型时，才需要报告 hardware、quantization 和 serving framework。

RQ3.3 的 Tok. 已确认来自同一目标模型 API usage 口径且包含 finalizer 输出。论文中应明确 baseline 与 stopped runs 使用相同字段和汇总方式；若原始 usage 记录不公开，至少提供复算说明或汇总脚本。该指标用于同一模型内的相对 token 对比，不应解释为跨模型可比的绝对成本，也不应写成 latency reduction。

### P2-3：收敛 RQ3.3 的成本表述

保留以下信息：在线 mapper 是本地规则处理，不调用额外 annotation model；离线微基准显示本地处理开销很小；触发停止后会发起第二次 finalizer 请求。

同时明确：表中 Tok. 是 API-reported token usage，包含 finalizer 输出；它不等于 wall-clock latency 或 monetary cost。除非补做完整端到端测量，否则不要声称已经验证延迟或费用节省。online/offline label agreement、false-stop rate 和 missed-stop rate 可以列为后续工作，而不是当前稿件的硬性新增实验。

### P2-4：简化方法呈现并统一术语

增加一个简短 worked example，展示 raw trace → actions → collapsed trace → pattern → intervention。统一 SD、AUX、closure share、drift share 等术语；删除不影响理解的简单公式或移到附录。不要为了回应 review 再增加大段新的数学定义。

## P3：定稿前统一

- 全文统一使用 benchmark-level、within-lineage、cross-family transfer 等范围明确的术语。
- 删除或改写 first、model-agnostic、consistently、robust、maintaining competitive accuracy 等超出证据的词。
- 检查 Abstract、Contributions、Findings、Threats 和 Conclusion 是否相互一致。
- 统一表格的小数位、缩写、percentage points/percent reduction 和颜色标记。
- 蓝色修订内容最终融入正文后，移除 `\textcolor{blue}{...}`。
- 评审原文 `review.md` 保留不动；本计划只保留行动项。

## 推荐执行顺序

1. 先完成 RQ2 oracle robustness analysis，并据此确认 Finding 2 是否需要缩小。
2. 决定 RQ3.2 是否能补 generic-advice control；不能补则明确降低因果归因。
3. 统一 GLM 在 RQ1、RQ2、RQ3 中的角色，并全面收缩泛化表述。
4. 补齐 RQ3.3 的 API usage 复现材料和指标边界；不将 token reduction 写成 latency/cost reduction。
5. 补方法、模型调用、annotation/judge 和 worked example 等最小复现信息。
6. 最后统一统计、术语、表格和蓝色修订标记，并进行一次针对 FSE 的模拟 review。

## 投稿前最小验收清单

### 已完成的文字与呈现项

- [x] 区分 trace validity 与 task correctness，清理相关术语混用；不将文字收缩视为已排除构念循环性。
- [x] RQ3.2 已报告组件消融，并明确承认当前消融无法做 pattern-specific attribution。
- [x] RQ3.2 已区分 generated-output tokens 与额外 prompt tokens，删除 comparable token cost 的笼统表述。
- [x] GLM generation 最新值 90.06/90.74/91.17 已同步表格、+0.88 pp、摘要、消融叙述及 Finding 3.2。
- [x] RQ3.3 已说明 mapper、finalizer 和 API Tok. 的关系；计量范围集中在 Setup，Finding/Conclusion 不再重复延迟免责声明。
- [x] RQ1/RQ2 正文仅分析 R1 两模型；GLM 原表内容注释保留，不增加附录。
- [x] 同源 R1 比较与额外模型迁移的文字范围已区分，保留 GLM judge 角色说明。
- [x] SD/AUX、closure/drift 定义及 RQ2 表题已对齐；Finding 3.2 明确比较平均 pass@1。
- [x] 当前稿件已成功编译；这不等于完成全部统计验证或 PDF 视觉检查。

### 仍待完成或核查

- [ ] 报告 validity×correctness 四格表；补 oracle-based robustness analysis 或其他外部验证。措辞调整不能替代该证据。
- [ ] 决定是否新增 generic-advice/mismatched-task control；如不做，保留现有归因边界。
- [ ] 实际量化额外 guidance 的 prompt-token overhead（目前只区分了口径）。
- [ ] 将 GLM prompting 更正值与原始实验汇总对应核查；当前表值按作者更正录入。
- [ ] 核对 RQ3.3 usage 原始字段与复算材料；本轮未审计完整 artifact。
- [ ] 补模式/提示/早停策略的开发和评估隔离信息，明确目标模型上的参数是否冻结。
- [ ] 补 judge 选择依据、rubric、agreement、人工裁决数量及 annotation 合并/人工子集/κ 对象。
- [ ] 补精确模型调用信息、mining/stopping 阈值来源及必要的不确定性报告。
- [ ] 明确 RQ3.1 的诊断用途和 benchmark-level 外部效度边界。
- [ ] 补简短 worked example；按需补每类 action 的来源及跨任务设计独有的发现。
- [ ] 决定 RQ3.3 预算匹配 baseline/组件消融的范围；不把 RQ3.2 消融当成早停消融。
- [ ] 最终统一剩余表格样式、蓝色修订标记，并检查 PDF 布局。
