# B18_Multi-agent coordination patterns: Five approaches and when to use them_多智能体协调模式：五种方案与适用时机

> 原文：https://claude.com/blog/multi-agent-coordination-patterns
> 来源：Anthropic Claude Blog（分类：Agents ｜ 产品：Claude Platform）｜发布日期：2026-04-10

## 📌 本篇速览

- 📅 2026-04-10　｜　⏱ 官方标注约 5 分钟（逐句精读约 20 分钟）
- 🏷 多智能体系统、协调模式、Generator-Verifier、Orchestrator-Subagent、Agent Teams、Message Bus、Shared State
- 🗂 [返回目录](00_目录与阅读进度.md)

本文承接上一篇《何时该用多智能体系统》，面向已决定采用多智能体、正在纠结用哪种协调模式的团队。作者指出很多团队按「听起来高级」而非「匹配问题」来选模式，建议从可行的最简单模式起步、观察短板、再逐步演进。全文逐一拆解五种模式的运行机制、适用场景与局限：生成器–验证器（质量关键且标准可明确）、编排者–子智能体（任务分解清晰、子任务有边界）、智能体团队（并行独立的长时任务）、消息总线（事件驱动流水线、生态持续增长）、共享状态（协作式研究、发现实时互通），并给出四组两两对比的选型问题与一张速查表。官方建议：多数场景从 orchestrator-subagent 起步，模式可组合、不互斥。

---

*Five multi-agent coordination patterns, their trade-offs, and when to evolve from one to another.*

*五种多智能体协调模式、各自的权衡取舍，以及何时该从一种演进到另一种。*

![hero](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6903d22562f020146c9ec973_f8f4644253bde2f901550431b871b6dcf91e5d9d-1000x1000.svg)

In an earlier post, we explored when multi-agent systems provide value and when a single agent is the better choice.

在之前的一篇文章中，我们探讨了多智能体系统（multi-agent system）什么时候能带来价值、什么时候单智能体反而是更好的选择。

This post is for teams that have made that call and now need to decide which coordination pattern fits their problem.

本文写给已经做出这个决定、现在需要判断哪种协调模式（coordination pattern）适合自己问题的团队。

We've seen teams choose patterns based on what sounds sophisticated rather than what fits the problem at hand.

我们见过不少团队选模式的依据是「哪个听起来更高级」，而不是哪个真正匹配手头的问题。

We recommend starting with the simplest pattern that could work, watching where it struggles, and evolving from there.

我们的建议是：从可能行得通的最简单模式起步，观察它在哪里吃力，再从那里开始演进。

This post examines the mechanics and limitations of five patterns:

本文将考察以下五种模式的运行机制与局限：

- **Generator-verifier**, for quality-critical output with explicit evaluation criteria

- **生成器–验证器（Generator-verifier）**：适合输出质量关键、且评判标准可以写明确的场景

- **Orchestrator-subagent**, for clear task decomposition with bounded subtasks

- **编排者–子智能体（Orchestrator-subagent）**：适合任务分解清晰、子任务有明确边界的场景

- **Agent teams**, for parallel, independent, long-running subtasks

- **智能体团队（Agent teams）**：适合并行、独立、长时间运行的子任务

- **Message bus**, for event-driven pipelines with a growing agent ecosystem

- **消息总线（Message bus）**：适合事件驱动的流水线、且智能体生态在持续增长的场景

- **Shared-state**, for collaborative work where agents build on each other's findings

- **共享状态（Shared-state）**：适合智能体需要在彼此发现之上继续构建的协作式工作

## Pattern 1: Generator-verifier｜模式一：生成器–验证器

This is the simplest multi-agent pattern and among the most deployed.

这是最简单的多智能体模式，也是部署最广泛的模式之一。

We introduced it as the verification subagent pattern in our previous post, and here we use the broader generator-verifier framing because the generator need not be an orchestrator.

在上一篇文章中我们以「验证子智能体」（verification subagent）模式的名义介绍过它，这里改用更宽泛的「生成器–验证器」提法——因为生成方并不非得是一个编排者。

### How it works｜运行机制

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1c7_1b56c9bc.png)

A generator receives a task and produces an initial output, which it passes to a verifier for evaluation.

生成器接到任务后产出一版初始输出，并将其交给验证器评估。

