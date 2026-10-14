# 03_cwc-long-running-agents_长时程 Claude 智能体的 Harness 原语

> 原文：https://github.com/anthropics/cwc-long-running-agents
> 来源：Anthropic 官方 GitHub（Code with Claude 2026 活动示例代码）｜性质：参考实现，官方声明**不维护、不接受贡献**

## 📌 本篇速览

- 📅 2026-05（Code with Claude 2026）　｜　📄 本篇逐句对照覆盖仓库三个核心文件：`README.md`、`claude-code-config/.claude/CLAUDE.md`（builder 系统提示）、`agents/evaluator.md`（评审子智能体提示）
- ⭐ ★★★★★ **必读，且是唯一可以直接抄代码的一篇** —— 它把 `/goal` 内部的三套机制拆出来变成你自己能装的 hook。综述里 default-FAIL 契约、证据门控、agent 自维护交接这三条，源头就是这个仓库。
- 🏷 default-FAIL contract、evidence gating、fresh-context evaluator、PROGRESS.md handoff、kill-switch、STEER.md
- 🗂 [返回专题目录](00_目录.md)　·　📖 [双语精读版（转述+提炼）](03_cwc-long-running-agents_双语精读.md)　·　🔗 [Harness 最佳实践现状综述](../02_Agent-Harness最佳实践现状综述_2026-08.md)

本仓库把 Claude Code `/goal` 命令内部的三套机制——「没证据不许说成功」的 default-FAIL 契约、独立上下文的只读评审者（fresh-context evaluator）、智能体自维护的交接文档（agent-maintained handoff）——拆成独立的 shell hook 和 subagent，任何项目 `cp -r` 就能装上；另附两个运维控制 hook（急停 + 中途转向）和进阶模式索引。

---

# README.md — Harness Primitives for Long-Running Claude Agents|README：长时程 Claude 智能体的 Harness 原语

Claude Code's built-in [`/goal`](https://code.claude.com/docs/en/goal) command gives you a generator/evaluator loop out of the box: set a completion condition and a separate fast model checks it after every turn until it's met.

