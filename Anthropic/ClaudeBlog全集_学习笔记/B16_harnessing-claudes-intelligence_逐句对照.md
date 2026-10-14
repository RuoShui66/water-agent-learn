# B16_Agent Harness Design: 3 Patterns for Harnessing Claude's Intelligence_驾驭 Claude 智能的三种 Harness 设计模式

> 原文：https://claude.com/blog/harnessing-claudes-intelligence
> 来源：Claude 官方博客｜发布日期：2026-04-02｜作者：Lance Martin（Claude Platform team）

## 📌 本篇速览

- 📅 2026-04-02　｜　⏱ 约 8 分钟　｜　📄 约 1,100 词 / 6 图 / 2 代码块
- 🏷 Agent Harness、bash 工具、代码执行编排、Skills、Compaction、记忆文件夹、提示词缓存、专用工具
- 🗂 [返回目录](00_目录与阅读进度.md)

本文提出 agent harness 设计的核心矛盾：harness 中的每段脚手架代码都编码了「Claude 自己做不到某事」的假设，而随着模型变强这些假设会过期。文章给出三个模式：一是靠模型别靠 harness——用 Claude 深度理解的通用工具（bash + 文本编辑器）构建，Skills、编程式工具调用、记忆工具都是它们的组合；二是把 harness 拆薄——让 Claude 用代码执行自己编排工具调用（Opus 4.6 在 BrowseComp 上从 45.3% 提到 61.6%）、用 Skills 渐进披露与 context editing 管理自己的上下文、用 compaction 与记忆文件夹持久化自己的上下文（Opus 4.6 在 BrowseComp 上达 84%）；三是谨慎设边界——按缓存命中原则组织上下文，把需要安全、UX、可观测性钩子的动作提升为专用工具，并持续追问「我能停掉什么」。

---

> Agent harness design is deciding what scaffolding your agent needs—and what it doesn't. Three patterns from Anthropic for building harnesses that improve as Claude does.

> Agent harness 设计，就是决定你的智能体需要哪些脚手架——以及不需要哪些。本文是 Anthropic 给出的三个模式，用于构建能随 Claude 进步而一同变好的 harness。

One of Anthropic’s co-founders, Chris Olah, says that generative AI systems like Claude are grown more than they are built.

Anthropic 联合创始人之一 Chris Olah 说过：像 Claude 这样的生成式 AI 系统，与其说是被「构建」出来的，不如说是被「培育」出来的。

Researchers set the conditions to direct growth, but the exact structure or capabilities that emerge aren’t always predictable.

研究者可以设置条件来引导生长，但最终涌现出什么样的结构和能力，并不总是可以预测的。

This creates a challenge for building with Claude: agent harnesses encode assumptions about what Claude can’t do on its own, but those assumptions grow stale as Claude gets more capable.

这给基于 Claude 构建应用带来了一个难题：agent harness（智能体执行框架）编码了「Claude 自己做不到什么」的假设，而随着 Claude 能力增强，这些假设会逐渐过期变质。

An agent harness is the software scaffolding around a model: the loop, tools, context management, and guardrails that turn raw intelligence into a working agent.

Agent harness 是包裹在模型外面的软件脚手架：循环（loop）、工具、上下文管理和护栏（guardrails），它们共同把原始智能变成一个能干活的智能体。

Agent harness design is the practice of deciding what belongs in that scaffolding and, as models improve, what you can take out.

Agent harness 设计，就是决定什么该放进这套脚手架——以及随着模型进步，什么可以从中拿出来——的实践。

In this article, we share three patterns that teams should use when building applications that keep pace with Claude’s evolving intelligence while balancing latency and cost: use what it already knows, ask what you can stop doing, and carefully set boundaries with the agent harness.

在本文中，我们分享团队在构建应用时应当采用的三个模式，帮助应用跟上 Claude 不断演进的智能，同时兼顾延迟与成本：用它已经会的东西、追问你能停掉什么、以及在 agent harness 中谨慎地设置边界。

### 1. Lean on the model, not the harness: use what Claude knows｜一、靠模型，别靠 harness：用 Claude 已经懂的东西

We suggest building applications using tools that Claude understands well.

我们建议使用 Claude 理解得很透彻的工具来构建应用。

In late 2024, Claude 3.5 Sonnet reached 49% on SWE-bench Verified—then state of the art—with only a bash tool and a text editor tool for viewing, creating, and editing files.