The verifier checks whether the output meets the required criteria and either accepts it as complete or rejects it with feedback.

验证器检查输出是否满足要求的标准：要么接受它作为完成结果，要么连同反馈一起将其打回。

If rejected, that feedback is routed back to the generator, which uses it to produce a revised attempt.

如果被打回，这份反馈会回传给生成器，生成器据此产出一版修订稿。

This loop continues until the verifier accepts the output or the maximum number of iterations is reached.

这个循环会一直持续，直到验证器接受输出、或达到最大迭代次数为止。

### Where it works well｜适用场景

Consider a support system that generates email responses to customer tickets.

设想一个为客户工单自动生成邮件回复的客服系统。

The generator produces an initial response using product documentation and ticket context.

生成器基于产品文档和工单上下文写出初版回复。

The verifier checks accuracy against the knowledge base, evaluates tone against brand guidelines, and confirms the response addresses each issue raised.

验证器则对照知识库核查准确性、对照品牌规范评估语气，并确认回复回应了工单中提出的每一个问题。

Failed checks return to the generator with feedback that names the exact problem, such as a feature misattributed to the wrong pricing tier or a ticket issue left unanswered.

检查不通过时，会带着点名具体问题的反馈退回给生成器，比如「把某功能归到了错误的定价档位」或「工单里的某个问题没有回答」。

Use this pattern when output quality is critical and evaluation criteria can be made explicit.

当输出质量至关重要、且评判标准能够被明确写出来时，就该用这个模式。

It's effective for code generation (one agent writes code, another writes and runs tests), fact-checking, rubric-based grading, compliance verification, and any domain where an incorrect output costs more than an additional generation cycle.

它在这些场景中很有效：代码生成（一个智能体写代码，另一个写并运行测试）、事实核查、基于评分细则的打分（rubric-based grading）、合规校验，以及一切「一次错误输出的代价高于多跑一轮生成」的领域。

### Where it struggles｜局限

The verifier is only as good as its criteria.

验证器的水平上限就是它拿到的标准。

A verifier told only to check whether output is good, with no further criteria, will rubber-stamp the generator's output.

如果只告诉验证器「检查输出好不好」而不给任何进一步的标准，它就会给生成器的产出无脑盖章（rubber-stamp）。

Teams most often fail by implementing the loop without defining what verification means, which creates the illusion of quality control without the substance.

团队最常见的失败方式是：搭好了循环，却没有定义「验证」到底意味着什么——这制造了质量管控的假象，却没有实质。

(We discussed this early victory problem in the previous post.)

（我们在上一篇文章中讨论过这个「过早胜利」（early victory）问题。）

The pattern also assumes generation and verification are separable skills.

这个模式还默认「生成」和「验证」是两种可以分离的能力。

If evaluating a creative approach is as hard as generating one, the verifier may not reliably catch problems.

如果评估一个创造性方案和生成它一样难，验证器就未必能可靠地发现问题。

Finally, iterative loops can stall.

最后，迭代循环可能会陷入停滞。

If the generator can't address the verifier's feedback, the system oscillates without converging.

如果生成器始终无法回应验证器的反馈，系统就会来回震荡而不收敛。

A maximum iteration limit with a fallback strategy (escalate to a human, return the best attempt with caveats) prevents this from becoming an infinite loop.

设一个最大迭代上限并配上兜底策略（升级给人处理，或带着注意事项返回最佳尝试），就能防止它变成死循环。

## Pattern 2: Orchestrator-subagent｜模式二：编排者–子智能体

Hierarchy defines this pattern.

层级（hierarchy）是这个模式的定义性特征。

One agent acts as a team lead that plans work, delegates tasks, and synthesizes results.

一个智能体充当团队负责人（team lead）：规划工作、分派任务、汇总结果。

Subagents handle specific responsibilities and report back.

子智能体各自承担具体职责，完成后向上汇报。

### How it works｜运行机制

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1c4_76abfe32.png)

A lead agent receives a task and determines how to approach it.

主导智能体（lead agent）接到任务后决定如何处理。

It may handle some subtasks directly while dispatching others to subagents.

它可能自己直接处理一部分子任务，同时把其余的派发给子智能体。

Subagents complete their work and return results, which the orchestrator synthesizes into a final output.

子智能体完成工作后返回结果，由编排者（orchestrator）将其综合成最终输出。

