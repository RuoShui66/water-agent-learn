# 02_A harness for every task: dynamic workflows in Claude Code_每个任务配一套 harness：Claude Code 的动态工作流

> 原文：https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code
> 作者：Thariq Shihipar、Sid Bidasaria（Anthropic）｜发布日期：2026-06-02

## 📌 本篇速览

- 📅 2026-06-02
- ⭐ ★★★★★ **必读** —— harness 产品化的终点形态：**harness 本身也由模型现场生成**。六种组合模式可以直接当设计词汇表背下来。
- 🏷 dynamic workflows、subagent 编排、六种组合模式、三种失败模式、ultracode
- 🗂 [返回专题目录](00_目录.md)

本文宣布 Claude Code 支持「动态工作流」（dynamic workflows）：Claude 可以为手头任务现场编写并执行一个 JavaScript 编排文件，派生和协调多个子智能体，每个子智能体拥有独立上下文窗口、可单独选择模型、可选择是否隔离在独立 worktree 中。文章解释了动态工作流要对抗的三种单上下文窗口失败模式（智能体偷懒、自我偏袒、目标漂移），给出六种可组合的编排模式（分类路由、扇出综合、对抗验证、生成过滤、锦标赛、循环直到完成），列举了迁移重构、深度研究、大规模验证、排序、规则遵从、根因调查、分诊、探索品味、评测、模型路由等使用场景，并讨论了何时不该用工作流、提示技巧、token 预算与保存分享方式。

---

Claude Code can now write and orchestrate its own multi-agent harness on the fly.

Claude Code 现在可以现场编写并编排属于它自己的多智能体 harness（编排框架）。

Here's how dynamic workflows work, and the patterns that get the most out of them.

本文介绍动态工作流（dynamic workflows）的工作原理，以及能把它们的价值发挥到最大的那些模式。

## Example prompts｜示例提示词

Before diving into the technical details, here are several example prompts to illustrate possibilities with workflows:

在深入技术细节之前，先看几个示例提示词，感受一下工作流能做什么：

- "This test fails maybe 1 in 50 runs. Set up a workflow to reproduce it. Form competing theories about the race, and don't stop until one theory survives the evidence."

- 「这个测试大概每 50 次运行会挂掉一次。建一个工作流去复现它。针对这个竞态（race）提出多个相互竞争的假说，在只剩一个假说经得起证据检验之前不要停。」

- "Using a workflow, go through my last 50 sessions and mine them for corrections I keep making and turn the recurring ones into `CLAUDE.md` rules"

- 「用一个工作流，翻遍我最近 50 次会话，挖掘我反复做出的纠正，把其中重复出现的整理成 `CLAUDE.md` 规则。」

- "Use a workflow to dig through #incidents in Slack for the past six months and find recurring root causes where nobody has filed a ticket."

- 「用一个工作流，把 Slack 里 #incidents 频道过去六个月的内容翻一遍，找出那些反复出现、但没人建过工单的根本原因。」

- "Take my business plan and run a workflow where different agents tear it apart from an investor's, a customer's, and a competitor's perspective."

- 「拿着我的商业计划书，跑一个工作流，让不同的智能体分别从投资人、客户和竞争对手的视角把它撕碎。」

- "Here's a folder of 80 resumes, use a workflow to rank them for the backend role and double-check the top ten. Interview me using the AskUserQuestion tool for a rubric."

- 「这个文件夹里有 80 份简历，用一个工作流针对后端岗位给它们排序，并对前十名做二次核查。用 AskUserQuestion 工具向我提问，整理出一份评分标准（rubric）。」

- "I need a name for this CLI tool. Use a workflow to brainstorm a bunch of options and run a tournament to pick the top 3."

- 「我需要给这个 CLI 工具起个名字。用一个工作流头脑风暴出一批候选，再跑一场锦标赛（tournament）选出前 3 名。」

- "Use a workflow to rename our User model to Account everywhere."

- 「用一个工作流把我们的 User 模型在所有地方重命名为 Account。」

- "Go through my blog post draft and verify every technical claim against the codebase using a workflow, I don't want to ship anything wrong."

- 「用一个工作流，把我博客草稿里的每一条技术论断都对照代码库验证一遍，我不想把任何错误的东西发出去。」

