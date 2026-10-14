# B17_How and when to use subagents in Claude Code_Claude Code 子智能体：怎么用、什么时候用

> 原文：https://claude.com/blog/subagents-in-claude-code
> 来源：Anthropic Claude Blog（分类：Agents ｜ 产品：Claude Code）｜发布日期：2026-04-07
> 原文存档：[Markdown](原文/B17_subagents-in-claude-code_原文.md)

## 📌 本篇速览

- 📅 2026-04-07　｜　⏱ 原文约 3000 词（逐句精读约 40 分钟）
- 🏷 subagent、上下文隔离、并行、fresh perspective、custom subagent、CLAUDE.md、skills、hooks、agent teams
- 🗂 [返回目录](00_目录与阅读进度.md)

官方最完整的 subagent 使用指南。**定义**：subagent 是有独立上下文窗口的隔离 Claude 实例，接任务→干活→只交回结果，像「浏览器标签页」。**五个该用的信号**：研究型任务（要读几十个文件）、多个无依赖的独立任务（并行）、需要无偏见视角（不继承主对话假设）、提交前独立验证（防过拟合测试）、流水线分阶段（每阶段专注）。经验阈值：**探索 ≥10 个文件或 ≥3 块独立工作 → 用 subagent**。**四层递进的触发方式**：对话直呼 → custom subagent（markdown 定义的常驻专家，靠 description 自动路由）→ CLAUDE.md（团队级策略）→ hooks（事件自动化）；建议从对话开始、模式清晰后再自动化。**五个不该用的场景**：强顺序依赖、同文件并行编辑、小任务、专家 Agent 定义太多（自动委派会变得不可靠）、需要 Agent 互相通信（subagent 只能向主对话汇报，互通要用 agent teams）。

---

Claude Code handles complex, multi-step projects well, but long sessions accumulate weight.

Claude Code 很擅长处理复杂的多步项目，但长会话会不断累积「重量」。

Every file read, every tangent explored, every half-finished thought stays in the context window, slowing responses and driving up token costs.

每一次文件读取、每一条探索过的岔路、每一个没想完的念头，都留在上下文窗口里，拖慢响应速度、推高 token 成本。

Consider building a new feature in a large TypeScript monorepo.

设想在一个大型 TypeScript monorepo 里开发一个新功能。

The main work is the implementation, but side tasks keep appearing: trace how an existing service handles auth, find the shared util for date formatting, check whether the design system already has a component close to what you need.

主线工作是实现功能，但支线任务不断冒出来：追踪某个现有服务怎么处理鉴权、找日期格式化的公共工具函数、查设计系统里是不是已经有一个接近你需要的组件。

None of these need the full project context, and running them inside the main session adds noise.

这些支线没有一个需要完整的项目上下文，而在主会话里跑它们只会增加噪音。

What if you could run them in parallel?

如果能把它们并行跑掉呢？

Enter subagents.

这就是子智能体（subagent）登场的地方。

A subagent is an isolated Claude instance with its own context window.

子智能体是一个隔离的 Claude 实例，拥有自己独立的上下文窗口。

It takes a task, does the work, and returns only the result.

它接下一个任务，完成工作，然后**只**把结果交回来。

Think of subagents as the browser tabs of a Claude Code session: a place to chase a tangent without losing the main thread.

可以把子智能体想成 Claude Code 会话里的浏览器标签页：一个可以去追岔路、又不会丢掉主线的地方。

In this article, we discuss when it makes sense to use subagents, how to invoke them, and when the overhead isn't worth it.

本文讨论什么时候用子智能体是合理的、怎么调用它们，以及什么时候这份开销不值得。

## What is a subagent?

## 什么是子智能体？

Subagents are self-contained agents that operate with their own context windows.

子智能体是自成一体的智能体，运行在自己的上下文窗口里。

When Claude spawns a subagent, that assistant works independently to read files, explore code, or make changes.

当 Claude 派生出一个子智能体时，它会独立工作：读文件、探索代码或做修改。

When it completes its task, the subagent returns only the relevant results to the main conversation.

任务完成后，子智能体只把相关结果返回给主对话。

Each subagent starts fresh, unburdened by the history of the conversation or invoked skills.

每个子智能体都是全新起步，不背负主对话的历史，也不背负已加载的 skills。

