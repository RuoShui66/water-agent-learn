# B25_How Anthropic runs large-scale code migrations with Claude Code_Anthropic 如何用 Claude Code 跑大规模代码迁移

> 原文：https://claude.com/blog/ai-code-migration
> 来源：Claude Blog｜发布日期：2026-07-16

## 📌 本篇速览

- 📅 2026-07-16　｜　⏱ 约 12 分钟　｜　📄 约 2,100 词 / 6 图
- 🏷 代码迁移、Claude Code、多智能体、对抗式审查、验证循环、规则手册
- 🗂 [返回目录](00_目录与阅读进度.md)

本文介绍 Anthropic 内部如何用 Claude Code 完成大规模代码迁移：过去一个月里，单个开发者借助 Claude Fable 5、Opus 4.8 与 dynamic workflows 迁移了 10 个代码包。文章以两个案例展开——Jarred Sumner 用不到两周把 Bun 从 Zig 迁到 Rust（百万行代码、合并前测试 100% 通过），Mike Krieger 一个周末把 Python 代码库迁成 16.5 万行 TypeScript——并总结出一套六步法：先立裁判（judge），再建规则手册、依赖图与缺口清单，经压力测试后全量翻译，最后编译、运行、对齐行为。全文核心论点是"你修的不是代码，而是产出这些代码的流程（循环）"，并给出前置人力投入、对抗式审查、机械化验证、按模型档位分工等最佳实践。

---

Code migrations, projects that port a production codebase to a new language, were multi-year endeavors until recently.

代码迁移（code migration）——把一个生产代码库整体移植到新语言的项目——直到最近还是动辄数年的工程。

In the last month, individual developers at Anthropic migrated 10 code packages consisting of tens to hundreds of thousands of lines of code using Claude Fable 5, Claude Opus 4.8, and [dynamic workflows](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code).

而在过去一个月里，Anthropic 的单个开发者就用 Claude Fable 5、Claude Opus 4.8 和[动态工作流](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code)（dynamic workflows）迁移了 10 个代码包，规模从几万行到几十万行不等。

In this article we’ll cover two examples along with best practices from these projects.

本文将介绍其中两个案例，以及从这些项目中总结出的最佳实践。

