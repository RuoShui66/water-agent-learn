# B14_Common workflow patterns for AI agents—and when to use them_AI 智能体的常见工作流模式及适用时机

> 原文：https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them
> 来源：Claude Blog｜发布日期：2026-03-05

## 📌 本篇速览

- 📅 2026-03-05　｜　⏱ 约 8 分钟　｜　📄 约 1,100 词 / 3 图
- 🏷 Agent 工作流、Sequential（串行）、Parallel（并行）、Evaluator-Optimizer（评估–优化）、多智能体编排
- 🗂 [返回目录](00_目录与阅读进度.md)

本文总结了 Anthropic 与几十个团队合作构建 AI 智能体后的观察：生产环境中三种工作流模式覆盖了绝大多数用例——串行（按固定顺序执行）、并行（多个智能体同时处理独立任务）、评估–优化（生成与评估两个智能体迭代打磨输出）。文章逐一给出每种模式的定义、适用时机、避免场景、典型示例与实践建议，并提供选型判断问题清单与模式组合思路。核心原则是克制：先用单个智能体试，能解决就不上工作流；默认串行，延迟成瓶颈且任务独立才并行，能测量出质量改进才加评估–优化循环。

---

[AI agents](https://www.anthropic.com/research/building-effective-agents) make decisions autonomously, and workflows are how you bring structure to that autonomy.

[AI 智能体](https://www.anthropic.com/research/building-effective-agents)（AI agent）能够自主决策，而工作流（workflow）正是给这种自主性带来结构的方式。

They establish execution patterns that channel agent capabilities toward complex problems requiring coordinated steps, predictable outcomes, and orchestrated timing.

工作流确立了执行模式（execution pattern），把智能体的能力引向那些需要多步协同、结果可预测、时序可编排的复杂问题。

When you need multiple agents working together, the real decision is which pattern fits your problem.

当你需要多个智能体协同工作时，真正要做的决策是：哪种模式适合你的问题。

We've worked with dozens of teams building AI agents, and in production, three patterns cover the vast majority of use cases: sequential, parallel, and evaluator-optimizer.

我们与几十个构建 AI 智能体的团队合作过，在生产环境中，三种模式覆盖了绝大多数用例：串行（sequential）、并行（parallel）和评估–优化（evaluator-optimizer）。

Each solves different problems, and picking the wrong one costs you in latency, tokens, or reliability.

每种模式解决的问题各不相同，选错模式会让你在延迟、token 开销或可靠性上付出代价。

This piece breaks down all three, with guidance on when each fits and how to combine them.

本文将逐一拆解这三种模式，说明各自的适用时机以及如何组合使用。

## How workflows and agents work together｜工作流与智能体如何协同

If you've managed a team, you already understand workflows.

如果你带过团队，你其实已经懂工作流了。

Think of a manufacturing assembly line: each station has a skilled worker making decisions about their specific tasks, but the overall flow is designed ahead of time—even when individual steps involve dynamic decisions like routing or retries.

想象一条制造业流水线：每个工位都有一名熟练工人，对自己负责的具体任务做决策，但整条产线的流程是提前设计好的——即使个别环节包含路由（routing）或重试（retry）这类动态决策。

Agent workflows operate the same way.

智能体工作流的运作方式完全相同。

### Understanding workflows vs. autonomous agents｜理解工作流与自主智能体的区别

Workflows don't replace agent autonomy; they shape where and how agents apply it.

工作流并不取代智能体的自主性，而是塑造这种自主性在何处、以何种方式发挥作用。

**A fully autonomous agent decides everything**: which tools to use, what order to execute tasks, and when to stop.

**完全自主的智能体自己决定一切**：用哪些工具、按什么顺序执行任务、何时停止。

**A workflow provides structure**: it establishes the overall flow, defines checkpoints, and sets boundaries for how agents operate at each step, while still allowing dynamic behavior within those boundaries.

**工作流提供的是结构**：它确立整体流程、定义检查点（checkpoint），并为智能体在每一步的行为划定边界，同时在边界之内仍然允许动态行为。

Each step in a workflow can still leverage an agent's reasoning and tool use, but the overall orchestration follows a defined path.

工作流中的每一步依然可以利用智能体的推理和工具使用能力，但整体编排（orchestration）遵循一条预定义的路径。

A workflow pattern gives you agent intelligence within each step, and a predictable process flows across the entire task.

工作流模式给你的，是每一步之内的智能体智能，以及贯穿整个任务的可预测流程。

## Agent workflow patterns｜智能体工作流模式

In production, we see three workflow patterns come up most often.

在生产环境中，我们看到三种工作流模式出现得最频繁。

Think of these as building blocks rather than rigid templates—you'll often combine or nest them as your requirements evolve:

把它们当成积木（building blocks）而不是僵化的模板——随着需求演化，你会经常组合或嵌套它们：

1. **Sequential workflows** — for executing tasks in a fixed order

1. **串行工作流**——用于按固定顺序执行任务

2. **Parallel workflows** — for running independent tasks across agents simultaneously

2. **并行工作流**——用于让多个智能体同时运行相互独立的任务

3. **Evaluator-optimizer workflows** — for outputs that need iterative refinement

3. **评估–优化工作流**——用于需要迭代打磨的输出

Each workflow type solves specific problems and comes with clear tradeoffs around complexity, cost, and performance.

每种工作流类型都解决特定的问题，也各自带着围绕复杂度、成本和性能的明确取舍。

Start with the simplest pattern that solves your problem.

从能解决你的问题的最简单模式开始。

Default to sequential.

默认选串行。

Move to parallel when latency is the bottleneck and tasks are independent and add evaluator-optimizer loops only when you can measure the quality improvement.

当延迟成为瓶颈且任务相互独立时再转向并行；只有当你能测量出质量改进时，才加入评估–优化循环。

### Sequential workflows｜串行工作流

Sequential workflows execute tasks in a predetermined order.

串行工作流按预先确定的顺序执行任务。

Agents at each stage process inputs, make decisions, make tool calls as needed, then pass results to the next stage.

每个阶段的智能体处理输入、做出决策、按需调用工具，然后把结果传递给下一个阶段。

The result is a clear chain of operations where outputs flow linearly through the system.

最终形成一条清晰的操作链，输出线性地流经整个系统。

![figure 1](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69a9d98c9196625199b6a5f0_fig1-sequential-workflow-v1%20(1).png)

**When to use:** Sequential workflows excel when tasks naturally break down into distinct stages with clear dependencies.

**何时使用**：当任务能天然拆分成依赖关系清晰的多个不同阶段时，串行工作流表现最佳。

You're trading some latency for higher accuracy by focusing each agent on a specific subtask instead of trying to handle everything at once.

你是在用一些延迟换取更高的准确率——让每个智能体专注于一个具体的子任务，而不是试图一次性包揽一切。

Use sequential workflows when there are:

在以下情况使用串行工作流：

- Multi-stage processes where each step depends on the previous output

- 多阶段流程，每一步都依赖上一步的输出

- Data transformation pipelines where each stage adds specific value

- 数据转换流水线（data transformation pipeline），每个阶段增加特定的价值

- Tasks that can't be parallelized due to inherent dependencies

- 因内在依赖关系而无法并行化的任务

- Iterative improvement cycles like draft-review-polish cycles

- 迭代改进循环，比如草稿–评审–润色（draft-review-polish）这样的循环

**When to avoid:** Skip sequential workflows when a single agent can handle the entire task effectively, or when agents need to collaborate rather than hand off work sequentially.

**何时避免**：当单个智能体就能有效处理整个任务，或者智能体之间需要的是协作而非顺序交接工作时，就不要用串行工作流。

If you're forcing a task into sequential steps when it doesn't naturally fit that structure, you're adding unnecessary complexity.

如果你把一个天然不适合串行结构的任务硬掰成串行步骤，那只是在添加不必要的复杂度。

**Example:** Sequential workflows work well when each step involves genuinely different work:

**示例**：当每一步涉及的确实是性质不同的工作时，串行工作流效果很好：

- Generating marketing copy, then translating it into multiple languages—or extracting data from documents, validating it against a schema, and loading it into a database

- 先生成营销文案，再把它翻译成多种语言；或者从文档中抽取数据、按 schema 校验、再载入数据库

- Content moderation pipelines also work well sequentially: extract content, classify it, apply moderation rules, then route appropriately

- 内容审核流水线也很适合串行：抽取内容、进行分类、应用审核规则、然后恰当地路由分发

**Pro tip:** First try your pipeline as a single agent, where the steps are just part of the prompt.

**实践建议**：先把整条流水线当成单个智能体来试——各个步骤只是提示词的一部分。

If that's good enough, you've solved the problem without additional complexity.

如果效果够好，你就在没有额外复杂度的情况下解决了问题。

Only split into a multi-step workflow when a single agent can't handle it reliably.

只有当单个智能体无法可靠完成时，才拆分成多步工作流。

### Parallel workflows｜并行工作流

Parallel workflows distribute independent tasks across multiple agents that execute simultaneously.

并行工作流把相互独立的任务分发给多个同时执行的智能体。

Instead of waiting for one agent to finish before starting the next, you run multiple agents at once and merge their results.

不必等一个智能体做完再启动下一个，而是让多个智能体同时运行，最后合并它们的结果。

This pattern can deliver speed improvements when tasks don't depend on each other.

当任务之间没有相互依赖时，这个模式能带来速度上的提升。

The approach resembles the fan-out/fan-in pattern from distributed systems.

这种做法类似于分布式系统中的扇出/扇入（fan-out/fan-in）模式。

You send the same or related work to multiple agents, each processes independently, then you aggregate or synthesize their outputs.

你把相同或相关的工作发给多个智能体，各自独立处理，最后聚合（aggregate）或综合（synthesize）它们的输出。

Agents don't hand off work to each other—they operate autonomously and produce results that contribute to the overall task.

智能体之间不互相交接工作——它们各自自主运行，产出的结果共同贡献给整体任务。

![figure 2](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69a9d9d2e30946c46eb80032_fig2-parallel-workflow-v1%20(1).png)

**When to use:** Parallelization makes sense when you can divide work into independent subtasks that benefit from simultaneous processing, or when you need multiple perspectives on the same problem.

**何时使用**：当工作可以拆分成能从同时处理中获益的独立子任务，或者你需要对同一个问题获得多个视角时，并行化才有意义。

It also enables separation of concerns: different engineers can own and optimize individual agents independently without their work interfering with each other.

它还能实现关注点分离（separation of concerns）：不同的工程师可以独立负责和优化各自的智能体，彼此的工作互不干扰。

For complex tasks, handling each consideration with a separate AI call often outperforms trying to juggle everything in one call.

对于复杂任务，用单独的 AI 调用处理每个考量点，往往比试图在一次调用里兼顾一切效果更好。

Consider parallel workflows for:

在以下场景考虑并行工作流：

- Sectioning approaches where different agents handle different aspects (like one processing queries while another screens for safety issues)

- 分区（sectioning）方式：不同智能体处理不同的方面（比如一个处理查询，另一个筛查安全问题）

- Evaluation scenarios where each agent assesses different quality dimensions

- 评估场景：每个智能体评估不同的质量维度

- Voting patterns where multiple agents analyze the same content and you aggregate their assessments

- 投票（voting）模式：多个智能体分析同一份内容，你再聚合它们的评估结果

**When to avoid:** Don't use parallel workflows when agents need cumulative context or must build on each other's work.

**何时避免**：当智能体需要累积的上下文，或必须在彼此的工作基础上继续推进时，不要用并行工作流。

Skip this pattern when resource constraints like API quotas make concurrent processing inefficient, or when you lack clear strategies for handling contradictory results from different agents.

当 API 配额之类的资源限制让并发处理变得低效，或者你缺乏处理不同智能体相互矛盾结果的清晰策略时，也应跳过这个模式。

If result aggregation becomes too complex or degrades output quality, parallelization isn't worth it.

如果结果聚合变得过于复杂，或者会降低输出质量，那并行化就不值得。

**Example:** Parallel workflows work well for:

**示例**：并行工作流适用于：

- Automating evaluations (each agent checks different quality metrics) or code review (multiple agents examine different vulnerability categories)

- 自动化评估（每个智能体检查不同的质量指标）或代码评审（多个智能体检查不同类别的漏洞）

- Document analysis is another strong use case: parallelize extraction of key themes, sentiment analysis, and factual verification, then combine the insights

- 文档分析是另一个很强的用例：并行执行关键主题抽取、情感分析和事实核查，然后把洞察合并起来

**Pro tip:** Design your aggregation strategy before implementing parallel agents.

**实践建议**：在实现并行智能体之前，先设计好你的聚合策略。

Will you take the majority vote?

是取多数投票？

Average confidence scores?

还是对置信度分数取平均？

Defer to the most specialized agent?

还是以最专业的那个智能体为准？

Having a clear plan for synthesizing results prevents you from collecting conflicting outputs with no way to resolve them.

有一套清晰的结果综合方案，能避免你收集了一堆相互冲突的输出却无从化解。

### Evaluator-optimizer workflows｜评估–优化工作流

Evaluator-optimizer workflows pair two agents in an iterative cycle: one generates content, another evaluates it against specific criteria, and the generator refines based on that feedback.

评估–优化工作流让两个智能体组成一个迭代循环：一个生成内容，另一个按特定标准评估内容，生成者再根据反馈进行改进。

This continues until the output meets your quality threshold or hits a maximum iteration count.

这个循环持续进行，直到输出达到你的质量阈值，或达到最大迭代次数。

The key insight is that generation and evaluation are different cognitive tasks.

关键洞察在于：生成和评估是两种不同的认知任务。

Separating them lets each agent specialize—the generator focuses on producing content, the evaluator focuses on applying consistent quality criteria.

把它们分开能让每个智能体各有专攻——生成者专注于产出内容，评估者专注于一致地应用质量标准。

![figure 3](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69a9d9f9dc54bd92bd71f921_fig3-evaluator-optimizer-workflow-v1%20(1).png)

**When to use:** This pattern works when you have clear, measurable quality criteria that an AI evaluator can apply consistently, and when the gap between first-attempt and final quality is meaningful enough to justify the extra tokens and latency.

**何时使用**：当你有清晰、可测量、AI 评估者能一致应用的质量标准，且首次尝试与最终质量之间的差距足够大、值得付出额外的 token 和延迟时，这个模式才适用。

Consider evaluator-optimizer workflows for:

在以下场景考虑评估–优化工作流：

- Code generation with specific requirements (security standards, performance benchmarks, style guidelines)

- 有特定要求的代码生成（安全标准、性能基准、代码风格规范）

- Professional communications where tone and precision matter

- 语气和精确度很重要的专业沟通文案

- Any scenario where first-draft quality consistently falls short of requirements

- 任何初稿质量持续达不到要求的场景

**When to avoid:** Skip evaluator-optimizer workflows when first-attempt quality already meets your needs—you're burning tokens on unnecessary iterations.

**何时避免**：当首次尝试的质量已经满足需求时，就不要用评估–优化工作流——那是在不必要的迭代上白白烧 token。

Don't use this pattern for real-time applications requiring immediate responses, simple routine tasks like basic classification, or when evaluation criteria are too subjective for an AI evaluator to apply consistently.

需要即时响应的实时应用、基础分类这类简单的例行任务，或评估标准过于主观、AI 评估者无法一致应用的情况，都不要用这个模式。

If deterministic tools exist (like linters for code style), use those instead.

如果存在确定性工具（比如用于代码风格检查的 linter），就直接用那些工具。

Also avoid this pattern when resource constraints outweigh quality improvements.

当资源约束的代价超过质量改进的收益时，也应避免这个模式。

**Example:** Evaluator-optimizer workflows work well for:

**示例**：评估–优化工作流适用于：

- Generating API documentation (generator writes docs, evaluator checks for completeness, clarity, and accuracy against the codebase)

- 生成 API 文档（生成者撰写文档，评估者对照代码库检查完整性、清晰度和准确性）

- Creating customer communications (generator drafts email, evaluator assesses tone and policy compliance)

- 撰写客户沟通内容（生成者起草邮件，评估者评估语气和政策合规性）

- Producing SQL queries (generator writes query, evaluator checks for efficiency and security issues)

- 生成 SQL 查询（生成者编写查询，评估者检查效率和安全问题）

**Pro tip:** Set clear stopping criteria before you start iterating.

**实践建议**：在开始迭代之前，先设定清晰的停止标准。

Define maximum iteration counts and specific quality thresholds.

定义最大迭代次数和具体的质量阈值。

Without these guardrails, you can end up in expensive loops where the evaluator keeps finding minor issues and the generator keeps tweaking, but quality plateaus well before you stop iterating.

没有这些护栏，你可能陷入代价高昂的循环：评估者不停地挑出小毛病，生成者不停地微调，但质量早在你停止迭代之前就已进入平台期。

Know when good enough is good enough.

要知道什么时候"够好"就是真的够好了。

## Choosing the right workflow pattern｜选择合适的工作流模式

The right workflow pattern depends on your task structure, quality requirements, and resource constraints.

合适的工作流模式取决于你的任务结构、质量要求和资源约束。

Before choosing a pattern, try the task as a single agent call first.

在选择模式之前，先用单次智能体调用把任务试一遍。

If that meets your quality bar, you're done.

如果这样就达到了你的质量标准，那就完事了。

If not, identify where it falls short—that tells you which pattern to reach for.

如果没达到，就找出它在哪里不够——这会告诉你该选哪种模式。

Here are a few questions to help you decide:

以下几个问题可以帮你做决策：

- Can a single agent handle this task effectively? If yes, don't use workflows at all.

- 单个智能体能有效处理这个任务吗？能的话，压根不需要用工作流。

- Does the task have clear sequential dependencies? Use sequential workflows.

- 任务是否存在清晰的顺序依赖？有的话，用串行工作流。

- Can subtasks be processed independently and simultaneously, and would faster completion help? Consider parallel workflows.

- 子任务能否独立且同时处理，更快完成是否有帮助？可以的话，考虑并行工作流。

- Does quality improve meaningfully with iterative refinement? Consider evaluator-optimizer patterns.

- 迭代打磨能否带来有意义的质量提升？能的话，考虑评估–优化模式。

Once you've selected a pattern, consider:

选定模式之后，还需要考虑：

- **Failure handling:** Define fallback behavior and retry logic for each step.

- **失败处理**：为每一步定义兜底行为（fallback）和重试逻辑。

- **Latency and cost constraints:** These determine how many agents you can run and how many iterations you can afford.

- **延迟与成本约束**：它们决定了你能跑多少个智能体、负担得起多少次迭代。

- **Measuring improvement:** Set a baseline with a single agent so you can tell whether the workflow actually helps.

- **测量改进**：用单个智能体建立基线（baseline），这样你才能判断工作流是否真的有帮助。

**Combining patterns:** These patterns aren't mutually exclusive.

**组合模式**：这些模式并不互斥。

You can nest them as complexity demands.

你可以按复杂度的需要嵌套使用它们。

- An evaluator-optimizer workflow might use parallel evaluation where multiple evaluators assess different quality dimensions simultaneously.

- 评估–优化工作流可以采用并行评估：多个评估者同时评估不同的质量维度。

- A sequential workflow might include parallel processing at certain stages where multiple independent operations happen before moving to the next step.

- 串行工作流可以在某些阶段引入并行处理：多个独立操作先同时完成，再进入下一步。

The key is matching pattern complexity to actual requirements.

关键是让模式的复杂度与实际需求相匹配。

Don't add parallel processing because you can—add it when concurrent execution provides clear benefits.

不要因为"能加"就加并行处理——只在并发执行能带来明确收益时才加。

Don't implement evaluator-optimizer loops unless they improve output quality in a way you can measure.

除非评估–优化循环能以可测量的方式提升输出质量，否则不要实现它。

## Evolve your workflows thoughtfully｜深思熟虑地演进你的工作流

Our best advice: start with the simplest pattern that works.

我们最好的建议是：从能解决问题的最简单模式起步。

If a sequential workflow handles your use case, don't add parallelization.

如果串行工作流能应对你的用例，就别加并行化。

If first-attempt quality is good enough, skip the evaluator-optimizer loop.

如果首次尝试的质量已经够好，就跳过评估–优化循环。

These three patterns give you clear upgrade paths as requirements change.

这三种模式为你提供了需求变化时的清晰升级路径。

A sequential workflow can incorporate parallel processing at bottleneck stages.

串行工作流可以在瓶颈阶段引入并行处理。

An agentic approach can add evaluation when quality standards tighten, and because these patterns are modular, you won't need complete rewrites.

当质量标准收紧时，智能体方案可以加入评估环节；而且由于这些模式是模块化的，你不需要彻底重写。

For implementation guidance, detailed examples, and advanced patterns including hybrid approaches, check out our full white paper: [*Building effective AI agents: architecture patterns and implementation frameworks*](https://resources.anthropic.com/ty-building-effective-ai-agents).

想了解实现指南、详细示例以及包括混合方案在内的进阶模式，请查阅我们的完整白皮书：[*Building effective AI agents: architecture patterns and implementation frameworks*](https://resources.anthropic.com/ty-building-effective-ai-agents)（构建高效 AI 智能体：架构模式与实现框架）。

*Build on the* [*Claude Developer Platform*](https://claude.com/platform/api) *today.*

*即刻在 [Claude 开发者平台](https://claude.com/platform/api)上开始构建吧。*


---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| workflow | 工作流 | 给智能体自主性套结构的执行模式；区别于 multi-agent 架构层 |
| autonomous agent | 自主智能体 | 自己决定工具、顺序、停止时机 |
| orchestration | 编排 | 步与步之间的整体流程控制 |
| checkpoint | 检查点 | 工作流在流程中预设的验证/控制点 |
| sequential workflow | 串行工作流 | 固定顺序、线性数据流 |
| parallel workflow | 并行工作流 | 独立任务同时执行 |
| evaluator-optimizer workflow | 评估–优化工作流 | 生成器与评估器配对迭代 |
| fan-out / fan-in | 扇出 / 扇入 | 分布式系统术语：分发与聚合 |
| sectioning | 分区 | 并行的一种形态：不同智能体处理不同侧面 |
| voting | 投票 | 并行的一种形态：多智能体判断同一内容后聚合 |
| aggregation strategy | 聚合策略 | 并行结果如何合并/裁决（多数票、平均置信度、专家优先） |
| cumulative context | 累积上下文 | 需要它时不适合并行 |
| separation of concerns | 关注点分离 | 并行的组织收益：不同工程师独立优化各自智能体 |
| stopping criteria | 停止标准 | 评估–优化的护栏：最大迭代次数 + 质量门槛 |
| quality threshold | 质量门槛 | 达标即停止迭代 |
| baseline | 基线 | 先用单智能体建立，用于测量工作流是否真有改进 |
| fallback / retry logic | 兜底行为 / 重试逻辑 | 每一步的失败处理配套 |
| draft-review-polish | 草稿–评审–润色 | 串行工作流的典型循环示例 |
| building blocks | 积木/构建块 | 官方对三种模式的定位：可组合，非僵化模板 |
