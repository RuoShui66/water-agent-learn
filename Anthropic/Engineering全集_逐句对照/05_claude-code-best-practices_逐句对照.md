# 05_Claude Code: Best practices for agentic coding_Claude Code：智能体编码最佳实践

> 原文：https://www.anthropic.com/engineering/claude-code-best-practices
> 作者：Anthropic Engineering｜发布日期：2025-04-18
> 注：原博客已迁移至 Claude Code 官方文档并持续更新，本文为 2026-08 抓取的最新版。

## 📌 本篇速览

- 📅 2025-04-18　｜　⏱ 约 30 分钟　｜　📄 5,348 词 / 0 图
- ⭐ ★★★★★ **必读** —— Anthropic 对自家旗舰编码智能体的官方实践总结，是理解上下文工程与人机协作工作流最直接、可操作性最强的一手材料。
- 🏷 Claude Code、上下文管理、智能体编码、验证闭环、子智能体
- 🖼 [图解笔记（面试速记）](05_claude-code-best-practices_直观图解与学习笔记.md)　·　🗂 [返回总目录](00_目录与阅读进度.md)

Anthropic 官方总结的 Claude Code 使用最佳实践，核心约束是上下文窗口会快速填满并拖低性能。文章围绕这一约束给出成体系的做法：给 Claude 可自行运行的验证手段（测试／构建／截图／Stop hook）、先探索再规划最后编码、在提示词中给出具体上下文、通过 CLAUDE.md、权限模式、CLI 工具、MCP、hook、技能、子智能体和插件配置环境，以及会话管理、并行会话与非交互扇出等自动化规模化手法，最后列出五种常见失败模式。

---

> Tips and patterns for getting the most out of Claude Code, from configuring your environment to scaling across parallel sessions.

> 从配置环境到跨多个并行会话规模化，充分发挥 Claude Code 效能的技巧与模式。

Claude Code is an agentic coding environment.

Claude Code 是一个智能体式（agentic）编码环境。

Unlike a chatbot that answers questions and waits, Claude Code can read your files, run commands, make changes, and autonomously work through problems while you watch, redirect, or step away entirely.

不同于回答完问题就干等着的聊天机器人，Claude Code 能读取你的文件、运行命令、修改代码，并自主推进问题的解决——而你可以在一旁观看、随时纠偏，也可以完全走开。

This changes how you work.

这改变了你的工作方式。

Instead of writing code yourself and asking Claude to review it, you describe what you want and Claude figures out how to build it. Claude explores, plans, and implements.

你不再是自己写代码、再让 Claude 来审查，而是描述你想要什么，由 Claude 想办法把它做出来。Claude 会探索、规划并动手实现。

But this autonomy still comes with a learning curve. Claude works within certain constraints you need to understand.

但这种自主性仍然伴随一条学习曲线。Claude 是在一些你需要了解的约束条件下工作的。

This guide covers patterns that have proven effective across Anthropic's internal teams and for engineers using Claude Code across various codebases, languages, and environments.

本指南涵盖的模式，已在 Anthropic 的内部团队中、以及在各类代码库、语言和环境中使用 Claude Code 的工程师那里被证明行之有效。

For how the agentic loop works under the hood, see [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works).

关于智能体循环（agentic loop）的底层工作原理，参见 [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)。

***

Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills.

大多数最佳实践都源自同一个约束：Claude 的上下文窗口（context window）填得很快，而性能会随着它被填满而下降。

Claude's context window holds your entire conversation, including every message, every file Claude reads, and every command output. However, this can fill up fast.

Claude 的上下文窗口装着你的整段对话，包括每条消息、Claude 读过的每个文件，以及每条命令的输出。然而，它可能很快就被填满。

A single debugging session or codebase exploration might generate and consume tens of thousands of tokens.

一次调试会话或一次代码库探索，就可能产生并消耗数万 token。

This matters since LLM performance degrades as context fills.

这一点很关键，因为 LLM 的性能会随上下文被填满而下降。

When the context window is getting full, Claude may start "forgetting" earlier instructions or making more mistakes.

当上下文窗口接近饱和时，Claude 可能开始"忘记"先前的指令，或者犯更多错误。

The context window is the most important resource to manage.

上下文窗口是最需要用心管理的资源。

