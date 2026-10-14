# Agent Harness 最佳实践现状综述（2026-08）

> 整理日期：2026-08-03 · 性质：跨文章综述（非单篇精读）
> 基线文章：Anthropic《Harness design for long-running application development》（2026-03-24，[本地笔记](Anthropic/Engineering全集_逐句对照/21_harness-design-long-running-apps_直观图解与学习笔记.md)）
> 覆盖范围：2026 年 3 月至 8 月初的官方文章、参考实现、产品发布与社区讨论，信源清单见文末

## 一句话结论

**三月文章的方法论没有被推翻，而是被产品化了。** 生成与评判分离、状态外置文件系统、模型升级后做消融减法——这三条在 2026 年 8 月依然是行业共识，且已从「每家手搓」沉淀为 Anthropic 的官方产品原语（Outcomes、`/goal`、Managed Agents、动态工作流）。同时 Claude 5 家族把能力边界又外推了一截，带来一条新共识：**运行框架（harness）不是在消失，而是在换形态——从「行为管教层」（逼模型自查、强制流程）收缩，向「基础设施层」（记忆、验收、容错、成本控制）转移。** 三个角色里，规划器（planner）降级为可选，评估器（evaluator）的独立上下文架构依旧承重，因为自评乐观是架构性缺陷，不随模型变强而消失。

## 这五个月发生了什么：时间线

| 日期                 | 事件                                                          | 对 harness 的意义                                     |
| ------------------ | ----------------------------------------------------------- | ------------------------------------------------- |
| 2026-02-11         | OpenAI《Harness engineering》（Ryan Lopopolo）                  | OpenAI 侧同名学科成立：「仓库即 harness」                      |
| 2026-03-24         | Anthropic《Harness design for long-running apps》             | 本综述的基线：planner/generator/evaluator 三角色            |
| 2026-03-25         | Anthropic《Claude Code auto mode》                            | 无人值守长跑的权限前提：分级放行 + 两阶段分类器                         |
| 2026-04-08         | Anthropic《Scaling Managed Agents》                           | harness 升格为基础设施：brain/hands/session 三层解耦          |
| 2026-04-19 / 04-28 | Addy Osmani《Agent Harness Engineering》《Long-Running Agents》 | 公开圈最好的综述：确认跨产品/跨 harness 架构趋同                     |
| 2026-05 上旬         | Code with Claude 2026 大会（SF；各信源日期记载不一）                      | 刻意不发新模型，只发 harness 原语                             |
| 2026-05-19         | 官方博客《New in Claude Managed Agents》                          | Outcomes（评分智能体，公测）、多智能体编排（公测）、Dreaming（记忆整理，研究预览） |
| 2026-05 中旬         | Claude Code `/goal`（v2.1.139+）                              | 生成/评判分离做成单命令                                      |
| 2026-06-02         | 官方博客《A harness for every task》                              | 动态工作流：harness 本身也由模型现场生成                          |
| 2026-06-09         | Claude Fable 5 / Mythos 5 发布                                | 官方首次在发布公告里宣告模型需要 "less scaffolding"               |
| 2026-06-22         | OpenAI《Codex-maxxing for long-running work》白皮书              | harness 概念扩展到工作区层：durable threads、memory vault    |
| 2026-06-30 / 07-24 | Claude Sonnet 5 / Opus 5 发布                                 | 能力边界继续外推；「删脚手架」成为迁移主题                             |

## 三月文章的存废清单（本文最重要的一节）

把三月文章的每个组件对着 2026 年 8 月的现状逐一核对：