Claude Code 内置的 [`/goal`](https://code.claude.com/docs/en/goal) 命令开箱即用地提供了一个「生成者/评审者」循环（generator/evaluator loop）：你设定一个完成条件（completion condition），一个独立的快速模型会在每一轮之后检查该条件，直到条件满足为止。

This repo ships the same underlying primitives as short, readable [hooks](https://code.claude.com/docs/en/hooks) and a [subagent](https://code.claude.com/docs/en/sub-agents), so you can see how each mechanism works and assemble a harness tuned to your project.

本仓库把同样的底层原语（primitive）以简短、可读的 [hook](https://code.claude.com/docs/en/hooks) 和一个[子智能体](https://code.claude.com/docs/en/sub-agents)（subagent）的形式交付出来，让你能看清每个机制是如何工作的，并组装出一套为你自己项目量身调校的 harness。

The patterns come from [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Nov 2025) and [Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps) (Mar 2026).

这些模式来自[《Effective Harnesses for Long-Running Agents》](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（2025 年 11 月）和[《Harness Design for Long-Running Application Development》](https://www.anthropic.com/engineering/harness-design-long-running-apps)（2026 年 3 月）两篇文章。

We recommend trying both the in-product features and a custom harness to see which fits your workflow.

我们建议把产品内置功能和自建 harness 两条路都试一试，看哪条更适合你的工作流。

| | In-product | Custom harness (this repo) |
|---|---|---|
| **What runs the loop** | [`/goal`](https://code.claude.com/docs/en/goal) | the [primitives below](#the-quality-loop) + a [loop you write](#running-the-loop) |
| **Who judges "done"** | a separate fast model checking your condition | your [`agents/evaluator.md`](https://github.com/anthropics/cwc-long-running-agents/blob/HEAD/claude-code-config/.claude/agents/evaluator.md) with your prompt |
| **Where it works** | Claude Code interactive, [`-p`](https://code.claude.com/docs/en/headless), Remote Control | Claude Code, headless, or [Agent SDK](https://docs.claude.com/en/docs/claude-code/sdk) |

> **中文对照表**
>
> | | 产品内置 | 自建 harness（本仓库） |
> |---|---|---|
> | **谁在跑循环** | `/goal` | 下文的原语 + 你自己写的循环 |
> | **谁判定「做完」** | 一个独立的快速模型检查你设定的条件 | 你的 `agents/evaluator.md`，用你自己写的提示词 |
> | **能跑在哪里** | Claude Code 交互式、`-p`（headless）、Remote Control | Claude Code、headless，或 Agent SDK |

Three primitives form the quality loop:

三个原语构成了质量循环（quality loop）：

- **Default-FAIL contract.** Every criterion starts `false`; the agent can't mark it passing without opening evidence first.

- **默认失败契约（Default-FAIL contract）。** 每条验收标准初始都是 `false`；智能体必须先打开证据文件，才能把它标记为通过。

- **Fresh-context evaluator.** A separate agent with no Write/Edit tools grades the work from a context window that never saw the build.

- **全新上下文评审者（Fresh-context evaluator）。** 一个没有 Write/Edit 工具的独立智能体，从一个从未见过构建过程的上下文窗口里给工作打分。

- **Agent-maintained handoff.** The agent writes its own progress notes and commits to git so the next session picks up cleanly.

- **智能体自维护交接（Agent-maintained handoff）。** 智能体自己撰写进度笔记并提交到 git，让下一次会话能干净地接手。

Two more operator-control hooks are included for when you want to watch or intervene.

此外还附带两个运维控制（operator-control）hook，供你想要观察或介入时使用。

The same patterns translate directly to `PreToolUse`/`Stop` callbacks in the [Agent SDK](https://docs.claude.com/en/docs/claude-code/sdk).

同样的模式可以直接迁移为 [Agent SDK](https://docs.claude.com/en/docs/claude-code/sdk) 中的 `PreToolUse`/`Stop` 回调。

> Built as the take-home for the Long-Running Agents station at Code with Claude 2026.

> 本仓库是 Code with Claude 2026 活动中「长时程智能体」展台的随手带走（take-home）示例。

> **These are example ingredients, not a turnkey harness.**

> **这些是示例原料，不是一套交钥匙（turnkey）的 harness。**

> Event demo; not maintained and not accepting contributions.

> 活动演示项目；不维护，也不接受贡献。

## How to use this repo|如何使用本仓库

**Read and cherry-pick.**

**阅读并按需挑选（cherry-pick）。**

Each primitive is one standalone file with no dependency on the others.

每个原语都是一个独立文件，彼此之间没有依赖。

The [quality-loop table](#the-quality-loop) below maps every one to its example here and its Agent SDK equivalent.

下方的[质量循环对照表](#the-quality-loop)把每个原语映射到它在本仓库中的示例文件，以及它在 Agent SDK 中的等价物。

Open the file, see how the mechanism works, copy what fits.

打开文件，看懂机制怎么运作，把合用的部分抄走。

**Or copy all of them as a starting point.** In your project, run `claude` and paste:

**或者把它们全部拷贝过去作为起点。** 在你的项目里运行 `claude` 并粘贴：

> Clone github.com/anthropics/cwc-long-running-agents into /tmp, copy its `claude-code-config/.claude/` directory into this project's root, make the hook scripts executable, then walk me through what each hook and the evaluator subagent does and what I'll need to adapt for this project.

> **中文译文**：把 github.com/anthropics/cwc-long-running-agents 克隆到 /tmp，把它的 `claude-code-config/.claude/` 目录拷贝到本项目根目录，给 hook 脚本加上可执行权限，然后逐个给我讲解每个 hook 和 evaluator 子智能体是干什么的，以及我需要为本项目改造哪些地方。

or do it yourself:

或者自己动手：

```bash
cp -r claude-code-config/.claude /path/to/your/project/
chmod +x /path/to/your/project/.claude/hooks/*.sh
```

Either way, this gives you all the examples wired into `.claude/` at once.

无论哪种方式，这都会把全部示例一次性接入你的 `.claude/` 目录。

Before relying on them: point `RESULTS_FILE` at your project's actual results file, adjust the evidence-file pattern in `track-read.sh`, and run `claude` from the directory that contains `.claude/` (hooks are not loaded when launching from a subdirectory).

在依赖它们之前：把 `RESULTS_FILE` 指向你项目里真实的结果文件，调整 `track-read.sh` 中的证据文件匹配模式，并且要在包含 `.claude/` 的那一层目录里运行 `claude`（从子目录启动时 hook 不会被加载）。

**If you're on the Agent SDK,** this repo is a pattern reference.

**如果你用的是 Agent SDK**，本仓库就是一份模式参考（pattern reference）。

The shell hooks here translate one-to-one to `PreToolUse`/`Stop` callbacks.

这里的 shell hook 可以一比一地翻译成 `PreToolUse`/`Stop` 回调。

To scaffold an SDK agent from inside Claude Code, install the [`agent-sdk-dev` plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/agent-sdk-dev) and ask Claude to build an agent that implements whichever of these primitives you want.

要在 Claude Code 里直接搭建一个 SDK 智能体的脚手架，可以安装 [`agent-sdk-dev` 插件](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/agent-sdk-dev)，然后让 Claude 构建一个实现了你想要的任意这些原语的智能体。

For a hand-written starting point, see the [autonomous-coding quickstart](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding) or the [agent-sdk-workshop](https://github.com/anthropics/agent-sdk-workshop) curriculum.

想要一个手写的起点，可以参考 [autonomous-coding 快速上手示例](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)或 [agent-sdk-workshop](https://github.com/anthropics/agent-sdk-workshop) 课程。

## The quality loop|质量循环

| Primitive | Claude Code example | Agent SDK equivalent | Enforcement |
|---|---|---|---|
| **Default-FAIL contract** | [`hooks/track-read.sh`](https://github.com/anthropics/cwc-long-running-agents/blob/HEAD/claude-code-config/.claude/hooks/track-read.sh) + [`hooks/verify-gate.sh`](https://github.com/anthropics/cwc-long-running-agents/blob/HEAD/claude-code-config/.claude/hooks/verify-gate.sh) | `PreToolUse` callback | hook |
| **Fresh-context evaluator** | [`agents/evaluator.md`](https://github.com/anthropics/cwc-long-running-agents/blob/HEAD/claude-code-config/.claude/agents/evaluator.md) subagent (no Write/Edit) | [`evaluator_optimizer.ipynb`](https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/evaluator_optimizer.ipynb) | you invoke it |
| **Agent-maintained handoff** | [`CLAUDE.md`](https://github.com/anthropics/cwc-long-running-agents/blob/HEAD/claude-code-config/.claude/CLAUDE.md) + [`hooks/commit-on-stop.sh`](https://github.com/anthropics/cwc-long-running-agents/blob/HEAD/claude-code-config/.claude/hooks/commit-on-stop.sh) | system prompt + `Stop` callback | convention + hook backstop |

> **中文对照表**
>
> | 原语 | Claude Code 示例 | Agent SDK 等价物 | 强制方式 |
> |---|---|---|---|
> | **默认失败契约** | `hooks/track-read.sh` + `hooks/verify-gate.sh` | `PreToolUse` 回调 | hook 强制 |
> | **全新上下文评审者** | `agents/evaluator.md` 子智能体（无 Write/Edit） | `evaluator_optimizer.ipynb` | 由你手动调用 |
> | **智能体自维护交接** | `CLAUDE.md` + `hooks/commit-on-stop.sh` | 系统提示 + `Stop` 回调 | 约定 + hook 兜底 |

### Default-FAIL contract|默认失败契约

Agents will mark a feature "passing" after a unit test or a curl when the UI is visibly broken.

即便 UI 明显是坏的，智能体也会在跑完一个单元测试或一条 curl 之后就把某个功能标成「通过」。

Asking nicely in the prompt doesn't reliably stop this.

在提示词里好言相劝并不能可靠地阻止这种行为。

The harness makes "done" structural.

harness 的做法是把「做完」变成结构性的（structural）约束。

Every feature is a row in a `test-results.json` file you create in your project:

每个功能都是你在项目里创建的 `test-results.json` 文件中的一行：

```json
{ "feature-1": { "passes": false }, "feature-2": { "passes": false } }
```

The only evidence that counts is a file matching the patterns in `track-read.sh` (screenshots, console logs, result files), and a `PreToolUse` hook denies any write to the results file unless the agent has first opened one with the Read tool.

唯一算数的证据，是匹配 `track-read.sh` 中模式的文件（截图、console 日志、结果文件）；一个 `PreToolUse` hook 会拒绝对结果文件的任何写入，除非智能体先用 Read 工具打开过其中一个证据文件。

The agent can't claim success it hasn't observed.

智能体无法宣称它没有亲眼观察到的成功。

(The shipped hook is intentionally simple; see the comments in `verify-gate.sh` for the gaps a production version would close.)

（仓库里附带的 hook 是刻意保持简单的；生产版本需要补上的缺口，见 `verify-gate.sh` 里的注释。）

### Fresh-context evaluator|全新上下文评审者

The builder shouldn't grade its own work.

构建者（builder）不应该给自己的工作打分。

After each feature, you (or your wrapper script) invoke a separate subagent (`agents/evaluator.md`) with no Write/Edit tools that reviews the diff and the screenshots from a context window that never saw the build, then returns `PASS` or `NEEDS_WORK` with specific findings.

每完成一个功能后，你（或你的 wrapper 脚本）调用一个没有 Write/Edit 工具的独立子智能体（`agents/evaluator.md`），它从一个从未见过构建过程的上下文窗口里审查 diff 和截图，然后返回 `PASS` 或 `NEEDS_WORK`，并附上具体发现（findings）。

On `NEEDS_WORK` the findings become the next builder session's starting prompt, closing the build/evaluate/rebuild loop.

当结果是 `NEEDS_WORK` 时，这些发现会成为下一次 builder 会话的开场提示词，从而闭合「构建/评审/重建」的循环。

Invoke it from your wrapper with `claude --agent evaluator -p "<review prompt>"`; what your loop does with the verdict is up to you.

在你的 wrapper 中用 `claude --agent evaluator -p "<review prompt>"` 调用它；至于你的循环拿这个裁决（verdict）做什么，由你自己决定。

### Agent-maintained handoff|智能体自维护交接

A fresh session has no memory of what the previous one did, and when a long session fills its context window Claude Code summarizes the history, which loses detail.

全新会话对上一次会话做了什么毫无记忆；而当一个长会话填满上下文窗口时，Claude Code 会对历史做摘要压缩，这会丢失细节。

So the agent maintains the handoff itself: it scopes each session to one feature, writes to a structured `PROGRESS.md` as it works and re-reads it first thing on every restart, and `git add`s and commits at meaningful checkpoints so `git log` is a second record.

所以由智能体自己维护交接：它把每次会话限定在一个功能范围内，边干活边往结构化的 `PROGRESS.md` 里写，每次重启后第一件事就是重读它，并在有意义的检查点执行 `git add` 和提交，让 `git log` 成为第二份记录。

`commit-on-stop.sh` is the backstop that catches whatever's still uncommitted at session end.

`commit-on-stop.sh` 是兜底（backstop）机制，负责在会话结束时把还没提交的东西都收进来。

This is the layer most sensitive to model capability; newer models drift less and self-scope better, so re-evaluate how much of `CLAUDE.md` you still need after each model release (see [Re-simplify on model upgrades](#going-further)).

这是对模型能力最敏感的一层；更新的模型漂移（drift）更少、自我界定范围的能力更强，所以每次模型发布后都要重新评估 `CLAUDE.md` 里还有多少内容是必要的（见[模型升级后的重新简化](#going-further)）。

A fourth core piece, a **rubric for subjective work**, isn't shipped here because it's project-specific; see [Going further](#going-further) for how to add one to the evaluator.

第四块核心组件——**针对主观性工作的评分标准（rubric）**——没有随仓库提供，因为它是项目相关的；如何给 evaluator 加上一份 rubric，见[更进一步](#going-further)。

## Running the loop|运行循环

Two ways to keep the build → evaluate → rebuild cycle going.

有两种方式让「构建 → 评审 → 重建」的循环持续运转。

`/goal` is built into Claude Code and works with or without this repo's primitives; the second path wires the contract file and your own `evaluator.md` directly into the loop.

`/goal` 内置于 Claude Code，无论有没有本仓库的原语都能用；第二条路则是把契约文件和你自己的 `evaluator.md` 直接接进循环里。

### `/goal`: built-in completion checker|`/goal`：内置的完成检查器

```
/goal every feature in PROGRESS.md is implemented, committed, and its tests pass
```

After every turn a separate fast model checks the condition and keeps the session going until it's met.

每一轮之后，一个独立的快速模型会检查该条件，并让会话持续运行，直到条件满足。

One line, no contract file or hooks.

一行命令，不需要契约文件，也不需要 hook。

Works the same in interactive Claude Code, [`claude -p`](https://code.claude.com/docs/en/headless), and Remote Control.

在交互式 Claude Code、[`claude -p`](https://code.claude.com/docs/en/headless)（headless）和 Remote Control 中的行为完全一致。

See the docs for [writing an effective condition](https://code.claude.com/docs/en/goal#write-an-effective-condition) and how `/goal` [compares to `/loop` and Stop hooks](https://code.claude.com/docs/en/goal#compare-to-other-autonomous-workflows).

关于[如何写一个有效的完成条件](https://code.claude.com/docs/en/goal#write-an-effective-condition)，以及 `/goal` [与 `/loop` 和 Stop hook 的对比](https://code.claude.com/docs/en/goal#compare-to-other-autonomous-workflows)，参见官方文档。

### Your `evaluator.md` as the gate|用你的 `evaluator.md` 当关卡

When you want the default-FAIL contract (`test-results.json` + `verify-gate`) enforcing evidence and your own evaluator prompt deciding `PASS`/`NEEDS_WORK`, the loop lives in your code.

当你想让默认失败契约（`test-results.json` + `verify-gate`）来强制证据、让你自己的 evaluator 提示词来裁决 `PASS`/`NEEDS_WORK` 时，循环就得放在你自己的代码里。

How depends on where you're running:

具体怎么做，取决于你跑在哪个平面上：

| Surface | How |
|---|---|
| **Claude Code** | custom [Stop hook](https://code.claude.com/docs/en/hooks#stop) runs the evaluator as a fresh `claude` process after each turn and blocks on anything but `PASS` |
| **Headless** ([`claude -p`](https://code.claude.com/docs/en/headless)) | wrapper script calls `claude --agent evaluator -p` between builds (example below) |
| [**Agent SDK**](https://docs.claude.com/en/docs/claude-code/sdk) | separate generator and evaluator `query()` calls; see [`evaluator_optimizer`](https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/evaluator_optimizer.ipynb) |

> **中文对照表**
>
> | 运行平面 | 做法 |
> |---|---|
> | **Claude Code** | 自定义 Stop hook 在每轮结束后把 evaluator 作为一个全新的 `claude` 进程跑起来，只要结果不是 `PASS` 就阻塞 |
> | **Headless**（`claude -p`） | wrapper 脚本在两次构建之间调用 `claude --agent evaluator -p`（示例见下） |
> | **Agent SDK** | 分开的 generator 和 evaluator `query()` 调用；参见 `evaluator_optimizer` |

```bash
while grep -q '"passes": false' test-results.json; do
  claude -p "Read PROGRESS.md and build the next unfinished feature per CLAUDE.md."
  VERDICT=$(claude --agent evaluator -p "Review the most recent commit against its spec.")
  [ "$(echo "$VERDICT" | head -1)" = "PASS" ] || echo "$VERDICT" > NEXT_FINDINGS.md
done
```

> **代码中提示词的中文译文**：builder 提示词——「读取 PROGRESS.md，按 CLAUDE.md 的规范构建下一个未完成的功能。」；evaluator 提示词——「对照规格说明，审查最近一次提交。」

Each pass is a fresh context.

每一轮循环都跑在一个全新的上下文里。

Exit when the contract file has nothing left failing, a cycle makes no changes, or a budget is hit; `touch AGENT_STOP` to stop early.

退出条件是：契约文件里不再有失败项、某一轮没有产生任何变更、或者预算耗尽；要提前停止，`touch AGENT_STOP` 即可。

The builder writes `test-results.json` (verify-gate enforces evidence-read first) and the evaluator returns a separate verdict; have your wrapper write the contract on `PASS` instead if you want "all true" to mean "independently confirmed."

builder 负责写 `test-results.json`（verify-gate 强制它必须先读过证据），evaluator 返回一份独立的裁决；如果你希望「全部为 true」意味着「经过独立确认」，可以改成让你的 wrapper 在收到 `PASS` 时才写契约文件。

## Operator controls|运维控制

Two more hooks for when you want to watch the loop run or intervene mid-stream:

另外两个 hook，供你想在循环运行时观察或中途介入之用：

| Hook | What it does |
|---|---|
| [`hooks/kill-switch.sh`](https://github.com/anthropics/cwc-long-running-agents/blob/HEAD/claude-code-config/.claude/hooks/kill-switch.sh) | Halts every tool call while an `AGENT_STOP` file exists at the project root. |
| [`hooks/steer.sh`](https://github.com/anthropics/cwc-long-running-agents/blob/HEAD/claude-code-config/.claude/hooks/steer.sh) | Surfaces the contents of `STEER.md` (project root) to the agent once and clears it, so you can redirect mid-run without restarting. |

> **中文对照表**
>
> | Hook | 作用 |
> |---|---|
> | `hooks/kill-switch.sh` | 只要项目根目录存在 `AGENT_STOP` 文件，就暂停所有工具调用。 |
> | `hooks/steer.sh` | 把项目根目录 `STEER.md` 的内容一次性呈现给智能体然后清空，让你无需重启即可中途转向。 |

## Watching it work|观察它运转

Everything the agent does lands on disk, so you can observe a long run from a terminal without any dashboard code:

智能体做的每件事都会落在磁盘上，所以你不需要写任何仪表盘代码，从终端就能观察一次长时程运行：

```bash
watch -n 2 'tail -20 PROGRESS.md'                          # its own notes
watch -n 5 'git log --oneline -8'                          # work saved
watch -n 5 'find screenshots -name "*.png" | tail -5'      # what it sees
watch -n 2 'wc -l < .claude/.evidence-reads 2>/dev/null'   # evidence reads (resets to 0 after each gated write)
```

> **代码注释的中文译文**：依次是——它自己的笔记；已保存的工作；它看到的东西；证据读取次数（每次通过门控的写入后清零）。

Run them in a `tmux` grid and you have a live view of every primitive.

把这几条命令放进一个 `tmux` 网格里跑，你就拥有了每个原语的实时视图。

## Going further|更进一步

The next layer of patterns, each covered in depth in [Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps):

下一层模式，每一个都在[《Harness Design for Long-Running Application Development》](https://www.anthropic.com/engineering/harness-design-long-running-apps)中有深入讲解：

| Pattern | What it adds | Reference |
|---|---|---|
| **Unattended loop** | Cap session length and have an outer script start the next one (pick next feature, build, evaluate, reset) | [Why naive implementations fall short](https://www.anthropic.com/engineering/harness-design-long-running-apps#why-naive-implementations-fall-short); [`ralph-loop`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-loop) plugin |
| **Planner agent** | A first session that expands a one-line ask into a `BUILD_PLAN.md` the loop then runs against | [The architecture](https://www.anthropic.com/engineering/harness-design-long-running-apps#the-architecture) |
| **Sprint contracts** | Builder and evaluator agree per-feature on what "done" means and write it to a file the hook enforces | [The architecture](https://www.anthropic.com/engineering/harness-design-long-running-apps#the-architecture) and [Removing the sprint construct](https://www.anthropic.com/engineering/harness-design-long-running-apps#removing-the-sprint-construct) |
| **Grading rubrics** | Give the evaluator scoring principles (functionality, design, craft, originality) with few-shot examples instead of binary pass/fail | [Frontend design: making subjective quality gradable](https://www.anthropic.com/engineering/harness-design-long-running-apps#frontend-design-making-subjective-quality-gradable); [`frontend-design`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design) plugin |
| **Browser-verified evaluator** | Let the evaluator open the running app itself instead of trusting the builder's screenshots | [Frontend design](https://www.anthropic.com/engineering/harness-design-long-running-apps#frontend-design-making-subjective-quality-gradable) (Playwright MCP usage); add [`@playwright/mcp`](https://github.com/microsoft/playwright-mcp) or Claude in Chrome to `tools:` in `agents/evaluator.md` |
| **Re-simplify on model upgrades** | After each model release, comment out harness pieces one at a time and see what's still load-bearing | [What comes next](https://www.anthropic.com/engineering/harness-design-long-running-apps#what-comes-next); [Harnessing Claude's Intelligence](https://claude.com/blog/harnessing-claudes-intelligence) |
| **Hosted runtime** | Anthropic hosts the loop, sandbox, and scheduling so you don't run any of this yourself | [Claude Managed Agents](https://docs.claude.com/en/docs/managed-agents) |

> **中文对照表**
>
> | 模式 | 增加了什么 | 参考 |
> |---|---|---|
> | **无人值守循环（Unattended loop）** | 限制单次会话长度，由外层脚本启动下一轮（选下一个功能、构建、评审、重置） | 《为什么朴素实现会失败》；`ralph-loop` 插件 |
> | **规划者智能体（Planner agent）** | 用第一次会话把一句话需求展开成 `BUILD_PLAN.md`，供后续循环执行 | 《架构》 |
> | **冲刺契约（Sprint contracts）** | builder 和 evaluator 逐功能商定「做完」的定义，写进由 hook 强制的文件里 | 《架构》与《移除冲刺构造》 |
> | **评分标准（Grading rubrics）** | 给 evaluator 提供评分原则（功能性、设计、工艺、原创性）加 few-shot 示例，替代二元的通过/不通过 | 《前端设计：让主观质量可评分》；`frontend-design` 插件 |
> | **浏览器验证的评审者（Browser-verified evaluator）** | 让 evaluator 自己打开运行中的应用，而不是信任 builder 的截图 | 《前端设计》（Playwright MCP 用法）；把 `@playwright/mcp` 或 Claude in Chrome 加进 `agents/evaluator.md` 的 `tools:` |
> | **模型升级后的重新简化（Re-simplify on model upgrades）** | 每次模型发布后，一次注释掉一块 harness，看什么还是承重的（load-bearing） | 《接下来会怎样》；《Harnessing Claude's Intelligence》 |
> | **托管运行时（Hosted runtime）** | 由 Anthropic 托管循环、沙箱与调度，你自己什么都不用跑 | Claude Managed Agents |

---

# CLAUDE.md — builder 的系统提示|长时程运行约定

> 文件路径：`claude-code-config/.claude/CLAUDE.md`。文件头部有两行版权注释（`Copyright 2026 Anthropic PBC` / `SPDX-License-Identifier: Apache-2.0`），此处从略。

## Long-running conventions for this project|本项目的长时程运行约定

### Always start here|永远从这里开始

Before doing anything else, read `PROGRESS.md`.

在做任何其他事情之前，先读 `PROGRESS.md`。

It is your handoff note from the previous session.

它是上一次会话留给你的交接笔记（handoff note）。

If it doesn't exist yet, create it now with four sections (`## Done`, `## In progress`, `## Next`, `## Notes`) and leave them empty.

如果它还不存在，现在就创建它，包含四个小节（`## Done`、`## In progress`、`## Next`、`## Notes`），内容先留空。

Then run `git log --oneline -10` to see what was just committed, and run the project's smoke test (or `npm run build` / `npm test`) once so you know you're starting from a working tree, not a broken handoff.

然后运行 `git log --oneline -10` 看看刚刚提交了什么，并把项目的冒烟测试（smoke test，或 `npm run build` / `npm test`）跑一遍，以确认你的起点是一棵能正常工作的代码树，而不是一次坏掉的交接。

### One feature at a time|一次只做一个功能

Work on exactly one item from `PROGRESS.md` per session.

每次会话只处理 `PROGRESS.md` 中的恰好一项。

Finish it (tests passing, screenshot verified) before starting another.

先把它彻底完成（测试通过、截图验证），再开始下一项。

If the user gives you a new task mid-session, add it to `PROGRESS.md` and finish the current item first.

如果用户在会话中途给你新任务，把它加进 `PROGRESS.md`，先完成当前这一项。

### Proof before passing|先有证据，再算通过

A test is only "passing" after you have:

一个测试只有在你完成以下步骤后才算「通过」：

1. Run it against the live app (Playwright screenshot or equivalent)

1. 对着运行中的真实应用跑过它（Playwright 截图或等价手段）

2. Opened the resulting screenshot or console log with the Read tool

2. 用 Read 工具打开过产生的截图或 console 日志

3. Confirmed it shows what it should

3. 确认它显示的内容符合预期

The `verify-gate` hook will deny writes to `test-results.json` until you have opened evidence.

在你打开证据文件之前，`verify-gate` hook 会拒绝对 `test-results.json` 的写入。

Do not try to work around it.

不要试图绕过它。

### Keep `PROGRESS.md` current|保持 `PROGRESS.md` 时刻最新

After each completed item, update `PROGRESS.md`: check off what's done, add what you learned, note what's next.

每完成一项就更新 `PROGRESS.md`：勾掉做完的，写下学到的，记下接下来要做的。

Future sessions read this file cold.

未来的会话会在毫无背景（cold）的情况下读这个文件。

### Commit often|频繁提交

The `Stop` hook commits tracked changes at session end, but also `git add` new files and commit yourself at meaningful checkpoints with descriptive messages.

`Stop` hook 会在会话结束时提交已跟踪的变更，但你自己也要在有意义的检查点 `git add` 新文件并提交，附上描述清晰的提交信息。

### If you're told to stop|如果有人让你停下

`OPERATOR STEERING:` messages come from a human via the steer hook.

`OPERATOR STEERING:` 开头的消息来自人类操作者，经由 steer hook 送达。

Treat them as higher priority than your current plan.

把它们当作比你当前计划更高优先级的指令来对待。

---

# agents/evaluator.md — 评审子智能体提示|全新上下文评审者的定义

> 文件路径：`claude-code-config/.claude/agents/evaluator.md`。开头是 YAML frontmatter（子智能体的名称、描述与工具配置），随后是系统提示正文；正文前同样有两行 Apache-2.0 版权注释，此处从略。

```yaml
---
name: evaluator
description: Skeptical second-opinion reviewer. Reads the diff and the builder's evidence, then returns PASS or NEEDS_WORK with specific findings. Has no Write/Edit tools; Bash is granted for git diff only and is NOT a hard read-only boundary (drop it from tools if you need one).
tools: Read, Glob, Grep, Bash
---
```

> **中文译文**：name：evaluator。description：持怀疑态度的第二意见评审者。读取 diff 和 builder 的证据，然后返回 PASS 或 NEEDS_WORK 并附具体发现。没有 Write/Edit 工具；Bash 仅为 git diff 而授予，它**不是**一道硬性的只读边界（如果你需要硬边界，就把 Bash 从 tools 里去掉）。tools：Read、Glob、Grep、Bash。

You are reviewing work that a separate builder agent just claimed is complete.

你正在审查一项由另一个 builder 智能体刚刚宣称已完成的工作。

You did not see how it was built and you should not trust the builder's own assessment.

你没有见过它是怎么构建出来的，也不应该相信 builder 对自己工作的评估。

Do the following every time:

每次都执行以下步骤：

1. Read the spec or acceptance criteria for the feature under review.

1. 读取被审查功能的规格说明（spec）或验收标准（acceptance criteria）。

2. Run `git diff` against the baseline to see exactly what changed.

2. 对基线（baseline）运行 `git diff`，弄清楚到底改了什么。

3. Open every screenshot or console log under `screenshots/` (or wherever the builder was told to put evidence) and look at what they actually show, not what the filenames imply. If a file fails to open or returns an error, treat it as missing evidence.

3. 打开 `screenshots/` 下（或 builder 被要求放置证据的任何位置）的每一张截图和每一份 console 日志，看它们实际显示了什么，而不是文件名暗示了什么。如果某个文件打不开或返回错误，就当作证据缺失处理。

4. Decide.

4. 做出裁决。

Plausibility is not correctness.

「看起来合理」不等于「正确」。

A diff that looks reasonable paired with a screenshot that shows a broken layout is NEEDS_WORK.

一份看起来合理的 diff，配上一张显示布局已坏的截图，结论就是 NEEDS_WORK。

Missing evidence for any acceptance criterion is NEEDS_WORK.

任何一条验收标准缺少证据，结论就是 NEEDS_WORK。

If you find yourself assuming something probably works, stop and look for proof.

如果你发现自己在假设某个东西「大概能用」，停下来，去找证据。

Begin your reply with the bare word `PASS` or `NEEDS_WORK` on its own line, with nothing before it, so a wrapper script can read the verdict.

回复的第一行必须是光秃秃的 `PASS` 或 `NEEDS_WORK`，独占一行，前面不能有任何内容，以便 wrapper 脚本读取裁决。

Then:

然后：

- `PASS`: one line stating what evidence convinced you.

- `PASS`：用一行说明是什么证据说服了你。

- `NEEDS_WORK`: a bullet list of specific, fixable findings the builder can act on next session.

- `NEEDS_WORK`：列出一个要点清单，包含 builder 下次会话可以直接着手处理的、具体且可修复的发现。

Use Bash only for `git diff`, `git log`, and `ls`/`cat`.

Bash 只能用于 `git diff`、`git log` 和 `ls`/`cat`。

You cannot edit, write, or run the application.

你不能编辑、不能写入，也不能运行这个应用。

Do not offer to fix anything yourself.

不要主动提出由你自己来修复任何问题。