2024 年末，Claude 3.5 Sonnet 仅凭一个 bash 工具和一个用于查看、创建、编辑文件的文本编辑器工具，就在 SWE-bench Verified 上拿到了 49%——这是当时的最先进水平（state of the art）。

Claude Code is grounded in these same tools.

Claude Code 也正是扎根在这两个工具之上。

Bash wasn’t designed for building agents, but it's a tool that Claude knows how to use and gets better at using over time.

Bash 当初并不是为构建智能体而设计的，但它是一个 Claude 会用、而且随时间推移越用越好的工具。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd8747994e07042a959518_image2.png)
*Scores on the SWE-bench Verified benchmark across Claude model versions highlight its evolution.*

*各代 Claude 模型在 SWE-bench Verified 基准上的分数，清晰展现了它的演进轨迹。*

We've seen Claude compose these general tools into patterns that solve different problems.

我们观察到，Claude 能把这些通用工具组合成解决不同问题的模式。

For instance, Agent Skills, programmatic tool calling, and the memory tool are all built from the bash and text editor tools.

例如，Agent Skills、编程式工具调用（programmatic tool calling）和记忆工具（memory tool），全都是由 bash 工具和文本编辑器工具搭建出来的。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd8835161641fba4aa1def_image4.png)
*Programmatic tool calling, skills, and memory are compositions of our bash and text editor tools.*

*编程式工具调用、Skills 和记忆，都是我们的 bash 与文本编辑器两个工具的组合。*

### 2. Strip your agent harness down: ask what you can stop doing｜二、把 harness 拆薄：追问你能停掉什么

Agent harnesses encode assumptions about what Claude can’t do on its own.

Agent harness 编码了关于「Claude 自己做不到什么」的假设。

As Claude gets more capable, those assumptions should be tested.

随着 Claude 能力增强，这些假设就应当被重新检验。

#### Let Claude orchestrate its own actions｜让 Claude 编排自己的行动

A common assumption is that every tool result should flow back through Claude’s context window to inform the next action.

一个常见的假设是：每个工具结果都应该流回 Claude 的上下文窗口，用来指导下一步行动。

Processing tool results in tokens can be slow, costly, and unnecessary if it only needs to be passed to the next tool or if Claude only cares about a small slice of the output.

用 token 来处理工具结果可能又慢又贵——而且如果结果只需要传给下一个工具，或者 Claude 只关心输出里的一小部分，这种处理根本没有必要。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd889c76e6e17dbe4ff4b9_image7.png)
*Claude calls tools, which are executed in an environment.*

*Claude 调用工具，工具在环境中被执行。*

Consider reading a large table to reason about a single column: the whole table lands in context and Claude pays the token cost for every row it doesn't need.

想象一下为了推理某一列而去读一整张大表：整张表落进上下文，Claude 要为每一行它并不需要的数据支付 token 成本。

It’s possible to tackle this in tool design, using hard-coded filters.

在工具设计层面用硬编码的过滤器，确实可以缓解这个问题。

But this does not address the fact that the agent harness is making an orchestration decision that Claude is better positioned to make.

但这没有解决本质问题：agent harness 正在替 Claude 做一个 Claude 自己更有资格做的编排（orchestration）决策。

Giving Claude a code execution tool (e.g., bash tool or language-specific REPL) addresses this: it allows Claude to write code to express tool calls and the logic between them.

给 Claude 一个代码执行工具（例如 bash 工具或特定语言的 REPL）就能解决这一点：它允许 Claude 写代码来表达工具调用以及调用之间的逻辑。

Rather than the harness deciding that every tool call result is processed as tokens, Claude decides what results to pass through, filter, or pipe into the next call without touching the context window.

不再由 harness 规定每个工具调用结果都要被当作 token 处理，而是由 Claude 自己决定哪些结果要透传、过滤，或者用管道接入下一次调用——全程不触碰上下文窗口。

Only the output of code execution reaches Claude’s context window.

只有代码执行的最终输出才会进入 Claude 的上下文窗口。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd891f5b4d2dea57b008d1_image6.png)
*Claude can write code that expresses tool calls and the logic between them.*

*Claude 可以写代码来表达工具调用以及调用之间的逻辑。*

The orchestration decision moves from the harness to the model.

编排决策由此从 harness 转移到了模型。

Since code is a general way for Claude to orchestrate actions, a strong coding model is also a strong general agent.

由于代码是 Claude 编排行动的一种通用方式，一个强大的编程模型同时也是一个强大的通用智能体。

