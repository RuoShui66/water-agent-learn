# 07_Long-running Agents_长时程智能体

> 原文：https://addyosmani.com/blog/long-running-agents/
> 作者：Addy Osmani｜发布日期：2026-04-28

## 📌 本篇速览

- 📅 2026-04-28　｜　📄 约 4,200 词
- ⭐ ★★★★☆ **值得读，独特价值在「横向对照」** —— 这是少有的把 **Anthropic / Cursor / Google 三家的长时程架构摆在一起比**的公开材料，能直接看出「架构趋同、命名各异」。三堵墙 + 五种生产模式可以当设计检查表。
- 🏷 三堵墙、Ralph loop、brain/hands/session、planner/worker/judge、memory drift、checkpoint-and-resume
- 🗂 [返回专题目录](00_目录.md)

本文先厘清「long-running」的三重含义（长时程推理 / 长时程执行 / 持久能动性），指出所有长时程智能体都会撞上的三堵墙（有限上下文、无持久状态、无自我验证），然后横向对照 Anthropic（harness 与 brain/hands/session 拆分）、Cursor（planner/worker/judge）、Google（Gemini Enterprise Agent Platform）三家的架构方案，总结五种生产环境设计模式，最后给出「今天该怎么落地」的分场景建议与当前仍未解决的局限。

---

**A long-running AI agent can keep making progress over hours, days, or weeks.**

**长时程运行（long-running）的 AI 智能体能够在数小时、数天甚至数周的时间里持续推进任务。**

**It can do this across many context windows and sandboxes, recover from failure, leave structured artifacts behind, and resume where it left off.**

**它可以跨越多个上下文窗口和沙箱来做到这一点：从失败中恢复、留下结构化的产物（artifacts），并从上次中断的地方继续。**

---

For two years the dominant image of an "AI agent" has been a chat window with a clever loop in it.

两年来，「AI 智能体」的主流形象一直是一个内嵌了聪明循环的聊天窗口。

You type a goal, the agent calls some tools, you watch tokens stream by, you stop watching when the work runs out of patience or the context window fills up.

你输入一个目标，智能体调用一些工具，你盯着 token 一行行流过，直到任务耗尽了耐心，或者上下文窗口被填满，你才不再盯着看。

That paradigm got us a long way, but it has a ceiling.

这个范式带我们走了很远，但它有天花板。

The model forgets.

模型会遗忘。

It declares "task complete" when it isn't.

任务明明没完成，它却宣布「任务已完成」。

It re-introduces a bug it fixed nine turns ago.

它会把九轮之前修好的 bug 重新引入回来。

The whole thing is structured around a single sitting.

整个系统的结构都是围绕「一次性坐下来干完」设计的。

Long-running agents are what comes next.

长时程智能体就是接下来的方向。

The idea is easy to state: an agent that keeps making forward progress on a goal across many sessions and many sandboxes, possibly many days or weeks, while leaving the workspace clean enough that the next session can pick up where the last one left off.

这个想法说起来很简单：一个智能体，能跨越许多会话和许多沙箱——可能是数天甚至数周——持续朝一个目标推进，同时把工作区保持得足够整洁，让下一个会话能从上一个会话中断的地方接着干。

The engineering is harder.

但工程实现要难得多。

You have to solve for persistence, recovery, and verification in a way that doesn't just paper over the cracks.

你必须真正解决持久化（persistence）、恢复（recovery）和验证（verification）这三个问题，而不是只把裂缝糊起来。

You have to build a state layer that lives outside the model's context window, and you have to design the handoff between sessions so the agent doesn't lose its mind when it wakes up and finds itself in a different sandbox with a different context window.

你必须构建一个活在模型上下文窗口之外的状态层，还要设计好会话之间的交接（handoff），这样智能体醒来时发现自己身处不同的沙箱、面对不同的上下文窗口，才不至于精神错乱。

This post is my attempt to lay out what's changed, who's pushing on it, and how an engineer can use long-running agents today without writing the whole thing from scratch.

这篇文章是我的一次尝试：讲清楚发生了什么变化、谁在推动这件事，以及一名工程师今天如何用上长时程智能体，而不必从零开始把整套东西写一遍。

---

## What "long-running" actually means｜「长时程」到底是什么意思

"Long-running" gets used to mean at least three different things in practice, and it helps to keep them separate.

「long-running」在实践中至少被用来指三件不同的事，把它们分开来看会很有帮助。

**Long-horizon reasoning.** The agent has to plan and execute over many dependent steps.

**长时程推理（Long-horizon reasoning）。**智能体必须在许多步步相依的环节上做规划和执行。

This is mostly a model-quality story: coherence, planning, the ability to recover from a wrong turn ten steps ago.

这主要是一个模型质量的故事：连贯性、规划能力、从十步之前走错的岔路上恢复过来的能力。

METR has been tracking this with their *time horizon* metric, which estimates how long a task a frontier model can complete with 50% reliability.

METR 一直在用他们的*时间跨度*（time horizon）指标追踪这件事——该指标估算前沿模型能以 50% 可靠性完成的任务时长。

