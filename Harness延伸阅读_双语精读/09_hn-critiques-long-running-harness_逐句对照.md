# 09_HN: Effective harnesses for long-running agents_长时程 harness 的反方观点（HN 讨论逐句对照）

> 原文：https://news.ycombinator.com/item?id=46081704
> 来源：Hacker News 讨论串（125 分 / 37 条评论，2025-11）｜性质：**从业者匿名讨论，无一手数据、无第三方核验，证据等级最低**

## 📌 本篇速览

- 📅 讨论围绕 Anthropic《Effective harnesses for long-running agents》展开，本文为讨论串核心评论的逐句对照全文
- ⭐ ★★★★☆ **值得读，用途明确：这是综述里所有反方观点的一手出处。** 面试或设计评审只讲共识会显得没有批判性——这一篇提供「我知道它的局限在哪」的原始弹药。
- 🏷 70/30 帕累托问题、understanding cannot be outsourced、专职 QA 智能体失效、成本失控、重新发明 issue tracker
- ⚠️ **证据等级提示**：以下全部是从业者的匿名自述，无对照实验、无可核验数字。引用时应当说「有从业者报告」，**不要说「研究表明」**。
- 🖼 配套转述版见 [09_双语精读](09_hn-critiques-long-running-harness_双语精读.md)　·　🗂 [返回专题目录](00_目录.md)

本篇收录讨论串中 31 条有实质观点的评论（合并为 30 个小节），按原讨论树顺序排列；纯灌水、勘误与已删除评论见文末「未收录评论概况」。

---

### 评论人 roughly｜70/30 曲线：LLM 的「省力假象」会把你引向深渊（全场最高赞主题）

One of the things that makes it very difficult to have reasonable conversations about what you can do with LLMs is the effort-to-outcome curve is basically exponential - with almost no effort, you can get 70% of the way there.

关于「LLM 到底能做什么」之所以很难进行理性讨论，一个原因在于它的投入-产出曲线（effort-to-outcome curve）基本上是指数型的——几乎不费什么力气，你就能走完前 70% 的路。

This looks amazing, and so people (mostly executives) look at this and think, "this changes everything!"

这看起来非常惊艳，于是人们（主要是高管们）看到这一幕就会想：「这将改变一切！」

The problem is the remaining 30% - the next 10-20% starts to require things like multi-agent judge setups, external memory, context management, and that gets you to something that's probably working but you sure shouldn't ship to production.

问题出在剩下的 30%——接下来的 10~20% 开始需要多智能体评判系统（multi-agent judge setups）、外部记忆（external memory）、上下文管理（context management）这类东西，而这些只能让你得到一个「大概能跑，但你绝对不该上生产环境」的东西。

As to the last 10% - I've seen agentic workflows with hundreds of different agents, multiple models, and fantastically complex evaluation frameworks to try to reduce the error rates past the ~10% mark.

至于最后那 10%——我见过用上数百个不同智能体、多个模型、外加极其复杂的评估框架的智能体工作流，就为了把错误率压到 10% 以下。

By a certain point, the amount of infrastructure and LLM calls are running into several hundred dollars per run, and you're still not getting guaranteed reliable output.

到了某个程度，基础设施和 LLM 调用的开销会飙到单次运行数百美元，而你仍然得不到有保证的可靠输出。

If you know what you're doing and you know where to fit the LLMs (they're genuinely the best system we've ever devised for interpreting and categorizing unstructured human input), they can be immensely useful, but they sing a siren song of simplicity that will lure you to your doom if you believe it.

如果你清楚自己在做什么、知道该把 LLM 放在哪个位置（它们确实是我们发明过的、解释和归类非结构化人类输入的最好系统），它们可以极其有用；但它们唱着一首「简单性的塞壬之歌」（siren song of simplicity）——你要是信了，它就会把你引向覆灭。

### 评论人 zephyrthenoble｜帕累托原则被误读：一把梭出来的「80%」其实只有 50%

Yes, it's essentially the Pareto principle.

对，这本质上就是帕累托原则（Pareto principle）。

The LLM community has conflated the 80% as difficult complicated work, when it was essentially boilerplate.

LLM 社区把那 80% 混同为困难复杂的工作，而它本质上只是样板代码（boilerplate）。

