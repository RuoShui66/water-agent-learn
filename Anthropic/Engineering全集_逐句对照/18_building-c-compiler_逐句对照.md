# 18_Building a C compiler with a team of parallel Claudes_用一支并行 Claude 团队构建 C 编译器

> 原文：https://www.anthropic.com/engineering/building-c-compiler
> 作者：Nicholas Carlini（Anthropic Engineering）｜发布日期：2026-02-05

## 📌 本篇速览

- 📅 2026-02-05　｜　⏱ 约 15 分钟　｜　📄 2,489 词 / 0 图
- ⭐ ★★★★☆ **强烈推荐** —— 这是多智能体并行自主开发的第一手工程实录，测试设计、任务拆分与并行化经验对构建长时运行 Agent 系统的工程师几乎句句可复用。
- 🏷 智能体团队、并行多智能体、长时自主运行 harness、测试与验证器设计、能力基准压测
- 🖼 [图解笔记（面试速记）](18_building-c-compiler_直观图解与学习笔记.md)　·　🗂 [返回总目录](00_目录与阅读进度.md)

Anthropic 研究员 Nicholas Carlini 让 16 个 Claude 智能体在无人干预下并行协作，通过近 2000 次 Claude Code 会话、约 2 万美元 API 成本，从零写出一个 10 万行 Rust 实现的 C 编译器，可在 x86/ARM/RISC-V 上编译 Linux 6.9 内核。文章重点分享了长时运行自主智能体团队的 harness 设计经验：极高质量的测试验证器、为模型局限（上下文污染、时间盲区）做环境设计、基于 git 锁文件的并行任务分配、用 GCC 作 oracle 拆解大任务，以及多角色分工。作者同时坦承该方法的能力天花板与完全自主开发带来的安全隐忧。

---

*Written by Nicholas Carlini, a researcher on our Safeguards team.*

*本文作者 Nicholas Carlini，是我们 Safeguards（安全防护）团队的研究员。*

I've been experimenting with a new approach to supervising language models that we’re calling "agent teams."

我最近一直在实验一种监督语言模型的新方法，我们称之为"智能体团队"（agent teams）。

With agent teams, multiple Claude instances work in parallel on a shared codebase without active human intervention.

在智能体团队模式下，多个 Claude 实例在同一个共享代码库上并行工作，无需人类的主动干预。

This approach dramatically expands the scope of what's achievable with LLM agents.

这种方法极大地拓展了 LLM 智能体所能达成的任务范围。

To stress test it, I tasked 16 agents with writing a Rust-based C compiler, from scratch, capable of compiling the Linux kernel.

为了对它做压力测试，我给 16 个智能体布置了一个任务：从零开始用 Rust 写一个 C 编译器，并且要能编译 Linux 内核。

Over nearly 2,000 Claude Code sessions and $20,000 in API costs, the agent team produced a 100,000-line compiler that can build Linux 6.9 on x86, ARM, and RISC-V.

历经近 2,000 次 Claude Code 会话（session）、花费 20,000 美元的 API 成本之后，这支智能体团队产出了一个 10 万行代码的编译器，能够在 x86、ARM 和 RISC-V 上构建 Linux 6.9。

