# B05_Building agents with the Claude Agent SDK_用 Claude Agent SDK 构建智能体

> 原文：https://claude.com/blog/building-agents-with-the-claude-agent-sdk
> 来源：Claude 官方博客｜发布日期：2025-09-29｜官方标注阅读时长约 5 分钟

## 📌 本篇速览

- 📅 2025-09-29　｜　⏱ 约 5 分钟
- 🏷 Claude Agent SDK、Claude Code、Agent Loop、上下文工程、子智能体、MCP
- 🗂 [返回目录](00_目录与阅读进度.md)

本文宣布 Claude Code SDK 正式更名为 Claude Agent SDK：驱动 Claude Code 的那套 agent harness 不仅能写代码，还能驱动深度研究、视频制作、笔记整理等各类智能体。文章的核心设计原则是「给智能体一台电脑」，并围绕「收集上下文 → 采取行动 → 验证成果 → 重复」的智能体循环，以一个邮件智能体为贯穿案例，逐一讲解 SDK 提供的能力：智能体式搜索与文件系统、语义检索、子智能体、上下文压缩；工具、Bash 脚本、代码生成、MCP；以及规则校验、视觉反馈、LLM 评审三种验证手段，最后给出测试与迭代智能体的实用检查清单。

---

The Claude Agent SDK is a collection of tools that helps developers build powerful agents on top of Claude Code.

Claude Agent SDK 是一套工具集，帮助开发者在 Claude Code 之上构建强大的智能体（agent）。

In this article, we walk through how to get started and share our best practices.

在这篇文章里，我们会讲解如何上手，并分享我们的最佳实践。

Last year, we shared lessons in building effective agents alongside our customers.

去年，我们分享了与客户一起构建高效智能体过程中总结的经验。

Since then, we've released Claude Code, an agentic coding solution that we originally built to support developer productivity at Anthropic.

从那以后，我们发布了 Claude Code——一个智能体式编程（agentic coding）解决方案，最初是为了提升 Anthropic 内部开发者的生产力而打造的。

Over the past several months, Claude Code has become far more than a coding tool.

在过去的几个月里，Claude Code 早已远远超出了一个编程工具的范畴。

At Anthropic, we’ve been using it for deep research, video creation, and note-taking, among countless other non-coding applications.

在 Anthropic 内部，我们一直用它做深度研究、视频制作和记笔记，以及数不清的其他非编程用途。

In fact, it has begun to power almost all of our major agent loops.

事实上，它已经开始驱动我们几乎所有主要的智能体循环（agent loop）。

In other words, the agent harness that powers Claude Code (the Claude Code SDK) can power many other types of agents, too.

换句话说，驱动 Claude Code 的那套智能体框架（agent harness），也就是 Claude Code SDK，同样可以驱动许多其他类型的智能体。

To reflect this broader vision, we're renaming the Claude Code SDK to the Claude Agent SDK.

为了体现这个更宏大的愿景，我们决定把 Claude Code SDK 更名为 Claude Agent SDK。

In this post, we'll highlight why we built the Claude Agent SDK, how to build your own agents with it, and share the best practices that have emerged from our team’s own deployments.

在这篇文章中，我们会阐明为什么要打造 Claude Agent SDK、如何用它构建你自己的智能体，并分享我们团队在自身部署实践中沉淀出来的最佳实践。

## Giving Claude a computer|给 Claude 一台电脑

The key design principle behind Claude Code is that Claude needs the same tools that programmers use every day.

Claude Code 背后的核心设计原则是：Claude 需要的正是程序员每天在用的那套工具。

It needs to be able to find appropriate files in a codebase, write and edit files, lint the code, run it, debug, edit, and sometimes take these actions iteratively until the code succeeds.

它需要能在代码库里找到合适的文件、编写和编辑文件、对代码做静态检查（lint）、运行、调试、修改，有时还要反复迭代这些操作，直到代码跑通为止。

We found that by giving Claude access to the user’s computer (via the terminal), it had what it needed to write code like programmers do.

我们发现，只要让 Claude 能够（通过终端）访问用户的电脑，它就具备了像程序员一样写代码所需的一切。

But this has also made Claude in Claude Code effective at *non*-coding tasks.

但这也让 Claude Code 中的 Claude 在**非**编程任务上同样表现出色。