Allegedly LLMs have saved us from that drudgery, but I personally have found that (without the complicated setups you mention) the 80% done project that gets one shot is in reality more like 50% done because it is built on an unstable foundation, and that final 20% involves a lot of complicated reworking of the code.

据说 LLM 把我们从这种苦役中解救了出来，但我个人的发现是（在没有你提到的那些复杂设置的前提下），那个一把梭（one shot）出来的「完成了 80%」的项目，实际上更像只完成了 50%——因为它建在一个不稳固的地基上，而最后那 20% 会牵扯到大量对代码的复杂返工。

There's still plenty of value but I think it is less than proponents would want you to believe.

价值仍然是有不少的，但我认为比鼓吹者想让你相信的要少。

Anecdotally, I have found that even if you type out paragraph after paragraph describing everything you need the agent to take care of, it eventually feels like you could have written a lot of the code yourself with the help of a good IDE by the time you can finally send your prompt off.

就个人经验而言，我发现哪怕你一段接一段地打字，把需要智能体处理的每件事都写清楚，等你终于能把提示词发出去的时候，往往会觉得：这些时间里靠一个好 IDE 你自己都能把很多代码写完了。

### 评论人 roughly｜理解系统这份工作无法外包给 LLM（本串最有分量的论证）

Yeah, my mental model at this point is there's two components to building a system: writing the code and understanding the system.

对，我现在的心智模型是：构建一个系统包含两个组成部分——写代码，和理解系统。

When you're the one writing the code, you get the understanding at the same time.

当写代码的人是你自己时，理解是同步获得的。

When you're not, you still need to put in that work to deeply grok the system.

当写代码的不是你时，你仍然必须投入那份工作去深刻地领会（grok）这个系统。

You can do it ahead of time while writing the prompts, you can do it while reviewing the code, you can do it while writing the test suite, or you can do it when the system is on fire during an outage, but the work to understand the system can't be outsourced to the LLM.

你可以在写提示词时提前做，可以在 review 代码时做，可以在写测试套件时做，也可以在系统着火、生产事故的当口做——但理解系统的这份工作，没法外包给 LLM。

### 评论人 beefnugs｜质疑：如果真是这样，为什么没出现「一线开发」这种岗位

This can't really be the full story, or else people would have already come up with the "first line developer" like first line support.

事情不可能就这么简单，否则人们早就该发明出类似「一线客服」的「一线开发」（first line developer）岗位了。

There is a dumbass or executive who creates that first 70 or 80%.

先由某个傻瓜或者高管搞出前 70% 或 80%。

Then hands off the entire thing to a professional developer to keep working on it.

然后把整个东西移交给一位专业开发者继续做下去。

The AI people sure dont want that, thats too telling about its limitations and value

搞 AI 的人肯定不想要这种模式——因为它太能暴露这项技术的局限和真实价值了。

### 评论人 peab｜反方：那 80% 在过去可能得雇一个初级工程师来做

Except in the past, I'd perhaps have to hire a junior engineer to do that 80%.

只不过在过去，那 80% 我可能得雇一个初级工程师（junior engineer）来做。

Now i don't need to do that

现在我不需要了。

### 评论人 theLiminator｜LLM 最好用的姿势是「极度复杂的自动补全」

*（先引用了 roughly 上文「简单性的塞壬之歌」那段话，然后回应：）*

I imagine using their embeddings and training a classifier on top of that is probably a lot more effective?

我猜，用它们的嵌入（embeddings）、再在上面训练一个分类器，可能会有效得多？

I've personally found agentic LLM workflows the most effective as extremely sophisticated autocomplete.

我个人发现，智能体式 LLM 工作流最有效的用法是当作「极度复杂的自动补全」（extremely sophisticated autocomplete）。

Instead of autocompleting the current next few tokens, I tell it precisely how to edit my code at a high level.

不是补全眼下的几个 token，而是我在高层面上精确地告诉它该如何修改我的代码。

You can't tell it stuff at a feature level, but telling it how to implement the feature saves me a ton of time.

你没法在「功能」这个层级上给它下指令，但告诉它「这个功能该怎么实现」能帮我省下大把时间。

### 评论人 roughly｜回应：向量嵌入普遍被低估，但复杂的工具编排还没有确定性替代

I'd be interested in seeing this in action - I think the vector embeddings are underused generally - but my understanding is that'd be for something closer to sentiment analysis?