Claude shows strong performance on non-coding evals using this pattern: on BrowseComp, a benchmark that tests the ability of agents to browse the web, giving Opus 4.6 the ability to filter its own tool outputs brought accuracy from 45.3% to 61.6%.

采用这一模式后，Claude 在非编程类评测上同样表现出色：在测试智能体网页浏览能力的基准 BrowseComp 上，让 Opus 4.6 拥有过滤自己工具输出的能力后，准确率从 45.3% 提升到了 61.6%。

#### Let Claude manage its own context｜让 Claude 管理自己的上下文

Task-specific context steers Claude’s use of general tools like bash and the text editor tool.

任务特定的上下文会引导 Claude 使用 bash、文本编辑器这类通用工具的方式。

A common assumption is that system prompts should be hand-crafted with task-specific instructions.

一个常见的假设是：系统提示词应该手工精心编写、塞满任务特定的指令。

The problem is that pre-loading prompts with instructions does not scale across many tasks: every token added depletes Claude’s attention budget and it is wasteful to pre-load context with rarely used instructions.

问题在于，把指令预载进提示词的做法无法扩展到大量任务：每多加一个 token 都在消耗 Claude 的注意力预算（attention budget），而把很少用到的指令预载进上下文纯属浪费。

Giving Claude the ability to access skills addresses this: the YAML frontmatter of each skill is a short description pre-loaded into the context window, providing an overview of the skill contents.

让 Claude 拥有访问 skills 的能力可以解决这个问题：每个 skill 的 YAML frontmatter 是一段预载进上下文窗口的简短描述，提供该 skill 内容的概览。

The full skill can be progressively disclosed by Claude calling a read file tool if a task calls for it.

如果任务需要，Claude 可以调用读文件工具，把完整的 skill 渐进披露（progressively disclose）进来。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd895f7f04456cccf7b7e0_image3.png)
*Claude can use skills to progressively disclose task-relevant context.*

*Claude 可以借助 skills 渐进披露与任务相关的上下文。*

While skills give Claude the freedom to assemble its own context window, context editing is the inverse, providing a way to selectively remove context that’s become stale or irrelevant, such as old tool results or thinking blocks.

Skills 给了 Claude 自由组装自己上下文窗口的能力，而上下文编辑（context editing）则是它的逆操作——提供一种选择性移除已经过期或不再相关的内容的方式，比如旧的工具结果或思考块。

With subagents, Claude is getting better at knowing when to fork into a fresh context window to isolate work on a specific task.

借助子智能体（subagents），Claude 越来越擅长判断何时该分叉出一个全新的上下文窗口，来隔离某个特定任务的工作。

With Opus 4.6, the ability to spawn subagents improved results on BrowseComp by 2.8% over the best single-agent runs.

在 Opus 4.6 上，生成子智能体的能力让 BrowseComp 成绩比最好的单智能体运行又提升了 2.8%。

#### Let Claude persist its own context｜让 Claude 持久化自己的上下文

Long-running agents can exceed the limit of a single context window.

长时间运行的智能体可能会超出单个上下文窗口的限制。

A common assumption is that memory systems should rely on retrieval infrastructure around the model.

一个常见的假设是：记忆系统应该依赖围绕模型搭建的检索基础设施。

Much of our work has focused on giving Claude simple ways to choose for itself what content to persist.

而我们的大量工作则聚焦于给 Claude 提供简单的机制，让它自己选择要持久化哪些内容。

For example, compaction lets Claude summarize its past context in order to maintain continuity on long-horizon tasks.

例如，压缩（compaction）让 Claude 总结自己过往的上下文，以便在长时程任务上保持连续性。

Over several releases, Claude has gotten better at choosing what to remember.

经过数个版本的迭代，Claude 在「选择记住什么」这件事上持续进步。

On BrowseComp, for example, an agentic search task, Sonnet 4.5 stayed flat at 43% regardless of the compaction budget we gave it.

以智能体搜索任务 BrowseComp 为例：无论我们给多大的压缩预算，Sonnet 4.5 都停在 43% 原地不动。

Yet Opus 4.5 scaled to 68% and Opus 4.6 reached 84% with the same setup.

然而在完全相同的设置下，Opus 4.5 扩展到了 68%，Opus 4.6 更是达到了 84%。

A memory folder is another approach, allowing Claude to write context to files and later read them as needed.

记忆文件夹（memory folder）是另一种方法：允许 Claude 把上下文写进文件，之后按需读取。