By giving it tools to run bash commands, edit files, create files and search files, Claude can read CSV files, search the web, build visualizations, interpret metrics, and do all sorts of other digital work – in short, create general-purpose agents with a computer.

只要给它运行 bash 命令、编辑文件、创建文件和搜索文件的工具，Claude 就能读取 CSV 文件、搜索网页、制作可视化图表、解读指标，以及完成各种其他数字化工作——简而言之，就是用一台电脑打造出通用型智能体。

The key design principle behind the Claude Agent SDK is to give your agents a computer, allowing them to work like humans do.

Claude Agent SDK 背后的核心设计原则就是：给你的智能体一台电脑，让它们像人类一样工作。

## Creating new types of agents|创造新型智能体

We believe giving Claude a computer unlocks the ability to build agents that are more effective than before.

我们相信，给 Claude 一台电脑，就能解锁构建比以往更高效的智能体的能力。

For example, with our SDK, developers can build:

举例来说，借助我们的 SDK，开发者可以构建：

- **Finance agents**:* *Build agents that can understand your portfolio and goals, as well as help you evaluate investments by accessing external APIs, storing data and running code to make calculations.

- **金融智能体（Finance agents）**：构建能理解你的投资组合与目标的智能体，并通过访问外部 API、存储数据、运行代码做计算，帮你评估投资。

- **Personal assistant agents**. Build agents that can help you book travel and manage your calendar, as well as schedule appointments, put together briefs, and more by connecting to your internal data sources and tracking context across applications.

- **私人助理智能体（Personal assistant agents）**：构建能帮你预订行程、管理日历的智能体，还能通过接入你的内部数据源、跨应用追踪上下文，来安排约会、整理简报等等。

- **Customer support agents:** Build agents that can handle high ambiguity user requests, like customer service tickets, by collecting and reviewing user data, connecting to external APIs, messaging users back and escalating to humans when needed.

- **客服智能体（Customer support agents）**：构建能处理高歧义用户请求（如客服工单）的智能体，通过收集并审查用户数据、连接外部 API、回复用户消息，并在必要时升级转交给人工来完成。

- **Deep research agents**: Build agents that can conduct comprehensive research across large document collections by searching through file systems, analyzing and synthesizing information from multiple sources, cross-referencing data across files, and generating detailed reports.

- **深度研究智能体（Deep research agents）**：构建能在大规模文档集合上开展全面研究的智能体，方式包括搜索文件系统、分析并综合多来源信息、跨文件交叉引用数据，以及生成详细报告。

And much more.

以及更多类型。

At its core, the SDK gives you the primitives to build agents for whatever workflow you're trying to automate.

归根结底，SDK 提供的是一组原语（primitives），无论你想自动化什么工作流，都可以用它们来构建智能体。

## Building your agent loop|构建你的智能体循环

In Claude Code, Claude often operates in a specific feedback loop: gather context -> take action -> verify work -> repeat.

在 Claude Code 中，Claude 通常运行在一个特定的反馈循环里：收集上下文 -> 采取行动 -> 验证成果 -> 重复。

![Agent feedback loop](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/697a4b28db0e40fd93e63875_image.png)

This offers a useful way to think about other agents, and the capabilities they should be given.

这为我们思考其他智能体以及它们应该被赋予哪些能力，提供了一个有用的框架。

To illustrate this, we’ll walk through the example of how we might build an email agent in the Claude Agent SDK.

为了具体说明，我们将以「如何用 Claude Agent SDK 构建一个邮件智能体」为例贯穿全文。

## Gather context|收集上下文

When developing an agent, you want to give it more than just a prompt: it needs to be able to fetch and update its own context.

开发智能体时，你给它的不能只是一段提示词（prompt）：它需要能够自己获取并更新自己的上下文。

Here’s how features in the SDK can help.

下面介绍 SDK 中的功能如何帮上忙。

### **Agentic search and the file system**|智能体式搜索与文件系统

The file system represents information that *could* be pulled into the model's context.

文件系统代表的是那些*可以*被拉进模型上下文的信息。

When Claude encounters large files, like logs or user-uploaded files, it will decide which way to load these into its context by using bash scripts like `grep` and `tail`.

当 Claude 遇到大文件——比如日志或用户上传的文件——时，它会借助 `grep`、`tail` 这类 bash 脚本，自行决定用哪种方式把内容加载进上下文。

In essence, the folder and file structure of an agent becomes a form of context engineering.

