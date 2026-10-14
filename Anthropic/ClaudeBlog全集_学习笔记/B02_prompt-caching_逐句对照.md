# B02_Prompt caching with Claude_Claude 的提示词缓存

> 原文：https://claude.com/blog/prompt-caching
> 来源：Anthropic Claude Blog（分类：Platform ｜ 产品：Claude API）｜发布日期：2025-08-14 页面（原始公告 2024-08，2024-12-17 GA）
> 原文存档：[Markdown](原文/B02_prompt-caching_原文.md)

## 📌 本篇速览

- 📅 2024-08 公告 / 2024-12-17 GA　｜　⏱ 原文约 680 词（逐句精读约 10 分钟）
- 🏷 prompt caching、成本 -90%、延迟 -85%、cache write/read 定价、agentic search
- 🗂 [返回目录](00_目录与阅读进度.md)

Prompt caching 官方发布文，与 [Harness 逐句对照系列的「prompt caching is everything」](../../Harness延伸阅读_双语精读/)互为表里：那篇讲**为什么缓存塑造 harness 设计**，这篇给**原始数字与定价模型**。核心数字：长提示词**成本最高降 90%、延迟最高降 85%**；三个实测：10 万 token 书籍问答 TTFT 11.5s→2.4s（-79%，成本 -90%）、万 token many-shot 1.6s→1.1s（-31%，成本 -86%）、长系统提示词 10 轮对话 ~10s→~2.5s（-75%，成本 -53%）。**定价模型必背**：cache write = 基础输入价 ×1.25，cache read = ×0.10——这两个系数是一切「为什么 harness 要 append-only、为什么系统提示词不能中途变」论证的经济学根基。官方点名的六个适用场景里，「conversational agents」「agentic search and tool use」是 Agent 应用最常见的两条主路径。

---

***Update:** Prompt caching is Generally Available on the Anthropic API. Prompt caching is also available in preview in Amazon Bedrock and on Google Cloud's Vertex AI. (December 17, 2024)*

***更新：**提示词缓存已在 Anthropic API 上正式可用（GA），并在 Amazon Bedrock 和 Google Cloud Vertex AI 上提供预览。（2024 年 12 月 17 日）*

Prompt caching, which enables developers to cache frequently used context between API calls, is now available on the Anthropic API.

提示词缓存（prompt caching）让开发者能在 API 调用之间缓存高频使用的上下文，现已在 Anthropic API 上可用。

With prompt caching, customers can provide Claude with more background knowledge and example outputs—all while reducing costs by up to 90% and latency by up to 85% for long prompts.

借助提示词缓存，客户可以给 Claude 提供更多背景知识和示例输出——同时对长提示词把成本降低最多 90%、延迟降低最多 85%。

Prompt caching is available today in public beta for Claude 3.5 Sonnet, Claude 3 Opus, and Claude 3 Haiku.

提示词缓存今天起对 Claude 3.5 Sonnet、Claude 3 Opus 和 Claude 3 Haiku 开放公开测试。

## When to use prompt caching

## 什么时候用提示词缓存

Prompt caching can be effective in situations where you want to send a large amount of prompt context once and then refer to that information repeatedly in subsequent requests, including:

当你想把大量提示词上下文发送一次、然后在后续请求中反复引用这些信息时，提示词缓存会很有效，包括：

- **Conversational agents:** Reduce cost and latency for extended conversations, especially those with long instructions or uploaded documents.

- **对话型智能体：**降低长对话的成本和延迟，尤其是带长指令或上传文档的对话。

- **Coding assistants:** Improve autocomplete and codebase Q&A by keeping a summarized version of the codebase in the prompt.

- **编程助手：**把代码库的摘要版保留在提示词里，改进自动补全和代码库问答。

- **Large document processing:** Incorporate complete long-form material including images in your prompt without increasing response latency.

- **大文档处理：**把包括图像在内的完整长篇材料放进提示词，而不增加响应延迟。

- **Detailed instruction sets:** Share extensive lists of instructions, procedures, and examples to fine-tune Claude's responses. Developers often include a few examples in their prompt, but with prompt caching you can get even better performance by including dozens of diverse examples of high quality outputs.

- **详尽指令集：**提供大量指令、流程和示例来微调 Claude 的回应。开发者通常只在提示词里放几个示例，但有了缓存，你可以放几十个多样化的高质量输出示例，获得更好的效果。

