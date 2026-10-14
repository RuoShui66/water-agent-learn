# B01_Claude can now use tools_Claude 现在能使用工具了

> 原文：https://claude.com/blog/tool-use-ga
> 来源：Anthropic Claude Blog（分类：Platform ｜ 产品：Claude API）｜发布日期：2024-05-30
> 原文存档：[Markdown](原文/B01_tool-use-ga_原文.md)

## 📌 本篇速览

- 📅 2024-05-30　｜　⏱ 原文约 690 词（逐句精读约 8 分钟）
- 🏷 tool use GA、流式工具调用、强制工具选择、thinking 标签、历史文献
- 🗂 [返回目录](00_目录与阅读进度.md)

⚠️ 这是 **2024 年中的历史文献**——tool use 在 Claude 3 全系 GA 的公告。价值在两点：① 面试时能讲出 tool use 的**演进时间线**（2024-05 GA 时 Claude 3 还**不支持并行工具调用**、Opus 靠 `<thinking>` 标签暴露推理——对比今天并行调用/interleaved thinking 已是默认，能体现你对技术脉络的把握）；② 五个官方定义的经典 tool use 用例（结构化抽取、自然语言→API 调用、查库回答、任务自动化、**编排多个快速子智能体**——最后一条是 subagent 概念的最早官方表述之一）。客户案例中 StudyFetch 的语音 AI 导师（工具驱动 UI、追踪进度、导航课件，正反馈 +42%）是「实时语音 + 工具驱动 UI」类 Agent 产品的早期对标案例。

---

Tool use, which enables Claude to interact with external tools and APIs, is now generally available across the entire Claude 3 model family on the Anthropic Messages API, Amazon Bedrock, and Google Cloud's Vertex AI.

工具使用（tool use）让 Claude 能与外部工具和 API 交互，现已在 Claude 3 全系模型上正式可用（GA），覆盖 Anthropic Messages API、Amazon Bedrock 和 Google Cloud 的 Vertex AI。

With tool use, Claude can perform tasks, manipulate data, and provide more dynamic—and accurate—responses.

借助工具使用，Claude 可以执行任务、操作数据，并给出更动态、也更准确的回应。

## Tool use

## 工具使用

Define a toolset for Claude and specify your request in natural language.

为 Claude 定义一个工具集，然后用自然语言说明你的请求。

Claude will then select the appropriate tool to fulfill the task and, when appropriate, execute the corresponding action:

Claude 会选择合适的工具来完成任务，并在恰当时执行相应的动作：

- **Extract structured data from unstructured text**: Pull names, dates, and amounts from invoices to reduce manual data entry.

- **从非结构化文本中提取结构化数据**：从发票里抽出名字、日期和金额，减少手工录入。

- **Convert natural language requests into structured API calls**: Enable teams to self-serve common actions (e.g., "cancel subscription") with simple commands.

- **把自然语言请求转成结构化 API 调用**：让团队用简单命令自助完成常见操作（如「取消订阅」）。

- **Answer questions by searching databases or using web APIs**: Provide instant, accurate responses to customer inquiries in support chatbots.

- **通过查询数据库或调用 Web API 来回答问题**：在客服机器人里对客户询问给出即时、准确的答复。

- **Automate simple tasks through software APIs**: Save time and minimize errors in data entry or file management.

- **通过软件 API 自动化简单任务**：在数据录入或文件管理中省时间、少出错。

- **Orchestrate multiple fast Claude subagents for granular tasks**: Automatically find the optimal meeting time based on attendee availability.

- **编排多个快速的 Claude 子智能体处理细粒度任务**：根据与会者的空闲时间自动找出最优会议时间。

## Improved developer experience

## 更好的开发者体验

To make it easier to leverage the intelligence of the Claude 3 models with tools, we've also built in features that help developers further customize the end-user experience.

为了让开发者更容易借助工具发挥 Claude 3 系列模型的智能，我们还内置了一些帮助进一步定制最终用户体验的特性。

- **Tool use with streaming reduces wait times to create more engaging interactions**: Streaming enables real-time responses in applications like customer support chatbots for smoother, more natural conversations.

- **流式工具调用缩短等待时间、带来更吸引人的交互**：流式让客服机器人这类应用能实时响应，对话更流畅自然。

- **Forced tool use allows developers to instruct Claude on tool selection**: Developers can specify which tools Claude should use or leave the choice with Claude, helping create more targeted and efficient applications.

- **强制工具使用允许开发者指定工具选择**：开发者可以指定 Claude 必须用哪个工具，也可以把选择权留给 Claude，从而构建更有针对性、更高效的应用。

- **Tools also work with images**: Claude can incorporate image inputs in live applications.

- **工具也支持图像**：Claude 可以在线上应用中结合图像输入使用工具。

During our beta many developers used Opus to build sophisticated user-facing assistants.

在 beta 期间，许多开发者用 Opus 构建面向用户的复杂助手。

To further enhance this experience, Opus will now include `<thinking>` tags in its outputs, clarifying Claude's reasoning and simplifying the debugging process for developers.