本质上，智能体的文件夹与文件结构本身就成了一种上下文工程（context engineering）。

Our email agent might store previous conversations in a folder called ‘Conversations’.

我们的邮件智能体可以把过往会话存放在一个叫 Conversations 的文件夹里。

This would allow it to search previous these for its context when asked about them.

这样，当被问到过往会话时，它就能自己去搜索这些内容来补充上下文。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/697a4b28db0e40fd93e6387e_image.webp)

### **Semantic search**|语义检索

Semantic search is usually faster than agentic search, but less accurate, more difficult to maintain, and less transparent.

语义检索（semantic search）通常比智能体式搜索更快，但准确性更低、更难维护，也更不透明。

It involves ‘chunking’ the relevant context, embedding these chunks as vectors, and then searching for concepts by querying those vectors.

它的做法是把相关上下文「切块」（chunking），将这些块嵌入为向量，然后通过查询这些向量来搜索概念。

Given its limitations, we suggest starting with agentic search, and only adding semantic search if you need faster results or more variations.

鉴于这些局限，我们建议先从智能体式搜索入手，只有当你需要更快的结果或更多样的变体时，再补充语义检索。

### **Subagents**|子智能体

Claude Agent SDK supports subagents by default.

Claude Agent SDK 默认就支持子智能体（subagent）。

Subagents are useful for two main reasons.

子智能体的价值主要体现在两点。

First, they enable parallelization: you can spin up multiple subagents to work on different tasks simultaneously.

第一，它们支持并行化：你可以同时启动多个子智能体，分头处理不同任务。

Second, they help manage context: subagents use their own isolated context windows, and only send relevant information back to the orchestrator, rather than their full context.

第二，它们有助于管理上下文：子智能体使用各自独立的上下文窗口（context window），只把相关信息传回给编排者（orchestrator），而不是回传全部上下文。

This makes them ideal for tasks that require sifting through large amounts of information where most of it won't be useful.

这使得它们特别适合那种需要在海量信息中筛选、而其中大部分信息其实没用的任务。

When designing our email agent, we might give it a 'search subagent' capability.

在设计邮件智能体时，我们可以给它一个「搜索子智能体」的能力。

The email agent could then spin off multiple search subagents in parallel—each running different queries against your email history—and have them return only the relevant excerpts rather than full email threads.

这样，邮件智能体就可以并行派生多个搜索子智能体——每个都对你的邮件历史执行不同的查询——并让它们只返回相关摘录，而不是完整的邮件会话串。

### **Compaction**|上下文压缩

When agents are running for long periods of time, context maintenance becomes critical.

当智能体长时间运行时，上下文的维护就变得至关重要。

The Claude Agent SDK’s compact feature automatically summarizes previous messages when the context limit approaches, so your agent won’t run out of context.

Claude Agent SDK 的压缩（compact）功能会在接近上下文上限时自动对先前的消息做摘要，让你的智能体不会耗尽上下文。

This is built on Claude Code’s compact slash command.

这个功能构建在 Claude Code 的 compact 斜杠命令之上。

## Take action|采取行动

Once you’ve gathered context, you’ll want to give your agent flexible ways of taking action.

收集好上下文之后，你还需要给智能体提供灵活的行动方式。

### **Tools**|工具

Tools are the primary building blocks of execution for your agent.

工具（tools）是智能体执行任务的首要构建单元。

Tools are prominent in Claude's context window, making them the primary actions Claude will consider when deciding how to complete a task.

工具在 Claude 的上下文窗口中占据显要位置，因此当 Claude 决定如何完成一项任务时，工具就是它优先考虑的行动选项。

This means you should be conscious about how you design your tools to maximize context efficiency.

这意味着你在设计工具时要有意识地最大化上下文效率。

You can see more best practices in our blog post, Writing effective tools for agents – with agents .

更多最佳实践可以参阅我们的博客文章《Writing effective tools for agents – with agents》。

As such, your tools should be primary actions you want your agent to take.

因此，你定义的工具应该是你希望智能体执行的主要动作。

Learn how to make custom tools in the Claude Agent SDK.

你可以了解如何在 Claude Agent SDK 中创建自定义工具。

For our email agent, we might define tools like “`fetchInbox`” or “`searchEmails`” as the agent’s primary, most frequent actions.

