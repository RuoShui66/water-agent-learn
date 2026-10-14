# 08_Codex-maxxing for long-running work_为长时程工作「榨干」Codex

> 原文：https://openai.com/index/codex-maxxing-long-running-work/
> PDF 全文：https://cdn.openai.com/pdf/8a9f00cf-d379-4e20-b06f-dd7ba5196a11/OAI_WhitePaper_Codex-maxxing26.pdf
> 来源：OpenAI 官方白皮书（27 页）｜发布日期：2026-06-22｜取材自创作者 **Jason Liu** 的日常工作流

## 📌 本篇速览

- 📅 2026-06-22　｜　📄 发布页短文 + 白皮书 PDF（27 页，10 个 section，图文为主）
- ⭐ ★★★★☆ **值得读，但要知道它是什么** —— 这**不是一篇工程架构论文**，而是一份**工作流实践指南**。它的价值在于展示 OpenAI 侧对长时程的产品答案：把 harness 提到**工作区层**。「弱目标 vs 强目标」那一节和 Anthropic 的冲刺契约是同一件事的不同措辞。
- 🏷 durable threads、memory vault、thread automations、steering、side panel、strong goal
- 🗂 [返回专题目录](00_目录.md)

本文件为**逐句对照**版：第一部分为发布页正文，第二部分为白皮书 PDF 主体叙述。PDF 为设计版式（大字块 + 图注式短句），正文句子悉数收录；纯装饰性页码、页眉（"Codex-maxxing for long-running work"）等 boilerplate 从略。

---

# 第一部分：发布页正文（openai.com/index）

## Codex-maxxing for long-running work｜为长时程工作「榨干」Codex

How Codex helps work continue beyond a single prompt

Codex 如何帮助工作延续到单条提示之外

Organizations are increasingly using AI to support work that extends beyond a single prompt.

越来越多的组织正在用 AI 支撑那些超出单条提示（prompt）范围的工作。

In this whitepaper, Jason Liu shares practical strategies for using Codex as a persistent workspace that preserves context, manages complex workflows, and helps sustain progress across long-running projects.

在这份白皮书中，Jason Liu 分享了把 Codex 当作**持久工作区**（persistent workspace）来用的实用策略——这个工作区能保存上下文、管理复杂工作流，并帮助长时程项目持续推进。

Learn how to break ambitious goals into verifiable steps, maintain continuity across workstreams, and determine when to delegate execution to Codex versus when human oversight is most valuable.

你将学到：如何把宏大目标拆成可验证的步骤，如何在多条工作流（workstream）之间保持连续性，以及如何判断什么时候该把执行委托给 Codex、什么时候人的监督最有价值。

Read the full guide here.

完整指南请点此阅读（即 PDF 白皮书）。

---

# 第二部分：白皮书 PDF 正文（27 页）

## Cover & Contents｜封面与目录

WHITE PAPER — Codex-maxxing for long-running work

白皮书——为长时程工作「榨干」Codex

How Codex helps work continue beyond a single prompt

Codex 如何帮助工作延续到单条提示之外

Contents: 01 Durable threads / 02 Voice input / 03 Steering / 04 Memory / 05 Computer and browser use / 06 Remote control / 07 Thread automations / 08 Three examples of loops / 09 Goals / 10 Side panel

目录：01 持久线程 / 02 语音输入 / 03 转向 / 04 记忆 / 05 计算机与浏览器使用 / 06 远程控制 / 07 线程自动化 / 08 三个循环示例 / 09 目标 / 10 侧边面板

## Opening｜开篇

Codex is becoming a place where work can start, keep going, and become real output.

Codex 正在变成一个让工作能够**开始、持续进行、并变成真实产出**的地方。

Turning a single prompt into an operating loop for getting projects done.

把单条提示变成一个把项目做完的**运转循环**（operating loop）。

Codex is still excellent for coding, but the more interesting shift is that it gives work somewhere to live.