[Claude Code](https://code.claude.com/docs/en/overview) uses this pattern.

[Claude Code](https://code.claude.com/docs/en/overview) 用的就是这个模式。

The main agent writes code, edits files, and runs commands itself, dispatching subagents in the background when it needs to search a large codebase or investigate independent questions so work continues while results stream back.

主智能体自己写代码、改文件、跑命令；当需要检索大型代码库或调查独立问题时，才在后台派出子智能体——这样主任务不中断，结果持续流式返回。

Each subagent operates in its own context window and returns distilled findings.

每个子智能体都在自己的上下文窗口（context window）里工作，只返回蒸馏后的结论。

This keeps the orchestrator's context focused on the primary task while exploration happens in parallel.

这让编排者的上下文始终聚焦于主任务，而探索工作在并行中完成。

### Where it works well｜适用场景

Consider an automated code review system.

设想一个自动化代码审查系统。

When a pull request arrives, the system needs to check for security vulnerabilities, verify test coverage, assess code style, and evaluate architectural consistency.

当一个 pull request 到达时，系统需要检查安全漏洞、验证测试覆盖率、评估代码风格、审查架构一致性。

Each check is distinct, requires different context, and produces a clear output.

每项检查各不相同、需要不同的上下文、并产出清晰的结果。

An orchestrator dispatches each check to a specialized subagent, collects the results, and synthesizes a unified review.

编排者把每项检查派给一个专精的子智能体，收集结果，再合成一份统一的评审。

Use this pattern when task decomposition is clear and subtasks have minimal interdependence.

当任务分解清晰、子任务之间几乎没有相互依赖时，就该用这个模式。

The orchestrator maintains a coherent view of the overall goal while subagents stay focused on specific responsibilities.

编排者保有对整体目标的连贯视野，子智能体则保持对具体职责的专注。

### Where it struggles｜局限

The orchestrator becomes an information bottleneck.

编排者会变成信息瓶颈（information bottleneck）。

When a subagent discovers something relevant to another subagent's work, that information has to travel back through the orchestrator.

当一个子智能体发现了与另一个子智能体工作相关的信息时，这条信息必须绕道编排者才能传递过去。

If the security subagent finds an authentication flaw that affects the architecture subagent's analysis, the orchestrator must recognize this dependency and route the information appropriately.

如果安全子智能体发现了一个会影响架构子智能体分析的认证缺陷，编排者就必须自己识别出这层依赖，并把信息正确转发。

After several such handoffs, critical details are often lost or summarized away.

经过几轮这样的转手之后，关键细节往往已经丢失，或在摘要中被抹平。

Sequential execution also limits throughput.

顺序执行也会限制吞吐量。

Unless explicitly parallelized, subagents run one after another, meaning the system incurs multi-agent token costs without the speed benefit.

除非显式并行化，子智能体是一个接一个跑的——这意味着系统付出了多智能体的 token 成本，却没有拿到速度上的收益。

## Pattern 3: Agent teams｜模式三：智能体团队

When work decomposes into parallel subtasks that can proceed independently for extended periods, orchestrator-subagent can become unnecessarily constraining.

当工作可以拆解成能够长时间独立推进的并行子任务时，编排者–子智能体模式反而可能成为不必要的束缚。

### How it works｜运行机制

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1cd_4282798b.png)

A coordinator spawns multiple worker agents as independent processes.

协调者（coordinator）以独立进程的形式启动多个工作智能体。

Teammates claim tasks from a shared queue, work on them autonomously across multiple steps, and signal completion.

队友（teammates）从共享队列中认领任务，跨多个步骤自主推进，完成后发出信号。

The difference from orchestrator-subagent is worker persistence.

它与编排者–子智能体模式的区别在于工作者的持久性（persistence）。

The orchestrator spawns a subagent for one bounded subtask, and the subagent terminates after returning a result.

编排者为一个有边界的子任务启动一个子智能体，子智能体返回结果后即终止。

Teammates stay alive across many assignments, accumulating context and domain specialization that improve their performance over time.

而队友会跨越多次任务分配持续存活，不断积累上下文和领域专精，其表现会随时间提升。

The coordinator assigns work and collects outcomes but doesn't reset workers between tasks.

协调者只负责分派工作、收集结果，任务之间不会重置工作者。

### Where it works well｜适用场景

Consider migrating a large codebase from one framework to another.

设想把一个大型代码库从一个框架迁移到另一个框架。

A teammate can migrate each service independently, with its own dependencies, test suite, and deployment configuration.

每个服务都有自己的依赖、测试套件和部署配置，一名队友可以独立完成对它的迁移。

A coordinator assigns each service to a teammate, and each teammate works through the migration autonomously: dependency updates, code changes, test fixes, validation.

协调者把每个服务分配给一名队友，每名队友自主推进迁移全程：更新依赖、修改代码、修复测试、做验证。

The coordinator collects completed migrations and runs integration tests across the full system.

协调者收集完成的迁移，并在整个系统上运行集成测试。

Use this pattern when subtasks are independent and benefit from sustained, multi-step work.

当子任务彼此独立、且能从持续的多步工作中获益时，就该用这个模式。

Each teammate builds up context about its domain rather than starting fresh with each dispatch.

每名队友会不断积累关于自己领域的上下文，而不是每次派发都从零开始。

### Where it struggles｜局限

Independence is the critical requirement.

独立性是这个模式的关键前提。

Unlike orchestrator-subagent, where the orchestrator can mediate between subagents and route information, teammates operate autonomously and can't easily share intermediate findings.

不同于编排者–子智能体模式中编排者可以在子智能体之间居中调解、转发信息，队友是自主运作的，很难共享中间发现。

If one teammate's work affects another's, neither is aware, and their outputs may conflict.

如果一名队友的工作影响到了另一名队友，双方都不会察觉，产出可能相互冲突。

Completion detection is also harder.

完成检测（completion detection）也更困难。

Since teammates work autonomously for variable durations, the coordinator must handle partial completion where one teammate finishes in two minutes and another takes twenty.

由于队友自主工作、耗时长短不一，协调者必须处理部分完成的情况——一名队友两分钟就做完了，另一名却要花二十分钟。

Shared resources compound both problems.

共享资源会让这两个问题雪上加霜。

When multiple teammates operate on the same codebase, database, or file system, two teammates may edit the same file or make incompatible changes.

当多名队友在同一个代码库、数据库或文件系统上操作时，两名队友可能编辑同一个文件，或做出互不兼容的改动。

The pattern requires careful task partitioning and conflict resolution mechanisms.

这个模式需要精心的任务划分和冲突解决机制。

## Pattern 4: Message bus｜模式四：消息总线

As agent count increases and interaction patterns grow complex, direct coordination becomes difficult to manage.

随着智能体数量增加、交互模式变复杂，直接协调会变得难以管理。

A message bus introduces a shared communication layer where agents publish and subscribe to events.

消息总线（message bus）引入一个共享通信层，智能体在其上发布（publish）和订阅（subscribe）事件。

### How it works｜运行机制

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1c1_78a53f59.png)