我有兴趣看看这个思路的实际效果——我认为向量嵌入总体上是被低估、用得太少的——但按我的理解，那更适合类似情感分析（sentiment analysis）的场景？

In this case I'm talking about a setup closer to where you've got an LLM agent with a set of tools that's interpreting a user's request to identify which of those tools are the right ones to use.

而我这里说的更接近这样一种设置：一个带一组工具的 LLM 智能体，负责解释用户的请求、判断该用其中哪些工具。

The requests can be complex, and involve multiple tool runs or chaining.

请求可能很复杂，涉及多次工具运行或链式调用（chaining）。

If that's doable by more deterministic mechanisms, I'd (genuinely) love to hear about it.

如果这能用更确定性的机制做到，我（真心地）很想听听。

### 评论人 peab｜LLM 的美在于低成本快速实验：结构化非结构化数据的速度

If you're only working on one problem that's very valuable to solve, then taking the time to train a classifier is great.

如果你只做一个非常值得解决的问题，那花时间训练一个分类器当然很好。

The beauty of LLMs is that you can run a ton of experiments, notebooks, demos etc because you can write classifiers and structure unstructured data so fast, in a reasonably accurate way (at the moment it seems roughly in line with say hiring an intern to label things)

LLM 的美妙之处在于你可以跑一大堆实验、notebook、demo 等等——因为你能以相当快的速度、以还算合理的准确率写出分类器、把非结构化数据结构化（眼下的水平大致相当于雇一个实习生来打标签）。

### 评论人 roughly｜数百智能体系统的真实开发过程：打地鼠

*（回应 morkalork 的追问「几百个智能体的工作流要多少人做多久」：）*

I've seen a couple solo efforts and a couple teams, but usually a few months.

我见过几个单人项目、也见过几个团队做的，但通常都要花几个月。

It tends to evolve as a kind of whack-a-mole situation - "we solved that failure case/hallucination, now we're getting this one."

它往往会演变成一种「打地鼠」（whack-a-mole）局面——「我们解决了那个失败案例/幻觉，现在又冒出了这个。」

### 评论人 ineedasername｜这些组织多半是在重造自己原本就有的问题

My sense is that these are organizations where they probably recreated, with some minor details changed, the same problems they already had.

我的感觉是，这些组织大概率只是把自己原本就有的问题换了些小细节又重造了一遍。

Under planned and over-engineered in the attempt to fix and if things ever work it's more from some awful meta stable chaos than anything else.

规划不足、又在修补时过度工程化（over-engineered），就算最后真能跑起来，也更多是靠某种糟糕的亚稳态混沌（meta stable chaos），而不是靠别的什么。

### 评论人 mips_avatar｜关键是避免长对话：200k 上下文用完就推倒重来（含其自我追评）

I now think the key is you avoid long running conversations.

我现在认为，关键就是避免长时间运行的对话。

If the piece didn't work out by the time you hit 200k context on Claude you are going to start over.

如果在 Claude 上用到 200k 上下文时这块工作还没做成，你就该从头再来。

Take whatever wins you learned from the first stab and give those insights to the model on round two, but throw the code out.

把第一次尝试里学到的所有「赢面」（wins）作为洞察喂给第二轮的模型，但代码要扔掉。

Maybe Claude's long running agent should just be hunting for any wins during the first 200k chucking it away and seeing if those wins change the initial goal.

也许 Claude 的长时程智能体就应该把第一个 200k 纯粹用来搜寻各种赢面，然后整个丢弃，再看看这些赢面是否会改变最初的目标。

### 评论人 _boffin_｜Anthropic 在从零重新发明项目追踪器

…it really feels like they're attempting to reinvent a project tracker and starting off from scratch in thinking about it.

……真的感觉他们是在试图重新发明一个项目追踪器（project tracker），而且是从零开始琢磨这件事。

It feels like they're a few versions behind what I'm doing, which is… odd.

感觉他们比我现在的做法落后好几个版本，这就……很奇怪。

Self-hosting a plane.io instance. Added a plane MCP tool to my codex.

我自托管了一个 plane.io 实例，给我的 Codex 加了一个 Plane 的 MCP 工具。

