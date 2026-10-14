# 06_Agent Harness Engineering_智能体运行框架工程

> 原文：https://addyosmani.com/blog/agent-harness-engineering/
> 作者：Addy Osmani（Google，《Learning JavaScript Design Patterns》作者）｜发布日期：2026-04-19

## 📌 本篇速览

- 📅 2026-04-19　｜　⏱ 约 18 分钟　｜　📄 约 3,550 词 / 4 图
- ⭐ ★★★★★ **公开圈最好的 harness 综述，非官方材料里的第一选择** —— 它给了两个直接可用的思维工具：**「棘轮法则」**（每个错误变成一条规则）和**「从行为倒推组件」**的设计表。「harness 不缩小，只是转移」这句判断就出自这篇。
- 🏷 the ratchet、working backwards from behaviour、context rot、Ralph Loop、Harness-as-a-Service、AGENTS.md
- 🗂 [返回专题目录](00_目录.md)

本文是 Addy Osmani 对新兴学科 harness engineering（运行框架工程）的全景综述：`coding agent = AI model(s) + harness`，智能体的实际行为主要由围绕模型的 harness 决定，而非模型本身。文章汇拢 Viv Trivedy、HumanLayer、Anthropic、Simon Willison 等多方线索，系统讲解「skill issue」重构、棘轮法则、从行为倒推 harness 组件（文件系统/Git、bash、沙箱、记忆、上下文管理、长时程执行、hooks、`AGENTS.md`）、「harness 不缩小只转移」、模型—harness 协同训练循环，以及 Harness-as-a-Service 的未来走向。

---

*A coding agent is the model plus everything you build around it.*

*编程智能体（coding agent），就是模型加上你围绕它构建的一切。*

*Harness engineering treats that scaffolding as a real artifact, and it tightens every time the agent slips.*

*Harness 工程（harness engineering）把这层脚手架当作真正的工程产物来对待，而且智能体每失误一次，它就收紧一格。*

---

Roughly: anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again.

大意就是：每当你发现智能体犯了一个错误，你就花时间用工程手段做出一个解决方案，让它永远不再犯同样的错。

We’ve spent the last two years arguing about models.

过去两年，我们一直在争论模型。

Which one is smartest, which one writes the cleanest React, which one hallucinates less.

哪个最聪明、哪个写的 React 最干净、哪个幻觉（hallucination）更少。

That conversation is fine as far as it goes, but it’s missing the other half of the system.

这种讨论本身没什么问题，但它漏掉了系统的另一半。

The model is one input into a running agent.

模型只是运行中的智能体的一个输入。

The rest is the *harness*: the prompts, tools, context policies, hooks, sandboxes, subagents, feedback loops, and recovery paths wrapped around the model so it can actually finish something.

其余的部分是 *harness*（运行框架）：包裹在模型周围的提示词、工具、上下文策略、hooks、沙箱、子智能体、反馈循环与恢复路径——正是它们让模型能真正把事情做完。

**A decent model with a great harness beats a great model with a bad harness.**

**一个不错的模型配上出色的 harness，胜过一个出色的模型配上糟糕的 harness。**

I’ve watched this play out on my own work over and over.

在我自己的工作里，我一次又一次看到这一点应验。

And increasingly the interesting engineering isn’t in picking the model, it’s in designing the scaffolding around it.

而且越来越多有意思的工程工作，不在于挑选模型，而在于设计模型周围的脚手架。

That discipline now has a name.

这门学问现在有了名字。

