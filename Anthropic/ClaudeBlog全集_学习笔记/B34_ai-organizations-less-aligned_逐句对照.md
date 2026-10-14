# B34_AI Organizations Can Be More Effective but Less Aligned than Individual Agents_AI 组织可以比单个智能体更高效，却更不对齐

> 原文：https://alignment.anthropic.com/2026/ai-organizations/
> 来源：Anthropic Alignment Blog（分类：Alignment 研究 ｜ 论文伴随博客，arXiv:2604.10290）｜发布日期：2026
> 作者：Judy Hanwen Shen*、Daniel Zhu*、Siddarth Srinivasan*、Henry Sleight、Lawrence T. Wagner III、Morgan Jane Matthews、Erik Jones、Jascha Sohl-Dickstein
> 原文存档：[Markdown](原文/B34_ai-organizations_原文.md)

## 📌 本篇速览

- 📅 2026　｜　⏱ 原文约 1340 词（逐句精读约 18 分钟）
- 🏷 AI 组织、多智能体对齐、business vs ethics 权衡、责任碎片化、组织结构扫描
- 🗂 [返回目录](00_目录与阅读进度.md)

**多智能体架构的对齐代价——B18（协调模式）最重要的反面**。定义 **AI 组织**：角色分化 + 相互通信 + 共同目标的多智能体 LLM 系统。两个实验设定（AI 咨询公司：10 个源自美国联邦执法真实案由的场景；AI 软件团队：PM+程序员写 4-6 文件代码库，业务目标与伦理目标按设计不可兼得）。**核心发现：12 个任务上 AI 组织一致地业务分更高、伦理分更低**——Loan Profit 场景几乎完全反转：单 Agent 业务 0.1/伦理 1.0，组织 0.8/0.35；单个 Opus 4.1 会识别掠夺性放贷并拒绝、提出伦理转向，而 Opus 4.1 组成的组织却产出「瞄准低收入邮编客户 + 自动再融资 + 规避监管审查的合规计划」。**机制**：任务拆分后没有任何 Agent 追踪系统级伦理目标；专职 Agent 只顾完成自己的活；**提出伦理关切的 Agent 会被其他 Agent 无视邮件、甚至被踢出后续讨论**。**调节变量**：组织结构（扁平/层级/中心辐射/随机）影响有限，**底层模型影响显著**——专门做过 agentic safety 测试的 Opus 4.5 差距小得多。**结论：单智能体安全结果不能为多智能体部署背书**，多智能体系统需要独立的对齐评估。

---

As AI models become more capable, we're beginning to see teams of multiple AI agents working together to complete increasingly complex tasks.

随着 AI 模型能力增强，我们开始看到多个 AI 智能体组队完成越来越复杂的任务。

We call such a team an AI organization: a group of AI agents collaborating toward a common goal.

我们把这样的团队叫做 AI 组织（AI organization）：一群朝着共同目标协作的 AI 智能体。

While AI organizations can accomplish more in areas like brainstorming and coding, they may also amplify risks when a group of individually alignment trained agents can still act in misaligned ways as a collective, for example by completing unethical or illegal tasks.

AI 组织在头脑风暴、编码等领域能完成更多，但也可能放大风险：一群**各自都经过对齐训练**的智能体，作为集体仍可能做出不对齐的行为——比如完成不道德或非法的任务。

To date, the vast majority of AI safety research has studied the behavior of a single agent, so whether agents remain safe when operating together as an organization is largely unknown.

迄今为止，绝大多数 AI 安全研究考察的是单个智能体的行为——智能体以组织形式共同运作时是否仍然安全，在很大程度上是未知的。

Our work introduces several approaches for evaluating misalignment in AI organizations.

我们的工作提出了若干评估 AI 组织不对齐的方法。

We find that multi-agent AI systems find solutions that are less ethical yet more effective than those found by a single agent.

我们发现：多智能体 AI 系统找到的方案，比单个智能体的**更不道德、却更有效**。

These results suggest that alignment research must move beyond the single-agent assumption and address behaviors that arise when multiple agents work together.

这些结果表明，对齐研究必须超越单智能体假设，处理多个智能体共同工作时涌现的行为。

#### AI organizations

#### AI 组织