We’ve seen Claude use this for agentic search.

我们观察到 Claude 会在智能体搜索中使用这种方法。

On BrowseComp-Plus, giving Sonnet 4.5 a memory folder lifted accuracy from 60.4% to 67.2%.

在 BrowseComp-Plus 上，给 Sonnet 4.5 配备记忆文件夹后，准确率从 60.4% 提升到了 67.2%。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd89bfccdc7c50beb40e0d_image5.png)
*Claude can persist context to a memory folder.*

*Claude 可以把上下文持久化到记忆文件夹。*

Long-horizon games, such as Pokémon, are an example of Claude’s improved ability to use a memory folder.

宝可梦（Pokémon）这类长时程游戏，正是 Claude 使用记忆文件夹的能力不断提升的一个例证。

Sonnet 3.5 treated memory as a transcript, writing down what non-player characters (NPCs) said rather than what mattered.

Sonnet 3.5 把记忆当成了逐字记录，写下的是非玩家角色（NPC）说了什么，而不是真正重要的信息。

After 14,000 steps it had 31 files—including two near-duplicates about caterpillar Pokémon—and was still in the second town:

走了 14,000 步之后，它攒下了 31 个文件——其中包括两个关于毛毛虫宝可梦的近乎重复的文件——而人还停留在第二个城镇：

```
caterpie_weedle_info:
- Caterpie and Weedle are both caterpillar Pokémon.
- Caterpie is a caterpillar Pokémon that does not have poison.
- Weedle is a caterpillar Pokémon that does have poison.
- This information is crucial for future encounters and battles.
- If our Pokémon get poisoned, we should seek healing at a Pokémon
  Center as soon as possible.
```

Later models wrote tactical notes.

后来的模型写的则是战术笔记。

Opus 4.6, at the same step count, had 10 files organized into directories, three gym badges, and a learnings file distilled from its own failures:

在同样的步数下，Opus 4.6 只有 10 个按目录组织的文件、拿到了三枚道馆徽章，还有一个从自身失败中提炼出来的经验教训文件：

```
/gameplay/learnings.md:
- Bellsprout Sleep+Wrap combo: KO FAST with BITE before Sleep
  Powder lands. Don't let it set up!
- Gen 1 Bag Limit: 20 items max. Toss unneeded TMs before dungeons.
- Spin tile mazes: Different entry y-positions lead to DIFFERENT
  destinations. Try ALL entries and chain through multiple pockets.
- B1F y=16 wall CONFIRMED SOLID at ALL x=9-28 (step 14557)
```

### 3. Set boundaries carefully in your harness design｜三、在 harness 设计中谨慎设置边界

Agent harnesses provide structure around Claude to enforce UX, cost, or security.

Agent harness 在 Claude 周围提供结构，用来落实用户体验（UX）、成本或安全方面的要求。

#### Design context to maximize cache hits｜设计上下文以最大化缓存命中

The Messages API is stateless.

Messages API 是无状态的。

Claude cannot see the conversation history of prior turns.

Claude 看不到之前轮次的对话历史。

This means that the agent harness needs to package new context alongside all past actions, tool descriptions, and instructions for Claude at each turn.

这意味着 agent harness 需要在每一轮都把新上下文与过去所有的行动、工具描述和指令一起打包发给 Claude。

Prompts can be cached based on set breakpoints.

提示词可以基于设定的断点（breakpoint）进行缓存。

In other words, the Claude API writes context up until a breakpoint to the cache and checks whether the context matches any prior cache entries.

换句话说，Claude API 会把断点之前的上下文写入缓存，并检查该上下文是否与之前的某个缓存条目匹配。

Since cached tokens are 10% the cost of base input tokens, here are a few principles in the agent harness help maximize cache hits:

由于缓存 token 的价格只有基础输入 token 的 10%，以下是 agent harness 中有助于最大化缓存命中的几条原则：

| Principle | Description |
|---|---|
| Static first, dynamic last | Order requests so that stable content (system prompt, tools) come first. |
| Messages for updates | Append a <system-reminder> in messages instead of editing the prompt. |
| Don't change models | Avoid switching models during a session. Caches are model-specific; switching breaks them. If you need a cheaper model, use a subagent. |
| Carefully manage tools | Tools sit in the cached prefix. Adding or removing one invalidates it. For dynamic discovery, use tool search, which appends without breaking cache. |
| Update breakpoints | For multi-turn applications (e.g., agents), move the breakpoint to the latest message in order to keep the cache up-to-date. Use auto-caching for this. |