Multiple subagents can run in parallel, and each can have different permissions: a research subagent might have read-only access, while an implementation subagent gets full editing capabilities.

多个子智能体可以并行运行，而且每个可以有不同权限：研究型子智能体可能只有只读权限，实现型子智能体则拥有完整编辑能力。

Claude Code includes several built-in subagent types, including:

Claude Code 内置了若干子智能体类型，包括：

- **General-purpose agents** for complex multi-step tasks

- **通用智能体（General-purpose）**：处理复杂的多步任务

- **Plan agents** that research codebases before presenting implementation strategies

- **规划智能体（Plan）**：在给出实现策略前先调研代码库

- **Explore agents** optimized for fast, read-only code search

- **探索智能体（Explore）**：为快速、只读的代码检索优化

Claude Code often spawns subagents on its own to handle assigned tasks.

Claude Code 经常会自己派生子智能体来处理分配到的任务。

It's also possible to direct that behavior explicitly and to define reusable specialists that Claude delegates to automatically.

你也可以显式引导这种行为，并定义可复用的「专家」，让 Claude 自动向它们委派任务。

Knowing when to reach for subagents is what makes the feature useful.

知道**什么时候**该伸手用子智能体，才是让这个功能真正有用的关键。

## When should you use subagents?

## 什么时候该用子智能体？

Certain categories of work benefit clearly from subagent delegation.

某些类别的工作能明显从子智能体委派中获益。

Learning to recognize them makes the feature far more effective.

学会识别这些类别，会让这个功能的效果大幅提升。

### Research-heavy tasks

### 研究密集型任务

When understanding how something works is a prerequisite to changing it, a subagent can explore the codebase and return a summary rather than dumping dozens of files into the conversation.

当「理解某个东西怎么工作」是「改它」的前提时，子智能体可以去探索代码库并返回一份摘要，而不是把几十个文件倾倒进对话里。

**The signal:** Gathering context requires reading dozens of files.

**信号：**收集上下文需要读几十个文件。

**The benefit:** The main conversation stays clean, and synthesized findings arrive instead of raw content.

**收益：**主对话保持干净，到手的是综合过的结论而不是原始内容。

### Multiple independent tasks

### 多个相互独立的任务

When fixing errors across several files, updating patterns in multiple components, or making changes that don't depend on each other, parallel subagents complete the task faster.

当要跨多个文件修错误、在多个组件里更新同一模式、或做彼此不依赖的修改时，并行子智能体能更快完成任务。

**The signal:** Sub-tasks have no dependencies between them.

**信号：**子任务之间没有依赖。

**The benefit:** Three subagents working simultaneously generally finish the task in less time.

**收益：**三个子智能体同时开工，通常用更少的时间完成任务。

### Fresh perspective needed

### 需要全新视角

When an unbiased review of an implementation is the goal, a subagent provides a clean slate because it doesn't inherit the assumptions, context, or blind spots from the primary conversation.

当目标是对某个实现做无偏见评审时，子智能体提供了一块白板——它不继承主对话的假设、上下文或盲区。

**The signal:** Verification is needed without conversation history influencing the analysis.

**信号：**需要验证，且不希望对话历史影响分析。

**The benefit:** Cleaner, more objective feedback.

**收益：**更干净、更客观的反馈。

**Pro-tip:** The /clear command also resets context and conversation history, providing a similarly unbiased slate, but at the cost of losing that history entirely. A subagent achieves the same fresh perspective while the main conversation stays intact.

**技巧：**/clear 命令也能重置上下文和历史、获得类似的无偏白板，但代价是历史彻底丢失。子智能体能实现同样的全新视角，而主对话完好无损。

### Verification before committing

### 提交前的验证

Before finalizing changes, an independent subagent can verify the implementation isn't overfitting to tests or missing edge cases.

在最终确定改动之前，独立的子智能体可以验证实现有没有过拟合测试、有没有漏掉边界情况。

**The signal:** A second opinion is warranted before committing code.

**信号：**提交代码前值得要一份第二意见。

**The benefit:** Catches issues that familiarity with the code might obscure.

**收益：**抓住那些「对代码太熟」反而看不见的问题。

### Pipeline workflows

### 流水线工作流

When a task has distinct phases (i.e., design, then implement, then test), each stage benefits from focused attention.