Added workflow instructions into Agents.md which cover standards, documentation, related work, labels, branch names, adding of comments before plan, after plan, at varying steps of implementation, summary before moving ticket to done.

在 Agents.md 里写入了工作流指令，涵盖：规范、文档、相关工作、标签、分支命名、在计划前/计划后/实现的各个步骤添加评论、把工单移到「完成」之前先写总结。

Creating new tickers and being able to relate to current or others, etc…

创建新工单、并能把它关联到当前或其他工单，等等……

It ain't that hard.

这没那么难。

Just do inception (high to mid level details) create epics and tasks.

做一次 inception（从高层到中层的细节梳理），创建 epic 和任务就行。

Add personas, details, notes, acceptance criteria and more. Can add comments yourself to update. Whatever.

加上人物角色（persona）、细节、备注、验收标准（acceptance criteria）等等；你自己也可以加评论来更新，随便什么都行。

Slice tickets thin and then go wild.

把工单切薄（slice tickets thin），然后放开手脚干。

Add tickets as your working though things. Make modifications.

边推进边加工单，随时改。

Why so difficult?

有什么难的？

### 评论人 threecheese｜这是在往回绕向 Workflow：用程序逻辑混合 agency 与控制

This is actually very interesting I think, as Anthropic pushes against The Bitter Lesson a bit!

我倒觉得这非常有意思——Anthropic 这是在稍稍顶撞「苦涩的教训」（The Bitter Lesson）！

The model is a great reasoner, but we still need a concrete way to manage tasks - like we needed for tool calling.

模型是很棒的推理者，但我们仍然需要一种具体的方式来管理任务——就像我们当初需要为工具调用（tool calling）做的那样。

Claude Code has an opinionated loop, something like ReAct/CoT etc with prompting tricks for tasks/skills/etc, but here they add a Hierarchical Controller/Worker thing leveraging the Claude SDK.

Claude Code 有一个带鲜明立场的循环，类似 ReAct/CoT（思维链）那套，加上针对 tasks/skills 等的提示词技巧；而这里他们借助 Claude SDK 又加了一层「分层控制器/工作者」（Hierarchical Controller/Worker）的东西。

Mixing agency with actual control using program logic - not just alignment using prompts screaming in all caps and emoji.

用程序逻辑把自主性（agency）和真正的控制混合起来——而不只是靠全大写加 emoji 咆哮的提示词来做对齐。

We *are* going to break out of the coding agent's loop in this way - it's sorta curving back around to Workflows, after leaving them behind for agency, but right now we need to orchestrate this with deterministic code written mostly by humans - like the git repo anthropic shared.

我们*确实*会以这种方式突破编码智能体的固有循环——这有点像绕了一圈又回到了工作流（Workflows），当初正是为了 agency 才把它抛下的；只是眼下我们还需要用主要由人类编写的确定性代码来做这层编排——就像 Anthropic 分享的那个 git 仓库那样。

This won't last long.

这个阶段不会持续太久。

### 评论人 imron｜他们用 JSON 文件和一个文本文件造了个 issue tracker

This was my take.

我也是这么看的。

They've made an issue tracker out of json files and a text file.

他们用一堆 JSON 文件和一个文本文件造出了一个 issue tracker。

Why not hook an mcp to an actual issue tracker?

为什么不接一个 MCP 到真正的 issue tracker 上呢？

### 评论人 _boffin_｜老派 XP 流程的 agent 化：把 inception 纪律编码成智能体能推理的图

Used an LLM to help write the following up as I'm still pretty scattered about the idea and on mobile.

下面这段是我用 LLM 帮忙整理的，因为这个想法在我脑子里还挺散，而且我在手机上打字。

Something I've been going over in my head: I used to work in a pretty strict Pivotal XP shop.

我最近一直在脑子里过一件事：我以前在一家相当严格的 Pivotal XP（极限编程）公司工作。

PM ran the team like a conductor.

PM 像乐队指挥一样带团队。

We had analysts, QA, leads, seniors.

我们有分析师、QA、lead、资深工程师。

Inceptions for new features were long, sometimes heated sessions with PM + Analyst + QA + Lead + a couple of seniors.

新功能的 inception 会议又长、有时还很激烈，参与者是 PM + 分析师 + QA + Lead + 几位资深工程师。

