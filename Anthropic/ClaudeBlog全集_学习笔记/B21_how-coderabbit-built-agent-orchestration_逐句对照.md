# B21_How CodeRabbit used Claude to build an agent orchestration system_CodeRabbit 如何用 Claude 构建 Agent 编排系统

> 原文：https://claude.com/blog/how-coderabbit-used-claude-to-build-an-agent-orchestration-system
> 来源：Anthropic Claude Blog（分类：客户案例 / How startups build with Claude ｜ 产品：Claude Platform + Claude Code）｜发布日期：2026-05-27
> 原文存档：[Markdown](原文/B21_how-coderabbit-used-claude-to-build-an-agent-orchestration-system_原文.md)

## 📌 本篇速览

- 📅 2026-05-27　｜　⏱ 原文约 1210 词（逐句精读约 16 分钟）
- 🏷 规划先行编排、隐式假设、PRD 即工件、模型分层路由、计划质量评测、质量闸门
- 🗂 [返回目录](00_目录与阅读进度.md)

最接近「工程化多模型编排」的客户案例（CodeRabbit：每周评审 200 万 PR、1.5 万+ 客户）。**问题诊断**：AI 代码最常见失败不是编译不过，而是「编译通过、测试通过、但不是团队想要的东西」——根因在模型上游：资深开发者把内化知识当共识，没写下来，Agent 用「看起来合理」的猜测填空（生动案例：做了用户系统却没有登录页，因为「用户要能登录」从没被说出口）。**方案**：在代码生成之前插入一个规划编排层——多个 Claude 协同分析需求、暴露假设，产出**协作式 PRD 作为共享工件与质量闸门**；论点：「代码生成越便宜，走错方向就越贵」。**模型路由三层**：Opus 管编排循环与战略方向，Sonnet 把输出串成结构化规划步骤，Haiku 做窄任务（上下文蒸馏、定向工具调用）——升降级决策不靠猜，靠评测（「Haiku 做得和 Sonnet 一样好就用 Haiku」）。**计划质量评测**：LLM judge 库按维度打分 + 下游代码可运行性/多余 scope/token 消耗回归度量 + 有无规划的对照实验；发现**计划的抽象层级本身要调**——太细则代码库一动就过期，太粗则回到填空问题。

---

*In our series, **How startups build with Claude**, we highlight how startups are transforming their industries with AI.*

*在我们的「初创公司如何用 Claude 构建」系列里，我们介绍初创公司如何用 AI 变革自己所在的行业。*

*In this article, we share how CodeRabbit built an agent orchestration layer that plans before AI generates code.*

*本文分享 CodeRabbit 如何构建一个「先规划、再让 AI 写代码」的智能体编排层。*

| 速览 | |
|---|---|
| 名称 | CodeRabbit |
| 成立 | 2023 |
| 创始人 | Harjot Gill（CEO） |
| 技术栈 | Claude Platform、Claude Code |
| 规模 | 每周评审 200 万个 PR，客户 15,000+ |

AI coding tools have collapsed the time between idea and working prototype.

AI 编程工具把「想法」到「能跑的原型」之间的时间压缩到了极短。

CodeRabbit, an AI code review platform, has noticed a different trend climbing alongside that throughput: code that compiles and passes tests but doesn't do what the team actually meant to build.

AI 代码评审平台 CodeRabbit 注意到，随着吞吐量上升，另一条曲线也在攀升：**能编译、能过测试，却不是团队真正想构建的东西**的代码。

David Loker, VP of AI at CodeRabbit, locates the cause upstream of the model.

CodeRabbit 的 AI 副总裁 David Loker 把原因定位在模型的上游。

Experienced developers often assume coding agents understand the same context they do, so they don't write down requirements that feel obvious to them.

资深开发者常常假设编程智能体理解和他们相同的上下文，于是那些「显而易见」的需求他们根本不写。

The coding agent then fills the gaps with whatever it considers plausible.

编程智能体就用它认为合理的东西去填这些空。

To close that gap, CodeRabbit used Claude to design and build an agent orchestration system that runs a structured planning phase before any code is generated.

为了补上这个缺口，CodeRabbit 用 Claude 设计并构建了一套智能体编排系统，在生成任何代码之前先跑一个结构化的规划阶段。

The team's working thesis is that planning quality determines output quality, and the cheaper code generation gets, the more expensive it becomes to move in the wrong direction.

团队的工作假设是：**规划质量决定产出质量；代码生成越便宜，朝错误方向前进就越昂贵。**

## Addressing the internal knowledge gap in AI coding

## 解决 AI 编程中的内隐知识缺口

When the CodeRabbit team studied AI-generated pull requests across their customer base, the most frequent failure mode was code that compiled and passed tests, yet still didn't solve the problem it was built to solve.