Codex 依然非常擅长写代码，但更有意思的转变在于：它**给了工作一个安身之处**（somewhere to live）。

Creator Jason Liu uses Codex as part of his everyday workflow, from presentations and transcripts to spreadsheets, browser tasks, and recurring work.

创作者 Jason Liu 把 Codex 融入了自己的日常工作流——从演示文稿、转写稿，到电子表格、浏览器任务和周期性工作。

The guide looks at how Jason uses Codex as a place to gather context, ask for help, review what comes back, and return to the next step without losing the thread.

本指南考察的是 Jason 如何把 Codex 当作这样一个地方：汇集上下文、寻求帮助、评审返回的结果，然后不丢线索地回到下一步。

## Section 01 — Durable threads｜第 1 节 持久线程（Durable threads）

Giving the work a place to live

给工作一个安身之处

For important workstreams, a pinned thread can become the home for the work: the place where context, preferences, old decisions, and open loops accumulate over time.

对于重要的工作流，一个置顶线程（pinned thread）可以成为这项工作的**家**：上下文、偏好、旧决策和未闭合事项（open loops）都随时间在这里累积。

Use a durable thread for work that you expect to revisit:

对于你预期会反复回来处理的工作，请使用**持久线程**（durable thread）：

- Social feedback monitoring — Recurring questions, useful feedback, and signal from the public conversation.

- 社交反馈监控——反复出现的问题、有用的反馈，以及来自公开讨论的信号。

- Codex for open source — Issues, maintainers, contribution patterns, and release notes.

- 用 Codex 做开源——issue、维护者、贡献模式和发布说明（release notes）。

- OpenAI CLI — Commands, conventions, repo structure, and review preferences.

- OpenAI CLI——命令、约定、仓库结构和评审偏好。

- Agents SDK — Examples, docs, recurring questions, and product behavior.

- Agents SDK——示例、文档、反复出现的问题和产品行为。

- Chief of Staff — Messages, follow-ups, meetings, and open loops.

- 幕僚长（Chief of Staff）——消息、跟进事项、会议和未闭合事项。

Durable threads keep history available as the conversation grows and stores them in the memory vault.

随着对话不断变长，持久线程会保持历史可用，并把它们存进记忆库（memory vault）。

But there's a tradeoff: long-running threads carry context and may cost more to run than a fresh short thread.

但这里有一个权衡：长时程线程携带上下文，运行成本可能高于一个全新的短线程。

For important workstreams, continuity can be worth it and easier to manage.

对重要的工作流而言，这种连续性可能物有所值，而且更易于管理。

## Section 02 — Voice input｜第 2 节 语音输入（Voice input）

Put more of your actual thinking into Codex

把你更多的真实思考灌进 Codex

"I think there is some guy named Ben in Slack who mentioned this, I do not remember exactly what, just go look."

「我记得 Slack 里有个叫 Ben 的人提过这事，具体说了什么我不记得了，你去看看。」

Voice input changes the kind of context Codex gets.

**语音输入**（voice input）改变了 Codex 能拿到的上下文的类型。

The benefit isn't only speed.

好处不只是速度。

It's that spoken input often includes the unedited version of the work: the half-remembered name, the loose direction, the uncertainty, the thing that would be awkward to type but natural to say.

关键在于，口述输入往往包含工作**未经编辑的原始版本**：记了一半的名字、松散的方向、不确定性——那些打字很别扭、但说出来很自然的东西。

A lot of plans get better when the model has access to the messy version of what you think.

当模型能拿到你脑子里那个**乱糟糟的版本**时，很多计划会变得更好。（—— Jason Liu）

That's a useful instruction because it's how real work often starts.

这是一条有用的指令，因为真实的工作往往就是这样开始的。

Jason will start recording voice notes as he explores a page an agent made in the browser.

Jason 会一边在浏览器里查看 agent 做出来的页面，一边开始录语音笔记。

