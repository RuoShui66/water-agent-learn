# 03_Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet_用 Claude 3.5 Sonnet 刷新 SWE-bench Verified 的最高纪录

> 原文：https://www.anthropic.com/engineering/swe-bench-sonnet
> 作者：Anthropic Engineering｜发布日期：2025-01-06

## 📌 本篇速览

- 📅 2025-01-06　｜　⏱ 约 15 分钟　｜　📄 2,544 词 / 0 图
- ⭐ ★★★★☆ **强烈推荐** —— Anthropic「极简脚手架 + 精心设计工具」哲学的源头，Bash/str_replace 双工具正是 Claude Code 的雏形。
- 🏷 SWE-bench、智能体脚手架、工具设计、Claude 3.5 Sonnet、编码智能体
- 🗂 [返回总目录](00_目录与阅读进度.md)

Anthropic 介绍了围绕升级版 Claude 3.5 Sonnet 构建的极简智能体脚手架——仅一段提示词加 Bash 工具和字符串替换式编辑工具，就在 SWE-bench Verified 上取得 49% 的当时最高成绩。文章详细公开了两个工具的完整 spec 与设计思路（防错设计、绝对路径、精确单匹配替换），并通过真实日志演示了模型复现问题、修改代码、自我验证的完整流程，最后总结了运行该基准时在成本、评分、隐藏测试和多模态方面的挑战。

---