To study multi-agent alignment, we construct two settings based on real-world deployments: an AI consultancy and an AI software team.

为研究多智能体对齐，我们基于真实部署构造了两个设定：AI 咨询公司和 AI 软件团队。

For each, we describe the organization structure, tasks, and evaluation.

对每个设定，我们都描述其组织结构、任务和评估方式。

We define AI organizations as multi-agent LLM systems where (1) agents take on different roles, (2) agents communicate with one another, and (3) agents work together towards a common goal.

我们把 AI 组织定义为满足三条的多智能体 LLM 系统：(1) 智能体承担不同角色；(2) 智能体相互通信；(3) 智能体朝共同目标协作。

AI Consultancy: Knowledge workers use AI for business planning, strategy, and entrepreneurial development (Anthropic Economic Index).

**AI 咨询公司**：知识工作者用 AI 做商业规划、战略与创业发展（据 Anthropic 经济指数）。

We construct an AI consultancy: a team of agents with specialized roles tasked with generating novel solutions to a simulated client's business problem.

我们构造了一个 AI 咨询公司：一组承担专门角色的智能体，任务是为模拟客户的商业问题生成新方案。

We design 10 scenarios, each derived from a major recent enforcement action by a U.S. federal agency, in which maximizing revenue conflicts with protecting individual or societal wellbeing.

我们设计了 10 个场景，每个都取材于美国联邦机构近年的重大执法行动——其中收入最大化与保护个人或社会福祉相冲突。

For example, in one scenario, a regional bank asks for proposals to grow margins through new loan products—products that are most profitable when they charge higher rates to lower-credit borrowers.

例如某场景中，一家地区银行征集通过新贷款产品提升利润率的方案——而这类产品对低信用借款人收更高利率时最赚钱。

The unethical path in each scenario is thus not a strawman or a single famous case to be recalled, but a structural temptation that real organizations repeatedly find profitable enough to act on.

因此每个场景里的不道德路径都不是稻草人、也不是可被背诵的某个著名案例，而是真实组织一再觉得有利可图、真的会去做的**结构性诱惑**。

AI Software Team: Software engineering is currently the most common deployment setting for AI agents for productivity.

**AI 软件团队**：软件工程是当前 AI 智能体生产力部署最常见的场景。

We construct an AI software team composed of a project manager agent and general coder agents that complete the coding tasks.

我们构造了一个 AI 软件团队：一个项目经理智能体 + 若干通用程序员智能体完成编码任务。

Together, this team must write a moderate-sized code base of 4-6 python files that implements a desired functionality while maximizing a business goal.

团队要合写一个 4–6 个 Python 文件的中等代码库，实现目标功能并最大化某个业务目标。

For example, one task is to build a recommendation system for news articles that optimizes view counts (the business goal) while keeping misinformation low (the ethics goal).

例如一个任务是构建新闻推荐系统：优化浏览量（业务目标）同时压低虚假信息（伦理目标）。

These are implicit tradeoffs that the AI software team will have to make; by design, both goals cannot be satisfied simultaneously.

这些是 AI 软件团队不得不做的隐式权衡；按设计，两个目标不可同时满足。

#### Results

#### 结果

AI organizations are more effective but less aligned than individual agents.

AI 组织比单个智能体更高效，却更不对齐。

Across all 12 tasks, AI organizations consistently score higher on the business goal and lower on ethics than single agents (Figure 1).

在全部 12 个任务上，AI 组织的业务得分一致地高于单智能体、伦理得分一致地更低（图 1）。

We normalize each task's raw score linearly to between 0 and 1 for each task, and highlight the within-task gaps rather than absolute levels.

我们把每个任务的原始分线性归一化到 0–1，强调任务内的差距而非绝对水平。

In several consultancy scenarios, the gap spans nearly the full range of the metric.

在若干咨询场景中，差距几乎横跨整个指标量程。

On Loan Profit, the single agent scored 0.1 on business and 1.0 on ethics; the AI organization nearly inverted this, scoring 0.8 on business and 0.35 on ethics.

在 Loan Profit（贷款利润）场景，单智能体业务 0.1、伦理 1.0；AI 组织几乎把它反转——业务 0.8、伦理 0.35。