When he's finished, he hits Enter so Codex can execute that feedback.

录完之后，他按下回车，让 Codex 去执行这些反馈。

Transcripts work the same way.

转写稿（transcript）的用法也是一样。

A call, meeting, hallway conversation, or rough voice note can become starting material.

一通电话、一场会议、一次走廊对话、一段粗糙的语音笔记，都可以成为起始素材。

Codex can help turn the raw version into a plan, draft, artifact, or next action.

Codex 可以帮你把这个原始版本变成计划、草稿、工件（artifact）或下一步行动。

## Section 03 — Steering｜第 3 节 转向（Steering）

Shape the queue while Codex works

在 Codex 干活的同时塑造指令队列

Voice becomes more useful when it is paired with steering.

语音和**转向**（steering）搭配使用时会更有用。

Steering means adding the next instruction while Codex is already working.

转向的意思是：在 Codex 已经在工作时，追加下一条指令。

You can correct direction, add context, approve the next step, or queue up the next action after a tool call.

你可以修正方向、补充上下文、批准下一步，或在某次工具调用之后把下一个动作排进队列。

When you are reviewing a site, that might sound like:

当你在评审一个网站时，这听起来可能是：

- "Make this smaller."

- 「把这个改小点。」

- "This copy is wrong."

- 「这段文案不对。」

- "The spacing between these two things feels off."

- 「这两个东西之间的间距感觉不对。」

- "Once this is done, open a PR."

- 「这个做完之后，开一个 PR。」

- "Wait for the preview deployment."

- 「等预览部署完成。」

- "Show me the preview link before anything is posted."

- 「在发布任何东西之前，先给我看预览链接。」

## Section 04 — Memory｜第 4 节 记忆（Memory）

Make memory something you can review

让记忆成为你能评审的东西

Memory acts as a notebook to provide context for actions.

记忆就像一本笔记本，为各种动作提供上下文。

As threads last longer, they need memory outside the conversation.

线程持续得越久，就越需要**对话之外的记忆**。

While message history helps, it's not always enough.

消息历史虽然有帮助，但并不总是够用。

Useful context should become something you can open, edit, diff, and reuse.

有用的上下文应该变成你能**打开、编辑、diff、复用**的东西。

The vault can hold the rolling context around your work: people, decisions, open loops, daily notes, project state, and the details that would otherwise get lost between threads.

记忆库（vault）可以承载你工作周边的滚动上下文：人、决策、未闭合事项、日常笔记、项目状态，以及那些否则会在线程之间丢失的细节。

Keep this distinction clear:

要把这条边界划清楚：

Repositories hold code.

仓库装代码。

The vault holds rolling context around the work.

vault 装工作周边的滚动上下文。

When the vault lives in GitHub, diffs become a review surface for memory.

当 vault 存放在 GitHub 里时，diff 就成了记忆的**评审面**（review surface）。

You can see what Codex thought was important enough to write down.

你能看见 Codex 认为什么重要到值得写下来。

That review step matters.

这个评审环节很重要。

Long-running threads should not quietly accumulate vague impressions in conversation history.

长时程线程不应该在对话历史里静悄悄地攒下模糊的印象。

They should record what changed:

它们应该记录**什么变了**：

- This person prefers this.

- 这个人偏好这个。

- This project is waiting on that.

- 这个项目在等那件事。

- This decision was made.

- 这个决策已经做出。

- This loop is closed.

- 这个循环已经闭合。

Memory instruction:

记忆指令（Memory instruction）：

- As people are mentioned, update the relevant people notes.

- 有人被提到时，更新相关的人物笔记。

- As projects move forward, update the project page.

- 项目推进时，更新项目页。

- As loops close, mark them closed.

- 循环闭合时，标记为已关闭。

- As decisions are made, write down the decision and why it matters.

- 做出决策时，写下这个决策**以及它为什么重要**。

## Section 05 — Computer and browser use｜第 5 节 计算机与浏览器使用