| 三月文章的组件/主张                | 2026-08 状态      | 依据                                                                                                                            |
| ------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 规划器（planner）独立成角色         | **降级为可选**       | Fable 5 原生跨阶段规划、自主委派子智能体；社区技术报告把显式 planner 列为可选项——「给目标而非步骤」                                                                   |
| 评估器（evaluator）独立成角色       | **指令层删除，架构层保留** | 见下文详述——这是理解现状的关键                                                                                                              |
| 冲刺分解 + 上下文重置              | **退役**          | 三月文章 V2 自己已删；新范式是 memory tool（跨会话）+ context editing（会话内清理）+ compaction（按需）三层组合，叠加 1M 上下文窗口                                    |
| 冲刺契约（sprint contract）     | **活着，且被产品化**    | `/goal` 官方条件模板（可度量终态 + 验证方式 + 约束 + 轮次上限）就是它的轻量版；Outcomes 的 rubric 定义是它的托管版                                                    |
| 通信全走文件、文件即外部状态            | **全面胜出**        | 官方多智能体编排沿用共享文件系统；Anthropic 数据：file-based memory 对 Fable 5 的性能提升约为对 Opus 4.8 的 3 倍（Slay the Spire 游戏基准）——至少在该基准上，记忆脚手架的回报反而更高了 |
| 评估器走真实交互（Playwright 实测）   | **依然是标准做法**     | 官方参考实现的证据门控（截图/日志才算数）、OpenAI 侧的 Chrome DevTools 协议接入，思路一致                                                                     |
| 「每个组件都编码一条能力假设，要反复压测」     | **升格为架构原则**     | Managed Agents 文把它上升为架构原则（接口稳定、实现可换——即接口要比假设活得久）；官方参考实现 README 把「模型升级后逐个注释组件」写进操作步骤                                           |
| 成本账（单智能体 $9 vs 完整框架 $200） | **仍是必须算的账**     | 官方明说动态工作流「更耗 token，适合复杂高价值任务」；HN 反方报告数百智能体工作流单次执行成本数百美元                                                                       |

### 评估器的现状要单独讲清楚

这是 2026 年中最容易讲错的一点。准确的表述是**「指令层删除、架构层保留」**：

- **指令层（已过时甚至有害）**：为旧模型写的「你必须自查」「每步强制验证」这类提示词脚手架，在 Opus 5 / Fable 5 上会引发过度验证、成本上升甚至性能下降——新模型默认主动自验证。
- **架构层（依旧承重）**：独立上下文的评审者仍然显著优于自评。据多个二手信源转述的 Anthropic 内部实验（Parameter Golf）：独立上下文的 verifier 子智能体抓出约 73% 的埋点问题，同上下文自评只有 7–33%。三月文章「模型对自己的产出天然乐观」这个动机没有过时，**只是解法从「常驻评估器智能体」变成了「按需的、独立上下文的评审子智能体」**。
- 判断标准依然是三月文章的能力边界三分法：任务在模型能稳定单干的范围内，评估器是纯开销；在边界上，评估器抓真缺口；超出边界，才需要分解加专门智能体。Claude 5 把边界又外推了，但边界之外评估器依旧承重。

## 当前六条核心共识

**1. 生成与评判分离，评判者必须有独立上下文。** Outcomes 的打分智能体「在自己的上下文窗口评估、刻意不看任务智能体的推理过程」；`/goal` 用一个全新的小模型（默认 Haiku）判断完成条件。自建系统时评估器永远不要共享生成器的上下文。

**2. 状态放文件系统和会话日志，不放上下文窗口。** Managed Agents 的三层解耦是这条的基础设施化：brain（模型 + 无状态 harness）/ hands（沙箱与工具，统一为 `execute(name, input) → string` 接口）/ session（append-only 事件日志，`getEvents()` 按位置切片读取）。容器当牲口不当宠物：挂了就是一次工具调用错误，`provision` 新的重试；harness 挂了 `wake(sessionId)` 从日志恢复。按需拉起容器直接换来 p50 首 token 时间下降约 60%、p95 下降超过 90%。

