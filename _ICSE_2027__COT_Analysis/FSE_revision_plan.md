# FSE 转投修改计划（精简版）

本计划根据三份 ICSE review 对当前稿件进行核查，重点保留会影响 FSE 接收的构念有效性、实验归因、跨模型主张和可复现性问题。原始评审意见仍保存在 `review.md`，本文件只作为执行清单，不重复抄录评审全文。

## 总体判断

当前稿件已经补充了 RQ3.2 的组件消融、RQ3.3 的在线规则 mapper 和额外目标模型结果，但仍有四个主要风险：

1. RQ2 的 validity 标签与 action patterns 来自同一 reasoning trace，仍存在构念循环性。
2. RQ3.2 的现有消融尚不能排除 generic advice 或 prompt 长度带来的收益。
3. RQ3.3 已说明在线实现，但 API token reduction 不能直接等同于端到端延迟或费用节省。
4. GLM、DS-V4-F 和两个 R1 模型提供的是不同层次的证据，不能统称为完整的跨模型泛化。

## P0：投稿前优先处理

### P0-1：验证 RQ2 结论是否依赖 validity 标签

**当前判断：仍需补强。**

valid/invalid 标签和 action features 都来自对同一 trace 的 LLM 分析。即使当前使用了多 judge 和人工裁决，也还不能排除 anti-pattern 的发现部分来自 validity 定义本身。

**必须完成：**

- 报告 validity 与 objective correctness oracle 的关系，至少给出总体四格表（correct-valid、correct-invalid、incorrect-valid、incorrect-invalid）。
- 不使用 validity label，直接按 oracle pass/fail 重做 RQ2 的核心 pattern/anti-pattern 对比，作为 robustness analysis。
- 根据结果收缩 Finding 2 的表述；如果 oracle 分组不能复现全部结果，不再把这些模式写成独立的 validity 机制。
- 在方法或附录中给出 validity judge rubric 的摘要，说明它没有直接把待发现的 anti-pattern 名称当作判断标准。

**可选增强：**控制 task、model 和 trace length 的回归/分层分析，以及完整的 judge agreement 表。如果数据成本过高，不作为投稿阻断项。

### P0-2：明确 RQ3.2 的归因边界

**当前判断：部分解决。**

Pattern-only 与 Anti-pattern-only 消融说明两个组件单独并不稳定，但不能排除通用建议、prompt 长度或任务错配等替代解释。

**必须完成：**

- 增加一个长度和格式匹配的 generic-advice control，或明确承认当前数据不能区分 pattern-specific effect 与 generic instruction effect。
- 报告额外 guidance 的 prompt-token overhead；不能只比较 generated-output tokens。
- 将 direct 结果定位为 within-source intervention，将 transferred 结果定位为 R1-derived guidance 在 DS-V4-F/GLM-5.1 上的迁移测试。
- 重写 Finding 3.2，保留任务和模型差异，不再使用 “consistently improve”“model-agnostic” 等绝对措辞。

**可选增强：**mismatched-task pattern control。如果无法补做，至少在 limitations 中明确该替代解释未被排除；randomized-pattern control 不作为必做项。

### P0-3：收缩跨模型泛化主张并统一 GLM 的角色

**当前判断：实验不必立即换模型，表述需要统一。**

- R1-0528 与 R1-Qwen3-8B 是 teacher/distillation，属于 within-lineage、cross-scale comparison，不是两个独立模型家族。
- RQ1 的 GLM 结果是单独重跑 macro-pattern mining 后得到的跨家族探索分析，不是冻结 R1 signature 后的严格 held-out test。
- RQ2 的 GLM 结果使用不同的 validity judge，且部分 invalid 子组很小，不宜作为主文的稳健 replication；可移至附录或保留为明确标注的 exploratory analysis。
- RQ3.2/RQ3.3 中将固定的 R1-derived guidance/policy 应用于 DS-V4-F 和 GLM-5.1，才是当前最清楚的跨家族迁移证据。
- GLM-5.1 参与过 primary R1 traces 的 validity judging，因此 RQ3 结果不能称为完整、完全独立的 discovery-to-intervention replication。

**必须完成：**

- 统一 Abstract、Findings、Discussion、Threats 和 Conclusion 中的泛化措辞。
- 删除或改写 “model-agnostic”“robust across model families”“generalizes across models”等绝对表述。
- 不用 GLM 样本数长段落充正文；如保留 RQ1/RQ2 GLM 表格，在表注或附录说明其分析角色和限制。

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

RQ3.3 的 Tok. 已确认来自 API usage 且包含 finalizer 输出。需要补齐对应的原始 usage 字段、三轮结果或复算脚本，使表格可以由 artifact 复核；不要把当前 runner 的字符数估算描述成 API usage 原始记录。

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

- [ ] RQ2 已有 oracle-based robustness analysis，或 Finding 2 已据结果收缩。
- [ ] RQ3.2 已加入 generic-advice control，或明确承认无法做 pattern-specific attribution。
- [ ] RQ3.2 的 prompt-token overhead 与 generated-output tokens 已区分。
- [ ] RQ3.3 已说明 mapper、finalizer 和 API Tok. 的关系，且未把 token reduction 等同于延迟/费用节省。
- [ ] RQ3.3 表格可由 artifact 中的 usage 记录或复算脚本核对。
- [ ] RQ1/RQ2/RQ3 中 GLM 的证据角色已明确区分。
- [ ] 全文不再用同源 R1 模型支撑独立跨家族泛化。
- [ ] validity judge、annotation 合并和模型调用信息达到最小可复现程度。
- [ ] benchmark-level 外部效度边界已写清楚。
- [ ] Abstract、Findings、Threats、Conclusion 和蓝色修订内容已统一。