Out of that you'd get: thinly sliced epics and tasks; clear ownership; everyone aligned on data flows and boundaries; specs, requirements, and acceptance criteria nailed at both high- and mid-level.

会开完你能得到：切得很薄的 epic 和任务；清晰的归属；所有人对数据流和边界达成一致；高层和中层的规格、需求、验收标准全部敲定。

At the end, everyone knew what was talking to what, what "done" meant, and where the edges were.

结束时，每个人都知道什么组件在跟什么组件通信、「完成」意味着什么、边界在哪里。

What I'm thinking about now is basically that process, but agentized and wired into the tooling:

我现在琢磨的，基本上就是这套流程——但把它智能体化（agentized），并接进工具链里：

Any ticket is an entry point into a graph, not just a blob of text — epics ↔ tasks ↔ subtasks; linked specs / decisions / notes; files and PRs that touched the same areas.

任何工单都是进入一张图（graph）的入口，而不只是一坨文本——epic ↔ 任务 ↔ 子任务；关联的规格/决策/笔记；动过相同区域的文件和 PR。

Standards live as versioned docs, not just a random Agents.md: Markdown (with diagrams) that declares where it applies — tags, ticket types, modules; tickets can pin those docs via labels/tags/links.

规范以版本化文档的形式存在，而不只是一个随手写的 Agents.md：带图表的 Markdown，声明自己适用的范围——标签、工单类型、模块；工单可以通过标签/链接把这些文档固定住。

From the agent's perspective, the UI is just a viewer/editor.

从智能体的视角看，UI 只是一个查看器/编辑器。

The real surface is an API: "given this ticket, type, module, and tags, give me all applicable standards, related work, and code history."

真正的接口面是一个 API：「给定这张工单、类型、模块和标签，把所有适用的规范、相关工作和代码历史都给我。」

The agent then plays something like the analyst + senior engineer role: pulls in the right standards automatically; proposes acceptance criteria and subtasks; explains why a file looks the way it does by walking past tickets / PRs / decisions.

然后智能体扮演的角色类似「分析师 + 资深工程师」：自动拉取正确的规范；提议验收标准和子任务；通过回溯过往的工单/PR/决策来解释一个文件为什么长成现在这样。

So it's less "LLM stapled to an issue tracker" and more "that old XP inception + thin-slice discipline, encoded as a graph the agent can actually reason over."

所以它不是「把 LLM 钉在一个 issue tracker 上」，而更像是「把老派 XP 的 inception + 薄切片纪律，编码成一张智能体真正能在其上推理的图」。

### 评论人 beefnugs｜追问：有没有项目试过强制 //TODO 规划层、一次只改一个函数？

Has any project tried forcing a planning layer as //TODO all throughout the code before making any changes? small loops like one //TODO at a time?

有没有项目试过在做任何修改之前，强制先在代码各处铺一层 //TODO 作为规划层？用「一次只处理一个 //TODO」这样的小循环？

What about limiting changes to a function at a time to remain focused?

那把修改限制在「一次一个函数」以保持聚焦呢？

Or is everyone a slave to however the model was designed and currently they are designed for giant one-shot generations only?

还是说所有人都只能受制于模型被设计成的样子——而它们目前就是只为巨大的一次性生成（one-shot generation）设计的？

Is it possible that all local models need to be better is more context used to make simpler smaller changes at a time?

有没有可能，本地模型欠缺的只是「用更多上下文、每次做更简单更小的修改」？

I haven't seen enough specific comparisons of how local models fail vs the expensive cloud models.

关于本地模型和昂贵的云端模型各自是怎么失败的，我还没见过足够具体的对比。

### 评论人 adamgordonbell｜Beads 与官方做法正在收敛

I did find beads helpful for some of this multi-context window tasks.

对于这类跨多个上下文窗口的任务，我确实觉得 beads 挺有帮助。

It sounds a little like there is some convergence between what they are suggesting and how it give you light weight sub tasks that survive a /clear.

听起来他们的建议和 beads 的做法有些收敛的迹象——后者给你的是能在 /clear 之后存活下来的轻量级子任务。

### 评论人 _boffin_｜「失忆的初级开发者」类比：harness 只是把交接纪律形式化了

Love the show!

爱你的节目！

I do see the convergence there.

我确实看到了那个收敛点。

Beads gives you that "state that survives /clear," and Anthropic's harness tries to do something similar at a higher level.

