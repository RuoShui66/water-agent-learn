# 01_New in Claude Managed Agents: dreaming, outcomes, and multiagent orchestration_Claude 托管智能体新能力：Dreaming、Outcomes 与多智能体编排

> 原文：https://claude.com/blog/new-in-claude-managed-agents
> 来源：Claude 产品博客（Product announcements）｜发布日期：2026-05-19

## 📌 本篇速览

- 📅 2026-05-19　｜　⏱ 官方标注约 5 分钟
- ⭐ ★★★★★ **必读** —— 这是 2026-03-24 harness 设计文里「手搓评估器」正式变成产品的那一刻，也是理解「哪些 harness 组件该外包给平台」的最直接材料。
- 🏷 Outcomes、Dreaming、multiagent orchestration、rubric grader、webhooks
- 🗂 [返回专题目录](00_目录.md)

Anthropic 在本文发布了 Claude Managed Agents 的一批新能力：Dreaming（research preview）是一个定时进程，回顾历史会话与记忆库、提取重复模式并整理记忆，让智能体跨会话自我改进；Outcomes（public beta）让开发者写一份质量评分标准，由独立上下文窗口中的打分器评判产出并指出改进点，内部基准显示任务成功率最多提升 10 个百分点；multiagent orchestration（public beta）让 lead agent 把复杂任务拆块，委派给各带独立模型、提示词和工具的 specialist 子智能体在共享文件系统上并行工作，全程可在 Claude Console 追溯；webhooks 则在任务完成时发通知。文末给出 Harvey（完成率提升约 6 倍）、Netflix、Spiral by Every、Wisedocs（评审提速 50%）四个客户案例。

---

Today we're launching dreaming in [Claude Managed Agents](https://claude.com/blog/claude-managed-agents) as a research preview.

