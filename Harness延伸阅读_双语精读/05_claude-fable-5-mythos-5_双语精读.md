# 05_Claude Fable 5 and Claude Mythos 5_Fable 5 / Mythos 5 发布公告

> 原文：https://www.anthropic.com/news/claude-fable-5-mythos-5
> 来源：Anthropic 官方 News｜发布日期：2026-06-09

## 📌 本篇速览

- 📅 2026-06-09
- ⭐ ★★★★☆ **值得读，但要读得克制** —— 它的价值集中在**两句话**：官方首次在发布公告里说模型 "needs less scaffolding"，以及 file-based memory 对 Fable 5 的收益反而是 Opus 4.8 的三倍。这两句话看似矛盾，恰恰是「脚手架换形态」论断的直接证据。
- 🏷 less scaffolding、Slay the Spire 记忆基准、Pokémon FireRed vision-only harness、safeguards <5%
- 🗂 [返回专题目录](00_目录.md)　·　🔗 [Harness 最佳实践现状综述](../02_Agent-Harness最佳实践现状综述_2026-08.md)

> 本文是双语精读与转述，不是逐句全文翻译；英文保留关键术语与短表述，完整正文请点原文链接。

## 一句话摘要

Anthropic 同时发布 **Claude Fable 5**（带安全防护的通用版）与 **Claude Mythos 5**（面向获授权用户解除防护的版本），并首次在发布公告层面把「模型需要更少脚手架」写成卖点——但同一篇公告里，**记忆类脚手架的收益反而变大了**。

## 核心内容

### 1. 「Less scaffolding」这句话的准确出处与准确范围

这是本篇被引用最多、也最容易被放大解读的一句。官方原话是：

> *"It also needs less scaffolding: for example, previous Claude models struggled to play Pokémon FireRed even with harnesses that gave them additional helpful tools, but Fable 5 beat FireRed with a minimal, vision-only harness."*
>
> 它也需要更少的脚手架：比如以前的 Claude 模型即使配上给了额外有用工具的 harness，玩 Pokémon FireRed 仍然吃力，而 Fable 5 用一个**极简的、纯视觉的 harness** 就通关了 FireRed。

⚠️ **读法提醒**：这句话的论据是**游戏基准里的工具类脚手架**，不是「所有 harness 组件都该删」。公告本身**没有给出任何针对开发者的 harness 设计建议**——把它当成「删脚手架」的全面授权是过度解读。真正可操作的消融指令在 [03_cwc-long-running-agents](03_cwc-long-running-agents_双语精读.md) 的 README 里。

### 2. 与之并列的反向证据：记忆脚手架收益反而变大

同一篇公告里的 Slay the Spire 测试结果：

> 持久化的 **file-based memory** 给 Fable 5 带来的性能提升，是给 Opus 4.8 的**三倍**；Fable 到达游戏最终章的频率也高出**三倍**。

**这两条放在一起才是本篇的真正信息量**：

| 脚手架类型 | Claude 5 时代的走向 |
|---|---|
| **工具/行为类**（给模型补工具、逼它按流程走） | 收益下降，可以删（FireRed vision-only 即证据）|
| **记忆/状态类**（file-based memory、外置状态） | **收益上升**（Slay the Spire 3× 即证据）|

综述里「harness 从行为管教层转移到基础设施层」这个判断，最硬的一手证据就是这一对数字来自**同一篇公告**。

### 3. 基准与能力

- **FrontierCode**：在 **medium effort** 下取得前沿模型中的最高分（注意官方点名的是 medium 档，不是最高档）
- **Finance Benchmark（Hebbia）**：*"highest score of any model"*
- **Vision tasks**：新的 state of the art
- **Analytics**：*"first to break 90% on our core analytics benchmark"*（首次突破 90%）
- 总体口径：*"state-of-the-art on nearly all tested benchmarks"*

### 4. 安全防护触发率

> Safeguards trigger, on average, in **less than 5% of sessions.**（防护平均在**不到 5%** 的会话中触发。）

这个数字是「拒答处理必须成为一等代码路径」的量化依据：**平均每 20 个会话就有 1 个可能被打断**，生产系统必须内建 fallback 与重试中间件，而不是当异常处理。

### 5. 定价

> **$10 / 百万 input tokens，$50 / 百万 output tokens。**

### 6. ⚠️ 公告里**没有**的内容（重要的证伪）

为避免把综述里的说法误挂到这篇公告名下，核对结果如下——以下内容**均不在本公告中**：

- temperature / top_p / top_k / budget_tokens 的废弃与 400 错误
- 自适应思考（adaptive thinking）永远开启
- 上下文窗口大小
- 输出 token 比 Opus 级多约 30%

这些说法要么属于 API 文档层面，要么来自社区技术报告（综述里已标注为「据社区技术报告」）。**引用时不要写成「发布公告称」**——这是面试里容易被追问出处的地方。

## 可直接带走的工程结论

1. **「less scaffolding」的官方证据只覆盖工具类脚手架**，而且是游戏基准；不要当成删掉验收契约和记忆层的理由。
2. **记忆类脚手架在新模型上回报更高，不是更低**——模型越强越会用外部状态，这与直觉相反但有官方数字。
3. **effort 不是越高越好**：官方自己在 FrontierCode 上报的是 **medium effort** 成绩，这与社区评测「medium 53.4% > xhigh 43.6%」的方向一致。
4. **<5% 的防护触发率意味着 refusal fallback 是刚需**，长跑任务里这个概率会被会话数放大。
5. 引用数字前先确认层级：**公告 / API 文档 / 社区报告**三者不能混着说。

## 与库内其他笔记的关系

- 它是综述「脚手架换形态」论断的一手证据来源，正反两条都在这一篇里。
- 它的「删脚手架」主张，操作版本在 [03_cwc-long-running-agents](03_cwc-long-running-agents_双语精读.md) 的 *Re-simplify on model upgrades*。
- 它验证的「每个组件都编码一条能力假设」出自 [21_harness-design-long-running-apps](../Anthropic/Engineering全集_逐句对照/21_harness-design-long-running-apps_直观图解与学习笔记.md)。
- 记忆脚手架的托管化方向见 [01_New in Claude Managed Agents](01_new-in-claude-managed-agents_双语精读.md) 的 Dreaming。