Viv Trivedy coined the term *harness engineering*, and his [“Anatomy of an Agent Harness”](https://x.com/Vtrivedy10/status/2031408954517971368) post is the cleanest derivation of what a harness actually is and why each piece exists.

Viv Trivedy 创造了 *harness engineering* 这个术语，他的[《Anatomy of an Agent Harness》](https://x.com/Vtrivedy10/status/2031408954517971368)一文，是关于 harness 究竟是什么、每个部件为何存在的最清晰推导。

[Dex Horthy](https://x.com/dexhorthy/status/1985699548153467120) has been tracking the pattern as it emerges.

[Dex Horthy](https://x.com/dexhorthy/status/1985699548153467120) 一直在追踪这一模式的浮现。

[HumanLayer](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) frames most agent failures as “skill issues” that come down to configuration rather than model weights.

[HumanLayer](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) 把大多数智能体失败定性为「技术不行」（skill issue）——归根结底是配置问题，而不是模型权重问题。

[Anthropic’s engineering team](https://www.anthropic.com/engineering/harness-design-long-running-apps) has published what I think is the best public breakdown of how to design a harness for long-running work.

[Anthropic 的工程团队](https://www.anthropic.com/engineering/harness-design-long-running-apps)发表了我认为是公开材料中关于「如何为长时运行的工作设计 harness」的最佳拆解。

And [Birgitta Böckeler](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) has a good overview of what this looks like from the user’s side.

而 [Birgitta Böckeler](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) 则从用户视角给出了一份不错的综述。

This post is my attempt to pull those threads together.

这篇文章是我把这些线索汇拢到一起的一次尝试。

---

## What is a harness, really?｜harness 究竟是什么？

Viv’s one-liner does most of the work:

Viv 的一句话概括已经把大部分事情说清楚了：

> Agent = Model + Harness.

> 智能体 = 模型 + Harness。

> If you’re not the model, you’re the harness.

> 只要你不是模型，你就是 harness。

A harness is every piece of code, configuration, and execution logic that isn’t the model itself.

harness 是模型本身之外的每一段代码、每一项配置和每一处执行逻辑。

A raw model is not an agent.

裸模型并不是智能体。

It becomes one once a harness gives it state, tool execution, feedback loops, and enforceable constraints.

只有当 harness 赋予它状态、工具执行、反馈循环和可强制执行的约束之后，它才成为智能体。

![The anatomy of an agent harness. The model sits in the middle; the harness surrounds it with context injection, control flow, action, persistence, and observation.](https://addyosmani.com/assets/images/harness-anatomy.jpeg)

> 图注：智能体 harness 的解剖图。模型位于中央；harness 以上下文注入、控制流、行动、持久化与观测将其环绕。

Concretely, a harness includes:

具体而言，harness 包括：

- System prompts, `CLAUDE.md`, `AGENTS.md`, skill files, and subagent prompts

- 系统提示词、`CLAUDE.md`、`AGENTS.md`、skill 文件，以及子智能体提示词

- Tools, skills, MCP servers, and their descriptions

- 工具、skills、MCP servers，及其各自的描述

- Bundled infrastructure (filesystem, sandbox, browser)

- 捆绑的基础设施（文件系统、沙箱、浏览器）

- Orchestration logic (subagent spawning, handoffs, model routing)

- 编排逻辑（子智能体派生、交接、模型路由）

- Hooks and middleware for deterministic execution (compaction, continuation, lint checks)

- 用于确定性执行的 hooks 与中间件（压缩、续跑、lint 检查）

- Observability (logs, traces, cost and latency metering)

- 可观测性（日志、trace、成本与延迟计量）

[Simon Willison](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/) reduces the loop part to its essence: an agent is a system that *“runs tools in a loop to achieve a goal.”*

[Simon Willison](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/) 把「循环」这部分还原到本质：智能体就是一个*「在循环中运行工具以达成目标」*的系统。

The skill is in the design of both the tools and the loop.

真功夫在于工具和循环二者的设计。

If that sounds like a lot of surface area, it is.

如果这听起来涉及面很广——确实如此。

And it’s *your* surface area, not the model provider’s.

而且这是*你的*地盘，不是模型供应商的。

Claude Code, Cursor, Codex, Aider, Cline: these are all harnesses.

Claude Code、Cursor、Codex、Aider、Cline：这些全都是 harness。

**The model underneath is sometimes the same, but the behaviour you experience is dominated by what the harness does.**

**底下的模型有时是同一个，但你体验到的行为，主要由 harness 的所作所为决定。**

```
coding agent = AI model(s) + harness
```

This equation, articulated by Viv and echoed by HumanLayer, is where the work actually lives.

这个由 Viv 提出、并得到 HumanLayer 呼应的等式，正是真正的工作所在。

The debate over the left-hand side is loud.

围绕等式左边的争论声音很大。

Most of the actual leverage sits on the right.

但绝大部分实际的杠杆都在右边。

---

## The “skill issue” reframe｜「Skill issue」重构

There’s a pattern I watch engineers fall into.

我见过工程师们反复陷入的一种模式。

The agent does something dumb, the engineer blames the model, and the blame gets filed under “wait for the next version.”

智能体干了件蠢事，工程师怪罪模型，然后这笔账被归档到「等下一个版本吧」。

The harness-engineering mindset rejects that default.

harness 工程的思维方式拒绝这种默认反应。

The failure is usually legible.

失败通常是可以读懂的。

The agent didn’t know about a convention, so you add it to `AGENTS.md`.

智能体不知道某条约定，那就把它加进 `AGENTS.md`。

The agent ran a destructive command, so you add a hook that blocks it.

智能体跑了一条破坏性命令，那就加一个 hook 拦住它。

The agent got lost in a 40-step task, so you split it into a planner and an executor.

智能体在一个 40 步的任务里迷了路，那就把它拆成规划者（planner）和执行者（executor）。

The agent kept “finishing” broken code, so you wire a typecheck back-pressure signal into the loop.

智能体总把有问题的代码当成「完工」，那就往循环里接一路类型检查的反压信号（back-pressure signal）。

HumanLayer says: *“it’s not a model problem. It’s a configuration problem.”*

HumanLayer 说：*「这不是模型问题，是配置问题。」*

Harness engineering is what happens when you take that seriously.

当你把这句话当真时，做出来的东西就是 harness 工程。

There’s a striking data point that shows up in both Viv’s write-up and HumanLayer’s.

Viv 和 HumanLayer 的文章里都出现了一个惊人的数据点。

On Terminal Bench 2.0, Claude Opus 4.6 running inside Claude Code scores far lower than the same model running in a custom harness.

在 Terminal Bench 2.0 上，跑在 Claude Code 里的 Claude Opus 4.6，得分远低于同一个模型跑在自建 harness 里的成绩。

Viv’s team moved a coding agent from Top 30 to Top 5 by changing only the harness.

Viv 的团队只改 harness，就把一个编程智能体从 Top 30 拉到了 Top 5。

Models get post-training coupled to the harness they were trained against.

模型在后训练（post-training）阶段会与其训练时所配的 harness 耦合。

Moving them into a different harness, with better tools for your codebase, a tighter prompt, and sharper back-pressure, can unlock capability the original harness was leaving on the floor.

把模型挪进另一个 harness——配上更适合你代码库的工具、更紧凑的提示词、更锐利的反压——可以解锁被原 harness 白白丢在地上的能力。

This is the opposite of the “just wait for GPT-6” narrative.

这与「等 GPT-6 就好了」的叙事截然相反。

**The gap between what today’s models can do and what you see them doing is largely a harness gap.**

**今天的模型能做到的，与你实际看到它们做到的，二者之间的差距在很大程度上是 harness 的差距。**

---

## The ratchet: every mistake becomes a rule｜棘轮：每个错误都变成一条规则

The most important habit in harness engineering is treating agent mistakes as permanent signals.

harness 工程中最重要的习惯，是把智能体的错误当作永久信号。

Not one-off stories to laugh about, not “bad runs” to retry.

不是一笑而过的一次性轶事，也不是重试一下就算了的「坏运行」。

Signals.

是信号。

If the agent ships a PR with a commented-out test and I merge it by accident, that’s an input.

如果智能体交付了一个含有被注释掉的测试的 PR，而我不小心把它合并了，这就是一条输入。

The next version of my `AGENTS.md` says “never comment out tests; delete them or fix them.”

我下一版 `AGENTS.md` 会写上「永远不要注释掉测试；要么删掉，要么修好」。

The next version of my pre-commit hook greps for `.skip(` and `xit(` in the diff.

我下一版 pre-commit hook 会在 diff 里 grep `.skip(` 和 `xit(`。

The next version of my reviewer subagent flags commented-out tests as a blocker.

我下一版评审子智能体会把被注释掉的测试标记为阻断项（blocker）。

You only add constraints when you’ve seen a real failure.

只有见过真实的失败，才添加约束。

You only remove them when a capable model has made them redundant.

只有当足够强的模型让某条约束变得多余时，才移除它。

**Every line in a good `AGENTS.md` should be traceable back to a specific thing that went wrong.**

**好的 `AGENTS.md` 里的每一行，都应该能追溯到某件具体出过错的事。**

This is also why harness engineering is a discipline rather than a framework.

这也是为什么 harness 工程是一门修行的学问（discipline），而不是一个框架。

The right harness for your codebase is shaped by your failure history.

适合你代码库的那个 harness，是由你的失败史塑造出来的。

You can’t download it.

你没法把它下载下来。

---

## Working backwards from behaviour｜从行为倒推

The framing from Viv that I find most useful when I’m actually designing a harness is to start from the behaviour you want and derive the harness piece that delivers it.

当我真正动手设计 harness 时，Viv 给出的最有用的框架是：从你想要的行为出发，倒推出实现它的那块 harness 部件。

His pattern: *behaviour we want (or want to fix) → harness design to help the model achieve this.*

他的模式是：*我们想要（或想修复）的行为 → 帮助模型实现该行为的 harness 设计。*

![Each harness feature derives from a behaviour the model can't deliver on its own. Work with real data durably maps to filesystem and git. Write and execute code maps to bash and code execution. Safe execution plus defaults maps to sandboxed environments and tooling. Remembering new knowledge maps to memory files, web search, and MCPs. Performance over long contexts maps to compaction, tool offloading, and skills. Long-horizon work maps to Ralph loops, planning, and verification.](https://addyosmani.com/assets/images/harness-behavior-mapping.jpeg)

> 图注：每项 harness 特性都源自一种模型自己无法交付的行为。「持久地处理真实数据」映射到文件系统与 git；「编写并执行代码」映射到 bash 与代码执行；「安全执行 + 默认配置」映射到沙箱环境与工具链；「记住新知识」映射到记忆文件、web 搜索与 MCP；「长上下文下的性能」映射到压缩、工具输出外置与 skills；「长时程工作」映射到 Ralph loops、规划与验证。

The useful thing about deriving it this way is that every harness component has a specific job.

用这种方式推导的好处在于，每个 harness 组件都有明确的职责。

**If you can’t name the behaviour a component exists to deliver, it probably shouldn’t be there.**

**如果你说不出某个组件是为了交付哪种行为而存在，它多半就不该在那儿。**

The rest of this section walks the pieces in roughly the order Viv does, with the specific patterns I’ve found worth stealing.

本节余下部分大致按 Viv 的顺序把这些部件过一遍，并附上我认为值得「偷学」的具体模式。

### Filesystem and Git: durable state｜文件系统与 Git：持久状态

The filesystem is the most foundational primitive, and it tends to be underrated because it’s boring.

文件系统是最基础的原语（primitive），它因为太无聊而常被低估。

Models can only directly operate on what fits in context.

模型只能直接操作那些装得进上下文的东西。

Without a filesystem, you’re copy-pasting into a chat window, and that isn’t a workflow.

没有文件系统，你就只能往聊天窗口里复制粘贴，那可算不上工作流。

Once you have a filesystem, the agent gets a workspace to read data, code, and docs; a place to offload intermediate work instead of holding it in context; and a surface where multiple agents and humans can coordinate through shared files.

一旦有了文件系统，智能体就得到了一个可以读取数据、代码和文档的工作区；一个可以卸载中间成果、而不必全都攥在上下文里的地方；以及一个让多个智能体与人类能够通过共享文件协调的界面。

Adding Git on top gives you versioning for free, so the agent can track progress, roll back errors, and branch experiments.

再在其上加上 Git，就免费获得了版本管理，智能体可以借此跟踪进度、回滚错误、用分支做实验。

Most of the other harness primitives end up pointing at the filesystem for something.

其他大多数 harness 原语，最终都会在某些事情上指向文件系统。

### Bash and code execution: the general-purpose tool｜Bash 与代码执行：通用工具

The main agent loop today is a ReAct loop: the model reasons, takes an action via a tool call, observes the result, and repeats.

今天主流的智能体循环是 ReAct 循环：模型推理，通过工具调用采取行动，观察结果，然后重复。

But a harness can only execute the tools it has logic for.

但 harness 只能执行它写好了相应逻辑的那些工具。

You can try to pre-build a tool for every possible action, or you can give the agent bash and let it build the tools it needs on the fly.

你可以试着为每一种可能的动作预建一个工具，也可以直接给智能体 bash，让它随用随造自己需要的工具。

Willison’s take on this is that agents already excel at shell commands; most tasks collapse to a few well-chosen CLI invocations.

Willison 对此的看法是：智能体本来就擅长 shell 命令；大多数任务最终都能收敛为几条精心挑选的 CLI 调用。

Harnesses still ship focused tools, but bash plus code execution has become the default general-purpose strategy for autonomous problem solving.

harness 仍然会内置一些聚焦的工具，但「bash + 代码执行」已成为自主解决问题的默认通用策略。

It’s the difference between teaching someone to use a single kitchen gadget and handing them a kitchen.

这就像「教人用一件单一功能的厨房小电器」和「直接把整个厨房交给他」的区别。

### Sandboxes and default tooling｜沙箱与默认工具链

Bash is only useful if it runs somewhere safe.

bash 只有跑在安全的地方才有用。

Running agent-generated code on your laptop is risky, and a single local environment doesn’t scale to many parallel agents.

在自己的笔记本上直接运行智能体生成的代码风险很大，而且单个本地环境也支撑不了大量并行智能体。

Sandboxes give agents an isolated operating environment.

沙箱给智能体提供一个隔离的运行环境。

Instead of executing locally, the harness connects to a sandbox to run code, inspect files, install dependencies, and verify work.

harness 不在本地执行，而是连接到沙箱去运行代码、检查文件、安装依赖、验证工作成果。

You can allow-list commands, enforce network isolation, spin up new environments on demand, and tear them down when the task is done.

你可以给命令设白名单（allow-list）、强制网络隔离、按需拉起新环境，并在任务完成后把它们销毁。

A good sandbox ships with good defaults: pre-installed language runtimes and packages, Git and test CLIs, a headless browser for web interaction.

好的沙箱自带好的默认配置：预装的语言运行时和软件包、Git 和测试 CLI、用于网页交互的无头浏览器（headless browser）。

Browsers, logs, screenshots, and test runners are what let the agent observe its own work and close the self-verification loop.

浏览器、日志、截图和测试运行器，正是让智能体得以观察自己的工作、闭合自我验证循环的东西。

The model doesn’t configure its execution environment.

模型并不配置自己的执行环境。

Deciding where the agent runs, what’s available, and how it verifies its output are all harness-level calls.

智能体在哪运行、有什么可用、如何验证输出——这些全是 harness 层面的决策。

### Memory and search: continual learning｜记忆与搜索：持续学习

Models have no additional knowledge beyond their weights and what’s currently in context.

除了权重和当前上下文里的内容，模型没有任何额外知识。

Without the ability to edit weights, the only way to add knowledge is through context injection.

在无法修改权重的前提下，添加知识的唯一途径就是上下文注入（context injection）。

The filesystem is again the primitive.

文件系统再一次充当了那个原语。

Harnesses support memory file standards like `AGENTS.md` that get injected on every start.

harness 支持像 `AGENTS.md` 这样的记忆文件标准，每次启动时都会注入。

As the agent edits that file, the harness reloads it, and knowledge from one session carries into the next.

当智能体编辑这个文件时，harness 会重新加载它，于是一个会话里的知识就被带进了下一个会话。

This is a crude but effective form of continual learning.

这是一种粗糙但有效的持续学习（continual learning）形式。

For knowledge that didn’t exist at training time (new library versions, current docs, today’s data) web search and MCP tools like Context7 bridge the cutoff.

对于训练时还不存在的知识（新的库版本、最新文档、今天的数据），web 搜索和 Context7 之类的 MCP 工具可以跨过知识截止线。

These are useful primitives to bake into the harness rather than leaving to the user.

这些原语值得直接内置进 harness，而不是留给用户自己解决。

### Battling context rot｜对抗上下文腐烂

Context rot is the observation that models get worse at reasoning and completing tasks as the context window fills up.

上下文腐烂（context rot）指的是这样一个观察：随着上下文窗口被填满，模型的推理和完成任务的能力会变差。

Context is scarce, and harnesses are largely delivery mechanisms for good context engineering.

上下文是稀缺资源，而 harness 在很大程度上就是优良上下文工程（context engineering）的交付机制。

Three techniques show up repeatedly:

有三种技巧反复出现：

**Compaction.**

**压缩（Compaction）。**

When the window gets close to full, something has to give.

当窗口快满时，总得有东西让路。

Letting the API error is not an option for a production harness, so the harness intelligently summarizes and offloads older context so the agent can keep working.

对生产级 harness 来说，任由 API 报错不是可选项，所以 harness 会智能地对较早的上下文做摘要和外置，让智能体能继续工作。

**Tool-call offloading.**

**工具调用输出外置（Tool-call offloading）。**

Large tool outputs (think 2,000-line log files) clutter context without adding much signal.

大体积的工具输出（想想 2000 行的日志文件）会塞满上下文，却没添加多少信号。

The harness keeps the head and tail tokens above a threshold and offloads the full output to the filesystem, where the agent can read it on demand.

harness 会在输出超过阈值时只保留开头和结尾的 token，把完整输出外置到文件系统，智能体需要时再按需去读。

**Skills with progressive disclosure.**

**渐进披露的 Skills（progressive disclosure）。**

Loading every tool and MCP into context at startup degrades performance before the agent takes a single action.

启动时把每个工具和 MCP 都加载进上下文，会让智能体还没采取任何行动，性能就已经先劣化了。

Skills let the harness reveal instructions and tools only when the task actually calls for them.

Skills 让 harness 只在任务真正需要时，才展开对应的指令和工具。

Anthropic’s harness post adds one more technique for the really long jobs: full context resets, where the harness tears the session down and rebuilds it from a compact hand-off file.

Anthropic 的 harness 文章为真正的超长任务补充了一招：完全上下文重置（full context reset）——harness 把会话整个拆掉，再从一份紧凑的交接文件重建。

They’re explicit that *compaction alone wasn’t sufficient* for long tasks; sometimes you need to start fresh with a structured brief.

他们明确指出，对于长任务，*仅靠压缩并不够*；有时你需要带着一份结构化的简报（brief）从头再来。

This is closer to how humans onboard a new engineer than to how we usually think about “memory.”

这更接近人类给新工程师做入职引导的方式，而不是我们通常理解的「记忆」。

### Long-horizon execution: Ralph Loops, planning, verification｜长时程执行：Ralph Loops、规划与验证

Autonomous long-horizon work is the holy grail and the hardest thing to get right.

自主的长时程（long-horizon）工作是圣杯，也是最难做对的事。

Today’s models suffer from early stopping, poor decomposition of complex problems, and incoherence as work stretches across multiple context windows.

今天的模型有几个毛病：过早停止、对复杂问题分解不佳，以及当工作跨越多个上下文窗口时前后失联。

The harness has to design around all of that.

harness 必须围绕这一切做设计。

I’ve written about autonomous coding loops like the Ralph Loop before in [self-improving agents](https://addyosmani.com/blog/self-improving-agents/) and in my [2026 trends piece](https://beyond.addy.ie/2026-trends/), but it’s worth restating in this framing: a hook intercepts the model’s attempt to exit and re-injects the original prompt into a fresh context window, forcing the agent to continue against a completion goal.

我之前在[《self-improving agents》](https://addyosmani.com/blog/self-improving-agents/)和我的 [2026 趋势文章](https://beyond.addy.ie/2026-trends/)里写过 Ralph Loop 这类自主编码循环，但值得在这个框架下重述一遍：一个 hook 拦截模型的退出企图，把原始提示词重新注入一个全新的上下文窗口，迫使智能体对着完成目标继续干下去。

Each iteration starts clean but reads state from the previous one through the filesystem.

每轮迭代都从干净状态开始，但会通过文件系统读取上一轮的状态。

It’s a surprisingly simple trick for turning a single-session agent into a multi-session one, and it’s the kind of primitive you’d never derive from “just use a smarter model.”

这是把单会话智能体变成多会话智能体的一个出奇简单的技巧，也是那种你永远无法从「换个更聪明的模型就行」推导出来的原语。

**Planning** is when the model decomposes a goal into a sequence of steps, usually into a plan file on disk.

**规划（Planning）**指模型把目标分解成一系列步骤，通常写进磁盘上的一个计划文件。

The harness supports this with prompting and reminders about how to use the plan file.

harness 通过提示词以及「如何使用计划文件」的提醒来支持这件事。

After each step, the agent checks its work via self-verification: hooks run a pre-defined test suite and loop failures back to the model with the error text, or the model reviews its own output against explicit criteria.

每完成一步，智能体都通过自我验证来检查工作：由 hooks 运行一套预定义的测试并把失败连同报错文本回传给模型，或者由模型对照明确的标准评审自己的输出。

**Planner / generator / evaluator splits.**

**规划者 / 生成者 / 评估者分离（Planner / generator / evaluator splits）。**

Anthropic’s long-running harness work is explicit that separating generation from evaluation into distinct agents outperforms self-evaluation, because agents reliably skew positive when grading their own work.

Anthropic 关于长时运行 harness 的工作明确指出：把生成与评估拆分成不同的智能体，效果优于自我评估，因为智能体给自己的工作打分时总是稳定地偏乐观。

It’s GANs for prose.

这就是文本版的 GAN。

The related pattern is the **sprint contract**, where the generator and evaluator negotiate what “done” actually means before code gets written.

与之相关的模式是**冲刺契约（sprint contract）**：在代码写下之前，生成者和评估者先协商好「完成」到底意味着什么。

In my own workflows, writing down the done-condition before starting has caught more scope drift than any prompt change I’ve ever made.

在我自己的工作流里，开工前写下完成条件（done-condition）所抓住的范围漂移（scope drift），比我做过的任何提示词改动都多。

### Hooks: the enforcement layer｜Hooks：强制层

Hooks are what separate “I told the agent to do X” from “the system enforces X.”

Hooks 是把「我告诉过智能体要做 X」和「系统强制执行 X」区分开来的东西。

A hook is a script that runs at a specific lifecycle point: before a tool call, after a file edit, before commit, on session start.

hook 是在特定生命周期节点运行的脚本：工具调用前、文件编辑后、提交前、会话启动时。

They’re the right place for things the agent should never forget but often does.

那些智能体永远不该忘、却经常忘掉的事，放在 hooks 里正合适。

Run typecheck and lint and tests after every edit and surface failures.

每次编辑后运行类型检查、lint 和测试，并把失败暴露出来。

Block destructive bash (`rm -rf`, `git push --force`, `DROP TABLE`).

拦截破坏性的 bash 命令（`rm -rf`、`git push --force`、`DROP TABLE`）。

Require approval before opening a PR or pushing to `main`.

在开 PR 或推送到 `main` 之前要求审批。

Auto-format on write so the agent doesn’t waste tokens on whitespace.

写入时自动格式化，让智能体不必在空白符上浪费 token。

The principle HumanLayer highlights and I’ve come to agree with is: **success is silent, failures are verbose.**

HumanLayer 强调、而我也已经认同的原则是：**成功保持沉默，失败大声说话（success is silent, failures are verbose）。**

If typecheck passes, the agent hears nothing.

类型检查通过，智能体什么也听不到。

If it fails, the error text gets injected into the loop and the agent self-corrects.

一旦失败，报错文本会被注入循环，智能体随即自我纠正。

That makes the feedback loop almost free in the common case and directly actionable when something goes wrong.

这让反馈循环在常规情形下几乎零成本，而在出问题时又能直接指导行动。

### `AGENTS.md` and tool choice｜`AGENTS.md` 与工具选择

The flat markdown rulebook at the root of your repo is still the single highest-leverage configuration point, because it lands in the system prompt every turn.

仓库根目录下这份扁平的 markdown 规则手册，仍然是杠杆最高的单一配置点，因为它每一轮都会落进系统提示词。

Conventions go here: package manager, test framework, formatting, “never touch `/legacy`,” “always use our logger.”

各种约定都放这里：包管理器、测试框架、格式化规则、「永远别碰 `/legacy`」、「始终用我们的 logger」。

Two hard-won lessons:

两条来之不易的教训：

Keep it short.

保持简短。

HumanLayer keeps theirs under 60 lines.

HumanLayer 把他们的那份控制在 60 行以内。

Every line is competing for attention, and more rules make each rule matter less.

每一行都在争夺注意力，规则越多，每条规则的分量就越轻。

**Pilot’s checklist, not style guide.**

**要飞行员检查单，不要风格指南。**

Earn each line.

每一行都要挣来。

Rules should trace to a specific past failure or a hard external constraint.

规则应当能追溯到某次具体的过往失败，或某条硬性的外部约束。

If they don’t, they’re noise.

否则它们就是噪音。

Ratchet; don’t brainstorm.

要棘轮，不要头脑风暴。

Same discipline applies to tools.

同样的纪律也适用于工具。

Each tool’s name, description, and schema gets stamped into the prompt every request.

每个工具的名称、描述和 schema 都会在每个请求里被压进提示词。

Ten focused tools outperform fifty overlapping ones because the model can hold the menu in its head.

十个聚焦的工具胜过五十个相互重叠的工具，因为模型能把整份菜单装进脑子里。

HumanLayer also flags a real security concern here: tool descriptions populate the prompt, so any MCP server you install is trusted text the model will read.

HumanLayer 还在这里指出了一个真实的安全隐患：工具描述会进入提示词，所以你安装的任何 MCP server 都是模型会读到的被信任文本。

A sloppy or malicious MCP can prompt-inject your agent before you’ve typed anything.

一个粗制滥造或恶意的 MCP，可以在你还没敲下任何字之前，就对你的智能体完成提示词注入（prompt injection）。

### What this looks like in production｜这在生产环境里长什么样

The clearest public picture I’ve seen of a mature harness is Fareed Khan’s (estimated) breakdown of [Claude Code’s architecture](https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0), and it’s worth sitting with the diagram for a minute.

关于成熟 harness，我见过的最清晰的公开图景是 Fareed Khan 对 [Claude Code 架构](https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0)的（推测性）拆解，那张图值得你花上一分钟细看。

![Claude Code architecture, annotated by layer: an input layer with the user interface, session manager, and permission gate; a knowledge layer with the skill registry, context compressor, task graph, and memory store; an integration layer with the MCP runtime and external servers; an execution layer with tool dispatch, a streaming runtime, and a prompt cache; an output layer returning verified task results; an observability layer with an event bus and background executor; and a multi-agent layer containing subagent spawning, teammate mailboxes, an FSM protocol, an autonomous board, and a worktree isolator. The master agent loop sits at the centre of the diagram, with arrows flowing in from every layer.](https://addyosmani.com/assets/images/claude-code-architecture.jpeg)

> 图注：按层标注的 Claude Code 架构：输入层含用户界面、会话管理器与权限闸门；知识层含 skill 注册表、上下文压缩器、任务图与记忆存储；集成层含 MCP 运行时与外部 servers；执行层含工具分发、流式运行时与提示词缓存；输出层返回经验证的任务结果；可观测层含事件总线与后台执行器；多智能体层含子智能体派生、队友邮箱、FSM 协议、自主看板与 worktree 隔离器。主智能体循环位于图的中央，每一层都有箭头汇入其中。

Almost every concept from the previous section shows up on this diagram as a named component.

上一节的几乎每个概念，都以具名组件的形式出现在这张图上。

Context injection is the knowledge layer.

上下文注入就是知识层。

Loop state lives in the memory store and the worktree isolator.

循环状态存放在记忆存储和 worktree 隔离器里。

Destructive-action hooks sit behind the permission gate.

拦截破坏性动作的 hooks 藏在权限闸门之后。

Subagent context firewalls are the entire multi-agent layer.

子智能体的上下文防火墙就是整个多智能体层。

The tool dispatch registry is where MCP servers and bash both plug in.

工具分发注册表则是 MCP servers 和 bash 共同接入的地方。

Khan’s argument is the same as Viv’s, just worked through a shipping product: **Claude Code’s trajectory is about the harness at least as much as about the model underneath it.**

Khan 的论点和 Viv 的一样，只是借一个已经上市的产品完整推演了一遍：**Claude Code 的发展轨迹，系于 harness 的程度至少不亚于系于它底下的模型。**

---

## Harnesses don’t shrink, they move｜harness 不会缩小，只会转移

One of the better observations in the Anthropic write-up is that as models improve, the space of interesting harness combinations doesn’t shrink.

Anthropic 那篇文章里较精彩的观察之一是：随着模型进步，有意思的 harness 组合空间并不会缩小。

It moves.

它只是转移。

The naive story is that better models make harnesses obsolete.

天真版本的故事是：模型变好了，harness 就过时了。

If the model can plan, no planner.

模型会规划了，就不需要规划器。

If the model is coherent at long horizons, no context resets.

模型在长时程上保持连贯了，就不需要上下文重置。

And yes, Opus 4.6 largely killed the context-anxiety failure mode (Sonnet 4.5 used to wrap up work prematurely as it approached what it thought was its context limit), which means a whole class of anxiety-mitigation scaffolding I was writing six months ago is now dead code.

而且没错，Opus 4.6 基本消灭了「上下文焦虑」这种失败模式（Sonnet 4.5 曾会在接近它自以为的上下文上限时过早收尾），这意味着我六个月前还在写的一整类焦虑缓解脚手架，如今成了死代码。

But the ceiling moved with the model.

但天花板随着模型一起挪高了。

Tasks that were unreachable are in play, and they have their own failure modes.

原本够不着的任务如今进了赛场，而它们有自己的失败模式。

The anxiety scaffolding goes away, and in its place you need a multi-day memory policy, or a harness that coordinates three specialized agents, or evaluators for design quality in generated UIs.

焦虑脚手架退场了，取而代之，你需要一套跨多天的记忆策略，或一个能协调三个专职智能体的 harness，或针对生成式 UI 设计质量的评估器。

The assumptions shift, and so does the scaffolding that encodes them.

假设变了，编码这些假设的脚手架也随之改变。

Anthropic puts it cleanly: *“every component in a harness encodes an assumption about what the model can’t do on its own.”*

Anthropic 说得很干净：*「harness 里的每个组件，都编码了一条关于模型自己做不到什么的假设。」*

When the model gets better at something, that component becomes load-bearing for nothing and should come out.

当模型在某方面变强，对应的组件就不再承重，应当拆除。

When the model unlocks something new, new scaffolding is needed to reach the new ceiling.

当模型解锁新能力，就需要新的脚手架去够到新的天花板。

### The model-harness training loop｜模型—harness 训练循环

The other thing that’s happening, which Viv names explicitly, is a feedback loop between harness design and model training.

另一件正在发生、且被 Viv 明确点名的事，是 harness 设计与模型训练之间的反馈循环。

![The model-harness training loop. A useful primitive is discovered in the harness, standardized into the product, used when training the next generation of models, and the next model improves at using that primitive. Cycle repeats.](https://addyosmani.com/assets/images/harness-training-loop.jpeg)

> 图注：模型—harness 训练循环。一个有用的原语在 harness 里被发现，被标准化进产品，在训练下一代模型时被使用，于是下一代模型更擅长使用该原语。循环往复。

Today’s agent products are post-trained with harnesses in the loop.

今天的智能体产品是在 harness 参与下做后训练的。

The model gets specifically better at the actions the harness designers think it should be good at: filesystem operations, bash, planning, subagent dispatch.

模型会专门在 harness 设计者认为它该擅长的动作上变强：文件系统操作、bash、规划、子智能体分发。

That’s why Opus 4.6 feels different inside Claude Code than inside someone else’s harness, and it’s why changing a tool’s logic sometimes causes strange regressions.

这就是为什么 Opus 4.6 在 Claude Code 里的手感和在别人的 harness 里不一样，也是为什么改动某个工具的逻辑有时会引发奇怪的回归。

A genuinely general model wouldn’t care whether you used `apply_patch` or `str_replace`, but co-training creates overfitting.

一个真正通用的模型不会在乎你用 `apply_patch` 还是 `str_replace`，但协同训练造成了过拟合。

The practical implication is twofold.

实践上的启示有两层。

**A harness is a living system, not a config file you set up once.**

**harness 是一个活的系统，不是一次配置完就了事的配置文件。**

And the “best” harness isn’t necessarily the one the model was trained inside; it’s the one designed for your task.

而且「最好的」harness 未必是模型在其中训练出来的那一个，而是为你的任务量身设计的那一个。

Viv’s Top 30 to Top 5 Terminal Bench jump is the clearest proof point I’ve seen.

Viv 团队在 Terminal Bench 上从 Top 30 跃至 Top 5，就是我见过的最清晰的实证。

---

## Harness-as-a-Service｜Harness 即服务

Viv’s other contribution is the **[HaaS](https://www.vtrivedy.com/posts/claude-code-sdk-haas-harness-as-a-service)** framing: Harness-as-a-Service.

Viv 的另一个贡献是 **[HaaS](https://www.vtrivedy.com/posts/claude-code-sdk-haas-harness-as-a-service)** 这个框架：Harness-as-a-Service（harness 即服务）。

The observation is that we’re moving from building on LLM APIs (which give you a completion) to building on harness APIs (which give you a runtime).

其观察是：我们正从基于 LLM API 构建（它给你的是一次补全），转向基于 harness API 构建（它给你的是一个运行时）。

The Claude Agent SDK, the Codex SDK, and the OpenAI Agents SDK all point in the same direction.

Claude Agent SDK、Codex SDK 和 OpenAI Agents SDK 全都指向同一个方向。

You get the loop, the tools, the context management, the hooks, and the sandbox primitives out of the box, and you customize them.

循环、工具、上下文管理、hooks、沙箱原语全部开箱即得，你要做的是在此之上做定制。

The shift matters because the default path used to be: build your own loop, wire up your own tool-calling, handle your own conversation state, invent your own approval flow.

这个转变之所以重要，是因为过去的默认路径是：自建循环、自接工具调用、自管会话状态、自造审批流程。

Now the default path is: pick a harness framework, configure it along the four pillars (system prompt, tools, context, subagents), and put the rest of your effort into domain-specific prompt and tool design.

现在的默认路径是：挑一个 harness 框架，沿四大支柱（系统提示词、工具、上下文、子智能体）做配置，把剩下的精力都投入领域特定的提示词与工具设计。

That’s what makes “skill issue” tractable.

这正是「skill issue」变得可解的原因。

You’re not rebuilding an agent from scratch every time something goes wrong.

不是每次出问题都从零重建一个智能体。

You’re tuning a configuration surface that’s already well-factored.

而是在调优一个已经被良好分解的配置面。

Viv’s line on this is also the best argument for starting messy: *“good agent building is an exercise in iteration. You can’t do iterations if you don’t have a v0.1.”*

Viv 关于这一点的那句话，也是「先乱着开干」的最佳论据：*「好的智能体构建是一场迭代练习。没有 v0.1，你就无从迭代。」*

---

## Where this is going｜这一切正走向何方

Look at the top coding agents side by side (Claude Code, Cursor, Codex, Aider, Cline) and **they look more like each other than their underlying models do.**

把头部编程智能体并排看一遍（Claude Code、Cursor、Codex、Aider、Cline），**它们彼此之间的相似程度，比它们底层模型之间的相似程度还高。**

The models are different.

模型各不相同。

The harness patterns are converging.

harness 模式却在收敛。

I don’t think that’s an accident.

我不认为这是偶然。

It’s the industry slowly finding the load-bearing pieces of scaffolding that turn a generative model into something that can ship.

这是整个行业在慢慢找出那些真正承重的脚手架部件——正是它们把一个生成式模型变成能交付东西的系统。

Viv’s framing of the open problems is the one I find most exciting: orchestrating many agents working in parallel on a shared codebase; agents that analyze their own traces to identify and fix harness-level failure modes; harnesses that dynamically assemble the right tools and context just-in-time for a given task instead of being pre-configured at startup.

Viv 对开放问题的梳理是我觉得最令人兴奋的：编排许多智能体在共享代码库上并行工作；让智能体分析自己的 trace，以识别并修复 harness 层面的失败模式；让 harness 针对给定任务即时（just-in-time）动态组装合适的工具与上下文，而不是在启动时就预先配置好。

That last one, in particular, feels like **where harnesses stop being static config and start becoming something closer to a compiler.**

尤其是最后一条，感觉正是 **harness 不再是静态配置、开始变得更接近一个编译器的地方。**
