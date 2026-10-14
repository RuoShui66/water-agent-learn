# 06_Agent Harness Engineering_智能体运行框架工程（Addy Osmani）

> 原文：https://addyosmani.com/blog/agent-harness-engineering/
> 作者：Addy Osmani（Google，《Learning JavaScript Design Patterns》作者）｜发布日期：2026-04-19

## 📌 本篇速览

- 📅 2026-04-19
- ⭐ ★★★★★ **公开圈最好的 harness 综述，非官方材料里的第一选择** —— 它给了两个直接可用的思维工具：**「棘轮法则」**（每个错误变成一条规则）和**「从行为倒推组件」**的设计表。综述里「harness 不缩小，只是转移」这句判断就出自这篇。
- 🏷 the ratchet、working backwards from behaviour、context rot、Ralph Loop、Harness-as-a-Service、AGENTS.md
- 🗂 [返回专题目录](00_目录.md)　·　🔗 [Harness 最佳实践现状综述](../02_Agent-Harness最佳实践现状综述_2026-08.md)

> 本文是双语精读与转述，不是逐句全文翻译；英文保留关键术语与短表述，完整正文请点原文链接。

## 一句话摘要

**`coding agent = AI model(s) + harness`** —— 智能体的质量取决于围绕模型的基础设施远多于模型本身，所以 *"a decent model with a great harness beats a great model with a bad harness"*（一个不错的模型配上出色的 harness，胜过一个出色的模型配上糟糕的 harness）。

## 核心内容

### 1. harness 到底包含什么

作者把 harness 定义为「模型之外的一切」，清单值得当检查表用：

- 系统提示词、`AGENTS.md`、skill 文件、子智能体提示词
- 工具、skills、带描述的 MCP servers
- 基础设施（文件系统、沙箱、浏览器）
- 编排逻辑（子智能体派生、交接、路由）
- 用于确定性执行的 hooks 与中间件
- 可观测性系统

关键判断：**模型只有在 harness 提供了状态、工具执行、反馈循环与可强制的约束之后，才成为「智能体」。**

### 2. 「Skill issue」重构（The "Skill Issue" Reframe）

把智能体的失败**当成配置问题而不是模型能力问题**。作者给的证据：

- 同一个 **Claude Opus 4.6**，在 Claude Code 里的得分**低于**它在工具更好、提示更紧的自建 harness 里的得分。
- **Viv 团队只改 harness、不换模型**，把一个编程智能体从 Terminal Bench 2.0 的 **Top 30 拉到 Top 5**。

这是综述里「把失败归咎于模型能力，通常是 harness 配置问题」的原始论据之一。

### 3. 棘轮法则（The Ratchet: Every Mistake Becomes a Rule）★

本篇最值得带走的一条方法论：**把智能体的每个错误当成永久信号，而不是一次性事故。**

每次失败必须沉淀成三者之一：
1. `AGENTS.md` 里的一条规则
2. 执行流水线里的一个 hook
3. 评审子智能体里的一个检查项

判据一句话：

> *"Every line in a good `AGENTS.md` should be traceable back to a specific thing that went wrong."*
> 好的 `AGENTS.md` 里的每一行，都应该能追溯到某件具体出过错的事。

**面试用法**：这条给了「你怎么迭代 harness」一个可执行答案——不是凭感觉加提示词，而是错误驱动的单向棘轮。

### 4. 从行为倒推组件（Working Backwards from Behaviour）★

先定义想要的行为，再倒推该装哪个组件。这张表可以直接当 harness 设计的对照表：

| 想要的行为 | 该装的组件 |
|---|---|
| **Durable state**（持久状态） | 文件系统 + Git |
| **General-purpose execution**（通用执行） | Bash + 代码执行 |
| **Safe execution**（安全执行） | 沙箱 + 默认工具链 |
| **Continual learning**（持续学习） | 记忆文件、web search、MCP 工具 |
| **Context management**（上下文管理） | compaction、工具调用输出外置、skill 渐进披露 |
| **Long-horizon execution**（长时程执行） | Ralph Loops、规划、验证、planner/evaluator 分离 |
| **Enforcement**（强制） | 生命周期各点的 hooks |

配套的细节论断：

- **文件系统与 Git 是地基原语**：文件系统负责把工作从上下文里卸载出去、提供智能体与人之间的协调面；Git 补上版本化与回滚。
- **Bash + 代码执行 > 为每个场景预建工具**：智能体擅长 shell，给它组合能力比给它成品工具更有效。
- **工具纪律**：*"ten focused tools outperform fifty overlapping ones"*（十个聚焦的工具胜过五十个重叠的工具）。
- ⚠️ **MCP servers 是被信任的文本**——恶意 server 是真实安全风险。

### 5. 对抗上下文腐烂（Battling Context Rot）

模型随上下文填满而退化。三招：