## How dynamic workflows work｜动态工作流的工作原理

Dynamic workflows execute a javascript file with special functions that help spawn and coordinate subagents.

动态工作流会执行一个 JavaScript 文件，其中带有帮助派生（spawn）和协调子智能体（subagent）的特殊函数。

They include standard JavaScript functions like JSON, Math, and Array to help process data.

它们还包含 JSON、Math、Array 这类标准 JavaScript 功能，用来辅助处理数据。

Dynamic workflows can decide which models an agent uses and whether subagents run in their own worktree, allowing Claude to choose the intelligence level and isolation needed.

动态工作流可以决定每个智能体使用哪个模型、子智能体是否在自己的 worktree 中运行，从而让 Claude 自行选择所需的智能等级和隔离程度。

If interrupted, resuming allows the workflow to pick up where it left off.

如果执行被打断，恢复后工作流可以从中断处继续跑下去。

## Why dynamic workflows｜为什么需要动态工作流

When the default Claude Code harness tackles a task, it must plan and execute within the same context window.

当默认的 Claude Code harness 处理一个任务时，它必须在同一个上下文窗口（context window）里完成规划和执行。

For many coding tasks this works well, but breaks down over long-running, massively parallel, highly structured, and/or adversarial tasks.

对很多编码任务来说这没问题，但遇到长时间运行、大规模并行、高度结构化和/或对抗性的任务时，这种方式就会失灵。

The longer Claude works on complex tasks in a single context window, the more it becomes susceptible to specific failure modes:

Claude 在单个上下文窗口里处理复杂任务的时间越长，就越容易陷入以下几种特定的失败模式：

- **Agentic laziness**: Claude stops before finishing complex, multi-part tasks and declares the job done after partial progress.

- **智能体偷懒（Agentic laziness）**：Claude 在复杂的多部分任务尚未完成时就停手，只推进了一部分就宣告任务已完成。

- **Self-preferential bias**: Claude tends to prefer its own results, especially when asked to verify them against a rubric.

- **自我偏袒（Self-preferential bias）**：Claude 倾向于偏爱自己产出的结果，尤其是在被要求按评分标准验证这些结果的时候。

- **Goal drift**: Gradual loss of fidelity to the original objective across many turns, especially after compaction. Each summarization step is lossy, and details can get lost.

- **目标漂移（Goal drift）**：经过许多轮对话后，对原始目标的忠实度逐渐流失，在上下文压缩（compaction）之后尤其明显。每一步摘要都是有损的，细节可能就此丢失。

Creating a workflow combats these by orchestrating separate Claude subagents with their own context windows and focused, isolated goals.

创建工作流对抗这些问题的方式，是编排多个各自拥有独立上下文窗口、目标专注且相互隔离的 Claude 子智能体。

## Dynamic vs static workflows｜动态工作流 vs 静态工作流

Static workflows created previously using the Claude Agent SDK or `claude -p` coordinate multiple instances of Claude Code together but are typically more generic since they work for all edge cases.

以前用 Claude Agent SDK 或 `claude -p` 创建的静态工作流也能把多个 Claude Code 实例协调起来，但因为要覆盖所有边界情况，它们通常更通用、更泛化。

With Claude Opus 4.8 and dynamic workflows, Claude is now intelligent enough to write a custom harness tailor-made for specific use cases.

有了 Claude Opus 4.8 和动态工作流，Claude 现在已经足够聪明，可以为特定用例量身定制一套专属 harness。

## Helpful patterns when using dynamic workflows｜使用动态工作流的实用模式

You can start using dynamic workflows by asking Claude to make one, or by using the trigger word "`ultracode`" to ensure Claude Code creates a workflow.

你可以直接让 Claude 创建一个动态工作流来开始使用，也可以用触发词「`ultracode`」来确保 Claude Code 一定会创建工作流。

Common patterns Claude might use and compose together when building workflows include:

Claude 在构建工作流时可能使用并相互组合的常见模式包括：

### Classify-and-act｜分类后行动

Use a classifier agent to decide on task type, then route to different agents or behaviors based on the task.

用一个分类器智能体判断任务类型，然后根据任务路由到不同的智能体或不同的行为。

Alternatively, use a classifier at the end to determine output.