Agents interact through two primitives: publish and subscribe.

智能体通过两个原语（primitive）交互：发布与订阅。

Agents subscribe to the topics they care about, and a router delivers matching messages.

智能体订阅自己关心的主题（topic），由路由器（router）投递匹配的消息。

New agents with new capabilities can start receiving relevant work without rewiring existing connections.

具备新能力的新智能体可以直接开始接收相关工作，而无需重新改动既有的连接。

### Where it works well｜适用场景

A security operations automation system demonstrates where this pattern excels.

一个安全运营（security operations）自动化系统能很好地展示这个模式的长处。

Alerts arrive from multiple sources, and a triage agent classifies each by severity and type, routing high-severity network alerts to a network investigation agent and credential-related alerts to an identity analysis agent.

告警从多个来源涌入，一个分诊（triage）智能体按严重程度和类型对每条告警分类：高危网络告警路由给网络调查智能体，凭证相关告警路由给身份分析智能体。

Each investigation agent may publish enrichment requests that a context-gathering agent fulfills.

每个调查智能体都可以发布信息补全（enrichment）请求，由一个上下文收集智能体来满足。

Findings flow to a response coordination agent that determines the appropriate action.

调查结论流向一个响应协调智能体，由它决定合适的处置动作。

This pipeline suits the message bus because events flow from one stage to the next, teams can add new agent types as threat categories evolve, and teams can develop and deploy agents independently.

这条流水线之所以适合消息总线，是因为：事件从一个阶段流向下一个阶段；随着威胁类别演化，团队可以新增智能体类型；而且各团队可以独立开发和部署智能体。

