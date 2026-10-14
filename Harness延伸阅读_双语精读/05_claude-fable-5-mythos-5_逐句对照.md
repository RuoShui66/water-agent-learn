# 05_Claude Fable 5 and Claude Mythos 5_Fable 5 与 Mythos 5 发布公告

> 原文：https://www.anthropic.com/news/claude-fable-5-mythos-5
> 来源：Anthropic 官方 News（Announcements）｜发布日期：2026-06-09（2026-06-09 有一处编辑更新）

## 📌 本篇速览

- 📅 2026-06-09
- ⭐ ★★★★☆ **值得读，但要读得克制** —— 它的价值集中在**两句话**：官方首次在发布公告里说模型 "needs less scaffolding"，以及 file-based memory 对 Fable 5 的收益反而是 Opus 4.8 的三倍。这两句话看似矛盾，恰恰是「脚手架换形态」论断的直接证据。
- 🏷 less scaffolding、Slay the Spire 记忆基准、Pokémon FireRed vision-only harness、safety classifiers、fallback <5%、trusted access program
- 🖼 [双语精读版（含读法提醒与工程结论）](05_claude-fable-5-mythos-5_双语精读.md)　·　🗂 [返回专题目录](00_目录.md)

Anthropic 同日发布两个同底座模型：**Claude Fable 5**（Mythos 级能力、加装安全防护后面向所有用户开放）与 **Claude Mythos 5**（同一模型、在部分领域解除防护，仅面向 Project Glasswing 的网络防御方与关键基础设施提供方）。公告主体分四块：能力评测（软件工程、知识工作、视觉、记忆与长上下文、生命科学、对齐）、早期客户反馈、新增的安全防护机制（网络安全 / 生物化学 / 蒸馏三类分类器 + 30 天数据留存新政），以及可用性与定价（$10 / $50 每百万 token，不到 Mythos Preview 的一半）。对 harness 设计者最相关的两处，一是视觉一节里「需要更少脚手架」的原话，二是记忆一节里「基于文件的持久记忆给 Fable 5 带来的提升是 Opus 4.8 的三倍」。

> ⚠️ 说明：原文正文中的基准对比表格与多张图表为网页内嵌组件，本文只逐句对照图表说明文字（caption），表格数据请点原文链接查看。页面顶部的两条状态更新横幅（6-12 暂停访问 / 7-1 恢复）附在文末。

---

Today we're launching Claude Fable 5: a Mythos-class1 model that we've made safe for general use.

今天我们发布 Claude Fable 5：一个经我们处理后可安全用于通用场景的 Mythos 级（Mythos-class）模型。

Fable 5's capabilities exceed those of any model we've ever made generally available.

Fable 5 的能力超过我们此前面向公众开放过的任何模型。

It is state-of-the-art on nearly all tested benchmarks of AI capability, showing exceptional performance in software engineering, knowledge work, vision, scientific research, and many other areas.

它在几乎所有受测的 AI 能力基准上都达到了业界最优（state-of-the-art），在软件工程、知识工作、视觉、科学研究等诸多领域表现突出。

The longer and more complex the task, the larger Fable 5's lead over our other models.

任务越长、越复杂，Fable 5 相对我们其他模型的领先幅度就越大。

Releasing a model this capable comes with risks.

发布一个能力如此之强的模型是有风险的。

Without safeguards, Fable 5's capabilities in areas like cybersecurity could be misused to cause serious damage.

在没有安全防护（safeguards）的情况下，Fable 5 在网络安全等领域的能力可能被滥用，造成严重危害。

We've therefore launched the model with safeguards that mean queries on some topics will instead receive a response from our next-most-capable model, Claude Opus 4.8.

因此我们在发布时为模型配备了安全防护：某些主题的查询会改由我们能力次强的模型 Claude Opus 4.8 来回答。

To release the model both safely and quickly, we've tuned these safeguards conservatively—they'll sometimes catch harmless requests, though they trigger, on average, in less than 5% of sessions.

为了既安全又快速地把模型发出去，我们把这些防护调得比较保守——它们有时会误伤无害的请求，不过平均而言，触发率低于 5% 的会话。

With more capable models arriving in the coming months, we're working to improve our safeguards and reduce false positives as quickly as we can.

随着未来几个月更强的模型陆续到来，我们正在尽快改进防护机制、降低误报（false positive）。

For a small group of cyberdefenders and infrastructure providers, we're also launching Claude Mythos 5.

面向一小批网络防御方（cyberdefender）与基础设施提供方，我们同时发布 Claude Mythos 5。

It's the same underlying model as Fable 5, but with the safeguards lifted in some areas.2

它与 Fable 5 是同一个底层模型，只是在部分领域解除了安全防护。

Mythos 5 will initially be deployed through Project Glasswing, in collaboration with the US government, as an upgrade to Claude Mythos Preview.

Mythos 5 起初将通过与美国政府合作的 Project Glasswing 部署，作为 Claude Mythos Preview 的升级版。

It has the strongest cybersecurity capabilities of any model in the world.

它拥有全世界所有模型中最强的网络安全能力。

Soon, we intend to expand access to Mythos 5 through a broader trusted access program.

不久之后，我们打算通过一个覆盖面更广的可信访问计划（trusted access program）来扩大 Mythos 5 的开放范围。

The capabilities of models like Fable 5 and Mythos 5 have the potential to do profound good for the world.

Fable 5、Mythos 5 这类模型的能力，有潜力为世界带来深远的益处。

We've seen the beginnings of this in Project Glasswing, where the models have helped cyber defenders secure critically important software.

我们已经在 Project Glasswing 中看到了这种苗头：模型帮助网络防御方加固了极其重要的软件。