🎬 **视频**：[在 YouTube 观看](https://www.youtube.com/watch?v=vNeIQS9GsZ8)

[The compiler is an interesting artifact](https://github.com/anthropics/claudes-c-compiler) on its own, but I focus here on what I learned about designing harnesses for long-running autonomous agent teams: how to write tests that keep agents on track without human oversight, how to structure work so multiple agents can make progress in parallel, and where this approach hits its ceiling.

[这个编译器本身就是一件有意思的作品](https://github.com/anthropics/claudes-c-compiler)，但本文的重点是我在为长时间运行的自主智能体团队设计执行框架（harness）时学到的东西：如何编写测试，让智能体在没有人类监督的情况下不跑偏；如何组织工作，让多个智能体能够并行推进；以及这种方法的天花板在哪里。

### Enabling long-running Claudes｜让 Claude 长时间持续运行

Existing agent scaffolds like Claude Code require an operator to be online and available to work jointly.

Claude Code 这类现有的智能体脚手架（scaffold），要求操作者在线并随时配合协作。

If you ask for a solution to a long and complex problem, the model may solve part of it, but eventually it will stop and wait for continued input—a question, a status update, or a request for clarification.

如果你要求它解决一个漫长而复杂的问题，模型也许能解决其中一部分，但最终它会停下来等待你的后续输入——提出一个问题、汇报一下进度，或是请求你澄清。

To elicit sustained, autonomous progress, I built a harness that sticks Claude in a simple loop (if you’ve seen Ralph-loop, this should look familiar).

为了激发持续、自主的进展，我构建了一个执行框架，把 Claude 放进一个简单的循环里（如果你见过 Ralph-loop，应该会觉得眼熟）。

When it finishes one task, it immediately picks up the next. *(Run this in a container, not your actual machine).*

它一完成一个任务，就立刻接手下一个。**（请在容器里运行这个脚本，别在你的真机上跑。）**

```
#!/bin/bash

while true; do
    COMMIT=$(git rev-parse --short=6 HEAD)
    LOGFILE="agent_logs/agent_${COMMIT}.log"

    claude --dangerously-skip-permissions \
           -p "$(cat AGENT_PROMPT.md)" \
           --model claude-opus-X-Y &> "$LOGFILE"
done

```

In the agent prompt, I tell Claude what problem to solve and ask it to approach the problem by breaking it into small pieces, tracking what it’s working on, figuring out what to work on next, and to effectively keep going until it’s perfect.

在智能体提示词（agent prompt）里，我告诉 Claude 要解决什么问题，并要求它按这样的方式推进：把问题拆成小块、跟踪自己当前在做什么、想清楚接下来该做什么，并且实际上要一直做下去，直到做得完美为止。

(On this last point, Claude has no choice. The loop runs forever—although in one instance, I did see Claude `pkill -9 bash` on accident, thus killing itself and ending the loop. Whoops!).

（关于最后这一点，Claude 别无选择。这个循环会永远跑下去——不过有一次，我确实看到 Claude 不小心执行了 `pkill -9 bash`，把自己杀掉了，循环也就此终结。哎呀！）

### Running Claude in parallel｜并行运行 Claude

Running multiple instances in parallel can address two weaknesses of a single-agent harness:

并行运行多个实例，可以弥补单智能体执行框架的两个弱点：

- One Claude Code session can only do one thing at a time. Especially as the scope of a project expands, debugging multiple issues in parallel is far more efficient.

- 一个 Claude Code 会话一次只能做一件事。尤其当项目规模扩大后，并行调试多个问题的效率要高得多。

- Running multiple Claude agents allows for specialization. While a few agents are tasked to solve the actual problem at hand, other specialized agents can be invoked to (for example) maintain documentation, keep an eye on code quality, or solve specialized sub-tasks.

- 运行多个 Claude 智能体还可以实现专业化分工（specialization）。当少数几个智能体负责解决手头的核心问题时，可以调用其他专职智能体去（比如）维护文档、盯着代码质量，或者解决专门的子任务。

My implementation of parallel Claude is bare-bones.

我的并行 Claude 实现非常简陋。

A new bare git repo is created, and for each agent, a Docker container is spun up with the repo mounted to `/upstream`.

先创建一个新的裸 git 仓库（bare repo），然后为每个智能体启动一个 Docker 容器，把这个仓库挂载到 `/upstream`。

Each agent clones a local copy to `/workspace`, and when it's done, pushes from its own local container to upstream.

每个智能体把仓库克隆一份本地副本到 `/workspace`，完成工作后，再从自己的本地容器推送（push）回上游（upstream）。

To prevent two agents from trying to solve the same problem at the same time, the harness uses a simple synchronization algorithm:

为了防止两个智能体同时去解决同一个问题，执行框架使用了一个简单的同步算法：

1. Claude takes a "lock" on a task by writing a text file to current_tasks/ (e.g., one agent might lock current_tasks/parse_if_statement.txt, while another locks current_tasks/codegen_function_definition.txt). If two agents try to claim the same task, git's synchronization forces the second agent to pick a different one.

1. Claude 通过向 current_tasks/ 目录写入一个文本文件来给任务加"锁"（lock）（例如，一个智能体可能锁住 current_tasks/parse_if_statement.txt，另一个则锁住 current_tasks/codegen_function_definition.txt）。如果两个智能体试图认领同一个任务，git 的同步机制会迫使第二个智能体另选一个。

2. Claude works on the task, then pulls from upstream, merges changes from other agents, pushes its changes, and removes the lock. Merge conflicts are frequent, but Claude is smart enough to figure that out.

2. Claude 完成任务后，从上游拉取（pull）代码，合并其他智能体的改动，推送自己的改动，然后移除锁。合并冲突（merge conflict）很常见，但 Claude 足够聪明，能自己搞定。

3. The infinite agent-generation-loop spawns a new Claude Code session in a fresh container, and the cycle repeats.

3. 无限的智能体生成循环会在一个全新容器里启动一个新的 Claude Code 会话，如此周而复始。

This is a very early research prototype.

这还是一个非常早期的研究原型。

I haven’t yet implemented any other method for communication between agents, nor do I enforce any process for managing high-level goals.

我还没有实现智能体之间任何其他的通信方式，也没有强制任何管理高层目标的流程。

I don’t use an orchestration agent.

我没有使用编排智能体（orchestration agent）。

Instead, I leave it up to each Claude agent to decide how to act.

相反，我让每个 Claude 智能体自己决定该怎么行动。

In most cases, Claude picks up the “next most obvious” problem.

大多数情况下，Claude 会挑起"下一个最显而易见"的问题。

When stuck on a bug, Claude will often maintain a running doc of failed approaches and remaining tasks.

当卡在某个 bug 上时，Claude 通常会维护一份持续更新的文档，记录已失败的尝试路径和剩余任务。

In the [git repository](https://github.com/anthropics/claudes-c-compiler) of the project, you can read through the history and watch it take out locks on various tasks.

在项目的 [git 仓库](https://github.com/anthropics/claudes-c-compiler)里，你可以通读提交历史，看到它给各种任务加锁的过程。

### Lessons from programming with Claude agent teams｜与 Claude 智能体团队一起编程的经验

The scaffolding runs Claude in a loop, but that loop is only useful if Claude can tell how to make progress.

脚手架让 Claude 在循环中运行，但只有当 Claude 能够判断如何取得进展时，这个循环才有用。

Most of my effort went into designing the environment around Claude—the tests, the environment, the feedback—so that it could orient itself without me.

我的大部分精力都花在设计 Claude 周围的环境上——测试、环境本身、反馈机制——让它不需要我也能自己找准方向。

These are the approaches I’ve found most helpful when orchestrating multiple Claude instances.

以下是我在编排多个 Claude 实例时发现最有用的做法。

#### Write extremely high-quality tests｜编写极高质量的测试

Claude will work autonomously to solve whatever problem I give it.

不管我给 Claude 什么问题，它都会自主地去解决。

So it’s important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem.

因此，任务验证器（verifier）必须近乎完美，否则 Claude 就会去解决错误的问题。

Improving the testing harness required finding high-quality compiler test suites, writing verifiers and build scripts for open-source software packages, and watching for mistakes Claude was making, then designing new tests as I identified those failure modes.

改进测试框架需要做这些事：寻找高质量的编译器测试套件（test suite）、为开源软件包编写验证器和构建脚本、观察 Claude 正在犯的错误，然后在识别出这些失败模式（failure mode）后设计新的测试。

For example, near the end of the project, Claude started to frequently break existing functionality each time it implemented a new feature.

例如，在项目接近尾声时，Claude 开始频繁地在每次实现新功能时破坏已有功能。

To address this, I built a continuous integration pipeline and implemented stricter enforcement that allowed Claude to better test its work so that new commits can’t break existing code.

为了解决这个问题，我搭建了一条持续集成（continuous integration）流水线，并实施了更严格的强制约束，让 Claude 能更好地测试自己的工作，使新提交无法破坏已有代码。

#### Put yourself in Claude’s shoes｜设身处地为 Claude 着想

I had to constantly remind myself that I was writing this test harness for Claude and not for myself, which meant rethinking many of my assumptions about how tests should communicate results.

我必须不断提醒自己：这套测试框架是写给 Claude 用的，不是写给我自己用的——这意味着我要重新审视自己关于"测试该如何传达结果"的许多预设。

For example, each agent is dropped into a fresh container with no context and will spend significant time orienting itself, especially on large projects.

例如，每个智能体都被扔进一个没有任何上下文（context）的全新容器，需要花大量时间来熟悉状况，在大型项目上尤其如此。

Before we even reach the tests, to help Claude help itself, I included instructions to maintain extensive READMEs and progress files that should be updated frequently with the current status.

在还没谈到测试之前，为了帮 Claude 自助，我在指令里就要求它维护详尽的 README 和进度文件，并频繁更新其中的当前状态。

I also kept in mind the fact that language models have inherent limitations, which, in this case, needed to be designed around.

我还时刻记着一个事实：语言模型存在固有局限，而在这个项目里，这些局限需要通过设计来绕开。

These include:

这些局限包括：

- **Context window pollution:** The test harness should not print thousands of useless bytes. At most, it should print a few lines of output and log all important information to a file so Claude can find it when needed. Logfiles should be easy to process automatically: if there are errors, Claude should write ERROR and put the reason on the same line so grep will find it. It helps to pre-compute aggregate summary statistics so Claude doesn't have to recompute them.

- **上下文窗口污染（Context window pollution）：** 测试框架不应该打印成千上万字节的无用内容。它最多只应打印几行输出，并把所有重要信息记录到文件里，让 Claude 需要时能找到。日志文件应当便于自动化处理：如果出错了，Claude 应该写下 ERROR 并把原因放在同一行，这样 grep 就能搜到。预先算好汇总统计数据也很有帮助，这样 Claude 就不必重新计算。

- **Time blindness:** Claude can't tell time and, left alone, will happily spend hours running tests instead of making progress. The harness prints incremental progress infrequently (to avoid polluting context) and includes a default `--fast` option that runs a 1% or 10% random sample. This subsample is deterministic per-agent but random across VMs, so Claude still covers all files but each agent can perfectly identify regressions.

- **时间盲区（Time blindness）：** Claude 感知不到时间，放任不管的话，它会心安理得地花几个小时跑测试而不是推进工作。所以执行框架只以较低频率打印增量进度（以免污染上下文），并提供一个默认的 `--fast` 选项，只跑 1% 或 10% 的随机抽样。这个子样本对每个智能体是确定性的，但在不同虚拟机（VM）之间是随机的，因此 Claude 整体上仍能覆盖所有文件，而每个智能体又能精确识别出回归（regression）。

#### Make parallelism easy｜让并行变得容易

When there are many distinct failing tests, parallelization is trivial: each agent picks a different failing test to work on.

当存在许多各不相同的失败测试时，并行化不费吹灰之力：每个智能体挑一个不同的失败测试来处理即可。

After the test suite reached a 99% pass rate, each agent worked on getting a different small open-source project (e.g., SQlite, Redis, libjpeg, MQuickJS, Lua) to compile.

在测试套件达到 99% 的通过率之后，每个智能体各自负责让一个不同的小型开源项目（如 SQlite、Redis、libjpeg、MQuickJS、Lua）编译通过。

But when agents started to compile the Linux kernel, they got stuck.

但当智能体们开始编译 Linux 内核时，它们卡住了。

Unlike a test suite with hundreds of independent tests, compiling the Linux kernel is one giant task.

与包含数百个独立测试的测试套件不同，编译 Linux 内核是一个巨大的整体任务。

Every agent would hit the same bug, fix that  bug, and then overwrite each other's changes.

每个智能体都会撞上同一个 bug，修复那个 bug，然后互相覆盖彼此的改动。

Having 16 agents running didn't help because each was stuck solving the same task.

跑着 16 个智能体也无济于事，因为每一个都卡在解决同一个任务上。

The fix was to use [GCC](https://gcc.gnu.org/) as an online known-good compiler oracle to compare against.

解决办法是把 [GCC](https://gcc.gnu.org/) 用作一个在线的、已知正确的编译器"参照基准"（oracle）来做对比。

I wrote a new test harness that randomly compiled most of the kernel using GCC, and only the remaining files with Claude's C Compiler.

我写了一套新的测试框架：随机地用 GCC 编译内核的大部分文件，只把剩下的文件交给 Claude 的 C 编译器编译。

If the kernel worked, then the problem wasn’t in Claude’s subset of the files.

如果内核能正常工作，那问题就不在 Claude 负责的那部分文件里。

If it broke, then it could further refine by re-compiling some of these files with GCC.

如果内核出了问题，还可以进一步细化排查：把其中一部分文件改用 GCC 重新编译。

This let each agent work in parallel, fixing different bugs in different files, until Claude's compiler could eventually compile all files.

这让每个智能体得以并行工作，在不同文件里修复不同的 bug，直到 Claude 的编译器最终能编译所有文件。

(After this worked, it was still necessary to apply delta debugging techniques to find pairs of files that failed together but worked independently.)

（这套方法奏效之后，仍然需要运用增量调试（delta debugging）技术，来找出那些"单独编译都没问题、放在一起就出错"的文件对。）

#### Multiple agent roles｜多种智能体角色

Parallelism also enables specialization.

并行也让专业化分工成为可能。

LLM-written code frequently re-implements existing functionality, so I tasked one agent with coalescing any duplicate code it found.

LLM 写的代码经常重复实现已有的功能，所以我安排了一个智能体专门负责合并它发现的所有重复代码。

I put another in charge of improving the performance of the compiler itself, and a third I made responsible for outputting efficient compiled code.

我让另一个智能体负责提升编译器自身的性能，又让第三个负责让编译产出的代码更高效。

I asked another agent to critique the design of the project from the perspective of a Rust developer, and make structural changes to the project to improve the overall code quality, and another to work on documentation.

我还让一个智能体从 Rust 开发者的视角来批评这个项目的设计，并对项目做结构性调整以提升整体代码质量；再让另一个智能体负责文档工作。

### Stress testing the limits of agent teams｜压力测试智能体团队的极限

This project was designed as a capability benchmark.

这个项目在设计上就是一个能力基准测试（capability benchmark）。

I am interested in stress-testing the limits of what LLMs can just *barely* achieve today in order to help us prepare for what models will reliably achieve in the future.

我感兴趣的是压力测试 LLM 今天*勉强*能够达到的极限，以便帮助我们为模型未来能够稳定达到的水平做好准备。

I’ve been using the C Compiler project as a benchmark across the entire Claude 4 model series.

我一直把这个 C 编译器项目当作贯穿整个 Claude 4 模型系列的基准测试。

As I did with prior projects, I started by drafting what I wanted: a from-scratch optimizing compiler with no dependencies, GCC-compatible, able to compile the Linux kernel, and designed to support multiple backends.

和以往的项目一样，我先起草了我想要的东西：一个从零开始、零依赖的优化编译器，兼容 GCC，能编译 Linux 内核，并且在设计上支持多后端（backend）。

While I specified some aspects of the design (e.g., that it should have an SSA IR to enable multiple optimization passes) I did not go into any detail on how to do so.

虽然我指定了设计的某些方面（例如，它应该有一个 SSA 形式的中间表示（SSA IR），以支持多轮优化（optimization pass）），但我没有对具体怎么做展开任何细节。

Previous Opus 4 models were barely capable of producing a functional compiler.

之前的 Opus 4 系列模型勉强能产出一个可用的编译器。

Opus 4.5 was the first to cross a threshold that allowed it to produce a functional compiler which could pass large test suites, but it was still incapable of compiling any real large projects.

Opus 4.5 是第一个跨过门槛的模型：它能产出一个可通过大型测试套件的可用编译器，但仍然无法编译任何真正的大型项目。

My goal with Opus 4.6 was to again test the limits.

我对 Opus 4.6 的目标，是再一次测试极限。

#### Evaluation｜评估

Over nearly 2,000 Claude Code sessions across two weeks, Opus 4.6 consumed 2 billion input tokens and generated 140 million output tokens, a total cost just under $20,000.

在两周时间里的近 2,000 次 Claude Code 会话中，Opus 4.6 消耗了 20 亿输入 token，生成了 1.4 亿输出 token，总成本略低于 20,000 美元。

Compared to even the most expensive Claude Max plans, this was an extremely expensive project.

即便和最贵的 Claude Max 订阅方案相比，这也是一个极其昂贵的项目。

But that total is a fraction of what it would cost me to produce this myself—let alone an entire team.

但这个总额只是我亲自做出同样东西所需成本的一个零头——更不用说雇一整个团队了。

This was a clean-room implementation (Claude did not have internet access at any point during its development); it depends only on the Rust standard library.

这是一个"洁净室"实现（clean-room implementation）（在整个开发过程中，Claude 任何时候都无法访问互联网）；它只依赖 Rust 标准库。

The 100,000-line compiler can build a bootable Linux 6.9 on x86, ARM, and RISC-V.

这个 10 万行的编译器可以在 x86、ARM 和 RISC-V 上构建出可启动的 Linux 6.9。

It can also compile QEMU, FFmpeg, SQlite, postgres, redis, and has a 99% pass rate on most compiler test suites including the [GCC torture test suite](https://gcc.gnu.org/onlinedocs/gccint/Torture-Tests.html).

它还能编译 QEMU、FFmpeg、SQlite、postgres、redis，并在大多数编译器测试套件上达到 99% 的通过率，其中包括 [GCC torture 测试套件](https://gcc.gnu.org/onlinedocs/gccint/Torture-Tests.html)。

It also passes the developer's ultimate litmus test: it can compile and run Doom.

它还通过了开发者的终极试金石测试：它能编译并运行 Doom。

The compiler, however, is not without limitations. These include:

不过，这个编译器并非没有局限。这些局限包括：

- It lacks the 16-bit x86 compiler that is necessary to boot Linux out of real mode. For this, it calls out to GCC (the x86_32 and x86_64 compilers are its own).

- 它缺少让 Linux 脱离实模式（real mode）启动所必需的 16 位 x86 编译器。这一部分它是调用 GCC 完成的（x86_32 和 x86_64 编译器则是它自己的）。

- It does not have its own assembler and linker; these are the very last bits that Claude started automating and are still somewhat buggy. The demo video was produced with a GCC assembler and linker.

- 它没有自己的汇编器（assembler）和链接器（linker）；这是 Claude 最后才着手自动化的部分，目前仍有不少 bug。演示视频是用 GCC 的汇编器和链接器制作的。

- The compiler successfully builds many projects, but not all. It's not yet a drop-in replacement for a real compiler.

- 这个编译器能成功构建很多项目，但并非全部。它还不能作为真实编译器的直接替代品（drop-in replacement）。

- The generated code is not very efficient. Even with all optimizations enabled, it outputs less efficient code than GCC with all optimizations *disabled.*

- 生成的代码效率不高。即便开启全部优化，它输出的代码也比*关闭*全部优化的 GCC 还要低效。

- The Rust code quality is reasonable, but is nowhere near the quality of what an expert Rust programmer might produce.

- Rust 代码质量尚可，但远远达不到 Rust 专家级程序员的水准。

The resulting compiler has nearly reached the limits of Opus’s abilities.

这个最终产出的编译器，已经几乎触及 Opus 能力的极限。

I tried (hard!) to fix several of the above limitations but wasn’t fully successful.

我（非常努力地！）尝试修复上述几项局限，但没有完全成功。

New features and bugfixes frequently broke existing functionality.

新功能和 bug 修复经常破坏已有功能。

As one particularly challenging example, Opus was unable to implement a 16-bit x86 code generator needed to boot into 16-bit real mode.

举一个特别有挑战性的例子：Opus 无法实现启动进入 16 位实模式所需的 16 位 x86 代码生成器。

While the compiler can output correct 16-bit x86 via the 66/67 opcode prefixes, the resulting compiled output is over 60kb, far exceeding the 32k code limit enforced by Linux.

虽然编译器可以通过 66/67 操作码前缀（opcode prefix）输出正确的 16 位 x86 代码，但编译产物超过 60kb，远超 Linux 强制的 32k 代码大小限制。

Instead, Claude simply cheats here and calls out to GCC for this phase (This is only the case for x86. For ARM or RISC-V, Claude’s compiler can compile completely by itself.)

于是 Claude 在这里干脆"作弊"，把这一阶段外包给 GCC（只有 x86 是这样。对于 ARM 或 RISC-V，Claude 的编译器可以完全独立完成编译。）

The [source code for the compiler is available](https://github.com/anthropics/claudes-c-compiler).

[编译器的源代码已经公开](https://github.com/anthropics/claudes-c-compiler)。

Download it, read through the code, and try it on your favorite C projects.

下载下来，通读代码，在你喜欢的 C 项目上试试它。

I’ve consistently found the best way to understand what language models can do is to push them to their limits, and then study where they start to break down.

我一贯发现，理解语言模型能做什么的最好方式，就是把它们推到极限，然后研究它们从哪里开始崩坏。

Over the coming days, I’ll continue having Claude push new changes if you want to follow along with Claude’s continued attempts at addressing these limitations.

接下来几天，我会继续让 Claude 推送新的改动——如果你想跟进 Claude 为解决这些局限所做的持续尝试，可以关注仓库。

### Looking forward｜展望未来

Each generation of language models opens up new ways of working with them.

每一代语言模型都会开启与它们协作的新方式。

Early models were useful for tab-completion in IDEs.

早期模型的用处是在 IDE 里做 Tab 补全。

Before long, models could complete a function body from its docstring.

没过多久，模型就能根据文档字符串（docstring）补全整个函数体。

The launch of Claude Code brought agents into the mainstream and enabled developers to pair-program with Claude.

Claude Code 的发布让智能体走向主流，使开发者能够与 Claude 结对编程（pair-program）。

But each of these products operates under the assumption that a user defines a task, an LLM runs for a few seconds or minutes and returns an answer, and then the user provides a follow-up.

但这些产品都建立在同一个假设之上：用户定义一个任务，LLM 运行几秒或几分钟后返回一个答案，然后用户再给出后续指示。

Agent teams show the possibility of implementing entire, complex projects autonomously.

智能体团队则展示了自主实现完整复杂项目的可能性。

This allows us, as users of these tools, to become more ambitious with our goals.

这让我们这些工具的使用者，可以在目标上变得更有野心。

We are still early, and fully autonomous development comes with real risks.

我们仍处于早期阶段，而完全自主的开发伴随着切实的风险。

When a human sits with Claude during development, they can ensure consistent quality and catch errors in real time.

当有人在开发过程中陪着 Claude 时，他们可以保证质量的一致性，并实时发现错误。

For autonomous systems, it is easy to see tests pass and assume the job is done, when this is rarely the case.

而对于自主系统，人们很容易看到测试通过就认为工作已经完成——但实际上很少真是这样。

I used to work in penetration testing, exploiting vulnerabilities in products produced by large companies, and the thought of programmers deploying software they’ve never personally verified is a real concern.

我以前做过渗透测试（penetration testing），专门利用大公司产品里的漏洞，所以一想到程序员会部署他们从未亲自验证过的软件，我是真心感到担忧。

So, while this experiment excites me, it also leaves me feeling uneasy.

因此，这个实验虽然让我兴奋，也让我感到不安。

Building this compiler has been some of the most fun I’ve had recently, but I did not expect this to be anywhere near possible so early in 2026.

构建这个编译器是我最近最开心的事情之一，但我完全没想到在 2026 年这么早的时候，这件事就已经接近可能。

The rapid progress in both language models and the scaffolds we use to interact with them opens the door to writing an enormous amount of new code.

语言模型以及我们与之交互所用脚手架的快速进步，为编写海量新代码打开了大门。

I expect the positive applications to outweigh the negative, but we’re entering a new world which will require new strategies to navigate safely.

我预计正面应用会超过负面影响，但我们正在进入一个新世界，而在其中安全前行需要新的策略。

#### Acknowledgements｜致谢

Special thanks to Josef Bacik, Edwin Chen, Bernardo Meurer Costa, Jake Eaton, Dan Kelley, Felix Klock, Jannet Park, Steve Weis, and many other people across Anthropic for their assistance and contributions.

特别感谢 Josef Bacik、Edwin Chen、Bernardo Meurer Costa、Jake Eaton、Dan Kelley、Felix Klock、Jannet Park、Steve Weis，以及 Anthropic 内部许多其他同事的协助与贡献。