对于我们的邮件智能体，可以定义 “`fetchInbox`”、“`searchEmails`” 这样的工具，作为智能体最主要、最高频的动作。

### **Bash & scripts**|Bash 与脚本

Bash is useful as a general-purpose tool to allow the agent to do flexible work using a computer.

Bash 作为一种通用工具非常有用，它让智能体能够灵活地使用电脑开展工作。

In our email agent, the user might have important information stored in their attachments.

在我们的邮件智能体中，用户可能把重要信息存在了附件里。

Claude could write code to download the PDF, convert it to text, and search across it to find useful information by calling, as depicted below:

Claude 可以编写代码来下载 PDF、将其转换为文本，并在其中搜索有用信息，如下图所示：

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/697a4b28db0e40fd93e6387b_image.webp)

### **Code generation**|代码生成

The Claude Agent SDK excels at code generation—and for good reason.

Claude Agent SDK 尤其擅长代码生成——这是有充分理由的。

Code is precise, composable, and infinitely reusable, making it an ideal output for agents that need to perform complex operations reliably.

代码精确、可组合、可无限复用，因此对于需要可靠执行复杂操作的智能体来说，代码是一种理想的输出形式。

When building agents, consider: which tasks would benefit from being expressed as code?

构建智能体时，不妨想一想：哪些任务用代码来表达会更有优势？

Often, the answer unlocks significant capabilities.

这个问题的答案往往能解锁可观的能力。

For example, our recent launch of file creation in Claude.AI relies entirely on code generation.

例如，我们最近在 Claude.AI 上推出的文件创建功能就完全依赖代码生成。

Claude writes Python scripts to create Excel spreadsheets, PowerPoint presentations, and Word documents, ensuring consistent formatting and complex functionality that would be difficult to achieve any other way.

Claude 会编写 Python 脚本来创建 Excel 电子表格、PowerPoint 演示文稿和 Word 文档，从而保证格式一致，并实现用其他方式很难做到的复杂功能。

In our email agent, we might want to allow users to create rules for inbound emails.

在我们的邮件智能体中，我们可能希望允许用户为收到的邮件创建规则。

To achieve this, we could write code to run on that event:

为此，我们可以编写在该事件触发时运行的代码：

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/697a4b28db0e40fd93e63878_image.webp)

### **MCPs**|MCP

The Model Context Protocol (MCP) provides standardized integrations to external services, handling authentication and API calls automatically.

模型上下文协议（Model Context Protocol，MCP）提供了对接外部服务的标准化集成，会自动处理鉴权和 API 调用。

This means you can connect your agent to tools like Slack, GitHub, Google Drive, or Asana without writing custom integration code or managing OAuth flows yourself.

这意味着你可以把智能体连接到 Slack、GitHub、Google Drive、Asana 这类工具，而不必自己编写定制集成代码或管理 OAuth 流程。

For our email agent, we might want to `search Slack messages` to understand team context, or `check Asana tasks` to see if someone has already been assigned to handle a customer request.

对于我们的邮件智能体，我们可能想 `search Slack messages`（搜索 Slack 消息）来了解团队背景，或者 `check Asana tasks`（查看 Asana 任务）来确认是否已有人被指派处理某个客户请求。

With MCP servers, these integrations work out of the box—your agent can simply call tools like search_slack_messages or get_asana_tasks and the MCP handles the rest.

有了 MCP 服务器，这些集成开箱即用——你的智能体只需调用 search_slack_messages 或 get_asana_tasks 这样的工具，剩下的都由 MCP 处理。

The growing MCP ecosystem means you can quickly add new capabilities to your agents as pre-built integrations become available, letting you focus on agent behavior.

不断壮大的 MCP 生态意味着，随着预构建集成陆续可用，你可以快速为智能体添加新能力，把精力集中在智能体行为本身上。

## Verify your work|验证你的成果

The Claude Code SDK finishes the agentic loop by evaluating its work.

Claude Code SDK 通过评估自己的工作来完成智能体循环的最后一环。

Agents that can check and improve their own output are fundamentally more reliable—they catch mistakes before they compound, self-correct when they drift, and get better as they iterate.

能够检查并改进自身输出的智能体，从根本上更可靠——它们能在错误累积恶化之前发现问题，在跑偏时自我纠正，并在迭代中不断变好。

The key is giving Claude concrete ways to evaluate its work.

关键在于给 Claude 提供具体可操作的评估手段。