当任务有清晰的阶段划分（设计→实现→测试）时，每个阶段都能从专注中获益。

**The signal:** Sequential stages with clear handoffs.

**信号：**顺序阶段之间有清晰的交接。

**The benefit:** Each subagent concentrates on its phase, without context from other stages creating noise.

**收益：**每个子智能体专注自己的阶段，其他阶段的上下文不会制造噪音。

**Pro-tip:** When a task requires exploring ten or more files, or involves three or more independent pieces of work, that's a strong signal to direct Claude toward subagents.

**技巧：**当任务需要探索 10 个以上文件、或包含 3 块以上独立工作时，就是引导 Claude 使用子智能体的强信号。

## How to direct subagent usage

## 如何引导子智能体的使用

Several methods exist for invoking subagents, ranging from simple conversation to automated workflows.

调用子智能体有多种方式，从简单对话到自动化工作流不等。

The right starting point depends on the workflow, and sophistication can be layered on as patterns emerge.

正确的起点取决于你的工作流；随着模式逐渐清晰，可以逐层叠加更复杂的机制。

### Conversational invocation

### 对话式调用

The most flexible approach is simply asking Claude to use subagents in conversation.

最灵活的方式，就是在对话里直接让 Claude 使用子智能体。

This works across all Claude Code interfaces: terminal, VS Code, JetBrains, the web, and desktop applications.

这在所有 Claude Code 界面都适用：终端、VS Code、JetBrains、网页版和桌面应用。

Natural language patterns that reliably invoke subagents include:

能可靠触发子智能体的自然语言说法包括：

- "Use a subagent to explore how authentication works in this codebase"

- 「用一个子智能体去探索这个代码库里鉴权是怎么工作的」

- "Have a separate agent review this code for security issues"

- 「让一个单独的智能体评审这段代码的安全问题」

- "Research this in parallel. Check the API routes, database models, and frontend components simultaneously"

- 「并行调研这个。同时检查 API 路由、数据库模型和前端组件」

- "Spin up subagents to fix these TypeScript errors across the different packages"

- 「起几个子智能体，把这些 TypeScript 错误在各个包里都修掉」

Being explicit matters.

明确表达很重要。

Specify the scope, request parallel execution when tasks are independent, and describe the desired output.

指明范围；任务相互独立时明确要求并行执行；描述你想要的输出。

Here's an effective prompt structure:

一个有效的提示词结构如下：

```
Use subagents to explore this codebase in parallel:

1. Find all API endpoints and summarize their purposes
2. Identify the database schema and relationships
3. Map out the authentication flow

Return a summary of each, not the full file contents.
```

```
用子智能体并行探索这个代码库：

1. 找出所有 API 端点并总结各自用途
2. 识别数据库 schema 和表间关系
3. 画出鉴权流程

每项返回摘要，不要返回完整文件内容。
```

This prompt works because it clearly defines three independent tasks, explicitly requests parallel execution, and specifies the output format.

这个提示词有效，是因为它清晰定义了三个独立任务、显式要求并行执行，并指定了输出格式。

Claude understands the intent and spawns appropriate subagents.

Claude 理解意图后，会派生相应的子智能体。

Tips for effective conversational invocation include:

有效的对话式调用技巧包括：

- **Scope tasks clearly.** "Explore how payments work" beats "explore everything."

- **把任务范围划清楚。**「探索支付是怎么工作的」好过「把所有东西都探索一遍」。

- **Request parallelization explicitly.** Say "these can run in parallel" or "work on all three simultaneously."

- **显式要求并行。**说「这些可以并行跑」或「三个同时做」。

- **Specify what should be returned.** Summaries, specific findings, or recommendations. Naming the output format helps Claude deliver it.

- **指定应该返回什么。**摘要、具体发现，还是建议。点名输出格式有助于 Claude 交付。

- **Ask for fresh context when unbiased analysis matters.** "Use a subagent that does not see our previous discussion" ensures clean evaluation.

- **需要无偏分析时，要求全新上下文。**「用一个看不到我们之前讨论的子智能体」能确保评估干净。

**Pro-tip:** When a subagent is taking a while, Ctrl+B sends it to the background. The conversation can continue while it runs, and results surface automatically when it finishes. The /tasks command shows anything running in the background.