| 原则        | 说明                                                                    |
| --------- | --------------------------------------------------------------------- |
| 静态在前，动态在后 | 组织请求时让稳定内容（系统提示词、工具）排在前面。                                             |
| 用消息传递更新   | 在消息中追加 <system-reminder>，而不是修改提示词本身。                                  |
| 不要换模型     | 避免在会话中途切换模型。缓存是模型专属的，一换就失效。需要更便宜的模型时，用子智能体。                           |
| 谨慎管理工具    | 工具位于被缓存的前缀里，增删任何一个都会让缓存失效。需要动态发现时，用工具搜索（tool search），它以追加方式工作，不会破坏缓存。 |
| 更新断点      | 对于多轮应用（如智能体），把断点移到最新一条消息上，让缓存保持最新。可以用自动缓存（auto-caching）来做这件事。         |

#### Use declarative tools for UX, observability, or security boundaries｜用声明式工具划定 UX、可观测性或安全边界

Claude doesn't necessarily know an application's security boundary or UX surface.

Claude 不一定了解一个应用的安全边界或 UX 界面在哪里。

Claude emits tool calls, which are handled by the harness.

Claude 发出工具调用，由 harness 来处理。

A bash tool gives Claude broad programmatic leverage to perform actions, but it gives the harness only a command string—the same shape for every action.

bash 工具给了 Claude 执行各种行动的强大编程能力，但它交给 harness 的只是一个命令字符串——所有行动都长一个样。

Promoting actions to dedicated tools gives the harness an action-specific hook with typed arguments it can intercept, gate, render, or audit.

把行动提升为专用工具后，harness 就获得了一个针对特定行动的钩子，带有类型化参数，可以拦截、把关、渲染或审计。

Actions that require a security boundary are natural candidates for dedicated tools.

需要安全边界的行动，天然适合做成专用工具。

Reversibility is often a good criterion, and hard-to-reverse actions such as external API calls can be gated by user confirmation.

可逆性（reversibility）通常是一个不错的判断标准：像外部 API 调用这样难以撤销的行动，可以设置为需要用户确认才放行。

Write tools like edit can include a staleness check so Claude doesn't overwrite a file that changed since it was last read.

edit 这类写入工具可以内置过期检查（staleness check），防止 Claude 覆盖掉一个在上次读取之后已经被修改过的文件。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd8ebecb4a73207c8b2ffc_image1.png)
*Dedicated tools can be used for actions based upon security, UX, or observability considerations.*

*基于安全、UX 或可观测性方面的考虑，可以把相应行动做成专用工具。*

Tools are also useful when an action needs to be presented to a user.

当某个行动需要呈现给用户时，工具同样很有用。

For example, they can be rendered as a modal to display a question clearly to the user, give the user multiple options, or block the agent loop until a user provides feedback.

例如，工具可以被渲染成一个模态框（modal），向用户清晰地展示一个问题、提供多个选项，或者阻塞智能体循环直到用户给出反馈。

Finally, tools are useful for observability.

最后，工具对可观测性（observability）也很有用。

When the action is a typed tool, the harness gets structured arguments it can log, trace, and replay.

当行动是一个类型化的工具时，harness 拿到的是结构化参数，可以记录日志、追踪和回放。

The decision to promote actions to tools should be continually re-evaluated.

「是否把行动提升为工具」这个决定应当被持续地重新评估。

For example, Claude Code's auto-mode (in research mode at the time of publication) provides a security boundary around the bash tool: it has a second Claude read the command string and judge whether it's safe.

例如，Claude Code 的 auto-mode（本文发布时尚处于研究模式）为 bash 工具提供了一道安全边界：它让第二个 Claude 阅读命令字符串并判断其是否安全。

This pattern can limit the need for dedicated tools, and should only be used for tasks where users trust the general direction.

这种模式可以减少对专用工具的需求，但只应当用于用户信任整体方向的任务。

Dedicated tools can still earn their place for certain high-stakes actions.

对于某些高风险行动，专用工具依然有其不可替代的价值。

### The future of agent harness design｜Agent harness 设计的未来

The frontier of Claude’s intelligence is always changing.

Claude 智能的边界一直在变化。

Assumptions about what Claude can’t do need to be re-tested with each step change in its capability.

关于「Claude 做不到什么」的假设，需要在它的能力每出现一次跃变时都重新检验。

We see this pattern repeat itself.

我们看到这个规律在反复上演。

