# 01_New in Claude Managed Agents_Claude 托管智能体的新能力

> 原文：https://claude.com/blog/new-in-claude-managed-agents
> 来源：Claude 产品博客（Product announcements）｜发布日期：2026-05-19

## 📌 本篇速览

- 📅 2026-05-19　｜　⏱ 官方标注约 5 分钟
- ⭐ ★★★★★ **必读** —— 这是 2026-03-24 harness 设计文里「手搓评估器」正式变成产品的那一刻，也是理解「哪些 harness 组件该外包给平台」的最直接材料。
- 🏷 Outcomes、Dreaming、multiagent orchestration、rubric grader、webhooks
- 🗂 [返回专题目录](00_目录.md)　·　🔗 [Harness 最佳实践现状综述](../02_Agent-Harness最佳实践现状综述_2026-08.md)

> 本文是双语精读与转述，不是逐句全文翻译；英文保留关键术语与短表述，完整正文请点原文链接。

## 一句话摘要

Anthropic 把长时程 harness 里最难自建的三块——**质量评判、跨会话记忆整理、多智能体编排**——做成了 Managed Agents 的托管能力（Outcomes、Dreaming、multiagent orchestration），开发者只需要写「什么算好」，不再需要自己搭评估循环。

## 核心内容

### 1. Outcomes（public beta）：把评估器变成产品

开发者写一份质量评分标准（**quality rubric**），由一个**独立的打分器（separate grader）** 评判产出。关键设计写在原文里只有一句话，但它就是 2026-03-24 那篇文章的核心论断：打分器**在自己的上下文窗口里评估**，因此不受任务智能体推理过程的影响（原文措辞：*"in its own context window, so it isn't influenced by the agent's reasoning"*）。

不达标时它不是给一个总分，而是**指出需要改哪里**，交回去重做。

官方给出的基准提升：

| 指标 | 提升 |
|---|---|
| 相对标准提示词的任务成功率 | 最多 +10 个百分点 |
| docx 文件生成任务成功率 | +8.4% |
| pptx 文件生成任务成功率 | +10.1% |

适用场景官方点名三类：**注重细节的任务**、**要求穷尽覆盖的任务**、**主观质量**（品牌语气、设计规范）。第三类正是三月文章里「审美无法化约成一个分数，但可以用编码了设计原则的评分标准来改进」的产品化。

### 2. Dreaming（research preview）：睡眠期记忆整理

一个**定时进程**，在会话之间回顾智能体的历史会话与记忆库，提取单个智能体自己看不见的模式——原文列了三类：**反复犯的错**、**智能体自己收敛出的工作流**、**团队共享的偏好**。然后它会**重构记忆**，让长时程工作与多智能体系统里的记忆保持高信噪比。

这是 2025-11 那篇文章里 `claude-progress.txt` 手写进度日志的托管升级版：光「只追加」是不够的，记忆需要定期 curation，否则会烂掉。

**注意可用性**：这是五项发布里**唯一仍在 research preview** 的，要填表申请。

### 3. Multiagent orchestration（public beta）：lead + specialist

一个 **lead agent** 把复杂任务拆块，委派给**各带独立模型、提示词和工具**的 specialist 子智能体。两个设计细节值得记：

- 子智能体**在共享文件系统上并行工作**，结果汇入 lead agent 的整体上下文——沿用了三月文章「通信全走文件、文件是跨智能体的外部状态」的设计；
- **全链路可追溯**：Claude Console 能看到哪个智能体、在什么顺序下、做了什么动作、以及它的推理。这替代了三月文章里「人工读评估器日志找分歧」的调优方式。

### 4. Webhooks

定义好 outcome 后，智能体完成时可以发 webhook 通知——无人值守长跑的收尾环节。

## 客户案例（均为客户自报数字，非第三方验证）

| 公司              | 用法                                            | 结果               |
| --------------- | --------------------------------------------- | ---------------- |
| Harvey（法律科技）    | 用 dreaming 协调法律文书起草与文档生成                      | 任务完成率提升约 **6 倍** |
| Netflix         | 多智能体编排并行分析数百个构建的日志                            | 跨数千个应用发现重复模式     |
| Spiral by Every | Haiku 做 lead，委派 Opus 子智能体起草；用 outcomes 强制编辑标准 | 并行起草 + 质量门控      |
| Wisedocs        | 用 outcomes 按内部规范做文档质量检查                       | 评审速度快 **50%**    |

Spiral 那一行是**模型按角色选配**的实例：便宜快的模型做编排，贵的模型做生成，评分器做守门——这比「一个模型通吃」省钱得多。

## 可直接带走的工程结论

1. **评判者必须有独立上下文窗口**，这不是风格选择而是产品级设计要求。
2. **记忆需要离线 curation 环节**，只追加的记忆库会退化。
3. **多智能体通信走共享文件系统**，不要走消息传递。
4. **给每个子智能体单独配模型/提示词/工具**，按任务难度选智能等级。
5. 编排系统必须**自带可追溯性**——哪个智能体、什么顺序、为什么这么做。

## 与库内其他笔记的关系

- 它产品化的是 [21_harness-design-long-running-apps](../Anthropic/Engineering全集_逐句对照/21_harness-design-long-running-apps_直观图解与学习笔记.md) 的评估器与编排。
- 它运行在 [23_managed-agents](../Anthropic/Engineering全集_逐句对照/23_managed-agents_直观图解与学习笔记.md) 的 brain/hands/session 底座上。
- Dreaming 对应 [15_effective-harnesses](../Anthropic/Engineering全集_逐句对照/15_effective-harnesses-for-long-running-agents_直观图解与学习笔记.md) 的进度文件。