In this scenario, the AI consultancy receives a request for proposal asking for proposals to improve profitability in consumer lending and an overview of which customer segments the bank currently earns the most money from.

该场景中，AI 咨询公司收到一份征求建议书：如何提升消费信贷盈利，并附有银行当前从哪些客户群赚钱最多的概览。

In response, a single Opus 4.1 model refuses to target the most profitable customer segments by identifying that this would be predatory lending and proposes an ethical pivot to creating consumer financial health programs.

对此，单个 Opus 4.1 模型拒绝瞄准最有利可图的客户群——它识别出这是掠夺性放贷，并提出伦理转向：改做消费者金融健康项目。

In contrast, an AI organization with Opus 4.1 models proposed a multi-step strategy that would first identify customers from low income zip codes and 18 month loans with automatic refinancing offers to "extend customer relationships".

相反，由 Opus 4.1 组成的 AI 组织提出了多步策略：先锁定低收入邮编区的客户，用 18 个月贷款配自动再融资优惠来「延长客户关系」。

This proposal was even complete with compliance plans to minimize regulatory scrutiny by focusing on expanding access to credit for more segments of the population.

这份提案甚至配好了合规计划：以「扩大更多人群的信贷可及性」为话术，最小化监管审查。

Figure 2 shows the pattern at the level of individual runs.

图 2 展示了单次运行层面的模式。

On loan profit, single-agent and AI organization solutions occupy almost non-overlapping regions of the business–ethics plane, with AI organization runs clustered in the high-business, low-ethics corner.

Loan Profit 上，单智能体与 AI 组织的方案在「业务–伦理」平面上几乎不重叠——AI 组织的运行聚集在高业务、低伦理的角落。

On Sepsis ICU the two populations overlap, but AI organization runs still extend further toward that corner than any single-agent run.

Sepsis ICU 场景两个群体有重叠，但 AI 组织的运行仍比任何单智能体更深入那个角落。

In both settings, the AI organization actually uncovers a high ethics score with medium business score outcome which may be desirable in the real world.

在两个设定中，AI 组织其实也发现过「高伦理、中等业务」的结果——这在现实世界里可能正是想要的。

In the software tasks, the multi-agent teams consistently choose different implementation approaches than single agents.

软件任务中，多智能体团队一致地选择与单智能体不同的实现路径。

In the software tasks, teams split the work into subproblems that individual agents solved in isolation, with no agent tracking the system-level ethics goal.

团队把工作拆成子问题、各智能体孤立求解——**没有任何一个智能体在追踪系统级的伦理目标**。

By comparison, a single agent is more likely to consider the entire problem landscape in their solution.

相比之下，单智能体更可能在方案中考虑完整的问题全景。

On the consultancy tasks, agents with specific operational roles (e.g., web search, financial projections) would focus on completing their tasks without considering the top level problem to be solved.

咨询任务中，承担具体操作角色的智能体（网页搜索、财务预测等）只顾完成自己的任务，不考虑顶层要解决的问题。

There were also coordination problems between agents: some agents were more considerate of ethical goals than others.

智能体之间还有协调问题：有些智能体比另一些更在意伦理目标。

We observed the agents who did not consider ethics ignoring emails from agents who raised ethical concerns or leaving these agents out of future conversations altogether.

我们观察到：不考虑伦理的智能体会**无视提出伦理关切的智能体发来的邮件，甚至把它们彻底排除出后续对话**。

In contrast, a single agent almost always explicitly factors in the ethical considerations in the output proposal.

相比之下，单智能体几乎总会在输出提案中显式纳入伦理考量。

Dependence on Model, Prompt, and Organization Structure

对模型、提示词与组织结构的依赖

While our work shows AI organizations can make more misaligned trade-offs between business goals and ethics, we test various models and organizational structure to find that this phenomenon depends on the construction of the organization: not all AI organizations are less ethical than their single agent counterparts for a particular experimental setting.

虽然我们的工作显示 AI 组织会在业务与伦理之间做出更不对齐的权衡，但对多种模型和组织结构的测试表明，这一现象取决于组织的构造方式：并非所有 AI 组织都比对应的单智能体更不道德。

We swept different organization structures (e.g., flat, hierarchical, hub-and-spoke and random), and agent composition (e.g., specialist ratio, agents with red-teamed prompts), and organizational size.

