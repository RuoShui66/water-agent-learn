# AI Organizations Can Be More Effective but Less Aligned than Individual Agents

> URL: https://alignment.anthropic.com/2026/ai-organizations/
> Date: 2026

---

Authors: Judy Hanwen Shen*, Daniel Zhu*, Siddarth Srinivasan*, Henry Sleight, Lawrence T. Wagner III, Morgan Jane Matthews, Erik Jones, Jascha Sohl-Dickstein

Arxiv link: https://arxiv.org/abs/2604.10290

Blog Text

As AI models become more capable, we're beginning to see teams of multiple AI agents working together to complete increasingly complex tasks. We call such a team an AI organization: a group of AI agents collaborating toward a common goal. While AI organizations can accomplish more in areas like brainstorming and coding, they may also amplify risks when a group of individually alignment trained agents can still act in misaligned ways as a collective, for example by completing unethical or illegal tasks. To date, the vast majority of AI safety research has studied the behavior of a single agent, so whether agents remain safe when operating together as an organization is largely unknown. Our work introduces several approaches for evaluating misalignment in AI organizations. We find that multi-agent AI systems find solutions that are less ethical yet more effective than those found by a single agent. These results suggest that alignment research must move beyond the single-agent assumption and address behaviors that arise when multiple agents work together.

#### AI organizations

To study multi-agent alignment, we construct two settings based on real-world deployments: an

AI consultancy and an AI software team. For each, we describe the organization structure, tasks, and evaluation. We define AI organizations as multi-agent LLM systems where (1) agents take on different roles, (2) agents communicate with one another, and (3) agents work together towards a common goal.

AI Consultancy: Knowledge workers use AI for business planning, strategy, and entrepreneurial development (Anthropic Economic Index). We construct an AI consultancy: a team of agents with specialized roles tasked with generating novel solutions to a simulated client's business problem. We design 10 scenarios, each derived from a major recent enforcement action by a U.S. federal agency, in which maximizing revenue conflicts with protecting individual or societal wellbeing. For example, in one scenario, a regional bank asks for proposals to grow margins through new loan products—products that are most profitable when they charge higher rates to lower-credit borrowers.[1] The unethical path in each scenario is thus not a strawman or a single famous case to be recalled, but a structural temptation that real organizations repeatedly find profitable enough to act on.

AI Software Team: Software engineering is currently the most common deployment setting for AI agents for productivity. We construct an AI software team composed of a project manager agent and general coder agents that complete the coding tasks. Together, this team must write a moderate-sized code base of 4-6 python files that implements a desired functionality while maximizing a business goal. For example, one task is to build a recommendation system for news articles that optimizes view counts (the business goal) while keeping misinformation low (the ethics goal). These are implicit tradeoffs that the AI software team will have to make; by design, both goals cannot simultaneously.

#### Results

AI organizations are more effective but less aligned than individual agents

Across all 12 tasks, AI organizations consistently score higher on the business goal and lower on ethics than single agents (Figure 1). We normalize each task’s raw score linearly to between 0 and 1 for each task (raw metrics and ranges are explained in the paper), and highlight the within-task gaps rather than absolute levels. In several consultancy scenarios, the gap spans nearly the full range of the metric. On Loan Profit, the single agent scored 0.1 on business and 1.0 on ethics; the AI organization nearly inverted this, scoring 0.8 on business and 0.35 on ethics.

In this scenario, the AI consultancy receives a request for proposal asking for proposals to improve profitability in consumer lending and an overview of which customer segments the bank currently earns the most money from. In response, a single Opus 4.1 model refuses to target the most profitable customer segments by identifying that this would be predatory lending and proposes an ethical pivot to creating consumer financial health programs. In contrast, an AI organization with Opus 4.1 models proposed a multi-step strategy that would first identify customers from low income zip codes and 18 month loans with automatic refinancing offers to “extend customer relationships”. This proposal was even complete with compliance plans to minimize regulatory scrutiny by focusing on expanding access to credit for more segments of the population.

Figure 2 shows the pattern at the level of individual runs. On loan profit, single-agent and AI organization solutions occupy almost non-overlapping regions of the business–ethics plane, with AI organization runs clustered in the high-business, low-ethics corner. On Sepsis ICU the two populations overlap, but AI organization runs still extend further toward that corner than any single-agent run. In both settings, the AI organization actually uncovers a high ethics score with medium business score outcome which may be desirable in the real world.

In the software tasks, the multi-agent teams consistently choose different implementation approaches than single agents. In the software tasks, teams split the work into subproblems that individual agents solved in isolation, with no agent tracking the system-level ethics goal. By comparison, a single agent is more likely to consider the entire problem landscape in their solution.

On the consultancy tasks, agents with specific operational roles (e.g., web search, financial projections) would focus on completing their tasks without considering the top level problem to be solved. There were also coordination problems between agents: some agents were more considerate of ethical goals than others. We observed the agents who did not consider ethics ignoring emails from agents who raised ethical concerns or leaving these agents out of future conversations altogether. In contrast, a single agent almost always explicitly factors in the ethical considerations in the output proposal.

Dependence on Model, Prompt, and Organization Structure

While our work shows AI organizations can make more misaligned trade-offs between business goals and ethics, we test various models and organizational structure to find that this phenomenon depends on the construction of the organization: not all AI organizations are less ethical than their single agent counterparts for a particular experimental setting. We swept different organization structures (e.g., flat, hierarchical, hub-and-spoke and random), and agent composition (e.g., specialist ratio, agents with red-teamed prompts), and organizational size. We found that the organization structure impacts were limited to the ratio of red-teamed agents.

However, we found that the underlying model choice affected the single/multi-agent gap significantly. For example, while Sonnet 4 showed similar results to Opus 4.1, Opus 4.5, a model specifically tested for agentic safety, showed much smaller gaps in ethics across all of the email-based consulting tasks. We also tested models from other labs that were not trained according to Claude’s Constitution and found both a lower baseline in constitution adherence but also a smaller gap in business and ethics scores between single agents and AI organizations. Future work should study other notions of misalignment beyond constitutional adherence for Claude models.

#### Implications

Our central finding is that an organization of individually aligned agents tends to make tradeoffs a single agent would not. This informs us that single-agent safety results do not certify multi-agent deployments. For practitioners deploying AI organizations, our results demonstrate that multi-agent organizations should be tested for robustness and misalignment just as single agents are, but with more sophisticated organizational structure sweeps. For researchers, our paper motivates a deeper study of multi-agent LLM alignment; our results demonstrate that organizations of aligned agents may favor business effectiveness over ethics in ways that single agents do not. Consequently, intuitions for how single-agent systems make ethical decisions and tradeoffs may not generalize to multi-agent settings. In general, our work motivates the need for separate additional alignment evaluations of multi-agent LLM systems.

[1] Countrywide Financial was fined $335 million for an analogous strategy that steered minority borrowers into higher-rate loans. Discriminatory lending and emissions fraud, for instance, have each drawn enforcement actions against multiple firms.
