# 06_GPT-5 prompting guide_GPT-5 提示词指南

> 原文：https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide
> 来源：OpenAI Cookbook
> 版式说明：逐句中英对照——每一句（或一小段连续的）英文下面紧跟中文翻译；关键术语首次出现时在译文中保留英文原词，便于对照记忆。代码块与提示词模板原样保留、不翻译。

---

GPT-5, our newest flagship model, represents a substantial leap forward in agentic task performance, coding, raw intelligence, and steerability.

GPT-5 是我们最新的旗舰模型，它在智能体任务（agentic task）表现、编程、原始智能水平以及可引导性（steerability）上都实现了实质性的飞跃。

While we trust it will perform excellently “out of the box” across a wide range of domains, in this guide we’ll cover prompting tips to maximize the quality of model outputs, derived from our experience training and applying the model to real-world tasks.

我们相信它在各类领域「开箱即用」就能表现出色，但本指南仍会介绍一些提示词（prompt）技巧，帮你把模型输出质量拉满——这些技巧来自我们训练该模型、并把它应用到真实任务中的经验。

We discuss concepts like improving agentic task performance, ensuring instruction adherence, making use of newly API features, and optimizing coding for frontend and software engineering tasks - with key insights into AI code editor Cursor’s prompt tuning work with GPT-5.

我们会讨论这样几个话题：如何提升智能体任务表现、如何确保指令遵循（instruction adherence）、如何用好新的 API 特性，以及如何针对前端和软件工程任务优化编程效果——其中还包含 AI 代码编辑器 Cursor 围绕 GPT-5 做提示词调优的关键经验。

