# OpenAI 与 Anthropic 的 Agent 技术路线对照

## 一句话结论

两家公司已经高度收敛：Agent 不是“更长的提示词”，而是模型、工具、循环、状态、执行环境、评测与安全边界共同组成的系统。差异主要在叙事重心：OpenAI 更强调平台原语和真实业务闭环，Anthropic 更强调 harness、上下文、工具接口和隔离机制的工程推导。

## 共同技术栈

| 层次 | OpenAI 常用表述 | Anthropic 常用表述 | 共同结论 |
|---|---|---|---|
| 决策核心 | model / reasoning | model / brain | 模型负责选择下一步，而不是直接完成所有工作 |
| 循环 | Responses API / Agents SDK | agent loop / harness | 调模型、执行工具、回传结果，直到退出条件满足 |
| 工具 | built-in tools / shell / computer use | tools / MCP / ACI | 工具是给非确定性智能体使用的接口，设计方式不同于普通 API |
| 状态 | conversation state / files / memory | session / memory / artifacts | 长任务必须把重要状态外置，不能只依赖上下文窗口 |
| 执行环境 | hosted container / sandbox | sandbox / container / VM | 模型生成的代码应在隔离环境中执行 |
| 长上下文 | compaction / skills / filesystem | compaction / reset / structured handoff | 关键不是把所有历史塞进去，而是保留高信号状态 |
| 评测 | traces / Evals / production feedback | tasks / trials / graders / transcripts | 应评测真实结果和环境状态，而不只评最终文字 |
| 安全 | guardrails / approvals / credential separation | containment / blast radius / vault proxy | 权限、凭据和执行环境必须结构性隔离 |

## OpenAI 路线

OpenAI 在 2025 年先把 Agent 的最小组成讲清楚：模型、工具、指令和循环；Responses API 与 Agents SDK 把工具调用、交接、追踪和护栏变成平台能力。到 2026 年，重点明显转向“给模型一台可控的计算机”：shell、文件系统、持久工作区、技能包、上下文压缩、沙箱快照与恢复。

OpenAI 的工程文章还有一个鲜明特征：经常从真实组织或垂直业务反推架构。内部数据 Agent 强调多层上下文与权限透传；税务 Agent 强调把专家纠错、生产 trace、评测和 Codex 改进串成闭环；Harness Engineering 则把代码库本身变成 Agent 可读、可验证的工作环境。

可以把这条路线概括为：

`平台原语 → 可执行计算机环境 → Agent-first 工作空间 → 生产反馈驱动的持续改进`

## Anthropic 路线

Anthropic 从 2024 年就强调“先使用简单、可组合模式，再按评测结果增加复杂度”。2025 年，它把三个关键面拆开讲透：上下文是有限注意力预算；工具是确定性系统与非确定性 Agent 之间的契约；多智能体只有在任务可并行、价值足够高时才值得支付额外 token 和协调成本。

2026 年的文章进一步把 harness 当成一等工程对象。长任务需要规划者、执行者、评估者以及结构化交接；托管 Agent 则应把会话、harness 和沙箱解耦，使任何一层都能失败和替换；安全的重点从大量弹窗式批准转向“Agent 最多能碰到什么”的硬隔离。

可以把这条路线概括为：

`简单可组合模式 → 上下文/工具工程 → 长任务 harness → 可恢复托管架构 → 爆炸半径控制`

## 最值得交叉阅读的四组文章

### 1. Agent 基础

- OpenAI《A practical guide to building agents》
- Anthropic《Building effective agents》

两篇共同反对过早堆叠多智能体。OpenAI 用“模型 + 工具 + 指令”描述 Agent，Anthropic用 workflows 与 agents 的区别来划定自主性边界。

### 2. 长任务运行时

- OpenAI《The next evolution of the Agents SDK》
- Anthropic《Scaling Managed Agents》

两篇都走向 harness 与 compute 分离：凭据不进入执行沙箱，状态外置后容器可丢弃并重建，执行单元可以并行扩展。

### 3. 上下文与领域知识

- OpenAI《Inside OpenAI’s in-house data agent》
- Anthropic《Effective context engineering for AI agents》

Anthropic给出“最小高信号 token 集”的原则；OpenAI给出生产实例：表使用记录、人类注释、代码语义、组织知识、记忆和运行时查询共同构成上下文。

### 4. 评测与改进

- OpenAI《Building self-improving tax agents with Codex》
- Anthropic《Demystifying evals for AI agents》

Anthropic给出任务、trial、grader、trace、outcome 的评测词汇表；OpenAI展示如何把真实专家纠错转成结构化证据、评测用例和自动改进任务。

## 2026 年值得记住的工程判断

1. 模型升级并不会自动消除 harness；它会让旧 harness 中针对弱模型的补丁变成负担，因此架构要允许替换策略。
2. 长任务可靠性的核心不是无限上下文，而是持久状态、结构化产物、可恢复会话和可审计轨迹。
3. 多智能体适合高价值、可并行、信息面宽的任务；强依赖共享状态的任务仍可能更适合单 Agent。
4. 安全不能主要依靠用户不停点击“允许”。更稳妥的是把凭据移出沙箱、限制网络出口、使用成熟隔离原语，并按用户监督能力选择边界。
5. 生产 Agent 的“自我改进”不是让模型随意改自己，而是把反馈变成数据和 eval，在受控门槛下验证后再部署。