Beads 给你的是「能在 /clear 之后存活的状态」，而 Anthropic 的 harness 试图在更高的层面做类似的事。

I've been thinking about this with a pretty simple, old-school analogy: You're at a shop with solid engineering and ticketing practices.

我一直用一个非常简单、老派的类比来想这件事：你在一家工程实践和工单实践都很扎实的公司。

You just hired a great junior developer.

你刚雇了一位很棒的初级开发者。

They know the stack, maybe even the domain basics, but they don't yet know: your business processes; the quirks of your microservices; local naming conventions, standards, etc.; team norms around testing, logging, and observability.

他们懂技术栈，甚至可能懂领域的基础，但他们还不了解：你们的业务流程；你们微服务的各种怪癖；本地的命名约定、规范等等；团队在测试、日志、可观测性上的行为规范。

You trust them with important tasks, but expect their *context* will frequently get blown away by interruptions, meetings, task-switching, and long weekends.

你放心把重要任务交给他们，但也预料到他们的*上下文*会频繁地被打断、会议、任务切换和长周末一扫而空。

T handle this, need to make sure each ticket or note contains enough structured info so that when they inevitably lose context, they can pick right back up.

为了应对这一点，你需要确保每张工单或笔记都包含足够的结构化信息，让他们在不可避免地丢失上下文之后，能立刻接着干。

For each ticket, you'd likely include: personas and user goals; acceptance criteria, Given/When/Then scenarios; links to specs, documentation, related tickets, or prior art; a short summary of their current understanding; rough plan (steps, what's done/not done); decisions made and their rationale ("I chose X because Y"); open questions or known gotchas.

每张工单里，你多半会写上：人物角色和用户目标；验收标准和 Given/When/Then 场景；规格、文档、相关工单或先例的链接；他们当前理解的简短总结；粗略计划（步骤、什么做完了/什么没做）；已做的决策及其理由（「我选 X 是因为 Y」）；待解问题或已知的坑。

End of day Friday, that junior would ideally leave notes that answer: *"If I have total amnesia next Tuesday, what's the minimum needed to quickly reload my context?"*

周五下班前，这位初级开发者最好留下一份笔记，回答这个问题：*「如果下周二我彻底失忆了，快速重载我的上下文最少需要什么？」*

To me, agent harnesses like Anthropic's or Beads are just formalizing exactly this pattern:

在我看来，Anthropic 或 Beads 这类智能体 harness，就是在把这个模式形式化：

`/clear` or `/new` is like a "long weekend brain wipe."

`/clear` 或 `/new` 就像一次「长周末洗脑式失忆」。

Persistent subtasks or controllers become structured scaffolding.

持久化的子任务或控制器变成了结构化的脚手架。

The crucial piece isn't remembering *everything*, just clearly capturing intent, decisions, rationale, and immediate next steps.

关键不在于记住*一切*，而在于清晰地捕获意图、决策、理由和紧接着的下一步。

My confusion about Anthropic's approach is why they're doing this over plain text files or JSON, instead of leveraging decades of existing tracker and project-management tooling—which already encode this exact workflow and best practice.

我对 Anthropic 做法的困惑在于：为什么要基于纯文本文件或 JSON 来做这件事，而不是利用几十年积累下来的现成追踪器和项目管理工具——它们早就把这套工作流和最佳实践编码进去了。

### 评论人 rancar2｜佐证：这些技巧跨 CLI 通用（Gemini CLI 亲测）

Having done this for Gemini CLI to get it to behave well several months ago to have a non-coding LLM CLI without costs, I can attest that these tips work well across CLIs.

几个月前我为 Gemini CLI 做过同样的事，让它表现得规矩些、当一个零成本的非编码用途 LLM CLI 来用——我可以作证，这些技巧在不同 CLI 之间是通用的。

### 评论人 ford｜我们把 git 想得太理所当然了：其他职能的产出怎么办？

I think we take git for granted as software engineers

我觉得作为软件工程师，我们把 git 看得太理所当然了。

Software engineering has decades of experience with proposing changes, merging them, staging them, deploying them, and rolling them back, and collaborating with other code-writers (engineers and agents).

软件工程在「提出变更、合并、暂存、部署、回滚，以及与其他代码书写者（工程师和智能体）协作」这件事上，有几十年的经验积累。