Use this pattern for event-driven pipelines where the workflow emerges from events rather than a predetermined sequence, and where the agent ecosystem is likely to grow.

当工作流是由事件涌现而来、而非预先确定的顺序，且智能体生态很可能持续增长时，就该用这个模式来构建事件驱动的流水线。

### Where it struggles｜局限

The flexibility of event-driven communication makes tracing harder.

事件驱动通信的灵活性让追踪（tracing）变得更难。

When an alert triggers a cascade of events across five agents, understanding what happened requires careful logging and correlation.

当一条告警在五个智能体之间触发一连串级联事件时，想弄清发生了什么，需要细致的日志记录和关联分析。

Debugging is harder than following an orchestrator's sequential decisions.

调试的难度高于跟随编排者的顺序决策。

Routing accuracy is also critical.

路由准确性也至关重要。

If the router misclassifies or drops an event, the system fails silently, handling nothing but never crashing.

如果路由器把事件分错类或直接弄丢，系统就会静默失败（fail silently）——什么都没处理，却也从不崩溃。

LLM-based routers provide semantic flexibility but introduce their own failure modes.

基于大语言模型（LLM）的路由器提供了语义上的灵活性，但也引入了它们自己的失败模式。

## Pattern 5: Shared state｜模式五：共享状态

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1ca_d18482f0.png)

Orchestrators, team leads, and message routers in the previous patterns all centrally manage information flow.

前面几种模式中的编排者、团队负责人和消息路由器，都是在集中式地管理信息流。

Shared state removes the intermediary by letting agents coordinate through a persistent store that all can read and write directly.

共享状态（shared state）去掉了这个中间人：让所有智能体通过一个都能直接读写的持久化存储来协调。

### How it works｜运行机制

Agents operate autonomously, reading from and writing to a shared database, file system, or document.

智能体自主运作，对一个共享的数据库、文件系统或文档进行读写。

There's no central coordinator.

没有中心协调者。

Agents check the store for relevant information, act on what they find, and write their findings back.

智能体到存储中查看相关信息，基于所见采取行动，再把自己的发现写回去。

Work typically begins when an initialization step seeds the store with a question or dataset, and ends when a termination condition is met: a time limit, a convergence threshold, or a designated agent determining the store contains a sufficient answer.

工作通常始于一个初始化步骤——向存储中播下一个问题或数据集；终于某个终止条件被满足——时间上限、收敛阈值，或由一个指定的智能体判定存储中已包含足够充分的答案。

### Where it works well｜适用场景

Consider a research synthesis system where multiple agents investigate different aspects of a complex question.

设想一个研究综合（research synthesis）系统：多个智能体各自调查一个复杂问题的不同侧面。

One explores academic literature, another analyzes industry reports, a third examines patent filings, a fourth monitors news coverage.

一个挖学术文献，一个分析行业报告，第三个查专利申请，第四个盯新闻报道。

Each agent's findings may inform the others' investigations.

每个智能体的发现都可能为其他智能体的调查提供线索。

The academic literature agent might discover a key researcher whose company the industry agent should examine more closely.

比如学术文献智能体可能发现一位关键研究者，而这位研究者的公司正值得行业智能体深挖。

With shared state, findings go directly into the store.

在共享状态模式下，发现会直接进入存储。

The industry agent can see the academic agent's discoveries immediately, without waiting for a coordinator to route the information.

行业智能体可以立刻看到学术智能体的发现，无需等待协调者转发信息。

Agents build on each other's work, and the shared store becomes an evolving knowledge base.

智能体在彼此的工作之上继续构建，共享存储演化成一个不断生长的知识库。

Shared state also removes the coordinator as a single point of failure.

共享状态还消除了协调者这个单点故障（single point of failure）。

If any one agent stops, the others continue reading and writing.

任何一个智能体停摆，其余的仍能继续读写。

In orchestrator and message-bus systems, a coordinator or router failure halts everything.

而在编排者和消息总线系统中，协调者或路由器一旦故障，一切都会停摆。

### Where it struggles｜局限

Without explicit coordination, agents may duplicate work or pursue contradictory approaches.

缺少显式协调时，智能体可能重复劳动，或采取相互矛盾的路线。

Two agents might independently investigate the same lead.