The headline finding is that the metric has been [doubling roughly every seven months](https://metr.org/time-horizons/) since 2019, and their [TH1.1 update](https://metr.org/blog/2026-1-29-time-horizon-1-1/) earlier this year doubled the count of 8-hour-plus tasks in the eval set.

最抢眼的发现是：自 2019 年以来，这个指标[大约每七个月翻一番](https://metr.org/time-horizons/)；而他们今年早些时候的 [TH1.1 更新](https://metr.org/blog/2026-1-29-time-horizon-1-1/)，把评测集中 8 小时以上任务的数量翻了一倍。

**If that curve holds, frontier agents complete tasks at the day scale by 2028 and the year scale by 2034.**

**如果这条曲线延续下去，前沿智能体将在 2028 年达到「天」级任务、2034 年达到「年」级任务。**

**Long-running execution.** The agent's *process* runs for hours or days.

**长时程执行（Long-running execution）。**智能体的*进程*要运行数小时或数天。

Maybe it's a coding job, maybe it's a research sweep, maybe it's a 24/7 monitoring service.

也许是一个编码任务，也许是一次研究扫描，也许是一个 7×24 小时的监控服务。

The model might be invoked thousands of times across the run.

在整个运行过程中，模型可能被调用成千上万次。

This is mostly a *harness* story, and it's the one this post is mostly about.

这主要是一个 *harness*（执行框架）的故事，也是本文主要讨论的那一种。

**Persistent agency.** The agent has an identity that outlives any single task.

**持久能动性（Persistent agency）。**智能体拥有一个超越任何单次任务而存在的身份。

It accumulates memory, learns user preferences, and is always available.

它会累积记忆、学习用户偏好，并且随时可用。

This is the [Memory Bank](https://docs.cloud.google.com/agent-builder/agent-engine/memory-bank/overview) flavor of long-running.

这是 [Memory Bank](https://docs.cloud.google.com/agent-builder/agent-engine/memory-bank/overview)（记忆库）这一流派的「长时程」。

In practice the three blur together.

在实践中，这三者会混在一起。

A real production agent does long-horizon reasoning *inside* a long-running execution *backed by* persistent agency.

一个真正的生产级智能体，是在长时程执行*之内*做长时程推理，*背后*再由持久能动性支撑。

But the engineering problems are different in each, and so are the products that solve them.

但三者的工程问题各不相同，解决它们的产品也各不相同。

---

## Why this matters｜为什么这件事重要

There are two reasons I believe this work matters a lot right now.

我认为这项工作在当下非常重要，理由有两个。

The first is a phase change in what's economically feasible to delegate.

第一，「哪些工作在经济上值得委派」正在发生相变（phase change）。

An agent that runs for ten minutes can answer a question, summarize a doc, fix a small bug.

一个运行十分钟的智能体，能回答一个问题、总结一份文档、修一个小 bug。

An agent that runs for ten hours can own an entire feature, finish a migration that was on the backlog for six quarters, or do the kind of overnight research sweep that used to require a junior analyst.

而一个运行十小时的智能体，可以「拥有」一整个功能特性、完成一项在待办清单上躺了六个季度的迁移，或者做那种过去需要一名初级分析师才能完成的通宵研究扫描。

One of Anthropic's [Claude Sonnet announcements](https://www.anthropic.com/news/claude-sonnet-4-5) put concrete numbers on this last fall: 30+ hours of autonomous coding in internal tests, including [one run](https://venturebeat.com/ai/anthropics-new-claude-can-code-for-30-hours-think-of-it-as-your-ai-coworker) that produced an 11,000-line Slack-style app.

去年秋天，Anthropic 的一次 [Claude Sonnet 发布](https://www.anthropic.com/news/claude-sonnet-4-5)给这件事标上了具体数字：内部测试中实现了 30+ 小时的自主编码，其中[一次运行](https://venturebeat.com/ai/anthropics-new-claude-can-code-for-30-hours-think-of-it-as-your-ai-coworker)产出了一个 1.1 万行代码的类 Slack 应用。

**That's already past the threshold where the answer to "should I delegate this?" is no longer obvious.**

**这已经越过了那个临界点——「这件事该不该委派给智能体？」的答案不再是显而易见的了。**

The second is that persistence changes what the agent *is*.

第二，持久化改变了智能体的*本质*。

A stateless agent answers your question and disappears.

一个无状态的智能体回答完你的问题就消失了。

A long-running one accumulates context: which competitor moved which way last week, which test flaked twice on Tuesday, what you usually mean by "the dashboard."

而一个长时程运行的智能体会累积上下文：上周哪个竞争对手朝哪个方向动了、周二哪个测试闪断（flake）了两次、你说「那个 dashboard」的时候通常指的是什么。

Anthropic's [Project Vend](https://www.anthropic.com/research/project-vend-1) was the most public early demonstration of this.

Anthropic 的 [Project Vend](https://www.anthropic.com/research/project-vend-1) 是这方面最公开的早期演示。

They had a Claude instance run an actual office vending business for a month, managing inventory, setting prices, talking to suppliers.

他们让一个 Claude 实例真的经营了一个月的办公室自动售货生意：管理库存、定价、和供应商沟通。

It failed in informative ways, and [the second phase](https://www.anthropic.com/research/project-vend-2) ran much better, but the point wasn't profitability.

它以富有信息量的方式失败了，[第二阶段](https://www.anthropic.com/research/project-vend-2)运转得好了很多，但重点从来不是盈利。

The point was watching what kinds of weird coherence problems show up when an agent has to maintain identity across weeks instead of turns.

重点是观察：当一个智能体必须以「周」而不是「轮次」为单位维持身份时，会冒出哪些诡异的连贯性问题。

Those are the same problems every team building production agents now hits.

而这些问题，正是如今每个构建生产级智能体的团队都会撞上的问题。

---

## The three walls every long-running agent hits｜每个长时程智能体都会撞上的三堵墙

Three walls show up in basically every write-up I've read this year.

在我今年读过的几乎每一篇相关文章里，都会出现这三堵墙。

**Finite context.** Even a 1M-token window fills.

**有限上下文（Finite context）。**即使是 100 万 token 的窗口也会被填满。

And [context rot](https://addyosmani.com/blog/agent-harness-engineering/), the steady degradation of model performance as the window gets full, kicks in well before the hard limit.

而且[上下文腐烂](https://addyosmani.com/blog/agent-harness-engineering/)（context rot）——即随着窗口逐渐填满、模型表现持续退化的现象——早在触及硬上限之前就已经发作了。

A 24-hour run is not going to fit in any context window the field has on its roadmap.

一次 24 小时的运行，装不进这个领域路线图上的任何一个上下文窗口。

Something has to give.

必须有什么东西做出让步。

**No persistent state.** A new session starts blank.

**无持久状态（No persistent state）。**新会话从一片空白开始。

Anthropic's framing in their [scientific computing post](https://www.anthropic.com/research/long-running-Claude) is the cleanest version I've seen: *"imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift."*

Anthropic 在他们的[科学计算文章](https://www.anthropic.com/research/long-running-Claude)里给出的表述是我见过最清晰的版本：*「想象一个由轮班工程师组成的软件项目，每个新来的工程师上岗时，对上一班发生的事情毫无记忆。」*

Without an explicit persistence story, every shift change is a productivity disaster.

如果没有一套显式的持久化方案，每次换班都是一场生产力灾难。

**No self-verification.** Models reliably skew positive when they grade their own work.

**无自我验证能力（No self-verification）。**模型给自己的工作打分时，总是稳定地偏向乐观。

Asked "are you done?" they answer "yes" more often than they should.

被问到「你做完了吗？」时，它们回答「是」的频率远高于应有的水平。

Without a separate signal that the work meets a bar, you get the agent that ships at 30% complete with full confidence.

如果没有一个独立的信号来确认工作达到了标准，你得到的就是那种完成度 30% 却信心满满交付的智能体。

Long-running agent designs are mostly answers to these three problems.

长时程智能体的各种设计，大多都是对这三个问题的回答。

**The major labs have converged on similar shapes of answer, but with very different surface area.**

**各大实验室已经收敛到形状相似的答案上，只是产品表面（surface area）大不相同。**

---

## The Ralph loop: one of the simpler practitioner versions of long-running agents｜Ralph 循环：长时程智能体较简单的实践者版本之一

The **Ralph loop** (sometimes called the Ralph Wiggum technique) is one of "simpler" practitioner version of long-running agents, popularized by [Geoffrey Huntley](https://ghuntley.com/ralph/) and [Ryan Carson](https://github.com/snarktank/ralph).

**Ralph 循环**（有时也叫 Ralph Wiggum 技法）是长时程智能体较「简单」的实践者版本之一，由 [Geoffrey Huntley](https://ghuntley.com/ralph/) 和 [Ryan Carson](https://github.com/snarktank/ralph) 推广开来。

The reference implementation is [literally a bash script](https://ghuntley.com/ralph/) that loops:

它的参考实现[真的就是一个循环执行的 bash 脚本](https://ghuntley.com/ralph/)：

1. Pick the next unfinished task from a list (`prd.json` or equivalent).

1. 从任务列表（`prd.json` 或类似文件）中取出下一个未完成的任务。

2. Build a prompt with the task, the relevant context, and any persistent notes.

2. 用该任务、相关上下文和所有持久化笔记构造一个提示词。

3. Call the agent.

3. 调用智能体。

4. Run tests or other checks.

4. 运行测试或其他检查。

5. Append what happened to `progress.txt`.

5. 把发生的事情追加写入 `progress.txt`。

6. Update the task list (done, failed, blocked).

6. 更新任务列表（已完成、失败、被阻塞）。

7. Go back to step 1.

7. 回到第 1 步。

The reason it works is the same reason any of the harnesses below work: state lives outside the agent's context.

它能奏效的原因，和下文任何一个 harness 能奏效的原因相同：状态活在智能体的上下文之外。

`prd.json` is the plan, `progress.txt` is the lab notes, `AGENTS.md` is the rolling rulebook.

`prd.json` 是计划，`progress.txt` 是实验笔记，`AGENTS.md` 是滚动更新的规则手册。

**The agent itself is amnesiac, but the filesystem isn't.**

**智能体本身是失忆的，但文件系统不是。**

Each iteration starts fresh and reads enough state from disk to keep going.

每次迭代都全新开始，从磁盘上读取足够的状态就能继续干下去。

Carson's [Compound Product](https://github.com/snarktank/compound-product) extends the idea by chaining multiple loops (an analysis loop that reads daily reports, a planning loop that emits a PRD, an execution loop that writes the code), which is roughly the open-source version of the planner-generator-evaluator triad Anthropic landed on independently.

Carson 的 [Compound Product](https://github.com/snarktank/compound-product) 把这个想法进一步扩展为多个循环的串联（读每日报告的分析循环、产出 PRD 的规划循环、写代码的执行循环），这大致就是 Anthropic 独立摸索出的「规划者-生成者-评估者」三件套的开源版本。

I went deeper on all of this in [Self-improving agents](https://addyosmani.com/blog/self-improving-agents/): task list structure, progress files, QA gates, monitoring, the failure modes you'll actually hit.

我在[《Self-improving agents》](https://addyosmani.com/blog/self-improving-agents/)一文中对这一切做了更深入的展开：任务列表的结构、进度文件、QA 关卡、监控，以及你实际会撞上的各种失败模式。

The short version is that you can build a working long-running agent in an evening with a bash script and a JSON file.

简短版结论是：用一个 bash 脚本加一个 JSON 文件，你一个晚上就能搭出一个能用的长时程智能体。

Most of what Google and Anthropic have productized is the work of making this pattern recoverable, secure, and observable at scale.

Google 和 Anthropic 产品化的大部分内容，其实就是把这个模式在规模化条件下做到可恢复、安全、可观测的那些工作。

The big-lab stories below are different ways of paying for that production-readiness.

下面这些大厂的故事，就是为这种「生产就绪」付出代价的不同方式。

---

## Anthropic: harnesses, then the brain/hands/session split｜Anthropic：先有 harness，再有 brain/hands/session 拆分

Anthropic has been the most public about the engineering.

在工程细节上，Anthropic 是公开程度最高的。

Two posts are worth reading end-to-end.

有两篇文章值得从头到尾读完。

The first is ["Effective harnesses for long-running agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), which lays out a two-agent harness for autonomous full-stack development.

第一篇是[《Effective harnesses for long-running agents》](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)，它给出了一个用于自主全栈开发的双智能体 harness。

An **initializer agent** runs once at the start of a project to set up the environment, expand the prompt into a structured `feature-list.json`, and write an `init.sh` that future sessions will run on boot.

一个**初始化智能体**（initializer agent）在项目开始时运行一次：搭建环境、把提示词展开成结构化的 `feature-list.json`，并写一个供未来会话启动时运行的 `init.sh`。

A **coding agent** is then woken up over and over, each session asked to make incremental progress on one feature, run tests, leave a `claude-progress.txt` note, and commit.

然后一个**编码智能体**（coding agent）被一遍遍唤醒，每个会话被要求在一个功能上做出增量进展、运行测试、留下一份 `claude-progress.txt` 笔记，然后提交代码。

A test ratchet (*"it is unacceptable to remove or edit tests because this could lead to missing or buggy functionality"*) sits in the prompt to stop the very common failure of an agent deleting failing tests to "make them pass."

提示词里放了一个测试棘轮（test ratchet）——*「删除或修改测试是不可接受的，因为这可能导致功能缺失或有缺陷」*——用来阻止一种极其常见的失败：智能体为了「让测试通过」而删掉失败的测试。

[InfoQ's writeup](https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/) extends this into a planner, generator, and evaluator triad, on the same logic that separating generation from evaluation matters because models grade their own work too generously.

[InfoQ 的报道](https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/)把它进一步扩展成「规划者、生成者、评估者」三件套，依据的是同一个逻辑：把生成与评估分开之所以重要，是因为模型给自己的工作打分太宽松。

The second is ["Scaling Managed Agents: Decoupling the brain from the hands"](https://www.anthropic.com/engineering/managed-agents), the architectural post behind [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) (Anthropic's hosted runtime, launched in early April).

第二篇是[《Scaling Managed Agents: Decoupling the brain from the hands》](https://www.anthropic.com/engineering/managed-agents)，也就是 [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)（Anthropic 于四月初推出的托管运行时）背后的架构文章。

The argument is that an agent has three components that should be independently replaceable.

其论点是：智能体有三个组件，它们应当可以彼此独立替换。

The Brain is the model and the harness loop that calls it.

Brain（大脑）是模型以及调用它的 harness 循环。

The Hands are sandboxed, ephemeral execution environments where tools actually run.

Hands（双手）是沙箱化的、临时性的执行环境，工具真正在这里运行。

The Session is an append-only event log of every thought, tool call, and observation.

Session（会话）则是一份只追加（append-only）的事件日志，记录每一次思考、工具调用和观察。

This sounds abstract and it isn't.

这听上去很抽象，其实不然。

Anthropic's framing: *"every component in a harness encodes an assumption about what the model can't do on its own."*

Anthropic 的表述是：*「harness 中的每个组件，都编码了一条关于模型自己做不到什么的假设。」*

When you couple them, an assumption that goes stale (e.g., the model used to need an explicit planner and now plans natively) means the whole system has to change at once.

当这些组件耦合在一起时，一条假设过时了（比如模型过去需要显式的规划器、现在能原生规划了），就意味着整个系统必须一次性全部改动。

When you decouple them, the harness becomes stateless, sandboxes become *cattle, not pets*, and a brain crash doesn't lose the run.

而当你把它们解耦后，harness 变成无状态的，沙箱变成*牲口而非宠物*（cattle, not pets），大脑崩溃也不会丢掉整个运行。

A fresh container calls `wake(sessionId)` and reconstitutes the state from the log.

一个全新的容器只需调用 `wake(sessionId)`，就能从日志中重建状态。

They reported [time-to-first-token dropped ~60% at p50 and over 90% at p95](https://www.anthropic.com/engineering/managed-agents) just from being able to start inference before the sandbox is ready.

他们报告称，仅仅因为能在沙箱就绪之前就开始推理，[首 token 时间在 p50 上下降了约 60%、在 p95 上下降了 90% 以上](https://www.anthropic.com/engineering/managed-agents)。

**The session-as-event-log idea is the part most teams underappreciate.**

**「会话即事件日志」这个想法，是大多数团队最低估的部分。**

It is what makes a long-running agent recoverable.

正是它让长时程智能体变得可恢复。

Without it, a container failure is a session failure and you're debugging into a stale snapshot.

没有它，容器故障就等于会话故障，你只能对着一份过期的快照做调试。

With it, the agent's memory is a queryable artifact that lives outside whatever process happens to be running at the moment.

有了它，智能体的记忆就成了一个可查询的产物，独立于此刻恰好在运行的任何进程而存在。

For the scientific computing crowd, Anthropic's [long-running Claude post](https://www.anthropic.com/research/long-running-Claude) reduces all of this to a simpler stack: `CLAUDE.md` as a living plan the agent edits as it learns, `CHANGELOG.md` as portable lab notes, `tmux` plus `SLURM` plus `git` as the execution and coordination layer, and the **Ralph loop**, a `for` loop that kicks the agent back into context whenever it claims completion and asks if it's *really* done.

面向科学计算人群，Anthropic 的[长时程 Claude 文章](https://www.anthropic.com/research/long-running-Claude)把这一切简化为一个更朴素的技术栈：`CLAUDE.md` 作为智能体边学边改的「活计划」，`CHANGELOG.md` 作为可携带的实验笔记，`tmux` 加 `SLURM` 加 `git` 作为执行与协调层，再加上 **Ralph 循环**——一个 `for` 循环，每当智能体声称完成时就把它踢回上下文里，追问它是不是*真的*做完了。

Their flagship case study is a Boltzmann solver Claude Opus 4.6 built over a few days that reached sub-percent agreement with a reference CLASS implementation.

他们的旗舰案例研究，是 Claude Opus 4.6 用几天时间构建的一个玻尔兹曼求解器（Boltzmann solver），其结果与参考的 CLASS 实现达到了误差小于 1% 的一致性。

Months-to-years of researcher time, compressed.

数月乃至数年的研究者时间，被压缩了。

Same patterns across all three posts: an explicit plan file, an explicit progress file, structured handoffs between sessions, separate generation from evaluation, and a loop that refuses to let the agent stop early.

三篇文章贯穿着同样的模式：一份显式的计划文件、一份显式的进度文件、会话之间的结构化交接、生成与评估分离，以及一个拒绝让智能体提前收工的循环。

---

## Cursor: planners, workers, judges｜Cursor：规划者、执行者、评判者

[Cursor's "Scaling long-running autonomous coding"](https://cursor.com/blog/scaling-agents) is the other essential read this year.

[Cursor 的《Scaling long-running autonomous coding》](https://cursor.com/blog/scaling-agents)是今年另一篇必读文章。

They walked into walls that Anthropic mostly papered over.

Anthropic 大多一笔带过的那些墙，他们是实打实撞上去的。

Their first attempt was a flat coordination model: equal-status agents writing to shared files with locks.

他们的第一次尝试是一个扁平的协调模型：地位平等的智能体带锁写入共享文件。

It became a bottleneck and made the agents risk-averse, churning rather than committing.

结果它成了瓶颈，还让智能体变得规避风险——空转折腾而不敢提交。

Their second attempt swapped locks for optimistic concurrency control, which removed the bottleneck but didn't fix the coordination problem.

第二次尝试用乐观并发控制（optimistic concurrency control）换掉了锁，瓶颈消除了，但协调问题并没有解决。

The third design is what's running in production now and what they describe as solving most of the problem:

第三版设计就是现在跑在生产环境里的那一版，他们描述它解决了大部分问题：

- **Planners** continuously explore the codebase and emit tasks. They can recursively spawn sub-planners.

- **规划者（Planners）**持续探索代码库并产出任务。它们可以递归派生子规划者。

- **Workers** are focused executors. They don't coordinate with each other and they don't worry about the big picture.

- **执行者（Workers）**是专注的执行单元。它们彼此之间不做协调，也不操心全局大图。

- **Judges** decide when an iteration is finished and when to restart.

- **评判者（Judges）**决定一次迭代何时算完成、何时该重启。

Two things stand out from the post.

这篇文章里有两点格外突出。

One: *"a surprising amount of the system's behavior comes down to how we prompt the agents"* more than the harness or the model.

第一：*「系统行为中出人意料的一大部分，取决于我们如何给智能体写提示词」*——比 harness 或模型的影响还大。

Two: different models slot into different roles.

第二：不同的模型适配不同的角色。

Their reported finding is that a GPT model was better than Opus for *extended autonomous work* specifically because Opus tended to stop early and take shortcuts.

他们报告的发现是：在*长时间自主工作*上，某个 GPT 模型比 Opus 更好，具体原因是 Opus 倾向于提前停手、走捷径。

**Same task, different role, different model.**

**同一个任务，不同的角色，用不同的模型。**

The matching is becoming part of the design surface.

「模型与角色的匹配」正在成为设计界面（design surface）的一部分。

This pairs with [Composer 2](https://cursor.com/blog/composer) (their proprietary frontier coding model that ships in [Cursor 3](https://cursor.com/changelog/2-0)) and their **background cloud agents**: long-running tasks that run on Anysphere's cloud infrastructure rather than your laptop.

与之配套的是 [Composer 2](https://cursor.com/blog/composer)（他们自研的前沿编码模型，随 [Cursor 3](https://cursor.com/changelog/2-0) 发布）和他们的**后台云端智能体**（background cloud agents）：长时程任务跑在 Anysphere 的云基础设施上，而不是你的笔记本上。

Eight-hour refactors and codebase-wide migrations survive a closed lid.

八小时的重构和全代码库范围的迁移，合上笔记本盖子也不会中断。

You can start a task locally, hit *run in cloud* when you realize it'll take 30 minutes, and re-attach later from your phone.

你可以在本地启动一个任务，意识到它要花 30 分钟时点一下*在云端运行*，稍后再从手机上重新接入。

Each agent runs in an isolated git worktree and merges back via PR.

每个智能体都运行在一个隔离的 git worktree 里，通过 PR 合并回主干。

The handoff between local and remote is the part most teams haven't figured out yet, and Cursor's bet is that it has to be its own product surface.

本地与远程之间的交接，是大多数团队还没想明白的部分；而 Cursor 押注的是：这必须成为一个独立的产品界面。

The shape ends up close to Anthropic's: roles are split, sessions are durable, judges sit beside the worker, and a long task runs in a cloud sandbox with git as the coordination substrate.

最终的形态与 Anthropic 的很接近：角色被拆分、会话是持久的、评判者伴在执行者身旁，长任务跑在云端沙箱里，以 git 作为协调基底。

---

## Google: long-running agents on the Agent Platform｜Google：Agent Platform 上的长时程智能体

Google's announcement at [Cloud Next '26](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform) two weeks ago folded Vertex AI into the **Gemini Enterprise Agent Platform** and turned long-running agents into a named product, with named SLAs.

两周前，Google 在 [Cloud Next '26](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform) 上宣布把 Vertex AI 并入 **Gemini Enterprise Agent Platform**，把长时程智能体变成了一个有正式名字的产品，还带着有正式名字的 SLA。

The pieces that matter for this post:

与本文相关的几个组件：

- **Agent Runtime** supports agents that *"run autonomously for days at a time"* with sub-second cold starts and on-demand sandbox provisioning. The launch post's example use case is a sales prospecting sequence that takes a week to play out, which is roughly the right shape for it.

- **Agent Runtime** 支持*「一次自主运行数天」*的智能体，具备亚秒级冷启动和按需沙箱供给。发布文章给的示例用例是一个需要一周才能走完的销售线索开发流程，这大致就是它适配的任务形状。

- **Agent Sessions** persist conversation and event history. You can pin them to a custom session ID that maps to your own CRM or DB record, so the agent's state lives next to the business state instead of in a separate AI silo.

- **Agent Sessions** 持久化对话与事件历史。你可以把它们钉在一个自定义会话 ID 上，映射到你自己的 CRM 或数据库记录，这样智能体的状态就挨着业务状态存放，而不是躺在一个独立的 AI 数据孤岛里。

- **[Agent Memory Bank](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank)** is the persistent long-term memory layer, generally available as of Next '26. It curates memories from sessions, scopes them to a user identity, and exposes a search API so the next agent invocation can pull what's relevant. Payhawk reported that auto-submitting expenses through a Memory-Bank-backed agent cut submission time by over 50%.

- **[Agent Memory Bank](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank)** 是持久化的长期记忆层，自 Next '26 起正式可用（GA）。它从会话中提炼记忆、把记忆限定到某个用户身份的范围内，并暴露一个搜索 API，让下一次智能体调用可以拉取相关内容。Payhawk 报告称，通过一个由 Memory Bank 支撑的智能体自动提交报销，把提交时间缩短了 50% 以上。

- **Agent Sandbox** handles hardened code execution.

- **Agent Sandbox** 负责经过安全加固的代码执行。

- **Agent-to-Agent Orchestration**, **Agent Registry**, **Agent Identity**, **Agent Gateway**, **Agent Observability**, and **Agent Simulation** cover basically every operational concern you'd otherwise build by hand for a production fleet, including the cryptographic-identity-and-audit-log story enterprises actually need to ship.

- **Agent-to-Agent Orchestration**（智能体间编排）、**Agent Registry**（注册中心）、**Agent Identity**（身份）、**Agent Gateway**（网关）、**Agent Observability**（可观测性）和 **Agent Simulation**（仿真）基本覆盖了你原本需要为生产级智能体舰队手工搭建的所有运维关切，包括企业真正上线所需的密码学身份与审计日志那一整套。

Architecturally this is the same brain/hands/session split Anthropic described, just productized at platform scale and bundled with [ADK](https://google.github.io/adk-docs/) (the code-first dev kit) and Agent Studio (the visual one).

从架构上看，这就是 Anthropic 描述的那套 brain/hands/session 拆分，只是被产品化到了平台规模，并与 [ADK](https://google.github.io/adk-docs/)（代码优先的开发套件）和 Agent Studio（可视化的那个）捆绑在一起。

If you're building inside Google Cloud, you don't have to design a session log or a memory store from scratch anymore.

如果你在 Google Cloud 里构建，你不再需要从零设计会话日志或记忆存储。

You wire an ADK agent into Memory Bank and Sessions, deploy onto Agent Runtime, and the persistence question is answered.

你把一个 ADK 智能体接上 Memory Bank 和 Sessions，部署到 Agent Runtime 上，持久化问题就有了答案。

Notice how much this looks like the pattern Anthropic and Cursor describe, just unbundled into named services with SLAs.

注意这与 Anthropic 和 Cursor 描述的模式何其相似——只是被拆解成了一个个带 SLA 的具名服务。

Three years ago you'd have built all of this yourself.

三年前，这一切你都得自己搭。

**Now you pick which version of "decoupled brain, hands, and session" you want to rent.**

**现在，你只需要挑选想「租」哪一家版本的「解耦的大脑、双手与会话」。**

---

## Five patterns for long-running agents in production｜生产环境长时程智能体的五种模式

Shubham Saboo and I [wrote up](https://x.com/GoogleCloudTech/status/2046989964077146490) five design patterns we've seen separate working long-running agents from demos.

Shubham Saboo 和我[写过](https://x.com/GoogleCloudTech/status/2046989964077146490)五种设计模式——据我们观察，正是它们把「能用的长时程智能体」和「演示 demo」区分开来。

They aren't Google-specific, but they map cleanly onto the primitives Agent Runtime now exposes, so it's worth walking through them here in shortened form.

这些模式并非 Google 专属，但它们与 Agent Runtime 现在暴露的原语（primitives）能干净地对应上，所以值得在这里用简化的形式过一遍。

**Checkpoint-and-resume.** The most common multi-day failure is context loss.

**检查点与恢复（Checkpoint-and-resume）。**跨天任务最常见的失败是上下文丢失。

An agent processes 200 documents over four hours, hits an error on document 201, and without a checkpoint you start from scratch.

一个智能体花四个小时处理了 200 份文档，在第 201 份上遇到错误——没有检查点的话，你就得从头再来。

Treat the agent like a long-running server process: write intermediate state to disk, checkpoint every N units of work, recover from failures.

把智能体当成一个长时间运行的服务器进程来对待：把中间状态写到磁盘、每 N 个工作单元打一个检查点、从失败中恢复。

The Agent Runtime sandbox gives you a persistent filesystem, but choosing the right checkpoint granularity (not every step, not only the end) is on you.

Agent Runtime 的沙箱给了你一个持久化文件系统，但选择正确的检查点粒度（不是每一步都打，也不是只在最后打）是你自己的责任。

**Delegated approval (human-in-the-loop).** Most "human-in-the-loop" implementations are: serialize state to JSON, fire a webhook, hope someone responds.

**委托审批（Delegated approval，即人在环中 human-in-the-loop）。**大多数「人在环中」的实现是：把状态序列化成 JSON，发一个 webhook，然后祈祷有人回应。

The state goes stale, the notification gets buried, the agent re-deserializes into a slightly different world.

结果状态过期了，通知被淹没了，智能体反序列化回来时已经身处一个略有不同的世界。

Long-running runtimes let the agent pause in place with full execution state intact: reasoning chain, working memory, tool history, pending action.

而长时程运行时允许智能体原地暂停、完整保留执行状态：推理链、工作记忆、工具历史、待执行的动作。

Hours of human time pass, the agent consumes zero compute, and it resumes with sub-second latency.

人类那边过去了几个小时，智能体消耗零计算资源，然后以亚秒级延迟恢复运行。

Mission Control is Google's inbox for this.

Mission Control 就是 Google 为此提供的收件箱。

The pattern works regardless of vendor.

但这个模式与厂商无关，放在哪家都成立。

**Memory-layered context.** A seven-day agent needs more than session state.

**分层记忆上下文（Memory-layered context）。**一个运行七天的智能体需要的不只是会话状态。

Memory Bank handles long-term curated memory, Memory Profiles add low-latency lookups, and the failure mode you'll hit in production is **memory drift**: the agent learns a procedural shortcut from a few atypical interactions and starts applying it broadly.

Memory Bank 负责长期的精选记忆，Memory Profiles 增加低延迟查询，而你在生产环境会撞上的失败模式是**记忆漂移**（memory drift）：智能体从少数几次非典型交互中学到一条流程捷径，然后开始到处滥用它。

**Govern memory like you govern microservices.**

**像治理微服务一样治理记忆。**

Agent Identity controls who can read and write which banks.

Agent Identity 控制谁能读写哪些记忆库。

Agent Registry tracks which version of which agent is running.

Agent Registry 追踪哪个智能体的哪个版本正在运行。

Agent Gateway enforces policy on the wire.

Agent Gateway 在通信链路上强制执行策略。

The auditing question stops being "what are my agents doing?" and becomes "what are my agents remembering, and how is that changing their behavior?"

审计问题不再是「我的智能体在干什么？」，而变成「我的智能体在记住什么，这些记忆又如何改变了它们的行为？」

**Ambient processing.** Not every long-running agent talks to a human.

**环境式处理（Ambient processing）。**并非每个长时程智能体都和人对话。

Some sit on a Pub/Sub stream or a BigQuery table and act on events as they arrive: content moderation, anomaly detection, inbox triage.

有些智能体守着一条 Pub/Sub 流或一张 BigQuery 表，随事件到来而行动：内容审核、异常检测、收件箱分拣。

The architectural decision worth making early is to not hardcode policy into the agent.

值得尽早做出的架构决策是：不要把策略硬编码进智能体。

Define it in the Gateway and the fleet picks up policy changes without redeploys.

把策略定义在 Gateway 里，整个舰队无需重新部署就能感知到策略变化。

Ambient agents run unsupervised for long stretches, and the only sane way to update a hundred of them is to update the policy layer once.

环境式智能体会长时间无人监督地运行，要更新一百个这样的智能体，唯一理智的办法是只更新一次策略层。

**Fleet orchestration.** In real systems, you rarely have one agent.

**舰队编排（Fleet orchestration）。**在真实系统中，你很少只有一个智能体。

A coordinator delegates sub-tasks to specialists (a Lead Researcher Agent, a Scoring Agent, an Outreach Agent), each running independently for different durations.

一个协调者把子任务委派给各个专家（首席研究员智能体、打分智能体、外联智能体），每个专家独立运行、时长各异。

Each specialist gets its own Identity (so the Outreach Agent can't read financial data meant for Scoring), its own policy enforcement, its own Registry entry.

每个专家都有自己的 Identity（这样外联智能体就读不到只给打分智能体看的财务数据）、自己的策略执行、自己的 Registry 条目。

This is the same coordinator/worker shape distributed systems have used for decades.

这就是分布式系统沿用了几十年的协调者/工作者（coordinator/worker）形态。

What's new is that ADK handles it declaratively with graph-based workflows, and a bad deployment in one specialist doesn't cascade to the others.

新东西在于：ADK 用基于图的工作流以声明式方式处理这一切，而且某个专家的一次糟糕部署不会级联影响到其他专家。

The patterns compose.

这些模式是可以组合的。

A compliance system might use checkpointing for document processing, delegated approval for review gates, memory layering for cross-session knowledge, and fleet orchestration to coordinate the specialists.

一个合规系统可能用检查点做文档处理、用委托审批做评审关卡、用分层记忆做跨会话知识、用舰队编排来协调各个专家。

The opening question is always the same: *what's the longest uninterrupted unit of work your agent needs to perform?*

开局的问题永远是同一个：*你的智能体需要执行的最长不间断工作单元是多长？*

Minutes, and you don't need long-running agents.

如果是分钟级，你根本不需要长时程智能体。

Hours or days, and these patterns are where to start.

如果是小时级或天级，这些模式就是你的起点。

The [full write-up with code samples](https://x.com/GoogleCloudTech/status/2046989964077146490) covers each pattern in depth.

[带代码示例的完整版文章](https://x.com/GoogleCloudTech/status/2046989964077146490)对每个模式都有深入展开。

---

## So how do you actually build one today?｜那么，今天到底该怎么造一个？

This is the practical question and it has a different answer depending on what you're building.

这是最实际的问题，而答案取决于你在构建什么。

**You're a developer who wants long-running coding work on your own repo.** Just use [Claude Code](https://addyosmani.com/blog/agent-harness-engineering/) (or Antigravity, Cursor, or Codex).

**你是一名开发者，想在自己的仓库上跑长时程编码工作。**直接用 [Claude Code](https://addyosmani.com/blog/agent-harness-engineering/)（或者 Antigravity、Cursor、Codex）就好。

The harness is already there.

harness 已经现成摆在那里了。

Treat your `AGENTS.md` like a pilot's checklist: short, every line earned by a real failure.

把你的 `AGENTS.md` 当成飞行员检查单来对待：要短，每一行都得是由一次真实的失败换来的。

Add hooks for typecheck and lint that surface failures back to the agent.

添加类型检查和 lint 的钩子（hooks），把失败信息回传给智能体。

Write a plan file before the agent starts.

在智能体启动之前先写好一份计划文件。

Use [the Ralph loop](https://addyosmani.com/blog/self-improving-agents/) when the agent claims it's done and you don't believe it.

当智能体声称做完了而你并不相信时，用上 [Ralph 循环](https://addyosmani.com/blog/self-improving-agents/)。

For multi-hour or overnight jobs, run in a worktree so a closed laptop doesn't kill the run, and have it commit progress every meaningful unit of work.

对于数小时或过夜的任务，在 worktree 里运行——这样合上笔记本不会杀掉任务——并让它在每个有意义的工作单元后提交进度。

**This is the path most people should take, and it's where the most leverage is right now.**

**这是大多数人应该走的路，也是当下杠杆最大的地方。**

**You're building a hosted agent product.** Don't build the runtime.

**你在构建一个托管的智能体产品。**别自己造运行时。

Pick a managed one.

挑一个托管方案。

The three real options today: [Google's Agent Platform](https://cloud.google.com/products/gemini-enterprise-agent-platform) (Agent Engine + Memory Bank + Sessions), [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview), or roll something on top of [ADK](https://google.github.io/adk-docs/), the [Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk), or [Codex SDK](https://platform.openai.com/docs/codex) and host it yourself.

如今真正的三个选项是：[Google 的 Agent Platform](https://cloud.google.com/products/gemini-enterprise-agent-platform)（Agent Engine + Memory Bank + Sessions）、[Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)，或者在 [ADK](https://google.github.io/adk-docs/)、[Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) 或 [Codex SDK](https://platform.openai.com/docs/codex) 之上自己搭一套并自行托管。

The trade-off is the usual one.

这里的权衡是老生常谈的那一种。

Managed gets you the brain/hands/session split, observability, identity, and an audit trail out of the box.

托管方案让你开箱即得 brain/hands/session 拆分、可观测性、身份体系和审计追踪。

Self-hosted gets you control and the ability to use weird models for weird roles (Cursor's pattern).

自托管则让你获得控制权，以及「给奇怪的角色用奇怪的模型」的能力（Cursor 的模式）。

For most teams, the right starting point is a managed runtime plus your own ADK or SDK code for the actual loop.

对大多数团队来说，正确的起点是：一个托管运行时，加上你自己用 ADK 或 SDK 写的实际循环代码。

**You're doing something autonomous and operational** (monitoring, research, ops).

**你在做某种自主运转的运营类事务**（监控、研究、运维）。

Memory Bank-style persistence is what you want, and it's the part that doesn't exist in Claude Code.

Memory Bank 式的持久化正是你需要的，而这恰恰是 Claude Code 里不存在的那部分。

ADK + Memory Bank + Cloud Run + Cloud Scheduler is the cleanest stack I've seen for "agent runs every N hours, accumulates state, alerts on a threshold."

对于「智能体每 N 小时运行一次、累积状态、越过阈值就报警」这类需求，ADK + Memory Bank + Cloud Run + Cloud Scheduler 是我见过最干净的技术栈。

This is also where Cursor's planner/worker/judge split starts to matter more than it does for IDE coding, because the work is genuinely parallel and the failure modes are different.

这也是 Cursor 的 planner/worker/judge 拆分开始比在 IDE 编码场景中更重要的地方，因为这类工作是真正并行的，失败模式也不一样。

A few things matter regardless of which path you take.

无论你走哪条路，有几件事都很重要。

*Write down the done-condition before the agent starts.*

*在智能体启动之前，先写下完成条件（done-condition）。*

This is the single highest-leverage move for long runs.

对长时程运行来说，这是杠杆最高的一个动作。

The Anthropic harness post calls it the feature list; Cursor calls it the planner's task spec.

Anthropic 的 harness 文章管它叫功能清单（feature list）；Cursor 管它叫规划者的任务规格（task spec）。

Either way, it's an external file with explicit, testable completion criteria, and it exists so the agent can't quietly redefine *done* mid-run.

不管叫什么，它都是一个带有显式、可测试完成标准的外部文件，它存在的意义就是让智能体没法在运行途中悄悄重新定义什么叫*完成*。

*Separate the evaluator from the generator.*

*把评估者与生成者分开。*

Self-grading is the failure mode.

自我打分就是那个失败模式。

A planner / worker / judge pipeline, or a generator / evaluator pair, is a real architectural pattern not a stylistic preference.

规划者/执行者/评判者流水线，或者生成者/评估者搭档，是一种真正的架构模式，而不是风格偏好。

Even if it's the same model in different roles with different prompts.

哪怕只是同一个模型戴着不同的提示词、扮演不同的角色也一样。

*Invest in the session log, not just the prompt.*

*把功夫下在会话日志上，而不只是提示词上。*

The append-only event log is what makes the agent recoverable, debuggable, and auditable.

只追加的事件日志，正是让智能体可恢复、可调试、可审计的东西。

If you can't reconstruct what the agent did in the last 24 hours from durable storage, what you have is a long-running shell script that happens to call an LLM, not a long-running agent.

如果你不能从持久存储中重建智能体过去 24 小时干了什么，那你手里的就只是一个恰好会调用大语言模型（LLM）的长时间运行的 shell 脚本，而不是一个长时程智能体。

*Treat compaction and context resets as first-class.*

*把压缩（compaction）与上下文重置当成一等公民来对待。*

Anthropic is explicit that summarization-as-compaction wasn't enough for very long jobs; they had to do full context resets where the harness tears the session down and rebuilds it from a structured handoff file.

Anthropic 明确表示，对于超长任务，「把摘要当压缩」是不够的；他们不得不做完全的上下文重置——由 harness 把会话拆掉，再从一份结构化的交接文件中重建。

It is essentially how humans onboard a new engineer.

这本质上就是人类给新工程师做入职引导的方式。

---

## There are some real limitations right now｜当下仍存在一些真实的局限

A few things are still genuinely unsolved.

有几件事至今仍是真正悬而未决的。

**Cost.** A 24-hour run with a frontier model and a few tools is not cheap.

**成本（Cost）。**用前沿模型加上几个工具跑一次 24 小时的运行，并不便宜。

Without budgets, circuit breakers, and a hard cap on tool spend, an agent can quietly burn through a week's API budget in an afternoon.

如果没有预算、熔断器（circuit breakers）和工具开销硬上限，一个智能体可以在一个下午悄无声息地烧光一周的 API 预算。

This is solvable, but it's an explicit step you have to take.

这是可以解决的，但需要你显式地去做这一步。

**Security.** A long-running agent with API keys, cloud access, and the ability to run shell commands has a much larger attack surface than a chat session.

**安全（Security）。**一个拥有 API 密钥、云访问权限、还能运行 shell 命令的长时程智能体，其攻击面比一次聊天会话大得多。

The brain/hands separation pattern matters here too: credentials should be unreachable from the sandbox where model-generated code runs, which is one of the benefits Anthropic calls out for Managed Agents.

brain/hands 分离模式在这里同样重要：凭据应当是模型生成代码所运行的沙箱触碰不到的，这也是 Anthropic 为 Managed Agents 点名列出的好处之一。

**Alignment drift.** Over many context windows, agents drift.

**对齐漂移（Alignment drift）。**跨越许多上下文窗口之后，智能体会漂移。

The original goal gets summarized, then re-summarized, then loses fidelity.

原始目标被摘要一次，再被摘要一次，然后逐渐失真。

This is the part hooks and judges exist to defend against.

钩子和评判者的存在，正是为了防御这一点。

It is also the most common reason "the agent went off and did something I didn't ask for."

这也是「智能体跑偏了，干了我没让它干的事」最常见的原因。

**Verification.** Auditing 24 hours of autonomous activity is a real human-time problem.

**验证（Verification）。**审计 24 小时的自主活动，是一个实打实的人力时间问题。

Observability and structured artifacts (PRs, commits, briefings, test runs) are how you make this tractable.

可观测性和结构化产物（PR、提交、简报、测试运行记录）是让这件事变得可处理的手段。

Without them, you're scrolling logs and you'll miss what matters.

没有它们，你就只能翻滚日志，而且一定会漏掉真正重要的东西。

**The human role.** This is the one I keep coming back to.

**人类的角色（The human role）。**这是我反复回到的一点。

Defining work crisply enough that an agent can run for a day on it is harder than doing the work yourself.

把工作定义得足够清晰、清晰到智能体能靠它跑上一整天，比你自己把活干了还难。

The skill that's appreciating in value isn't writing code.

真正在升值的技能不是写代码。

It's writing specs that survive contact with an autonomous executor.

而是写出能经受住「与自主执行者接触」考验的规格说明（spec）。

---

## Where this is going｜这一切正走向何方

Google, Anthropic, and Cursor have converged on roughly the same shape.

Google、Anthropic 和 Cursor 已经收敛到了大致相同的形态上。

**Separate the model loop from the execution sandbox from the durable session log.**

**把模型循环、执行沙箱、持久会话日志三者彼此分离。**

**Split planning from generation from evaluation.**

**把规划、生成、评估三者拆分开。**

**Bake in compaction, hooks, and context resets.**

**把压缩、钩子和上下文重置内建进去。**

**Expose memory as a managed service that any agent invocation can query.**

**把记忆作为一个任何智能体调用都能查询的托管服务暴露出来。**

Surface area is what differs.

差异只在产品表面。

Google's Agent Platform is the enterprise-stack version, with the identity and audit trail story baked in.

Google 的 Agent Platform 是企业级技术栈版本，身份体系和审计追踪那一套是内建的。

The patterns underneath are the same.

底下的模式是一样的。

Claude Managed Agents is "Anthropic's harness, hosted."

Claude Managed Agents 是「Anthropic 的 harness，托管版」。

Cursor's background agents are "long-running coding, pulled out of the IDE and into the cloud."

Cursor 的后台智能体则是「长时程编码，从 IDE 里拽出来放进云端」。

The harder problems for the next year aren't in any of those layers individually.

未来一年更难的问题，不在上述任何单独一层里。

They're in the coordination above them.

而在它们之上的协调层。

Many long-running agents on a shared codebase.

许多长时程智能体共用一个代码库。

Agents that read their own traces and patch their own harnesses.

能读取自己的运行轨迹（trace）、修补自己 harness 的智能体。

Harnesses that assemble tools and context just-in-time for a task instead of being pre-configured at startup.

为任务即时（just-in-time）组装工具和上下文、而非在启动时预先配置好的 harness。

That's where the agent stops looking like a smarter chat window and starts looking like a colleague who's been on the project longer than you have.

到那时，智能体就不再像一个更聪明的聊天窗口，而开始像一位在这个项目上待得比你还久的同事。

The model is still load-bearing.

模型依然是承重结构。

But the gap between a chat window and an agent you can leave running overnight is mostly in the state, sessions, and structured handoffs wrapped around it.

但「一个聊天窗口」和「一个你可以放心让它通宵运行的智能体」之间的差距，大部分在于包裹在模型外面的状态、会话与结构化交接。

That's where I'd spend my learning time right now.

如果是现在，我会把学习时间花在那里。

---

*If you want the prerequisite reading, my [Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/) post covers the harness primitives this one builds on, and [Self-improving agents](https://addyosmani.com/blog/self-improving-agents/) goes deeper on the Ralph loop pattern.*

*如果你想要前置阅读材料：我的[《Agent Harness Engineering》](https://addyosmani.com/blog/agent-harness-engineering/)一文讲了本文所依赖的 harness 原语，而[《Self-improving agents》](https://addyosmani.com/blog/self-improving-agents/)则对 Ralph 循环模式做了更深入的展开。*