Here are three approaches we've found effective:

以下是我们发现行之有效的三种方法：

### **Defining rules**|定义规则

The best form of feedback is providing clearly defined rules for an output, then explaining which rules failed and why.

最好的反馈形式是：为输出提供清晰定义的规则，然后说明哪些规则未通过以及原因。

Code linting is an excellent form of rules-based feedback.

代码静态检查（linting）就是一种极佳的基于规则的反馈。

The more in-depth in feedback the better.

反馈越深入越好。

For instance, it is usually better to generate TypeScript and lint it than it is to generate pure JavaScript because it provides you with multiple additional layers of feedback.

例如，生成 TypeScript 并对其做静态检查，通常比生成纯 JavaScript 更好，因为前者能提供多层额外的反馈。

When generating an email, you may want Claude to check that the email address is valid (if not, throw an error) and that the user has sent an email to them before (if so, throw a warning).

在生成邮件时，你可能希望 Claude 检查邮箱地址是否有效（无效则抛出错误），并检查用户此前是否给对方发过邮件（若有则抛出警告）。

### **Visual feedback**|视觉反馈

When using an agent to complete visual tasks, like UI generation or testing, visual feedback (in the form of screenshots or renders) can be helpful.

当用智能体完成视觉类任务（比如 UI 生成或测试）时，视觉反馈（以截图或渲染结果的形式）会很有帮助。

For example, if sending an email with HTML formatting, you could screenshot the generated email and provide it back to the model for visual verification and iterative refinement.

例如，要发送一封带 HTML 格式的邮件时，你可以对生成的邮件截图，再把截图交回给模型做视觉验证与迭代打磨。

The model would then check whether the visual output matches what was requested.

模型随后会检查视觉输出是否符合要求。

For instance:

例如：

- **Layout** - Are elements positioned correctly? Is spacing appropriate?

- **布局（Layout）**——元素的位置是否正确？间距是否合适？

- **Styling** - Do colors, fonts, and formatting appear as intended?

- **样式（Styling）**——颜色、字体和格式呈现是否符合预期？

- **Content hierarchy** - Is information presented in the right order with proper emphasis?

- **内容层级（Content hierarchy）**——信息呈现的顺序是否正确、重点是否得当？

- **Responsiveness** - Does it look broken or cramped? (though a single screenshot has limited viewport info)

- **响应式（Responsiveness）**——页面看起来是否错乱或拥挤？（不过单张截图能提供的视口信息有限）

Using an MCP server like Playwright, you can automate this visual feedback loop—taking screenshots of rendered HTML, capturing different viewport sizes, and even testing interactive elements—all within your agent's workflow.

借助 Playwright 这样的 MCP 服务器，你可以把这个视觉反馈循环自动化——对渲染后的 HTML 截图、捕捉不同视口尺寸、甚至测试交互元素——全部都在智能体的工作流之内完成。

![Claude provides visual feedback on the body of an email generated by an agent.](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/697a4b28db0e40fd93e63881_image.webp)

### **LLM as a judge**|LLM 评审

You can also have another language model “judge" the output of your agent based on fuzzy rules.

你还可以让另一个语言模型基于模糊规则来「评审」你的智能体的输出。

This is generally not a very robust method, and can have heavy latency tradeoffs, but for applications where any boost in performance is worth the cost, it can be helpful.

一般来说这不是一种非常稳健的方法，还可能带来严重的延迟代价，但对于那些任何性能提升都值回成本的应用场景，它是有帮助的。

Our email agent might have a separate subagent judge the tone of its drafts, to see if they fit well with the user’s previous messages.

我们的邮件智能体可以用一个单独的子智能体来评审草稿的语气，看它们是否与用户以往的邮件风格相契合。

## Testing and improving your agent|测试并改进你的智能体

After you’ve gone through the agent loop a few times, we recommend testing your agent, and ensuring that it’s well-equipped for its tasks.

在你把智能体循环跑过几轮之后，我们建议对智能体进行测试，确保它为自己的任务做好了充分准备。

The best way to improve an agent is to look carefully at its output, especially the cases where it fails, and to put yourself in its shoes: does it have the right tools for the job?

改进智能体的最好办法，是仔细审视它的输出——尤其是失败的案例——并设身处地站在它的角度想：它手里的工具适合这个活儿吗？

