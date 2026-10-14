# 04_Keep Claude working toward a goal_让 Claude 朝一个目标持续工作

> 原文：https://code.claude.com/docs/en/goal
> 来源：Claude Code 官方文档｜要求版本：**v2.1.139 或更高**

## 📌 本篇速览

- 📅 2026-05 中旬起（随 v2.1.139 发布）
- ⭐ ★★★★★ **必读** —— 「评估器外循环」被压缩成一条命令的官方形态。**「写出有效的条件」一节是整篇最值钱的部分**，它就是「冲刺契约」的官方模板。
- 🏷 `/goal`、completion condition、prompt-based Stop hook、small fast model、auto mode 正交组合
- 🗂 [返回专题目录](00_目录.md)

本文是 `/goal` 命令的官方文档逐句对照全译：`/goal` 设定一个完成条件（completion condition），每轮结束后由一个独立的小快模型判断条件是否成立；不成立就自动开下一轮，成立就自动清除目标——本质上是一个会话级的 prompt-based Stop hook 封装。

---

# Keep Claude working toward a goal｜让 Claude 朝一个目标持续工作

> Set a completion condition with /goal and Claude keeps working across turns until the condition is met.
>
> 用 /goal 设定一个完成条件，Claude 就会跨轮次持续工作，直到条件被满足。

> 📝 **Note**
>
> `/goal` requires Claude Code v2.1.139 or later.
>
> `/goal` 需要 Claude Code v2.1.139 或更高版本。

The `/goal` command sets a completion condition and Claude keeps working toward it without you prompting each step.

`/goal` 命令设定一个完成条件（completion condition），Claude 会朝它持续工作，不需要你每一步都发提示词催促。

After each turn, a small fast model checks whether the condition holds.

每一轮（turn）结束后，一个小而快的模型（small fast model）会检查条件是否成立。

If not, Claude starts another turn instead of returning control to you.

如果不成立，Claude 会开始新的一轮，而不是把控制权交还给你。

The goal clears automatically once the condition is met.

一旦条件被满足，目标会自动清除。

Use a goal for substantial work with a verifiable end state:

对于具有可验证终态（verifiable end state）的实质性工作，可以使用目标：

* Migrating a module to a new API until every call site compiles and tests pass

  把一个模块迁移到新 API，直到所有调用点都能编译通过且测试全绿

* Implementing a design doc until all acceptance criteria hold

  实现一份设计文档，直到所有验收标准（acceptance criteria）都成立

* Splitting a large file into focused modules until each is under a size budget

  把一个大文件拆分成职责聚焦的模块，直到每个模块都小于尺寸预算

* Working through a labeled issue backlog until the queue is empty

  逐个处理带标签的 issue 待办队列，直到队列清空

## Compare ways to keep a session running｜对比几种让会话持续运行的方式

Three approaches keep the current session running between prompts.

有三种方式可以让当前会话在两次提示词之间持续运行。

Pick based on what should start the next turn:

根据「下一轮应该由什么来触发」进行选择：