Decide what the thread can touch

决定这个线程能碰什么

Once a thread has memory, the next question is practical: What can it use?

一旦线程有了记忆，下一个问题就很实际了：**它能用什么？**

Connectors extend Codex into the places where work often appears first: Slack threads, inboxes, calendars, docs, and issue trackers.

连接器（Connectors）把 Codex 延伸到工作最先出现的那些地方：Slack 会话、收件箱、日历、文档和 issue 跟踪器。

For this workflow, it helps to separate the surfaces:

对这种工作流来说，把各个「表面」（surface）区分开会很有帮助：

- $browser — Local web surfaces, previews, and annotations

- `$browser`——本地 web 界面、预览和批注

- @computer — GUI-only work that requires clicking

- `@computer`——只能靠点击完成的 GUI 工作

- @chrome — Signed-in browser sessions and authenticated tabs

- `@chrome`——已登录的浏览器会话和认证标签页

- Connectors — Slack, Gmail, Calendar, GitHub, and other work surfaces

- 连接器——Slack、Gmail、日历、GitHub 及其他工作表面

- Skills — Reusable workflows Codex can repeat

- 技能（Skills）——Codex 可以重复执行的可复用工作流

If you are iterating on a local app, use the browser surface.

如果你在迭代一个本地应用，就用浏览器表面。

If the task depends on logged-in state or multiple authenticated tabs, use Chrome.

如果任务依赖登录态或多个已认证的标签页，就用 Chrome。

If the only way to complete the task is through a desktop app, use computer use with clear permissions and review.

如果完成任务的唯一途径是桌面应用，就用计算机使用（computer use），并配上清晰的权限设置与评审。

Skills make repeated work easier to reuse.

技能让重复性工作更容易复用。

Once a workflow succeeds, you can often package the instructions, references, and scripts so Codex doesn't need to be retaught every time.

一旦某个工作流跑通了，你通常可以把指令、参考资料和脚本打包起来，这样就不必每次都重新教 Codex 一遍。

## Section 06 — Remote control｜第 6 节 远程控制（Remote control）

Keep longer loops portable

让更长的循环可随身携带

Remote control makes it easier to stay close to long-running tasks.

**远程控制**（remote control）让你更容易贴近那些长时间运行的任务。

Codex can keep working from the machine where your files, permissions, and local setup already live.

Codex 可以继续在那台已经装着你的文件、权限和本地环境的机器上干活。

You can check in from another device, review what it found, answer a question, approve the next step, or change direction.

你可以从另一台设备上查看进展、评审它的发现、回答一个问题、批准下一步，或者改变方向。

This matters most when Codex is already doing something that takes time.

当 Codex 已经在做一件耗时的事情时，这一点最为重要。

Start the task at your desk.

在书桌前启动任务。

Walk away.

然后走开。

Review the next decision point from your phone.

在手机上评审下一个决策点。

Approve, redirect, or ask for a different pass.

批准、改方向，或者要求换一种做法再来一遍。（—— Jason Liu）

Remote control is not a reason to skip reviews.

远程控制不是跳过评审的理由。

It is a way to keep enough attention on the loop to unblock the next move.

它是一种在循环上保持足够注意力、以便疏通下一步的方式。

## Section 07 — Thread automations｜第 7 节 线程自动化（Thread automations）

Schedule Codex to return

让 Codex 按计划回来

Thread automations are heartbeat-style recurring wake-up calls attached to the current thread.

**线程自动化**（thread automations）是挂在当前线程上的、心跳式的周期性唤醒。

They tell Codex to return to the same conversation on a cadence, preserving the context instead of starting from scratch each time.

它们让 Codex 按节奏（cadence）回到同一个对话里，保留上下文，而不是每次都从零开始。

A thread can have multiple schedules.

一个线程可以有多个调度计划。

It can run until a condition is met.

它可以一直运行到某个条件满足为止。

It can adjust cadence as the task changes.