两个智能体可能各自独立地调查同一条线索。

Agent interactions produce system behavior rather than top-down design, which makes outcomes less predictable.

系统行为是由智能体交互涌现出来的，而非自上而下设计出来的，这让结果更难预测。

The harder failure mode is reactive loops.

更棘手的失败模式是反应式循环（reactive loop）。

For example, Agent A writes a finding, Agent B reads it and writes a follow-up, Agent A sees the follow-up and responds.

例如：智能体 A 写下一个发现，智能体 B 读到后写了一条跟进，智能体 A 又看到这条跟进并作出回应。

The system keeps burning tokens on work that isn't converging.

系统就这样在不收敛的工作上持续烧 token。

Duplicate work and concurrent writes have known engineering fixes (locking, versioning, partitioning).

重复劳动和并发写入有成熟的工程解法（加锁、版本控制、分区）。

Reactive loops are a behavioral problem and need first-class termination conditions: a time budget, a convergence threshold (no new findings for N cycles), or a designated agent whose job is to decide when the store contains a sufficient answer.

而反应式循环是一个行为层面的问题，需要把终止条件当作一等公民来设计：时间预算、收敛阈值（连续 N 个周期没有新发现），或者一个专职智能体，其职责就是判定存储中何时已包含足够充分的答案。

Systems that treat termination as an afterthought tend to cycle indefinitely or stop arbitrarily when one agent's context fills.

把终止当作事后补丁的系统，往往会无限循环下去，或在某个智能体的上下文被填满时随意停止。

## Choosing and evolving between patterns｜模式的选择与演进

The right pattern depends on a handful of structural questions about the system.

选对模式，取决于关于系统的几个结构性问题。

In our previous post, we argued for context-centric decomposition, which divides work by what context each agent needs rather than by what type of work it does.

在上一篇文章中，我们主张以上下文为中心的分解（context-centric decomposition）：按每个智能体需要什么上下文来划分工作，而不是按它做什么类型的工作。

That principle applies here too.

这个原则在这里同样适用。

The patterns differ in how they manage context boundaries and information flow.

这些模式的差异，正在于它们如何管理上下文边界与信息流。

### Orchestrator-subagent vs. agent teams｜编排者–子智能体 vs. 智能体团队

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1d0_cb379a56.png)

Both involve a coordinator dispatching work to other agents.

两者都是由一个协调者向其他智能体派发工作。

The question is how long workers need to maintain their context.

关键问题是：工作者需要把上下文维持多久。

- **Choose orchestrator-subagent** when subtasks are short, focused, and produce clear outputs. The code review system works well here because each check runs its analysis, generates a report, and returns within a single bounded invocation. The subagent doesn't need to carry context across multiple cycles.

- **选编排者–子智能体**：当子任务短小、聚焦、产出清晰时。代码审查系统在这里就很合适——每项检查在一次有边界的调用内完成分析、生成报告、返回结果，子智能体不需要跨多个周期携带上下文。

- **Choose agent teams** when subtasks benefit from sustained, multi-step work. The codebase migration fits here because each teammate develops real familiarity with its assigned service: the dependency graph, test patterns, deployment configuration. That accumulated context improves performance in ways one-shot dispatch can't replicate.

- **选智能体团队**：当子任务能从持续的多步工作中获益时。代码库迁移就属于这种情况——每名队友会对自己负责的服务建立起真正的熟悉度：依赖图谱、测试模式、部署配置。这种积累起来的上下文带来的性能提升，是一次性派发无法复制的。

When subagents need to retain state across invocations, agent teams are the better fit.

当子智能体需要跨调用保留状态时，智能体团队是更好的选择。

### Orchestrator-subagent vs. message bus｜编排者–子智能体 vs. 消息总线

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1dc_4313c333.png)

Both can handle multi-step workflows.

两者都能处理多步骤的工作流。

The question is how predictable the workflow structure is.

关键问题是：工作流的结构有多可预测。

- **Choose orchestrator-subagent** when the sequence of steps is known in advance. The code review system follows a fixed pipeline: receive a PR, run checks, synthesize results.

- **选编排者–子智能体**：当步骤顺序事先已知时。代码审查系统走的就是固定流水线：接收 PR、跑检查、合成结果。

