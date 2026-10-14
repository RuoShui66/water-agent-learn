# B20_Built-in memory for Claude Managed Agents_Claude 托管智能体的内置记忆

> 原文：https://claude.com/blog/claude-managed-agents-memory
> 来源：Claude 产品博客（Product announcements · Claude Platform）｜发布日期：2026-04-23｜官方标注阅读时长约 5 分钟

## 📌 本篇速览

- 📅 2026-04-23　｜　⏱ 约 5 分钟
- 🏷 Managed Agents、记忆（Memory）、文件系统记忆、企业级部署、public beta
- 🗂 [返回目录](00_目录与阅读进度.md)

本文宣布 Claude Managed Agents（托管智能体）的内置记忆功能进入公开测试（public beta）：智能体可以从每一次会话中学习，背后是一个针对长时程智能体调优的"intelligence-optimized"记忆层。核心设计是记忆以文件形式存储并直接挂载到文件系统，Claude 沿用已有的 bash 与代码执行能力读写记忆；文件形态也带来可导出、可经 API 独立管理的可携带性。面向企业部署，记忆提供作用域权限、审计日志、版本回滚与内容脱敏，多智能体可并发共享同一存储。文末列举 Netflix、Rakuten（首轮错误降低 97%）、Wisedocs（验证提速 30%）、Ando 四家客户的实践与引语。

---