| Approach | Next turn starts when | Stops when |
| :--- | :--- | :--- |
| `/goal` | The previous turn finishes | A model confirms the condition is met |
| [`/loop`](https://code.claude.com/docs/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop) | A time interval elapses | You stop it, or Claude decides the work is done |
| [Stop hook](https://code.claude.com/docs/en/hooks-guide#prompt-based-hooks) | The previous turn finishes | Your own script or prompt decides |

| 方式 | 下一轮何时开始 | 何时停止 |
| :--- | :--- | :--- |
| `/goal` | 上一轮结束时 | 一个模型确认条件已满足 |
| [`/loop`](https://code.claude.com/docs/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop) | 一个时间间隔过去后 | 你手动停止，或 Claude 判断工作已完成 |
| [Stop hook](https://code.claude.com/docs/en/hooks-guide#prompt-based-hooks) | 上一轮结束时 | 由你自己的脚本或提示词决定 |

`/goal` and a Stop hook both fire after every turn.

`/goal` 和 Stop hook 都在每一轮结束后触发。

`/goal` is a session-scoped shortcut: you type a condition and it's active for the current session only.

`/goal` 是一个会话级（session-scoped）的快捷方式：你输入一个条件，它只对当前会话生效。

A Stop hook lives in your settings file, applies to every session in its scope, and can run a script for deterministic checks or a prompt for model-evaluated ones.

而 Stop hook 存放在你的设置文件里，对其作用域内的所有会话都生效，并且既可以运行脚本做确定性检查，也可以用提示词做由模型评估的检查。

[Auto mode](https://code.claude.com/docs/en/auto-mode-config) on its own approves tool calls within a single turn but doesn't start a new one.

[Auto mode](https://code.claude.com/docs/en/auto-mode-config) 单独使用时，只会在单轮之内自动批准工具调用，但不会开启新的一轮。

Claude stops when it judges the work done.

Claude 自己判断工作完成时就会停下。

`/goal` adds a separate evaluator that checks your condition after every turn, so completion is decided by a fresh model rather than the one doing the work.

`/goal` 增加了一个独立的评估器（evaluator），在每轮之后检查你的条件，因此「是否完成」由一个新鲜的模型来判定，而不是由正在干活的那个模型判定。

The two are complementary: auto mode removes per-tool prompts, and `/goal` removes per-turn prompts.

两者是互补关系：auto mode 消除了逐工具的审批提示，`/goal` 消除了逐轮的催促提示。

> 💡 **Tip**
>
> The approaches above keep the current session running.
>
> 上面这些方式是让当前会话持续运行。
>
> You can also schedule work that runs independent of any open session, such as nightly tests or morning triage.
>
> 你也可以调度独立于任何已打开会话之外运行的工作，例如每夜测试或清晨分诊（triage）。
>
> See [scheduling options](https://code.claude.com/docs/en/scheduled-tasks#compare-scheduling-options) for cloud routines and desktop scheduled tasks.
>
> 关于云端例程（cloud routines）和桌面端计划任务，参见[调度选项](https://code.claude.com/docs/en/scheduled-tasks#compare-scheduling-options)。

## Use `/goal`｜使用 `/goal`

One goal can be active per session.

每个会话同时只能有一个活跃目标。

The same command sets, checks, and clears it depending on the argument.

同一条命令根据参数的不同，分别用于设定、查看和清除目标。

### Set a goal｜设定目标

Run `/goal` followed by the condition you want satisfied.

运行 `/goal`，后面跟上你希望被满足的条件。

If a goal is already active, the new one replaces it.

如果已有活跃目标，新目标会替换掉它。

```text
/goal all tests in test/auth pass and the lint step is clean
```

> 🀄 上例含义：`test/auth` 目录下所有测试通过，且 lint 步骤无任何问题。

Setting a goal starts a turn immediately, with the condition itself as the directive.

设定目标会立刻开始一轮，条件本身就是指令。

You don't need to send a separate prompt.

你不需要再单独发一条提示词。

While the goal is active, a `◎ /goal active` indicator shows how long the goal has been running.

目标处于活跃状态时，会显示一个 `◎ /goal active` 指示器，展示目标已经运行了多久。

A goal doesn't change permissions.

目标不会改变权限。

In the default permission mode, Claude still asks before tool calls that your settings don't already allow, such as the test command above.

在默认权限模式下，对于你的设置尚未放行的工具调用（比如上面那条测试命令），Claude 仍然会先询问你。

To let goal turns run unattended, pair `/goal` with [auto mode](https://code.claude.com/docs/en/auto-mode-config).

要让目标驱动的轮次无人值守地运行，需要把 `/goal` 和 [auto mode](https://code.claude.com/docs/en/auto-mode-config) 搭配使用。

After each turn, the evaluator returns a short reason explaining why the condition is or isn't met.

每一轮结束后，评估器会返回一条简短的理由，解释条件为什么已满足或尚未满足。

The most recent reason appears in the status view and in the transcript so you can see what Claude is working toward next.

最近一次的理由会显示在状态视图和对话记录（transcript）中，方便你看到 Claude 接下来在朝什么方向努力。

> 📝 **Note**
>
> A goal keeps running until the condition is met or you run `/goal clear`.
>
> 目标会一直运行，直到条件被满足，或者你运行 `/goal clear`。
>
> Run `/goal` with no argument to see turns and tokens spent so far.
>
> 运行不带参数的 `/goal`，可以查看到目前为止已消耗的轮数和 token。

### Write an effective condition｜写出有效的条件

The [evaluator](#how-evaluation-works) judges your condition against what Claude has surfaced in the conversation.

[评估器](#how-evaluation-works)是根据 Claude 已经在对话中呈现（surfaced）出来的内容来判定你的条件的。

It doesn't run commands or read files independently, so write the condition as something Claude's own output can demonstrate.

它不会独立运行命令或读取文件，所以条件必须写成「Claude 自己的输出就能证明」的形式。

"All tests in `test/auth` pass" works because Claude runs the tests and the result lands in the transcript for the evaluator to read.

「`test/auth` 中所有测试通过」之所以可行，是因为 Claude 会去运行测试，其结果会落到对话记录里供评估器读取。

A condition that holds up across many turns usually has:

一个能撑过多轮考验的条件，通常具备以下要素：

* **One measurable end state**: a test result, a build exit code, a file count, an empty queue

  **一个可度量的终态**：一个测试结果、一个构建退出码、一个文件数量、一个空队列

* **A stated check**: how Claude should prove it, such as "`npm test` exits 0" or "`git status` is clean"

  **一个明示的验证方式**：Claude 应该如何证明它，例如「`npm test` 以 0 退出」或「`git status` 是干净的」

* **Constraints that matter**: anything that must not change on the way there, such as "no other test file is modified"

  **要紧的约束**：达成过程中任何不允许被改动的东西，例如「不得修改其他任何测试文件」

The condition can be up to 4,000 characters.

条件最长可达 4,000 个字符。

To bound how long a goal runs, include a turn or time clause in the condition, such as `or stop after 20 turns`.

要限制目标的运行时长，可以在条件中写入轮数或时间子句，例如 `or stop after 20 turns`（或在 20 轮后停止）。

Claude reports progress against that clause each turn and the evaluator judges it from the conversation.

Claude 每轮都会汇报针对该子句的进度，评估器则依据对话内容来判定。

### Check status｜查看状态

Run `/goal` with no arguments to see the current state.

运行不带参数的 `/goal`，即可查看当前状态。

```text
/goal
```

If a goal is active, the status shows:

如果有目标处于活跃状态，状态视图会显示：

* The condition

  条件本身

* How long it has been running

  它已经运行了多久

* How many turns have been evaluated

  已经评估了多少轮

* The current token spend

  当前的 token 花费

* The evaluator's most recent reason

  评估器最近一次给出的理由

The turn count and the most recent reason appear after the first evaluation has run.

轮数和最近一次的理由会在第一次评估运行之后才出现。

If no goal is active but one was achieved earlier in the session, the status shows the achieved condition along with its duration, turn count, and token spend.

如果当前没有活跃目标，但本会话早些时候有一个目标已达成，状态视图会显示那个已达成的条件，以及它的持续时长、轮数和 token 花费。

### Clear a goal｜清除目标

Run `/goal clear` to remove an active goal before its condition is met.

运行 `/goal clear` 可以在条件被满足之前移除一个活跃目标。

```text
/goal clear
```

Claude prints `Goal cleared:` followed by the condition to confirm, or `No goal set` if nothing was active.

Claude 会打印 `Goal cleared:` 并跟上该条件以作确认；如果没有活跃目标，则打印 `No goal set`。

`stop`, `off`, `reset`, `none`, and `cancel` are accepted as aliases for `clear`.

`stop`、`off`、`reset`、`none` 和 `cancel` 都被接受为 `clear` 的别名。

Running `/clear` to start a new conversation also removes any active goal.

运行 `/clear` 开启新对话时，也会一并移除任何活跃目标。

### Resume with an active goal｜带着活跃目标恢复会话

A goal that was still active when a session ended is restored when you resume that session with `--resume` or `--continue`.

会话结束时仍处于活跃状态的目标，会在你用 `--resume` 或 `--continue` 恢复该会话时被一并恢复。

The condition carries over, but the turn count, timer, and token-spend baseline all reset on resume.

条件会延续下来，但轮数、计时器和 token 花费基线在恢复时会全部重置。

A goal that was already achieved or cleared is not restored.

已经达成或已被清除的目标不会被恢复。

### Run non-interactively｜非交互式运行

`/goal` works in [non-interactive mode](https://code.claude.com/docs/en/headless), in the [desktop app](https://code.claude.com/docs/en/desktop), and through [Remote Control](https://code.claude.com/docs/en/remote-control).

`/goal` 可以在[非交互模式](https://code.claude.com/docs/en/headless)、[桌面应用](https://code.claude.com/docs/en/desktop)以及 [Remote Control](https://code.claude.com/docs/en/remote-control) 中使用。

Setting a goal with `-p` runs the loop to completion in a single invocation:

用 `-p` 设定目标，会在单次调用中把整个循环跑到完成：

```bash
claude -p "/goal CHANGELOG.md has an entry for every PR merged this week"
```

> 🀄 上例含义：以非交互方式设定目标「CHANGELOG.md 中包含本周合并的每一个 PR 的条目」，命令会一直运行到条件满足。

With the default text output, nothing prints until the condition is met, so a goal that runs many turns can look stuck.

在默认的文本输出模式下，条件满足之前不会打印任何内容，因此一个跑了很多轮的目标看起来可能像是卡住了。

Add `--output-format stream-json --verbose` to emit each message as the loop runs.

加上 `--output-format stream-json --verbose`，就能在循环运行过程中逐条输出每条消息。

Interrupt the process with Ctrl+C to stop a non-interactive goal before the condition is met.

用 Ctrl+C 中断进程，即可在条件满足之前停止一个非交互式目标。

## How evaluation works｜评估如何工作

`/goal` is a wrapper around a session-scoped [prompt-based Stop hook](https://code.claude.com/docs/en/hooks#prompt-based-hooks).

`/goal` 本质上是对一个会话级[基于提示词的 Stop hook](https://code.claude.com/docs/en/hooks#prompt-based-hooks)（prompt-based Stop hook）的封装。

Each time Claude finishes a turn, Claude Code sends the condition and the conversation so far to your configured [small fast model](https://code.claude.com/docs/en/model-config), which defaults to Haiku on the Claude API; on a third-party provider, check your [provider page](https://code.claude.com/docs/en/third-party-integrations) for the platform's default.

每当 Claude 结束一轮，Claude Code 就把条件和到目前为止的对话发送给你配置的[小快模型](https://code.claude.com/docs/en/model-config)——在 Claude API 上默认是 Haiku；如果用的是第三方提供商，请查阅你的[提供商页面](https://code.claude.com/docs/en/third-party-integrations)了解该平台的默认值。

The model answers yes or no and gives a short reason.

该模型回答「是」或「否」，并给出一条简短理由。

* **No**: Claude keeps working and takes the reason as guidance for the next turn.

  **否**：Claude 继续工作，并把这条理由当作下一轮的指引。

* **Yes**: Claude Code clears the goal and records an achieved entry in the transcript.

  **是**：Claude Code 清除目标，并在对话记录中写入一条「已达成」条目。

To evaluate on a different model, set [`ANTHROPIC_DEFAULT_HAIKU_MODEL`](https://code.claude.com/docs/en/model-config#environment-variables).

要用别的模型做评估，可以设置 [`ANTHROPIC_DEFAULT_HAIKU_MODEL`](https://code.claude.com/docs/en/model-config#environment-variables)。

> ⚠️ **Warning**
>
> Claude Code reads `ANTHROPIC_DEFAULT_HAIKU_MODEL` everywhere it uses the small fast model, not only for `/goal` evaluation.
>
> Claude Code 在所有用到小快模型的地方都会读取 `ANTHROPIC_DEFAULT_HAIKU_MODEL`，不只是 `/goal` 评估。
>
> When you set it, Claude Code also resolves the [`haiku` alias](https://code.claude.com/docs/en/model-config#model-aliases) to that model and runs [background functionality](https://code.claude.com/docs/en/costs#background-token-usage), such as conversation summarization, on it.
>
> 一旦你设置了它，Claude Code 也会把 [`haiku` 别名](https://code.claude.com/docs/en/model-config#model-aliases)解析到该模型，并在其上运行[后台功能](https://code.claude.com/docs/en/costs#background-token-usage)，例如对话摘要。

The evaluator runs on whichever provider your session is configured for.

评估器运行在你的会话所配置的那个提供商上。

It does not call tools, so it can only judge what Claude has already surfaced in the conversation.

它不会调用工具，因此只能判定 Claude 已经在对话中呈现出来的内容。

> 📝 **Note**
>
> Evaluation tokens are billed on the small fast model configured for your provider and are typically negligible compared to main-turn spend.
>
> 评估消耗的 token 按你的提供商所配置的小快模型计费，与主轮次的花费相比通常可以忽略不计。

## Requirements｜使用要求

`/goal` runs only in workspaces where you have accepted the trust dialog, because the evaluator is part of the hooks system.

`/goal` 只在你已经接受过信任对话框（trust dialog）的工作区中运行，因为评估器是 hooks 系统的一部分。

`/goal` is also unavailable when [`disableAllHooks`](https://code.claude.com/docs/en/hooks#disable-or-remove-hooks) is set at any settings level or when [`allowManagedHooksOnly`](https://code.claude.com/docs/en/settings#hook-configuration) is set in managed settings.

当任意设置层级设置了 [`disableAllHooks`](https://code.claude.com/docs/en/hooks#disable-or-remove-hooks)，或者受管设置（managed settings）中设置了 [`allowManagedHooksOnly`](https://code.claude.com/docs/en/settings#hook-configuration) 时，`/goal` 同样不可用。

In each case, the command tells you why instead of silently doing nothing.

在上述任一情况下，该命令都会告诉你原因，而不是默不作声地什么都不做。

## See also｜另请参阅

* [Run a prompt repeatedly with `/loop`](https://code.claude.com/docs/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop): re-run on a time interval instead of until a condition holds

  [用 `/loop` 反复运行一条提示词](https://code.claude.com/docs/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop)：按时间间隔重复运行，而不是运行到条件成立为止

* [Prompt-based hooks](https://code.claude.com/docs/en/hooks-guide#prompt-based-hooks): write your own Stop hook when you need custom evaluation logic

  [基于提示词的 hooks](https://code.claude.com/docs/en/hooks-guide#prompt-based-hooks)：需要自定义评估逻辑时，自己写一个 Stop hook

* [Auto mode](https://code.claude.com/docs/en/auto-mode-config): approve tool calls automatically so each goal turn runs unattended

  [Auto mode](https://code.claude.com/docs/en/auto-mode-config)：自动批准工具调用，让每个目标轮次都无人值守地运行

* [Scheduling comparison](https://code.claude.com/docs/en/scheduled-tasks#compare-scheduling-options): run work on a schedule independent of any open session

  [调度方式对比](https://code.claude.com/docs/en/scheduled-tasks#compare-scheduling-options)：按计划运行工作，独立于任何已打开的会话