- **Choose message bus** when the workflow emerges from events and may vary based on what's discovered. The security operations system can't predict what alerts will arrive or what investigation paths they'll require. New alert types may emerge that need new handling. The message bus accommodates that variability by routing events to capable agents rather than following a predetermined sequence.

- **选消息总线**：当工作流由事件涌现、且可能随所发现的情况而变化时。安全运营系统无法预测会来什么告警、需要走什么调查路径；还可能出现需要新处置方式的新告警类型。消息总线通过把事件路由给有相应能力的智能体、而非遵循预定顺序，来容纳这种多变性。

As conditional logic accumulates in the orchestrator to handle an expanding variety of cases, the message bus makes that routing explicit and extensible.

当编排者里为了应付越来越多的情况而不断堆积条件逻辑时，消息总线能把这种路由变得显式且可扩展。

### Agent teams vs. shared state｜智能体团队 vs. 共享状态

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1df_a8950920.png)

Both involve agents working autonomously.

两者都是智能体自主工作。

The question is whether agents need each other's findings.

关键问题是：智能体之间是否需要彼此的发现。

- **Choose agent teams** when agents work on separate partitions that don't interact. The codebase migration fits here because each teammate handles its service and the coordinator combines results at the end.

- **选智能体团队**：当智能体在互不交叉的独立分区上工作时。代码库迁移就属于这种情况——每名队友各管自己的服务，协调者在最后合并结果。

- **Choose shared state** when agents' work is collaborative and findings should flow between them in real time. The research synthesis system is a better match because the academic agent's discovery of a key researcher immediately becomes relevant to the industry agent's investigation.

- **选共享状态**：当智能体的工作是协作性质、发现需要在彼此之间实时流动时。研究综合系统就更匹配这种模式——学术智能体发现的一位关键研究者，会立刻与行业智能体的调查产生关联。

Once teammates need to communicate with each other rather than only share final results, shared state makes that more natural.

一旦队友之间需要相互沟通、而不只是共享最终结果，共享状态就能让这件事更自然。

### Message bus vs. shared state｜消息总线 vs. 共享状态

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1d4_46c9b982.png)

Both support complex multi-agent coordination.

两者都支持复杂的多智能体协调。

The question is whether work flows as discrete events or accumulates into a shared knowledge base.

关键问题是：工作是以离散事件的形式流动，还是不断累积成一个共享知识库。

- **Choose message bus** when agents react to events in a pipeline. The security operations system processes alerts stage by stage, with each event triggering the next before completing. The pattern is efficient at routing events to capable agents.

- **选消息总线**：当智能体在流水线中对事件作出反应时。安全运营系统逐阶段处理告警，每个事件在完成前触发下一个。这个模式在把事件路由给有相应能力的智能体这件事上很高效。

- **Choose shared state** when agents build on accumulated findings over time. The research synthesis system gathers knowledge continuously. Agents return to the store repeatedly, seeing what others have discovered and adjusting their investigations.

- **选共享状态**：当智能体需要在随时间累积的发现之上继续构建时。研究综合系统在持续地收集知识；智能体反复回到存储，查看其他人发现了什么，并调整自己的调查方向。

The message bus still has a router, which means a central component decides where events go.

消息总线仍然有一个路由器，这意味着由一个中心组件决定事件的去向。

Shared state is decentralized.

共享状态则是去中心化的。

If eliminating single points of failure is a priority, shared state provides that more completely.

如果消除单点故障是优先事项，共享状态能更彻底地做到这一点。

If agents in a message bus system are publishing events to share findings rather than trigger actions, shared state is a better fit.

如果消息总线系统中的智能体发布事件是为了共享发现、而不是触发动作，那么共享状态是更合适的选择。

## Getting started｜起步建议

Production systems often combine patterns.

生产系统常常是多种模式的组合。

A common hybrid uses orchestrator-subagent for the overall workflow with shared state for a collaboration-heavy subtask.

一种常见的混合方案：整体工作流用编排者–子智能体，协作密集的子任务用共享状态。

Another uses message bus for event routing with agent team-style workers handling each event type.

另一种是：事件路由用消息总线，每类事件由智能体团队式的工作者来处理。

These patterns are building blocks, not mutually exclusive choices.

这些模式是积木（building blocks），不是互斥的单选题。

The following table summarizes when each pattern is appropriate.

下表总结了每种模式各自适用的情形。