| 技术 | 做法 |
|---|---|
| **Compaction** | 智能地摘要并卸载较早的上下文 |
| **Tool-call offloading** | 把大输出（如 2,000 行日志）挪到文件系统 |
| **Progressive disclosure** | 只在需要时加载工具 / MCP |

作者转述 Anthropic 的关键结论：长任务上 *"compaction alone wasn't sufficient"*（光靠压缩不够）——有时需要**完整的上下文重置 + 结构化交接文件**。

### 6. 长时程执行的五种模式

- **Ralph Loops**：用 hook 拦截「完成」企图，在**全新上下文窗口**里重新注入原始提示词
- **Planning**：把目标拆成步骤序列，支持 plan 文件
- **Self-verification**：跑预定义测试套件，失败结果回灌给模型
- **Planner / generator / evaluator splits**：生成与评估分离，因为**智能体自评时倾向偏高**（agents skew positive self-grading）
- **Sprint contracts**：写代码之前先谈妥「done」的条件

### 7. Hooks：强制层（The Enforcement Layer）

在 pre-tool-call、post-file-edit、before-commit、on-session-start 等生命周期点执行的脚本。核心原则：

> **"Success is silent, failures are verbose."**（成功静默，失败聒噪。）

类型检查、lint、测试失败要立刻浮到智能体面前。

### 8. `AGENTS.md` 的写法

- 它是**每一轮都会落进系统提示词的 markdown 规则手册**
- **控制在 60 行以内**（引用 HumanLayer 的实践基准）
- 定位是**飞行员检查单，不是风格指南**
- 每条规则都要能追溯到一次过往失败或一条硬约束（呼应棘轮法则）

### 9. Harness 不缩小，只是转移（Harnesses Don't Shrink, They Move）★

这是综述那句判断的原始出处：

> 每个 harness 组件**都编码了一条「模型自己做不到什么」的假设**。更好的模型会消灭一部分脚手架，但**同时制造出需要新组件的新失败模式**。

配套的一个重要洞察——**模型-harness 训练回路（The Model-Harness Training Loop）**：

> 现代模型在后训练阶段就**把 harness 放进了回路里**，因此会专门变得更擅长 harness 意图中的动作（文件系统操作、bash、规划、子智能体派发）。这会造成对**特定 harness 设计的过拟合**。

这条解释了为什么同一个模型换 harness 差距巨大：模型是**对着某一类 harness 训练出来的**。

### 10. Harness-as-a-Service（HaaS）

行业从「在 LLM API 上开发」转向「在 harness API 上开发」。Claude Agent SDK、Codex SDK、OpenAI Agents SDK 提供 loop、工具、上下文管理、hooks、沙箱，你只在**四根支柱**上做定制：**system prompt、tools、context、subagents**。

引 Viv 的话：

> *"good agent building is an exercise in iteration. You can't do iterations if you don't have a v0.1."*
> 做好智能体是一场迭代练习——没有 v0.1 就无法迭代。

### 11. 未来方向

顶级编程智能体（Claude Code、Cursor、Codex、Aider、Cline）尽管底层模型不同，**却在 harness 模式上趋同**。开放问题：并行智能体在共享代码库上的编排、智能体分析 trace 自行修复 harness 问题、just-in-time 组装工具与上下文而非预先配置。

作者的收尾观察：harness 可能从「静态配置」演化为**「更接近编译器的东西」**（*something closer to a compiler*）。

## 可直接带走的工程结论

1. **每个错误都要落成一条规则、一个 hook 或一个评审检查项**——棘轮只能单向走。
2. **`AGENTS.md` 每行都要有出处**，控制在 60 行内；它是检查单不是风格指南。
3. **先定行为再选组件**，用第 4 节那张表反查自己缺什么。
4. **给 bash + 代码执行，别为每个场景预建工具**；工具要少而聚焦（10 > 50）。
5. **hooks 遵循「成功静默、失败聒噪」**。
6. **模型是对着 harness 训练的**——所以换 harness 的性能差距是结构性的，不是玄学。
7. **别自己造 loop**：从 SDK 起步，只在四根支柱上做定制。
8. **harness 复杂度不会消失，只会转移**——把预算留给新出现的失败模式。

## 与库内其他笔记的关系

- 它是对 [21_harness-design-long-running-apps](../Anthropic/Engineering全集_逐句对照/21_harness-design-long-running-apps_直观图解与学习笔记.md) 与 [15_effective-harnesses](../Anthropic/Engineering全集_逐句对照/15_effective-harnesses-for-long-running-agents_直观图解与学习笔记.md) 的跨厂商综述。
- 「harness 不缩小只是转移」与 [05_Fable 5 公告](05_claude-fable-5-mythos-5_双语精读.md) 的正反两条数字互为印证。
- `AGENTS.md` 那一节与 OpenAI 侧的「仓库即 harness」是同一问题的两种答案，见 [OpenAI 04_Harness-engineering](../OpenAI/最新/04_Harness-engineering_中文精读.md)。
- 同作者的续篇见 [07_Long-Running Agents](07_long-running-agents-osmani_双语精读.md)。