Here are some other questions to ask as you’re evaluating whether or not your agent is well-equipped to do its job:

在评估你的智能体是否具备完成任务的充分条件时，还可以问自己下面这些问题：

- If your agent misunderstands the task, it might be missing key information. Can you alter the structure of your search APIs to make it easier to find what it needs to know?

- 如果智能体误解了任务，可能是它缺少关键信息。你能否调整搜索 API 的结构，让它更容易找到需要知道的内容？

- If your agent fails at a task repeatedly, can you add a formal rule in your tool calls to identify and fix the failure?

- 如果智能体在某项任务上反复失败，你能否在工具调用中加入一条正式规则，来识别并修复这种失败？

- If your agent can’t fix its errors, can you give it more useful or creative tools to approach the problem differently?

- 如果智能体无法修复自己的错误，你能否给它更有用或更有创意的工具，让它换一种思路解决问题？

- If your agent’s performance varies as you add features, build a representative test set for programmatic evaluations (or evals) based on customer usage.

- 如果随着功能增加，智能体的表现出现波动，那就基于客户的真实使用情况，构建一个具有代表性的测试集，用于程序化评估（evals）。

## Getting started|开始上手

The Claude Agent SDK makes it easier to build autonomous agents by giving Claude access to a computer where it can write files, run commands, and iterate on its work.

Claude Agent SDK 让构建自主智能体变得更容易：它让 Claude 可以使用一台电脑，在上面写文件、运行命令，并对自己的工作不断迭代。

With the agent loop in mind (gathering context, taking action, and your verifying work), you can build reliable agents that are easy to deploy and iterate on.

牢记智能体循环（收集上下文、采取行动、验证成果），你就能构建出可靠、易于部署和迭代的智能体。

You can get started with the Claude Agent SDK today.

你今天就可以开始使用 Claude Agent SDK。

For developers who are already building on the SDK, we recommend migrating to the latest version by following this guide.

对于已经在基于该 SDK 开发的开发者，我们建议按照迁移指南升级到最新版本。

## Acknowledgements|致谢

Written by Thariq Shihipar with notes and editing from Molly Vorwerck, Suzanne Wang, Alex Isken, Cat Wu, Keir Bradwell, Alexander Bricken & Ashwin Bhat.

本文由 Thariq Shihipar 撰写，Molly Vorwerck、Suzanne Wang、Alex Isken、Cat Wu、Keir Bradwell、Alexander Bricken 与 Ashwin Bhat 参与了批注与编辑。


---

## 术语中英对照表

| 英文 | 中文 | 说明 |
|---|---|---|
| Claude Agent SDK | Claude 智能体 SDK | 由 Claude Code SDK 更名而来，通用智能体开发套件 |
| agent harness | 智能体运行支架 | 驱动 Claude Code 的那套运行框架 |
| agent loop | 智能体循环 | gather context → take action → verify work → repeat |
| gather context | 收集上下文 | 循环第一阶段 |
| take action | 采取行动 | 循环第二阶段 |
| verify work | 验证成果 | 循环第三阶段 |
| agentic search | 智能体式搜索 | 用 bash（`grep`/`tail`）在文件系统里按需翻找 |
| semantic search | 语义检索 | 切块 + 向量化 + 查询；更快但更不准、更难维护、更不透明 |
| chunking | 切块 | 语义检索的第一步 |
| subagent | 子智能体 | 独立上下文窗口，只回传相关信息给编排者 |
| orchestrator | 编排者 | 接收子智能体回传结果的主智能体 |
| compaction | 压缩 | 接近上下文上限时自动总结历史消息 |
| context engineering | 上下文工程 | 文中论断：文件夹结构本身就是一种上下文工程 |
| primitives | 原语 | SDK 提供的基础构建单元 |
| code generation | 代码生成 | 精确、可组合、可无限复用的行动形态 |
| MCP (Model Context Protocol) | 模型上下文协议 | 标准化外部集成，自动处理鉴权与 API 调用 |
| rules-based feedback | 规则式反馈 | 最可靠的验证方式，如 lint、error/warning 分级 |
| visual feedback | 视觉反馈 | 截图/渲染交回模型校验，可用 Playwright 自动化 |
| LLM as a judge | 模型评判 | 按模糊规则评判输出；官方承认不够稳健且延迟代价大 |
| evals | 程序化评估 | 基于客户真实用法构建的代表性测试集 |