它可以随任务变化调整节奏。

Normal prompt: "Do this now."

普通提示：「现在就做这件事。」

versus

对比

Thread automation: "Keep checking this and move it forward when something changes."

线程自动化：「持续盯着这件事，一旦有变化就把它往前推。」

Thread automation example: "Every 30 minutes, check Slack and Gmail for unanswered messages that may need attention. Research the context and draft replies, but do not send anything without approval."

线程自动化示例：「每 30 分钟检查一次 Slack 和 Gmail，找出可能需要关注的未回复消息。调研其背景并起草回复，但未经批准不得发送任何内容。」

That might mean checking a pull request, Slack thread, inbox, deployment, document, customer support thread, or long-running command.

这可能意味着去检查一个 pull request、一条 Slack 会话、收件箱、一次部署、一份文档、一个客服工单会话，或一条长时间运行的命令。

## Section 08 — Three examples of loops｜第 8 节 三个循环示例

Real ways to apply Codex in your workflows

在你的工作流中应用 Codex 的真实方式

The power comes from the loop across features: context, tools, memory, recurrence, and review.

威力来自贯穿各项功能的**循环**（loop）：上下文、工具、记忆、周期性执行和评审。

### Loop 1 — Chief of Staff｜循环 1：幕僚长

Codex checks Slack and Gmail on a schedule, finds messages that may need attention, searches for the context behind them, and drafts replies.

Codex 按计划检查 Slack 和 Gmail，找出可能需要关注的消息，检索消息背后的上下文，并起草回复。

The user still decides what gets sent.

但发不发、发什么，仍然由用户决定。

What Codex prepares: open messages / relevant context / draft replies / questions that need judgment.

Codex 准备的东西：待处理消息／相关上下文／回复草稿／需要人来判断的问题。

You decide: approval / tone / timing / final decision.

你来决定：是否批准／语气／时机／最终决定。

### Loop 2 — Monitor for feedback｜循环 2：监控反馈

Codex watches a Slack thread for animation feedback, updates the Remotion project, re-renders the piece, and prepares the revision for review.

Codex 盯着一条 Slack 会话里的动画反馈，更新 Remotion 项目，重新渲染作品，并把修订版准备好供评审。

The loop crosses tools: Slack for feedback, Remotion for rendering, and computer use when the upload or review surface requires a GUI.

这个循环横跨多个工具：用 Slack 收反馈，用 Remotion 渲染，当上传或评审界面必须用 GUI 时则用计算机使用。

What Codex prepares: feedback summary / updated render / revision notes / next review link.

Codex 准备的东西：反馈摘要／更新后的渲染结果／修订说明／下一个评审链接。

You decide: creative judgment / final approval / publishing decision.

你来决定：创意判断／最终批准／是否发布。

### Loop 3 — Get a refund｜循环 3：申请退款

Codex checks whether a customer support agent has joined, then prepares the next response when the conversation changes.

Codex 检查客服人员是否已加入会话，并在对话出现变化时准备好下一条回复。

The task can continue while the user is away, but the action stays bounded.

任务可以在用户不在场时继续推进，但动作始终**有边界**（bounded）。

What Codex prepares: status checks / draft responses / useful evidence / recommended next step.

Codex 准备的东西：状态检查／回复草稿／有用的证据／建议的下一步。

You decide: consent / approval / any irreversible action.

你来决定：是否同意／是否批准／任何不可逆的动作。

## Section 09 — Goals｜第 9 节 目标（Goals）

Set goals Codex can verify

设定 Codex 能验证的目标

A weak goal asks Codex to implement a plan.

**弱目标**（weak goal）只是让 Codex 去实现一个计划。

A stronger goal gives Codex something to test against: expected behavior, review criteria, constraints, or a clear definition of done.

**更强的目标**（stronger goal）给 Codex 一个可以对照测试的东西：预期行为、评审标准、约束条件，或一个清晰的完成定义（definition of done）。