Memory on [Claude Managed Agents](https://claude.com/blog/claude-managed-agents) is available today in public beta.

[Claude Managed Agents](https://claude.com/blog/claude-managed-agents)（Claude 托管智能体）的记忆功能今日起进入公开测试（public beta）。

Your agents can now learn from every session, using an intelligence-optimized memory layer that balances performance with flexibility.

你的智能体现在可以借助一个为智能表现而优化（intelligence-optimized）的记忆层从每一次会话中学习，这个记忆层在性能与灵活性之间取得了平衡。

Because memories are stored as files, developers can export them, manage them via the API, and keep full control over what agents retain.

由于记忆以文件形式存储，开发者可以将其导出、通过 API 进行管理，并对智能体到底记住了什么保有完全的控制权。

![figure](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69e911b25f02df256c8cba87_Claude-Blog-CMA-Memory.png)

## How memory works in Claude Manged Agents|Claude 托管智能体中的记忆如何工作

Memory for Claude Managed Agents is a built-in, intelligence-optimized memory layer that lets agents learn from every session.

Claude Managed Agents 的记忆是一个内置的（built-in）、为智能表现而优化的记忆层，让智能体能够从每一次会话中学习。

Memory is optimized against internal benchmarks for long-running agents that improve across sessions and share what they've learned with each other.

这套记忆针对内部基准（internal benchmarks）做了优化，基准场景就是那些跨会话持续改进、并互相分享所学的长时程智能体（long-running agents）。

We've found that agents are most effective with memory when it builds on the tools they already use.

我们发现，当记忆构建在智能体已经在使用的工具之上时，效果最好。

Memory on Claude Managed Agents mounts directly onto a filesystem, so Claude can rely on the same bash and code execution capabilities that make it effective at agentic tasks.

Claude Managed Agents 的记忆直接挂载到文件系统上，因此 Claude 可以沿用那些让它擅长智能体任务（agentic tasks）的 bash 与代码执行能力。

With filesystem-based memory, [our latest models](https://www.anthropic.com/news/claude-opus-4-7#:~:text=Memory.%20Opus%204.7%20is%20better%20at%20using%20file%20system%2Dbased%20memory.%20It%20remembers%20important%20notes%20across%20long%2C%20multi%2Dsession%20work%2C%20and%20uses%20them%20to%20move%20on%20to%20new%20tasks%20that%2C%20as%20a%20result%2C%20need%20less%20up%2Dfront%20context.) save more comprehensive, well-organized memories and are more discerning about what to remember for a given task.

基于文件系统的记忆之下，[我们最新的模型](https://www.anthropic.com/news/claude-opus-4-7#:~:text=Memory.%20Opus%204.7%20is%20better%20at%20using%20file%20system%2Dbased%20memory.%20It%20remembers%20important%20notes%20across%20long%2C%20multi%2Dsession%20work%2C%20and%20uses%20them%20to%20move%20on%20to%20new%20tasks%20that%2C%20as%20a%20result%2C%20need%20less%20up%2Dfront%20context.)会写下更全面、组织更好的记忆，并且对"针对当前任务什么值得记"更有分辨力。

## Portable memories for production-grade agents|面向生产级智能体的可携带记忆

Memory is built for enterprise deployments, with scoped permissions, audit logs, and full programmatic control.

记忆是为企业级部署而构建的，带有作用域权限（scoped permissions）、审计日志（audit logs）和完整的程序化控制能力。

Stores can be shared across multiple agents with different access scopes.

记忆存储（store）可以在多个智能体之间以不同的访问范围共享。

For example, an org-wide store might be read-only, while per-user stores allow reads and writes.

例如，组织级（org-wide）的存储可以设为只读，而按用户（per-user）的存储则允许读写。

Multiple agents can work concurrently against the same store without overwriting each other.

多个智能体可以并发操作同一个存储，而不会互相覆盖。

Memories are files that can be exported and independently managed via the API, giving developers full control.

记忆就是文件，可以导出，也可以通过 API 独立管理，控制权完全交到开发者手中。

All changes are tracked with a detailed audit log, so you can tell which agent and session a memory came from.

所有变更都记录在详细的审计日志中，因此你可以知道每条记忆来自哪个智能体、哪次会话。

You can roll back to an earlier version or redact content from history.

你可以将记忆回滚（roll back）到早期版本，或从历史中脱敏移除（redact）内容。

Updates also surface in the [Claude Console](https://platform.claude.com/) as session events, so developers can trace what an agent learned and where it came from.

记忆更新还会以会话事件（session event）的形式出现在 [Claude Console](https://platform.claude.com/) 中，开发者可以据此追踪智能体学到了什么、又是从哪里学来的。

## **What teams are building**|客户团队在构建什么

Teams have been using memory to close feedback loops, speed up verification, and replace custom retrieval infrastructure:

各团队一直在用记忆来闭合反馈回路、加速验证流程，并替代自建的检索基础设施：

- **Netflix** agents carry context across sessions, including insights that took multiple turns to uncover and corrections from a human mid-conversation, instead of manually updating prompts and skills.

- **Netflix** 的智能体可以跨会话携带上下文——包括那些花了多轮对话才挖掘出来的洞察，以及人类在对话中途给出的纠正——而不必再手动更新提示词和 skills。

- **Rakuten's** task-based long-running agents use memory to learn from every session and avoid repeating past mistakes, cutting first-pass errors by 97%, all within workspace-scoped, observable boundaries.

- **Rakuten（乐天）**的任务型长时程智能体用记忆从每次会话中学习、避免重复过去的错误，将首轮错误（first-pass errors）降低了 97%，而这一切都发生在以工作区为作用域、可观测的边界之内。

- **Wisedocs** built their document verification pipeline on Managed Agents, using cross-session memory to spot and remember recurring document issues, speeding up verification by 30%.

- **Wisedocs** 把文档验证流水线构建在 Managed Agents 之上，用跨会话记忆发现并记住反复出现的文档问题，使验证提速 30%。

- **Ando** is building their workplace messaging platform on Managed Agents, capturing how each organization interacts instead of building memory infrastructure themselves.

- **Ando** 正在 Managed Agents 上构建他们的工作场所消息平台，直接捕捉每个组织的互动方式，而无需自建记忆基础设施。

![logo](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/68d5faa6352b26bf7542cb9b_logo_rakuten-light.svg)

> Memory in Claude Managed Agents lets us put continuous learning into production at scale.

> Claude Managed Agents 的记忆功能让我们能够把持续学习规模化地推上生产环境。

> Our agents distill lessons from every session, delivering 97% fewer first-pass errors at 27% lower cost and 34% lower latency, so users spend less time nudging agents to fix mistakes the system has already learned to avoid.

> 我们的智能体从每次会话中提炼经验教训，带来了 97% 更少的首轮错误、27% 更低的成本和 34% 更低的延迟——用户不再需要花时间反复提醒智能体去修复那些系统早已学会规避的错误。

> And because memory is workspace-scoped and observable, continuous learning stays under our control.

> 而且由于记忆以工作区为作用域且可观测，持续学习始终处于我们的掌控之中。

> — Yusuke Kaji, General Manager, AI for Business

> —— Yusuke Kaji，AI for Business 总经理

![logo](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a1edcd77828fd211e8ca469_ando-light.svg)

> A lot of our work at Ando is making sense of fast-moving, messy conversations between teams and their agents.

> Ando 的大量工作，是从团队与其智能体之间快速流动、杂乱无章的对话中理出头绪。

> Memory lets us stop building memory infra and focus on the product itself.

> 记忆功能让我们得以不再自建记忆基础设施，而是专注于产品本身。

> — Sara Du, Founder

> —— Sara Du，创始人

![logo](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69ea2b010f3f3d0c408c6ec5_wisedocs-light.svg)

> A good memory API gets rid of many infrastructure headaches, especially when building across agents and sessions.

> 一个好的记忆 API 能消除许多基础设施上的头疼事，尤其是在跨智能体、跨会话构建系统的时候。

> In our document verification pipeline on Claude Managed Agents, we used cross-session memory to let our agents identify and remember common issues — including ones we didn't think about.

> 在我们构建于 Claude Managed Agents 上的文档验证流水线中，我们用跨会话记忆让智能体自己识别并记住常见问题——包括那些我们自己都没想到的问题。

> It's sped verification up 30%.

> 它让验证提速了 30%。

> — Denys Linkov, Head of Machine Learning

> —— Denys Linkov，机器学习负责人

## Getting started|开始使用

Memory on Managed Agents is now available in public beta on the Claude Platform.

Managed Agents 的记忆功能现已在 Claude Platform 上进入公开测试。

Visit the [Claude Console](https://platform.claude.com/workspaces/default/memory-stores) or use our new CLI to deploy your first agent with memory.

访问 [Claude Console](https://platform.claude.com/workspaces/default/memory-stores)，或使用我们新推出的 CLI，部署你的第一个带记忆的智能体。

Explore the [documentation](https://platform.claude.com/docs/en/managed-agents/memory) to learn more.

浏览[官方文档](https://platform.claude.com/docs/en/managed-agents/memory)了解更多信息。


---

## 术语中英对照表

| 英文 | 中文 | 说明 |
|---|---|---|
| Managed Agents | 托管智能体 | Anthropic 平台托管运行的智能体产品 |
| memory layer | 记忆层 | 内置、"intelligence-optimized"，针对长时程基准调优 |
| memory store | 记忆存储 | 可被多个智能体以不同权限共享的存储单元 |
| filesystem-mounted memory | 文件系统挂载记忆 | 记忆挂载为文件目录，复用 bash / 代码执行能力 |
| scoped permissions | 作用域权限 | 例：组织级只读 + 用户级读写 |
| audit log | 审计日志 | 记录每条记忆来自哪个智能体、哪个会话 |
| rollback | 回滚 | 将记忆退回早期版本 |
| redaction | 内容脱敏 | 从记忆历史中移除敏感内容 |
| session event | 会话事件 | 记忆更新在 Claude Console 中的呈现形式 |
| first-pass errors | 首轮错误 | Rakuten 报告降低 97% 的指标 |
| portable memories | 可携带记忆 | 文件形态、可导出、可独立经 API 管理 |
| public beta | 公开测试 | 本功能当前的发布阶段 |