I'm very interested in what this will look like for outputs from other job functions.

我非常好奇：这套东西放到其他职能的工作产出上会是什么样子。

And if we'll end up with a similar framework that makes non-deterministic, often-wrong LLMs easier to work with.

以及我们最终会不会得到一个类似的框架，让非确定性、经常出错的 LLM 更容易共事。

### 评论人 daxfohl｜专职 QA 智能体听着合理但不好使：不收敛，只会来回打摆

IME a dedicated testing / QA agent sounds nice but doesn't work, for same reasons as AI / human interaction.

以我的经验（IME），专职的测试/QA 智能体听起来很美，但并不好使——原因和 AI 与人类交互的问题如出一辙。

The more you try to diverge from the original dev agent's approach, the less and less chance there is that the dev agent will get to where you want it to be.

你越是想让它偏离原来那个开发智能体的路数，开发智能体到达你想要的终点的概率就越来越小。

Far more frequently it'll get stuck in a loop between two options that are both not what you want.

更常见得多的情况是：它卡在两个选项之间来回循环，而这两个都不是你想要的。

So adding a QA agent, while it sounds logical, just ends up being even more of this.

所以加一个 QA 智能体，虽然听起来合逻辑，最终只是让这种情况变本加厉。

Rather than converging on a solution, they just get all out of whack.

它们不是向一个解收敛，而是彻底跑偏失调。

Until that is solved, far better just to have your dev agent be smart about doing its own QA.

在这个问题解决之前，远不如让你的开发智能体聪明地自己做 QA。

The only way I could see the QA agent idea working now is if it had the power to roll back the entire change, reset the dev agent, update the task with some hints of things not to overlook, and trigger the dev process from scratch.

眼下我能想到的 QA 智能体唯一可行的形态是：它有权回滚整个变更、重置开发智能体、往任务里补几条「别漏掉这些」的提示，然后从零重新触发开发流程。

But that seems pretty inefficient, and IDK if it would work any better.

但那看起来相当低效，而且我也不知道会不会更好用。

### 评论人 awayto｜别只告诉智能体「你只能编辑」：它知道自己拥有完整的 CRUD

> Run pwd to see the directory you're working in. You'll only be able to edit files in this directory.

> （引用原文提示词）运行 pwd 查看你所在的工作目录。你只能编辑这个目录里的文件。

If you're using the agent to produce any kind of code that has access to manipulate the filesystem, may as well have it understand its own abilities as having the entirety of CRUD, not just updates.

如果你让智能体生产任何有权操作文件系统的代码，那不如让它把自己的能力理解成完整的 CRUD（增删改查），而不只是「更新」。

I could easily see the agent talking itself into working around "only be able to edit" with its other knowledge that it can just write a script to do whatever it wants.

我完全能想象智能体说服自己绕过「只能编辑」这条限制——因为它同时也知道，自己可以写个脚本为所欲为。

This also reinforces to devs that they basically shouldn't trust the agent when it comes to the filesystem.

这也再次提醒开发者：在文件系统这件事上，基本不该信任智能体。

As for pwd for existing projects, I start each session running tree local to the part of the project filesystem I want to have worked on.

至于给已有项目用 pwd 这招，我的做法是每次会话开始时，在我想让它处理的那部分项目文件系统里跑一遍 tree。

### 评论人 adidoit｜最先进的办法竟是「措辞强硬的指令」：这是 LLM 的根本局限

Fascinating that the state-of-the-art in building agentic harnesses for long running agent workflows is to ... "use strong-worded instructions"

很有意思：构建长时程智能体工作流 harness 的最先进水平（state-of-the-art），居然是……「使用措辞强硬的指令」。

Anthropomorphism of LLMs is obviously flawed but remains the best way to actually build good Agents.

把 LLM 拟人化（anthropomorphism）显然有缺陷，但它仍然是真正构建出好智能体的最佳方式。

I do think this is one thing that will hold enterprise adoption back: can you really trust systems like these in production where the best control you can offer is that you're pleading with it to not do something?

我确实认为这会拖累企业级采用：当你能提供的最好控制手段是「恳求它别做某件事」时，你真的敢在生产环境信任这样的系统吗？

Of course good engineering will build deterministic verification and scaffolds into prevent issues but it is a fundamental limitation of LLMs