| Situation | Pattern |
|---|---|
| Quality-critical output, explicit evaluation criteria | Generator-Verifier |
| Clear task decomposition, bounded subtasks | Orchestrator-Subagent |
| Parallel workload, independent long-running subtasks | Agent Teams |
| Event-driven pipeline, growing agent ecosystem | Message Bus |
| Collaborative research, agents share discoveries | Shared State |
| No single point of failure required | Shared State |

| 情形               | 模式                              |
| ---------------- | ------------------------------- |
| 输出质量关键、评判标准明确    | 生成器–验证器（Generator-Verifier）     |
| 任务分解清晰、子任务有边界    | 编排者–子智能体（Orchestrator-Subagent） |
| 并行工作负载、独立的长时子任务  | 智能体团队（Agent Teams）              |
| 事件驱动流水线、智能体生态在增长 | 消息总线（Message Bus）               |
| 协作式研究、智能体共享发现    | 共享状态（Shared State）              |
| 要求无单点故障          | 共享状态（Shared State）              |

For most use cases, we recommend starting with orchestrator-subagent.

对于大多数用例，我们建议从编排者–子智能体起步。

It handles the widest range of problems with the least coordination overhead.

它能以最少的协调开销，应对最广范围的问题。

Observe where it struggles, then evolve toward other patterns as specific needs become clear.

观察它在哪里吃力，等具体需求变得清晰后，再向其他模式演进。

*In upcoming posts, we will examine each pattern in depth with production implementations and case studies.*

*在接下来的文章中，我们将结合生产环境实现和案例研究，对每种模式逐一深入剖析。*

*For background on when multi-agent systems are worth the investment, see* [*Building multi-agent systems: when and how to use them*](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)*.*

*关于多智能体系统何时值得投入的背景知识，参见[《构建多智能体系统：何时用以及如何用》](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)。*

## Acknowledgements｜致谢

Written by Cara Phillips, with contributions from Eugene Yan, Jiri De Jonghe, Samuel Weller, and Erik S.

本文由 Cara Phillips 撰写，Eugene Yan、Jiri De Jonghe、Samuel Weller 和 Erik S. 亦有贡献。


---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| coordination pattern | 协调模式 | 全文主题：多智能体之间信息流动的组织方式 |
| generator-verifier | 生成器–验证器 | 产出与评判分离，反馈闭环 |
| verification subagent | 验证子智能体 | 上一篇文章中 generator-verifier 的旧称 |
| rubber-stamp | 无脑盖章 | 验证器缺乏明确标准时的失效表现 |
| rubric-based grading | 按评分细则打分 | generator-verifier 的典型应用 |
| orchestrator-subagent | 编排者–子智能体 | 层级式派发，子智能体用完即弃，官方推荐起点 |
| information bottleneck | 信息瓶颈 | 编排者模式的核心弱点：横向信息必须绕道中心 |
| distilled findings | 蒸馏后的结论 | 子智能体返回给编排者的压缩产出 |
| agent teams | 智能体团队 | 常驻工人 + 共享任务队列 |
| worker persistence | 工人常驻 | agent teams 与 orchestrator-subagent 的本质差别 |
| completion detection | 完成检测 | agent teams 的难点：如何判断全部完成 |
| task partitioning | 任务分区 | agent teams 避免资源冲突的前提 |
| message bus | 消息总线 | publish/subscribe + 中心路由 |
| publish / subscribe | 发布 / 订阅 | 消息总线仅有的两个交互原语 |
| enrichment request | 补充信息请求 | 安全运营案例中调查 Agent 发布的事件类型 |
| fail silently | 静默失败 | 路由器误分类/丢事件时的失效表现 |
| shared state | 共享状态 | 去中心化，通过持久化存储直接协调 |
| reactive loop | 反应式循环 | 共享状态最贵的失败模式：不收敛地互相触发 |
| termination condition | 终止条件 | 反应式循环的解法：时间预算/收敛阈值/专职判停 Agent |
| convergence threshold | 收敛阈值 | 终止条件之一：连续 N 周期无新发现即停 |
| single point of failure | 单点故障 | 共享状态相对其他模式的结构性优势 |
| context-centric decomposition | 以上下文为中心的分解 | 按所需上下文而非工作类型拆分任务 |
| building blocks | 积木/构件 | 模式可组合，非互斥选项 |
