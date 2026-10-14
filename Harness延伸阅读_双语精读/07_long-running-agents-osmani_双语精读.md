# 07_Long-Running Agents_长时程智能体（Addy Osmani）

> 原文：https://addyosmani.com/blog/long-running-agents/
> 作者：Addy Osmani｜发布日期：2026-04-28

## 📌 本篇速览

- 📅 2026-04-28
- ⭐ ★★★★☆ **值得读，独特价值在「横向对照」** —— 这是唯一一篇把 **Anthropic / Cursor / Google 三家的长时程架构摆在一起比**的公开材料，能直接看出「架构趋同、命名各异」。三堵墙 + 五种生产模式可以当设计检查表。
- 🏷 三堵墙、Ralph loop、brain/hands/session、planner/worker/judge、memory drift、checkpoint-and-resume
- 🗂 [返回专题目录](00_目录.md)　·　🔗 [Harness 最佳实践现状综述](../02_Agent-Harness最佳实践现状综述_2026-08.md)

> 本文是双语精读与转述，不是逐句全文翻译；英文保留关键术语与短表述，完整正文请点原文链接。

## 一句话摘要

长时程智能体靠**外置持久状态、结构化交接、恢复机制**跨会话保持进度，从而让「委派更大的任务」在经济上变得可行——各家（Anthropic、Cursor、Google）的架构已经趋同，差异只在产品表面。

## 核心内容

### 1. 「Long-running」其实是三件不同的事

这个三分法很有用，因为面试里问「长时程」经常是在问其中一个：

| 维度 | 含义 |
|---|---|
| **Long-horizon reasoning**（长时程推理） | 多步、步步相依的规划 |
| **Long-running execution**（长时程执行） | 进程横跨数小时/数天，成千上万次模型调用 |
| **Persistent agency**（持久能动性） | 智能体保持身份、累积记忆、学习偏好 |

配套数据：**METR 追踪的「时间跨度」指标约每 7 个月翻一番**；按此外推，前沿智能体在 **2028 年**达到日级任务、**2034 年**达到年级任务。

经济性论证一句话：**10 分钟的智能体只能回答问题，10 小时的智能体可以「拥有一整个功能」**（own an entire feature）。

### 2. 三堵墙（Three Walls Every Long-Running Agent Hits）★

每个长时程智能体必然撞上的三堵墙，也是 harness 三大组件的存在理由：

1. **有限上下文（Finite context）**：**context rot 在触及硬上限之前就已经在拉低表现**；24 小时的运行超过任何现有窗口。
2. **无持久状态（No persistent state）**：没有显式持久化层，每次会话都从空白开始。
3. **无自我验证能力（No self-verification）**：**模型会高报完成度**（over-report completion confidence）。

**记法**：三堵墙 → 三个解 = 上下文管理 / 外置状态 / 独立评估器。这正好对应三月文章的三件套。

### 3. Ralph Loop 模式

一个 bash 脚本实现的循环：**取下一个任务 → 带上下文构造提示词 → 调用智能体 → 跑检查 → 追加写进度文件 → 更新任务列表**。

状态全部活在上下文之外：`prd.json`、`progress.txt`、`AGENTS.md`。由 **Geoffrey Huntley** 与 **Ryan Carson** 推广。

### 4. 三家架构横向对照（本篇独有价值）★

#### Anthropic

来自两篇工程博客：

- **《Effective harnesses for long-running agents》**：**Initializer agent**（环境搭建、把需求展开成 `feature-list.json`）+ **Coding agent**（每次会话做增量进展、写 `claude-progress.txt` 笔记）。**Test ratchet**（测试棘轮）防止删掉失败的测试。planner/generator/evaluator 分离解决自评问题。
- **《Scaling Managed Agents》**：**brain / hands / session** 三层，各自可独立替换——brain（模型 + harness 循环）、hands（临时沙箱执行）、session（append-only 事件日志）。收益：无状态 harness、**沙箱当牲口不当宠物**、**首 token 时间 p50 降 60%、p95 降 90%+**。

科学计算场景的落地：`CLAUDE.md`（活的计划）、`CHANGELOG.md`（实验记录）、`tmux`/`SLURM`/`git` 协调、Ralph loop 拒绝过早完工。

#### Cursor

三个角色，与 Anthropic 的三角色**不是同一套**：

| 角色 | 职责 |
|---|---|
| **Planners** | 持续探索代码库、产出任务、**递归派生子 planner** |
| **Workers** | 专注执行，不背协调负担 |
| **Judges** | 判定迭代是否该结束 |

