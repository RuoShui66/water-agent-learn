# B09_Structured outputs on the Claude Developer Platform_Claude 开发者平台上的结构化输出

> 原文：https://claude.com/blog/structured-outputs-on-the-claude-developer-platform
> 来源：Anthropic Claude Blog（分类：Platform ｜ 产品：Claude Developer Platform）｜发布日期：2025-11-14（2026-02-04 GA）
> 原文存档：[Markdown](原文/B09_structured-outputs-on-the-claude-developer-platform_原文.md)

## 📌 本篇速览

- 📅 2025-11-14（2026-02-04 GA）　｜　⏱ 原文约 420 词（逐句精读约 6 分钟）
- 🏷 structured outputs、JSON schema 保证、工具定义遵从、多智能体通信
- 🗂 [返回目录](00_目录与阅读进度.md)

结构化输出发布文：**API 响应保证符合你给定的 JSON schema 或工具定义**，且官方明确「对模型性能无影响」。两种用法：JSON 模式（请求里给 schema）与 tools 模式（输出自动遵从工具定义）。三个关键场景里有两个直接对应 Agent 架构：**多智能体架构（智能体间通信格式一致性）**和**复杂搜索工具（多个检索字段必须准确合规）**——后者正是多路检索 Agent 汇总证据时的场景。收益表述可直接引用：可靠输出、更少重试、代码库不再需要 failover 逻辑和复杂错误处理。

---

***Update:** Now generally available (GA) natively on the Claude Developer Platform and in Amazon Bedrock for Claude Sonnet 4.5, Opus 4.5, and Haiku 4.5. GA adds support for more complex schemas. (Feb 4, 2026)*

***更新：**现已在 Claude 开发者平台原生及 Amazon Bedrock 上对 Claude Sonnet 4.5、Opus 4.5 和 Haiku 4.5 正式可用（GA）。GA 版本增加了对更复杂 schema 的支持。（2026 年 2 月 4 日）*

***Update:** Now available on Claude Haiku 4.5—supported on the Claude Developer Platform, natively and in Microsoft Foundry. (Dec 4, 2025)*

***更新：**现已支持 Claude Haiku 4.5——在 Claude 开发者平台原生及 Microsoft Foundry 上可用。（2025 年 12 月 4 日）*

The Claude Developer Platform now supports structured outputs for Claude Sonnet 4.5 and Opus 4.1.

Claude 开发者平台现在为 Claude Sonnet 4.5 和 Opus 4.1 提供结构化输出（structured outputs）支持。

Available in public beta, this feature ensures API responses always match your specified JSON schemas or tool definitions.

该特性以公开测试版提供，确保 API 响应永远符合你指定的 JSON schema 或工具定义。

With structured outputs, developers can eliminate schema-related parsing errors and failed tool calls by ensuring that Claude's responses conform to a defined schema—whether you're extracting data from images, orchestrating agents, or integrating with external APIs.

借助结构化输出，开发者可以消除与 schema 相关的解析错误和失败的工具调用——无论你是在从图像提取数据、编排智能体，还是对接外部 API，Claude 的响应都保证符合既定 schema。

### Building reliable applications

### 构建可靠的应用

For developers building applications and agents in production, a single error in data formatting can cause cascading failures.

对在生产环境构建应用和智能体的开发者来说，一个数据格式错误就可能引发级联故障。

Structured outputs solves this by guaranteeing your response matches the exact structure you define, without any impact to model performance.

结构化输出通过保证响应严格匹配你定义的结构来解决这个问题——并且对模型性能没有任何影响。

This makes Claude dependable for applications and agents where accuracy is critical, including:

这让 Claude 在准确性至关重要的应用和智能体场景中变得可靠，包括：

- **Data extraction** when downstream systems rely on error-free, consistent formats.

- **数据提取**：下游系统依赖无错、一致的格式。

- **Multi-agent architectures** where consistent communication between agents is critical for a performant, stable experience.

- **多智能体架构**：智能体之间格式一致的通信，对高性能、稳定的体验至关重要。

- **Complex search tools** where multiple search fields must be filled in accurately and conform to specific patterns.

- **复杂搜索工具**：多个检索字段必须填写准确、并符合特定模式。

Structured outputs can be used two ways: with JSON or tools.

结构化输出有两种用法：JSON 或 tools。

When used with JSON, you provide your schema definition in the API request.

JSON 用法下，你在 API 请求里提供 schema 定义。

For tools, you define your tool specifications, and Claude's output conforms to those tool definitions automatically.

tools 用法下，你定义工具规格，Claude 的输出自动遵从这些工具定义。

The end result is a reliable output, reduced retries, and a simplified codebase that no longer needs failover logic or complex error handling.

最终结果是：可靠的输出、更少的重试，以及一个不再需要故障转移逻辑或复杂错误处理的更简洁的代码库。

### Customer Spotlight: OpenRouter

### 客户案例：OpenRouter

OpenRouter provides 4M+ developers access to all major AI models through a single, unified interface.

OpenRouter 通过单一统一接口，为 400 多万开发者提供所有主流 AI 模型的访问。

"Structured outputs have become a really valuable part of the agentic AI stack. Agents constantly ingest and produce structured data, so Anthropic's structured outputs close a real gap for developers. Agent workflows run reliably, every time, and teams can focus on their customers rather than debugging tool calls," said Chris Clark, COO, OpenRouter.

OpenRouter COO Chris Clark 说：「结构化输出已经成为智能体 AI 技术栈中非常有价值的一环。智能体持续地摄入和产出结构化数据，所以 Anthropic 的结构化输出为开发者补上了一个真实的缺口。智能体工作流每一次都能可靠运行，团队可以专注于客户，而不是调试工具调用。」

### Getting started

### 快速上手

Structured outputs is now available in public beta for Sonnet 4.5 and Opus 4.1 on the Claude Developer Platform, with support for Haiku 4.5 coming soon.

结构化输出现已在 Claude 开发者平台上对 Sonnet 4.5 和 Opus 4.1 开放公开测试，Haiku 4.5 支持即将推出。

Explore our documentation for supported JSON schema types, implementation examples, and best practices.

支持的 JSON schema 类型、实现示例和最佳实践见[文档](https://docs.claude.com/en/docs/build-with-claude/structured-outputs)。

---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| structured outputs | 结构化输出 | 响应保证匹配 JSON schema / 工具定义 |
| JSON schema | JSON 模式 | 请求内声明的输出结构约束 |
| tool definitions | 工具定义 | 第二种用法：输出自动遵从工具规格 |
| cascading failures | 级联故障 | 一个格式错误在生产系统里的放大效应 |
| failover logic | 故障转移逻辑 | 有了保证后可从代码库里删掉的东西 |
| agentic AI stack | 智能体 AI 技术栈 | OpenRouter 引言中的定位 |