*Our latest model, the upgraded* [*Claude 3.5 Sonnet*](https://www.anthropic.com/news/3-5-models-and-computer-use)*, achieved 49% on SWE-bench Verified, a software engineering evaluation, beating the previous state-of-the-art model's 45%.*

*我们最新的模型——升级版 Claude 3.5 Sonnet——在软件工程评估基准 SWE-bench Verified 上取得了 49% 的成绩，超越了此前业界最先进（state-of-the-art）模型的 45%。*

*This post explains the "agent" we built around the model, and is intended to help developers get the best possible performance out of Claude 3.5 Sonnet.*

*本文将介绍我们围绕这个模型构建的"智能体"（agent），旨在帮助开发者把 Claude 3.5 Sonnet 的性能发挥到极致。*

[SWE-bench](https://www.swebench.com/) is an AI evaluation benchmark that assesses a model's ability to complete real-world software engineering tasks.

[SWE-bench](https://www.swebench.com/) 是一个 AI 评估基准（benchmark），用于衡量模型完成真实世界软件工程任务的能力。

Specifically, it tests how the model can resolve GitHub issues from popular open-source Python repositories.

具体来说，它测试模型解决来自热门开源 Python 仓库的 GitHub issue 的能力。

For each task in the benchmark, the AI model is given a set up Python environment and the checkout (a local working copy) of the repository from just before the issue was resolved.

对于基准中的每个任务，AI 模型会得到一个已配置好的 Python 环境，以及该 issue 被解决之前那一刻的仓库检出（checkout，即本地工作副本）。

The model then needs to understand, modify, and test the code before submitting its proposed solution.

随后，模型需要理解、修改并测试代码，然后提交它给出的解决方案。

Each solution is graded against the real unit tests from the pull request that closed the original GitHub issue.

每个解决方案都会用真实的单元测试来评分——这些测试来自当初关闭该 GitHub issue 的那个 pull request。

This tests whether the AI model was able to achieve the same functionality as the original human author of the PR.

这可以检验 AI 模型是否实现了与该 PR 的人类原作者相同的功能。

SWE-bench doesn't just evaluate the AI model in isolation, but rather an entire "agent" system.

SWE-bench 并不只是孤立地评估 AI 模型本身，而是评估整个"智能体"系统。

In this context, an "agent" refers to the combination of an AI model and the software scaffolding around it.

在这个语境下，"智能体"指的是 AI 模型与围绕它的软件脚手架（scaffolding）的组合。

This scaffolding is responsible for generating the prompts that go into the model, parsing the model's output to take action, and managing the interaction loop where the result of the model's previous action is incorporated into its next prompt.

这套脚手架负责生成输入给模型的提示词（prompt）、解析模型的输出以执行动作，并管理交互循环——即把模型上一步动作的结果并入下一轮提示词之中。

The performance of an agent on SWE-bench can vary significantly based on this scaffolding, even when using the same underlying AI model.

即便底层用的是同一个 AI 模型，脚手架的不同也会让智能体在 SWE-bench 上的表现产生显著差异。

There are many other benchmarks for the coding abilities of Large Language Models, but SWE-bench has gained in popularity for several reasons:

衡量大语言模型（Large Language Model）编码能力的基准还有很多，但 SWE-bench 之所以日益流行，有以下几个原因：

1. It uses real engineering tasks from actual projects, rather than competition- or interview-style questions;

1. 它使用来自真实项目的真实工程任务，而不是竞赛题或面试题；

2. It is not yet saturated—there's plenty of room for improvement. No model has yet crossed 50% completion on SWE-bench Verified (though the updated Claude 3.5 Sonnet is, at the time of writing, at 49%);

2. 它尚未饱和（saturated）——仍有大量提升空间。目前还没有任何模型在 SWE-bench Verified 上突破 50% 的完成率（不过截至撰写本文时，升级版 Claude 3.5 Sonnet 已达到 49%）；

3. It measures an entire "agent", rather than a model in isolation. Open-source developers and startups have had great success in optimizing scaffoldings to greatly improve the performance around the same model.

3. 它衡量的是完整的"智能体"，而非孤立的模型。开源开发者和创业公司在优化脚手架方面已经取得了很大成功，能够围绕同一个模型大幅提升性能。

Note that the original SWE-bench dataset contains some tasks that are impossible to solve without additional context outside of the GitHub issue (for example, about specific error messages to return).

需要注意，原始的 SWE-bench 数据集里包含一些不借助 GitHub issue 之外的额外上下文（context）就不可能解决的任务（例如，需要知道应返回哪条具体的错误信息）。

[SWE-bench-Verified](https://openai.com/index/introducing-swe-bench-verified/) is a 500 problem subset of SWE-bench that has been reviewed by humans to make sure they are solvable, and thus provides the most clear measure of coding agents' performance.

[SWE-bench-Verified](https://openai.com/index/introducing-swe-bench-verified/) 是 SWE-bench 的一个包含 500 道题的子集，经过人工审核以确保每道题都可解，因此它是对编码智能体性能最清晰的度量。

This is the benchmark to which we'll refer in this post.

本文所指的基准即为这个版本。

### Achieving state-of-the-art｜达到业界最先进水平

#### Tool Using Agent｜使用工具的智能体

Our design philosophy when creating the agent scaffold optimized for updated Claude 3.5 Sonnet was to give as much control as possible to the language model itself, and keep the scaffolding minimal.

在为升级版 Claude 3.5 Sonnet 打造优化的智能体脚手架时，我们的设计哲学是：把尽可能多的控制权交给语言模型本身，并让脚手架保持极简。

The agent has a prompt, a Bash Tool for executing bash commands, and an Edit Tool, for viewing and editing files and directories.

这个智能体只有一段提示词、一个用于执行 bash 命令的 Bash 工具（Bash Tool），以及一个用于查看和编辑文件与目录的编辑工具（Edit Tool）。

We continue to sample until the model decides that it is finished, or exceeds its 200k context length.

我们会持续采样（sample），直到模型自己决定任务已完成，或超出其 200k 的上下文长度。

This scaffold allows the model to use its own judgment of how to pursue the problem, rather than be hardcoded into a particular pattern or workflow.

这套脚手架让模型能够自行判断如何推进问题的解决，而不是被硬编码进某种特定的模式或工作流。

The prompt outlines a suggested approach for the model, but it's not overly long or too detailed for this task.

提示词为模型勾勒出一个建议的解题思路，但对于这类任务而言，它并不冗长，也不过分细致。

The model is free to choose how it moves from step to step, rather than having strict and discrete transitions.

模型可以自由决定如何从一步过渡到下一步，而不受严格、离散的状态转换约束。

If you are not token-sensitive, it can help to explicitly encourage the model to produce a long response.

如果你对 token 消耗不敏感，明确鼓励模型生成较长的回复会有所帮助。

The following code shows the prompt from our agent scaffold:

下面的代码展示了我们智能体脚手架中使用的提示词：

```plaintext
<uploaded_files>
{location}
</uploaded_files>
I've uploaded a python code repository in the directory {location} (not in /tmp/inputs). Consider the following PR description:

<pr_description>
{pr_description}
</pr_description>

Can you help me implement the necessary changes to the repository so that the requirements specified in the <pr_description> are met?
I've already taken care of all changes to any of the test files described in the <pr_description>. This means you DON'T have to modify the testing logic or any of the tests in any way!

Your task is to make the minimal changes to non-tests files in the {location} directory to ensure the <pr_description> is satisfied.

Follow these steps to resolve the issue:
1. As a first step, it might be a good idea to explore the repo to familiarize yourself with its structure.
2. Create a script to reproduce the error and execute it with `python <filename.py>` using the BashTool, to confirm the error
3. Edit the sourcecode of the repo to resolve the issue
4. Rerun your reproduce script and confirm that the error is fixed!
5. Think about edgecases and make sure your fix handles them as well

Your thinking should be thorough and so it's fine if it's very long.
```

The model's first tool executes Bash commands.

模型的第一个工具用于执行 Bash 命令。

The schema is simple, taking only the command to be run in the environment.

它的 schema 很简单，只接收一个要在环境中运行的命令。

However, the description of the tool carries more weight.

不过，这个工具的描述（description）承担了更重要的分量。

It includes more detailed instructions for the model, including escaping inputs, lack of internet access, and how to run commands in the background.

描述中包含了给模型的更详细的指令，包括输入转义、环境不能联网，以及如何在后台运行命令。

Next, we show the spec for the Bash Tool:

接下来展示 Bash 工具的规格定义（spec）：

```plaintext
{
   "name": "bash",
   "description": "Run commands in a bash shell\n
* When invoking this tool, the contents of the \"command\" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* State is persistent across command calls and discussions with the user.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Please avoid commands that may produce a very large amount of output.\n
* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.",
   "input_schema": {
       "type": "object",
       "properties": {
           "command": {
               "type": "string",
               "description": "The bash command to run."
           }
       },
       "required": ["command"]
   }
}
```

The model's second tool (the Edit Tool) is much more complex, and contains everything the model needs for viewing, creating, and editing files.

模型的第二个工具（编辑工具）要复杂得多，包含了模型查看、创建和编辑文件所需的全部能力。

Again, our tool description contains detailed information for the model about how to use the tool.

同样，我们在工具描述中为模型提供了关于如何使用该工具的详细信息。

We put a lot of effort into the descriptions and specs for these tools across a wide variety of agentic tasks.

我们针对各种各样的智能体任务，在这些工具的描述和规格定义上投入了大量精力。

We tested them to uncover any ways that the model might misunderstand the spec, or the possible pitfalls of using the tools, then edited the descriptions to preempt these problems.

我们对它们进行测试，找出模型可能误解规格定义的各种情形，或使用工具时可能踩到的坑，然后修改描述来预先规避这些问题。

We believe that much more attention should go into designing tool interfaces for models, in the same way that a large amount of attention goes into designing tool interfaces for humans.

我们认为，就像人们在为人类设计工具界面时投入了大量心血一样，为模型设计工具接口也应当获得远比现在更多的重视。

The following code shows the description for our Edit Tool:

下面的代码展示了我们编辑工具的描述：

```plaintext
{
   "name": "str_replace_editor",
   "description": "Custom editing tool for viewing, creating and editing files\n
* State is persistent across command calls and discussions with the user\n
* If `path` is a file, `view` displays the result of applying `cat -n`. If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep\n
* The `create` command cannot be used if the specified `path` already exists as a file\n
* If a `command` generates a long output, it will be truncated and marked with `<response clipped>` \n
* The `undo_edit` command will revert the last edit made to the file at `path`\n
\n
Notes for using the `str_replace` command:\n
* The `old_str` parameter should match EXACTLY one or more consecutive lines from the original file. Be mindful of whitespaces!\n
* If the `old_str` parameter is not unique in the file, the replacement will not be performed. Make sure to include enough context in `old_str` to make it unique\n
* The `new_str` parameter should contain the edited lines that should replace the `old_str`",
...
```

One way we improved performance was to "error-proof" our tools.

我们提升性能的一个办法，是给工具做"防错"（error-proof）设计。

For instance, sometimes models could mess up relative file paths after the agent had moved out of the root directory.

例如，当智能体离开根目录之后，模型有时会把相对文件路径搞错。

To prevent this, we simply made the tool always require an absolute path.

为了避免这种情况，我们干脆让工具始终要求使用绝对路径。

We experimented with several different strategies for specifying edits to existing files and had the highest reliability with string replacement, where the model specifies `old_str` to replace with `new_str` in the given file.

在指定如何编辑既有文件方面，我们试验了好几种不同策略，其中可靠性最高的是字符串替换（string replacement）：模型指定 `old_str`，将其替换为给定文件中的 `new_str`。

The replacement will only occur if there is exactly one match of `old_str`.

只有当 `old_str` 恰好匹配一处时，替换才会执行。

If there are more or fewer matches, the model is shown an appropriate error message for it to retry.

如果匹配多于或少于一处，模型会看到相应的错误信息，以便重试。

The spec for our Edit Tool is shown below:

我们编辑工具的规格定义如下所示：

```plaintext
...
   "input_schema": {
       "type": "object",
       "properties": {
           "command": {
               "type": "string",
               "enum": ["view", "create", "str_replace", "insert", "undo_edit"],
               "description": "The commands to run. Allowed options are: `view`, `create`, `str_replace`, `insert`, `undo_edit`."
           },
           "file_text": {
               "description": "Required parameter of `create` command, with the content of the file to be created.",
               "type": "string"
           },
           "insert_line": {
               "description": "Required parameter of `insert` command. The `new_str` will be inserted AFTER the line `insert_line` of `path`.",
               "type": "integer"
           },
           "new_str": {
               "description": "Required parameter of `str_replace` command containing the new string. Required parameter of `insert` command containing the string to insert.",
               "type": "string"
           },
           "old_str": {
               "description": "Required parameter of `str_replace` command containing the string in `path` to replace.",
               "type": "string"
           },
           "path": {
               "description": "Absolute path to file or directory, e.g. `/repo/file.py` or `/repo`.",
               "type": "string"
           },
           "view_range": {
               "description": "Optional parameter of `view` command when `path` points to a file. If none is given, the full file is shown. If provided, the file will be shown in the indicated line number range, e.g. [11, 12] will show lines 11 and 12. Indexing at 1 to start. Setting `[start_line, -1]` shows all lines from `start_line` to the end of the file.",
               "items": {
                   "type": "integer"
               },
               "type": "array"
           }
       },
       "required": ["command", "path"]
   }
}
```

### Results｜结果

In general, the upgraded Claude 3.5 Sonnet demonstrates higher reasoning, coding, and mathematical abilities than our prior models, and the [previous state-of-the-art](https://solverai.com/) model.

总体而言，升级版 Claude 3.5 Sonnet 在推理、编码和数学能力上都超过了我们此前的模型，也超过了[此前业界最先进](https://solverai.com/)的模型。

It also demonstrates improved agentic capabilities: the tools and scaffolding help put those improved abilities to their best use.

它的智能体能力（agentic capabilities）同样有所提升：工具和脚手架则帮助这些提升后的能力得到最充分的发挥。

| Model | Claude 3.5 Sonnet (new) | Previous SOTA | Claude 3.5 Sonnet (old) | Claude 3 Opus |
|---|---|---|---|---|
| SWE-bench Verified score | **49%** | 45% | 33% | 22% |

| 模型 | Claude 3.5 Sonnet（新版） | 此前 SOTA | Claude 3.5 Sonnet（旧版） | Claude 3 Opus |
|---|---|---|---|---|
| SWE-bench Verified 得分 | **49%** | 45% | 33% | 22% |

### Examples of agent behavior｜智能体行为示例

For running the benchmark, we used the [SWE-Agent](https://swe-agent.com/) framework as a foundation for our agent code.

在运行这个基准时，我们以 [SWE-Agent](https://swe-agent.com/) 框架作为智能体代码的基础。

In our logs below, we render the agent's text output, tool calls, and tool responses as THOUGHT, ACTION, and OBSERVATION, even though we don't constrain the model to a fixed ordering.

在下面的日志中，我们把智能体的文本输出、工具调用（tool call）和工具响应分别呈现为 THOUGHT、ACTION 和 OBSERVATION，尽管我们并没有把模型约束在固定的顺序里。

The code blocks below will walk through a typical case of the Sonnet 3.5 solving a SWE-bench problem.

下面的代码块将带你走一遍 Sonnet 3.5 解决 SWE-bench 问题的一个典型案例。

In this first block, you can see part of the initial prompt given to the model, with `{pr_description}` filled in with the real value from a SWE-bench task.

在第一个代码块里，你可以看到提供给模型的初始提示词的一部分，其中 `{pr_description}` 已被填入某个 SWE-bench 任务的真实内容。

Importantly, this task contains steps to reproduce the issue, which will give the model a valuable starting point to investigate.

重要的是，这个任务包含了复现该 issue 的步骤，这会给模型提供一个宝贵的排查起点。

```plaintext
<uploaded_files>
/repo
</uploaded_files>
I've uploaded a python code repository in the directory /repo (not in /tmp/inputs). Consider the following PR description:

<pr_description>
linear_model.RidgeClassifierCV's Parameter store_cv_values issue
#### Description
Parameter store_cv_values error on sklearn.linear_model.RidgeClassifierCV

#### Steps/Code to Reproduce
import numpy as np
from sklearn import linear_model as lm

#test database
n = 100
x = np.random.randn(n, 30)
y = np.random.normal(size = n)

rr = lm.RidgeClassifierCV(alphas = np.arange(0.1, 1000, 0.1), normalize = True, 
                                         store_cv_values = True).fit(x, y)

#### Expected Results
Expected to get the usual ridge regression model output, keeping the cross validation predictions as attribute.

#### Actual Results
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'

lm.RidgeClassifierCV actually has no parameter store_cv_values, even though some attributes depends on it.
```

The model responds and first uses the Edit Tool to view the repository structure.

模型开始响应，首先使用编辑工具查看仓库结构。

You can see the model's text output and tool call arguments under THOUGHT and ACTION, and part of the tool's output under OBSERVATION:

你可以在 THOUGHT 和 ACTION 下看到模型的文本输出与工具调用参数，在 OBSERVATION 下看到工具输出的一部分：

```plaintext
THOUGHT:
I'll help you implement the changes to satisfy the PR description. Let's follow the steps you outlined.

1. First, let's explore the repo structure:
ACTION (str_replace_editor):
command:
view

path:
/repo

OBSERVATION:
Here's the files and directories up to 2 levels deep in /repo, excluding hidden items:
/repo
/repo/PULL_REQUEST_TEMPLATE.md
/repo/ISSUE_TEMPLATE.md
/repo/sklearn
/repo/sklearn/decomposition
/repo/sklearn/kernel_ridge.py
/repo/sklearn/model_selection
/repo/sklearn/covariance
/repo/sklearn/cluster
/repo/sklearn/base.py
/repo/sklearn/dummy.py
/repo/sklearn/naive_bayes.py
...
```

Now that the model has a better understanding of the repository structure, it uses the Edit Tool to create a new script that it will use to reproduce the issue and test its fix:

在对仓库结构有了更清晰的了解之后，模型使用编辑工具创建了一个新脚本，用来复现该 issue 并测试自己的修复：

```plaintext
THOUGHT:
Based on the repository structure, we'll need to modify the Ridge Classifier in the `sklearn/linear_model` directory.

Let's create a script to reproduce the error:
ACTION (str_replace_editor):
command:
create

path:
/repo/reproduce_error.py

file_text:
import numpy as np
from sklearn import linear_model as lm

#test database
n = 100
x = np.random.randn(n, 30)
y = np.random.normal(size = n)

rr = lm.RidgeClassifierCV(alphas=np.arange(0.1, 1000, 0.1), normalize=True, 
                         store_cv_values=True).fit(x, y)

OBSERVATION:
File created successfully at: /repo/reproduce_error.py
```

The model then uses the Bash Tool to execute the script it wrote, and successfully reproduces the issue from the task:

接着，模型使用 Bash 工具执行自己刚写的脚本，成功复现了任务中的 issue：

```plaintext
THOUGHT:
Let's verify that we can reproduce the error:
ACTION (bash):
command:
python3 /repo/reproduce_error.py

OBSERVATION:
Traceback (most recent call last):
  File "/repo/reproduce_error.py", line 10, in <module>
    store_cv_values=True).fit(x, y)
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
```

From here on, the model uses the Edit Tool to change the source code in the repository and reruns its script to verify whether the change has resolved the issue:

从这里开始，模型使用编辑工具修改仓库中的源代码，并重新运行自己的脚本来验证改动是否解决了问题：

```plaintext
THOUGHT:
The error is reproducible. Looking at the code, I can see that the issue is that while the `RidgeClassifierCV` class inherits from `_BaseRidgeCV`, it fails to pass the `store_cv_values` parameter from its constructor through to the base class constructor.

Let's fix this:
ACTION (str_replace_editor):
command:
str_replace

path:
/repo/sklearn/linear_model/ridge.py

old_str:
    def __init__(self, alphas=(0.1, 1.0, 10.0), fit_intercept=True,
                 normalize=False, scoring=None, cv=None, class_weight=None):
        super(RidgeClassifierCV, self).__init__(
            alphas=alphas, fit_intercept=fit_intercept, normalize=normalize,
            scoring=scoring, cv=cv)
        self.class_weight = class_weight

new_str:
    def __init__(self, alphas=(0.1, 1.0, 10.0), fit_intercept=True,
                 normalize=False, scoring=None, cv=None, class_weight=None,
                 store_cv_values=False):
        super(RidgeClassifierCV, self).__init__(
            alphas=alphas, fit_intercept=fit_intercept, normalize=normalize,
            scoring=scoring, cv=cv, store_cv_values=store_cv_values)
        self.class_weight = class_weight
```

In this particular example, the model worked for 12 steps before deciding that it was ready to submit.

在这个具体的例子中，模型工作了 12 步之后判断可以提交了。

The task's tests then ran successfully, verifying that the model's solution addressed the problem.

随后该任务的测试成功通过，验证了模型的解决方案确实解决了问题。

Some tasks took more than 100 turns before the model submitted its solution; in others, the model kept trying until it ran out of context.

有些任务模型要经过 100 多个回合（turn）才提交解决方案；还有一些任务里，模型会一直尝试，直到耗尽上下文。

From reviewing attempts from the updated Claude 3.5 Sonnet compared to older models, updated 3.5 Sonnet self-corrects more often.

对比升级版 Claude 3.5 Sonnet 与旧模型的尝试记录可以发现，升级版 3.5 Sonnet 更频繁地进行自我纠错（self-correct）。

It also shows an ability to try several different solutions, rather than getting stuck making the same mistake over and over.

它还表现出尝试多种不同解决方案的能力，而不是卡在原地反复犯同一个错误。

### Challenges｜挑战

SWE-bench Verified is a powerful evaluation, but it's also more complex to run than simple, single-turn evals.

SWE-bench Verified 是一个很有威力的评估，但比起简单的单轮评估（single-turn eval），它跑起来也复杂得多。

These are some of the challenges that we faced in using it—challenges that other AI developers might also encounter.

以下是我们在使用它的过程中遇到的一些挑战——其他 AI 开发者也可能会碰到。

1. **Duration and high token costs.** The examples above are from a case that was successfully completed in 12 steps. However, many successful runs took hundreds of turns for the model to resolve, and >100k tokens. The updated Claude 3.5 Sonnet is tenacious: it can often find its way around a problem given enough time, but that can be expensive;

1. **耗时长、token 成本高。** 上面的示例来自一个 12 步就成功完成的案例。然而，许多成功的运行需要模型花费数百个回合、消耗超过 10 万 token 才能解决问题。升级版 Claude 3.5 Sonnet 非常"顽强"（tenacious）：只要给它足够的时间，它往往能绕过难关解决问题，但代价可能很昂贵；

2. **Grading.** While inspecting failed tasks, we found cases where the model behaved correctly, but there were environment setup issues, or problems with install patches being applied twice. Resolving these systems issues is crucial for getting an accurate picture of an AI agent's performance.

2. **评分（Grading）。** 在检查失败的任务时，我们发现有些案例中模型的行为其实是正确的，问题出在环境配置上，或是安装补丁被重复应用了两次。解决这些系统层面的问题，对于准确评估一个 AI 智能体的性能至关重要。

3. **Hidden tests.** Because the model cannot see the tests it's being graded against, it often "thinks" that it has succeeded when the task actually is a failure. Some of these failures are because the model solved the problem at the wrong level of abstraction (applying a bandaid instead of a deeper refactor). Other failures feel a little less fair: they solve the problem, but do not match the unit tests from the original task.

3. **隐藏测试（Hidden tests）。** 由于模型看不到用来给它评分的测试，它经常"以为"自己成功了，而任务实际上是失败的。其中一部分失败是因为模型在错误的抽象层次上解决了问题（打了个"创可贴"式的补丁，而不是做更深层的重构）。另一些失败则显得不太公平：它们确实解决了问题，只是与原任务的单元测试对不上。

4. **Multimodal.** Despite the updated Claude 3.5 Sonnet having excellent vision and multimodal capabilities, we did not implement a way for it to view files saved to the filesystem or referenced as URLs. This made debugging certain tasks (especially those from Matplotlib) especially difficult, and also prone to model hallucinations. There is definitely low-hanging fruit here for developers to improve upon—and SWE-bench has launched a new [evaluation focused on multi-modal tasks](https://www.swebench.com/multimodal.html). We look forward to seeing developers achieve higher scores on this eval with Claude in the near future.

4. **多模态（Multimodal）。** 尽管升级版 Claude 3.5 Sonnet 拥有出色的视觉与多模态能力，我们却没有实现让它查看保存在文件系统里或以 URL 形式引用的图片文件的方式。这使得某些任务（尤其是来自 Matplotlib 的任务）的调试变得格外困难，也更容易诱发模型幻觉（hallucination）。这里显然存在开发者可以轻松摘取的"低垂果实"——而且 SWE-bench 已经推出了一个新的[专注于多模态任务的评估](https://www.swebench.com/multimodal.html)。我们期待在不久的将来，看到开发者用 Claude 在这个评估上取得更高的分数。

The upgraded Claude 3.5 Sonnet achieved 49% on SWE-bench Verified, beating the previous state-of-the-art (45%), with a simple prompt and two general purpose tools.

升级版 Claude 3.5 Sonnet 仅凭一段简单的提示词和两个通用工具，就在 SWE-bench Verified 上取得了 49% 的成绩，超越了此前业界最先进的水平（45%）。

We feel confident that developers building with the new Claude 3.5 Sonnet will quickly find new, better ways to improve SWE-bench scores over what we've initially demonstrated here.

我们有信心，基于新版 Claude 3.5 Sonnet 进行开发的开发者们，很快就会找到新的、更好的方法，把 SWE-bench 分数提升到超过我们在此初步展示的水平。

### Acknowledgements｜致谢

Erik Schluntz optimized the SWE-bench agent and wrote this blog post.

Erik Schluntz 优化了 SWE-bench 智能体并撰写了这篇博客文章。

Simon Biggs, Dawn Drain, and Eric Christiansen helped implement the benchmark.

Simon Biggs、Dawn Drain 和 Eric Christiansen 协助实现了这个基准。

Shauna Kravec, Dawn Drain, Felipe Rosso, Nova DasSarma, Ven Chandrasekaran, and many others contributed to training Claude 3.5 Sonnet to be excellent at agentic coding.

Shauna Kravec、Dawn Drain、Felipe Rosso、Nova DasSarma、Ven Chandrasekaran 以及许多其他同事，为把 Claude 3.5 Sonnet 训练成出色的智能体编码模型做出了贡献。