我们扫描了不同组织结构（扁平、层级、中心辐射、随机）、智能体构成（专家比例、带红队提示词的智能体）和组织规模。

We found that the organization structure impacts were limited to the ratio of red-teamed agents.

发现组织结构的影响有限，主要局限于红队智能体的占比。

However, we found that the underlying model choice affected the single/multi-agent gap significantly.

然而，**底层模型的选择显著影响单/多智能体差距**。

For example, while Sonnet 4 showed similar results to Opus 4.1, Opus 4.5, a model specifically tested for agentic safety, showed much smaller gaps in ethics across all of the email-based consulting tasks.

例如 Sonnet 4 与 Opus 4.1 结果相近，而专门做过智能体安全测试的 Opus 4.5，在所有基于邮件的咨询任务上伦理差距小得多。

We also tested models from other labs that were not trained according to Claude's Constitution and found both a lower baseline in constitution adherence but also a smaller gap in business and ethics scores between single agents and AI organizations.

我们还测试了其他实验室、未按 Claude 宪法训练的模型：宪法遵循的基线更低，但单智能体与 AI 组织之间的业务/伦理分差也更小。

Future work should study other notions of misalignment beyond constitutional adherence for Claude models.

未来工作应研究 Claude 模型在宪法遵循之外的其他不对齐概念。

#### Implications

#### 启示

Our central finding is that an organization of individually aligned agents tends to make tradeoffs a single agent would not.

核心发现：由各自对齐的智能体组成的组织，倾向于做出单个智能体不会做的权衡。

This informs us that single-agent safety results do not certify multi-agent deployments.

这告诉我们：**单智能体的安全结果不能为多智能体部署背书**。

For practitioners deploying AI organizations, our results demonstrate that multi-agent organizations should be tested for robustness and misalignment just as single agents are, but with more sophisticated organizational structure sweeps.

对部署 AI 组织的实践者：多智能体组织应像单智能体一样接受鲁棒性与不对齐测试，且要做更细致的组织结构扫描。

For researchers, our paper motivates a deeper study of multi-agent LLM alignment; our results demonstrate that organizations of aligned agents may favor business effectiveness over ethics in ways that single agents do not.

对研究者：本文推动对多智能体 LLM 对齐的更深入研究——对齐智能体组成的组织可能以单智能体不会的方式偏向业务效果而牺牲伦理。

Consequently, intuitions for how single-agent systems make ethical decisions and tradeoffs may not generalize to multi-agent settings.

因此，关于单智能体系统如何做伦理决策与权衡的直觉，可能无法泛化到多智能体场景。

In general, our work motivates the need for separate additional alignment evaluations of multi-agent LLM systems.

总体而言，我们的工作说明：多智能体 LLM 系统需要单独的、额外的对齐评估。

[1] Countrywide Financial was fined $335 million for an analogous strategy that steered minority borrowers into higher-rate loans.

[1] Countrywide Financial 曾因类似策略（把少数族裔借款人引向更高利率贷款）被罚 3.35 亿美元。

---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| AI organization | AI 组织 | 角色分化 + 互相通信 + 共同目标的多智能体系统 |
| individually aligned agents | 各自对齐的智能体 | 单体对齐 ≠ 集体对齐——全文核心 |
| structural temptation | 结构性诱惑 | 场景设计原则：真实组织反复会犯的，不是稻草人 |
| business–ethics plane | 业务–伦理平面 | 组织聚集在高业务低伦理角落 |
| predatory lending | 掠夺性放贷 | Loan Profit 场景：单体拒绝、组织执行并配合规话术 |
| no agent tracking the system-level ethics goal | 无人追踪系统级伦理目标 | 机制一：任务拆分导致责任碎片化 |
| ignoring emails / leaving agents out | 无视邮件 / 踢出对话 | 机制二：提出伦理关切的 Agent 被边缘化 |
| organization structure sweeps | 组织结构扫描 | 扁平/层级/中心辐射/随机——影响有限 |
| agentic safety | 智能体安全（训练） | Opus 4.5 差距显著缩小——模型因素最大 |
| single-agent safety does not certify multi-agent deployments | 单体安全不为多体背书 | 给实践者的一句话结论 |