为进一步增强这种体验，Opus 现在会在输出中包含 `<thinking>` 标签，把 Claude 的推理讲清楚，简化开发者的调试过程。

Our Claude 3 models are currently unable to support parallel tool calls.

我们的 Claude 3 模型目前**尚不支持并行工具调用**。

## Customer spotlight: StudyFetch

## 客户案例：StudyFetch

AI-native learning platform StudyFetch uses Claude's tool use capabilities to power its personalized AI tutor, Spark.E.

AI 原生学习平台 StudyFetch 用 Claude 的工具使用能力驱动其个性化 AI 导师 Spark.E。

By integrating tools to track student progress, navigate course materials and lectures, and create interactive user interfaces, StudyFetch has created a more engaging educational environment for students globally.

通过集成「追踪学生进度、导航课程材料与讲座、创建交互式用户界面」等工具，StudyFetch 为全球学生打造了更有吸引力的学习环境。

"Claude with tool use is accurate and cost-effective, and now powers our live voice-enabled AI tutoring sessions. Within just a few days, we integrated tools into our platform," said Ryan Trattner, CTO and Co-Founder at StudyFetch.

StudyFetch CTO 兼联合创始人 Ryan Trattner 说：「带工具使用的 Claude 准确且划算，现在驱动着我们的实时语音 AI 辅导会话。我们只花了几天就把工具集成进了平台。」

"As a result, our AI tutor, Spark.E, acts agentically—displaying interactive UIs, tracking student progress in context, and navigating through lectures and materials. Since implementing Claude with tool use, we've observed a 42% increase in positive human feedback."

「结果是，我们的 AI 导师 Spark.E 表现得非常有『智能体范』——展示交互式 UI、在上下文中追踪学生进度、在讲座和材料中导航。自从接入带工具使用的 Claude，我们观察到正面人工反馈增加了 42%。」

## Customer spotlight: Intuned

## 客户案例：Intuned

Intuned, the browser automation platform, uses Claude to power data extraction within their cloud platform.

浏览器自动化平台 Intuned 用 Claude 驱动其云平台内的数据提取。

With AI-powered data extraction, Intuned is able to drastically improve the developer experience in building and executing more reliable browser automations.

借助 AI 驱动的数据提取，Intuned 大幅改善了构建和执行更可靠浏览器自动化的开发者体验。

"Claude 3 Haiku with tool use has been a game changer for us. After accessing the model and running our benchmarks on it, we realized the quality, speed, and price combination is unmatched," said Faisal Ilaiwi, Co-Founder at Intuned.

Intuned 联合创始人 Faisal Ilaiwi 说：「带工具使用的 Claude 3 Haiku 对我们是颠覆性的。拿到模型跑完基准测试后，我们意识到它的质量、速度、价格组合无可匹敌。」

"Haiku is helping us scale our customers' data extraction tasks to a completely new level."

「Haiku 正帮我们把客户的数据提取任务扩展到全新的量级。」

## Customer spotlight: Hebbia

## 客户案例：Hebbia

Hebbia is building the AI knowledge worker for leading financial and legal services firms.

Hebbia 在为头部金融和法律服务公司构建 AI 知识工作者。

They use Claude 3 Haiku to help power several complex, multi-step customer workflows.

他们用 Claude 3 Haiku 驱动若干复杂的多步客户工作流。

"We leverage Claude 3 Haiku for generating live suggestions, automating prompt writing, and extracting key metadata from long documents," shared Divya Mehta, Product Manager at Hebbia.

Hebbia 产品经理 Divya Mehta 分享道：「我们用 Claude 3 Haiku 生成实时建议、自动撰写提示词、从长文档中提取关键元数据。」

"Claude 3 Haiku's tool use feature has unlocked capabilities and speed for our platform to generate reliable suggestions and prompts in real-time."

「Claude 3 Haiku 的工具使用特性为我们的平台解锁了实时生成可靠建议和提示词的能力与速度。」

## Get started

## 快速上手

You can get started with tool use today on the Anthropic Messages API, Amazon Bedrock, and Google Cloud's Vertex AI.

你今天就可以在 Anthropic Messages API、Amazon Bedrock 和 Google Cloud Vertex AI 上开始使用工具功能。

To learn more, explore our documentation, tool use tutorial, and Anthropic Cookbooks on tool use.

想了解更多，请查阅我们的文档、工具使用教程和 Anthropic Cookbook。

---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| tool use | 工具使用 | 2024-05 在 Claude 3 全系 GA |
| generally available (GA) | 正式可用 | 从 beta 毕业 |
| forced tool use | 强制工具使用 | 开发者可指定必须调用某工具（今天的 tool_choice） |
| streaming | 流式 | 工具调用与流式响应结合以降延迟 |
| `<thinking>` tags | 思考标签 | 2024 年 Opus 暴露推理的方式（extended thinking 的前身） |
| parallel tool calls | 并行工具调用 | **当时不支持**——时间线知识点 |
| subagents | 子智能体 | 「编排多个快速子智能体」是该概念最早的官方表述之一 |
| act agentically | 表现出智能体行为 | StudyFetch 引言里的早期用法 |