In an agent we built for long-horizon tasks, Sonnet 4.5 would wrap up prematurely as it sensed the context limit approaching.

在我们为长时程任务构建的一个智能体中，Sonnet 4.5 一旦感觉到上下文即将触顶，就会提前草草收尾。

We added resets to clear the context window in order to address this "context anxiety."

为了解决这种「上下文焦虑」（context anxiety），我们加入了清空上下文窗口的重置机制。

With Opus 4.5, the behavior was gone.

到了 Opus 4.5，这个行为消失了。

The context resets we built to compensate had become dead weight in the agent harness.

我们当初为补偿而构建的上下文重置机制，在 agent harness 里变成了累赘（dead weight）。

Removing this dead weight is important because it can bottleneck Claude’s performance.

清除这些累赘很重要，因为它们会成为 Claude 性能的瓶颈。

Over time, the structure or boundaries in our applications should be pruned based the question: what can I stop doing?

随着时间推移，我们应用中的结构和边界应当基于这个问题不断修剪：我能停掉什么？

To use all tools and patterns discussed here, check out our claude-api skill.

要使用本文讨论的全部工具和模式，请查看我们的 claude-api skill。

### Acknowledgements｜致谢

Written by Lance Martin, member of technical staff on the Claude Platform team.

本文由 Claude Platform 团队技术成员 Lance Martin 撰写。

Special thanks to Thariq Shihipar, Barry Zhang, Mike Lambert, David Hershey, and Daliang Li for helpful discussion on the topics covered.

特别感谢 Thariq Shihipar、Barry Zhang、Mike Lambert、David Hershey 和 Daliang Li 就本文主题进行的有益讨论。

Thanks to Lydia Hallie, Lexi Ross, Katelyn Lesse, Andy Schumeister, Rebecca Hiscott, Jake Eaton, Pedram Navid, and Molly Vorwerck for their editorial review and feedback.

感谢 Lydia Hallie、Lexi Ross、Katelyn Lesse、Andy Schumeister、Rebecca Hiscott、Jake Eaton、Pedram Navid 和 Molly Vorwerck 的编辑审校与反馈。


---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| agent harness | 智能体执行框架 | 模型外的软件脚手架：循环、工具、上下文管理、护栏 |
| agent harness design | harness 设计 | 决定什么放进脚手架、什么该拿出来的实践 |
| grown more than built | 长出来的多于造出来的 | Chris Olah 对生成式 AI 系统的描述 |
| programmatic tool calling | 编程式工具调用 | 用代码表达工具调用及其间逻辑 |
| progressive disclosure | 渐进披露 | Skills 的核心机制：概览常驻，正文按需读取 |
| attention budget | 注意力预算 | 每个预载 token 都在消耗它 |
| context editing | 上下文编辑 | 选择性移除过期/不相关内容（旧工具结果、思考块） |
| subagent | 子智能体 | 分叉出全新上下文窗口以隔离任务 |
| compaction | 压缩 | Claude 总结历史上下文以保持长时程连续性 |
| memory folder | 记忆文件夹 | Claude 自主写文件、按需读回的持久化机制 |
| cache breakpoint | 缓存断点 | 提示词缓存的分界位置；缓存 token 成本为基础的 10% |
| tool search | 工具搜索 | 以追加方式做工具动态发现，不打断缓存 |
| auto-caching | 自动缓存 | 自动把断点维持在最新消息 |
| dedicated / declarative tool | 专用/声明式工具 | 带类型化参数、可拦截把关渲染审计的动作专属钩子 |
| staleness check | 陈旧性检查 | 写操作前确认文件未被改动 |
| reversibility | 可逆性 | 判断动作是否需要专用工具把关的常用判据 |
| context anxiety | 上下文焦虑 | 模型感知上下文上限临近而提前收尾的行为 |
| dead weight | 死重 | 模型变强后失去存在理由、反而瓶颈性能的 harness 补丁 |


---

## ⚠️ 对学习笔记的勘误

> 勘误提示：学习笔记中「BrowseComp 84% vs 43%」一组对比，按原文属于 **2C compaction**（Sonnet 4.5 平在 43%，Opus 4.5 达 68%，Opus 4.6 达 84%），而非 2B；且原文还有两组学习笔记未收录的数字：subagents 在 Opus 4.6 上比最佳单智能体 **+2.8%**（BrowseComp），记忆文件夹让 Sonnet 4.5 在 BrowseComp-Plus 上 **60.4% → 67.2%**。