当然，好的工程会构建确定性验证和脚手架来预防问题，但这终究是 LLM 的一个根本性局限。

### 评论人 CurleighBraces｜提问：这些智能体配合 BDD 工具会怎样？

I wonder how good these agents would be using something like cucumber and behaviour driven development tools?

我很好奇，这些智能体用上 Cucumber 之类的行为驱动开发（BDD）工具会表现如何？

### 评论人 wild_egg｜回答：基本是专家级，效果很好

Basically experts at it, works great.

基本就是这方面的专家，效果很好。

### 评论人 dangoodmanUT｜注意到一个细节：模型更不容易乱改 JSON 文件

> … the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files.

> （引用原文）……相比 Markdown 文件，模型更不容易不恰当地修改或覆盖 JSON 文件。

Very interesting.

非常有意思。

### 评论人 johndhi｜根本性质疑：我们为什么需要长时程智能体？

Why do we need long running agents?

我们为什么需要长时程智能体？

Most of my experienced value with LLMs has been like 1 to 10 turn chats.

我从 LLM 获得的价值，绝大部分来自 1 到 10 轮的对话。

Should they just ban longer chats to solve these issues?

要不干脆禁掉更长的对话，这些问题不就解决了？

### 评论人 vidarh｜多周长跑的真实案例：人只需低频介入，价值才最大

Because you get the biggest time-savings when you can let it run longer between each time it needs a human in the loop.

因为只有当你能让它在两次需要人类介入（human in the loop）之间跑得更久时，才能获得最大的时间节省。

I have multi-*week* runs of Claude Code going to work on a compiler project.

我有跑了*数周*的 Claude Code 会话，在做一个编译器项目。

I have a week-long run of Claude Code where it is writing a real-time strategy game.

我还有一个跑了一周的 Claude Code 会话，在写一个即时战略游戏。

In both cases I occasionally review code, and complain a bit about things it has gotten wrong until it's back on track.

两个项目里，我都只是偶尔 review 代码，对它做错的地方抱怨几句，直到它回到正轨。

In both cases it is working to specs that have produced plans that have produced TODO lists.

两个项目里，它都是照着「规格 → 计划 → TODO 清单」这条链在干活。

In the latter it wrote the specs itself.

后一个项目的规格是它自己写的。

In the former, the specs are externally imposed (rubyspecs test suite).

前一个项目的规格是外部强加的（rubyspecs 测试套件）。

In both cases it means I get involved ranging from ever tens of minutes to every few hours, but mostly then to just confirm it can continue, with more detailed reviews every day or so.

两个项目里，我介入的频率从每几十分钟到每几小时不等，但大多数时候只是确认它可以继续，更细致的 review 大约每天一次。

Having to review output and give instructions every turn would drastically diminish the value.

如果每一轮都得 review 输出、下指令，价值就会大打折扣。

### 评论人 vidarh｜成本回答：顶级 Claude Max 订阅，刚升的级

*（回应 maxlamb 的追问「这种多周长跑每天大概花多少钱」：）*

I'm on the top Claude Max tier. Just upgraded.

我用的是最高档的 Claude Max，刚升级的。

I could probably make do with the lower one, but I hit the limit (for the first time) on the lower Claude Max this week, and I get enough value from it that I was not about to wait for a session reset.

低一档的其实大概也够用，但这周我（头一次）在低档 Claude Max 上撞到了额度上限，而它给我的价值足够多，我可不打算干等会话额度重置。

### 评论人 ford｜类比反讽：「为什么要把 Yahoo 搜索做快？我挺习惯等 2-3 秒的」

"Why are we trying to make Yahoo Search faster? I already am fine with my 2-3s wait time"

「我们为什么要把 Yahoo 搜索做得更快？我已经很习惯 2-3 秒的等待了呀。」

---

## 未收录评论概况

未收录 8 条：morkalork（一句追问「几百个智能体要多少人做多久」，语境已并入 roughly 的回复小节）、maxlamb（一句追问成本，语境已并入 vidarh 的回复小节）、tomwojcik / imron / _boffin_ 三条关于 plane.io 应为 plane.so 的链接勘误互动、slurrpurr 一句玩笑（"BDSM for LLMs"）、以及 2 条已删除/被折叠（dead）评论。