To see how a session fills up in practice, [watch an interactive walkthrough](https://code.claude.com/docs/en/context-window) of what loads at startup and what each file read costs.

想直观了解一次会话是如何被填满的，可以[观看交互式演示](https://code.claude.com/docs/en/context-window)，看看启动时会加载什么、每次读文件要付出多少上下文成本。

Track context usage continuously with a [custom status line](https://code.claude.com/docs/en/statusline), and see [Reduce token usage](https://code.claude.com/docs/en/costs#reduce-token-usage) for strategies on reducing token usage.

用[自定义状态栏（status line）](https://code.claude.com/docs/en/statusline)持续跟踪上下文用量；关于减少 token 消耗的策略，参见 [Reduce token usage](https://code.claude.com/docs/en/costs#reduce-token-usage)。

***

## Give Claude a way to verify its work｜给 Claude 一个验证工作成果的途径

<Tip>
  Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from.

  给 Claude 一个它自己能运行的检查：测试、构建、可供比对的截图。这是"你必须盯着的会话"与"你可以放手走开的会话"之间的分水岭。
</Tip>

Claude stops when the work looks done.

Claude 会在工作"看起来完成了"的时候停下来。

Without a check it can run, "looks done" is the only signal available, and you become the verification loop: every mistake waits for you to notice it.

如果没有一个它能运行的检查，"看起来完成了"就是唯一可用的信号，而你就成了那个验证环节：每个错误都要等你亲自去发现。

Give Claude something that produces a pass or fail, and the loop closes on its own.

给 Claude 一个能产出"通过/失败"信号的东西，这个循环就能自行闭合。

Claude does the work, runs the check, reads the result, and iterates until the check passes.

Claude 完成工作、运行检查、读取结果，然后不断迭代，直到检查通过。

The check is anything that returns a signal Claude can read in the conversation: a test suite, a build exit code, a linter, a script that diffs output against a fixture, or a [browser screenshot](https://code.claude.com/docs/en/chrome) compared against a design.

这个检查可以是任何能在对话中返回 Claude 可读信号的东西：一套测试、构建的退出码、一个 linter、一个把输出与基准数据（fixture）做 diff 的脚本，或是一张与设计稿比对的[浏览器截图](https://code.claude.com/docs/en/chrome)。

| Strategy                              | Before                                                  | After                                                                                                                                                                                                   |
| ------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Provide verification criteria**     | *"implement a function that validates email addresses"* | *"write a validateEmail function. example test cases: [user@example.com](mailto:user@example.com) is true, invalid is false, [user@.com](mailto:user@.com) is false. run the tests after implementing"* |
| **Verify UI changes visually**        | *"make the dashboard look better"*                      | *"\[paste screenshot] implement this design. take a screenshot of the result and compare it to the original. list differences and fix them"*                                                            |
| **Address root causes, not symptoms** | *"the build is failing"*                                | *"the build fails with this error: \[paste error]. fix it and verify the build succeeds. address the root cause, don't suppress the error"*                                                             |

| 策略                 | 之前                | 之后                                                                                                    |
| ------------------ | ----------------- | ----------------------------------------------------------------------------------------------------- |
| **提供验证标准**         | *「实现一个校验邮箱地址的函数」* | *「写一个 validateEmail 函数。示例测试用例：user@example.com 为 true，invalid 为 false，user@.com 为 false。实现完成后运行这些测试」* |
| **以可视化方式验证 UI 改动** | *「把仪表盘弄好看点」*      | *「[粘贴截图] 实现这个设计。对结果截图并与原图比对，列出差异并修复」*                                                                 |
| **解决根因，而非症状**      | *「构建失败了」*         | *「构建失败并报出这个错误：[粘贴错误]。修复它并验证构建成功。要解决根本原因，不要把错误压掉」*                                                     |

Once the check exists, decide how hard it gates the stop:

检查一旦就位，接下来要决定它对"何时停止"的把关有多严：

* **In one prompt**: ask Claude to run the check and iterate in the same message, as in the table above.

* **在单条提示词里**：像上表那样，在同一条消息里要求 Claude 运行检查并迭代。

* **Across a session**: set the check as a [`/goal` condition](https://code.claude.com/docs/en/goal). A separate evaluator re-checks it after every turn and Claude keeps working until it holds.

* **贯穿整个会话**：把检查设为 [`/goal` 条件](https://code.claude.com/docs/en/goal)。每个回合结束后都会有一个独立的评估器重新校验，Claude 会一直工作，直到条件成立。

* **As a deterministic gate**: a [Stop hook](https://code.claude.com/docs/en/hooks#stop) runs your check as a script and blocks the turn from ending until it passes. Claude Code overrides the hook and ends the turn after 8 consecutive blocks.

* **作为确定性闸门**：[Stop hook](https://code.claude.com/docs/en/hooks#stop)会以脚本形式运行你的检查，在其通过之前阻止回合结束。若连续被阻塞 8 次，Claude Code 会越过该 hook 并结束回合。

* **By a second opinion**: a [verification subagent](https://code.claude.com/docs/en/sub-agents) or a [dynamic workflow](https://code.claude.com/docs/en/workflows) that checks its own findings has a fresh model try to refute the result, so the agent doing the work isn't the one grading it.

* **靠第二意见**：使用[验证子智能体（subagent）](https://code.claude.com/docs/en/sub-agents)，或一个会复核自身结论的[动态工作流](https://code.claude.com/docs/en/workflows)，让一个全新的模型尝试推翻结果——这样干活的智能体就不是给自己打分的那一个。

Each step trades setup for attention.

每往上一级，都是在用更多前期配置换取更少的人工盯守。

The prompt version works on any task today. The `/goal` and Stop hook versions are what let an unattended run finish correctly without you.

提示词版本今天就能用在任何任务上。而 `/goal` 和 Stop hook 版本，才是让无人值守的运行在没有你的情况下也能正确收尾的关键。

Have Claude show evidence rather than asserting success: the test output, the command it ran and what it returned, or a screenshot of the result.

让 Claude 出示证据，而不是口头宣称成功：测试输出、它运行的命令及其返回结果，或结果的截图。

Reviewing evidence is faster than re-running the verification yourself, and it works for sessions you weren't watching.

审查证据比你自己把验证重新跑一遍更快，而且对你没有盯着的会话同样有效。

***

## Explore first, then plan, then code｜先探索，再规划，然后写代码

<Tip>
  Separate research and planning from implementation to avoid solving the wrong problem.

  把调研和规划与实现分开，避免解决了错误的问题。
</Tip>

Letting Claude jump straight to coding can produce code that solves the wrong problem.

让 Claude 直接上手写代码，可能会产出"解错了题"的代码。

Use [plan mode](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) to separate exploration from execution.

使用[规划模式（plan mode）](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode)把探索与执行分开。

The recommended workflow has four phases:

推荐的工作流分为四个阶段：

<Steps>
  <Step title="Explore｜探索">
    Enter plan mode. Claude reads files and answers questions without making changes.

    进入规划模式。Claude 会阅读文件、回答问题，而不做任何改动。

    ```txt title="claude (plan mode)" wrap theme={null}
    read /src/auth and understand how we handle sessions and login.
    also look at how we manage environment variables for secrets.
    ```
  </Step>

  <Step title="Plan｜规划">
    Ask Claude to create a detailed implementation plan.

    让 Claude 制定一份详细的实现计划。

    ```txt title="claude (plan mode)" wrap theme={null}
    I want to add Google OAuth. What files need to change?
    What's the session flow? Create a plan.
    ```

    Press `Ctrl+G` to open the plan in your text editor for direct editing before Claude proceeds.

    按 `Ctrl+G` 可以在你的文本编辑器中打开这份计划，在 Claude 继续之前直接编辑它。
  </Step>

  <Step title="Implement｜实现">
    Switch out of plan mode and let Claude code, verifying against its plan.

    退出规划模式，让 Claude 写代码，并对照它的计划进行验证。

    ```txt title="claude (default mode)" wrap theme={null}
    implement the OAuth flow from your plan. write tests for the
    callback handler, run the test suite and fix any failures.
    ```
  </Step>

  <Step title="Commit｜提交">
    Ask Claude to commit with a descriptive message and create a PR.

    让 Claude 用一条描述清晰的提交信息完成 commit，并创建 PR。

    ```txt title="claude (default mode)" wrap theme={null}
    commit with a descriptive message and open a PR
    ```
  </Step>
</Steps>

<Callout>
  Plan mode is useful, but also adds overhead.

  规划模式很有用，但也会带来额外开销。

  For tasks where the scope is clear and the fix is small (like fixing a typo, adding a log line, or renaming a variable) ask Claude to do it directly.

  对于范围明确、改动很小的任务（比如修个拼写错误、加一行日志、重命名一个变量），直接让 Claude 动手就行。

  Planning is most useful when you're uncertain about the approach, when the change modifies multiple files, or when you're unfamiliar with the code being modified.

  规划在这些时候最有用：你对实现方案没有把握、改动会涉及多个文件，或者你对要修改的代码并不熟悉。

  If you could describe the diff in one sentence, skip the plan.

  如果你能用一句话把这个 diff 描述清楚，那就跳过规划。
</Callout>

***

## Provide specific context in your prompts｜在提示词里给出具体的上下文

<Tip>
  The more precise your instructions, the fewer corrections you'll need.

  你的指令越精确，需要纠正的次数就越少。
</Tip>

Claude can infer intent, but it can't read your mind.

Claude 能推断你的意图，但它读不了你的心。

Reference specific files, mention constraints, and point to example patterns.

要引用具体的文件、说明约束条件，并指出可以参照的范例模式。

| Strategy                                                                                         | Before                                               | After                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------ | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Scope the task.** Specify which file, what scenario, and testing preferences.                  | *"add tests for foo.py"*                             | *"write a test for foo.py covering the edge case where the user is logged out. avoid mocks."*                                                                                                                                                                                                                                                                    |
| **Point to sources.** Direct Claude to the source that can answer a question.                    | *"why does ExecutionFactory have such a weird api?"* | *"look through ExecutionFactory's git history and summarize how its api came to be"*                                                                                                                                                                                                                                                                             |
| **Reference existing patterns.** Point Claude to patterns in your codebase.                      | *"add a calendar widget"*                            | *"look at how existing widgets are implemented on the home page to understand the patterns. HotDogWidget.php is a good example. follow the pattern to implement a new calendar widget that lets the user select a month and paginate forwards/backwards to pick a year. build from scratch without libraries other than the ones already used in the codebase."* |
| **Describe the symptom.** Provide the symptom, the likely location, and what "fixed" looks like. | *"fix the login bug"*                                | *"users report that login fails after session timeout. check the auth flow in src/auth/, especially token refresh. write a failing test that reproduces the issue, then fix it"*                                                                                                                                                                                 |

| 策略                                                | 之前                                        | 之后                                                                                                                                             |
| ------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **框定任务范围。** 指明是哪个文件、什么场景，以及测试方面的偏好。               | *「给 foo.py 加测试」*                          | *「给 foo.py 写一个测试，覆盖用户已登出这个边界情况。不要用 mock。」*                                                                                                     |
| **指向信息来源。** 把 Claude 引导到能回答这个问题的源头。               | *「ExecutionFactory 的 api 为什么这么奇怪？」*       | *「翻一遍 ExecutionFactory 的 git 历史，总结它的 api 是怎么演变成今天这样的」*                                                                                          |
| **参照已有模式。** 把 Claude 指向你代码库里现成的模式。                | *「加一个日历组件」*                               | *「看看首页上现有的组件是怎么实现的，理解其中的模式。HotDogWidget.php 是个好例子。按照同样的模式实现一个新的日历组件，允许用户选择月份，并可以前后翻页选择年份。从零开始写，除了代码库里已经用到的库之外不要引入其他库。」*                            |
| **描述症状。** 给出症状、可能的位置，以及"修好了"是什么样。                 | *「修一下登录的 bug」*                            | *「用户反馈会话超时后登录失败。检查 src/auth/ 里的认证流程，特别是 token 刷新那部分。先写一个能复现该问题的失败测试，然后修复它」*                                                                    |

Vague prompts can be useful when you're exploring and can afford to course-correct.

当你处在探索阶段、并且有余裕随时纠偏时，模糊的提示词也是有用的。

A prompt like `"what would you improve in this file?"` can surface things you wouldn't have thought to ask about.

像 `"what would you improve in this file?"`（这个文件里你会改进什么？）这样的提示词，能挖出一些你根本想不到要去问的东西。

### Provide rich content｜提供丰富的内容

<Tip>
  Use `@` to reference files, paste screenshots/images, or pipe data directly.

  用 `@` 引用文件、直接粘贴截图/图片，或者用管道直接把数据喂进来。
</Tip>

You can provide rich data to Claude in several ways:

你可以通过多种方式给 Claude 提供丰富的数据：

* **Reference files with `@`** instead of describing where code lives. Claude reads the file before responding.

* **用 `@` 引用文件**，而不是去描述代码在哪儿。Claude 会先读这个文件再作答。

* **Paste images directly**. Copy/paste or drag and drop images into the prompt.

* **直接粘贴图片**。把图片复制粘贴或拖拽到提示词里。

* **Give URLs** for documentation and API references. Use `/permissions` to allowlist frequently-used domains.

* **给出 URL**，指向文档和 API 参考。用 `/permissions` 把常用域名加入白名单。

* **Pipe in data** by running `cat error.log | claude` to send file contents directly.

* **用管道灌入数据**，比如运行 `cat error.log | claude`，把文件内容直接发过去。

* **Let Claude fetch what it needs**. Tell Claude to pull context itself using Bash commands, MCP tools, or by reading files.

* **让 Claude 自己去取它需要的东西**。告诉 Claude 自行通过 Bash 命令、MCP 工具或读文件来获取上下文。

***

## Configure your environment｜配置你的环境

A few setup steps make Claude Code significantly more effective across all your sessions.

只需几步配置，就能让 Claude Code 在你所有的会话中都显著更高效。

For a full overview of extension features and when to use each one, see [Extend Claude Code](https://code.claude.com/docs/en/features-overview).

关于各类扩展能力的完整概览以及何时该用哪一种，参见 [Extend Claude Code](https://code.claude.com/docs/en/features-overview)。

### Write an effective CLAUDE.md｜写一份高效的 CLAUDE.md

<Tip>
  Run `/init` to generate a starter CLAUDE.md file based on your current project structure, then refine over time.

  运行 `/init` 可以基于你当前的项目结构生成一份 CLAUDE.md 初始文件，之后再逐步打磨。
</Tip>

CLAUDE.md is a special file that Claude reads at the start of every conversation.

CLAUDE.md 是一个特殊文件，Claude 在每次对话开始时都会读取它。

Include Bash commands, code style, and workflow rules.

在里面写上 Bash 命令、代码风格和工作流规则。

This gives Claude persistent context it can't infer from code alone.

这为 Claude 提供了仅凭代码无法推断出来的持久上下文。

The `/init` command analyzes your codebase to detect build systems, test frameworks, and code patterns, giving you a solid foundation to refine.

`/init` 命令会分析你的代码库，识别构建系统、测试框架和代码模式，给你一个可供打磨的扎实基础。

There's no required format for CLAUDE.md files, but keep it short and human-readable. For example:

CLAUDE.md 没有强制格式要求，但要保持简短、便于人阅读。例如：

```markdown CLAUDE.md theme={null}
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

Run `/context` to confirm Claude loaded the file.

运行 `/context` 确认 Claude 确实加载了这个文件。

CLAUDE.md is loaded every session, so only include things that apply broadly.

CLAUDE.md 每次会话都会被加载，所以只放那些普遍适用的内容。

For domain knowledge or workflows that are only relevant sometimes, use [skills](https://code.claude.com/docs/en/skills) instead.

对于只是偶尔才用得上的领域知识或工作流，改用[技能（skills）](https://code.claude.com/docs/en/skills)。

Claude loads them on demand without bloating every conversation.

Claude 会按需加载它们，而不会让每次对话都变得臃肿。

Keep it concise. For each line, ask: *"Would removing this cause Claude to make mistakes?"* If not, cut it.

保持精简。对每一行都问一句：*「删掉这条会不会导致 Claude 犯错？」* 如果不会，就删掉。

Bloated CLAUDE.md files cause Claude to ignore your actual instructions!

臃肿的 CLAUDE.md 会导致 Claude 忽略你真正要它遵守的指令！

| ✅ Include                                            | ❌ Exclude                                          |
| ---------------------------------------------------- | -------------------------------------------------- |
| Bash commands Claude can't guess                     | Anything Claude can figure out by reading code     |
| Code style rules that differ from defaults           | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners      | Detailed API documentation (link to docs instead)  |
| Repository etiquette (branch naming, PR conventions) | Information that changes frequently                |
| Architectural decisions specific to your project     | Long explanations or tutorials                     |
| Developer environment quirks (required env vars)     | File-by-file descriptions of the codebase          |
| Common gotchas or non-obvious behaviors              | Self-evident practices like "write clean code"     |

| ✅ 应该写进去                     | ❌ 不该写进去                       |
| --------------------------- | ---------------------------- |
| Claude 猜不出来的 Bash 命令        | 任何 Claude 读代码就能自己搞清楚的东西      |
| 与默认约定不同的代码风格规则              | Claude 早已知道的标准语言惯例           |
| 测试说明和偏好使用的测试运行器             | 详尽的 API 文档（改成放个文档链接）         |
| 仓库礼仪（分支命名、PR 规范）            | 经常变动的信息                      |
| 你项目特有的架构决策                  | 冗长的解释或教程                     |
| 开发环境的特殊之处（必需的环境变量）          | 逐个文件描述整个代码库                  |
| 常见的坑或不那么显而易见的行为             | 「写干净的代码」这类不言自明的老生常谈         |

If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost.

如果明明写了规则禁止某件事，Claude 却还是一再照做，那多半是文件太长，那条规则被淹没了。

If Claude asks you questions that are answered in CLAUDE.md, the phrasing might be ambiguous.

如果 Claude 问你的问题在 CLAUDE.md 里明明有答案，那可能是措辞有歧义。

Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts.

把 CLAUDE.md 当代码来对待：出问题时去审查它，定期修剪，并通过观察 Claude 的行为是否真的发生变化来验证你的改动。

You can tune instructions by adding emphasis (e.g., "IMPORTANT" or "YOU MUST") to improve adherence.

你可以通过加强语气（例如 "IMPORTANT" 或 "YOU MUST"）来调优指令，提高遵守率。

Check CLAUDE.md into git so your team can contribute. The file compounds in value over time.

把 CLAUDE.md 提交进 git，好让团队一起贡献。这个文件的价值会随时间复利增长。

CLAUDE.md files can import additional files using `@path/to/import` syntax:

CLAUDE.md 文件可以用 `@path/to/import` 语法导入其他文件：

```markdown CLAUDE.md theme={null}
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

You can place CLAUDE.md files in several locations:

CLAUDE.md 文件可以放在好几个位置：

* **Home folder (`~/.claude/CLAUDE.md`)**: applies to all Claude sessions

* **主目录（`~/.claude/CLAUDE.md`）**：对所有 Claude 会话生效。

* **Project root (`./CLAUDE.md`)**: check into git to share with your team

* **项目根目录（`./CLAUDE.md`）**：提交进 git，与团队共享。

* **Project root (`./CLAUDE.local.md`)**: personal project-specific notes; add this file to your `.gitignore` so it isn't shared with your team

* **项目根目录（`./CLAUDE.local.md`）**：个人的、项目专属的笔记；把这个文件加进 `.gitignore`，这样就不会共享给团队。

* **Parent directories**: useful for monorepos where both `root/CLAUDE.md` and `root/foo/CLAUDE.md` are pulled in automatically

* **父级目录**：适用于 monorepo，`root/CLAUDE.md` 和 `root/foo/CLAUDE.md` 会被自动一起加载。

* **Child directories**: Claude pulls in child CLAUDE.md files on demand when it reads a file in those directories

* **子目录**：当 Claude 读取这些目录下的文件时，会按需把子目录的 CLAUDE.md 拉进来。

### Configure permissions｜配置权限

<Tip>
  Use [auto mode](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode) to let a classifier handle approvals, `/permissions` to allowlist specific commands, or `/sandbox` for OS-level isolation. Each reduces interruptions while keeping you in control.

  用 [auto 模式](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode)让分类器模型来处理授权，用 `/permissions` 把特定命令加入白名单，或者用 `/sandbox` 做操作系统级隔离。这几种方式都能在你仍掌握控制权的前提下减少打断。
</Tip>

By default, Claude Code requests permission for actions that might modify your system: file writes, Bash commands, MCP tools, etc.

默认情况下，Claude Code 对可能修改你系统的操作都会请求授权：写文件、Bash 命令、MCP 工具等等。

This is safe but tedious.

这样很安全，但也很烦。

After the tenth approval you're not really reviewing anymore, you're just clicking through.

批到第十次的时候，你其实已经不是在审查了，只是在无脑点确认。

There are three ways to reduce these interruptions:

有三种办法可以减少这类打断：

* **Auto mode**: a separate classifier model reviews commands and blocks only what looks risky: scope escalation, unknown infrastructure, or hostile-content-driven actions. Best when you trust the general direction of a task but don't want to click through every step

* **Auto 模式**：由一个独立的分类器模型来审查命令，只拦截看起来有风险的：越权扩大范围、未知的基础设施，或由恶意内容驱动的操作。适合你信任任务的大方向、但不想每一步都点确认的场景。

* **Permission allowlists**: permit specific tools you know are safe, like `npm run lint` or `git commit`

* **权限白名单**：放行你确定安全的特定工具，比如 `npm run lint` 或 `git commit`。

* **Sandboxing**: enable OS-level isolation that restricts filesystem and network access, allowing Claude to work more freely within defined boundaries

* **沙箱（Sandboxing）**：启用操作系统级隔离，限制文件系统和网络访问，让 Claude 在划定的边界内更自由地干活。

Read more about [permission modes](https://code.claude.com/docs/en/permission-modes), [permission rules](https://code.claude.com/docs/en/permissions), and [sandboxing](https://code.claude.com/docs/en/sandboxing).

更多内容参见[权限模式](https://code.claude.com/docs/en/permission-modes)、[权限规则](https://code.claude.com/docs/en/permissions)和[沙箱](https://code.claude.com/docs/en/sandboxing)。

### Use CLI tools｜使用命令行工具

<Tip>
  Tell Claude Code to use CLI tools like `gh`, `aws`, `gcloud`, and `sentry-cli` when interacting with external services.

  在与外部服务打交道时，告诉 Claude Code 去用 `gh`、`aws`、`gcloud`、`sentry-cli` 这类命令行工具。
</Tip>

CLI tools are the most context-efficient way to interact with external services.

命令行工具是与外部服务交互时最省上下文的方式。

If you use GitHub, install the `gh` CLI.

如果你用 GitHub，就装上 `gh` 这个 CLI。

Claude knows how to use it for creating issues, opening pull requests, and reading comments.

Claude 知道怎么用它来创建 issue、开 pull request、读评论。

Without `gh`, Claude can still use the GitHub API, but unauthenticated requests often hit rate limits.

没有 `gh` 的话，Claude 仍然可以调 GitHub API，但未认证的请求经常会撞上限流。

Claude is also effective at learning CLI tools it doesn't already know.

Claude 也很擅长现学它本来不会用的命令行工具。

Try prompts like `Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.`

可以试试这样的提示词：`Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.`（用 `foo-cli-tool --help` 了解 foo 工具，然后用它来解决 A、B、C。）

### Connect MCP servers｜接入 MCP 服务器

<Tip>
  Run `claude mcp add` to connect external tools like Notion, Figma, or your database.

  运行 `claude mcp add` 接入 Notion、Figma 或你的数据库等外部工具。
</Tip>

With [MCP servers](https://code.claude.com/docs/en/mcp), you can ask Claude to implement features from issue trackers, query databases, analyze monitoring data, integrate designs from Figma, and automate workflows.

有了 [MCP 服务器](https://code.claude.com/docs/en/mcp)，你就可以让 Claude 根据缺陷跟踪系统里的条目来实现功能、查询数据库、分析监控数据、对接 Figma 里的设计稿，以及自动化各种工作流。

### Set up hooks｜设置 hook

<Tip>
  Use hooks for actions that must happen every time with zero exceptions.

 对于那些必须每次都执行、不容任何例外的操作，用 hook。
</Tip>

[Hooks](https://code.claude.com/docs/en/hooks-guide) run scripts automatically at specific points in Claude's workflow.

[hook](https://code.claude.com/docs/en/hooks-guide)会在 Claude 工作流的特定节点自动运行脚本。

Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens.

不同于 CLAUDE.md 里那些只具建议性质的指令，hook 是确定性的，能保证该动作一定发生。

Claude can write hooks for you.

Claude 可以帮你写 hook。

Try prompts like *"Write a hook that runs eslint after every file edit"* or *"Write a hook that blocks writes to the migrations folder."*

试试这样的提示词：*「写一个 hook，在每次编辑文件后运行 eslint」*，或者 *「写一个 hook，禁止写入 migrations 目录」*。

Edit `.claude/settings.json` directly to configure hooks by hand, and run `/hooks` to browse what's configured.

想手工配置 hook 就直接编辑 `.claude/settings.json`，运行 `/hooks` 可以查看当前都配了些什么。

### Create skills｜创建技能

<Tip>
  Create `SKILL.md` files in `.claude/skills/` to give Claude domain knowledge and reusable workflows.

  在 `.claude/skills/` 下创建 `SKILL.md` 文件，为 Claude 提供领域知识和可复用的工作流。
</Tip>

[Skills](https://code.claude.com/docs/en/skills) extend Claude's knowledge with information specific to your project, team, or domain.

[技能](https://code.claude.com/docs/en/skills)用你项目、团队或领域专属的信息来扩展 Claude 的知识。

Claude applies them automatically when relevant, or you can invoke them directly with `/skill-name`.

相关时 Claude 会自动调用它们，你也可以用 `/skill-name` 直接触发。

Create a skill by adding a directory with a `SKILL.md` to `.claude/skills/`:

创建技能的方式是在 `.claude/skills/` 下加一个包含 `SKILL.md` 的目录：

```markdown .claude/skills/api-conventions/SKILL.md theme={null}
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

Skills can also define repeatable workflows you invoke directly:

技能也可以定义供你直接调用的可重复工作流：

```markdown .claude/skills/fix-issue/SKILL.md theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

Run `/fix-issue 1234` to invoke it.

运行 `/fix-issue 1234` 就能调用它。

Use `disable-model-invocation: true` for workflows with side effects that you want to trigger manually.

对于那些有副作用、你希望手动触发的工作流，加上 `disable-model-invocation: true`。

### Create custom subagents｜创建自定义子智能体

<Tip>
  Define specialized assistants in `.claude/agents/` that Claude can delegate to for isolated tasks.

  在 `.claude/agents/` 中定义专门化的助手，Claude 可以把独立的任务委派给它们。
</Tip>

[Subagents](https://code.claude.com/docs/en/sub-agents) run in their own context with their own set of allowed tools.

[子智能体](https://code.claude.com/docs/en/sub-agents)运行在各自独立的上下文里，拥有各自的可用工具集。

They're useful for tasks that read many files or need specialized focus without cluttering your main conversation.

对于那些要读很多文件、或需要专项聚焦、又不想弄乱主对话的任务，它们很有用。

```markdown .claude/agents/security-reviewer.md theme={null}
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

Tell Claude to use subagents explicitly: *"Use a subagent to review this code for security issues."*

明确告诉 Claude 去用子智能体：*「用一个子智能体来审查这段代码的安全问题。」*

### Install plugins｜安装插件

<Tip>
  Run `/plugin` to browse the marketplace. Plugins add skills, tools, and integrations without configuration.

  运行 `/plugin` 浏览插件市场。插件无需配置就能带来技能、工具和各种集成。
</Tip>

[Plugins](https://code.claude.com/docs/en/plugins) bundle skills, hooks, subagents, and MCP servers into a single installable unit from the community and Anthropic.

[插件](https://code.claude.com/docs/en/plugins)把技能、hook、子智能体和 MCP 服务器打包成一个可安装单元，来源包括社区和 Anthropic。

If you work with a typed language, install a [code intelligence plugin](https://code.claude.com/docs/en/discover-plugins#code-intelligence) to give Claude precise symbol navigation and automatic error detection after edits.

如果你使用的是带类型系统的语言，装一个[代码智能插件](https://code.claude.com/docs/en/discover-plugins#code-intelligence)，让 Claude 能精确地做符号跳转，并在编辑后自动检测错误。

For guidance on choosing between skills, subagents, hooks, and MCP, see [Extend Claude Code](https://code.claude.com/docs/en/features-overview#match-features-to-your-goal).

关于如何在技能、子智能体、hook 和 MCP 之间做选择，参见 [Extend Claude Code](https://code.claude.com/docs/en/features-overview#match-features-to-your-goal)。

***

## Communicate effectively｜有效地沟通

The way you communicate with Claude Code significantly impacts the quality of results.

你与 Claude Code 沟通的方式，会显著影响结果的质量。

### Ask codebase questions｜就代码库提问

<Tip>
  Ask Claude questions you'd ask a senior engineer.

  把你会问资深工程师的问题拿来问 Claude。
</Tip>

When onboarding to a new codebase, use Claude Code for learning and exploration.

刚接触一个新代码库时，用 Claude Code 来学习和探索。

You can ask Claude the same sorts of questions you would ask another engineer:

你可以问 Claude 那些你会去问其他工程师的问题：

* How does logging work?

* 日志是怎么工作的？

* How do I make a new API endpoint?

* 我该怎么新建一个 API 端点？

* What does `async move { ... }` do on line 134 of `foo.rs`?

* `foo.rs` 第 134 行的 `async move { ... }` 是干什么的？

* What edge cases does `CustomerOnboardingFlowImpl` handle?

* `CustomerOnboardingFlowImpl` 处理了哪些边界情况？

* Why does this code call `foo()` instead of `bar()` on line 333?

* 第 333 行这段代码为什么调用 `foo()` 而不是 `bar()`？

Using Claude Code this way is an effective onboarding workflow, improving ramp-up time and reducing load on other engineers.

这样使用 Claude Code 是一套高效的新人上手流程，能缩短熟悉周期，也减轻其他工程师的负担。

No special prompting required: ask questions directly.

不需要什么特别的提示词技巧：直接问就行。

### Let Claude interview you｜让 Claude 来访谈你

<Tip>
  For larger features, have Claude interview you first. Start with a minimal prompt and ask Claude to interview you using the `AskUserQuestion` tool.

  面对较大的功能时，先让 Claude 访谈你。用一条极简的提示词开场，要求 Claude 使用 `AskUserQuestion` 工具来访谈你。
</Tip>

Claude asks about things you might not have considered yet, including technical implementation, UI/UX, edge cases, and tradeoffs.

Claude 会问到一些你可能还没考虑过的方面，包括技术实现、UI/UX、边界情况和各种取舍。

Replace `[brief description]` with your feature before sending the prompt.

发送这条提示词前，把 `[brief description]` 换成你要做的功能。

```text wrap theme={null}
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Once the spec is complete, start a fresh session to execute it.

规格文档写完后，另开一个全新会话去执行它。

The new session has clean context focused entirely on implementation, and you have a written spec to reference.

新会话的上下文是干净的、完全聚焦于实现，而你手上还有一份成文的规格可供参考。

The most useful specs are self-contained: they name the files and interfaces involved, state what is out of scope, and end with an end-to-end verification step that proves the feature works.

最有用的规格文档是自包含的：点明涉及哪些文件和接口，声明哪些内容不在范围内，并以一个能证明功能确实可用的端到端验证步骤收尾。

Time spent making the spec precise pays off more than time spent watching the implementation.

花时间把规格写精确，比花时间盯着实现过程回报更高。

***

## Manage your session｜管理你的会话

Conversations are persistent and reversible. Use this to your advantage!

对话是持久化的，也是可回退的。要善加利用这一点！

### Course-correct early and often｜尽早且频繁地纠偏

<Tip>
  Correct Claude as soon as you notice it going off track.

  一旦发现 Claude 跑偏，立刻纠正它。
</Tip>

The best results come from tight feedback loops.

最好的结果来自紧凑的反馈闭环。

Though Claude occasionally solves problems perfectly on the first attempt, correcting it quickly generally produces better solutions faster.

尽管 Claude 偶尔能一次就完美解决问题，但及时纠正它通常能更快得到更好的方案。

* **`Esc`**: stop Claude mid-action with the `Esc` key. Context is preserved, so you can redirect.

* **`Esc`**：用 `Esc` 键在 Claude 执行到一半时叫停。上下文会被保留，因此你可以重新指路。

* **`Esc + Esc` or `/rewind`**: press `Esc` twice or run `/rewind` to open the rewind menu and restore previous conversation and code state, or summarize from a selected message.

* **`Esc + Esc` 或 `/rewind`**：连按两次 `Esc` 或运行 `/rewind` 打开回退菜单，恢复之前的对话与代码状态，或者从某条选定的消息开始做摘要。

* **`"Undo that"`**: have Claude revert its changes.

* **`"Undo that"`**：让 Claude 撤销它做的改动。

* **`/clear`**: reset context between unrelated tasks. Long sessions with irrelevant context can reduce performance.

* **`/clear`**：在互不相关的任务之间重置上下文。带着无关上下文的长会话会拖低表现。

If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches.

如果在同一个会话里，你为同一个问题纠正了 Claude 两次以上，那这份上下文已经被失败的尝试塞满了。

Run `/clear` and start fresh with a more specific prompt that incorporates what you learned.

运行 `/clear`，用一条更具体、并且吸收了你刚学到的经验的提示词重新开始。

A clean session with a better prompt almost always outperforms a long session with accumulated corrections.

一个干净会话配上更好的提示词，几乎总是胜过一个堆满纠错记录的长会话。

### Manage context aggressively｜积极主动地管理上下文

<Tip>
  Run `/clear` between unrelated tasks to reset context.

  在互不相关的任务之间运行 `/clear` 来重置上下文。
</Tip>

Claude Code automatically compacts conversation history when you approach context limits, which preserves important code and decisions while freeing space.

当接近上下文上限时，Claude Code 会自动压缩（compact）对话历史，在腾出空间的同时保留重要的代码和决策。

During long sessions, Claude's context window can fill with irrelevant conversation, file contents, and commands.

在长会话中，Claude 的上下文窗口可能被无关的对话、文件内容和命令占满。

This can reduce performance and sometimes distract Claude.

这会降低表现，有时还会把 Claude 带偏。

* Use `/clear` frequently between tasks to reset the context window entirely

* 在任务之间频繁使用 `/clear`，把上下文窗口彻底重置。

* When auto compaction triggers, Claude summarizes what matters most, including code patterns, file states, and key decisions

* 自动压缩触发时，Claude 会总结最要紧的东西，包括代码模式、文件状态和关键决策。

* For more control, run `/compact <instructions>`, like `/compact Focus on the API changes`

* 想要更强的控制力，就运行 `/compact <instructions>`，比如 `/compact Focus on the API changes`。

* To compact only part of the conversation, use `Esc + Esc` or `/rewind`, select a message checkpoint, and choose **Summarize from here** or **Summarize up to here**. The first condenses messages from that point forward while keeping earlier context intact; the second condenses earlier messages while keeping recent ones in full. See [the rewind menu's summarize options](https://code.claude.com/docs/en/checkpointing#rewind-and-summarize).

* 若只想压缩对话的一部分，用 `Esc + Esc` 或 `/rewind`，选中一个消息检查点，然后选择 **Summarize from here**（从此处往后摘要）或 **Summarize up to here**（摘要至此处）。前者把该点之后的消息压缩，同时完整保留更早的上下文；后者压缩更早的消息，完整保留较近的消息。参见[回退菜单的摘要选项](https://code.claude.com/docs/en/checkpointing#rewind-and-summarize)。

* Customize compaction behavior in CLAUDE.md with instructions like `"When compacting, always preserve the full list of modified files and any test commands"` to ensure critical context survives summarization

* 在 CLAUDE.md 里自定义压缩行为，写上类似 `"When compacting, always preserve the full list of modified files and any test commands"`（压缩时始终保留完整的修改文件清单和所有测试命令）这样的指令，确保关键上下文在摘要后依然存在。

* For quick questions that don't need to stay in context, use [`/btw`](https://code.claude.com/docs/en/interactive-mode#side-questions-with-%2Fbtw). The answer appears in a dismissible overlay and never enters conversation history, so you can check a detail without growing context.

* 对于那些不需要留在上下文里的临时小问题，用 [`/btw`](https://code.claude.com/docs/en/interactive-mode#side-questions-with-%2Fbtw)。答案会显示在一个可关闭的浮层里，永远不会进入对话历史，这样你就能查个细节而不撑大上下文。

### Use subagents for investigation｜用子智能体做调研

<Tip>
  Delegate research with `"use subagents to investigate X"`. They explore in a separate context, keeping your main conversation clean for implementation.

  用 `"use subagents to investigate X"` 把调研工作委派出去。它们在独立的上下文里探索，让你的主对话保持干净、专注于实现。
</Tip>

Since context is your fundamental constraint, subagents are one of the most powerful tools available.

既然上下文是你最根本的约束，子智能体就是最强大的工具之一。

When Claude researches a codebase it reads lots of files, all of which consume your context.

Claude 调研代码库时会读大量文件，而这些全都在消耗你的上下文。

Subagents run in separate context windows and report back summaries:

子智能体运行在各自独立的上下文窗口里，只把摘要汇报回来：

```text wrap theme={null}
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

The subagent explores the codebase, reads relevant files, and reports back with findings, all without cluttering your main conversation.

子智能体会去探索代码库、阅读相关文件、把结论汇报回来——全程都不会弄乱你的主对话。

You can also use subagents for verification after Claude implements something:

在 Claude 实现完某个东西之后，你也可以用子智能体来做验证：

```text wrap theme={null}
use a subagent to review this code for edge cases
```

### Rewind with checkpoints｜用检查点回退

<Tip>
  Every prompt you send creates a checkpoint. You can restore conversation, code, or both to any previous checkpoint.

  你发出的每一条提示词都会创建一个检查点（checkpoint）。你可以把对话、代码、或两者一起恢复到之前的任意一个检查点。
</Tip>

Claude automatically snapshots files before each change so a checkpoint can restore them.

Claude 会在每次改动前自动为文件打快照，这样检查点才能把它们还原回来。

Double-tap `Escape` or run `/rewind` to open the rewind menu.

连按两下 `Escape` 或运行 `/rewind` 打开回退菜单。

You can restore conversation only, restore code only, restore both, or summarize from a selected message.

你可以只恢复对话、只恢复代码、两者都恢复，或者从某条选定的消息开始做摘要。

See [Checkpointing](https://code.claude.com/docs/en/checkpointing) for details.

详情参见 [Checkpointing](https://code.claude.com/docs/en/checkpointing)。

Instead of carefully planning every move, you can tell Claude to try something risky.

与其小心翼翼地谋划每一步，不如直接让 Claude 去试一些有风险的做法。

If it doesn't work, rewind and try a different approach.

如果行不通，回退，换一条路再试。

Checkpoints are saved with the conversation, so you can close your terminal, resume the session later, and still rewind.

检查点是随对话一起保存的，所以你可以关掉终端，之后再恢复会话，仍然能够回退。

<Warning>
  Checkpoints only track changes made through Claude's file editing tools. Changes made through Bash commands or external processes are not captured. This isn't a replacement for git.

  检查点只跟踪通过 Claude 的文件编辑工具所做的改动。通过 Bash 命令或外部进程所做的改动不会被记录。它不能替代 git。
</Warning>

### Resume conversations｜恢复对话

<Tip>
  Name sessions with `/rename` and treat them like branches: each workstream gets its own persistent context.

  用 `/rename` 给会话命名，并把它们当成分支来对待：每条工作线都有自己独立的持久上下文。
</Tip>

Claude Code saves conversations locally, so when a task spans multiple sittings you don't have to re-explain the context.

Claude Code 会把对话保存在本地，所以当一个任务要分好几次来做时，你不必重新解释一遍上下文。

Run `claude --continue` to pick up the most recent session, or `claude --resume` to choose from a list.

运行 `claude --continue` 接着最近一次会话继续，或者用 `claude --resume` 从列表中挑选。

Give sessions descriptive names like `oauth-migration` so you can find them later.

给会话起有描述性的名字，比如 `oauth-migration`，方便日后查找。

See [Manage sessions](https://code.claude.com/docs/en/sessions) for the full set of resume, branch, and naming controls.

关于恢复、分支和命名的完整控制方式，参见 [Manage sessions](https://code.claude.com/docs/en/sessions)。

***

## Automate and scale｜自动化与规模化

Once you're effective with one Claude, multiply your output with parallel sessions, non-interactive mode, and fan-out patterns.

一旦你能把一个 Claude 用好，就可以用并行会话、非交互模式和扇出（fan-out）模式来成倍放大产出。

Everything so far assumes one human, one Claude, and one conversation.

到目前为止，所有内容都默认是一个人、一个 Claude、一段对话。

But Claude Code scales horizontally. The techniques in this section show how you can get more done.

但 Claude Code 是可以横向扩展的。本节的技巧会告诉你如何完成更多工作。

### Run non-interactive mode｜使用非交互模式

<Tip>
  Use `claude -p "prompt"` in CI, pre-commit hooks, or scripts. Add `--output-format stream-json --verbose` for streaming JSON output.

 在 CI、pre-commit hook 或脚本中使用 `claude -p "prompt"`。加上 `--output-format stream-json --verbose` 可以得到流式 JSON 输出。
</Tip>

With `claude -p "your prompt"`, you can run Claude non-interactively, without an interactive prompt.

用 `claude -p "your prompt"` 就能以非交互方式运行 Claude，不需要交互式的输入界面。

The run still creates a resumable session unless you pass `--no-session-persistence`.

除非你传入 `--no-session-persistence`，否则这次运行仍会创建一个可恢复的会话。

[Non-interactive mode](https://code.claude.com/docs/en/headless) is how you integrate Claude into CI pipelines, pre-commit hooks, or any automated workflow.

[非交互模式](https://code.claude.com/docs/en/headless)是把 Claude 集成进 CI 流水线、pre-commit hook 或任何自动化工作流的方式。

The output formats let you parse results programmatically: plain text, JSON, or streaming JSON.

它的输出格式让你可以用程序解析结果：纯文本、JSON，或流式 JSON。

```bash theme={null}
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json --verbose
```

The first command prints plain text.

第一条命令输出纯文本。

The `json` format returns a single JSON object with a `result` field.

`json` 格式返回一个带 `result` 字段的 JSON 对象。

The `stream-json` format prints one JSON object per line, starting with an init event.

`stream-json` 格式每行输出一个 JSON 对象，以一个 init 事件开头。

### Run multiple Claude sessions｜同时运行多个 Claude 会话

<Tip>
  Run multiple Claude sessions in parallel to speed up development, run isolated experiments, or start complex workflows.

  并行运行多个 Claude 会话，以加速开发、跑隔离的实验，或启动复杂的工作流。
</Tip>

Pick the parallel approach that fits how much coordination you want to do yourself:

根据你自己愿意承担多少协调工作，来挑选合适的并行方案：

* [Worktrees](https://code.claude.com/docs/en/worktrees): run separate CLI sessions in isolated git checkouts so edits don't collide

* [Worktrees](https://code.claude.com/docs/en/worktrees)：在互相隔离的 git 检出目录里跑各自独立的 CLI 会话，这样编辑之间不会冲突。

* [Desktop app](https://code.claude.com/docs/en/desktop#work-in-parallel-with-sessions): manage multiple local sessions visually, each in its own worktree

* [桌面应用](https://code.claude.com/docs/en/desktop#work-in-parallel-with-sessions)：可视化地管理多个本地会话，每个会话有自己的 worktree。

* [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web): run sessions on Anthropic-managed cloud infrastructure in isolated VMs

* [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)：在 Anthropic 托管的云基础设施上、以隔离的虚拟机运行会话。

* [Agent teams](https://code.claude.com/docs/en/agent-teams): automated coordination of multiple sessions with shared tasks, messaging, and a team lead

* [智能体团队（Agent teams）](https://code.claude.com/docs/en/agent-teams)：对多个会话进行自动化协调，具备共享任务、消息传递以及一个团队负责人。

Beyond parallelizing work, multiple sessions enable quality-focused workflows.

除了把工作并行化，多会话还能支撑以质量为导向的工作流。

A fresh context improves code review since Claude won't be biased toward code it just wrote.

全新的上下文能提升代码审查的质量，因为 Claude 不会偏袒它刚刚写出来的代码。

For example, use a Writer/Reviewer pattern:

举例来说，可以采用「作者／审查者」（Writer/Reviewer）模式：

| Session A (Writer)                                                      | Session B (Reviewer)                                                                                                                                                     |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Implement a rate limiter for our API endpoints`                        |                                                                                                                                                                          |
|                                                                         | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
| `Here's the review feedback: [Session B output]. Address these issues.` |                                                                                                                                                                          |

| 会话 A（作者）                                        | 会话 B（审查者）                                                                                       |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `为我们的 API 端点实现一个限流器`                            |                                                                                                   |
|                                                 | `审查 @src/middleware/rateLimiter.ts 里的限流器实现。找找边界情况、竞态条件，以及它与我们现有中间件模式的一致性。`                        |
| `这是审查反馈：[会话 B 的输出]。把这些问题处理掉。`                   |                                                                                                   |

You can do something similar with tests: have one Claude write tests, then another write code to pass them.

测试上也可以照此办理：让一个 Claude 写测试，再让另一个写代码去通过这些测试。

### Fan out across files｜跨文件扇出

<Tip>
  Loop through tasks calling `claude -p` for each. Use `--allowedTools` to scope permissions for batch operations.

  遍历所有任务，对每个任务调用一次 `claude -p`。用 `--allowedTools` 为批量操作限定权限范围。
</Tip>

For large migrations or analyses, you can distribute work across many parallel Claude invocations:

面对大规模迁移或分析，你可以把工作分摊给许多并行的 Claude 调用：

<Steps>
  <Step title="Generate a task list｜生成任务清单">
    Have Claude list all files that need migrating (e.g., `list all 2,000 Python files that need migrating`)

    让 Claude 列出所有需要迁移的文件（例如 `list all 2,000 Python files that need migrating`）。
  </Step>

  <Step title="Write a script to loop through the list｜写一个脚本遍历这份清单">
    ```bash theme={null}
    for file in $(cat files.txt); do
      claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
        --allowedTools "Edit,Bash(git commit *)"
    done
    ```
  </Step>

  <Step title="Test on a few files, then run at scale｜先拿几个文件试跑，再放开规模">
    Refine your prompt based on what goes wrong with the first 2-3 files, then run on the full set.

    根据头 2—3 个文件暴露出来的问题打磨提示词，然后再对全量文件运行。

    The `--allowedTools` flag restricts what Claude can do, which matters when you're running unattended.

    `--allowedTools` 参数限制了 Claude 能做什么——在无人值守运行时，这一点很重要。
  </Step>
</Steps>

You can also integrate Claude into existing data/processing pipelines:

你也可以把 Claude 集成到现有的数据／处理流水线中：

```bash theme={null}
claude -p "<your prompt>" --output-format json | your_command
```

Use `--verbose` for debugging during development, and turn it off in production.

开发调试时用 `--verbose`，上生产就把它关掉。

### Run autonomously with auto mode｜用 auto 模式自主运行

For uninterrupted execution with background safety checks, use [auto mode](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode).

如果想要不被打断、同时又有后台安全检查的执行方式，使用 [auto 模式](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode)。

A classifier model reviews commands before they run, blocking scope escalation, unknown infrastructure, and hostile-content-driven actions while letting routine work proceed without prompts.

一个分类器模型会在命令执行前进行审查，拦截越权扩大范围、未知基础设施和由恶意内容驱动的操作，同时让常规工作无需确认即可继续。

```bash theme={null}
claude --permission-mode auto -p "fix all lint errors"
```

For non-interactive runs with the `-p` flag, auto mode aborts if the classifier repeatedly blocks actions, since there is no user to fall back to.

在使用 `-p` 参数的非交互运行中，如果分类器反复拦截操作，auto 模式会直接中止，因为此时没有用户可供回退询问。

See [when auto mode falls back](https://code.claude.com/docs/en/permission-modes#when-auto-mode-falls-back) for thresholds.

具体阈值参见 [when auto mode falls back](https://code.claude.com/docs/en/permission-modes#when-auto-mode-falls-back)。

### Add an adversarial review step｜加一道对抗式审查环节

<Tip>
  Before treating a task as done, have a subagent review the diff in a fresh context and report gaps.

  在把一项任务视为完成之前，让一个子智能体在全新的上下文里审查 diff，并报告其中的缺口。
</Tip>

The longer Claude works unattended, the more an independent check matters before you count the work as done.

Claude 在无人值守下工作得越久，在你认定工作完成之前，一次独立检查就越重要。

A reviewer running in a fresh [subagent](https://code.claude.com/docs/en/sub-agents) context sees only the diff and the criteria you give it, not the reasoning that produced the change, so it evaluates the result on its own terms.

运行在全新[子智能体](https://code.claude.com/docs/en/sub-agents)上下文中的审查者，只能看到 diff 和你给它的判定标准，看不到产生这些改动的推理过程，因此它会独立地评判结果本身。

For a correctness check, run the bundled [`/code-review` skill](https://code.claude.com/docs/en/commands), which reviews the current diff for bugs in a fresh subagent and returns findings to the session.

想做正确性检查，就运行内置的 [`/code-review` 技能](https://code.claude.com/docs/en/commands)，它会在一个全新的子智能体中审查当前 diff 中的 bug，并把发现返回给会话。

To check the diff against your plan instead, write the review prompt yourself.

如果你想改为对照计划来核查 diff，那就自己写审查提示词。

Name the work to check, the plan to check it against, and what counts as a finding:

点明要检查的工作、用来对照的计划，以及什么才算是一条"发现"：

```text wrap theme={null}
Use a subagent to review the rate limiter diff against PLAN.md. Check that
every requirement is implemented, the listed edge cases have tests, and
nothing outside the task's scope changed. Report gaps, not style preferences.
```

Because the reviewer runs as a subagent, the implementing session receives the gaps directly and can fix them and re-review without you copying findings between windows.

由于审查者是以子智能体身份运行的，负责实现的那个会话会直接收到这些缺口，可以立刻修复并重新审查，不需要你在窗口之间来回复制粘贴。

For longer autonomous runs, an [agent team](https://code.claude.com/docs/en/agent-teams) can keep this loop going across many tasks while you spot-check the recorded findings.

对于更长时间的自主运行，[智能体团队](https://code.claude.com/docs/en/agent-teams)可以让这个循环跨越许多任务持续运转，而你只需抽查记录下来的发现。

<Callout>
  A reviewer prompted to find gaps will usually report some, even when the work is sound, because that is what it was asked to do.

  一个被要求去找缺口的审查者，通常总会报出一些来——即便这份工作本身没问题，因为这正是它被要求做的事。

  Chasing every finding leads to over-engineering: extra abstraction layers, defensive code, and tests for cases that can't happen.

  追着每一条发现去改，会导致过度设计：多余的抽象层、防御性代码，以及为根本不可能发生的情况写的测试。

  Tell the reviewer to flag only gaps that affect correctness or the stated requirements, and treat the rest as optional.

  告诉审查者只标记那些影响正确性或明示需求的缺口，其余的都当作可选项处理。
</Callout>

***

## Avoid common failure patterns｜避开常见的失败模式

These are common mistakes. Recognizing them early saves time:

以下是一些常见错误。及早识别它们能省下时间：

* **The kitchen sink session.** You start with one task, then ask Claude something unrelated, then go back to the first task. Context is full of irrelevant information.
  > **Fix**: `/clear` between unrelated tasks.

* **大杂烩会话。** 你先开始做一个任务，接着问了 Claude 一件不相干的事，然后又回到第一个任务。上下文里塞满了无关信息。
  > **解法**：在互不相关的任务之间用 `/clear`。

* **Correcting over and over.** Claude does something wrong, you correct it, it's still wrong, you correct again. Context is polluted with failed approaches.
  > **Fix**: After two failed corrections, `/clear` and write a better initial prompt incorporating what you learned.

* **反复纠错。** Claude 做错了，你纠正它，还是错，你再纠正。上下文被失败的尝试污染了。
  > **解法**：两次纠正都失败后，就 `/clear`，并把你学到的东西融进去，重写一条更好的初始提示词。

* **The over-specified CLAUDE.md.** If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise.
  > **Fix**: Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook.

* **过度堆砌的 CLAUDE.md。** 如果你的 CLAUDE.md 太长，Claude 会忽略掉其中一半，因为重要的规则淹没在噪声里了。
 > **解法**：狠心修剪。如果没有那条指令 Claude 本来就做得对，那就删掉它，或者把它改成一个 hook。

* **The trust-then-verify gap.** Claude produces a plausible-looking implementation that doesn't handle edge cases.
  > **Fix**: Always provide verification (tests, scripts, screenshots). If you can't verify it, don't ship it.

* **先信任、后验证的落差。** Claude 产出了一份看上去像模像样、却没处理边界情况的实现。
  > **解法**：永远提供验证手段（测试、脚本、截图）。如果你没法验证它，就别把它发出去。

* **The infinite exploration.** You ask Claude to "investigate" something without scoping it. Claude reads hundreds of files, filling the context.
  > **Fix**: Scope investigations narrowly or use subagents so the exploration doesn't consume your main context.

* **无止境的探索。** 你让 Claude 去"调查"某件事，却没有限定范围。Claude 读了几百个文件，把上下文填满了。
  > **解法**：把调查范围收窄，或者改用子智能体，这样探索就不会消耗你的主上下文。

***

## Develop your intuition｜培养你自己的直觉

The patterns in this guide aren't set in stone.

本指南里的这些模式并非一成不变。

They're starting points that work well in general, but might not be optimal for every situation.

它们是通常行之有效的起点，但未必对每种情形都是最优解。

Sometimes you *should* let context accumulate because you're deep in one complex problem and the history is valuable.

有时候你*就该*让上下文不断累积，因为你正深陷在一个复杂问题里，而这段历史本身很有价值。

Sometimes you should skip planning and let Claude figure it out because the task is exploratory.

有时候你该跳过规划、让 Claude 自己去摸索，因为这个任务本来就是探索性的。

Sometimes a vague prompt is exactly right because you want to see how Claude interprets the problem before constraining it.

有时候一条模糊的提示词恰恰正合适，因为你想先看看 Claude 会怎么理解这个问题，再去给它加约束。

Pay attention to what works.

留意什么方式管用。

When Claude produces great output, notice what you did: the prompt structure, the context you provided, the mode you were in.

当 Claude 产出很棒的结果时，回想一下你做了什么：提示词的结构、你提供的上下文、你当时所处的模式。

When Claude struggles, ask why. Was the context too noisy? The prompt too vague? The task too big for one pass?

当 Claude 卡住时，问问为什么。是上下文太嘈杂？提示词太笼统？还是这个任务大到一次做不完？

Over time, you'll develop intuition that no guide can capture.

久而久之，你会培养出任何指南都无法囊括的直觉。

You'll know when to be specific and when to be open-ended, when to plan and when to explore, when to clear context and when to let it accumulate.

你会知道何时该具体、何时该开放，何时该规划、何时该探索，何时该清空上下文、何时该任它累积。

## Related resources｜相关资源

* [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works): the agentic loop, tools, and context management

* [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)：智能体循环、工具与上下文管理。

* [Extend Claude Code](https://code.claude.com/docs/en/features-overview): skills, hooks, MCP, subagents, and plugins

* [Extend Claude Code](https://code.claude.com/docs/en/features-overview)：技能、hook、MCP、子智能体与插件。

* [Common workflows](https://code.claude.com/docs/en/common-workflows): step-by-step recipes for debugging, testing, PRs, and more

* [Common workflows](https://code.claude.com/docs/en/common-workflows)：调试、测试、PR 等场景的分步操作手册。

* [CLAUDE.md](https://code.claude.com/docs/en/memory): store project conventions and persistent context

* [CLAUDE.md](https://code.claude.com/docs/en/memory)：存放项目规范与持久上下文。