**技巧：**子智能体跑得久时，Ctrl+B 可以把它送到后台。它运行期间对话可以继续，完成后结果自动浮现。/tasks 命令能查看所有后台任务。

### Custom subagents

### 自定义子智能体

When the same kind of subagent keeps getting requested (a security reviewer, a test writer, a docs proofreader), it can be defined once as a custom subagent.

当同一类子智能体被反复请求时（安全评审员、测试编写者、文档校对员），可以把它一次性定义为自定义子智能体。

Claude then delegates to it automatically whenever a task matches its description, no prompting required.

之后只要任务匹配它的描述，Claude 就会自动向它委派，无需再提示。

Custom subagents live as markdown files in `.claude/agents/` (project-level, shared with the team) or `~/.claude/agents/` (user-level, available across all projects).

自定义子智能体以 markdown 文件的形式存放在 `.claude/agents/`（项目级，与团队共享）或 `~/.claude/agents/`（用户级，跨所有项目可用）。

Each one gets its own system prompt, tool permissions, and optionally its own model.

每一个都有自己的系统提示词、工具权限，还可以选配自己的模型。

The easiest way to create one is the /agents command, which walks through setup interactively and can generate a first draft from a description.

创建它最简单的方式是 /agents 命令——交互式引导配置，还能根据一段描述生成初稿。

The file can also be written by hand, for example:

文件也可以手写，例如：

```
---
name: security-reviewer
description: Reviews code changes for security vulnerabilities,
  injection risks, auth issues, and sensitive data exposure.
  Use proactively before commits touching auth, payments, or user data.
tools: Read, Grep, Glob
model: sonnet
---

You are a security-focused code reviewer. Analyze the provided
changes for:
- SQL injection, XSS, and command injection risks
- Authentication and authorization gaps
- Sensitive data in logs, errors, or responses
- Insecure dependencies or configurations

Return a prioritized list of findings with file:line references
and a recommended fix for each. Be critical. If you find nothing,
say so explicitly rather than inventing issues.
```

（配置示例：name 安全评审员；description 写明「评审代码改动中的安全漏洞、注入风险、鉴权问题和敏感数据暴露，在涉及鉴权/支付/用户数据的提交前主动使用」；tools 限定 Read/Grep/Glob 只读三件套；model 选 sonnet。系统提示词要求按优先级返回带 file:line 引用的发现清单，一无所获时要明说，而不是编造问题。）

With this in place, Claude routes matching work to the subagent automatically.

有了这份配置，Claude 会把匹配的工作自动路由给这个子智能体。

It can also be invoked by name: "Have the security-reviewer look at the staged changes."

也可以点名调用：「让 security-reviewer 看看暂存区的改动。」

Custom subagents work best when:

自定义子智能体最适合以下情况：

- A specialist should be available for Claude to delegate to automatically when a task matches

- 希望有一个专家常备着，任务匹配时 Claude 自动委派

- The work benefits from a tightly scoped system prompt and restricted tools

- 这项工作能从收紧范围的系统提示词和受限工具中获益

- The configuration should be shared across a team or reused across projects

- 这份配置需要团队共享或跨项目复用

**Pro-tip:** The description field is what Claude uses to decide when to delegate. Be specific about the trigger conditions, not just the capability. "Reviews code for security issues before commits" routes better than "security expert."

**技巧：**description 字段是 Claude 决定何时委派的依据。要写清**触发条件**，而不只是能力。「在提交前评审代码安全问题」比「安全专家」路由得更准。

For the full configuration reference, including permission modes and how project and user subagents interact, see our Claude Code subagents docs.