CodeRabbit 团队研究了客户群中 AI 生成的 PR，发现最高频的失败模式是：代码能编译、能过测试，却仍然没有解决它本来要解决的问题。

"As we gain experience as developers, we internalize knowledge," Loker says.

「随着开发经验增长，我们会把知识内化，」Loker 说。

"All those things are in our head, and we assume other developers know them too. But then we make that assumption of the AI system as well, that it also implicitly understands. We're not even aware that we're assuming those things."

「这些东西都在我们脑子里，我们假设其他开发者也知道。然后我们对 AI 系统也做了同样的假设——以为它也隐式地理解。我们甚至意识不到自己在做这些假设。」

Vague prompts force the underlying system to fill gaps with whatever it considers plausible.

模糊的提示词迫使底层系统用它认为合理的东西填空。

That guess often diverges from what the developer had in mind.

而这个猜测常常偏离开发者心里想的。

Loker offers a personal example.

Loker 给了一个亲身例子。

While building a memory system on a side project, he spent hours iterating with a coding agent until everything ran.

在一个业余项目里做记忆系统时，他和编程智能体迭代了好几个小时，直到一切都能跑。

When he asked the agent how to use it, the instructions told him to pass in a user token.

当他问智能体怎么使用时，说明让他传入一个用户 token。

There was no login page.

可根本没有登录页。

He had specified that the system required users but never said users needed a way to sign in.

他说明了系统需要用户，却从没说过用户需要一种登录方式。

The agent filled the gap, and hours of work landed in a product missing a front door.

智能体填掉了这个空，几小时的工作最后落在一个**没有前门**的产品上。

"What ends up happening is you build a lot more stuff on top of it, then much later you find there's a problem," Loker says.

「实际发生的是：你在它上面又盖了很多东西，很久之后才发现有问题，」Loker 说。

"In AI workflows, late validation can be very expensive."

「在 AI 工作流里，晚验证可能非常昂贵。」

## An orchestration layer that runs before AI coding solutions

## 跑在 AI 编码之前的编排层

CodeRabbit's response was to insert a planning system in front of code generation.

CodeRabbit 的应对，是在代码生成前面插入一个规划系统。

It coordinates multiple Claude models to analyze requirements and surface assumptions before producing a structured execution plan that defines what should be built and what constraints it needs to satisfy.

它协调多个 Claude 模型分析需求、把假设暴露出来，然后产出一份结构化执行计划——定义该构建什么、需要满足什么约束。

"This planning system is not meant to replace Claude Code's Plan Mode," Loker says.

「这个规划系统不是要取代 Claude Code 的 Plan Mode，」Loker 说。

"It's a higher level orchestration that happens before Claude Code, to point it in a really narrow and right direction where everything that needs to be explicit is made explicit, and we are aware of all assumptions that are being made."

「它是发生在 Claude Code 之前的更高层编排，把 Claude Code 指向一个非常窄、且正确的方向——所有需要显式化的东西都被显式化，所有正在做的假设我们都心里有数。」

The output is a collaborative product requirements document (PRD): a plan created with full context, validated by stakeholders across the team, and reviewed before implementation starts.

产出是一份协作式产品需求文档（PRD）：在完整上下文下创建、由团队各方干系人验证、在实现开始前评审过的计划。

Claude Code picks up that plan and uses it to generate a fine-grained implementation plan.

Claude Code 接过这份计划，用它生成细粒度的实现计划。

The plan becomes a shared artifact that captures what was decided and why, which not only helps teams avoid rework and validate later that the output matched the original intent, but also onboard new engineers.

这份计划成为一个共享工件，记录「决定了什么、为什么」——不仅帮团队避免返工、事后验证产出是否符合最初意图，还能用来让新工程师快速上手。

## Routing across the Claude model family

## 在 Claude 模型家族间路由

CodeRabbit matches each model tier to task complexity to optimize for cost and latency.

CodeRabbit 按任务复杂度匹配模型层级，优化成本和延迟。

Opus drives the orchestration loop and the higher-level strategic work of understanding the problem and setting overall direction.

Opus 驱动编排循环，以及理解问题、设定总体方向这类更高层的战略工作。

Sonnet takes that output and sequences it into structured planning steps.

Sonnet 接过这些输出，把它编排成结构化的规划步骤。

Haiku handles narrowly scoped operations like context distillation and targeted tool use, where the question is specific enough that a smaller model can answer it well.

Haiku 处理范围很窄的操作，比如上下文蒸馏和定向工具调用——问题足够具体，小模型就能答好。

"If Haiku does as well as Sonnet on a given task, we use Haiku," Loker says.