今天，我们以研究预览版（research preview）的形式在 [Claude Managed Agents](https://claude.com/blog/claude-managed-agents) 中推出 dreaming 功能。

Dreaming extends [memory](https://claude.com/blog/claude-managed-agents-memory) by reviewing past sessions to find patterns and help agents self-improve.

Dreaming 是对[记忆](https://claude.com/blog/claude-managed-agents-memory)（memory）功能的扩展：它回顾历史会话、从中发现模式，帮助智能体自我改进。

We're also making outcomes, multiagent orchestration, and webhooks available to developers building with Managed Agents.

我们同时向使用 Managed Agents 构建应用的开发者开放了 outcomes、多智能体编排（multiagent orchestration）和 webhooks。

Together, these updates make agents more capable at handling complex tasks with minimal steering.

这些更新合在一起，让智能体只需极少的人工引导就能更好地处理复杂任务。

## **Build self-improving agents with dreaming**|**用 dreaming 打造自我改进的智能体**

[Dreaming](https://platform.claude.com/docs/en/managed-agents/dreams) is a scheduled process in Claude Managed Agents that reviews agent sessions and memory stores, extracts patterns, and curates memories so agents improve over time.

[Dreaming](https://platform.claude.com/docs/en/managed-agents/dreams) 是 Claude Managed Agents 中的一个定时进程（scheduled process）：它回顾智能体的会话和记忆库、提取其中的模式、并整理（curate）记忆，让智能体随着时间不断进步。

You decide how much control you want: dreaming can update memory automatically, or you can review changes before they land.

控制权的粒度由你决定：dreaming 可以自动更新记忆，你也可以在变更落地之前先行审核。

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69f8e9ad765c7eed52dcf468_Claude-Managed-Agents-Blog-Followup-Dreaming.png)

Dreaming surfaces patterns that a single agent can’t see on its own, including recurring mistakes, workflows that agents converge on, and preferences shared across a team.

Dreaming 能浮现出单个智能体靠自己看不见的模式，包括反复出现的错误、多个智能体不约而同收敛出的工作流，以及整个团队共享的偏好。

It also restructures memory so it stays high-signal as it evolves.

它还会重构记忆，让记忆在不断演化的过程中始终保持高信噪比。

This is especially useful for long-running work and multiagent orchestration.

这对长时程工作和多智能体编排尤其有用。

Together, memory and dreaming form a robust memory system for self-improving agents.

记忆与 dreaming 合在一起，构成了一套支撑智能体自我改进的健壮记忆系统。

Memory lets each agent capture what it learns *as it works*.

记忆让每个智能体在*工作过程中*随时记下学到的东西。

Dreaming refines that memory *between sessions*, pulling shared learnings across agents and keeping it up-to-date.

Dreaming 则在*会话之间*提炼这些记忆，汇集跨智能体的共同经验，并保持记忆的时效性。

Dreaming is available in Managed Agents on the Claude Platform; developers can [request access here](https://claude.com/form/claude-managed-agents).

Dreaming 已在 Claude 平台的 Managed Agents 中提供；开发者可以[在此申请访问](https://claude.com/form/claude-managed-agents)。

## **Outcomes: define the quality bar for agent work**|**Outcomes：为智能体的工作定义质量标准**

With [outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes), you write a rubric describing what success looks like and the agent works toward it.

借助 [outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes)，你写一份描述「成功长什么样」的评分标准（rubric），智能体就会朝着它努力。

A separate grader evaluates the output against your criteria in its own context window, so it isn't influenced by the agent's reasoning.

一个独立的打分器（grader）会在自己的上下文窗口里按你的标准评估产出，因此它不会受任务智能体推理过程的影响。

When something isn't right, the grader pinpoints what needs to change and the agent takes another pass.

当结果不对劲时，打分器会精确指出需要改动的地方，智能体再做一轮修改。

Agents do their best work when they know what "good" looks like.

智能体只有知道「好」长什么样，才能做出最好的工作。

For example, a structural framework, a presentation standard, or a set of requirements that need to be met.

例如：一个结构框架、一套演示文稿规范，或一组必须满足的需求。

With outcomes, agents can check their work against that bar and self-correct until the output is good enough, without a human needing to review each attempt.

有了 outcomes，智能体可以对照这条基准线检查自己的工作并自我纠正，直到产出足够好为止，而不需要人类去逐次审核每一轮尝试。

Outcomes is particularly useful for tasks that require attention to detail and exhaustive coverage.

Outcomes 对那些要求注重细节、要求穷尽覆盖的任务尤其有用。

It also works for subjective quality, like whether copy matches a brand voice or a design follows visual guidelines.

它也适用于主观质量判断，比如文案是否符合品牌语气、设计是否遵循视觉规范。

In testing, outcomes improved task success by up to 10 points over a standard prompting loop, with the largest gains on the hardest problems.

在测试中，相比标准的提示词循环，outcomes 把任务成功率最多提升了 10 个百分点，且在最难的问题上提升最大。

Outcomes also improved file generation quality, with +8.4% task success on docx and +10.1% on pptx in our internal benchmarks.

Outcomes 还改善了文件生成质量：在我们的内部基准中，docx 任务成功率提升 8.4%，pptx 提升 10.1%。

You can also now define an outcome, let the agent run, and get notified by a [webhook](http://platform.claude.com/docs/en/managed-agents/webhooks) when it's done.

现在你还可以先定义好一个 outcome，让智能体自行运行，完成时通过 [webhook](http://platform.claude.com/docs/en/managed-agents/webhooks) 接收通知。

## **Multiagent orchestration: Handle complex tasks with multiple agents**|**多智能体编排：用多个智能体处理复杂任务**

When there is too much work for a single agent to do well, [multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multi-agent) lets a lead agent break the job into pieces and delegate each one to a specialist with its own model, prompt, and tools.

当工作量大到单个智能体难以做好时，[多智能体编排](https://platform.claude.com/docs/en/managed-agents/multi-agent)允许一个主导智能体（lead agent）把任务拆分成若干块，并把每一块委派给一个专家智能体（specialist）——每个专家都有自己独立的模型、提示词和工具。

For example, a lead agent can run an investigation while subagents fan out through deploy history, error logs, metrics, and support tickets.

例如，lead agent 可以主持一场故障调查，同时让子智能体（subagent）分头去翻查部署历史、错误日志、监控指标和支持工单。

These specialists work in parallel on a shared filesystem and contribute to the lead agent's overall context.

这些专家智能体在共享文件系统（shared filesystem）上并行工作，并把成果汇入 lead agent 的整体上下文。

The lead agent can check back in with other agents mid-workflow because events are persistent and every agent remembers what it's done.

lead agent 可以在工作流进行到一半时回头与其他智能体核对进展，因为事件是持久化的，每个智能体都记得自己做过什么。

You can also trace every step in the [Claude Console](https://platform.claude.com/): which agent did what, in what order, and why, giving you full visibility into how your task was delegated and executed.

你还可以在 [Claude Console](https://platform.claude.com/) 中追溯每一个步骤：哪个智能体做了什么、按什么顺序、出于什么原因——让你对任务是如何被委派和执行的拥有完全的可见性。

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69f8ea208aefcf18345ee3ef_Claude-Managed-Agents-Blog-Followup-Sessions-UI.png)

## **What teams are building**|**各团队正在构建什么**

Teams are using dreaming, outcomes, and multiagent orchestration to ship agents that verify their own work, learn across sessions, and parallelize complex jobs:

各团队正在用 dreaming、outcomes 和多智能体编排交付这样的智能体：能自行验证工作成果、能跨会话学习、能把复杂任务并行化：

- [Harvey](https://www.harvey.ai/) uses Managed Agents to coordinate complex legal work like long-form drafting and document creation. With dreaming, their agents remember what they learned between sessions, including filetype workarounds and tool-specific patterns. Completion rates went up ~6x in their tests.

- [Harvey](https://www.harvey.ai/) 用 Managed Agents 协调复杂的法律工作，比如长篇文书起草和文档生成。借助 dreaming，他们的智能体能跨会话记住学到的东西，包括文件类型的变通处理方法和特定工具的使用模式。在他们的测试中，任务完成率提升了约 6 倍。

- Netflix's platform team built an analysis agent that processes logs from hundreds of builds across different sources. With changes that affect thousands of applications, what matters is finding the issues that recur across many of them. Multiagent orchestration lets the agent analyze batches in parallel and surface only the patterns worth acting on.

- Netflix 的平台团队构建了一个分析智能体，用于处理来自不同数据源的数百次构建的日志。当一次变更会影响数千个应用时，关键在于找出那些在大量应用中反复出现的问题。多智能体编排让这个智能体可以并行分析各批次日志，只把值得采取行动的模式浮现出来。

- [Spiral](http://writewithspiral.com/) by Every is using multiagent orchestration and outcomes to power the writing agent behind their new API and CLI. The lead agent runs on [Haiku](https://www.anthropic.com/claude/haiku): it fields incoming requests, poses quick follow-up questions when needed, then delegates the drafting to subagents running on [Opus](https://www.anthropic.com/claude/opus). When a user asks for multiple drafts, the subagents run in parallel. Writing quality is Spiral's core value, so they use outcomes to enforce it. Each draft is scored against a rubric of Every's editorial principles and the user's voice, both pulled from memory. Only drafts that clear the bar are returned.

- Every 旗下的 [Spiral](http://writewithspiral.com/) 正在用多智能体编排和 outcomes 驱动其新 API 和 CLI 背后的写作智能体。lead agent 运行在 [Haiku](https://www.anthropic.com/claude/haiku) 上：它接收传入请求，必要时快速追问几个问题，然后把起草工作委派给运行在 [Opus](https://www.anthropic.com/claude/opus) 上的子智能体。当用户要求生成多份草稿时，这些子智能体会并行运行。写作质量是 Spiral 的核心价值，所以他们用 outcomes 来强制保障它。每份草稿都会对照一份评分标准打分——标准由 Every 的编辑原则和用户的个人语气构成，两者都从记忆中提取。只有过线的草稿才会返回给用户。

- [Wisedocs](https://www.wisedocs.ai/blogs/building-managed-agents-for-document-verification) built a document quality check agent on Managed Agents, using outcomes to grade each review against their internal guidelines. Reviews now run 50% faster, while staying aligned with their team's standards.

- [Wisedocs](https://www.wisedocs.ai/blogs/building-managed-agents-for-document-verification) 基于 Managed Agents 构建了一个文档质量检查智能体，用 outcomes 按照内部规范给每次评审打分。现在评审速度提升了 50%，同时始终与团队标准保持一致。

## **Getting started**|**开始使用**

Dreaming is available in research preview, outcomes, multiagent orchestration, and memory are available in public beta as part of Managed Agents.

Dreaming 目前以研究预览版提供；outcomes、多智能体编排和记忆功能则作为 Managed Agents 的一部分，以公开测试版（public beta）提供。

To get started with dreaming, request access [here](https://claude.com/form/claude-managed-agents).

要开始使用 dreaming，请[在此申请访问](https://claude.com/form/claude-managed-agents)。

Explore our [documentation](https://platform.claude.com/docs/en/managed-agents/overview) to learn more or visit the [Claude Console](https://platform.claude.com/) to deploy your first agent.

想了解更多，请查阅我们的[文档](https://platform.claude.com/docs/en/managed-agents/overview)；或者访问 [Claude Console](https://platform.claude.com/) 部署你的第一个智能体。