**3. 「做完」写成可验证契约，默认失败。** 官方参考实现 [cwc-long-running-agents](https://github.com/anthropics/cwc-long-running-agents) 的三原语可以直接抄：**default-FAIL 契约**（`test-results.json` 每个功能初始 `false`，只有结构化证据——截图、console 日志、result 文件——才算数）；**证据门控**（`PreToolUse` hook：没读过证据文件就阻断结果写入，写一次清一次日志）；**agent 自维护交接**（`PROGRESS.md` + `Stop` hook 自动 commit）。`/goal` 条件的官方写法四件套：一个可度量终态 + 明示验证方式（如 "npm test exits 0"）+ 过程约束 + 轮次/时间上限。

**4. 模型升级后做消融减法——「脚手架即技术债」。** 这是 7 月迁移潮的主叙事：为旧模型弱点写的补偿性指令（MUST 式工具强制语、强制思考循环、强制验证步骤）在 Claude 5 上引发过度触发；据社区分析，前沿模型只能可靠遵循约 150–200 条指令；据 Boris Cherny 在 Opus 5 发布后的访谈，Claude Code 系统提示迁移时删掉约 80% 而基准无回归。方法不变：一次只删一个组件，用冻结的 eval 验证——「简化模型指令，而不是放松验收标准」。

**5. 安全靠结构性隔离，不靠弹窗。** 凭证对沙箱结构性不可达（资源捆绑式 auth，或 vault + 专用 proxy）；权限分级（只读直通 / git 可回滚的项目内写操作免审 / shell 与网络走两阶段分类器）；审查器 reasoning-blind——只看用户消息和工具调用，剥掉模型自述，防止被辩解说服。拦截用 deny-and-continue 而非硬终止，让误报在长跑中的代价只是一次重试。

**6. 先用平台原语，再手搓；自己只写领域判断。** 2026 年的默认起点是 Claude Agent SDK（loop、压缩、子智能体、hooks、会话恢复、checkpoint 全内置）或 Managed Agents（连沙箱都托管）。真正留给你的活是 rubric 内容、领域工具、验收阈值——**rubric 本身是隐性目标函数，措辞直接改变产出风格，这部分永远是人的判断力**。

## 手搓组件 → 产品原语对照表

三月文章里作者手搓的每个组件，现在都有官方产品化形态：

| 2026-03 手搓组件                          | 2026-08 产品原语                       | 备注                                                                                   |
| ------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------ |
| 独立评估器 + rubric + 硬阈值 + 打回重做           | **Outcomes**（Managed Agents，公测）    | 官方内部基准：文件生成任务成功率 docx +8.4%、pptx +10.1%                                              |
| 评估器外循环（跑到达标为止）                        | **`/goal`**（Claude Code v2.1.139+） | 实现上就是会话级 prompt-based Stop hook 的封装；条件上限 4,000 字符                                    |
| 「测试真的过了才许停」                           | **agent-based Stop hook**（实验性）     | 带工具的多轮验证钩子                                                                           |
| 上下文重置 + 交接文档                          | **三层压缩体系**                         | microcompact / full compact / session memory compact，API 级 compaction 2026-01 发 beta |
| `claude-progress.txt` 式进度记忆           | **Dreaming**（研究预览）                 | 定时进程在会话间提取模式、重构记忆保信噪比                                                                |
| planner-generator-evaluator 编排 + 文件通信 | **多智能体编排**（公测）+ **动态工作流**          | lead 委派 specialist、共享文件系统；动态工作流让 Claude 现场生成编排代码                                     |
| 「每轮产物都要留档」                            | **checkpoints / `/rewind`**        | 每次改动前自动存档，代码/对话可分别恢复，保留 30 天                                                         |
| 逐工具人工审批                               | **auto mode**                      | 与 `/goal` 正交互补：auto mode 消逐工具审批，`/goal` 消逐轮催促                                        |

官方在 6 月 2 日的动态工作流博客里点名的三种失败模式——智能体偷懒（agentic laziness，复杂任务提前停手）、自我偏袒（self-preferential bias，自我验证偏袒）、目标漂移（goal drift，多轮后目标漂移）——正是 2025-11 与 2026-03 两篇文章诊断的问题。**产品化的是机制，不是判断力：rubric 仍需人工调校。**

## 脚手架没有消失，而是换了形态

Claude 5 时代删掉了行为管教类脚手架，但同时出现了**新的必要脚手架**，全部属于基础设施层：

- **拒答处理成为一等代码路径**：Fable 5 的安全分类器平均在不到 5% 的会话中触发（发布公告口径），生产系统必须内建自动 fallback（如回退 Opus 4.8）与重试中间件。Fable 5 发布三天后曾被临时暂停（据 InfoQ 报道）——单一旗舰模型依赖的风险被现实验证过一次。
- **effort 成为新调参维度，且越高不等于越好**：据社区评测，Opus 5 在 FrontierCode 上 medium effort 得 53.4%、xhigh 反而降到 43.6%。正确做法是用冻结 eval 逐档实测，取能可靠完成工作的最低档。
- **参数清理**：Fable 5 废除 temperature/top_p/top_k/budget_tokens（传入即 400 错误），自适应思考永远开启；据社区技术报告，输出 token 比 Opus 级多约 30%，token 预算要重测。
- **异步设计**：单请求可合法运行数分钟，streaming/轮询是标配。
- **记忆治理**：新失败模式是记忆漂移（memory drift，从非典型交互学到捷径并过度泛化）——把记忆当微服务管。

而 harness 仍是最大杠杆的证据在 2026 年反而更硬了：

> **数字：同一个 Fable 5，Cursor harness 比 Claude Code harness 的功能通过率高 12.8 个百分点（72.6% vs 59.8%，Endor Labs 2026-06 实验）；ARC-AGI-3 上同代 Claude 模型在不同 harness 与配置下的公开成绩从约 1.5% 到 30%+ 不等（差距含 reasoning effort 配置因素，个别更高宣称存在过拟合争议）。「拉开差距的是 harness 而非模型。」**

另一条被泼冷水的路线：让智能体自动进化 harness。arXiv 2607.12227（2026-07）在 Terminal-Bench 2.1 上实测，自动 harness 进化并不稳定优于简单的 test-time scaling 且泛化有限（实验基于 GPT-5.4 / Opus 4.6，尚未在 Claude 5 上复现）——**手工设计 + eval 驱动的删减仍是当前最佳实践**。

## OpenAI 侧对照：「仓库即 harness」

OpenAI 的路线与 Anthropic 同题不同层（详见[本地精读](OpenAI/最新/04_Harness-engineering_中文精读.md)）。Anthropic 做「运行内架构」（一次长跑内部的角色分工与上下文管理），OpenAI 做「仓库即 harness」——把可读性、约束、文档、可观测性压进 repo 与组织流程：

- **AGENTS.md 当地图不当百科**：单一大 AGENTS.md 被明确宣布失败（挤占上下文、指导过多则一切失焦、立即腐烂、无法机械校验）；替代方案是约 100 行的目录，指向结构化 docs/ 知识库，配专职 linter + doc-gardening 智能体自动开修复 PR。
- **约束机械化**：分层架构靠自定义 linter 强制，且 **lint 报错信息直接写成给智能体的修复指令**——错误信息就是注入上下文的提示词。
- **评审 agent 化**：本地自审 → 请求专门评审智能体 → 循环到全部满意；后台 GC 智能体每天扫漂移、开小重构 PR 自动合并——熵治理从「每周五人工清理 AI 残渣」进化为自动化。
- **实验数据**：空仓库起步 5 个月约 100 万行代码、0 行人工编写、约 1,500 个 PR（单一内部实验的官方自估，无对照组，质量无第三方核验）；单次 Codex 运行常超 6 小时。另一实验：GPT-5.3-Codex 不间断运行约 25 小时、产出约 3 万行代码，靠 Prompt.md / Plan.md / Implement.md / Documentation.md 四文件持久项目记忆。
- **合流证据**：6 月的 Codex-maxxing 白皮书把 durable threads、memory vault、thread automations 产品化，对应 Anthropic 的 Managed Agents 路线；使用数据显示 2026 年 5 月抽样中 25.6% 的用户发起过 8 小时级等价工作量请求——长任务已是常态而非演示。

两家的共识可以合成一句：**Anthropic 把状态外置到会话日志，OpenAI 把知识外置到仓库——方向相同：智能体运行时上下文里拿不到的知识等于不存在。**

## 反方声音：值得记住的批评

面试或设计评审里只讲共识会显得没有批判性，这些反方观点同样来自 2026 年的公开讨论：

- **70/30 帕累托问题**（HN）：LLM 轻松做到前 70%，给管理层制造虚假乐观；剩下 30% 需要昂贵基础设施（多智能体、评审框架），有人报告数百智能体工作流单次执行成本数百美元且无可靠性保证。
- **理解无法外包**（HN）：写代码与理解系统同时发生，这部分认知劳动委托给 LLM 后不会消失，只会延迟到 code review、测试或生产事故时偿还——这是对「规格写好就能全托管」叙事的直接反驳。
- **控制的根本局限**（HN）：「你能提供的最好控制就是恳求它别做某事」——靠拟人化指令而非确定性保证。auto mode 的量化印证：完整流水线在真实越权动作上的漏报率（FNR）仍有 17%。
- **专职 QA 智能体会失效**（HN 实践者）：开发智能体和测试智能体方法分歧导致收敛问题，陷入循环——评估器不是免费午餐，需要校准投入。
- **极端乐观预测与现实的张力**：Boris Cherny（Claude Code 作者）称自己约八个月没手写过代码、预言 Claude Code 一年后可能只剩 100 行；而 Osmani 的观察是 harness 复杂度不缩小、只是转移到新任务层。目前证据更支持后者。
- **数字要打折**：Anthropic 自己承认「8x 产出」几乎可以肯定是高估（官方报告中更可比的同任务对照约为 4x）；Harvey 的 6 倍、Wisedocs 的 50% 是客户自报；Outcomes 的 +8.4%/+10.1% 是内部基准，无第三方验证。

## 数字备忘（面试硬通货）

| 数字 | 出处 |
|---|---|
| 单智能体 $9/20 分钟 vs 完整框架 $200/6 小时（贵 20+ 倍） | 三月文章原文 |
| 独立上下文 verifier 抓 ~73% 埋点问题 vs 同上下文自评 7–33% | Anthropic 内部实验（Parameter Golf），经二手转述 |
| TTFT p50 -60%、p95 -90%+ | Managed Agents 解耦（2026-04-08） |
| Outcomes：文件生成任务成功率 docx +8.4%、pptx +10.1% | 官方博客（2026-05-19，内部基准） |
| file-based memory 对 Fable 5 的提升 ≈ 对 Opus 4.8 的 3 倍 | Fable 5 发布公告（Slay the Spire 游戏基准） |
| 同一 Fable 5 换 harness：功能通过率差 12.8pp | Endor Labs（2026-06-17） |
| 前沿模型可靠遵循指令上限约 150–200 条；Claude Code 系统提示迁 Opus 5 删约 80% 无回归 | 社区分析（Corti 2026-07 等） |
| Opus 5 FrontierCode：medium 53.4% > xhigh 43.6% | 社区评测转述 |
| 用户对 93% 的权限弹窗未细看即同意 | auto mode 文章（2026-03-25） |
| 25.6% 用户发起过 8 小时级请求（2026-05 抽样） | OpenAI《How agents are transforming work》（2026-06-25） |

注意一个常见口误：**「30+ 小时自主编码」出自 Sonnet 4.5 时代（2025 年）的内部观察，不是 Claude 5 家族的官方宣称**——Claude 5 的官方口径是定性的 "sustained autonomy" 加数小时至数天级实测案例。

## 面试高频问答

**Q：三月那篇三智能体文章现在还算最佳实践吗？**
A：方法论算，具体架构要打折。三条核心（生成/评判分离、真实交互验收、模型升级做消融）已成行业共识并被产品化。但三角色本身：planner 因为新模型原生规划能力已降级为可选；evaluator 要分两层说——逼模型自查的指令层已过时甚至有害，独立上下文评审的架构层依旧承重（据二手转述的内部实验，独立 verifier 抓 73% 问题 vs 自评 7–33%）；冲刺分解和上下文重置则被 memory tool + context editing + compaction 三层组合取代。

**Q：模型这么强了，为什么还要 harness？**
A：两个证据。一是同模型换 harness 差距仍然巨大：同一个 Fable 5 在 Cursor 和 Claude Code 里功能通过率差 12.8 个百分点，ARC-AGI-3 上不同 harness 差一个数量级以上。二是脚手架在换形态而非消失：行为管教类该删（前沿模型可靠遵循的指令只有约 150–200 条，多了反而有害），但 refusal fallback、异步设计、记忆治理、验收契约这些基础设施层脚手架是新增的刚需。

**Q：新模型发布后你会怎么处理现有 harness？**
A：迁移基线法：先在旧模型上冻结一个 eval 基线，只换模型字符串跑对照，再动提示词。然后做消融——一次只删一个组件，验证是否还承重；优先删的是补偿性指令（MUST 式强制、强制验证循环），保留的是验收标准、完成定义和安全边界。一句话：「简化模型指令，而不是放松验收标准。」实例：Claude Code 迁 Opus 5 时删了约 80% 系统提示而基准无回归。

**Q：怎么防止长跑智能体「做了一半说全部完成」？**
A：default-FAIL 契约加证据门控。结果文件里每个功能初始标 false，只有结构化证据（截图、console 日志、测试输出）才允许翻转；用 PreToolUse hook 强制「没读过证据文件就不许写结果文件」；评审交给独立上下文的只读子智能体，按字面打开证据核验，不信任文件名。这套在 Anthropic 官方参考实现 cwc-long-running-agents 里有可直接抄的代码。

**Q：无人值守跑一晚上，怎么配？**
A：正交两件套：auto mode 消除逐工具审批（分级权限 + 两阶段分类器），`/goal` 消除逐轮催促（小模型每轮判完成条件）。goal 条件要写成 transcript 里可证明的形式（评估器不跑命令不读文件），带轮次上限兜底；再配 kill-switch 文件（`touch AGENT_STOP` 即停）和 `STEER.md` 中途转向。凭证走 vault，永不进沙箱。

## 必须记住的 10 句话

1. 三月文章没有被推翻，而是被产品化了——评估器变成 Outcomes 和 `/goal`，编排下沉进 Managed Agents。
2. Harness 不是在消失，而是从行为管教层转移到基础设施层。
3. Planner 降级为可选，evaluator 的独立上下文架构永远承重——自评乐观是架构性缺陷，不随模型变强而消失。
4. 评判者必须有独立上下文：独立 verifier 抓 73% 问题，同上下文自评只有 7–33%（Parameter Golf 内部实验，二手转述）。
5. 状态放文件系统和会话日志，不放上下文窗口——智能体可以失忆，存储不失忆。
6. 「做完」要写成 default-FAIL 契约：无证据即失败，证据是文件不是声称。
7. 每个 harness 组件都编码一条「模型做不到什么」的假设；模型升级后逐个消融，接口要比假设活得久。
8. 简化模型指令，而不是放松验收标准——据社区分析，前沿模型可靠遵循的指令只有约 150–200 条。
9. 同模型换 harness 差 12.8 个百分点——把失败归咎于模型能力，通常是 harness 配置问题。
10. 平台原语解决机制，你解决判断力——rubric 是隐性目标函数，措辞直接改变产出风格。

## 30 秒口述版

> 2026 年 3 月那篇三智能体 harness 文章，到 8 月的现状是「方法论全面胜出、具体架构被产品化」。生成评判分离变成了 Outcomes 和 `/goal`，文件外置状态变成了 Managed Agents 的会话日志，消融减法变成了每次模型发布后的标准迁移动作。Claude 5 时代的新共识是脚手架换形态：删掉逼模型自查的行为管教，新增 refusal fallback、异步设计、记忆治理这些基础设施。三个角色里 planner 可选了，但 evaluator 的独立上下文架构永远承重，因为自评乐观不随模型变强消失——据内部实验的二手转述，独立评审抓 73% 的问题，自评只有 7% 到 33%。同一个 Fable 5 换个 harness 功能通过率差 12.8 个百分点——模型决定下限，harness 仍然决定你拿到多少。

## 自测

- [ ] 能说出评估器「指令层删除、架构层保留」的含义和 73% vs 7–33% 的数据吗？
- [ ] 能列出三月文章至少 5 个手搓组件对应的产品原语吗？
- [ ] 能解释 default-FAIL 契约 + 证据门控的具体机制（两个 hook 各干什么）吗？
- [ ] 能讲出「新增的基础设施层脚手架」至少 3 项吗？
- [ ] 能复述迁移基线法的操作顺序吗？
- [ ] 能举出至少 3 条反方观点并给出自己的回应吗？

## 相关本地笔记

- 📚 **[Harness 延伸阅读 · 双语精读专题目录](Harness延伸阅读_双语精读/00_目录.md)** —— 本文引用的、值得读原文的 9 篇信源已全部扒下来做成双语精读（含参考实现、`/goal` 文档、Osmani 两篇综述、Codex-maxxing 白皮书、HN 反方讨论）
- [15_effective-harnesses-for-long-running-agents（2025-11-26，两段式前身）](Anthropic/Engineering全集_逐句对照/15_effective-harnesses-for-long-running-agents_直观图解与学习笔记.md)
- [21_harness-design-long-running-apps（2026-03-24，本综述基线）](Anthropic/Engineering全集_逐句对照/21_harness-design-long-running-apps_直观图解与学习笔记.md)
- [22_claude-code-auto-mode（2026-03-25，逐句对照）](Anthropic/Engineering全集_逐句对照/22_claude-code-auto-mode_逐句对照.md)
- [23_managed-agents（2026-04-08，基础设施化）](Anthropic/Engineering全集_逐句对照/23_managed-agents_直观图解与学习笔记.md)
- [OpenAI 04_Harness-engineering（2026-02-11，仓库即 harness）](OpenAI/最新/04_Harness-engineering_中文精读.md)
- [00_两家公司Agent技术路线对照](00_两家公司Agent技术路线对照.md)

## 信源清单与可靠度说明

**官方一手**：
- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)（2026-03-24）
- [How we built Claude Code auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode)（2026-03-25）
- [Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)（2026-04-08）
- [New in Claude Managed Agents](https://claude.com/blog/new-in-claude-managed-agents)（2026-05-19）
- [A harness for every task: dynamic workflows](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)（2026-06-02）
- [cwc-long-running-agents 参考实现](https://github.com/anthropics/cwc-long-running-agents) · [`/goal` 文档](https://code.claude.com/docs/en/goal)
- [Claude Fable 5 / Mythos 5 发布](https://www.anthropic.com/news/claude-fable-5-mythos-5)（2026-06-09）
- [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/)（2026-02-11）· [Codex-maxxing 白皮书](https://openai.com/index/codex-maxxing-long-running-work/)（2026-06-22）

**高质量二手**：
- [Addy Osmani: Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/)（2026-04-19）· [Long-Running Agents](https://addyosmani.com/blog/long-running-agents/)（2026-04-28）
- [InfoQ 三智能体 harness 分析](https://infoq.com/news/2026/04/anthropic-three-agent-harness-ai/)（2026-04-04）
- [Hightouch 生产案例](https://www.amplifypartners.com/blog-posts/how-hightouch-built-their-long-running-agent-harness)（2026-01-20，作者为投资方，无量化数据）
- [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering)（社区分类法，3.4k stars）
- [HN 讨论：Effective harnesses](https://news.ycombinator.com/item?id=46081704)（反方观点主要来源）

**需要打折的数字**：Parameter Golf 的 73%/7–33% 经多层二手转述，原始出处未直接核验；「8x 产出」Anthropic 自认高估（官方报告更可比的同任务对照约 4x）；Harvey 6x、Wisedocs 50% 为客户自报；150–200 条指令上限、FrontierCode effort 对比来自社区分析（Corti 等），非官方口径；Fable 5 输出 token +30% 出自社区技术报告（HuggingFace）；OpenAI 百万行实验为单一内部实验自估、无对照组；Code with Claude 大会具体日期各信源记载不一（5 月 6/8/12 日均有）。

> 本文为跨信源综述，观点归属以文内标注为准；引用请回到官方原文核对。