Jarred Sumner, co-founder of Bun and Member of Technical Staff at Anthropic, used Claude Code to [migrate Bun from Zig to Rust](https://bun.com/blog/bun-in-rust).

Jarred Sumner——Bun 联合创始人、Anthropic 技术团队成员（Member of Technical Staff）——用 Claude Code [把 Bun 从 Zig 迁移到了 Rust](https://bun.com/blog/bun-in-rust)。

A million lines of code were produced in less than two weeks, with 100% of Bun's existing test suite passing in CI before merge.

不到两周就产出了一百万行代码，且合并前 Bun 现有的测试套件在 CI 中 100% 通过。

Nineteen regressions surfaced after merge and have all been fixed.

合并后出现了 19 个回归（regression），目前已全部修复。

The Rust port was shipped inside Claude Code in June.

这个 Rust 移植版已于 6 月随 Claude Code 一起上线。

Mike Krieger, co-lead of Anthropic Labs, migrated a Python codebase to 165,000 lines of TypeScript over a weekend.

Mike Krieger——Anthropic Labs 联合负责人——用一个周末把一个 Python 代码库迁移成了 16.5 万行 TypeScript。

This included hundreds of agents, eight phase gates, three adversarial review rounds, and a final parity check that diffed every command's output against the Python original.

这个过程动用了数百个 agent、8 道阶段闸门（phase gates）、3 轮对抗式审查（adversarial review），最后还做了一次对等性检查（parity check）：把每条命令的输出与 Python 原版逐一 diff 比对。

Claude Code’s new capabilities change the math for these long-deferred projects.

Claude Code 的新能力改变了这类被长期搁置的项目的经济账。

Below is the six-step process we now use, drawn from what these migrations taught us.

下面是我们现在使用的六步流程，提炼自这些迁移项目教给我们的经验。

The core insight is that you don’t fix the code.

核心洞察是：你修的不是代码。

**You fix the process (loop) that produced the code**.

**你修的是产出这些代码的流程（循环）**。

## What is an AI code migration?｜什么是 AI 代码迁移？

An AI code migration uses AI agents to port a production codebase to a new language or framework.

AI 代码迁移指用 AI agent 把生产代码库移植到新的语言或框架。

Instead of translating files by hand, engineers write migration rules and verification loops; agents then translate, compile, and test until the new code's behavior matches the original — compressing multi-year projects into weeks.

工程师不再逐个文件手工翻译，而是编写迁移规则和验证循环（verification loops）；然后由 agent 负责翻译、编译、测试，直到新代码的行为与原版一致——把原本数年的项目压缩到几周。

## **Why and when to migrate languages**｜为什么迁、什么时候迁

Before going straight into *the how*, it’s worth discussing *the when* and *why* because the assumptions around these projects have evolved.

在直接讲*怎么迁*之前，值得先聊聊*何时迁*和*为什么迁*，因为围绕这类项目的基本假设已经变了。

Teams launch migrations because of landscape changes between their initial build and current project.

团队启动迁移，通常是因为从最初构建到现在，技术格局发生了变化。

Either a known trade-off has become limiting, a better approach has emerged, or the original ecosystem is shrinking.

要么是当年已知的取舍开始成为限制，要么是出现了更好的方案，要么是原有生态正在萎缩。

For example, Jarred originally chose Zig because it offered C-level performance with radical simplicity, ideal for a solo founder “writing Bun in 1 year in a cramped Oakland apartment pre-LLM.”

例如，Jarred 当年选择 Zig，是因为它以极致的简洁提供了 C 级别的性能——对一个"在 LLM 时代之前、蜗居奥克兰的小公寓里用一年写出 Bun"的独立创始人来说是理想选择。

This simplicity came with known tradeoffs, [which he writes about here](https://bun.com/blog/bun-in-rust#just-be-really-smart-and-don-t-make-mistakes).

这种简洁自带一些已知代价，[他在这里写过](https://bun.com/blog/bun-in-rust#just-be-really-smart-and-don-t-make-mistakes)。

Fast forward to 2026.

时间快进到 2026 年。

Bun's CLI is getting over 10 million monthly downloads and is used extensively within Claude Code.

Bun 的 CLI 月下载量已超过 1000 万，并且在 Claude Code 内部被大量使用。

As recently as last quarter, those tradeoffs wouldn’t have been enough to justify freezing the roadmap and committing resources to a multi-quarter project.

就在上个季度，这些代价还不足以让人有理由冻结路线图、把资源投入一个跨多个季度的项目。

Migrating languages can deliver smaller, faster, and safer systems, but no one wants to pay for them.

语言迁移能换来更小、更快、更安全的系统，但没人愿意为它买单。

Software engineers have also had to contend with the career risk inherent in these formerly mega-projects.

软件工程师还不得不面对这类昔日超级工程固有的职业风险。

You could maintain two parallel code bases for quarters or years, and if the end result was 90% parity, you had a bigger headache than when you started.

你可能要并行维护两套代码库几个季度甚至几年，而如果最终结果只有 90% 的对等度，你的麻烦比开始前还大。

Now, the worst case scenario is you delete the branch and try again.

而现在，最坏的情况不过是删掉分支重来一次。

There still needs to be a justifiable business case.

当然，商业理由仍然需要成立。

While million line migrations no longer cost $3 to $4 million in engineering resources over the course of a four year project, they still cost tens to hundreds of thousands of dollars or more to execute.

百万行级迁移虽然不再需要"四年工期、300–400 万美元工程资源"，但执行起来仍要花费几万到几十万美元甚至更多。

The Bun migration, for example, consumed 5.9 billion uncached input tokens and 690 million output tokens — around $165,000 at API pricing.

例如 Bun 的迁移消耗了 59 亿未缓存输入 token 和 6.9 亿输出 token——按 API 定价约合 16.5 万美元。

The main portion of Mike’s port was 27 million tokens.

Mike 移植的主体部分则是 2700 万 token。

![figure-01](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a58f8844b99cec5d277a9ee_27e78c5a.png)

**Jarred’s million-line PR.**

**Jarred 的百万行 PR。**

**However, the migration case no longer needs to be existential.**

**不过，迁移的立项理由不再需要是生存级的了。**

A year of memory-bug patches in the changelog, or one chronic bottleneck, can now justify it.

变更日志里一年份的内存 bug 补丁，或者一个长期存在的瓶颈，如今就足以立项。

The compile step was the impetus for Mike's project.

编译这一步就是 Mike 项目的直接动因。

The internal tool his team works on ships to users as a single binary.

他团队开发的内部工具以单一二进制文件的形式交付给用户。

Producing that binary with the Python toolchain took roughly eight minutes per platform, totaling a 30-minute wait across the build matrix on every release.

用 Python 工具链生成这个二进制文件，每个平台大约要 8 分钟——每次发版横跨整个构建矩阵总共要等 30 分钟。

After the port, the same compile now takes about two seconds, the binary starts 6x faster, and the team was able to retire a separate deployment pipeline.

移植之后，同样的编译现在大约 2 秒完成，二进制启动快了 6 倍，团队还得以退役一条独立的部署流水线。

## **Why AI changes the code migration math**｜为什么 AI 改变了代码迁移的经济账

Claude Fable 5 is our most capable, generally available model.

Claude Fable 5 是我们能力最强、公开可用的模型。

Fable and Opus 4.8 are particularly good at delegating, directing, and verifying parallel workstreams with subagents while finding multiple paths towards stated goals.

Fable 和 Opus 4.8 特别擅长用子 agent（subagent）进行委派、指挥和并行工作流的验证，同时能针对既定目标找出多条实现路径。

Large code migrations are a particularly effective use case for these advanced models because:

大型代码迁移之所以是这些先进模型的绝佳用例，原因如下：

- **The work is parallel**. Work can be executed across thousands of independent units such as files and crates, so agents can work at the same time rather than have one waiting on the other.

- **工作天然并行**。任务可以拆分到数千个相互独立的单元（如文件、crate）上执行，agent 可以同时开工，而不是一个等着另一个。

- **Context is clear and comprehensive.**The old code serves as a great spec for the model. It also serves as a core reference to help build the guide for translation agents to follow.

- **上下文清晰而完备。**旧代码本身就是给模型的绝佳规格说明（spec），同时也是构建翻译 agent 所遵循指南的核心参考。

- **There is a built-in referee**. Many large codebases will include a test suite that agents can use to verify their work. Agents perform their best when verification is objective, because the model can grind against a ground truth for days without a human arbitrating quality.

- **自带裁判**。许多大型代码库都有测试套件，agent 可以用它验证自己的工作。验证客观时 agent 表现最好，因为模型可以对着基准真值（ground truth）连续打磨好几天，无需人来仲裁质量。

- **The queue writes itself**. When a compiler or test run fails, that becomes the next item for an agent to fix.

- **队列自己写自己**。编译或测试一失败，失败项就自动成为 agent 的下一个待修任务。

- **They require consistency and edge case handling**: The process is built so drift has nowhere to hide: reviewers cite the rule behind every finding, so a violation becomes a queue item instead of a quiet divergence. And when an agent does hit an edge case, the fix becomes a rule every subsequent agent follows.

- **迁移要求一致性和边缘情况处理**：整个流程的设计让偏差无处藏身——审查者对每个发现都要引用背后的规则，于是违规变成一个队列项，而不是悄无声息的发散。而当 agent 真的撞上边缘情况时，那个修复会沉淀为一条所有后续 agent 都遵守的规则。

As we will see below, both Mike and Jarred used Fable for key steps in their migration process, particularly in **an advisory pattern** that used multiple model classes to optimize token consumption.

正如下文将看到的，Mike 和 Jarred 都在迁移流程的关键步骤中使用了 Fable，尤其是采用了一种**顾问模式**（advisory pattern）：混用多个模型档位来优化 token 消耗。

## **Six steps for large code migrations**｜大型代码迁移六步法

*The process below has been generalized to be relevant to multiple languages and scenarios.*

*下面的流程已做泛化处理，适用于多种语言和场景。*

*For additional details, you can read*[*Jarred’s blog*](https://bun.com/blog/bun-in-rust)*.*

*更多细节可以阅读 [Jarred 的博客](https://bun.com/blog/bun-in-rust)。*

*You can also access the*[*Migration starter kit.*](https://github.com/anthropics/code-migration-kit-with-claude-code)

*你也可以获取[迁移入门套件（Migration starter kit）](https://github.com/anthropics/code-migration-kit-with-claude-code)。*

*Note: The starter kit is a generalized template of the process above — it's not what these specific ports ran on.*

*注意：starter kit 是上述流程的通用化模板——并不是这两个移植项目实际运行的代码。*

### **Prerequisites**｜前置条件

A prerequisite before starting on your migration project is to have a strong judge in place, otherwise you won’t have an exit condition or measure of success.

启动迁移项目之前的前置条件，是先建立一个强有力的裁判（judge），否则你既没有退出条件，也没有衡量成功的标准。

The judge must be able to evaluate both the original code and the target code on equal terms.

这个裁判必须能够以同等标准评估原始代码和目标代码。

Test suites written in the original language will often depend on internal functions that won't exist in the target code.

用原语言编写的测试套件往往依赖一些在目标代码中不存在的内部函数。

To build this judge:

构建这个裁判的方法：

- **Categorize existing tests**. Use Claude to identify which tests are expressible as external calls and which depend on internals that won't port.

- **给现有测试分类**。让 Claude 识别哪些测试可以表达为外部调用，哪些依赖无法移植的内部实现。

- **Rewrite for portability.** Convert the external-facing tests into assertions that can run against both the original and the port. Use adversarial agents to verify the rewritten tests don't weaken the assertions.

- **重写以获得可移植性。**把面向外部的测试改写成既能跑在原版、又能跑在移植版上的断言。并用对抗式 agent 验证改写后的测试没有削弱断言强度。

- **Validate the judge**. Run it against the original code to confirm it passes. Then run it against deliberately broken code to confirm it fails — a judge that doesn't catch breakage isn't a judge.

- **验证裁判本身**。先对原始代码跑一遍，确认它能通过；再对故意破坏的代码跑一遍，确认它会失败——抓不出破坏的裁判不配叫裁判。

Jarred had a large test suite written in a third language (TypeScript), but that will not be the case for most projects.

Jarred 恰好有一个用第三种语言（TypeScript）编写的大型测试套件，但大多数项目不会有这种运气。

For his Python-to-TypeScript port, Mike created a parity harness of seven real-world scenarios and considered any behavior change a bug to be fixed.

在 Python 到 TypeScript 的移植中，Mike 构建了一个包含七个真实场景的对等性测试框架（parity harness），并把任何行为变化都视为待修复的 bug。

Before we get into each stage, this graphic may help you follow along.

在逐步展开每个阶段之前，这张图可以帮你跟上思路。

This mostly follows Jarred’s methodology, with reviews and gates at each stage.

它主要遵循 Jarred 的方法论：每个阶段都设有审查和闸门。

Mike followed a similar overall structure using similar loop workflows, but he ran the entire migration end to end, revised the rules and the workflow based on the results, and ran it again — discarding the output each time until the third run.

Mike 采用了类似的整体结构和类似的循环工作流，但他的做法是端到端跑完整个迁移、根据结果修订规则和工作流、然后再跑一遍——每次都丢弃产出，直到第三次运行才保留。

![figure-02](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a58f8854b99cec5d277aa48_e7dd47de.png)

### **Step 1 — Create the rulebook, dependency map, and gap inventory**｜第一步——创建规则手册、依赖图与缺口清单

![figure-03](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a58fa78da7794274460319e_Code-migration-step1.jpeg)

In this stage we are creating the foundations of our migration: an inventory of places where code will need to be refactored rather than just translated, a rulebook for how to translate our code, and a dependency map to order our migration implementation workstreams.

这个阶段我们要打好迁移的地基，产出三样东西：一份"需要重构而非直接翻译"之处的清单、一本指导代码翻译的规则手册（rulebook），以及一张用来排定迁移实施工作流顺序的依赖图（dependency map）。

The order matters: the rulebook must come before the gap inventory.

顺序很重要：规则手册必须先于缺口清单（gap inventory）。

The gap inventory is defined by what the rulebook's defaults won't cover, and the two are tested together in a joint audit.

缺口清单的定义正是"规则手册的默认规则覆盖不到的部分"，而且两者要放在一起做联合审计（joint audit）。

#### **Rulebook**｜规则手册

The exact shape of the [rulebook](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/templates/RULEBOOK.md) depends on key architectural decisions you must make at the start.

[规则手册](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/templates/RULEBOOK.md)的具体形态取决于你在开局就必须拍板的关键架构决策。

Chief among them, if the new code will follow the same structure, or if it will be completely redesigned.

其中最重要的一条：新代码是保留原有结构，还是彻底重新设计。

If it’s the former (Jarred), the rulebook will primarily be lookup tables that translates types and idioms between languages while pointing to the gap inventory for the harder-to-translate components.

如果是前者（Jarred 的情况），规则手册主要是在两种语言之间转换类型和惯用法的查找表，难翻译的组件则指向缺口清单。

If it’s the latter (Mike), it will be a design document.

如果是后者（Mike 的情况），它就是一份设计文档。

Jarred created his rulebook by chatting with Claude, forming a policy for each area of ambiguity.

Jarred 通过与 Claude 对话来构建他的规则手册，为每一个存在歧义的领域形成一条策略（policy）。

He also used eight subagents specifically designed to review for 8 different categories of common failure modes based on his own intuition.

他还基于自己的直觉设计了 8 个专门的子 agent，分别审查 8 类不同的常见失败模式。

#### **Dependency map**｜依赖图

You need to understand file dependencies to effectively break up workstreams for a parallel migration so you know which files to migrate first and which files to contain in the same batch.

要为并行迁移有效地拆分工作流，你必须理解文件之间的依赖关系，才知道哪些文件先迁、哪些文件该放在同一批次里。

Some languages and codebases have explicit manifests that make this easy, but for legacy codebases and many popular languages like C/C++ and Python, these dependencies need to be discovered and mapped.

有些语言和代码库有显式的清单文件（manifest），这件事就很容易；但对于遗留代码库以及 C/C++、Python 这类流行语言，这些依赖关系需要被发现并映射出来。

Claude Code can deploy agents to create and run a deterministic script to produce this map.

Claude Code 可以部署 agent 来编写并运行一个确定性脚本，生成这张依赖图。

The [prompt in the migration kit](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/01-dependency-map.md) uses a workflow to create a review-and-fix loop.

[迁移套件里的这条提示词](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/01-dependency-map.md)用一个工作流构建了"审查—修复"循环。

*Note: The starter kit is a generalized template of the process laid out in this post — it's not what these specific ports ran on.*

*注意：starter kit 是本文所述流程的通用化模板——并不是这两个移植项目实际运行的代码。*

#### **Gap inventory and skeptic reviewers**｜缺口清单与怀疑派审查者

The new language has different requirements from the old language that must be met.

新语言有一些不同于旧语言、且必须满足的要求。

For Zig to Rust the difference was manual memory management (C and C++ work the same way).

对 Zig 到 Rust 而言，差异在于手动内存管理（C 和 C++ 的工作方式与之相同）。

For example:

例如：

Zig

```
fn readConfig(allocator: std.mem.Allocator) ![]u8 {
    const buf = try allocator.alloc(u8, 1024);
    // ...fill buf...
    return buf; // caller must free this — but only the comment says so
}

// A caller that forgets 'defer allocator.free(buf)' still compiles — the leak only surfaces at runtime.
```

Rust

```
fn read_config() -> Vec<u8> { 
let buf = vec![0u8; 1024]; 
// ...fill buf... 
buf // ownership moves to the caller; memory is freed automatically 
} 
// Use it after it's moved? Free it twice? Neither compiles. 
// Forget to free it? There's no free call to forget — drop is automatic.
```

For Python to TypeScript the gap was interfaces and contracts.

对 Python 到 TypeScript 而言，缺口在于接口（interface）与契约（contract）。

Python doesn’t require a contract declaring what shape of object it will accept or what it returns, but TypeScript does.

Python 不要求声明"接受什么形状的对象、返回什么"的契约，但 TypeScript 要求。

For example:

例如：

Python

```
def register(handler):
    handler.setup()
    return handler.run({"retries": 3})

# Any object with .setup() and .run() works here. Which objects actually get passed in? Read the whole codebase to find out.

```

TypeScript

```
interface RunResult { ok: boolean } 

interface Handler 
{ setup(): void; 
run(opts: { retries: number }): Promise<RunResult>; 
} 

function register(handler: Handler): Promise<RunResult> { 
handler.setup(); 
return handler.run({ retries: 3 }); } 

// The contract must be written down before this compiles
```

Both Jarred and Mike created gap inventory files capturing this implicit knowledge.

Jarred 和 Mike 都创建了缺口清单文件，把这类隐性知识固化下来。

Jarred inventoried these gaps up front, which is what we do here, while Mike chose to translate first and then create the gap inventory by auditing afterwards.

Jarred 在开工前就把缺口盘点了出来（也就是本流程采用的做法），而 Mike 选择先翻译、之后再通过审计来补建缺口清单。

You may need to do both.

你可能两种都需要做。

Check out this sample [Claude Code prompt to create a gap inventory file](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/02-gap-inventory.md).

可以参考这条示例：[用 Claude Code 创建缺口清单文件的提示词](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/02-gap-inventory.md)。

### **Step 2 — Stress-test the rules**｜第二步——压力测试规则

![figure-04](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a58fbe31db98b8b59d39ba8_MIgration-step2.jpeg)

This step involves a mini-migration that serves as a “shakedown cruise” for the larger migration.

这一步是做一次迷你迁移，充当大迁移之前的"试航"（shakedown cruise）。

In this step, Jarred used one agent to translate three files using the rulebook, one agent to translate three files “like a senior Rust engineer,” and one agent to use the diff to create new translation rules.

在这一步，Jarred 用一个 agent 按规则手册翻译三个文件，再用另一个 agent"像资深 Rust 工程师那样"翻译同样三个文件，然后让第三个 agent 根据两者的 diff 产出新的翻译规则。

At this stage he caught two critical issues that would have created numerous issues if fanned out across all 1,448 files.

在这个阶段他抓住了两个关键问题——如果扩散到全部 1,448 个文件，这两个问题会引发无数麻烦。

The prompt may look something like [this](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/03-stress-test.md).

提示词大概长[这样](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/03-stress-test.md)。

This type of stress test **only works for structure-preserving migrations**, where two translations of the same file are comparable line by line.

这种压力测试**只适用于保留结构的迁移**——同一文件的两份译文能够逐行比较。

If your rulebook is a redesign — like Mike's — the equivalent test is attacking the design document directly with adversarial reviewers, then validating it with a disposable end-to-end run.

如果你的规则手册是一份重新设计的文档——像 Mike 那样——等价的测试就是让对抗式审查者直接攻击这份设计文档，然后用一次"用完即扔"的端到端运行来验证它。

Regardless, throw out any translated files.

无论哪种情况，都要把翻译出来的文件全部扔掉。

The goal is to refine the rules, not make incremental progress.

目标是打磨规则，而不是攒进度。

### **Step 3 — Translate everything**｜第三步——全量翻译

![figure-05](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a58fd9c8899de91189a89e0_ai-migation-step4-5-6.jpeg)

For the remaining steps, you run the same multi-agent loop architecture: implement, review, and fix.

余下的各步都运行同一套多 agent 循环架构：实现、审查、修复。

You can offload implementer work to smaller models and keep reviewers on larger ones.

你可以把实现者（implementer）的工作卸载给较小的模型，让审查者保持用较大的模型。

For example, Mike used Claude Sonnet when he fanned out 12 subagents for the main migration.

例如，Mike 在为主迁移扇出（fan out）12 个子 agent 时用的就是 Claude Sonnet。

The work queue should be mechanical.

工作队列应当是机械化的。

A batch script decides what’s done by checking whether the translated file exists on disk, then slices the pending files into batches for the implementer agents.

一个批处理脚本通过检查"翻译后的文件是否已存在于磁盘上"来判定完成状态，然后把待处理文件切成批次，分给实现者 agent。

Because the queue is rebuilt from disk every time, the migration is resumable by construction.

由于队列每次都从磁盘重建，这个迁移在设计上天然可续跑（resumable by construction）。

At this stage, agents can be overly cautious with how much work they do.

在这个阶段，agent 对自己该做多少工作可能过于保守。

The fix can be a blunt, emphatic prompt instruction with context that the compiler will catch mistakes in the next step.

解法可以是一条直白、语气强硬的提示词指令，并附上背景说明：下一步编译器会兜住错误。

Anything the translator can’t execute confidently gets flagged with // TODO(port): <reason> to be dealt with in step 4.

翻译 agent 没有把握处理的内容，都用 // TODO(port): <reason> 标记出来，留到第四步处理。

From here on, the to-do lists write themselves: the compiler enumerates the errors, the smoke tests find the crashes, the suite reports the failures.

从这里开始，待办清单就自己写自己了：编译器枚举错误，冒烟测试（smoke test）找出崩溃，测试套件报告失败。

Two adversarial reviewers evaluate the work of the implementers using separate contexts and disagreement between reviewers goes to a third agent.

两个对抗式审查者在相互独立的上下文中评估实现者的工作，审查者之间的分歧交给第三个 agent 裁决。

When a reviewer keeps catching the same mistake across files, the fix isn't per-file.

当审查者在多个文件中反复抓到同一个错误时，修复就不该按文件来。

You add one sentence to the rulebook and regenerate the affected batch.

你往规则手册里加一句话，然后重新生成受影响的批次。

The rulebook keeps growing through this step; the code never gets hand-patched against it.

规则手册在这一步持续增长；代码从不针对它做手工补丁。

One important design decision to note in this step is where the compiler sits.

这一步有个值得注意的重要设计决策：编译器放在哪里。

Mike ran the TypeScript compiler inside every loop, because it checks a unit in seconds.

Mike 把 TypeScript 编译器放在每个循环内部运行，因为它检查一个单元只要几秒。

Jarred banned the compiler from the loop entirely and deferred it to the next step, because cargo takes minutes.

Jarred 则把编译器彻底逐出循环、推迟到下一步，因为 cargo 一跑就是几分钟。

At this step, much of the heavy lifting has been done and [the prompts start to get shorter.](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/04-translation-kickoff.md)

到了这一步，大部分重活已经干完，[提示词开始变短。](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/04-translation-kickoff.md)

### **Steps 4, 5, 6 — Compile, run, and match behavior**｜第四、五、六步——编译、运行、对齐行为

![figure-06](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a58fd76153c143199b57e1b_ai-migration-step3.jpeg)

These three steps share the same loop architecture and need progressively less human judgment, so we cover them together.

这三步共用同一套循环架构，且对人类判断的需求逐步递减，所以我们放在一起讲。

**Step 4**, for example, may often dissolve into step 3 depending on the language and size of the migration.

比如**第四步**，取决于迁移的语言和规模，往往可以直接并入第三步。

Depending on the size and difficulty of the compiler step, agents may not run this at all.

取决于编译步骤的规模和难度，agent 甚至可能完全不亲自跑它。

Jarred executed this with an orchestrator script that invoked the compiler once across the whole workspace.

Jarred 的做法是用一个编排（orchestrator）脚本，对整个工作区只调用一次编译器。

“Fixer agents” then ran through the error list in parallel with adversarial review.

然后由"修复 agent"（fixer agents）在对抗式审查的伴随下，并行清扫错误列表。

The build runs again, rinse and repeat.

再跑一次构建，如此往复。

Reviewing the error list is helpful to catch systemic issues that may require adjustments.

人工审阅错误列表有助于抓出可能需要调整的系统性问题。

For example, Jarred ran into thousands of Rust module errors that surfaced after fixing cyclic imports that Zig's lazy compilation tolerated.

例如，Jarred 在修复循环导入（Zig 的惰性编译对此是容忍的）之后，冒出了数千个 Rust 模块错误。

He fixed the loop by encoding logic to classify which dependence to delete, move, or restructure the boundary.

他的修法是修循环本身：把"哪种依赖该删除、该移动、该重构边界"的分类逻辑编码进流程。

**Step 5**also has a mechanical source of truth similar to the compiler error list: crashes from the smoke test.

**第五步**同样有一个类似编译错误列表的机械化事实来源：冒烟测试产生的崩溃。

Again, the loop fix was to group issues into categories, in this case grouping causes by root cause that are reviewed by adversarial subagents.

同样，对循环的修复是把问题归类——这里是按根因（root cause）分组，再交由对抗式子 agent 审查。

**Step 6** and the end of our story is comparing the programs’ behavior across the two codebases.

**第六步**——也是整个故事的收尾——是比较两个代码库中程序的行为。

Our files have now been translated, compiled, and smoke tested.

至此，我们的文件已经完成了翻译、编译和冒烟测试。

Now it's time to shard them and run the test suite (from the prerequisite stage) against them.

现在该把它们分片（shard），并用（前置条件阶段准备的）测试套件去跑它们。

Tackle failures with "fixer agents" that review the failed tests against both codebases.

用"修复 agent"来处理失败：它们对照两个代码库审查失败的测试。

Adversarial reviewers check their fixes.

对抗式审查者再检查这些修复。

The next stage in this loop is a [build daemon](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/scripts/build_daemon.sh), which is the only process allowed to rebuild the binary.

这个循环的下一环是[构建守护进程](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/scripts/build_daemon.sh)（build daemon）——唯一被允许重新构建二进制的进程。

Fixers write patches; the daemon batches them, rebuilds once, re-runs the affected tests, and feeds the results back.

修复 agent 写补丁；守护进程把补丁攒成批、只重建一次、重跑受影响的测试，再把结果反馈回去。

This serializes the most expensive operation instead of letting multiple agents trigger it independently.

这把最昂贵的操作串行化了，而不是任由多个 agent 各自独立触发它。

When the same failure repeats across many tests, the fix moves upstream: you amend the rule that produced the bug and regenerate only the files that rule touched.

当同一失败在很多测试中重复出现时，修复要上移到上游：修正产生这个 bug 的那条规则，只重新生成该规则触及的文件。

Mike's approach matters here, because many developers won't have a built-out or ported test suite.

Mike 的做法在这里很有参考价值，因为很多开发者并没有一套现成或已移植的测试套件。

Mike had Claude create a small script to run 7 real-world scenarios against both the new port and the original Python codebase, and diffed the results.

Mike 让 Claude 写了一个小脚本，把 7 个真实场景同时跑在新移植版和原始 Python 代码库上，然后 diff 比对结果。

Each failing scenario got its own fix agent, and the loop ran until all seven passed.

每个失败的场景都分到一个专属修复 agent，循环一直跑到七个场景全部通过。

Then he went one step further.

然后他又更进了一步。

Claude designed its own end-to-end test suite and ran it autonomously overnight, fixing what broke and re-running four nights in a row.

Claude 自己设计了一套端到端测试套件并在夜间自主运行：坏了就修、修完重跑，连跑了四个晚上。

As a result, it caught the paper cuts no scenario list would have predicted.

结果，它抓住了任何场景清单都预料不到的那些"小剐蹭"问题。

The lesson is that a missing test suite doesn't block this step.

这里的经验是：缺少测试套件并不会卡住这一步。

If you can't inherit a referee, have Claude build one.

如果你继承不到一个裁判，就让 Claude 造一个。

Your original codebase is the ground truth either way.

无论哪种方式，你的原始代码库都是基准真值。

## **Code migrations best practices**｜代码迁移最佳实践

Every run taught us something the previous one didn't.

每一次运行都教会我们上一次没学到的东西。

It’s a safe bet your next migration will teach you things this guide can't.

可以笃定地说，你的下一次迁移也会教给你本指南教不了的东西。

But a few practices held up across every project:

但有几条实践在每个项目中都站得住脚：

- **Don't follow this guide blindly.** Each migration is different. Treat this as a starting point, and plan your specific migration with Claude before committing to it.

- **不要盲目照搬本指南。**每次迁移都不一样。把它当作起点，在正式投入之前先和 Claude 一起规划你的具体迁移方案。

- **Don’t focus on individual failures.** Individual failures are the loop's job. Fixer agents burn those down. Your attention belongs on the patterns.

- **不要盯着单个失败。**单个失败是循环的职责，修复 agent 会把它们烧掉。你的注意力应该放在模式（pattern）上。

- **Make review adversarial and verification mechanical.** Adversarial review allows for longer running tasks and is often worth the token consumption. Let scripts — a compiler, a diff, a test suite — be the referee.

- **让审查对抗化、让验证机械化。**对抗式审查支撑更长时间运行的任务，通常值得那些 token 消耗。让脚本——编译器、diff、测试套件——来当裁判。

- **Don't use the largest model for everything.** Token spend concentrates in your loops, so design them deliberately. Smaller models handle the high-volume implementation fan-out well; save your largest model for reviewers and for anything that writes rules other agents will follow.

- **不要什么都用最大的模型。**token 开销集中在循环里，所以循环要精心设计。较小的模型能很好地承担大批量的实现扇出；把最大的模型留给审查者，以及任何要写下"其他 agent 都会遵循的规则"的环节。

- **Front-load the human hours.** The rulebook and the stress test are the most time-consuming. Everything after is mostly queues burning down.

- **把人力时间前置。**规则手册和压力测试最耗时间。之后的一切基本就是队列在燃尽。

- **Make the work queue mechanical and resumable.** Done should mean "the output file exists on disk."

- **让工作队列机械化、可续跑。**"完成"的定义应该是"输出文件已存在于磁盘上"。

## **Review loop results, not code**｜审查循环的结果，而不是代码

Jarred’s Bun migration is now in production, although every migration has tradeoffs.

Jarred 的 Bun 迁移现已投入生产，当然每次迁移都有取舍。

For example, about 4% of the Rust code sits inside "unsafe" blocks, mostly single-line pointer operations at C/C++ boundaries.

例如，约 4% 的 Rust 代码位于 "unsafe" 块中，大多是 C/C++ 边界上的单行指针操作。

But the new codebase is measurably better.

但新代码库有可度量的提升。

Every memory leak the team's tooling can detect has been fixed: one benchmark of 2,000 repeated builds dropped from 6,745 MB of memory to 609.

团队工具能检测到的每一个内存泄漏都已修复：一个 2,000 次重复构建的基准测试，内存占用从 6,745 MB 降到了 609 MB。

The binary is 19% smaller on Linux and Windows.

在 Linux 和 Windows 上，二进制文件小了 19%。

And cross-language optimization made it 2–5% faster across HTTP serving and real-world workloads like next build and tsc.

跨语言优化还让它在 HTTP 服务以及 next build、tsc 等真实工作负载上快了 2–5%。

Consider whether it’s time to re-run the math of your long deferred migration.

不妨想想：是不是该给你那个被长期搁置的迁移重新算一次账了。

Pick the codebase you've been tolerating and ask Claude what the migration process looks like for it.

挑出那个你一直在忍受的代码库，去问问 Claude：它的迁移流程会是什么样。

***Related***｜相关链接

- [*Migration starter kit*](https://github.com/anthropics/code-migration-kit-with-claude-code)*Note: The starter kit is a generalized template of the process above — it's not what these specific ports ran on.*

- [*迁移入门套件（Migration starter kit）*](https://github.com/anthropics/code-migration-kit-with-claude-code)*注意：starter kit 是上述流程的通用化模板——并不是这两个移植项目实际运行的代码。*

- [*Code-modernization plugin*](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization)*— for legacy modernization and framework upgrades rather than language ports*

- [*代码现代化插件（Code-modernization plugin）*](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization)*——面向遗留系统现代化和框架升级，而非语言移植*

- [*Dynamic workflows in Claude Code*](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code)

- [*Claude Code 中的动态工作流（Dynamic workflows）*](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code)


---

## 术语中英对照表

| 英文 | 中文 | 出处/说明 |
|---|---|---|
| rulebook | 规则手册 | 翻译策略与架构决策载体；结构保留型=映射查找表，重新设计型=设计文档 |
| dependency map | 依赖图 | 确定性脚本产出，用于切分并行工作流与排序 |
| gap inventory | 缺口清单 | 新语言显式要求、旧语言隐式处理的知识编目 |
| judge | 裁判 | 前置条件：能平等评估新旧两版代码的验证器 |
| parity harness | 对等性测试框架 | Mike 的七场景新旧行为 diff 框架 |
| structure-preserving migration | 结构保留型迁移 | 可逐行对比翻译结果（Zig→Rust） |
| redesign (migration) | 重新设计型迁移 | 规则手册变设计文档（Python→TS） |
| stress test / shakedown cruise | 压力测试 / 试航 | 3 文件迷你迁移，双路翻译对 diff |
| implementer / reviewer / fixer | 实现者 / 审查者 / 修复者 | 循环三角色 |
| adversarial review | 对抗式审查 | 双审查者独立上下文评估 + 第三方仲裁分歧 |
| skeptic reviewers | 怀疑派审查者 | Step 1 攻击规则条目的审查 agent |
| mechanical verification | 机械化验证 | 编译器 / diff / 测试套件当裁判 |
| work queue | 工作队列 | 从磁盘状态重建，完成=产物在磁盘上存在 |
| resumable by construction | 天生可恢复 | 队列机制的架构结果 |
| build daemon | 构建守护进程 | 唯一允许重建二进制的进程，串行化最贵操作 |
| smoke test | 冒烟测试 | Step 5 的机械事实来源（崩溃） |
| phase gates | 阶段闸门 | Mike 流程中的 8 道关卡 |
| advisory pattern | 顾问模式 | 多模型档位混用以优化 token 消耗 |
| queue burndown | 队列燃尽 | 人力前置之后剩余工作的形态 |
| `// TODO(port): <reason>` | 移植待办标记 | 翻译者没把握的内容标记后进入下一步队列 |
