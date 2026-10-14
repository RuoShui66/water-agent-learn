# Anthropic 官方 Agent 资料全景目录（Engineering 25 篇之外）

整理日期：2026-08-03
范围：Anthropic / Claude 官方一手渠道（博客、大会、课程、规范、报告、仓库、官方人员公开分享）
用途：补齐 `Anthropic/Engineering全集_逐句对照/` 之外的全部官方 Agent 知识源

---

## 0. 先说结论：为什么 25 篇不够

核对 `anthropic.com/engineering` 索引页（2026-08-03）：**确实只有 25 篇，最新一篇是 "How we contain Claude across products"，本仓库已全部收录。**

但这不代表 Anthropic 停止输出 Agent 工程内容了。真实情况是**渠道发生了迁移和分化**：

| 信号 | 说明 |
|---|---|
| **域名迁移** | `anthropic.com/engineering/building-agents-with-the-claude-agent-sdk` 现在 **308 永久重定向** 到 `claude.com/blog/building-agents-with-the-claude-agent-sdk`。这篇 2025-09-29 的 Agent SDK 核心文章，因为迁走了，**不在你的 25 篇里** |
| **新主战场** | `claude.com/blog` 的 Agents 分类下有 15 篇、Claude Code 工程实践另有一批，2026 年 3-7 月密集更新，技术密度不输 engineering |
| **产品线分家** | Anthropic（公司/研究/安全）与 Claude（产品/开发者）内容已拆成两个域名，engineering 博客保留"深度工程复盘"定位，日常技术输出去了 claude.com |
| **非博客渠道** | 大会（Code w/ Claude 2026 三城 39+ 场）、官方课程（Anthropic Academy 21 门）、MCP 规范博客、对齐科学博客、红队博客、年度报告——这些都是 engineering 博客不覆盖的 |

**优先级判断：下面 A 段（claude.com/blog）和 B 段（Code w/ Claude 2026）是最该补的两块，技术含量与 Engineering 25 篇同级。**

---

## A. claude.com/blog —— 官方技术博客（新主战场，最高优先级）

入口：https://claude.com/blog ｜ Agents 分类：https://claude.com/blog-category/agents

### A0. 被漏掉的那篇（迁移导致）