「如果某个任务上 Haiku 做得和 Sonnet 一样好，我们就用 Haiku，」Loker 说。

"If the evaluation harness tells us the plan quality improves when we give Opus more room, we give it more room. We don't guess."

「如果评测系统告诉我们，给 Opus 更多空间计划质量会提升，我们就给它更多空间。**我们不靠猜。**」

## Building an eval harness for plan quality

## 为计划质量搭建评测系统

CodeRabbit had a mature evaluation system for code review, but nothing for evaluating planning output.

CodeRabbit 有一套成熟的代码评审评测系统，但没有任何评估规划产出的手段。

Building that infrastructure became its own project.

搭建这套基础设施本身就成了一个项目。

The system started with hand-tuned examples and manual inspection.

这套系统从手工调校的示例和人工检查起步。

The team developed a library of LLM judges that scored specific dimensions of plan quality.

团队开发了一个 LLM 评审器（judge）库，对计划质量的特定维度打分。

Because plans eventually produce code, the team could also measure whether the generated code worked, whether it contained extra scope, and how many tokens it took to get there.

因为计划最终会产出代码，团队还能度量：生成的代码是否能用、是否夹带多余范围（scope）、以及花了多少 token 才走到那一步。

Running the same task with and without the planning step gave them a way to isolate the value of planning itself.

同一个任务带规划和不带规划各跑一遍，让他们得以隔离出规划本身的价值。

"We didn't realize what the right level of detail was going to be for that plan," Loker says.

「我们一开始并不知道计划的正确详细程度应该是多少，」Loker 说。

Plans that were too granular went stale the moment the codebase shifted.

太细的计划，代码库一变就过期。

Plans that were too high-level left room for the agent to fill in assumptions, which was the original problem the planning layer was meant to solve.

太粗的计划，又给智能体留下了填假设的空间——而这正是规划层原本要解决的问题。

Finding the working level of abstraction took iteration, which is what the eval harness made possible.

找到可用的抽象层级需要迭代，而评测系统正是让这种迭代成为可能的东西。

## Catching errors before any code gets written

## 在写下任何代码之前抓住错误

In an AI-native coding workflow, many of the decisions that used to surface during code review are now made earlier, in the planning layer.

在 AI 原生的编码工作流里，许多过去在代码评审阶段才浮现的决策，现在提前到了规划层。

Building a plan that the team can review and align on before code generation starts catches mistakes early.

在代码生成开始前，构建一份团队能评审并对齐的计划，可以尽早抓住错误。

"What we've built, using the Claude ecosystem, is a team-wide planning system," Loker says.

「我们用 Claude 生态构建的，是一套团队级的规划系统，」Loker 说。

"The plan itself becomes a quality gate. If we can make sure the quality of that plan is really good upfront, the downstream effect is very pronounced. You end up with a lot better code at the end of it."

「计划本身成为一道质量闸门。如果我们能在前端确保计划质量足够好，下游效应会非常显著——最后你会得到好得多的代码。」

| CodeRabbit 团队的最佳实践 | |
|---|---|
| 你真正想创造的结果是什么、怎么度量？ | 不只对 AI 把规格说明写显式，也要在 MPP（maximum possible product，最大可能产品）里定义你想要什么。 |
| 哪些假设仍是隐式的？ | 问 Claude：缺了什么？计划里有没有哪些部分是以隐式假设而非显式规格的形式存在的？ |
| 哪些工作流或边界情况容易被忘掉？ | 让 Claude 帮忙找出你可能没考虑到的场景。 |
| 上线前怎么知道产出符合意图？ | 建立工作记录：一份被保存、被复用的规划工件编年史。 |

---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| agent orchestration layer | 智能体编排层 | 跑在代码生成之前的规划系统 |
| implicit assumptions | 隐式假设 | 失败根因：内化知识没写下来，Agent 填空 |
| late validation | 晚验证 | 「AI 工作流里晚验证非常昂贵」 |
| collaborative PRD | 协作式产品需求文档 | 规划层的产出物 = 共享工件 = 质量闸门 |
| quality gate | 质量闸门 | 计划本身的新角色 |
| model routing | 模型路由 | Opus 战略 / Sonnet 结构化 / Haiku 窄任务 |
| context distillation | 上下文蒸馏 | Haiku 承担的典型窄任务 |
| eval harness | 评测系统 | 升降级决策的依据（「我们不靠猜」） |
| LLM judges | LLM 评审器 | 按维度给计划质量打分 |
| extra scope | 多余范围 | 下游度量之一：代码有没有夹带私货 |
| level of abstraction | 抽象层级 | 计划太细会过期、太粗会填空——要调 |
| MPP (maximum possible product) | 最大可能产品 | CodeRabbit 自造术语：显式定义想要什么 |