或者反过来，在流程末尾用一个分类器来决定最终输出。

### Fan-out-and-synthesize｜扇出后综合

Split a task into many smaller steps, run an agent on each step, then synthesize results.

把任务拆成许多小步骤，每个步骤跑一个智能体，最后综合所有结果。

This is particularly useful for large numbers of smaller steps where each benefits from its own clean context window.

当小步骤数量很多、且每一步都能从自己干净的上下文窗口中受益时，这种模式特别有用。

The synthesize step waits for all fan-out agents, then merges their structured outputs into one result.

综合步骤会等待所有扇出的智能体完成，然后把它们的结构化输出合并成一个结果。

### Adversarial verification｜对抗式验证

For each spawned agent, run a separate spawned agent to adversarially verify its output against a rubric or criteria.

每派生一个智能体，就再派生一个独立的智能体，按评分标准或准则对前者的产出做对抗式验证。

### Generate-and-filter｜生成后过滤

Generate a number of ideas on a topic, then filter them by a rubric or verification, dedupe duplicates, and return only the highest quality, tested ideas.

先就某个主题生成一批想法，然后按评分标准或验证流程过滤、去重，只返回质量最高、经过检验的想法。

### Tournament｜锦标赛

Instead of dividing work, have agents compete on it.

不是把工作拆分开，而是让智能体们在同一件事上竞争。

Spawn N agents that each attempt the same task using different approaches.

派生 N 个智能体，各自用不同的方法尝试同一个任务。

Prompts or models then judge the results in a pairwise fashion using a judging agent until a winner emerges.

然后由提示词或模型通过一个评判智能体对结果做两两比较（pairwise）评判，直到决出胜者。

### Loop until done｜循环直到完成

For tasks with unknown work amounts, loop spawning agents until a stop condition is met (no new findings, or no more errors in logs) instead of a fixed number of passes.

对于工作量未知的任务，不要设定固定的执行轮数，而是循环派生智能体，直到满足停止条件（没有新发现，或日志里不再有错误）。

## Use cases｜使用场景

### Migrations and refactors｜迁移与重构

Bun was rewritten from Zig to Rust using workflows.

Bun 从 Zig 到 Rust 的重写就是用工作流完成的。

Break down the task into steps that need operating on—callsites, failing tests, modules, etc.

把任务分解成需要逐一处理的步骤——调用点（callsite）、失败的测试、模块等等。

Spin off a subagent for every fix in a worktree, then have another agent adversarially review and merge them.

为每个修复在 worktree 中派生一个子智能体，然后让另一个智能体做对抗式审查并合并这些修复。

Consider telling the agent not to use resource intensive commands to maximally parallelize.

可以考虑告诉智能体不要使用资源密集型命令，以便最大化并行度。

### Deep research｜深度研究

Claude Code includes a deep research skill (`/deep-research`) using dynamic workflows.

Claude Code 内置了一个使用动态工作流的深度研究技能（`/deep-research`）。

It fans-out web searches, fetches sources, adversarially verifies claims, and synthesizes a cited report.

它会扇出多路网页搜索、抓取信源、对论断做对抗式验证，最后综合出一份带引用的报告。

This pattern applies to research beyond web searches—compiling Slack status reports or exploring how features work in codebases.

这个模式不只适用于网页搜索类研究——汇编 Slack 状态报告、探索代码库里某个功能如何工作，都可以套用。

### Deep verification｜深度验证

If you have a report where you want to check and source every factual claim, generate a workflow where one agent identifies all factual claims, then spin off subagents to check each in-detail.

如果你有一份报告，想核查其中每一条事实性论断并给出出处，可以生成这样一个工作流：先由一个智能体识别出所有事实性论断，再派生子智能体逐条深入核查。

A verification agent can check the source subagent to ensure source quality.

还可以再加一个验证智能体去检查负责找出处的子智能体，确保信源质量。

### Sorting｜排序

When you have a list to sort by qualitative measurement that Claude Code evaluates well—support tickets by bug severity, for example—avoid sorting 1000+ rows in one prompt as quality degrades.

当你有一个列表需要按某种 Claude Code 擅长评估的定性指标排序时——比如按 bug 严重程度给支持工单排序——不要在一个提示词里排 1000 多行，那样质量会下降。