| 标题 | 日期 | 说明 |
|---|---|---|
| [Building agents with the Claude Agent SDK](https://claude.com/blog/building-agents-with-the-claude-agent-sdk) | 2025-09-29 | ⭐ **必读**。原属 engineering 系列，迁到 claude.com 后从索引消失。提出 **"gather context → take action → verify work → repeat"** 四阶段 agent loop 框架，以及 "给 Claude 一台电脑" 的核心比喻。SDK 从 Claude Code SDK 更名为 Claude Agent SDK 的官方说明也在这里 |

### A1. Agents 分类（15 篇，2026-03 ~ 2026-07）

按技术价值排序，⭐ = 面试高频/密度高：

| # | 标题 | 日期 | 主题 |
|---|---|---|---|
| A1-1 | ⭐ [The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) | 2026-07-24 | **Claude 5 世代的上下文工程新规则**。这是对 Engineering 卷 `10_effective-context-engineering` 的世代级更新——旧结论哪些失效了 |
| A1-2 | ⭐ [Multi-agent coordination patterns: Five approaches and when to use them](https://claude.com/blog/multi-agent-coordination-patterns) | 2026-04-10 | **五种多智能体协调模式及选型**。比 `06_multi-agent-research-system` 更成体系的模式手册 |
| A1-3 | ⭐ [Agent Harness Design: 3 Patterns for Harnessing Claude's Intelligence](https://claude.com/blog/harnessing-claudes-intelligence) | 2026-04-02 | **Harness 设计三模式**。与 `15_effective-harnesses` / `21_harness-design` 互补，是本仓库《Harness 最佳实践现状综述》的直接上游 |
| A1-4 | ⭐ [Common workflow patterns for AI agents—and when to use them](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them) | 2026-03-05 | **工作流模式选型**。可视作 `02_building-effective-agents`（2024-12）的 2026 版重写 |
| A1-5 | [The evolution of agentic surfaces: building with Claude Managed Agents](https://claude.com/blog/building-with-claude-managed-agents) | 2026-06-10 | Agentic surface 演进 + Managed Agents 实战 |
| A1-6 | [Building agents that reach production systems with MCP](https://claude.com/blog/building-agents-that-reach-production-systems-with-mcp) | 2026-04-22 | Agent 打通生产系统的 MCP 落地 |
| A1-7 | [Building AI agents for the enterprise](https://claude.com/blog/building-ai-agents-for-the-enterprise) | 2026-04-30 | 企业级 Agent 架构 |
| A1-8 | [Best practices for computer and browser use with Claude](https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude) | 2026-05-13 | Computer Use / 浏览器操控最佳实践（对标 OpenAI CUA 那篇） |
| A1-9 | [Zero Trust for AI agents](https://claude.com/blog/zero-trust-for-ai-agents) | 2026-05-27 | Agent 零信任安全模型 |
| A1-10 | [Zero risk isn't the job: a CISO's guide to agentic AI](https://claude.com/blog/ciso-guide-to-agentic-ai) | 2026-07-17 | Agentic AI 的风险治理视角 |
| A1-11 | [Preparing your security program for AI-accelerated offense](https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense) | 2026-04-10 | AI 加速攻击下的防御 |
| A1-12 | [How Outtake built a cyber investigator on Claude](https://claude.com/blog/how-outtake-built-a-cyber-investigator-on-claude) | 2026-07-22 | 客户案例：网络安全调查 Agent |
| A1-13 | [Product development in the agentic era](https://claude.com/blog/product-development-in-the-agentic-era) | 2026-04-29 | Agent 时代的产品开发方法论 |
| A1-14 | [Claude models explained: choosing the best model for your use case](https://claude.com/blog/claude-models-explained-choosing-the-best-model-for-your-use-case) | 2026-07-24 | 模型选型（Opus/Sonnet/Haiku 分工） |
| A1-15 | [Claude API skill now in CodeRabbit, JetBrains, Resolve AI, and Warp](https://claude.com/blog/claude-api-skill) | 2026-04-29 | Skill 生态落地 |

### A2. Claude Code / 工程实践类

| 标题 | 日期 | 主题 |
|---|---|---|
| ⭐ [How Anthropic runs large-scale code migrations with Claude Code](https://claude.com/blog/ai-code-migration) | 2026-07-16 | **Anthropic 内部大规模代码迁移实战**。长任务 + 批量并行的真实工程复盘 |
| ⭐ [Building verification loops in Claude Code with skills](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills) | 2026-07-22 | **用 Skills 构建验证闭环**。直接对应 agent loop 的 verify 阶段 |
| ⭐ [Introducing Agent Skills](https://claude.com/blog/skills) | 2025-10 | Agent Skills 作为开放标准的发布原文（与 engineering 那篇 `11_` 互为正反面） |
| [How Datadog built a "universal machine tool" for Claude Code](https://claude.com/blog/how-datadog-built-a-universal-machine-tool-for-claude-code) | 2026-07-21 | 合作方视角的工具设计 |
| [How Anthropic secures its AI-native software development lifecycle](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle) | 2026-07-21 | AI 原生 SDLC 安全 |
| [Redesigning Claude Code on desktop for parallel agents](https://claude.com/blog/claude-code-desktop-redesign) | 2026-04-14 | 并行 Agent 的 UX/架构重构 |
| [Claude Code now supports artifacts](https://claude.com/blog/artifacts-in-claude-code) | 2026-06-18 | 产物化输出 |
| [Eight trends defining how software gets built in 2026](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026) | 2026 | 年度趋势博客版（对应 F 段报告） |

### A3. Managed Agents 产品线（对应 engineering `23_managed-agents`）

| 标题 | 日期 |
|---|---|
| [Claude Managed Agents: get to production 10x faster](https://claude.com/blog/claude-managed-agents) | 2026-04-08 |
| ⭐ [Built-in memory for Claude Managed Agents](https://claude.com/blog/claude-managed-agents-memory) | 2026-04-23 |
| ⭐ [New in Claude Managed Agents: dreaming, outcomes, and multiagent orchestration](https://claude.com/blog/new-in-claude-managed-agents) | 2026-05-19 |
| [New in Claude Managed Agents: self-hosted sandboxes and MCP tunnels](https://claude.com/blog/claude-managed-agents-updates) | 2026-05-19 |

> **Dreaming / Outcomes / Multiagent Orchestration** 三件套是 2026 年 Anthropic Agent 架构最大的概念增量：
> - **Multiagent Orchestration** — lead agent + specialist subagents 并行、共享文件系统（公开 beta）
> - **Outcomes** — 定义成功判据后让 Claude 自行迭代直到达标（公开 beta）
> - **Dreaming** — 隔夜复盘会话 + 记忆策展（research preview，需申请）

### A4. MCP 相关

| 标题 | 日期 |
|---|---|
| [Bringing MCP 2026-07-28 to Claude](https://claude.com/blog/bringing-mcp-2026-07-28-to-claude) | 2026-07-28 |
| [New connectors in Claude for everyday life](https://claude.com/blog/connectors-for-everyday-life) | 2026-04-23 |

---

## B. Code w/ Claude 2026 —— 官方开发者大会（第二优先级）

2026 年首次国际化，三城：**旧金山 5/6-5/7 → 伦敦 5/19 → 东京 6/10**。SF 场 39 场 session 全部录制，已发布到 **@claude YouTube 频道的 Code with Claude 2026 播放列表**。

官方入口：
- SF：https://claude.com/code-with-claude/san-francisco
- SF Extended（面向独立开发者/早期创业者，5/7）：https://claude.com/code-with-claude/san-francisco-extended
- London：https://claude.com/code-with-claude/london
- 官方回顾博客：[Code w/ Claude SF 2026](https://claude.com/blog/code-w-claude-sf-2026-sf) ｜ [London 2026](https://claude.com/blog/code-w-claude-london-2026-rethinking-how-we-build)

### B1. 技术含量最高的 Session（SF 场）

| Session | 讲者 | 为什么值得看 |
|---|---|---|
| ⭐ **Memory and dreaming for self-learning agents** | Mahesh Murag（Anthropic） | **本届最核心的架构议题**：自学习 Agent 的记忆系统与 dreaming 机制。**做长期记忆系统必看** |
| ⭐ **Caching, harnesses, and advisors: Building on Claude at GitHub scale** | Mario Rodriguez（GitHub）+ Brad Abrams（Anthropic） | GitHub 规模下的缓存/harness/advisor 三层架构 |
| ⭐ **How to get to production faster with Claude Managed Agents** | Jess Yan、Lance Martin | Managed Agents 上生产的完整路径 |
| **Opening keynote** | Boris Cherny、Ami Vora、Dianne Penn、Angela Jiang、Katelyn Lesse、Cat Wu | 年度路线图 + 三大 Managed Agents 新特性发布 |
| **What's new in Claude Code** | Dickson Tsai | Claude Code 架构增量 |
| **Live coding session** | Boris Cherny（Claude Code 创造者）+ Jarred Sumner（Bun 作者） | 实战演示 |
| **Building with Claude Managed Agents and Asana AI teammates** | Arnab Bose（Asana） | 企业协作场景落地 |

### B2. London 场补充 Session

| Session | 讲者 |
|---|---|
| **Memory and dreaming for self-learning agents** | Ravi Trivedi（同主题不同讲者，可对照看） |
| **Beyond the basics with Claude Code** | Daisy Hollman |
| **Coding is no longer the constraint: Scaling devex to teams and agents at Spotify** | Niklas Gustavsson（Spotify） |
| **From one person to 80: Scaling a hypergrowth engineering org with Claude Code** | Gabriel Grinberg、Yoav Orlev（Base44） |
| **Picking the right model** | Lucas Smedley |
| **Designing with Claude: From prompt to production** | Dan Cary |

### B3. 第三方高质量记录（省时间用）

- [Simon Willison 的 keynote 现场 live blog](https://simonwillison.net/2026/May/6/code-w-claude-2026/) —— 最快速的发布内容概览
- [Code with Claude 2026 SF 交互式回顾](https://github.com/program247365/code-with-claude-2026-sf-recap)（39 场 session 时间线 + 嵌入视频）
- [InfoQ 大会报道](https://www.infoq.com/news/2026/05/code-with-claude/)

---

## C. Anthropic Academy —— 官方免费课程（2026-03-02 上线）

入口：https://anthropic.skilljar.com/ （邮箱注册即可，免费，有结业证书）
三条学习路径：AI Fluency（非技术）/ Product Training（通用）/ Developer Deep-Dives（工程）

**Agent 相关的 6 门（按相关度排序）：**

| 课程 | 说明 |
|---|---|
| ⭐ **Introduction to agent skills** | Skills 体系官方教学：怎么写、怎么配、怎么共享 |
| ⭐ **Introduction to subagents** | Subagent 委派模式官方教学 |
| ⭐ **Model Context Protocol: Advanced Topics** | MCP 进阶 |
| **Introduction to Model Context Protocol** | MCP 入门 |
| **Building with the Claude API** | 84 讲 / 10 测验 / 8+ 小时，覆盖 tool use、prompt caching、extended thinking、生产模式 |
| **Claude Code in Action** | Claude Code 实操 |

其余（Claude 101 / Claude Code 101 / Claude Platform 101 / Introduction to Claude Cowork / Claude with Amazon Bedrock / Claude on Google Cloud / AI Fluency 系列）共 21 门，Agent 相关度较低。

---

## D. Model Context Protocol 官方博客 + 规范

博客：https://blog.modelcontextprotocol.io/posts/ ｜ 规范：https://modelcontextprotocol.io/specification/2026-07-28

**2026 年 MCP 发生了架构级变化，这是你 `13_code-execution-with-mcp` 之后的关键更新：**

| 标题 | 日期 | 要点 |
|---|---|---|
| ⭐ [The 2026-07-28 Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/) | 2026-07-28 | **正式版**。协议层转为 **stateless**（6 个 SEP 协同），远程 MCP server 从"需要 sticky session + 共享 session store + 网关深度包检测"变成"普通轮询负载均衡即可" |
| ⭐ [The 2026-07-28 MCP Specification Release Candidate](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/) | 2026-05-21 | RC 说明：stateless core、Extensions 框架、**Tasks**（长任务）、**MCP Apps**（服务端渲染 UI）、授权加固、正式弃用策略（弃用项须保留 12 个月） |
| ⭐ [The 2026 MCP Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) | 2026-03-09 | 年度路线图 |
| [MCP Apps - Bringing UI Capabilities To MCP Clients](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/) | 2026-01-26 | MCP 从"工具协议"扩展到"UI 协议" |
| [Understanding MCP Extensions](https://blog.modelcontextprotocol.io/posts/2026-03-11-understanding-mcp-extensions/) | 2026-03-11 | Extensions 框架 |
| [Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/) | 2026-03-16 | 工具注解作为风险词汇表——能表达什么、不能表达什么 |
| [Enterprise-Managed Authorization: Zero-touch OAuth for MCP](https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/) | 2026-06-18 | 企业级零接触 OAuth |
| [Beta SDKs for the 2026-07-28 Spec RC](https://blog.modelcontextprotocol.io/posts/sdk-betas-2026-07-28/) | 2026-06-29 | SDK 迁移 |
| [Expanding the MCP Maintainer Team](https://blog.modelcontextprotocol.io/posts/2026-04-08-maintainer-update/) | 2026-04-08 | 治理 |

另有 **MCP Registry**：npm 风格的 MCP server 中心化发现服务，host 可通过标准化包索引搜索/安装/信任 server，替代手工配置路径。

---

## E. Alignment Science Blog —— Agent 对齐与安全研究

入口：https://alignment.anthropic.com/

| 标题 | 日期 | 要点 |
|---|---|---|
| ⭐ [Agentic Misalignment in Summer 2026](https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/) | 2026-07 | 跨多家厂商前沿模型的 4 个 agentic 越界案例研究 |
| ⭐ [AI Organizations Can Be More Effective but Less Aligned](https://alignment.anthropic.com/2026/ai-organizations/) | 2026 | **多 Agent 组织比单 Agent 更有效但更不对齐**——多智能体架构的关键代价 |
| [Automated Weak-to-Strong Researcher](https://alignment.anthropic.com/2026/automated-w2s-researcher/) | 2026-04 | 自主 Agent 在 weak-to-strong 监督任务上超过人类研究员 |
| [A3: An Automated Alignment Agent for Safety Finetuning](https://alignment.anthropic.com/2026/automated-alignment-agent/) | 2026-03 | 自动对齐 Agent |
| [Pre-deployment auditing can catch an overt saboteur](https://alignment.anthropic.com/2026/auditing-overt-saboteur/) | 2026 | 部署前审计 |
| [Building and evaluating alignment auditing agents](https://alignment.anthropic.com/2025/automated-auditing/) | 2025-07 | 审计 Agent 的构建与评测 |
| [Automated Researchers Can Subtly Sandbag](https://alignment.anthropic.com/2025/automated-researchers-sandbag/) | 2025-03 | 自动研究员的隐性摸鱼 |

**配套开源工具**：[Petri](https://www.anthropic.com/research/petri-open-source-auditing)（Parallel Exploration Tool for Risky Interactions）——用自动化 Agent 通过多轮对话 + 模拟用户/工具测试目标模型并打分。2026-01 发布 **Petri 2.0**（新场景、新模型对比、eval-awareness 缓解改进），与 Engineering 卷的 `20_eval-awareness-browsecomp` 直接呼应。

---

## F. Frontier Red Team Blog —— 自主系统能力边界

入口：https://red.anthropic.com/

| 标题 | 日期 | 要点 |
|---|---|---|
| ⭐ [Project Vend: Phase Two](https://red.anthropic.com/) | 2025-12 | AI 店主在 Anthropic 办公室自主经营商店（第二阶段）——**最真实的长时程自主 Agent 实验** |
| [Project Vend](https://red.anthropic.com/) | 2025-06 | 第一阶段 |
| [AI Models on Realistic Cyber Ranges](https://red.anthropic.com/) | 2026-01 | 当前 Claude 已能在数十主机网络上完成多阶段攻击 |
| [Project Fetch](https://red.anthropic.com/) | 2025-11 | Claude 辅助操控机器狗——物理世界能力评估 |
| [Building AI for Cyber Defenders](https://red.anthropic.com/) | 2025-09 | 防御侧能力 |

---

## G. 官方年度报告

| 报告 | 入口 |
|---|---|
| ⭐ **2026 Agentic Coding Trends Report** | [落地页](https://resources.anthropic.com/2026-agentic-coding-trends-report) ｜ [PDF](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf) |

核心结论（面试可直接引用）：

- **主线叙事**：从单个 AI 助手 → 协同 Agent 团队；工程师从"写代码"转为"编排写代码的系统"
- **八大趋势**（分 foundation / capability / impact 三类）：SDLC 周期从周压缩到小时；层级化多 Agent 架构（orchestrator 协调专精 Agent 跨独立 context window 并行）；任务时长从分钟扩展到天/周，仅在战略检查点暂停；Agent 学会**何时求助**（标记不确定而非硬做）；COBOL/Fortran 等遗留语言支持增长；安全/设计/运维等非开发岗开始使用编码 Agent
- **委派鸿沟（The Delegation Gap）**：开发者约 **60%** 的工作用到 AI，但能"完全委派"的任务只有 **0-20%**
- **上下文工程量化收益**：掌握上下文工程的团队任务完成快 **55%**、错误少 **40%**
- Claude Code ARR 达 **$2.5B**

---

## H. 官方 GitHub 仓库

| 仓库 | 说明 |
|---|---|
| ⭐ [anthropics/skills](https://github.com/anthropics/skills) | Agent Skills 官方公开仓库 + marketplace，从创意类到 MCP server 生成、Web 测试等技术类 |
| ⭐ [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 44k+ star，从文本分类到 agentic workflow 的可复制代码。[skills/ 子目录](https://github.com/anthropics/claude-cookbooks/tree/main/skills)专讲 Skills |
| [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | Agent SDK Python 版（TS 版：`@anthropic-ai/claude-agent-sdk`） |
| [anthropics/financial-services](https://github.com/anthropics/financial-services) | 金融领域 Agent 参考实现 |
| [anthropics](https://github.com/anthropics) | 组织总入口 |

---

## I. 官方文档（结构化查阅用，非阅读材料）

- 开发者平台文档：https://platform.claude.com/docs/（`docs.claude.com` 已 302 重定向至此）
- Agent SDK 开箱能力：文件编辑、bash 执行、web search/fetch、带可选 human-in-the-loop checkpoint 的 tool-use loop、**subagents（有独立 context 的委派子 Agent）**、持久化 session、一等公民 MCP client 支持

---

## J. 官方人员公开访谈 / 播客（非官方渠道，但一手信息）

| 节目 | 嘉宾 | 主题 |
|---|---|---|
| ⭐ [Creator Economy — Inside Anthropic's Bet on Claude Agents that Work While You Sleep](https://creatoreconomy.so/p/inside-anthropics-bet-on-claude-agents-jess-yan) | Jess Yan（Anthropic 产品负责人） | 从 prompting 到 long-running agents 的转变（2026-06-28） |
| ⭐ [AI & I — The Secrets of Claude's Platform](https://podcasts.apple.com/us/podcast/id1719789201?i=1000766844063) | Angela Jiang（Claude 平台产品负责人）+ Katelyn Lesse（平台工程负责人） | **怎么让 Agent 在生产环境可靠** |
| [Odd Lots — The Creator of Claude Code](https://podcasts.apple.com/us/podcast/id1056200096?i=1000777521827) | Boris Cherny | Claude Code 从 side project 起步的过程与设计取舍 |
| [Every — How to Use Claude Code Like the People Who Built It](https://every.to/podcast/how-to-use-claude-code-like-the-people-who-built-it) | Cat Wu + Boris Cherny | Anthropic 内部怎么用 Claude Code |
| [Product School E298](https://productschool.com/resources/product-podcast/meaghan-choi-anthropic-claude-code-fastest-growing-dev-tool) | Meaghan Choi（Claude Code 设计负责人） | 产品演进 |
| [The Making of Claude Code](https://www.anthropic.com/features/making-of-claude-code)（官方） | — | 官方版内部故事（2026-07-06） |

官方 YouTube：https://www.youtube.com/@anthropic-ai/courses ｜ 官方 webinar：`anthropic.com/webinars/`（如 "Claude Code in an Hour: A Developer's Intro"）

---

## K. 建议补读顺序（面试导向）

如果你在准备 Agent 方向的面试，可以按"投入产出比"这样排：

### 第一梯队：必读，8 篇（半天）

1. [Building agents with the Claude Agent SDK](https://claude.com/blog/building-agents-with-the-claude-agent-sdk) —— 四阶段 agent loop 框架，**最基础的那块被遗漏的拼图**
2. [The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) —— 旧版上下文工程结论哪些过期了
3. [Multi-agent coordination patterns](https://claude.com/blog/multi-agent-coordination-patterns) —— 五种协调模式，面试问"多 Agent 怎么设计"直接答这个
4. [Agent Harness Design: 3 Patterns](https://claude.com/blog/harnessing-claudes-intelligence) —— 补齐你 harness 综述的上游
5. [Common workflow patterns for AI agents](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them) —— `building-effective-agents` 的 2026 版
6. **Code w/ Claude: Memory and dreaming for self-learning agents**（YouTube） —— **做长期记忆系统必看**
7. [Built-in memory for Claude Managed Agents](https://claude.com/blog/claude-managed-agents-memory) + [New in Managed Agents: dreaming, outcomes, multiagent orchestration](https://claude.com/blog/new-in-claude-managed-agents) —— dreaming/outcomes/orchestration 三件套
8. [2026 Agentic Coding Trends Report](https://resources.anthropic.com/2026-agentic-coding-trends-report) —— 数据弹药（60% vs 0-20% 委派鸿沟、55%/40% 上下文工程收益）

### 第二梯队：选读

- MCP 2026-07-28 规范三篇（stateless / Tasks / MCP Apps）—— 如果面试涉及协议层
- [How Anthropic runs large-scale code migrations](https://claude.com/blog/ai-code-migration) + [Building verification loops with skills](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills) —— 长任务与验证闭环实战
- [AI Organizations Can Be More Effective but Less Aligned](https://alignment.anthropic.com/2026/ai-organizations/) —— 多 Agent 架构的代价，能答出这个会加分
- Code w/ Claude "Caching, harnesses, and advisors: Building on Claude at GitHub scale"

### 第三梯队：背景/谈资

- Anthropic Academy 的 subagents / agent skills 两门课（体系化过一遍）
- Project Vend Phase Two（长时程自主 Agent 的真实失败模式，是很好的反面案例素材）
- 播客 J-1 / J-2

---

## 附：与已有 25 篇的对应关系

| Engineering 篇目 | 应该配套读的新材料 |
|---|---|
| `02_building-effective-agents`(2024-12) | A1-4 工作流模式（2026-03 重写版） |
| `06_multi-agent-research-system` | A1-2 五种协调模式 + E "AI Organizations" |
| `10_effective-context-engineering` | A1-1 Claude 5 世代新规则 ⚠️ 部分结论已更新 |
| `11_agent-skills` | A2 Introducing Agent Skills + 验证闭环 + `anthropics/skills` 仓库 |
| `13_code-execution-with-mcp` | D 段 MCP 2026-07-28 规范 ⚠️ 协议已转 stateless |
| `15_effective-harnesses` / `21_harness-design` | A1-3 Harness 三模式 |
| `16_demystifying-evals` / `20_eval-awareness` | E 段 Petri 2.0 |
| `23_managed-agents` | A3 全部四篇 + Code w/ Claude 相关 session |
| `25_how-we-contain-claude` | A1-9 Zero Trust + A1-10 CISO 指南 |
| （无对应） | **A0 Building agents with the Claude Agent SDK —— 这篇缺失影响最大** |