We've also seen it in life sciences research, where the models are positing novel hypotheses and speeding up the development of new therapeutics.

我们在生命科学研究中也看到了：模型正在提出新颖的假说，并加速新疗法的研发。

Fable 5 and Mythos 5 are being offered at $10 per million input tokens and $50 per million output tokens—less than half the price of Claude Mythos Preview.

Fable 5 与 Mythos 5 的定价为每百万输入 token 10 美元、每百万输出 token 50 美元——不到 Claude Mythos Preview 价格的一半。

Today's joint launch is another step towards our goal of bringing advanced AI capabilities to as many users as possible, as quickly and as safely as we can.

今天这次联合发布，是我们朝着「尽可能快、尽可能安全地把先进 AI 能力带给尽可能多的用户」这一目标又迈出的一步。

## Evaluating Claude Fable 5 and Claude Mythos 5｜评测 Claude Fable 5 与 Claude Mythos 5

The table below compares the capabilities of Fable 5 and Mythos 5 to other leading models.

下表将 Fable 5 与 Mythos 5 的能力和其他领先模型作了对比。

> 📊 该基准对比表为网页内嵌组件，本地对照文件未复制表格数据，请点[原文链接](https://www.anthropic.com/news/claude-fable-5-mythos-5)查看。

Fable 5 and Mythos 5 can work autonomously for longer than any previous Claude models.

Fable 5 与 Mythos 5 能够自主工作的时长超过以往任何 Claude 模型。

Below we discuss how these skills apply to software engineering, and cover the model's improved capabilities in knowledge work, vision, memory, and life sciences research.

下面我们将讨论这些能力如何应用于软件工程，并介绍模型在知识工作、视觉、记忆和生命科学研究方面的能力提升。

Software engineering.

**软件工程。**

During early testing, Stripe reported that Fable 5 compressed months of engineering into days.

在早期测试中，Stripe 反馈说 Fable 5 把数月的工程量压缩到了几天。

In a 50-million-line Ruby codebase, the model performed a codebase-wide migration in a day that would otherwise have taken a whole team over two months by hand.

在一个 5000 万行的 Ruby 代码库上，模型用一天完成了一次全代码库迁移，而这项工作若由整个团队手工完成需要两个多月。

Fable 5 is also more token-efficient than past Claude models: on Cognition's FrontierCode evaluation, which tests whether models can pass difficult coding tasks while meeting the standards of high-quality production codebases, Fable 5 scores highest among frontier models, even at medium effort.

Fable 5 的 token 效率也高于以往的 Claude 模型：在 Cognition 的 FrontierCode 评测（考察模型能否在满足高质量生产代码库标准的前提下通过高难度编码任务）中，Fable 5 在前沿模型里得分最高——即便只用中等推理档位（medium effort）也是如此。

Knowledge work.

**知识工作。**

Fable 5 shows strong performance on complex analytical tasks.

Fable 5 在复杂分析类任务上表现强劲。

On Hebbia's Finance Benchmark for senior-level reasoning, Fable 5 has the highest score of any model, with substantial gains in document-based reasoning, chart and table interpretation, and problem solving.

在 Hebbia 面向资深水平推理的 Finance Benchmark 上，Fable 5 取得了所有模型中的最高分，在基于文档的推理、图表解读和问题求解上都有大幅提升。

IMC noted that Fable 5 aced their trading-analysis evaluations nearly across the board, including factual lookup, conceptual reasoning, root-cause analysis, and expected-value analysis.

IMC 表示，Fable 5 几乎在他们所有的交易分析评测上都拿了满分，包括事实查询、概念推理、根因分析和期望值分析。

Vision.

**视觉。**

Fable 5 is the new state-of-the-art model for tasks involving vision.

在涉及视觉的任务上，Fable 5 是新的业界最优模型。

It can extract precise numbers from detailed scientific figures and can perform complex vision-based tasks like rebuilding a web app's source code from screenshots alone.

它能从精细的科学图表中提取准确数字，也能完成复杂的视觉类任务——比如仅凭截图重建一个 Web 应用的源代码。

It also needs less scaffolding: for example, previous Claude models struggled to play Pokémon FireRed even with harnesses that gave them additional helpful tools, but Fable 5 beat FireRed with a minimal, vision-only harness.

它也需要更少的脚手架（scaffolding）：比如以往的 Claude 模型即使配上提供了额外有用工具的 harness，玩《宝可梦 火红》（Pokémon FireRed）仍然吃力，而 Fable 5 只用一个极简的、纯视觉的 harness 就通关了火红。

A time-lapse of Claude playing Pokémon FireRed from start to finish using only raw game screenshots—with no maps, navigation aids, or extra game-state information.

（图注）Claude 仅凭原始游戏截图从头到尾通关《宝可梦 火红》的延时录像——没有地图、没有导航辅助、也没有额外的游戏状态信息。

Earlier Claude models needed a complex helper harness to play Pokémon; Claude Fable 5 completed the game with vision alone.

早先的 Claude 模型需要一套复杂的辅助 harness 才能玩宝可梦；Claude Fable 5 仅靠视觉就通了关。

Memory and long-context.

**记忆与长上下文。**

Fable 5 stays focused across millions of tokens in long-running tasks and improves its outputs using its own notes.

在长时程任务中，Fable 5 能在数百万 token 的跨度上保持专注，并利用自己写下的笔记改进产出。

When we had the model play the deck-building game Slay the Spire, giving it access to persistent file-based memory improved its performance three times more than for Opus 4.8; Fable also reached the game's final act three times more often.

当我们让模型玩卡牌构筑游戏《杀戮尖塔》（Slay the Spire）时，给它接入基于文件的持久记忆所带来的性能提升，是 Opus 4.8 的三倍；Fable 打到游戏最终章的频率也高出三倍。

Solar eclipses / Factorio / VibeCAD / Fluid with Classical EDM

（演示分栏标题）日食 / 异星工厂 / VibeCAD / 古典电音流体模拟

Claude Fable 5 built this simulation of the solar system, deriving the planets' orbital motion from physics first principles and using it to predict solar eclipses.

（图注）Claude Fable 5 构建了这个太阳系模拟：从物理学第一性原理推导行星轨道运动，并据此预测日食。

Claude Fable 5 autonomously plays Factorio, the factory-building game beloved by engineers, strategizing and building an automated factory on its own.

（图注）Claude Fable 5 自主游玩工程师们钟爱的工厂建造游戏《异星工厂》（Factorio），自己制定策略并搭建自动化工厂。

Claude Fable 5 designs a complete 3D-printable model in a browser-based CAD editor.

（图注）Claude Fable 5 在一个基于浏览器的 CAD 编辑器里设计出了完整的可 3D 打印模型。

The editor itself was also created by Fable 5, including the built-in AI copilot that does the modeling.

编辑器本身也是 Fable 5 做的，包括其中负责建模的内置 AI 副驾。

A fluid simulation coded by Claude Fable 5 where the motion is synchronized to the beat of a classical music EDM remix—which Claude Fable 5 produced using code, having never heard music before.

（图注）一段由 Claude Fable 5 编写的流体模拟，其运动与一首古典音乐 EDM 混音的节拍同步——而这首混音也是 Claude Fable 5 用代码生成的，尽管它从未听过音乐。

Drug design: Using Mythos 5, our internal protein design experts accelerated aspects of the drug design process by around 10 times.

**药物设计：** 借助 Mythos 5，我们内部的蛋白质设计专家把药物设计流程中的若干环节加速了约 10 倍。

In one example, they found that Mythos 5, with protein design and bioinformatics tools but no human assistance, matches or beats skilled human operators.

在一个例子中，他们发现 Mythos 5 在配备蛋白质设计与生物信息学工具、但没有任何人类协助的情况下，表现追平甚至超过了熟练的人类操作者。

In doing so, the model executes all of the tasks that are normally completed by a scientist: choosing binding sites, selecting and running protein design tools, and recovering from failures along the way.

在此过程中，模型执行了通常由科学家完成的全部任务：挑选结合位点、选择并运行蛋白质设计工具，以及在过程中从失败里恢复。

Nine of the 14 protein targets from this study (shown below) yielded strong candidates for drug design that we're currently investigating.

这项研究涉及的 14 个蛋白质靶点中（见下图），有 9 个产出了有力的药物设计候选，我们正在对其做进一步研究。

Protein complexes designed by Mythos 5.

（图注）由 Mythos 5 设计的蛋白质复合物。

Targets include immune checkpoints, growth-factor and receptor signaling, neurodegeneration, muscle disease, and harder structural targets.

靶点涵盖免疫检查点、生长因子与受体信号通路、神经退行性疾病、肌肉疾病，以及更难攻的结构性靶点。

Novel hypotheses in molecular biology.

**分子生物学中的新颖假说。**

Mythos 5 is our first model to consistently produce novel, compelling scientific hypotheses.

Mythos 5 是我们第一个能稳定产出新颖且有说服力的科学假说的模型。

In blinded head-to-head comparisons against Opus-class models, our scientists preferred Mythos's molecular biology hypotheses ~80% of the time, and have advanced several to experimental evaluation.

在与 Opus 级模型的盲测一对一比较中，我们的科学家约 80% 的情况下更青睐 Mythos 提出的分子生物学假说，并已将其中数个推进到实验验证阶段。

In the meantime, one Mythos hypothesis—a novel mechanism for an E. coli protein—was corroborated in a study from a lab independently working on the same problem.

与此同时，Mythos 提出的一个假说——关于某个大肠杆菌蛋白的新机制——被一个独立研究同一问题的实验室的研究所印证。

Novel research in genomics.

**基因组学中的原创研究。**

Mythos 5 conducted novel genomics research in over a week of largely autonomous work.

Mythos 5 在一周多的时间里以基本自主的方式开展了原创的基因组学研究。

It assembled single-cell data for millions of cells spanning 138 animal species and designed and trained a custom machine learning model to identify cells performing the same role in even distantly related organisms.

它汇集了跨 138 个动物物种、数百万个细胞的单细胞数据，并设计训练了一个定制机器学习模型，用来识别在亲缘关系很远的生物体中承担相同功能的细胞。

With only high-level human input, Mythos 5's trained model outperformed a recent model published in the journal Science—despite being 100 times smaller.

在人类只提供高层次输入的情况下，Mythos 5 训练出的模型胜过了近期发表在《科学》（Science）杂志上的一个模型——尽管其规模只有后者的百分之一。

We intend to publish these results in the coming months.

我们打算在未来几个月内发表这些结果。

Alignment.

**对齐。**

In our automated alignment assessment, we found that Mythos 5's level of misaligned behavior (including misaligned actions taken by the model such as deception and cooperation with misuse of the model by a user) was low, and similar to that of Opus 4.8.

在我们的自动化对齐评估中，我们发现 Mythos 5 的失准行为（misaligned behavior）水平较低，与 Opus 4.8 相当——这里的失准行为包括模型采取的失准动作，例如欺骗，以及配合用户滥用模型。

Given that they are the same underlying model, Fable 5's level of alignment will be similar.

鉴于两者是同一个底层模型，Fable 5 的对齐水平也会与之类似。

The assessment is described in full, along with a detailed suite of other safety and capabilities tests, in the model's system card.

该评估的完整描述，连同其他一整套详细的安全与能力测试，都记载在模型的系统卡（system card）中。

Overall level of misaligned behaviors from our automated alignment assessment.

（图注）我们自动化对齐评估中测得的失准行为总体水平。

See section 6.2.3.1 of the system card for more.

更多内容见系统卡第 6.2.3.1 节。

## Early feedback for Claude Fable 5｜Claude Fable 5 的早期反馈

Customers with early access ran their own tests on Fable 5.

获得早期访问权限的客户在 Fable 5 上跑了各自的测试。

Below, in their words, is a selection of what they're seeing:

以下是他们观察到的情况的节选，均为原话：

Claude Fable 5 is the state of the art model on CursorBench.

Claude Fable 5 是 CursorBench 上的业界最优模型。

It's opened up a class of long-horizon problems that were out of reach for earlier models.

它打开了一类此前模型够不着的长时程（long-horizon）问题。

> — Michael Truell，CEO 兼联合创始人（Cursor）

Claude Fable 5 is a real step forward for the developers GitHub serves.

对 GitHub 服务的开发者来说，Claude Fable 5 是实实在在的一步跨越。

In our early testing, it took on complex, long-horizon coding tasks with a level of autonomy and reliability that exceeded previous benchmarks.

在我们的早期测试中，它处理复杂的长时程编码任务时所表现出的自主性与可靠性，超出了以往的基准水平。

But what excites us most is the direction it points: a future where developers can hand increasingly ambitious work to agents and trust the results across the software lifecycle.

但最让我们兴奋的是它指向的方向：一个开发者可以把越来越宏大的工作交给智能体、并在整个软件生命周期中信任其结果的未来。

> — Mario Rodriguez，首席产品官（GitHub）

These are the strongest results of any Claude model we've had the opportunity to test.

这是我们有机会测试过的所有 Claude 模型中最强的结果。

Claude Fable 5 is a clear step forward on agentic coding and prototyping.

在智能体编码（agentic coding）与原型开发上，Claude Fable 5 是明确的一步跨越。

> — Matt Colyer，开发者方向产品总监

Claude Fable 5's reasoning is a clear step beyond Opus 4.8.

Claude Fable 5 的推理能力明显超出 Opus 4.8 一个台阶。

It works at senior research scientist grade — picking directions, allocating resources, killing its incorrect beliefs, and producing novel first-principles outputs.

它的工作水准达到了资深研究科学家的级别——选定方向、分配资源、砍掉自己的错误信念，并产出基于第一性原理的新颖成果。

> — Sean Ward，CEO 兼联合创始人

Claude Fable 5 understands what builders mean, not just what they type.

Claude Fable 5 理解的是构建者的意图，而不只是他们敲进去的字。

Apps that took a hundred prompts a year ago, it now one-shots.

一年前需要上百条提示词才能做出来的应用，它现在一次就搞定。

When a customer really hits a wall, it's the model we reach for to get them past it quickly, so they can finish what they set out to build.

当客户真的卡住时，我们就搬出这个模型帮他们快速突破，好让他们把想做的东西做完。

> — Fabian Hedin，CTO 兼联合创始人

Claude Fable 5 feels materially different.

Claude Fable 5 给人的感觉是有实质性差别的。

In blind review, our lawyers found its redlines matched or beat our current model every time.

在盲审中，我们的律师发现它给出的修订标注每一次都追平或胜过我们当前使用的模型。

> — Aveek Duttagupta，技术团队成员

At the highest effort, Claude Fable 5 reflects on and validates its own work.

在最高推理档位下，Claude Fable 5 会反思并验证自己的工作。

For us, that's what makes highly autonomous operations possible — the extra thinking pays for itself.

对我们来说，正是这一点让高度自主的运作成为可能——多花的那些思考是划算的。

> — Yusuke Kaji，商用 AI 业务总经理

Claude Fable 5 delivers more capable engineering in fewer turns than prior models — handling the complex multi-agent workflows our employees run daily in Claude Code.

Claude Fable 5 用比以往模型更少的轮次交付了更强的工程能力——能扛住我们员工每天在 Claude Code 里跑的复杂多智能体工作流。

> — Luke Anderson，CTO

Claude Fable 5 is the highest-scoring model on FrontierBench, Cognition's frontier coding eval.

在 Cognition 的前沿编码评测 FrontierBench 上，Claude Fable 5 是得分最高的模型。

It excels at long-horizon reasoning and generalizes to unfamiliar tools out of the box.

它擅长长时程推理，并且开箱即用地泛化到不熟悉的工具上。

> — Scott Wu，CEO（Cognition）

Claude Fable 5 is the strongest finance-first model we've tested, both on general finance and reasoning.

Claude Fable 5 是我们测试过的最强的「金融优先」模型，无论在通用金融还是推理方面。

It's a notable step up.

这是一次显著的提升。

> — Damian Miraglia，应用 AI 首席工程师

Claude Fable 5 is the first to break 90% on our core analytics benchmark of complex, long-running analytical tasks — a 10-point jump over Opus.

在我们那套由复杂长时分析任务组成的核心分析基准上，Claude Fable 5 是第一个突破 90% 的模型——比 Opus 高出 10 个百分点。

On the hardest questions, it shows strong judgment and attention to nuance.

在最难的问题上，它展现出很强的判断力和对细微差别的把握。

> — Izzy Miller，AI 研究负责人

Claude Fable 5 is the strongest model we've tested on frontier physics research while using a third of the reasoning tokens.

在前沿物理研究上，Claude Fable 5 是我们测过的最强模型，而它只用了三分之一的推理 token。

In 36 hours it got nearly to where GPT-5.5 landed after four days.

36 小时内，它就基本达到了 GPT-5.5 花四天才到达的位置。

> — Matthew Pines，CEO

On ViBench, our end-to-end vibe-coding benchmark, Claude Fable 5 is the highest-performing model we've tested — nearly saturating our base use cases and building apps in less time with fewer tokens.

在我们的端到端 vibe-coding 基准 ViBench 上，Claude Fable 5 是我们测过表现最好的模型——几乎把我们的基础用例刷满了，而且用更少的时间、更少的 token 就把应用搭了出来。

> — Michele Catasta，总裁兼 AI 负责人

Claude Fable 5 beats Opus 4.8 on our everyday spreadsheet suite at every effort level — and it does it with fewer turns, finishing runs 25–30% faster.

在我们的日常电子表格测试集上，Claude Fable 5 在每一个推理档位都胜过 Opus 4.8——而且轮次更少，整体跑完快 25–30%。

> — Peter Wang，首席科学官

## Claude Fable 5's new safeguards｜Claude Fable 5 的新安全防护

Mythos-class models have reached a threshold where they present significant risks.

Mythos 级模型已经跨过了一个门槛，开始带来重大风险。

In April we began Project Glasswing, releasing the first Mythos-class model (Claude Mythos Preview) to only a limited group of cyber defenders and critical software infrastructure providers.

四月我们启动了 Project Glasswing，把第一个 Mythos 级模型（Claude Mythos Preview）只发布给一小批网络防御方和关键软件基础设施提供方。

When we did so, we stated that we hoped to eventually release Mythos-level capabilities to all our users, so long as we had developed new safeguards that were strong enough to reliably prevent misuse.

当时我们表示，希望最终能把 Mythos 级能力开放给所有用户——前提是我们已经研发出足够强、能可靠防止滥用的新防护机制。

Over the past few months we have been improving these safeguards, and they are now robust enough for a general release.

过去几个月我们一直在改进这些防护，现在它们已经稳健到可以支撑一次面向公众的发布。

Because we have prioritized safety, we've deliberately tuned the safeguards to be cautious, and they are still stricter than would be ideal—for example, sometimes benign requests will trigger our classifiers.

由于我们把安全放在首位，我们刻意把防护调得偏谨慎，它们目前仍比理想状态更严格——比如有时无害的请求也会触发我们的分类器（classifier）。

We recognize that this will be frustrating to some users, and our aim is to reduce false positives as we update and refine the safeguards after launch.

我们知道这会让一些用户感到沮丧；我们的目标是在发布后持续更新和细化防护，把误报降下来。

Below we discuss each of Fable 5's new safeguards in turn.

下面我们逐一介绍 Fable 5 的各项新防护。

Our wider suite of safeguards is discussed and evaluated in the model's system card and our most recent risk report.

我们更完整的防护体系在模型的系统卡和我们最新的风险报告中有讨论与评估。

### Safety classifiers｜安全分类器

The frontier cybersecurity and research biology capabilities of Mythos-class models mean that they pose a substantial risk of uplift to malicious actors.

Mythos 级模型在网络安全与研究型生物学上的前沿能力，意味着它们有很大风险为恶意行为者提供能力增益（uplift）。

That is, these models could provide information or advice that assists those actors in causing serious harm that they couldn't have received from other sources (for example, from internet search engines).

也就是说，这些模型可能提供某些信息或建议，帮助这些行为者造成严重危害，而这些信息是他们从其他渠道（比如互联网搜索引擎）拿不到的。

Furthermore, a great deal of advanced usage of AI models is dual use: the same queries that are beneficial in the hands of cybersecurity professionals and biology researchers could be dangerous if available to malicious actors.

此外，AI 模型的大量高级用法都是双用途（dual use）的：同样的查询，在网络安全专家和生物研究者手里是有益的，落到恶意行为者手里就可能是危险的。

We therefore need strong safeguards to prevent misuse, and their coverage needs to be broad.

因此我们需要强有力的防护来阻止滥用，而且覆盖面必须足够广。

The safeguards themselves have to stand up to sustained and sophisticated attempts to bypass them (also known as "jailbreaking" the system).

防护本身必须能顶住持续而精巧的绕过尝试（也就是所谓的对系统「越狱」，jailbreaking）。

The uplift from Mythos-level capabilities is valuable to many adversaries—for instance, those who could financially gain from cyberattacks—and we therefore expect them to be motivated to try to circumvent our safety measures.

Mythos 级能力带来的增益对许多对手都很有价值——比如那些能从网络攻击中获利的人——所以我们预计他们会有强烈动机去设法绕开我们的安全措施。

Fable 5 comes with a new set of classifiers: separate AI systems that detect potential misuse, including jailbreak attempts, and prevent the main model (in this case, Fable 5) from responding.

Fable 5 配备了一套新的分类器：这是一些独立的 AI 系统，用来检测潜在的滥用（包括越狱尝试），并阻止主模型（这里就是 Fable 5）作答。

We've been running classifiers on our models for some time, and Fable 5's classifiers are an extension of this previous work with extra coverage.

我们在模型上运行分类器已有一段时间，Fable 5 的分类器是在此前工作基础上扩展、增加了覆盖范围。

When Fable's classifiers detect a request related to cybersecurity, biology and chemistry, or distillation, the response is automatically handled by Claude Opus 4.8 instead.

当 Fable 的分类器检测到与网络安全、生物化学或蒸馏（distillation）相关的请求时，该请求会自动改由 Claude Opus 4.8 来回答。

Users will be informed whenever this occurs.

每当这种情况发生时，用户都会收到告知。

Opus 4.8 is a highly capable model in its own right: a response that falls back to Opus is a far better experience than an outright refusal from Fable.

Opus 4.8 本身就是一个能力很强的模型：回退（fall back）到 Opus 作答，体验远好于 Fable 直接拒答。

Our early data shows that more than 95% of Fable sessions involve no fallback at all—for those sessions, Fable 5's performance is effectively the same as that of Mythos 5.

我们的早期数据显示，超过 95% 的 Fable 会话完全不涉及回退——在这些会话里，Fable 5 的表现实际上与 Mythos 5 相同。

The following are the areas covered by the classifiers:

分类器覆盖的领域如下：

1. Cybersecurity.

**1. 网络安全。**

Mythos-class models excel at discovering and exploiting software vulnerabilities.

Mythos 级模型极擅长发现并利用软件漏洞。

They can thus make cyberattacks substantially easier and cheaper to commit.

因此它们可能让实施网络攻击变得容易得多、便宜得多。

Mythos-class models also show strong skills in agentic hacking.

Mythos 级模型在智能体式入侵（agentic hacking）上也表现出很强的能力。

This involves performing multiple different parts of a cyberattack in addition to finding exploits—reconnaissance, discovery, lateral movement, and more.

这不仅包括找到可利用的漏洞，还包括执行网络攻击中的多个不同环节——侦察、探测、横向移动等等。

To prevent these agentic hacking skills providing uplift in cyberattacks, we designed our cybersecurity classifiers to cover both exploitation and offensive cyber tasks in a broader sense.

为了防止这些智能体式入侵能力在网络攻击中提供增益，我们把网络安全分类器设计成既覆盖漏洞利用，也覆盖更广义上的攻击性网络任务。

As shown in the graph below, our classifiers prevent Fable from making any progress on these tasks.

如下图所示，我们的分类器让 Fable 在这些任务上无法取得任何进展。

Results of running cyber evaluations,3 with Fable 5 in a mode that blocks responses rather than falling back to Opus 4.8.

（图注）网络安全评测的运行结果，其中 Fable 5 处于「直接拦截回答」而非回退到 Opus 4.8 的模式。

Evaluations did not involve attempts to evade safeguards.

评测中没有包含规避防护的尝试。

We extensively red-teamed our classifiers to test their robustness against jailbreaks.

我们对分类器做了大量红队测试（red-teaming），检验其抵御越狱的稳健性。

As well as internal testing, we ran an external bug bounty that produced no universal jailbreaks in over 1,000 hours of testing.

除内部测试外，我们还开展了一项外部漏洞赏金计划，在 1000 多小时的测试中没有产生任何通用越狱（universal jailbreak）。

External red-teaming organizations we engaged also failed to find any universal jailbreaks on long-form agentic tasks so far—although the UK AISI has made progress towards one within a brief initial testing window.4

我们聘请的外部红队组织到目前为止也没能在长篇智能体任务上找到通用越狱——尽管英国 AISI 在一个短暂的初期测试窗口里已经朝这个方向取得了一些进展。

It is likely impossible to completely prevent universal jailbreaks, but our goal is to make any remaining jailbreaks sufficiently slow and costly that we can detect and prevent them before they are used at scale.

要完全杜绝通用越狱大概是不可能的，但我们的目标是让残余的越狱手段足够慢、足够昂贵，好让我们在它们被大规模使用之前发现并阻止。

The graph below, from one of our internal evaluations, illustrates how Fable 5's safeguards give it greater resistance to jailbreaks than our previous generally accessible models.

下图来自我们的一项内部评测，展示了 Fable 5 的防护如何使其比我们此前面向公众开放的模型更能抵抗越狱。

Results of an internal evaluation in which an automated red-teamer tries to use the model to complete a short task related to offensive cybersecurity across 400 turns, restarting and rewinding when blocked.

（图注）一项内部评测的结果：一个自动化红队在 400 轮对话中试图让模型完成一项与攻击性网络安全相关的短任务，被拦截时就重启或回退重来。

The tasks are mostly simple and not representative of real cyber usage—they are sometimes as simple as encrypting files on a remote server.

这些任务大多很简单，并不代表真实的网络攻防用法——有时简单到只是加密远程服务器上的文件。

On more complex and realistic tasks, we have not yet seen successful jailbreaks on our production system.

在更复杂、更贴近现实的任务上，我们的生产系统尚未出现成功的越狱。

Note that Opus 4.6 does not have blocking cyber safeguards.

请注意，Opus 4.6 并没有拦截式的网络安全防护。

One of our external partners found that Fable 5's safeguards against harmful cyber queries were the most robust of any model tested (including Opus 4.8 and Opus 4.7).

我们的一家外部合作方发现，Fable 5 针对有害网络安全查询的防护是所有受测模型中最稳健的（受测模型包括 Opus 4.8 和 Opus 4.7）。

Fable 5 complied with zero harmful single-turn requests relating to planning a cyberattack, exploit development, or defense evasion.

在涉及策划网络攻击、开发漏洞利用程序或规避防御的有害单轮请求中，Fable 5 的配合次数为零。

This held whether or not one of the requests used any of 30 different public jailbreak techniques.

无论请求中是否使用了 30 种公开越狱技术中的任何一种，这一结果都成立。

2. Biology and chemistry.

**2. 生物与化学。**

We have long used our classifiers to block our models from responding on a narrow selection of bioweapons-related queries.

长期以来，我们一直用分类器阻止模型回应一小类与生物武器相关的查询。

But we are no longer certain that blocking this narrow selection is enough.

但我们现在不再确信，只拦截这一小类就够了。

This is for two reasons: first, we have reason for concern about well-resourced malicious actors attempting to gain uplift from our models for highly risky biological research.

原因有二：第一，我们有理由担心资源雄厚的恶意行为者试图从我们的模型中获取增益，用于高风险的生物学研究。

Second, models now have a greater ability to accomplish real-world scientific tasks.

第二，模型如今完成真实世界科学任务的能力更强了。

For example, we tested Mythos 5's ability to complete a challenging step in designing adeno-associated viruses (AAVs).

举例来说，我们测试了 Mythos 5 完成腺相关病毒（adeno-associated virus，AAV）设计中某个高难度步骤的能力。

AAVs are a component for delivering gene therapies, but the same capability, in the wrong hands, could enable the design of dangerous viruses.

AAV 是递送基因疗法的一个组件，但同样的能力若落入不当之手，就可能被用来设计危险病毒。

In this task, various AI models were evaluated on their ability to predict how a genetic modification would impact the assembly of the virus's outer shell (among a set of therapeutically relevant unpublished candidates developed by Dyno Therapeutics).

在这项任务中，多个 AI 模型被评估预测某项基因改造会如何影响病毒外壳组装的能力（测试对象是 Dyno Therapeutics 开发的一组与治疗相关、尚未发表的候选体）。

We did not explicitly train our models to perform this task—and yet Mythos-class models outperformed sophisticated models dedicated to protein tasks (known as "protein language models") using their biological reasoning alone.

我们并没有专门训练模型来做这项任务——然而 Mythos 级模型仅凭自身的生物学推理，就胜过了专门针对蛋白质任务的复杂模型（即所谓的「蛋白质语言模型」）。

This demonstrates a promising ability to complete simple but important tasks in gene therapy research and development—but also highlights the risk posed by such dual-use capabilities.

这展现出在基因疗法研发中完成简单但重要任务的可期能力——同时也凸显了这类双用途能力所带来的风险。

Results of an evaluation in which our models predicted the unpublished experimental properties of the viral shell of a simple virus.

（图注）一项评测的结果：我们的模型预测某种简单病毒的病毒外壳未发表的实验性质。

Viral shell assembly is the simplest viral trait to predict in this context, but it is nonetheless an important property to get right when designing more complex features.

在这一情境下，病毒外壳组装是最容易预测的病毒特性，但在设计更复杂的功能时，把这个性质预测对仍然很重要。

AAV = adeno-associated virus.

AAV = 腺相关病毒。

Our priority was to safely release Fable as soon as we could, even at the cost of overly broad safeguards.

我们的首要目标是尽快安全地发布 Fable，哪怕代价是防护范围过宽。

Therefore, for the time being we have arranged for Fable to fall back to Opus 4.8 on most requests related to biology and chemistry.

因此，目前我们让 Fable 在大多数与生物和化学相关的请求上回退到 Opus 4.8。

As with all of our classifiers, we hope to narrow these safeguards as soon as possible: as can be seen from the evidence above, there is great potential for positive applications of Fable for science, and we do not want false positives from our classifiers to get in the way.

与我们所有的分类器一样，我们希望尽快收窄这些防护：从上面的证据可以看出，Fable 在科学上有巨大的正向应用潜力，我们不希望分类器的误报挡了路。

In the coming weeks, some biomedical researchers and companies will be able to join our trusted access program for biology capabilities in Mythos 5 (discussed below).

未来几周内，部分生物医学研究者和公司将可以加入我们针对 Mythos 5 生物学能力的可信访问计划（下文详述）。

3. Distillation.

**3. 蒸馏。**

We've previously identified large-scale attempts to extract ("distill") Claude's capabilities to train competing models in authoritarian countries.

我们此前已识别出一些大规模尝试：提取（「蒸馏」）Claude 的能力，用于在威权国家训练竞争模型。

Distillation of Fable 5's abilities could indirectly lead to the proliferation of near-frontier AI capabilities—and these could be released without the appropriate safeguards.

对 Fable 5 能力的蒸馏可能间接导致接近前沿的 AI 能力扩散——而这些能力可能在没有适当防护的情况下被发布出去。

Requests that are flagged by our classifiers as being part of such distillation attempts will fall back to Opus 4.8.

被我们的分类器标记为属于此类蒸馏尝试的请求，将回退到 Opus 4.8。

### A new data retention policy｜新的数据留存政策

Finally, we're making a change to the way we handle business customer data for Fable 5, Mythos 5, and future models with similar or higher capability levels.

最后，我们要调整对 Fable 5、Mythos 5 以及未来同等或更高能力级别模型的企业客户数据处理方式。

We will require 30-day retention for all traffic on Mythos-class models, on both first- and third-party surfaces.

我们将要求对 Mythos 级模型上的所有流量保留 30 天，第一方与第三方渠道均适用。

We won't use this data to train new Claude models, or for any non-safety-related purpose, and we've instituted new privacy protections including logging all human access to the data and ensuring its deletion after 30 days in almost all cases (see this post for further details).

我们不会用这些数据训练新的 Claude 模型，也不会用于任何与安全无关的目的；我们还建立了新的隐私保护措施，包括记录所有人工访问该数据的行为，并确保在几乎所有情况下 30 天后删除（详见相关说明文章）。

The data will help us defend against complex and novel attacks (including new jailbreaks and attacks that operate across many requests) as well as help us identify and reduce false positives.

这些数据将帮助我们防御复杂而新颖的攻击（包括新的越狱手法和跨多个请求实施的攻击），也帮助我们识别并减少误报。

## Claude Mythos 5 and the trusted access program｜Claude Mythos 5 与可信访问计划

Beginning today, all users who currently have access to Claude Mythos Preview (for example, our cybersecurity partners in Project Glasswing) will be able to upgrade to Claude Mythos 5—the same model as Claude Fable 5 but with cyber safeguards lifted.

从今天起，所有当前拥有 Claude Mythos Preview 访问权限的用户（例如 Project Glasswing 中的网络安全合作伙伴）都可以升级到 Claude Mythos 5——与 Claude Fable 5 同一个模型，但解除了网络安全方面的防护。

Users will find Mythos 5 comparable to, or somewhat stronger than, Mythos Preview in most cases, while costing substantially less.

用户会发现在多数情况下 Mythos 5 与 Mythos Preview 相当或略强，而成本大幅降低。

In consultation with the US government, we plan to steadily expand access to Claude Mythos 5, continuing our periodic addition of new partners, as well as pursuing a trusted access program that allows cybersecurity organizations to apply in a more systematic manner.

在与美国政府磋商的基础上，我们计划稳步扩大 Claude Mythos 5 的开放范围：一方面继续定期新增合作伙伴，另一方面推进一个可信访问计划，让网络安全组织能以更系统化的方式提出申请。

Our plans also include opening a trusted access program for biology, to help accelerate biomedical research and discover new therapies with Mythos-class capabilities.

我们的计划还包括开设一个面向生物学的可信访问计划，用 Mythos 级能力帮助加速生物医学研究、发现新疗法。

This program will provide access to Fable 5 with the biology and chemistry safeguards removed (but the cyber safeguards still in place).

该计划将提供解除了生物与化学防护（但网络安全防护仍保留）的 Fable 5 访问权限。

It will enroll a small number of researchers from a variety of life science organizations spanning fundamental and translational research; we're planning to expand access to this program while simultaneously making our safeguards better.

它将吸纳来自各类生命科学组织、横跨基础研究与转化研究的少量研究者；我们计划在扩大该计划开放范围的同时，持续改进我们的防护机制。

## Availability｜可用性

Claude Fable 5 is available everywhere today.

Claude Fable 5 今日起在所有渠道可用。

Claude Mythos 5 is restricted to Glasswing partners (with cyber safeguards lifted) and soon to select biology researchers (with biology and chemistry safeguards lifted) only, until our broader trusted access program is available.

在更广泛的可信访问计划开放之前，Claude Mythos 5 仅限 Glasswing 合作伙伴使用（解除网络安全防护），不久后还将开放给部分生物学研究者（解除生物与化学防护）。

Pricing for both models is $10 per million input tokens and $50 per million output tokens.

两个模型的定价均为每百万输入 token 10 美元、每百万输出 token 50 美元。

Developers can use claude-fable-5 via the Claude API.

开发者可以通过 Claude API 使用 `claude-fable-5`。

We expect demand for Fable 5 to be very high, and difficult to predict.

我们预计 Fable 5 的需求会非常高，且难以预测。

On the Claude API and consumption-based Enterprise plans, Fable 5 is fully available from today.

在 Claude API 和按用量计费的企业版方案上，Fable 5 从今天起完全可用。

For subscription plans, we'd rather give access sooner than later, so we're rolling out more conservatively, in stages:

对于订阅制方案，我们宁可早开放也不愿拖着，因此采取更保守的分阶段推出方式：

- From today through June 22, Fable 5 is included on Pro, Max, Team, and seat-based Enterprise plans at no extra cost.

- 从今天起至 6 月 22 日，Pro、Max、Team 以及按席位计费的企业版方案都免费包含 Fable 5。

- On June 23, we'll remove Fable 5 from those plans. Using it after that will require usage credits. If capacity allows, we'll extend the included window.

- 6 月 23 日，我们将把 Fable 5 从这些方案中移除，此后使用需要消耗用量额度（usage credits）。若产能允许，我们会延长免费包含的窗口期。

- After this point—when sufficient capacity allows us to do so—we aim to restore Fable 5 as a standard part of subscription plans. We intend to do this as quickly as we can.

- 在此之后——一旦产能充足——我们的目标是让 Fable 5 重新成为订阅方案的标准组成部分，并且会尽快落实。

Throughout this period, we'll communicate any changes ahead of time so users know where things stand.

在整个期间，任何变更我们都会提前告知，让用户清楚当前状况。

Edit June 9, 2026: Updated the discussion of AAVs to note that the candidates were developed by Dyno Therapeutics.

2026 年 6 月 9 日编辑：更新了关于 AAV 的表述，注明相关候选体由 Dyno Therapeutics 开发。

---

## 附：页面顶部状态更新横幅｜Page update banners

> 这两条是原文页面顶部的状态横幅，非正文内容，但记录了发布后的重要变动，一并对照收录。

Update — Claude Mythos 5 and Fable 5 redeployed (Jul 1, 2026)

更新——Claude Mythos 5 与 Fable 5 重新部署（2026 年 7 月 1 日）

Claude Fable 5 and Mythos 5 are now available.

Claude Fable 5 与 Mythos 5 现已恢复可用。

Claude Mythos 5 and Fable 5 access unavailable (Jun 12, 2026)

Claude Mythos 5 与 Fable 5 访问不可用（2026 年 6 月 12 日）

We are suspending access to Claude Fable 5 and Claude Mythos 5.

我们正在暂停 Claude Fable 5 与 Claude Mythos 5 的访问。

We apologize for this disruption to our customers and are working to restore access as soon as possible.

我们为此次服务中断向客户致歉，正在尽快恢复访问。