Instead run a tournament, a pipeline of pairwise-comparison agents (comparative judgment is more reliable than absolute scoring), or bucket-rank in parallel then merge.

正确做法是跑一场锦标赛、跑一条由两两比较智能体组成的流水线（比较式评判比绝对打分更可靠），或者并行分桶排名再合并。

Each comparison is its own agent, so the deterministic loop holds the bracket while only running order stays in context.

每次比较都是一个独立的智能体，所以对阵表由确定性的循环代码持有，上下文里只留当前的执行顺序。

### Memory and rule adherence｜记忆与规则遵从

If you have particular rules Claude misses or struggles with, create a workflow with a list of rules checked by verifier agents—one verifier per rule.

如果有某些规则 Claude 总是漏掉或做不好，可以创建一个工作流，用验证智能体逐条检查规则清单——每条规则配一个专职验证者。

Creating a skeptic persona subagent to review rules helps avoid too many false positives.

创建一个「怀疑者」人设的子智能体来复审规则，有助于避免过多误报。

Mine recent sessions and code review comments for recurring corrections, cluster them with parallel agents, adversarially verify each candidate (would this rule prevent a real mistake?), then distill survivors back into `CLAUDE.md`.

从最近的会话和代码审查评论中挖掘反复出现的纠正，用并行智能体做聚类，对每个候选规则做对抗式验证（这条规则真能防住一个真实的错误吗？），再把幸存下来的规则提炼回 `CLAUDE.md`。

### Root-cause investigation｜根因调查

Debugging works best with several independent hypotheses tested separately.

调试最好的方式是让多个独立假说分别接受检验。

Single context windows risk self-preferential bias.

单一上下文窗口存在自我偏袒的风险。

Workflows structurally prevent this by spinning up agents generating hypotheses from disjoint evidence—separate agents for logs, files, and data.

工作流从结构上杜绝了这个问题：让不同智能体各自基于互不重叠的证据生成假说——日志、文件、数据各配一个独立的智能体。

Each hypothesis faces a panel of verifiers and refuters.

每个假说都要面对一个由验证者和反驳者组成的评审团。

This applies beyond code: sales (why did sales drop in March?), data engineering (pipeline failures), or any post-mortem.

这不只适用于代码：销售分析（三月的销售额为什么下滑？）、数据工程（流水线故障），以及任何事后复盘都能用。

### Triaging at scale｜大规模分诊

Every team has support queues, bug reports, or backlogs that humans cannot fully process.

每个团队都有人力处理不完的支持队列、bug 报告或积压任务。

A triage workflow classifies each item, dedupes against tracked items, and takes action—attempting fixes or escalating to humans.

一个分诊（triage）工作流会对每一项做分类，与已跟踪的条目去重，然后采取行动——尝试修复，或升级给人类处理。

A useful triage pattern is quarantine: bar agents reading untrusted public content from taking high-privilege actions, which instead go to agents responsible for acting on information.

一个有用的分诊模式是隔离（quarantine）：禁止读取不可信公开内容的智能体执行高权限操作，这些操作交由专门负责根据信息采取行动的智能体执行。

Pair triage workflows with `/loop` for continuous operation.

把分诊工作流和 `/loop` 搭配使用，就能持续不间断地运转。

### Exploration and taste｜探索与品味

Workflows help exploring different solution approaches, especially taste-based work like design or naming that benefits from a rubric.

工作流有助于探索不同的解决方案思路，尤其是设计、命名这类依赖品味、能从评分标准中受益的工作。

Ask Claude to explore solutions and give a review agent a rubric for good solutions.

让 Claude 去探索各种方案，并给一个审查智能体一份「什么算好方案」的评分标准。

Complete the task when the review agent meets criteria.

当审查智能体判定方案达标时，任务即告完成。

Solutions can be ordered or selected via tournament based on the rubric.

各方案还可以基于评分标准，通过锦标赛来排序或选优。

### Evals｜评测

Run lightweight evals for particular tasks by spinning off separate agents in a worktree and then spinning off comparison agents to compare and grade outputs against a rubric.

针对特定任务跑轻量级评测（eval）：在 worktree 里派生多个独立智能体，再派生比较智能体按评分标准对产出进行比较和打分。

For example, evaluating and refining a created skill against particular criteria.