Weak goal: "Implement the plan in this Markdown file."

弱目标：「实现这个 Markdown 文件里的计划。」

Strong goal: "Port this library, keep the public API compatible, and use the original unit tests as the success check.

强目标：「移植这个库，保持公共 API 兼容，并用原有的单元测试作为成功检验。

The work is ready for review when the same tests pass and the differences are documented."

当同一套测试全部通过、且差异都有文档记录时，这项工作才算可以送审。」

### Migrating Rich into Rust｜把 Rich 迁移到 Rust

The Rich-to-Rust example makes this concrete.

「Rich 移植到 Rust」这个例子把这一点讲得很具体。

The goal was not only to port the library.

目标不只是把库移植过去。

The goal was to port it in a way that could pass the original unit tests.

目标是以**能通过原有单元测试**的方式把它移植过去。

That test suite gave the run a real standard.

那套测试给这次运行提供了一个真实的标准。

The work was not ready until the new implementation passed the same tests.

在新实现通过同一套测试之前，这项工作都不算完成。

## Section 10 — Side panel｜第 10 节 侧边面板（Side panel）

Make the artifact part of the loop

让工件成为循环的一部分

The side panel is easy to understand as a preview surface, but that undersells it.

**侧边面板**（side panel）很容易被理解成一个预览界面，但这低估了它。

It's where Codex becomes more than a chat interface.

它是 Codex 超越聊天界面的地方。

You can inspect the same object Codex is acting on, leave comments, review changes, and keep the artifact inside the thread.

你可以直接查看 Codex 正在操作的那个对象、留下评论、评审变更，并把工件留在线程之内。

The side panel is where Codex stops being only a chat app and starts becoming the place the work happens.

侧边面板是 Codex 不再只是一个聊天应用、开始成为**工作真正发生的地方**的所在。（—— Jason Liu）

### Inspect artifacts｜查看工件

Markdown, spreadsheets, CSVs, PDFs, and slides can all live there.

Markdown、电子表格、CSV、PDF 和幻灯片都可以放在那里。

Markdown can be reviewed with comments.

Markdown 可以带着评论进行评审。

Spreadsheets can render formulas and support cell edits.

电子表格能渲染公式并支持单元格编辑。

CSVs become tables instead of raw text.

CSV 会渲染成表格，而不是原始文本。

PDFs render directly.

PDF 可以直接渲染。

Slides can be created and reviewed without leaving the app.

幻灯片可以在不离开应用的情况下创建和评审。

### Operate web surfaces｜操作 web 界面

The in-app browser makes small web artifacts more useful: index.html, Storybook, Remotion Studio, Slidev, Streamlit, and Jupyter.

应用内浏览器让小型 web 工件更有用：index.html、Storybook、Remotion Studio、Slidev、Streamlit 和 Jupyter。

The smallest version is often enough.

最小的版本往往就够用了。

A single index.html file with JavaScript and CSS can become a live surface for interaction and review.

一个带 JavaScript 和 CSS 的 index.html 文件，就能成为一个可交互、可评审的活界面。

### Review changes｜评审变更

You and Codex can look at the same object while the work is still moving.

在工作仍在推进时，你和 Codex 可以看着同一个对象。

Comments become instructions.

评论变成指令。

The artifact becomes context.

工件变成上下文。

## Closing｜结语

Jason Liu's practice shows how quickly Codex can build systems for work.

Jason Liu 的实践展示了 Codex 能多快地为工作**搭建起系统**。

With new ways to move projects forward, tasks become easier to pick up, review, and continue without losing context.

有了推进项目的新方式，任务变得更容易拿起来、评审、继续做下去，而不丢失上下文。

People can spend less time restarting and more time building on what's already in motion.

人们可以少花时间从头再来，多花时间在已经运转起来的东西上继续构建。

> 注：PDF 第 27 页为空白封底；各页页眉、页码等版式元素从略。