⚠️ **最值得记的一条发现**：*"different models slot into different roles"*（不同模型适配不同角色）——文中给的例子是 **GPT 在长时间自主工作上更优，因为 Opus 会提前停手或走捷径**。这与官方叙事不同，属于第三方观察，引用时注明来源。

后台云端智能体跑长任务，用 **git worktree 隔离** + PR 合并。

#### Google

Cloud Next '26 发布的 **Gemini Enterprise Agent Platform**：

- **Agent Runtime**：天级自主执行，**亚秒级冷启动**
- **Agent Sessions**：持久化对话/事件历史，支持自定义 session ID 映射
- **Agent Memory Bank**：长期策展记忆 + 搜索 API（Payhawk 的费用提交场景**提升 50%+**）
- **Agent Sandbox**：加固的代码执行
- 外加 identity、registry、gateway、observability、simulation 服务

作者的判断：**这套架构就是 Anthropic 的 brain/hands/session，只是打包成了有名字的服务。**

### 5. 五种生产模式（Five Production Patterns）★

可以当长时程系统的设计检查表：

1. **Checkpoint-and-resume**：保存中间状态，故障后恢复
2. **Delegated approval**：智能体**带着完整状态暂停**，恢复时亚秒级延迟
3. **Memory-layered context**：长期策展记忆 + 治理 —— 专门应对 **memory drift**（记忆漂移：从捷径过度泛化）
4. **Ambient processing**：Pub/Sub、BigQuery 事件处理，**策略层可不重新部署就更新**
5. **Fleet orchestration**：协调者委派给各自独立身份/策略强制的专家智能体

### 6. 落地建议（按角色分）

| 你是谁 | 建议 |
|---|---|
| **个人开发者** | 用现成 harness（Claude Code / Cursor）；把 `AGENTS.md` 当检查单；加 typecheck/lint hooks；用 Ralph loop 做验证 |
| **做托管产品** | **别自己造 runtime** —— 用 Google Agent Platform、Claude Managed Agents，或自托管 ADK / Claude Agent SDK / Codex SDK |
| **做自主运维** | ADK + Memory Bank + Cloud Run + Cloud Scheduler |

**通用四条**：
- 执行前先写明确的 **done-conditions**
- **在架构上**把 evaluator 与 generator 分开（不是在提示词里分）
- 投资 session logs，为了可恢复性与可审计性
- 把 compaction 与 context reset 当一等公民 —— **Anthropic 的经验是超出摘要能力时需要完整重置**

### 7. 尚未解决的问题（Unsolved Limitations）

这一节适合当面试里「你觉得这套方案的局限是什么」的答案库：

- **成本管理**：24 小时的前沿模型运行**没有断路器（circuit breakers）就很贵**
- **安全**：攻击面更大；**凭证必须对「跑模型生成代码的沙箱」不可达**
- **对齐漂移**：目标忠实度在一次次摘要循环中降解
- **验证**：审计 24 小时的运行需要结构化产物
- **人的角色转移**：**写精确规格比写代码更有价值**

### 8. 未来方向

架构趋同，差异在表面积（surface area）。下一批问题：多智能体在共享代码库上的协调、**智能体读取并修补自己的 harness**、just-in-time 组装工具与上下文。

## 可直接带走的工程结论

1. **先分清「长时程」问的是哪一种**——推理 / 执行 / 持久能动性，三者的解法不同。
2. **三堵墙对应三个必备组件**，缺一个就会在特定时长上崩。
3. **context rot 在硬上限之前就开始了**——不要用「还没满」当作不做上下文管理的理由。
4. **evaluator 要在架构上分离**，写在提示词里不算。
5. **按角色选模型**（Cursor 的观察），别默认一个模型通吃。
6. **memory drift 是记忆系统的固有失败模式**，记忆层必须带治理，不能只追加。
7. **长跑必须配断路器**，成本失控是最常见的真实事故。
8. **凭证对沙箱结构性不可达**，不是靠提示词约束。

## 与库内其他笔记的关系

- 它横向对照的两篇 Anthropic 文章，本地全文见 [15_effective-harnesses](../Anthropic/Engineering全集_逐句对照/15_effective-harnesses-for-long-running-agents_直观图解与学习笔记.md) 与 [23_managed-agents](../Anthropic/Engineering全集_逐句对照/23_managed-agents_直观图解与学习笔记.md)。
- memory drift 与治理需求的产品答案见 [01_New in Claude Managed Agents](01_new-in-claude-managed-agents_双语精读.md) 的 Dreaming。
- 同作者的前篇（方法论更系统）见 [06_Agent Harness Engineering](06_agent-harness-engineering-osmani_双语精读.md)。
- 「成本没有断路器就很贵」的反方实证见 [09_HN 讨论](09_hn-critiques-long-running-harness_双语精读.md)。