比如，按特定标准评估并打磨一个新创建的技能（skill）。

### Model and intelligence routing｜模型与智能等级路由

Create a classifier agent tuned to your tasks that decides which model to use.

创建一个针对你的任务调校过的分类器智能体，由它决定使用哪个模型。

This helps when tasks involve many tool calls and conducting research can identify the best model.

当任务涉及大量工具调用、且通过一番调研就能确定最佳模型时，这种做法很有帮助。

The best model for "explain how the auth module works" depends on auth module file count and codebase shape.

「解释一下 auth 模块是怎么工作的」这个任务用哪个模型最好，取决于 auth 模块的文件数量和代码库的形态。

A classifier agent researches this and routes to Sonnet or Opus based on expected task complexity.

分类器智能体会先调研这些情况，再根据预期的任务复杂度路由到 Sonnet 或 Opus。

## When not to use dynamic workflows｜什么时候不该用动态工作流

Workflows are new.

工作流还是个新事物。

While many use cases create outsized results, they are not needed for every task and may use significantly more tokens.

虽然在很多用例里它能带来超出寻常的效果，但并非每个任务都需要它，而且它可能会消耗明显更多的 token。

Use workflows creatively to push Claude Code in new ways.

请创造性地使用工作流，把 Claude Code 推向新的用法。

For regular coding tasks, ask: does it really need more compute?

对于常规编码任务，先问一句：这个任务真的需要更多算力吗？

Most traditional coding tasks do not need five reviewers.

大多数传统编码任务并不需要五个审查者。

The same judgment applies architecturally: the multi-agent versus single-agent decision follows similar logic—parallelism and specialization must earn their coordination cost.

同样的判断也适用于架构层面：多智能体还是单智能体的抉择遵循类似的逻辑——并行与专业化必须挣回它们的协调成本。

## Tips for building dynamic workflows｜构建动态工作流的技巧

### Prompting｜提示词

Detailed prompting using specific techniques creates the best results.

使用具体技巧的详细提示词能产出最好的结果。

Workflows need not be just for large tasks—you can prompt the model to use a "quick workflow."

工作流并非只能用于大任务——你也可以提示模型用一个「快速工作流」（quick workflow）。

For example, create quick adversarial review of an assumption.

比如，对某个假设快速做一轮对抗式审查。

### Combine with `/goal` and `/loop`｜与 `/goal` 和 `/loop` 组合

When using repeatable workflows (triage, research, verification), pair them with `/loop` for regular intervals and `/goal` to set hard completion requirements.

在使用可重复执行的工作流（分诊、研究、验证）时，可以搭配 `/loop` 设定固定间隔运行，搭配 `/goal` 设定硬性的完成要求。

### Token usage budgets｜token 用量预算

Set explicit token usage budgets for dynamic workflows to limit task token use.

为动态工作流设置显式的 token 用量预算，以限制任务的 token 消耗。

Prompt with a budget like: "use 10k tokens," which sets the cap.

在提示词里写明预算，比如「use 10k tokens」（使用 1 万 token），就能设定上限。

### Saving and sharing dynamic workflows｜保存与分享动态工作流

Save workflows by pressing "s" in the workflow menu.

在工作流菜单里按「s」即可保存工作流。

Check these into `~/.claude/workflows` or distribute via a skill.

可以把它们签入 `~/.claude/workflows`，或者通过技能（skill）来分发。

To share via a skill, put JavaScript workflow files in the skill folder and reference them in the SKILL.MD.

要通过技能分享，把 JavaScript 工作流文件放进技能目录，并在 SKILL.MD 中引用它们。

For more flexibility, prompt Claude to think of skill workflows as templates rather than scripts to run verbatim.

想要更高的灵活性，可以提示 Claude 把技能里的工作流当作模板来看待，而不是逐字执行的脚本。

## A new starting point for discovery｜探索的新起点

Workflows are a helpful new way to extend Claude Code.

工作流是扩展 Claude Code 的一种实用的新方式。

Think of them as a starting point to explore new Claude usage ways to accomplish tasks.

把它们看作一个起点，用来探索让 Claude 完成任务的新用法。

Much remains to discover about best usage practices.

关于最佳使用实践，还有大量的东西有待发掘。