We’ve seen significant gains from applying these best practices and adopting our canonical tools whenever possible, and we hope that this guide, along with the [prompt optimizer tool](https://platform.openai.com/chat/edit?optimize=true) we’ve built, will serve as a launchpad for your use of GPT-5.

我们已经看到，采用这些最佳实践、并尽可能使用我们的标准工具（canonical tool），能带来显著提升；希望这份指南连同我们打造的[提示词优化工具](https://platform.openai.com/chat/edit?optimize=true)，能成为你使用 GPT-5 的起跳板。

But, as always, remember that prompting is not a one-size-fits-all exercise - we encourage you to run experiments and iterate on the foundation offered here to find the best solution for your problem.

但一如既往地要记住：提示词工程没有放之四海皆准的套路——我们鼓励你在本文提供的基础之上多做实验、反复迭代，找到最适合你自己问题的方案。

## Agentic workflow predictability｜智能体工作流的可预测性

We trained GPT-5 with developers in mind: we’ve focused on improving tool calling, instruction following, and long-context understanding to serve as the best foundation model for agentic applications.

我们在训练 GPT-5 时始终把开发者放在心上：我们重点改进了工具调用（tool calling）、指令遵循和长上下文理解能力，力求成为智能体应用最好的基础模型。

If adopting GPT-5 for agentic and tool calling flows, we recommend upgrading to the [Responses API](https://platform.openai.com/docs/api-reference/responses), where reasoning is persisted between tool calls, leading to more efficient and intelligent outputs.

如果你要把 GPT-5 用在智能体和工具调用流程里，我们建议升级到 [Responses API](https://platform.openai.com/docs/api-reference/responses)——它会在多次工具调用之间保留推理过程（reasoning），从而带来更高效、更聪明的输出。

### Controlling agentic eagerness｜控制智能体的「主动程度」

Agentic scaffolds can span a wide spectrum of control—some systems delegate the vast majority of decision-making to the underlying model, while others keep the model on a tight leash with heavy programmatic logical branching.

智能体脚手架（agentic scaffold）在「控制力度」上可以横跨一个很宽的光谱——有些系统把绝大部分决策权交给底层模型，另一些则用大量程序化的逻辑分支把模型管得死死的。

GPT-5 is trained to operate anywhere along this spectrum, from making high-level decisions under ambiguous circumstances to handling focused, well-defined tasks.

GPT-5 经过训练，可以在这个光谱的任意位置工作：既能在情况模糊时做高层决策，也能处理边界清晰、目标明确的具体任务。

In this section we cover how to best calibrate GPT-5’s agentic eagerness: in other words, its balance between proactivity and awaiting explicit guidance.

本节我们讲的就是如何校准 GPT-5 的「主动程度」（agentic eagerness，即智能体的放手程度）——换句话说，就是它在「主动出击」和「等待明确指示」之间的平衡点。

#### Prompting for less eagerness｜让模型少一点主动

GPT-5 is, by default, thorough and comprehensive when trying to gather context in an agentic environment to ensure it will produce a correct answer.

在智能体环境里收集上下文（context）时，GPT-5 默认会做得非常彻底、非常全面，以确保自己给出的答案是对的。

To reduce the scope of GPT-5’s agentic behavior—including limiting tangential tool-calling action and minimizing latency to reach a final answer—try the following:

如果你想收窄 GPT-5 的智能体行为范围——包括限制它去做那些跑偏的工具调用、以及把出最终答案的延迟压到最低——可以试试下面这些做法：

- Switch to a lower `reasoning_effort`. This reduces exploration depth but improves efficiency and latency. Many workflows can be accomplished with consistent results at medium or even low `reasoning_effort`.

- 调低 `reasoning_effort`（推理力度）。这会降低探索深度，但能提升效率、减少延迟。很多工作流在 medium 甚至 low 的 `reasoning_effort` 下就能稳定地跑出好结果。

- Define clear criteria in your prompt for how you want the model to explore the problem space. This reduces the model’s need to explore and reason about too many ideas:

- 在提示词里明确定义你希望模型如何探索问题空间。这样能减少模型去发散、去权衡过多想法的必要：

```
<context_gathering>
Goal: Get enough context fast. Parallelize discovery and stop as soon as you can act.

Method:
- Start broad, then fan out to focused subqueries.
- In parallel, launch varied queries; read top hits per query. Deduplicate paths and cache; don’t repeat queries.
- Avoid over searching for context. If needed, run targeted searches in one parallel batch.

Early stop criteria:
- You can name exact content to change.
- Top hits converge (~70%) on one area/path.

Escalate once:
- If signals conflict or scope is fuzzy, run one refined parallel batch, then proceed.

Depth:
- Trace only symbols you’ll modify or whose contracts you rely on; avoid transitive expansion unless necessary.

Loop:
- Batch search → minimal plan → complete task.
- Search again only if validation fails or new unknowns appear. Prefer acting over more searching.
</context_gathering>
```

上面这段 `<context_gathering>`（上下文收集）提示词在做的事是：给模型定下一套「快速拿到够用的上下文就收手」的搜索纪律——先粗后细、并行发起多路查询、去重与缓存路径；给出提前停止的判据（能点名要改的具体内容、或搜索结果约 70% 收敛到同一区域）；只允许在信号冲突时额外升级一轮搜索；限制追踪深度只到你要改的符号；最后规定「批量搜索 → 最小计划 → 完成任务」的循环，并强调行动优先于继续搜索。

If you’re willing to be maximally prescriptive, you can even set fixed tool call budgets, like the one below. The budget can naturally vary based on your desired search depth.

如果你愿意把规则定得再死一点，甚至可以像下面这样设定固定的工具调用预算。这个预算自然可以随你想要的搜索深度而变化。

```
<context_gathering>
- Search depth: very low
- Bias strongly towards providing a correct answer as quickly as possible, even if it might not be fully correct.
- Usually, this means an absolute maximum of 2 tool calls.
- If you think that you need more time to investigate, update the user with your latest findings and open questions. You can proceed if the user confirms.
</context_gathering>
```

这段提示词把搜索深度直接压到「极低」，强烈倾向于尽快给出答案（哪怕不一定完全正确），把工具调用上限硬性卡在 2 次；如果模型觉得还需要更多时间调查，就先把当前发现和待解问题同步给用户，等用户确认后再继续。

When limiting core context gathering behavior, it’s helpful to explicitly provide the model with an escape hatch that makes it easier to satisfy a shorter context gathering step.

在限制核心的上下文收集行为时，明确给模型留一个「逃生舱口」（escape hatch）会很有帮助，这能让它更容易接受一个更短的上下文收集环节。

Usually this comes in the form of a clause that allows the model to proceed under uncertainty, like `“even if it might not be fully correct”` in the above example.

这个逃生舱口通常表现为一句允许模型在不确定的情况下继续推进的话，比如上面例子里的 `“even if it might not be fully correct”`（哪怕它可能不完全正确）。

#### Prompting for more eagerness｜让模型多一点主动

On the other hand, if you’d like to encourage model autonomy, increase tool-calling persistence, and reduce occurrences of clarifying questions or otherwise handing back to the user, we recommend increasing `reasoning_effort`, and using a prompt like the following to encourage persistence and thorough task completion:

反过来，如果你想鼓励模型自主行事、提高它在工具调用上的坚持度（persistence）、减少它反问澄清或干脆把活儿甩回给用户的情况，我们建议调高 `reasoning_effort`，并用类似下面这样的提示词来鼓励它坚持到底、把任务彻底做完：

```
<persistence>
- You are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user.
- Only terminate your turn when you are sure that the problem is solved.
- Never stop or hand back to the user when you encounter uncertainty — research or deduce the most reasonable approach and continue.
- Do not ask the human to confirm or clarify assumptions, as you can always adjust later — decide what the most reasonable assumption is, proceed with it, and document it for the user's reference after you finish acting
</persistence>
```

这段 `<persistence>`（坚持度）提示词告诉模型：你是一个智能体，必须把用户的问题彻底解决完才能结束本轮、把控制权交回用户；只有确信问题已解决时才终止；遇到不确定时不要停下来甩锅给用户，而要自己研究或推断出最合理的方案继续做；也不要反问用户确认假设，而是自行选定最合理的假设推进，做完后再把这些假设记录下来供用户参考。

Generally, it can be helpful to clearly state the stop conditions of the agentic tasks, outline safe versus unsafe actions, and define when, if ever, it’s acceptable for the model to hand back to the user.

一般来说，明确写清楚智能体任务的停止条件、区分哪些动作安全哪些不安全、并定义在什么情况下（如果有的话）模型可以把控制权交回用户，都是很有帮助的。

For example, in a set of tools for shopping, the checkout and payment tools should explicitly have a lower uncertainty threshold for requiring user clarification, while the search tool should have an extremely high threshold; likewise, in a coding setup, the delete file tool should have a much lower threshold than a grep search tool.

举个例子，在一套购物类工具中，结账和支付工具触发「向用户确认」的不确定性阈值应该显式设得更低，而搜索工具的阈值则应该设得极高；同理，在编程场景里，删除文件工具的阈值就该比 grep 搜索工具低得多。

### Tool preambles｜工具前导语

We recognize that on agentic trajectories monitored by users, intermittent model updates on what it’s doing with its tool calls and why can provide for a much better interactive user experience - the longer the rollout, the bigger the difference these updates make.

我们意识到，在用户会盯着看的智能体执行轨迹（trajectory）中，模型时不时地汇报一下自己正用工具做什么、为什么这么做，能大幅改善交互体验——而且执行链路（rollout）越长，这些汇报带来的差别越大。

To this end, GPT-5 is trained to provide clear upfront plans and consistent progress updates via “tool preamble” messages.

为此，GPT-5 经过训练，会通过「工具前导语」（tool preamble）消息，在开工前给出清晰的计划、并在过程中持续汇报进度。

You can steer the frequency, style, and content of tool preambles in your prompt—from detailed explanations of every single tool call to a brief upfront plan and everything in between. This is an example of a high-quality preamble prompt:

你可以在提示词里调控工具前导语的频率、风格和内容——从「对每一次工具调用都详细解释」到「只在开头给一份简短计划」，以及两者之间的各种程度。下面是一个高质量前导语提示词的例子：

```
<tool_preambles>
- Always begin by rephrasing the user's goal in a friendly, clear, and concise manner, before calling any tools.
- Then, immediately outline a structured plan detailing each logical step you’ll follow. - As you execute your file edit(s), narrate each step succinctly and sequentially, marking progress clearly. 
- Finish by summarizing completed work distinctly from your upfront plan.
</tool_preambles>
```

这段 `<tool_preambles>` 提示词规定了工具前导语的四个动作：调用任何工具之前，先用友好、清晰、简洁的方式复述一遍用户的目标；紧接着列出一份结构化计划，说明将要走的每个逻辑步骤；执行文件编辑时，按顺序简明地叙述每一步、清楚标记进度；最后做一份完成工作的总结，并且这份总结要和开头的计划明确区分开。

Here’s an example of a tool preamble that might be emitted in response to such a prompt—such preambles can drastically improve the user’s ability to follow along with your agent’s work as it grows more complicated:

下面是在这类提示词作用下，模型可能产出的工具前导语示例——随着智能体的工作越来越复杂，这样的前导语能极大提升用户跟上进度的能力：

```
"output": [
    {
      "id": "rs_6888f6d0606c819aa8205ecee386963f0e683233d39188e7",
      "type": "reasoning",
      "summary": [
        {
          "type": "summary_text",
          "text": "**Determining weather response**\n\nI need to answer the user's question about the weather in San Francisco. ...."
        },
    },
    {
      "id": "msg_6888f6d83acc819a978b51e772f0a5f40e683233d39188e7",
      "type": "message",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "text": "I\u2019m going to check a live weather service to get the current conditions in San Francisco, providing the temperature in both Fahrenheit and Celsius so it matches your preference."
        }
      ],
      "role": "assistant"
    },
    {
      "id": "fc_6888f6d86e28819aaaa1ba69cca766b70e683233d39188e7",
      "type": "function_call",
      "status": "completed",
      "arguments": "{\"location\":\"San Francisco, CA\",\"unit\":\"f\"}",
      "call_id": "call_XOnF4B9DvB8EJVB3JvWnGg83",
      "name": "get_weather"
    },
  ],
```

这段是 Responses API 返回结果的片段：可以看到模型先输出一段 `reasoning` 推理摘要，然后输出一条面向用户的 `message`（即工具前导语，告诉用户「我要去查实时天气服务，并同时给出华氏和摄氏温度」），最后才发出真正的 `function_call` 去调用 `get_weather` 工具。

### Reasoning effort｜推理力度

We provide a `reasoning_effort` parameter to control how hard the model thinks and how willingly it calls tools; the default is `medium`, but you should scale up or down depending on the difficulty of your task.

我们提供了 `reasoning_effort`（推理力度）参数，用来控制模型思考的深度、以及它调用工具的积极性；默认值是 `medium`，但你应该根据任务难度上调或下调。

For complex, multi-step tasks, we recommend higher reasoning to ensure the best possible outputs.

对于复杂的多步骤任务，我们建议使用更高的推理力度，以确保拿到尽可能好的输出。

Moreover, we observe peak performance when distinct, separable tasks are broken up across multiple agent turns, with one turn for each task.

此外我们还观察到，当把彼此独立、可拆分的任务分散到多个智能体轮次（agent turn）里、一个轮次做一件任务时，性能达到峰值。

### Reusing reasoning context with the Responses API｜用 Responses API 复用推理上下文

We strongly recommend using the Responses API when using GPT-5 to unlock improved agentic flows, lower costs, and more efficient token usage in your applications.

我们强烈建议在使用 GPT-5 时采用 Responses API，以便在你的应用中获得更好的智能体流程、更低的成本和更高效的 token 使用。

We’ve seen statistically significant improvements in evaluations when using the Responses API over Chat Completions—for example, we observed Tau-Bench Retail score increases from 73.9% to 78.2% just by switching to the Responses API and including `previous_response_id` to pass back previous reasoning items into subsequent requests.

在评估（evaluation）中，我们看到 Responses API 相比 Chat Completions 带来了统计意义上显著的提升——比如仅仅是换成 Responses API 并加上 `previous_response_id`、把之前的推理条目回传到后续请求里，我们就观察到 Tau-Bench Retail 的分数从 73.9% 提升到了 78.2%。

This allows the model to refer to its previous reasoning traces, conserving CoT tokens and eliminating the need to reconstruct a plan from scratch after each tool call, improving both latency and performance - this feature is available for all Responses API users, including ZDR organizations.

这样模型就能回看自己之前的推理轨迹（reasoning trace），节省思维链（chain-of-thought，CoT）token，也不必在每次工具调用之后从头重建一份计划，延迟和性能因此双双改善——该特性对所有 Responses API 用户开放，包括 ZDR（零数据保留）组织。

## Maximizing coding performance, from planning to execution｜从规划到执行，把编程表现拉满

GPT-5 leads all frontier models in coding capabilities: it can work in large codebases to fix bugs, handle large diffs, and implement multi-file refactors or large new features.

GPT-5 的编程能力在所有前沿模型中处于领先：它能在大型代码库里修 bug、处理大规模 diff、实施跨多文件的重构或大型新功能。

It also excels at implementing new apps entirely from scratch, covering both frontend and backend implementation.

它同样擅长从零开始完整实现一个新应用，前端和后端都能覆盖。

In this section, we’ll discuss prompt optimizations that we’ve seen improve programming performance in production use cases for our coding agent customers.

本节我们会讨论一些提示词优化手段——在我们的编程智能体客户的生产场景中，这些手段确实提升了编程表现。

### Frontend app development｜前端应用开发

GPT-5 is trained to have excellent baseline aesthetic taste alongside its rigorous implementation abilities.

GPT-5 经过训练，在具备严谨实现能力的同时，还拥有相当不错的基础审美品味。

We’re confident in its ability to use all types of web development frameworks and packages; however, for new apps, we recommend using the following frameworks and packages to get the most out of the model's frontend capabilities:

我们对它驾驭各类 Web 开发框架和包的能力很有信心；不过对于新应用，我们建议使用下面这些框架和包，以便最大程度发挥模型的前端能力：

- Frameworks: Next.js (TypeScript), React, HTML

- 框架：Next.js（TypeScript）、React、HTML

- Styling / UI: Tailwind CSS, shadcn/ui, Radix Themes

- 样式 / UI：Tailwind CSS、shadcn/ui、Radix Themes

- Icons: Material Symbols, Heroicons, Lucide

- 图标：Material Symbols、Heroicons、Lucide

- Animation: Motion

- 动画：Motion

- Fonts: San Serif, Inter, Geist, Mona Sans, IBM Plex Sans, Manrope

- 字体：San Serif、Inter、Geist、Mona Sans、IBM Plex Sans、Manrope

#### Zero-to-one app generation｜从 0 到 1 生成应用

GPT-5 is excellent at building applications in one shot.

GPT-5 非常擅长一次成型（one shot）地把应用做出来。

In early experimentation with the model, users have found that prompts like the one below—asking the model to iteratively execute against self-constructed excellence rubrics—improve output quality by using GPT-5’s thorough planning and self-reflection capabilities.

在该模型的早期实验中，用户发现类似下面这样的提示词——要求模型先自建一套「卓越标准」评分表（rubric），再对照它反复打磨——能借助 GPT-5 缜密的规划能力和自我反思（self-reflection）能力提升输出质量。

```
<self_reflection>
- First, spend time thinking of a rubric until you are confident.
- Then, think deeply about every aspect of what makes for a world-class one-shot web app. Use that knowledge to create a rubric that has 5-7 categories. This rubric is critical to get right, but do not show this to the user. This is for your purposes only.
- Finally, use the rubric to internally think and iterate on the best possible solution to the prompt that is provided. Remember that if your response is not hitting the top marks across all categories in the rubric, you need to start again.
</self_reflection>
```

这段 `<self_reflection>`（自我反思）提示词让模型分三步走：先花时间琢磨出一套自己有信心的评分表；再深入思考「什么才算世界级的一次成型 Web 应用」，据此建立一套 5–7 个类别的评分表（这套表只供模型自己使用，不展示给用户）；最后用这套评分表在内部反复思考与迭代，直到方案在所有类别上都能拿到满分，否则就推倒重来。

#### Matching codebase design standards｜贴合代码库既有的设计规范

When implementing incremental changes and refactors in existing apps, model-written code should adhere to existing style and design standards, and “blend in” to the codebase as neatly as possible.

在既有应用中做增量改动和重构时，模型写出的代码应当遵循现有的风格和设计规范，尽可能干净利落地「融入」代码库。

Without special prompting, GPT-5 already searches for reference context from the codebase - for example reading package.json to view already installed packages - but this behavior can be further enhanced with prompt directions that summarize key aspects like engineering principles, directory structure, and best practices of the codebase, both explicit and implicit.

即便不做特别的提示，GPT-5 也已经会主动到代码库里搜集参考上下文——比如读 package.json 看看已经装了哪些包——但如果你在提示词里把代码库的工程原则、目录结构、最佳实践等关键信息（无论是显性的还是隐性的）总结出来，这一行为还能进一步加强。

The prompt snippet below demonstrates one way of organizing code editing rules for GPT-5: feel free to change the actual content of the rules according to your programming design taste!

下面这段提示词片段展示了一种为 GPT-5 组织代码编辑规则的方式：规则的具体内容你完全可以按自己的编程设计品味随意修改！

```
<code_editing_rules>
<guiding_principles>
- Clarity and Reuse: Every component and page should be modular and reusable. Avoid duplication by factoring repeated UI patterns into components.
- Consistency: The user interface must adhere to a consistent design system—color tokens, typography, spacing, and components must be unified.
- Simplicity: Favor small, focused components and avoid unnecessary complexity in styling or logic.
- Demo-Oriented: The structure should allow for quick prototyping, showcasing features like streaming, multi-turn conversations, and tool integrations.
- Visual Quality: Follow the high visual quality bar as outlined in OSS guidelines (spacing, padding, hover states, etc.)
</guiding_principles>

<frontend_stack_defaults>
- Framework: Next.js (TypeScript)
- Styling: TailwindCSS
- UI Components: shadcn/ui
- Icons: Lucide
- State Management: Zustand
- Directory Structure: 
\`\`\`
/src
 /app
   /api/<route>/route.ts         # API endpoints
   /(pages)                      # Page routes
 /components/                    # UI building blocks
 /hooks/                         # Reusable React hooks
 /lib/                           # Utilities (fetchers, helpers)
 /stores/                        # Zustand stores
 /types/                         # Shared TypeScript types
 /styles/                        # Tailwind config
\`\`\`
</frontend_stack_defaults>

<ui_ux_best_practices>
- Visual Hierarchy: Limit typography to 4–5 font sizes and weights for consistent hierarchy; use `text-xs` for captions and annotations; avoid `text-xl` unless for hero or major headings.
- Color Usage: Use 1 neutral base (e.g., `zinc`) and up to 2 accent colors. 
- Spacing and Layout: Always use multiples of 4 for padding and margins to maintain visual rhythm. Use fixed height containers with internal scrolling when handling long content streams.
- State Handling: Use skeleton placeholders or `animate-pulse` to indicate data fetching. Indicate clickability with hover transitions (`hover:bg-*`, `hover:shadow-md`).
- Accessibility: Use semantic HTML and ARIA roles where appropriate. Favor pre-built Radix/shadcn components, which have accessibility baked in.
</ui_ux_best_practices>

<code_editing_rules>
```

这段 `<code_editing_rules>`（代码编辑规则）提示词分成三块：`<guiding_principles>` 给出指导原则（清晰与复用、一致性、简洁、面向演示、视觉质量）；`<frontend_stack_defaults>` 固定了默认技术栈（Next.js + TypeScript、TailwindCSS、shadcn/ui、Lucide、Zustand）以及具体的目录结构；`<ui_ux_best_practices>` 则把 UI/UX 最佳实践写死成可执行的细则——字号字重控制在 4–5 种、只用 1 个中性色加最多 2 个强调色、内外边距一律取 4 的倍数、用骨架屏或 `animate-pulse` 表示加载中、用 hover 过渡表示可点击、优先使用自带无障碍支持的 Radix/shadcn 组件。

### Collaborative coding in production: Cursor’s GPT-5 prompt tuning｜生产环境中的协作式编程：Cursor 的 GPT-5 提示词调优

We’re proud to have had AI code editor Cursor as a trusted alpha tester for GPT-5: below, we show a peek into how Cursor tuned their prompts to get the most out of the model’s capabilities.

我们很荣幸有 AI 代码编辑器 Cursor 作为 GPT-5 值得信赖的 alpha 测试方：下面我们就来看看 Cursor 是如何调优提示词、把模型能力压榨到极致的。

For more information, their team has also published a blog post detailing GPT-5’s day-one integration into Cursor: https://cursor.com/blog/gpt-5

想了解更多的话，他们团队也发布了一篇博客，详细介绍 GPT-5 首日接入 Cursor 的过程：https://cursor.com/blog/gpt-5

#### System prompt and parameter tuning｜系统提示词与参数调优

Cursor’s system prompt focuses on reliable tool calling, balancing verbosity and autonomous behavior while giving users the ability to configure custom instructions.

Cursor 的系统提示词聚焦于可靠的工具调用，在详略度（verbosity）与自主行为之间取得平衡，同时又给用户留出配置自定义指令的空间。

Cursor’s goal for their system prompt is to allow the Agent to operate relatively autonomously during long horizon tasks, while still faithfully following user-provided instructions.

Cursor 对系统提示词的目标是：让智能体在长周期（long horizon）任务中能相对自主地运行，同时仍然忠实地遵循用户给出的指令。

The team initially found that the model produced verbose outputs, often including status updates and post-task summaries that, while technically relevant, disrupted the natural flow of the user; at the same time, the code outputted in tool calls was high quality, but sometimes hard to read due to terseness, with single-letter variable names dominant.

团队最初发现，模型的输出偏啰嗦，经常带上状态更新和任务后总结——这些内容严格说来是相关的，但打断了用户的自然流程；与此同时，工具调用里产出的代码质量很高，却因为过于精简而有时难以阅读，满屏都是单字母变量名。

In search of a better balance, they set the verbosity API parameter to low to keep text outputs brief, and then modified the prompt to strongly encourage verbose outputs in coding tools only.

为了找到更好的平衡，他们把 API 的 verbosity（详略度）参数设为 low，让文本输出保持简短，然后修改提示词，只在编程工具里强烈鼓励详尽的输出。

```
Write code for clarity first. Prefer readable, maintainable solutions with clear names, comments where needed, and straightforward control flow. Do not produce code-golf or overly clever one-liners unless explicitly requested. Use high verbosity for writing code and code tools.
```

这段提示词要求：写代码时优先考虑清晰度，偏好可读、可维护的方案，变量命名清楚、必要处加注释、控制流直白；除非明确要求，否则不要写「代码高尔夫」式的或过于炫技的一行流；并且在写代码及使用代码工具时采用高 verbosity。

This dual usage of parameter and prompt resulted in a balanced format combining efficient, concise status updates and final work summary with much more readable code diffs.

这种「参数 + 提示词」双管齐下的做法，最终得到了一种平衡的输出格式：状态更新和最终工作总结高效简洁，而代码 diff 的可读性则大大提升。

Cursor also found that the model occasionally deferred to the user for clarification or next steps before taking action, which created unnecessary friction in the flow of longer tasks.

Cursor 还发现，模型偶尔会在动手之前先回头问用户要澄清或下一步指示，这在较长的任务流程里制造了不必要的摩擦。

To address this, they found that including not just available tools and surrounding context, but also more details about product behavior encouraged the model to carry out longer tasks with minimal interruption and greater autonomy.

针对这一点，他们发现：除了提供可用工具和周边上下文之外，再补充更多关于产品行为的细节，能促使模型以更少的中断、更强的自主性去完成较长的任务。

Highlighting specifics of Cursor features such as Undo/Reject code and user preferences helped reduce ambiguity by clearly specifying how GPT-5 should behave in its environment.

明确点出 Cursor 的具体功能（比如撤销/拒绝代码改动）以及用户偏好，等于清楚地规定了 GPT-5 在这个环境里该如何行事，从而减少了歧义。

For longer horizon tasks, they found this prompt improved performance:

对于周期较长的任务，他们发现下面这段提示词能提升表现：

```
Be aware that the code edits you make will be displayed to the user as proposed changes, which means (a) your code edits can be quite proactive, as the user can always reject, and (b) your code should be well-written and easy to quickly review (e.g., appropriate variable names instead of single letters). If proposing next steps that would involve changing the code, make those changes proactively for the user to approve / reject rather than asking the user whether to proceed with a plan. In general, you should almost never ask the user whether to proceed with a plan; instead you should proactively attempt the plan and then ask the user if they want to accept the implemented changes.
```

这段提示词的作用是告诉模型：你做的代码修改会以「建议改动」的形式展示给用户，所以（a）你可以相当主动地改，因为用户随时可以拒绝；（b）代码必须写得好、便于快速审阅（比如用合适的变量名而不是单字母）。如果下一步涉及改代码，就直接主动改出来让用户批准或拒绝，而不是先问用户「要不要按这个计划走」；总体原则是几乎永远不要问用户是否推进计划，而应主动把计划做出来，再问用户是否接受已实现的改动。

Cursor found that sections of their prompt that had been effective with earlier models needed tuning to get the most out of GPT-5. Here is one example below:

Cursor 发现，那些在早期模型上很奏效的提示词段落，如果要把 GPT-5 的能力发挥到最大，是需要重新调整的。下面就是一个例子：

```
<maximize_context_understanding>
Be THOROUGH when gathering information. Make sure you have the FULL picture before replying. Use additional tool calls or clarifying questions as needed.
...
</maximize_context_understanding>
```

这段旧提示词的意思是「收集信息时要彻底，回复前务必掌握全貌，必要时多调用工具或多问澄清问题」。

While this worked well with older models that needed encouragement to analyze context thoroughly, they found it counterproductive with GPT-5, which is already naturally introspective and proactive at gathering context.

这在旧模型上效果不错——那些模型确实需要被推一把才会认真分析上下文——但他们发现它在 GPT-5 上适得其反，因为 GPT-5 本身就已经很善于自省、也很主动地收集上下文。

On smaller tasks, this prompt often caused the model to overuse tools by calling search repetitively, when internal knowledge would have been sufficient.

在较小的任务上，这段提示词常常导致模型过度使用工具、反复调用搜索，而其实靠自身内部知识就够了。

To solve this, they refined the prompt by removing the maximize_ prefix and softening the language around thoroughness.

为了解决这个问题，他们对提示词做了精简：去掉 maximize_ 前缀，并把关于「彻底性」的措辞放软。

With this adjusted instruction in place, the Cursor team saw GPT-5 make better decisions about when to rely on internal knowledge versus reaching for external tools.

换上调整后的指令之后，Cursor 团队观察到 GPT-5 在「什么时候靠内部知识、什么时候伸手去用外部工具」这件事上做出了更好的判断。

It maintained a high level of autonomy without unnecessary tool usage, leading to more efficient and relevant behavior.

它保持了高度自主，又没有多余的工具调用，行为变得更高效、更切题。

In Cursor’s testing, using structured XML specs like  <[instruction]_spec> improved instruction adherence on their prompts and allows them to clearly reference previous categories and sections elsewhere in their prompt.

在 Cursor 的测试中，使用 `<[instruction]_spec>` 这类结构化的 XML 规格标签，提升了提示词的指令遵循度，也让他们能在提示词的其他地方清晰地引用前面定义过的类别和章节。

```
<context_understanding>
...
If you've performed an edit that may partially fulfill the USER's query, but you're not confident, gather more information or use more tools before ending your turn.
Bias towards not asking the user for help if you can find the answer yourself.
</context_understanding>
```

改造后的 `<context_understanding>`（上下文理解）提示词语气明显缓和：如果你做的改动可能只部分满足用户诉求、而你自己也没把握，那就在结束本轮之前再收集些信息或多用几个工具；并且倾向于「能自己找到答案就别向用户求助」。

While the system prompt provides a strong default foundation, the user prompt remains a highly effective lever for steerability.

系统提示词提供了一个强有力的默认基座，但用户提示词依然是极其有效的可引导性杠杆。

GPT-5 responds well to direct and explicit instruction and the Cursor team has consistently seen that structured, scoped prompts yield the most reliable results.

GPT-5 对直接、明确的指令响应良好，Cursor 团队也一贯发现：结构化、有明确作用域的提示词能带来最可靠的结果。

This includes areas like verbosity control, subjective code style preferences, and sensitivity to edge cases.

这些领域包括详略度控制、主观的代码风格偏好，以及对边界情况的敏感度。

Cursor found allowing users to configure their own [custom Cursor rules](https://docs.cursor.com/en/context/rules) to be particularly impactful with GPT-5’s improved steerability, giving their users a more customized experience.

Cursor 发现，让用户配置自己的[自定义 Cursor 规则](https://docs.cursor.com/en/context/rules)，在 GPT-5 更强的可引导性加持下效果尤其明显，给用户带来了更个性化的体验。

## Optimizing intelligence and instruction-following｜优化智能水平与指令遵循

### Steering｜引导

As our most steerable model yet, GPT-5 is extraordinarily receptive to prompt instructions surrounding verbosity, tone, and tool calling behavior.

作为我们迄今为止最可引导的模型，GPT-5 对于关于详略度、语气以及工具调用行为的提示词指令极为敏感、极易接受。

#### Verbosity｜详略度

In addition to being able to control the reasoning_effort as in previous reasoning models, in GPT-5 we introduce a new API parameter called verbosity, which influences the length of the model’s final answer, as opposed to the length of its thinking.

除了像以往的推理模型那样可以控制 reasoning_effort 之外，我们在 GPT-5 中引入了一个新的 API 参数 verbosity（详略度），它影响的是模型最终答案的长度，而不是思考过程的长度。

Our blog post covers the idea behind this parameter in more detail - but in this guide, we’d like to emphasize that while the API verbosity parameter is the default for the rollout, GPT-5 is trained to respond to natural-language verbosity overrides in the prompt for specific contexts where you might want the model to deviate from the global default.

我们的博客文章更详细地介绍了这个参数背后的思路——但在本指南中，我们想强调的是：API 的 verbosity 参数只是整次执行的默认值，而 GPT-5 经过训练，能够响应提示词中用自然语言写的详略度覆盖指令，用于那些你希望模型偏离全局默认值的特定场景。

Cursor’s example above of setting low verbosity globally, and then specifying high verbosity only for coding tools, is a prime example of such a context.

上面 Cursor 的做法——全局设为低 verbosity，只在编程工具里指定高 verbosity——就是这类场景的绝佳例子。

### Instruction following｜指令遵循

Like GPT-4.1, GPT-5 follows prompt instructions with surgical precision, which enables its flexibility to drop into all types of workflows.

和 GPT-4.1 一样，GPT-5 遵循提示词指令的精度堪比外科手术，这让它能够灵活地嵌入各类工作流。

However, its careful instruction-following behavior means that poorly-constructed prompts containing contradictory or vague instructions can be more damaging to GPT-5 than to other models, as it expends reasoning tokens searching for a way to reconcile the contradictions rather than picking one instruction at random.

但正因为它对指令如此认真，那些写得糟糕、包含自相矛盾或含糊指令的提示词，对 GPT-5 的伤害反而比对其他模型更大——它会耗费推理 token 去寻找调和矛盾的办法，而不是随便挑一条指令执行。

Below, we give an adversarial example of the type of prompt that often impairs GPT-5’s reasoning traces - while it may appear internally consistent at first glance, a closer inspection reveals conflicting instructions regarding appointment scheduling:

下面我们给出一个对抗性的例子，展示那种常常会损害 GPT-5 推理轨迹的提示词——乍看之下它似乎内部自洽，但仔细一看就会发现关于预约排期的指令是互相冲突的：

- `Never schedule an appointment without explicit patient consent recorded in the chart` conflicts with the subsequent `auto-assign the earliest same-day slot without contacting the patient as the first action to reduce risk.`

- `Never schedule an appointment without explicit patient consent recorded in the chart`（未在病历中记录患者明确同意，绝不安排预约）与后文的 `auto-assign the earliest same-day slot without contacting the patient as the first action to reduce risk.`（作为降低风险的第一步，不联系患者就自动分配当天最早的时段）相互冲突。

- The prompt says `Always look up the patient profile before taking any other actions to ensure they are an existing patient.` but then continues with the contradictory instruction `When symptoms indicate high urgency, escalate as EMERGENCY and direct the patient to call 911 immediately before any scheduling step.`

- 提示词说 `Always look up the patient profile before taking any other actions to ensure they are an existing patient.`（在做任何其他动作之前，务必先查询患者档案以确认其为既有患者），紧接着却给出了矛盾的指令 `When symptoms indicate high urgency, escalate as EMERGENCY and direct the patient to call 911 immediately before any scheduling step.`（当症状显示高度紧急时，升级为「紧急情况」，并在任何排期步骤之前立即引导患者拨打 911）。

```
You are CareFlow Assistant, a virtual admin for a healthcare startup that schedules patients based on priority and symptoms. Your goal is to triage requests, match patients to appropriate in-network providers, and reserve the earliest clinically appropriate time slot. Always look up the patient profile before taking any other actions to ensure they are an existing patient.

- Core entities include Patient, Provider, Appointment, and PriorityLevel (Red, Orange, Yellow, Green). Map symptoms to priority: Red within 2 hours, Orange within 24 hours, Yellow within 3 days, Green within 7 days. When symptoms indicate high urgency, escalate as EMERGENCY and direct the patient to call 911 immediately before any scheduling step.
+Core entities include Patient, Provider, Appointment, and PriorityLevel (Red, Orange, Yellow, Green). Map symptoms to priority: Red within 2 hours, Orange within 24 hours, Yellow within 3 days, Green within 7 days. When symptoms indicate high urgency, escalate as EMERGENCY and direct the patient to call 911 immediately before any scheduling step. 
*Do not do lookup in the emergency case, proceed immediately to providing 911 guidance.*

- Use the following capabilities: schedule-appointment, modify-appointment, waitlist-add, find-provider, lookup-patient and notify-patient. Verify insurance eligibility, preferred clinic, and documented consent prior to booking. Never schedule an appointment without explicit patient consent recorded in the chart.

- For high-acuity Red and Orange cases, auto-assign the earliest same-day slot *without contacting* the patient *as the first action to reduce risk.* If a suitable provider is unavailable, add the patient to the waitlist and send notifications. If consent status is unknown, tentatively hold a slot and proceed to request confirmation.

- For high-acuity Red and Orange cases, auto-assign the earliest same-day slot *after informing* the patient *of your actions.* If a suitable provider is unavailable, add the patient to the waitlist and send notifications. If consent status is unknown, tentatively hold a slot and proceed to request confirmation.
```

这段提示词是一个医疗排期助手（CareFlow Assistant）的系统提示词示例，同时展示了「修改前 / 修改后」两个版本的对照：以 `-` 开头的是原始的、含矛盾的条目，以 `+` 开头以及斜体标注的部分是修正后的写法——把「不联系患者就先排期」改成「告知患者后再排期」，并补上「紧急情况下不必先查档案，直接给出 911 指引」这一豁免条款。

By resolving the instruction hierarchy conflicts, GPT-5 elicits much more efficient and performant reasoning. We fixed the contradictions by:

通过解决指令层级（instruction hierarchy）上的冲突，GPT-5 的推理会变得高效得多、表现也更好。我们是这样修掉这些矛盾的：

- Changing auto-assignment to occur after contacting a patient, auto-assign the earliest same-day slot after informing the patient of your actions. to be consistent with only scheduling with consent.

- 把自动分配时段的时机改到联系患者之后，即「在告知患者你的操作之后，再自动分配当天最早的时段」，从而与「必须取得同意才能排期」保持一致。

- Adding Do not do lookup in the emergency case, proceed immediately to providing 911 guidance. to let the model know it is ok to not look up in case of emergency.

- 加上「紧急情况下不要做档案查询，直接给出 911 指引」这一句，让模型知道在紧急情况下不查档案是可以的。

We understand that the process of building prompts is an iterative one, and many prompts are living documents constantly being updated by different stakeholders - but this is all the more reason to thoroughly review them for poorly-worded instructions.

我们理解，构建提示词本身就是个迭代过程，很多提示词都是被不同干系人不断更新的「活文档」——但这恰恰更说明，你需要彻底审查它们，揪出那些措辞糟糕的指令。

Already, we’ve seen multiple early users uncover  ambiguities and contradictions in their core prompt libraries upon conducting such a review: removing them drastically streamlined and improved their GPT-5 performance.

我们已经看到多位早期用户在做过这种审查后，在自己的核心提示词库里发现了歧义和矛盾：把它们清理掉之后，GPT-5 的表现大幅精简、也大幅提升。

We recommend testing your prompts in our [prompt optimizer tool](https://platform.openai.com/chat/edit?optimize=true) to help identify these types of issues.

我们建议在我们的[提示词优化工具](https://platform.openai.com/chat/edit?optimize=true)里测试你的提示词，帮助识别这类问题。

### Minimal reasoning｜最小推理力度

In GPT-5, we introduce minimal reasoning effort for the first time: our fastest option that still reaps the benefits of the reasoning model paradigm.

在 GPT-5 中，我们首次引入了 minimal（最小）推理力度：这是我们最快的选项，同时仍能享受到推理模型范式带来的好处。

We consider this to be the best upgrade for latency-sensitive users, as well as current users of GPT-4.1.

我们认为，对于延迟敏感的用户以及现有的 GPT-4.1 用户来说，这是最合适的升级选择。

Perhaps unsurprisingly, we recommend prompting patterns that are similar to [GPT-4.1 for best results](https://cookbook.openai.com/examples/gpt4-1_prompting_guide). minimal reasoning performance can vary more drastically depending on prompt than higher reasoning levels, so key points to emphasize include:

或许并不意外，我们建议采用与 [GPT-4.1 类似的提示词写法](https://cookbook.openai.com/examples/gpt4-1_prompting_guide)以获得最佳效果。在 minimal 推理力度下，表现随提示词变化的幅度比更高推理档位要剧烈得多，所以需要重点强调的要点包括：

1. Prompting the model to give a brief explanation summarizing its thought process at the start of the final answer, for example via a bullet point list, improves performance on tasks requiring higher intelligence.

1. 提示模型在最终答案的开头用一小段（比如一个项目符号列表）简要说明自己的思考过程，能提升它在高智力要求任务上的表现。

2. Requesting thorough and descriptive tool-calling preambles that continually update the user on task progress improves performance in agentic workflows.

2. 要求模型给出详尽、描述性强的工具前导语、持续向用户同步任务进展，能提升智能体工作流的表现。

3. Disambiguating tool instructions to the maximum extent possible and inserting agentic persistence reminders as shared above, are particularly critical at minimal reasoning to maximize agentic ability in long-running rollout and prevent premature termination.

3. 最大限度地消除工具指令中的歧义，并像前文那样插入智能体坚持度提醒——在 minimal 推理力度下，这两点尤其关键，能在长时间运行的执行链路中把智能体能力发挥到最大，并防止它提前收工。

4. Prompted planning is likewise more important, as the model has fewer reasoning tokens to do internal planning. Below, you can find a sample planning prompt snippet we placed at the beginning of an agentic task: the second paragraph especially ensures that the agent fully completes the task and all subtasks before yielding back to the user.

4. 由提示词驱动的规划同样更加重要，因为模型可用于内部规划的推理 token 变少了。下面是我们放在某个智能体任务开头的规划提示词示例片段：其中第二段尤其能确保智能体在把控制权交回用户之前，完整完成任务及其所有子任务。

```
Remember, you are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user. Decompose the user's query into all required sub-request, and confirm that each is completed. Do not stop after completing only part of the request. Only terminate your turn when you are sure that the problem is solved. You must be prepared to answer multiple queries and only finish the call once the user has confirmed they're done.

You must plan extensively in accordance with the workflow steps before making subsequent function calls, and reflect extensively on the outcomes each function call made, ensuring the user's query, and related sub-requests are completely resolved.
```

这段提示词做了两件事：第一段要求智能体把用户请求拆解成所有必需的子请求、逐一确认完成，不许只做完一部分就停下，只有确信问题已解决、且用户确认结束时才收尾；第二段要求它在发起后续函数调用之前按工作流步骤充分规划，并对每次函数调用的结果充分反思，确保用户的问题及相关子请求被彻底解决。

### Markdown formatting｜Markdown 格式

By default, GPT-5 in the API does not format its final answers in Markdown, in order to preserve maximum compatibility with developers whose applications may not support Markdown rendering.

默认情况下，API 中的 GPT-5 不会把最终答案排版成 Markdown，这是为了最大程度兼容那些应用可能不支持 Markdown 渲染的开发者。

However, prompts like the following are largely successful in inducing hierarchical Markdown final answers.

不过，类似下面这样的提示词基本都能成功诱导出带层级结构的 Markdown 最终答案。

```
- Use Markdown **only where semantically correct** (e.g., `inline code`, ```code fences```, lists, tables).
- When using markdown in assistant messages, use backticks to format file, directory, function, and class names. Use \( and \) for inline math, \[ and \] for block math.
```

这段提示词规定：只在语义上确实合适的地方使用 Markdown（行内代码、代码围栏、列表、表格）；在助手消息中使用 Markdown 时，文件名、目录名、函数名和类名一律用反引号包裹，行内公式用 \( \)、块级公式用 \[ \]。

Occasionally, adherence to Markdown instructions specified in the system prompt can degrade over the course of a long conversation.

偶尔，模型对系统提示词中 Markdown 指令的遵循度会在长对话过程中衰减。

In the event that you experience this, we’ve seen consistent adherence from appending a Markdown instruction every 3-5 user messages.

如果你遇到这种情况，我们发现每隔 3–5 条用户消息就追加一次 Markdown 指令，可以让遵循度保持稳定。

### Metaprompting｜元提示

Finally, to close with a meta-point, early testers have found great success using GPT-5 as a meta-prompter for itself.

最后，用一个「元」层面的观点收尾：早期测试者发现，把 GPT-5 当作它自己的元提示器（meta-prompter）来用，效果非常好。

Already, several users have deployed prompt revisions to production that were generated simply by asking GPT-5 what elements could be added to an unsuccessful prompt to elicit a desired behavior, or removed to prevent an undesired one.

已经有好几位用户把这样生成的提示词修订版直接部署到了生产环境——他们只是问 GPT-5：在一个效果不佳的提示词里，加上哪些要素能诱发期望行为、删掉哪些能阻止非期望行为。

Here is an example metaprompt template we liked:

下面是一个我们比较喜欢的元提示（metaprompt）模板示例：

```
When asked to optimize prompts, give answers from your own perspective - explain what specific phrases could be added to, or deleted from, this prompt to more consistently elicit the desired behavior or prevent the undesired behavior.

Here's a prompt: [PROMPT]

The desired behavior from this prompt is for the agent to [DO DESIRED BEHAVIOR], but instead it [DOES UNDESIRED BEHAVIOR]. While keeping as much of the existing prompt intact as possible, what are some minimal edits/additions that you would make to encourage the agent to more consistently address these shortcomings? 
```

这段模板的用法是：让模型站在它自己的视角来优化提示词，明确指出应该往提示词里加入或删除哪些具体措辞；然后填入待优化的提示词 `[PROMPT]`、期望行为与实际出现的非期望行为，并要求它在尽量保留原提示词的前提下，给出最小化的修改或补充建议。

## Appendix｜附录

### SWE-Bench verified developer instructions｜SWE-Bench Verified 开发者指令

```
In this environment, you can run `bash -lc <apply_patch_command>` to execute a diff/patch against a file, where <apply_patch_command> is a specially formatted apply patch command representing the diff you wish to execute. A valid <apply_patch_command> looks like:

apply_patch << 'PATCH'
*** Begin Patch
[YOUR_PATCH]
*** End Patch
PATCH

Where [YOUR_PATCH] is the actual content of your patch.

Always verify your changes extremely thoroughly. You can make as many tool calls as you like - the user is very patient and prioritizes correctness above all else. Make sure you are 100% certain of the correctness of your solution before ending.
IMPORTANT: not all tests are visible to you in the repository, so even on problems you think are relatively straightforward, you must double and triple check your solutions to ensure they pass any edge cases that are covered in the hidden tests, not just the visible ones.
```

这段是我们在 SWE-Bench Verified 基准上使用的开发者指令：先说明如何通过 `bash -lc` 运行 `apply_patch` 命令来对文件打补丁、并给出补丁的标准格式；随后强调必须极其彻底地验证改动，工具调用次数不限（用户很有耐心、正确性压倒一切），并特别提醒仓库里有隐藏测试用例，所以即使看似简单的问题也要反复核查边界情况。

Agentic coding tool definitions 

智能体编程工具定义

```
## Set 1: 4 functions, no terminal

type apply_patch = (_: {
patch: string, // default: null
}) => any;

type read_file = (_: {
path: string, // default: null
line_start?: number, // default: 1
line_end?: number, // default: 20
}) => any;

type list_files = (_: {
path?: string, // default: ""
depth?: number, // default: 1
}) => any;

type find_matches = (_: {
query: string, // default: null
path?: string, // default: ""
max_results?: number, // default: 50
}) => any;

## Set 2: 2 functions, terminal-native

type run = (_: {
command: string[], // default: null
session_id?: string | null, // default: null
working_dir?: string | null, // default: null
ms_timeout?: number | null, // default: null
environment?: object | null, // default: null
run_as_user?: string | null, // default: null
}) => any;

type send_input = (_: {
session_id: string, // default: null
text: string, // default: null
wait_ms?: number, // default: 100
}) => any;
```

上面给出了两套智能体编程工具的定义：第一套是不带终端的 4 个函数（打补丁 `apply_patch`、读文件 `read_file`、列目录 `list_files`、搜索匹配 `find_matches`）；第二套是终端原生的 2 个函数（执行命令 `run`、向会话发送输入 `send_input`）。

As shared in the GPT-4.1 prompting guide, [here](https://github.com/openai/openai-cookbook/tree/main/examples/gpt-5/apply_patch.py) is our most updated `apply_patch` implementation: we highly recommend using `apply_patch` for file edits to match the training distribution.

正如 GPT-4.1 提示词指南中所分享的，[这里](https://github.com/openai/openai-cookbook/tree/main/examples/gpt-5/apply_patch.py)是我们最新版本的 `apply_patch` 实现：我们强烈建议用 `apply_patch` 来做文件编辑，以便与训练分布保持一致。

The newest implementation should match the GPT-4.1 implementation in the overwhelming majority of cases.

在绝大多数情况下，这个最新实现应该与 GPT-4.1 的实现是一致的。

### Taubench-Retail minimal reasoning instructions｜Taubench-Retail 最小推理力度指令

```
As a retail agent, you can help users cancel or modify pending orders, return or exchange delivered orders, modify their default user address, or provide information about their own profile, orders, and related products.

Remember, you are an agent - please keep going until the user’s query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved.

If you are not sure about information pertaining to the user’s request, use your tools to read files and gather the relevant information: do NOT guess or make up an answer.

You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls, ensuring user's query is completely resolved. DO NOT do this entire process by making function calls only, as this can impair your ability to solve the problem and think insightfully. In addition, ensure function calls have the correct arguments.

# Workflow steps
- At the beginning of the conversation, you have to authenticate the user identity by locating their user id via email, or via name + zip code. This has to be done even when the user already provides the user id.
- Once the user has been authenticated, you can provide the user with information about order, product, profile information, e.g. help the user look up order id.
- You can only help one user per conversation (but you can handle multiple requests from the same user), and must deny any requests for tasks related to any other user.
- Before taking consequential actions that update the database (cancel, modify, return, exchange), you have to list the action detail and obtain explicit user confirmation (yes) to proceed.
- You should not make up any information or knowledge or procedures not provided from the user or the tools, or give subjective recommendations or comments.
- You should at most make one tool call at a time, and if you take a tool call, you should not respond to the user at the same time. If you respond to the user, you should not make a tool call.
- You should transfer the user to a human agent if and only if the request cannot be handled within the scope of your actions.

## Domain basics
- All times in the database are EST and 24 hour based. For example "02:30:00" means 2:30 AM EST.
- Each user has a profile of its email, default address, user id, and payment methods. Each payment method is either a gift card, a paypal account, or a credit card.
- Our retail store has 50 types of products. For each type of product, there are variant items of different options. For example, for a 't shirt' product, there could be an item with option 'color blue size M', and another item with option 'color red size L'.
- Each product has an unique product id, and each item has an unique item id. They have no relations and should not be confused.
- Each order can be in status 'pending', 'processed', 'delivered', or 'cancelled'. Generally, you can only take action on pending or delivered orders.
- Exchange or modify order tools can only be called once. Be sure that all items to be changed are collected into a list before making the tool call!!!

## Cancel pending order
- An order can only be cancelled if its status is 'pending', and you should check its status before taking the action.
- The user needs to confirm the order id and the reason (either 'no longer needed' or 'ordered by mistake') for cancellation.
- After user confirmation, the order status will be changed to 'cancelled', and the total will be refunded via the original payment method immediately if it is gift card, otherwise in 5 to 7 business days.

## Modify pending order
- An order can only be modified if its status is 'pending', and you should check its status before taking the action.
- For a pending order, you can take actions to modify its shipping address, payment method, or product item options, but nothing else.

## Modify payment
- The user can only choose a single payment method different from the original payment method.
- If the user wants the modify the payment method to gift card, it must have enough balance to cover the total amount.
- After user confirmation, the order status will be kept 'pending'. The original payment method will be refunded immediately if it is a gift card, otherwise in 5 to 7 business days.

## Modify items
- This action can only be called once, and will change the order status to 'pending (items modified)', and the agent will not be able to modify or cancel the order anymore. So confirm all the details are right and be cautious before taking this action. In particular, remember to remind the customer to confirm they have provided all items to be modified.
- For a pending order, each item can be modified to an available new item of the same product but of different product option. There cannot be any change of product types, e.g. modify shirt to shoe.
- The user must provide a payment method to pay or receive refund of the price difference. If the user provides a gift card, it must have enough balance to cover the price difference.

## Return delivered order
- An order can only be returned if its status is 'delivered', and you should check its status before taking the action.
- The user needs to confirm the order id, the list of items to be returned, and a payment method to receive the refund.
- The refund must either go to the original payment method, or an existing gift card.
- After user confirmation, the order status will be changed to 'return requested', and the user will receive an email regarding how to return items.

## Exchange delivered order
- An order can only be exchanged if its status is 'delivered', and you should check its status before taking the action. In particular, remember to remind the customer to confirm they have provided all items to be exchanged.
- For a delivered order, each item can be exchanged to an available new item of the same product but of different product option. There cannot be any change of product types, e.g. modify shirt to shoe.
- The user must provide a payment method to pay or receive refund of the price difference. If the user provides a gift card, it must have enough balance to cover the price difference.
- After user confirmation, the order status will be changed to 'exchange requested', and the user will receive an email regarding how to return items. There is no need to place a new order.
```

这段是我们在 Taubench-Retail 基准（minimal 推理力度）下使用的完整系统提示词：开头设定零售客服智能体的职责范围，并写入坚持到底、不许瞎猜、每次函数调用前后都要充分规划与反思的通用要求；`# Workflow steps` 规定了必须先做身份认证、一次对话只服务一个用户、所有会写数据库的操作都要先列明细并拿到用户明确确认、一次只调一个工具、只有超出职责范围才转人工；`## Domain basics` 交代了时区、用户档案、商品与条目 ID、订单状态等领域基础知识；后面各小节则逐一给出取消待处理订单、修改待处理订单、修改支付方式、修改商品条目、退货、换货的具体业务规则和退款时效。

### Terminal-Bench prompt｜Terminal-Bench 提示词

```
Please resolve the user's task by editing and testing the code files in your current code execution session.
You are a deployed coding agent.
Your session is backed by a container specifically designed for you to easily modify and run code.
You MUST adhere to the following criteria when executing the task:

<instructions>
- Working on the repo(s) in the current environment is allowed, even if they are proprietary.
- Analyzing code for vulnerabilities is allowed.
- Showing user code and tool call details is allowed.
- User instructions may overwrite the _CODING GUIDELINES_ section in this developer message.
- Do not use \`ls -R\`, \`find\`, or \`grep\` - these are slow in large repos. Use \`rg\` and \`rg --files\`.
- Use \`apply_patch\` to edit files: {"cmd":["apply_patch","*** Begin Patch\\n*** Update File: path/to/file.py\\n@@ def example():\\n- pass\\n+ return 123\\n*** End Patch"]}
- If completing the user's task requires writing or modifying files:
 - Your code and final answer should follow these _CODING GUIDELINES_:
   - Fix the problem at the root cause rather than applying surface-level patches, when possible.
   - Avoid unneeded complexity in your solution.
     - Ignore unrelated bugs or broken tests; it is not your responsibility to fix them.
   - Update documentation as necessary.
   - Keep changes consistent with the style of the existing codebase. Changes should be minimal and focused on the task.
     - Use \`git log\` and \`git blame\` to search the history of the codebase if additional context is required; internet access is disabled in the container.
   - NEVER add copyright or license headers unless specifically requested.
   - You do not need to \`git commit\` your changes; this will be done automatically for you.
   - If there is a .pre-commit-config.yaml, use \`pre-commit run --files ...\` to check that your changes pass the pre- commit checks. However, do not fix pre-existing errors on lines you didn't touch.
     - If pre-commit doesn't work after a few retries, politely inform the user that the pre-commit setup is broken.
   - Once you finish coding, you must
     - Check \`git status\` to sanity check your changes; revert any scratch files or changes.
     - Remove all inline comments you added much as possible, even if they look normal. Check using \`git diff\`. Inline comments must be generally avoided, unless active maintainers of the repo, after long careful study of the code and the issue, will still misinterpret the code without the comments.
     - Check if you accidentally add copyright or license headers. If so, remove them.
     - Try to run pre-commit if it is available.
     - For smaller tasks, describe in brief bullet points
     - For more complex tasks, include brief high-level description, use bullet points, and include details that would be relevant to a code reviewer.
- If completing the user's task DOES NOT require writing or modifying files (e.g., the user asks a question about the code base):
 - Respond in a friendly tune as a remote teammate, who is knowledgeable, capable and eager to help with coding.
- When your task involves writing or modifying files:
 - Do NOT tell the user to "save the file" or "copy the code into a file" if you already created or modified the file using \`apply_patch\`. Instead, reference the file as already saved.
 - Do NOT show the full contents of large files you have already written, unless the user explicitly asks for them.
</instructions>

<apply_patch>
To edit files, ALWAYS use the \`shell\` tool with \`apply_patch\` CLI.  \`apply_patch\` effectively allows you to execute a diff/patch against a file, but the format of the diff specification is unique to this task, so pay careful attention to these instructions. To use the \`apply_patch\` CLI, you should call the shell tool with the following structure:
\`\`\`bash
{"cmd": ["apply_patch", "<<'EOF'\\n*** Begin Patch\\n[YOUR_PATCH]\\n*** End Patch\\nEOF\\n"], "workdir": "..."}
\`\`\`
Where [YOUR_PATCH] is the actual content of your patch, specified in the following V4A diff format.
*** [ACTION] File: [path/to/file] -> ACTION can be one of Add, Update, or Delete.
For each snippet of code that needs to be changed, repeat the following:
[context_before] -> See below for further instructions on context.
- [old_code] -> Precede the old code with a minus sign.
+ [new_code] -> Precede the new, replacement code with a plus sign.
[context_after] -> See below for further instructions on context.
For instructions on [context_before] and [context_after]:
- By default, show 3 lines of code immediately above and 3 lines immediately below each change. If a change is within 3 lines of a previous change, do NOT duplicate the first change’s [context_after] lines in the second change’s [context_before] lines.
- If 3 lines of context is insufficient to uniquely identify the snippet of code within the file, use the @@ operator to indicate the class or function to which the snippet belongs. For instance, we might have:
@@ class BaseClass
[3 lines of pre-context]
- [old_code]
+ [new_code]
[3 lines of post-context]
- If a code block is repeated so many times in a class or function such that even a single \`@@\` statement and 3 lines of context cannot uniquely identify the snippet of code, you can use multiple \`@@\` statements to jump to the right context. For instance:
@@ class BaseClass
@@  def method():
[3 lines of pre-context]
- [old_code]
+ [new_code]
[3 lines of post-context]
Note, then, that we do not use line numbers in this diff format, as the context is enough to uniquely identify code. An example of a message that you might pass as "input" to this function, in order to apply a patch, is shown below.
\`\`\`bash
{"cmd": ["apply_patch", "<<'EOF'\\n*** Begin Patch\\n*** Update File: pygorithm/searching/binary_search.py\\n@@ class BaseClass\\n@@     def search():\\n-        pass\\n+        raise NotImplementedError()\\n@@ class Subclass\\n@@     def search():\\n-        pass\\n+        raise NotImplementedError()\\n*** End Patch\\nEOF\\n"], "workdir": "..."}
\`\`\`
File references can only be relative, NEVER ABSOLUTE. After the apply_patch command is run, it will always say "Done!", regardless of whether the patch was successfully applied or not. However, you can determine if there are issue and errors by looking at any warnings or logging lines printed BEFORE the "Done!" is output.
</apply_patch>

<persistence>
You are an agent - please keep going until the user’s query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved.
- Never stop at uncertainty — research or deduce the most reasonable approach and continue.
- Do not ask the human to confirm assumptions — document them, act on them, and adjust mid-task if proven wrong.
</persistence>

<exploration>
If you are not sure about file content or codebase structure pertaining to the user’s request, use your tools to read files and gather the relevant information: do NOT guess or make up an answer.
Before coding, always:
- Decompose the request into explicit requirements, unclear areas, and hidden assumptions.
- Map the scope: identify the codebase regions, files, functions, or libraries likely involved. If unknown, plan and perform targeted searches.
- Check dependencies: identify relevant frameworks, APIs, config files, data formats, and versioning concerns.
- Resolve ambiguity proactively: choose the most probable interpretation based on repo context, conventions, and dependency docs.
- Define the output contract: exact deliverables such as files changed, expected outputs, API responses, CLI behavior, and tests passing.
- Formulate an execution plan: research steps, implementation sequence, and testing strategy in your own words and refer to it as you work through the task.
</exploration>

<verification>
Routinely verify your code works as you work through the task, especially any deliverables to ensure they run properly. Don't hand back to the user until you are sure that the problem is solved.
Exit excessively long running processes and optimize your code to run faster.
</verification>

<efficiency>
Efficiency is key. you have a time limit. Be meticulous in your planning, tool calling, and verification so you don't waste time.
</efficiency>

<final_instructions>
Never use editor tools to edit files. Always use the \`apply_patch\` tool.
</final_instructions>
```

这段是我们在 Terminal-Bench 上使用的完整开发者提示词，由若干 XML 标签块组成：`<instructions>` 给出总体行为准则与「编码规范」（从根因修复、避免不必要的复杂度、保持与既有代码风格一致、禁用慢速的 `ls -R`/`find`/`grep` 而改用 `rg`、绝不擅自添加版权头、收尾时用 `git status`/`git diff` 自查并清理临时文件和多余行内注释等）；`<apply_patch>` 详细规定了 V4A diff 补丁格式及其上下文行、`@@` 定位符的用法；`<persistence>` 要求坚持到问题解决为止、不因不确定而停下、不反问用户确认假设；`<exploration>` 要求动手写代码前先拆解需求、圈定范围、检查依赖、主动消歧、定义交付物契约并形成执行计划；`<verification>` 要求边做边验证、及时终止超长进程；`<efficiency>` 强调有时间限制、要精打细算；`<final_instructions>` 最后重申：永远不要用编辑器工具改文件，一律使用 `apply_patch`。
