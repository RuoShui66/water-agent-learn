# B32_Building AI agents for the enterprise_为企业构建 AI 智能体

> 原文：https://claude.com/blog/building-ai-agents-for-the-enterprise
> 来源：Anthropic Claude Blog（分类：Enterprise ｜ 白皮书导览页）｜发布日期：2026-04-30
> 原文存档：[Markdown](原文/B32_building-ai-agents-for-the-enterprise_原文.md)
> ⚠️ 本篇是**白皮书导览页**（约 290 词）：正文是完整指南的目录式摘要，三大支柱详情在可下载的 guide 里。

## 📌 本篇速览

- 📅 2026-04-30　｜　⏱ 原文约 290 词（逐句精读约 5 分钟）
- 🏷 企业 AI 转型三支柱、agentic thinking divide、复利 vs 平台期、Claude Cowork 六个月部署框架
- 🗂 [返回目录](00_目录与阅读进度.md)

企业侧宏观叙事的导览页。背景数据：Anthropic Economic Index（2025-09）显示美国 40% 员工报告工作中使用 AI（2023 年为 20%）。核心问题：AI 带来的是**持久优势还是一个季度就见顶的增量收益**？领先企业的差异：把 agentic AI 嵌入员工工作方式、流程运转和产品可能性，**把组织知识编码进随时间复利的系统**——竞争对手难以复制。指南五块：跨越「agentic thinking divide」（为什么有的部署复利、有的停滞）；用反映组织实际工作方式的 AI 给员工提能；压缩信息密集流程但不牺牲人在环判断；构建创造收入（而非只降成本）的新产品能力；Claude Cowork 六个月部署框架 + 欧莱雅/Lyft/乐天案例。

---

Our September 2025 Anthropic Economic Index found that in the U.S., 40 percent of employees report using AI at work, up from 20 percent in 2023.

我们 2025 年 9 月的 Anthropic 经济指数发现：美国 40% 的员工报告在工作中使用 AI，2023 年这个数字是 20%。

While these are significant gains, a looming question remains: will AI produce lasting advantages or incremental gains that plateau within a quarter?

涨幅可观，但一个悬而未决的问题仍在：AI 带来的是持久优势，还是一个季度内就进入平台期的增量收益？

The enterprises pulling ahead are doing something different.

正在领先的企业做的事情不一样。

They're embedding agentic AI into how employees work, how processes run, and what products are possible.

他们把 agentic AI 嵌入员工的工作方式、流程的运转方式，以及产品的可能性边界。

They're encoding institutional knowledge into systems that compound over time, and they're seeing returns that are difficult for competitors to replicate.

他们把组织知识编码进随时间复利的系统，收获的是竞争对手难以复制的回报。

To help leaders chart this path, we put together a guide on the three pillars of enterprise AI transformation, with examples from organizations doing this work today: L'Oreal, Lyft, and Rakuten.

为帮助管理者规划这条路，我们整理了一份企业 AI 转型三支柱指南，附有正在实践的组织案例：欧莱雅、Lyft、乐天。

The guide also covers how to bring these capabilities to every team in your organization with Claude Cowork, without requiring a custom build for each one.

指南还讲了如何用 Claude Cowork 把这些能力带给组织里的每个团队——无需为每个团队定制开发。

In this guide, we share:

指南内容包括：

- How to overcome the "agentic thinking divide" and why some AI deployments compound while others stall

- 如何跨越「agentic 思维鸿沟」——为什么有的 AI 部署会复利、有的会停滞

- Best practices for upskilling employees with AI that reflects how your organization actually works

- 用反映组织真实工作方式的 AI 为员工提能的最佳实践

- Examples of how organizations can compress information-dense processes without sacrificing human-in-the-loop judgement and expertise

- 组织如何压缩信息密集的流程、又不牺牲人在环的判断与专长

- Guidance for building new product capabilities that generate revenue, not just reduce cost

- 构建**创造收入**（而非只是降本）的新产品能力的指引

- A six-month deployment framework for rolling out Claude Cowork

- Claude Cowork 的六个月部署框架

- Customer stories from L'Oreal, Lyft, and Rakuten

- 欧莱雅、Lyft、乐天的客户故事

The companies getting the biggest returns from AI are being deliberate about how they teach it to employees, where they apply it, and what they build next.

从 AI 获得最大回报的公司，都在有意识地设计：怎么教给员工、用在哪里、接下来构建什么。

---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| Anthropic Economic Index | Anthropic 经济指数 | 40% 员工用 AI（2023: 20%）数据出处 |
| agentic thinking divide | agentic 思维鸿沟 | 部署复利 vs 停滞的分水岭 |
| compound over time | 随时间复利 | 组织知识编码进系统的回报形态 |
| human-in-the-loop | 人在环 | 流程压缩的底线 |
| revenue, not just reduce cost | 创收而非只降本 | 产品能力建设的标尺 |
