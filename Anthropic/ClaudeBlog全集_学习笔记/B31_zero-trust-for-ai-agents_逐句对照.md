# B31_Zero Trust for AI agents_AI 智能体的零信任

> 原文：https://claude.com/blog/zero-trust-for-ai-agents
> 来源：Anthropic Claude Blog（分类：Security ｜ 白皮书导览页）｜发布日期：2026-05-27
> 原文存档：[Markdown](原文/B31_zero-trust-for-ai-agents_原文.md)
> ⚠️ 本篇是**白皮书导览页**（约 380 词）：正文是完整指南的目录式摘要，完整框架在可下载的 guide 里。

## 📌 本篇速览

- 📅 2026-05-27　｜　⏱ 原文约 380 词（逐句精读约 6 分钟）
- 🏷 Zero Trust、AI 加速攻防、agent 威胁面、三层成熟度框架、八阶段实施、Agentic SOAR
- 🗂 [返回目录](00_目录与阅读进度.md)

Agent 安全的**威胁模型总览**。核心判断：前沿模型把「漏洞→利用」的时间线从数月压缩到数小时——攻防双方同时加速，且这**对部署 Agent 的组织重要两次**：基础设施本身暴露于 AI 加速的进攻，Agent 又引入了「解读目标、选择工具、执行多步操作」的自治性——传统访问控制拦不住 Agent 滥用合法权限。**Zero Trust 三句话**（trust nothing, verify everything, assume breach）需要为智能体系统重塑：密码学根植的身份、按任务收窄的权限、防投毒的记忆、以自治攻击者速度运转的防御。指南五块内容：Agent 特有安全考量（工具访问/自主决策/上下文持久化/多智能体协调）、威胁景观（**prompt injection、tool poisoning、身份与权限滥用、memory poisoning、供应链攻击**——这五个名词值得背）、三层框架（Foundation/Advanced/Optimized 按成熟度与风险偏好映射）、八阶段实施工作流（身份→权限收窄→沙箱→输入输出控制→记忆防护）、Agentic SOAR（用智能体跑安全运营，快过 AI 加速的攻击者）+ 医疗/金融/政府合规对齐。

---

Frontier AI models are compressing the timeline between vulnerability and exploit from months to hours.

前沿 AI 模型正把「漏洞」到「利用」之间的时间线从数月压缩到数小时。

Defenders who adopt these tools find and fix bugs faster; attackers who adopt them, or who simply wait for defenders' patches and reverse-engineer them into exploits, move faster too.

采用这些工具的防守方发现和修复 bug 更快了；采用它们的攻击方——或干脆等防守方发补丁、再把补丁逆向成利用工具的人——也更快了。

This is not a future concern: models can already find serious vulnerabilities that traditional tooling and human reviewers have missed for years.

这不是未来的担忧：模型已经能找到传统工具和人类审查者漏了多年的严重漏洞。

This acceleration matters twice for any organization deploying agents.

对任何部署智能体的组织，这种加速**重要两次**。

The infrastructure your agents run on is exposed to AI-accelerated offense like the rest of your estate, and the agents themselves introduce autonomy to interpret goals, select tools, and execute multi-step operations.

你的智能体运行其上的基础设施，和你其余资产一样暴露在 AI 加速的进攻之下；而智能体本身又引入了自治性——解读目标、选择工具、执行多步操作。

Traditional access controls won't prevent agents from misusing legitimate permissions, and monitoring needs to account for attacks designed to succeed through persistence rather than exploitation.

传统访问控制拦不住智能体滥用合法权限；监控也要考虑那些靠「潜伏坚持」而非「漏洞利用」取胜的攻击。

Zero Trust—trust nothing, verify everything, and assume breach has already occurred—gives security leaders a proven foundation to address this.

零信任——什么都不信、一切皆验证、假设入侵已经发生——为安全负责人提供了应对这一切的成熟地基。

But the principles need new shape for agentic systems: identities that are cryptographically rooted, permissions scoped per task, memory protected against poisoning, and defensive operations that run at the speed of autonomous attackers.

但这些原则需要为智能体系统重塑形态：密码学根植的身份、按任务收窄的权限、防投毒保护的记忆，以及以自治攻击者的速度运转的防御行动。

To help security and risk leaders build for this shift, we put together a practical framework for deploying autonomous AI agents in the enterprise.

为帮助安全与风险负责人为这一转变做建设，我们整理了一套在企业部署自治 AI 智能体的实用框架。

In this guide, we share:

指南内容包括：

- The security considerations unique to agentic systems, including tool access, autonomous decision-making, context persistence, and multi-agent coordination

- 智能体系统特有的安全考量：工具访问、自主决策、上下文持久化、多智能体协调

- The current threat landscape for agents, including prompt injection, tool poisoning, identity and privilege abuse, memory poisoning, and supply chain attacks

- 当前的智能体威胁景观：提示注入、工具投毒、身份与权限滥用、记忆投毒、供应链攻击

- A three-tier Zero Trust framework (Foundation, Advanced, and Optimized) mapped to organizational maturity and risk tolerance

- 三层零信任框架（基础 / 进阶 / 优化），按组织成熟度与风险容忍度映射

- An eight-phase implementation workflow covering identity, access scoping, sandboxing, input and output controls, and memory safeguards

- 八阶段实施工作流：身份、访问收窄、沙箱、输入输出控制、记忆防护

- How to run agentic security operations (Agentic SOAR) fast enough to contend with AI-accelerated attackers

- 如何把智能体安全运营（Agentic SOAR）跑得够快，与 AI 加速的攻击者抗衡

- Compliance alignment for regulated industries including healthcare, finance, and government

- 医疗、金融、政府等受监管行业的合规对齐

---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| Zero Trust | 零信任 | trust nothing / verify everything / assume breach |
| AI-accelerated offense | AI 加速的进攻 | 漏洞→利用从数月到数小时 |
| tool poisoning | 工具投毒 | 五大威胁之一：被篡改的工具定义/结果 |
| memory poisoning | 记忆投毒 | 五大威胁之一：污染 Agent 的持久记忆 |
| identity and privilege abuse | 身份与权限滥用 | Agent 滥用合法权限，传统 ACL 拦不住 |
| persistence | 潜伏/坚持 | 靠持续存在而非漏洞利用取胜的攻击 |
| cryptographically rooted identity | 密码学根植的身份 | 零信任在 Agent 场景的重塑之一 |
| permissions scoped per task | 按任务收窄的权限 | 对应 B23 的 JIT 思路 |
| Agentic SOAR | 智能体安全编排与响应 | 用 Agent 跑防御，速度对齐攻击者 |