完整配置参考（包括权限模式、项目级与用户级子智能体如何交互）见 [Claude Code subagents 文档](https://code.claude.com/docs/en/sub-agents)。

### CLAUDE.md instructions

### CLAUDE.md 指令

Custom subagents define who the specialists are.

自定义子智能体定义的是「专家是谁」。

CLAUDE.md files define the rules for when Claude should reach for them.

CLAUDE.md 文件定义的是「Claude 什么时候该去找他们」的规则。

If every code review should go through a read-only subagent, or every architecture question should trigger a research pass first, CLAUDE.md is where that policy lives.

如果每次代码评审都该走只读子智能体、每个架构问题都该先触发一轮调研，那这条策略就该写在 CLAUDE.md 里。

Claude reads it at the start of every conversation, so the behavior stays consistent across sessions and teammates without anyone needing to remember to ask.

Claude 在每次对话开始时都会读它，所以这种行为在跨会话、跨团队成员之间保持一致，不需要任何人记得去提。

CLAUDE.md is a good fit for subagent instructions when:

以下情况适合把子智能体指令放进 CLAUDE.md：

- Code reviews should always use read-only subagents

- 代码评审应当总是使用只读子智能体

- The project has specific research patterns Claude should follow

- 项目有 Claude 应遵循的特定调研模式

- Consistent behavior is needed across team members and sessions

- 需要跨成员、跨会话的一致行为

Here's an example of a simple CLAUDE.md file that triggers a subagent given specific conditions:

下面是一个简单示例——在特定条件下触发子智能体的 CLAUDE.md：

```
## Code review standards

When asked to review code, ALWAYS use a subagent with READ-ONLY access
(Glob, Grep, Read only). The review should ALWAYS check for:
- Security vulnerabilities
- Performance issues
- Adherence to project patterns in /docs/architecture.md

Return findings as a prioritized list with file:line references.
```

（示例：被要求评审代码时，永远用只读权限的子智能体（仅 Glob/Grep/Read）；评审永远检查安全漏洞、性能问题、是否符合 /docs/architecture.md 的项目模式；发现按优先级返回并带 file:line 引用。）

With the above CLAUDE.md file, every code review request automatically uses the defined pattern, eliminating the need to specify it each time.

有了上面这份 CLAUDE.md，每次代码评审请求都会自动套用既定模式，不必每次重新说明。

### Skills

### Skills

For complex multi-step workflows that run repeatedly, skills provide a reusable interface.

对于反复运行的复杂多步工作流，skills 提供了一个可复用的接口。

Define a skill once in .claude/skills/, then invoke it with /skill-name or let Claude load it automatically when a task matches its description.

在 .claude/skills/ 里定义一次 skill，之后用 /skill-name 调用，或让 Claude 在任务匹配其描述时自动加载。

Skills differ from CLAUDE.md files in scope.

skills 和 CLAUDE.md 的差别在作用范围。

CLAUDE.md files are always loaded and shapes every interaction.

CLAUDE.md 始终被加载，塑造每一次交互。

A skill is loaded on demand, either because it was invoked explicitly or because Claude matched the current task to the skill's description field.

skill 则是按需加载——要么被显式调用，要么 Claude 把当前任务匹配到了它的 description 字段。

That makes skills the right place for workflows that should be available but not applied to every prompt.

这让 skills 成为「应当随取随用、但不必套在每个提示词上」的工作流的正确归宿。

Skills fit well when:

以下情况适合用 skills：

- Certain actions get run regularly

- 某些操作会被定期执行

- Different team members need access to the same complex operation

- 不同团队成员需要使用同一套复杂操作

- Standardizing how certain tasks are performed across the team matters

- 需要在团队内标准化某些任务的执行方式

Here's an example of a deep-review skill for comprehensive code review:

下面是一个用于全面代码评审的 deep-review skill 示例：

```
# .claude/skills/deep-review/SKILL.md

---
name: deep-review
description: Comprehensive code review that checks security,
  performance, and style in parallel. Use when reviewing staged
  changes before a commit or PR.
---

Run three parallel subagent reviews on the staged changes:

1. Security review - check for vulnerabilities, injection risks,
   authentication issues, and sensitive data exposure
2. Performance review - check for N+1 queries, unnecessary iterations,
   memory leaks, and blocking operations
3. Style review - check for consistency with project patterns
   documented in /docs/style-guide.md

Synthesize findings into a single summary with priority-ranked issues.
Each issue should include the file, line number, and recommended fix.
```

（示例：/deep-review 对暂存改动并行跑三个子智能体评审——安全（漏洞/注入/鉴权/敏感数据）、性能（N+1 查询/多余迭代/内存泄漏/阻塞操作）、风格（是否符合风格指南），最后综合成一份按优先级排序、带文件行号和修复建议的摘要。）

In the code snippet above, /deep-review triggers a three-part subagent analysis on demand.

在上面的代码片段中，/deep-review 按需触发三路子智能体分析。

Because the description mentions reviewing staged changes before commits, Claude can also reach for this skill automatically when that context comes up.

由于 description 提到「提交前评审暂存改动」，当这种上下文出现时，Claude 也会自动取用这个 skill。

A skill is a directory, not a single file.

skill 是一个目录，不是单个文件。

Alongside `SKILL.md`, it can hold templates Claude fills in, example outputs showing the expected format, or scripts Claude executes as part of the workflow.

除了 `SKILL.md`，它还能装 Claude 用来填空的模板、展示预期格式的示例输出，以及工作流中 Claude 要执行的脚本。

The legacy `.claude/commands/` format was a single flat file, so everything had to live in the prompt itself.

旧的 `.claude/commands/` 格式是单个扁平文件，所有东西都只能挤在提示词本身里。

### Hooks

### Hooks

Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code's lifecycle.

Hooks 是用户定义的 shell 命令、HTTP 端点或 LLM 提示词，在 Claude Code 生命周期的特定节点自动执行。

Hooks can automate subagent workflows based on events.

Hooks 能基于事件把子智能体工作流自动化。

Hooks trigger on specific actions and run subagent tasks without manual invocation.

Hooks 在特定动作上触发，无需手动调用即可运行子智能体任务。

Hooks are the right tool when:

以下情况适合用 hooks：

- Every commit should be reviewed automatically before it's created

- 每次提交在创建前都应自动评审

- Security checks should run without anyone remembering to ask

- 安全检查应该在没人记得去要求的情况下照样运行

- CI-like quality gates belong in the local development process

- 类似 CI 的质量闸门应该内置到本地开发流程

Here is an example of a Stop hook that blocks Claude from ending its turn until a test is passed:

下面是一个 Stop hook 示例——在测试通过之前，阻止 Claude 结束它的回合：

```
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-tests.sh"
          }
        ]
      }
    ]
  }
}
```

And the script at `.claude/hooks/check-tests.sh`:

以及 `.claude/hooks/check-tests.sh` 里的脚本：

```
#!/bin/bash
INPUT=$(cat)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')

# Don't loop forever — if we already blocked once this turn, let it through
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
  exit 0
fi

if ! npm test --silent > /dev/null 2>&1; then
  jq -n '{
    decision: "block",
    reason: "Tests are failing. Run `npm test` to see the failures and fix them before finishing."
  }'
  exit 0
fi

exit 0
```

（脚本逻辑：Stop 事件触发时跑测试套件；测试失败则输出 `decision: "block"` + 原因，Claude Code 不让 Claude 停下，并把原因作为继续工作的指令喂回对话；`stop_hook_active` 守卫防止无限循环——如果 Claude 已经因为上一次 block 在继续了，就放行。）

When Claude finishes its turn, the Stop event fires.

Claude 结束回合时，Stop 事件被触发。

The script runs the test suite—if tests fail, it returns JSON with `decision: "block"` and a `reason`.

脚本运行测试套件——测试失败时返回带 `decision: "block"` 和 `reason` 的 JSON。

Claude Code reads that, doesn't let Claude stop, and feeds the reason back into the conversation as instruction to keep working.

Claude Code 读到后不让 Claude 停止，并把 reason 作为「继续干活」的指令喂回对话。

The `stop_hook_active` guard at the top prevents infinite loops: if Claude is already continuing because of a previous stop-hook block, the script lets it exit.

顶部的 `stop_hook_active` 守卫防止无限循环：如果 Claude 已经在因上一次 stop-hook 拦截而继续工作，脚本就放它通过。

Hooks represent the most automated approach to subagent orchestration.

Hooks 代表了子智能体编排中自动化程度最高的方式。

Conversational invocation or CLAUDE.md instructions are the better starting point; hooks come later, as workflows mature.

对话式调用或 CLAUDE.md 指令是更好的起点；hooks 留到后面、工作流成熟之后再上。

## Practical patterns for using subagents

## 子智能体的实用模式

The following patterns demonstrate subagent direction applied to common scenarios.

以下模式展示了子智能体引导在常见场景中的应用。

### Research before implementing

### 先调研，后实现

When adding a feature to unfamiliar code, delegating research to a subagent first keeps the implementation discussion informed rather than exploratory, for example:

在不熟悉的代码里加功能时，先把调研委派给子智能体，能让实现阶段的讨论有据可依，而不是边摸索边讨论。例如：

```
Before I implement user notifications, use a subagent to research:
- How are emails currently sent in this codebase?
- What notification patterns already exist?
- Where should new notification logic live based on the current architecture?

Summarize findings, then we'll plan the implementation together.
```

（示例：实现用户通知之前，用子智能体调研——现在邮件怎么发的？已有哪些通知模式？按当前架构新逻辑该放哪？总结发现后一起规划实现。）

A synthesized summary arrives instead of twenty files of raw context, and the implementation discussion starts from a solid foundation.

到手的是一份综合摘要，而不是二十个文件的原始上下文；实现讨论从坚实的基础上开始。

### Parallel modifications

### 并行修改

When the same pattern needs updating across multiple files, parallel subagents finish faster and maintain focus, for example:

当同一模式需要在多个文件里更新时，并行子智能体完成得更快、也更专注。例如：

```
Use parallel subagents to update the error handling in these files:
- src/api/users.ts
- src/api/orders.ts
- src/api/products.ts

Each should follow the pattern established in src/api/auth.ts.
Work on all three simultaneously.
```

（示例：三个文件的错误处理并行更新，各自遵循 auth.ts 里的既定模式，三个同时做。）

Three subagents working in parallel complete in roughly the time one would take.

三个并行的子智能体，大约在一个子智能体的时间里完成全部工作。

Each focuses on its file without context from the others creating confusion or inconsistency.

每个专注自己的文件，不会被其他文件的上下文搞混或搞得不一致。

### Independent review

### 独立评审

After implementing something complex, verification from a subagent that hasn't been influenced by the implementation journey catches what familiarity obscures, for example:

实现复杂功能后，让一个没被实现过程影响的子智能体来验证，能抓住「太熟悉」而看不见的问题。例如：

```
Use a fresh subagent with read-only access to review my implementation of the payment flow. It should not see our previous discussion. I want an unbiased review.

Check for: security vulnerabilities, unhandled edge cases, and error handling gaps. Be critical.
```

（示例：用一个只读权限、看不到之前讨论的全新子智能体评审支付流实现，要求无偏见、够挑剔：查安全漏洞、未处理的边界情况、错误处理缺口。）

The review subagent evaluates the code without knowing what tradeoffs were considered, what approaches were rejected, or what assumptions were made.

评审子智能体在不知道「考虑过哪些取舍、否决过哪些方案、做过哪些假设」的情况下评估代码。

This outside perspective surfaces issues the main conversation might miss.

这种局外人视角能浮现出主对话可能漏掉的问题。

### Pipeline workflow

### 流水线工作流

For multi-stage tasks, chaining subagents with explicit handoffs between phases keeps each stage focused, for example:

对多阶段任务，用显式交接把子智能体串起来，能让每个阶段保持专注。例如：

```
Let's build this feature as a pipeline:

1. First subagent: Design the API contract and write it to docs/api-spec.md
2. Second subagent: Implement the backend endpoints based on that spec
3. Third subagent: Write integration tests for the implementation

Each stage should complete before the next begins. Use the output
files as the handoff mechanism between stages.
```

（示例：三段流水线——设计 API 契约写入 spec 文件→按 spec 实现后端端点→为实现写集成测试；上一阶段完成才开始下一阶段，**用输出文件作为阶段间交接机制**。）

Using a pipeline workflow, each stage in the task receives focused context.

采用流水线工作流，任务的每个阶段都拿到聚焦的上下文。

The design subagent isn't distracted by implementation concerns, the implementation subagent works from a clean spec, and the testing subagent evaluates the result independently.

设计子智能体不被实现细节分心，实现子智能体从一份干净的 spec 出发，测试子智能体独立评估结果。

## When shouldn't you use subagents?

## 什么时候不该用子智能体？

While subagents are a useful feature, subagents carry overhead.

子智能体虽然有用，但它们是有开销的。

Each one spins up its own context, consumes tokens, and adds a layer of indirection between the developer and the work.

每一个都要起自己的上下文、消耗 token，并在开发者和工作之间加一层间接。

They're worth that cost when context isolation, parallelism, or a fresh perspective actually helps.

只有当上下文隔离、并行、或全新视角真的有帮助时，这份成本才值得。

For smaller or tightly sequential tasks, sticking to the main conversation is usually simpler, for example:

对于较小或强顺序的任务，留在主对话里通常更简单。例如：

- **Sequential, dependent work.** When step two needs the full output of step one, and step three needs both, a single session handling the chain is usually cleaner than a relay of subagents passing state through files.

- **顺序依赖的工作。**当第二步需要第一步的完整输出、第三步又需要前两步时，让单个会话处理整条链，通常比一串子智能体靠文件传状态的接力赛更干净。

- **Same-file edits.** Two subagents editing the same file in parallel is a recipe for conflict. In this scenario, keep tightly coupled changes in one context window.

- **同文件编辑。**两个子智能体并行编辑同一个文件是冲突的配方。这种场景下，把紧耦合的改动留在一个上下文窗口里。

- **Small tasks.** For a quick fix or a focused question, the overhead of delegation outweighs the benefit. Just prompt or ask in your main conversation.

- **小任务。**快速修复或聚焦提问，委派的开销大于收益。直接在主对话里问就好。

- **Too many specialist agents.** It's tempting to define a custom subagent for everything, but flooding Claude with options makes automatic delegation less reliable. Most teams settle on a handful of well-scoped agents rather than a sprawling roster.

- **专家智能体定义太多。**给每件事都定义一个自定义子智能体很有诱惑力，但选项太多会让自动委派变得不可靠。大多数团队最终落在少数几个范围清晰的智能体上，而不是一张臃肿的名册。

- **Work that needs agents to coordinate with each other.** Subagents report back to the main conversation but can't talk to one another. For tasks where subagents need to communicate, use agent teams. With agent teams, subagents coordinate across separate sessions rather than within one, which makes them heavier and more expensive.

- **需要智能体互相协调的工作。**子智能体只向主对话汇报，彼此之间不能对话。需要子智能体互相通信的任务，请用 agent teams。agent teams 中的智能体跨独立会话协调而非在一个会话内，因此更重、更贵。

The signals described earlier (i.e., needing a second opinion, a lack of dependencies between sub-tasks, and extensive research) make it clear when delegation to a subagent is worth it.

前面描述的那些信号（需要第二意见、子任务之间无依赖、大量调研）能清楚地告诉你什么时候值得委派给子智能体。

## Start conversational, automate later

## 从对话开始，之后再自动化

Subagents deliver their full value when used deliberately.

有意识地使用子智能体，才能发挥它们的全部价值。

The automatic invocation Claude provides is helpful, but knowing when to delegate research, parallelize work, and request a fresh perspective produces better results than leaving it to chance.

Claude 的自动调用固然有帮助，但知道什么时候该委派调研、并行工作、要一份全新视角，比听天由命效果更好。

When using subagents, start with conversational prompts.

使用子智能体时，从对话式提示开始。

Notice which requests keep occurring and build automation as those patterns clarify.

留意哪些请求在反复出现，随着模式清晰再构建自动化。

The goal is to make subagent delegation effortless, so your attention stays on the work that matters.

目标是让子智能体委派变得毫不费力，好让你的注意力留在真正重要的工作上。

---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| subagent | 子智能体 | 独立上下文的隔离实例，只交回结果；比作浏览器标签页 |
| context isolation | 上下文隔离 | subagent 三大价值之一（另两个：并行、全新视角） |
| fresh perspective / clean slate | 全新视角 / 白板 | 不继承主对话假设与盲区 |
| overfitting to tests | 过拟合测试 | 提交前独立验证要抓的问题 |
| pipeline workflow | 流水线工作流 | 阶段间用输出文件作交接机制 |
| conversational invocation | 对话式调用 | 四层触发方式的起点 |
| custom subagent | 自定义子智能体 | markdown 定义；description 决定自动路由 |
| description field | 描述字段 | 写触发条件而非能力；「提交前评审」优于「安全专家」 |
| CLAUDE.md | 项目记忆文件 | 定义「何时找专家」的团队策略，每次对话必加载 |
| skill | 技能 | 按需加载的工作流目录（模板/示例/脚本） |
| hook | 钩子 | 生命周期事件上的自动执行；Stop hook 可阻止模型停手 |
| layer of indirection | 一层间接 | subagent 的成本之一 |
| agent teams | 智能体团队 | subagent 互相不能通信时的升级选项；更重更贵 |