- **Agentic search and tool use:** Enhance performance for scenarios involving multiple rounds of tool calls and iterative changes, where each step typically requires a new API call.

- **智能体搜索与工具使用：**提升多轮工具调用和迭代修改场景的性能——这些场景里每一步通常都要发起一次新的 API 调用。

- **Talk to books, papers, documentation, podcast transcripts, and other long-form content:** Bring any knowledge base alive by embedding the entire document(s) into the prompt, and letting users ask it questions.

- **与书籍、论文、文档、播客转录等长内容对话：**把整份文档嵌进提示词，让用户直接对它提问，让任何知识库「活」起来。

Early customers have seen substantial speed and cost improvements with prompt caching for a variety of use cases—from including a full knowledge base to 100-shot examples to including each turn of a conversation in their prompt.

早期客户已经在各种用例中看到显著的速度和成本改善——从放入完整知识库、到 100-shot 示例、再到把对话每一轮都放进提示词。

| **用例** | **无缓存延迟（首 token 时间）** | **有缓存延迟（首 token 时间）** | **成本降幅** |
|---|---|---|---|
| 与一本书对话（10 万 token 缓存提示词） | 11.5s | 2.4s（-79%） | -90% |
| Many-shot 提示（1 万 token 提示词） | 1.6s | 1.1s（-31%） | -86% |
| 多轮对话（长系统提示词的 10 轮对话） | ~10s | ~2.5s（-75%） | -53% |

### How we price cached prompts

### 缓存提示词如何定价

Cached prompts are priced based on the number of input tokens you cache and how frequently you use that content.

缓存提示词的定价基于你缓存的输入 token 数量，以及你使用这些内容的频率。

Writing to the cache costs 25% more than our base input token price for any given model, while using cached content is significantly cheaper, costing only 10% of the base input token price.

对任一模型，**写入缓存比基础输入 token 价贵 25%**；而**读取缓存内容便宜得多，只需基础输入价的 10%**。

| 模型 | 基础输入 | 缓存写入 | 缓存读取 | 输出 |
|---|---|---|---|---|
| Claude 3.5 Sonnet（200K 窗口） | $3 / MTok | $3.75 / MTok | $0.30 / MTok | $15 / MTok |
| Claude 3 Opus（200K 窗口） | $15 / MTok | $18.75 / MTok | $1.50 / MTok | $75 / MTok |
| Claude 3 Haiku（200K 窗口） | $0.25 / MTok | $0.30 / MTok | $0.03 / MTok | $1.25 / MTok |

*（表：2024 年发布时的定价；系数关系 write=×1.25、read=×0.10 沿用至今。）*

### Customer spotlight: Notion

### 客户案例：Notion

Notion is adding prompt caching to Claude-powered features for its AI assistant, Notion AI.

Notion 正在把提示词缓存加入其 AI 助手 Notion AI 中由 Claude 驱动的功能。

With reduced costs and increased speed, Notion is able to optimize internal operations and create a more elevated and responsive user experience for their customers.

凭借更低的成本和更快的速度，Notion 得以优化内部运营，并为客户打造更高级、更灵敏的用户体验。

> We're excited to use prompt caching to make Notion AI faster and cheaper, all while maintaining state-of-the-art quality.

> 我们很兴奋能用提示词缓存让 Notion AI 更快、更便宜，同时保持最先进的质量。

— Simon Last, Co-founder at Notion

——Simon Last，Notion 联合创始人

### Get started

### 快速上手

To start using the prompt caching public beta on the Anthropic API, explore our documentation and pricing page.

要在 Anthropic API 上开始使用提示词缓存公开测试版，请查阅我们的文档和定价页。

---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| prompt caching | 提示词缓存 | API 调用之间复用高频上下文 |
| cache write / cache read | 缓存写入 / 读取 | 定价系数：write ×1.25，read ×0.10 |
| time to first token (TTFT) | 首 token 时间 | 延迟主指标：书籍问答 11.5s→2.4s |
| many-shot prompting | 多示例提示 | 缓存使「几十个示例」变得经济可行 |
| agentic search and tool use | 智能体搜索与工具使用 | 每步一次 API 调用的场景，缓存收益最大 |
| MTok | 百万 token | 定价单位 |
