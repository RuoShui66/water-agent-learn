# 04_Keep Claude working toward a goal_让 Claude 朝一个目标持续工作（`/goal` 官方文档）

> 原文：https://code.claude.com/docs/en/goal
> 来源：Claude Code 官方文档｜要求版本：**v2.1.139 或更高**

## 📌 本篇速览

- 📅 2026-05 中旬起（随 v2.1.139 发布）
- ⭐ ★★★★★ **必读** —— 「评估器外循环」被压缩成一条命令的官方形态。**「写条件」这一节是整篇最值钱的部分**，因为它就是三月文章「冲刺契约」的官方模板。
- 🏷 `/goal`、completion condition、prompt-based Stop hook、small fast model、auto mode 正交组合
- 🗂 [返回专题目录](00_目录.md)　·　🔗 [Harness 最佳实践现状综述](../02_Agent-Harness最佳实践现状综述_2026-08.md)

> 本文是双语精读与转述，不是逐句全文翻译；英文保留关键术语与短表述，完整正文请点原文链接。

## 一句话摘要

`/goal` 设定一个**完成条件（completion condition）**，每轮结束后由一个**独立的小快模型**判断条件是否成立；不成立就自动开下一轮，成立就自动清除目标——**本质上是一个会话级的 prompt-based Stop hook 封装**。

## 核心内容

### 1. 它解决什么问题：三种「让会话继续」的方式对照

官方给的这张表是选型依据，按「下一轮由什么触发」区分：

| 方式 | 下一轮什么时候开始 | 什么时候停 |
|---|---|---|
| **`/goal`** | 上一轮结束时 | 一个模型确认条件已满足 |
| **`/loop`** | 一个时间间隔过去 | 你手动停，或 Claude 判断工作已完成 |
| **Stop hook** | 上一轮结束时 | 你自己的脚本或提示词决定 |

`/goal` 与 Stop hook 都在每轮后触发，区别是：**`/goal` 是会话级快捷方式**（只对当前会话有效），**Stop hook 住在设置文件里**（对作用域内所有会话生效，且可以跑脚本做确定性检查）。

### 2. 与 auto mode 的正交关系（面试常考）

官方原话说得很清楚：

> Auto mode 单独使用时只在**单轮之内**自动批准工具调用，但**不会开启新的一轮**；Claude 自己判断工作做完就停。`/goal` 加了一个**独立的评估器**在每轮后检查你的条件，所以「完成」是由一个**新鲜的模型**判定，而不是由干活的那个模型判定。

一句话记法：**auto mode 消除逐工具审批，`/goal` 消除逐轮催促——两者互补而非替代。**

### 3. 怎么写一个好条件（本篇最核心）

先记住评估器的**硬约束**：

> The evaluator **doesn't run commands or read files independently** —— 它只能根据 Claude 已经在对话里"surfaced"出来的内容做判断。

所以条件必须写成**「Claude 自己的输出能证明」**的形式。官方举的正例：「All tests in `test/auth` pass」之所以可行，是因为 Claude 会去跑测试，而结果会落到 transcript 里供评估器读取。

**能撑过多轮的条件通常有三件套**（这就是冲刺契约的官方版）：

| 要素 | 英文 | 例子 |
|---|---|---|
| 一个**可度量的终态** | One measurable end state | 测试结果、构建退出码、文件数量、空队列 |
| 一个**明示的验证方式** | A stated check | `npm test` exits 0、`git status` is clean |
| **要紧的约束** | Constraints that matter | 「no other test file is modified」 |

外加第四件——**兜底上限**：把轮次或时间子句写进条件本身，例如 `or stop after 20 turns`。Claude 每轮汇报对该子句的进度，评估器从对话里判断。

> 📏 **条件长度上限 4,000 字符。**

官方给的适用场景（都是「有可验证终态的实质性工作」）：把模块迁到新 API 直到所有调用点编译且测试通过；实现设计文档直到所有验收标准成立；把大文件拆分直到每个都小于尺寸预算；清空一个带标签的 issue 待办队列。

### 4. 命令三态

一个会话同时只能有一个活跃目标，同一条命令按参数分设定/查看/清除：

```text
/goal all tests in test/auth pass and the lint step is clean
```

- **设定即开跑**：设定目标会**立刻起一轮**，条件本身就是指令，不需要再发提示词。活跃时显示 `◎ /goal active` 指示器。
- **`/goal`（无参数）查看状态**：条件、已运行时长、已评估轮数、当前 token 花费、**评估器最近一次给的理由**。
- **`/goal clear` 清除**：`stop` / `off` / `reset` / `none` / `cancel` 都是它的别名；跑 `/clear` 开新对话也会一并清掉。

⚠️ **目标不改变权限**。默认权限模式下 Claude 仍会为设置未放行的工具调用询问你。要让 goal 轮真正无人值守，**必须配 auto mode**。

**恢复行为**：会话结束时仍活跃的目标，在 `--resume` / `--continue` 时会被恢复——但**轮数、计时器、token 花费基线全部重置**。已达成或已清除的目标不恢复。

### 5. 非交互式跑法

```bash
claude -p "/goal CHANGELOG.md has an entry for every PR merged this week"
```

用 `-p` 设定目标会在**单次调用内把整个循环跑完**。

⚠️ 默认文本输出下**条件满足前什么都不打印**，跑很多轮时看起来像卡死了。加 `--output-format stream-json --verbose` 可以逐条输出。Ctrl+C 中断。

### 6. 评估机制（How evaluation works）

- `/goal` 是**会话级 prompt-based Stop hook** 的封装。
- 每轮结束，Claude Code 把**条件 + 至今为止的对话**发给你配置的 **small fast model**（Claude API 上默认 **Haiku**；第三方 provider 看各自平台默认）。
- 模型回答 yes / no 并给一句简短理由。**No** → Claude 继续干，并**把这个理由当作下一轮的指导**；**Yes** → 清除目标，在 transcript 里记一条 achieved。
- 换评估模型：设 `ANTHROPIC_DEFAULT_HAIKU_MODEL`。

> ⚠️ **官方警告**：`ANTHROPIC_DEFAULT_HAIKU_MODEL` 是全局生效的——Claude Code 在所有用到 small fast model 的地方都读它，`haiku` 别名和后台功能（如对话摘要）也会一起跑到那个模型上。

> 💰 评估 token 计在 small fast model 上，相对主轮花费通常可忽略。

### 7. 使用前提

`/goal` **只在你已接受信任对话框（trust dialog）的工作区里可用**，因为评估器属于 hooks 系统。以下情况不可用（命令会明确告诉你原因，而不是静默失效）：

- 任何设置层级设了 `disableAllHooks`
- 托管设置里设了 `allowManagedHooksOnly`

## 可直接带走的工程结论

1. **判定「完成」的模型必须不是干活的那个模型**——这是 `/goal` 相对 auto mode 唯一的、也是全部的架构增量。
2. **条件必须写成 transcript 里可证明的形式**。评估器不跑命令、不读文件，写「代码质量好」等于没写。
3. **四件套模板背下来**：可度量终态 + 明示验证方式 + 过程约束 + 轮次/时间上限。
4. **一定要写兜底上限**（`or stop after 20 turns`），否则条件写歪了就是无限烧钱。
5. **`/goal` 不放权限，auto mode 才放**——无人值守必须两个一起配。
6. 需要**确定性检查**（跑脚本、查退出码）就别用 `/goal`，直接写脚本型 Stop hook——`/goal` 的评估器只会读对话。
7. headless 跑长目标记得加 `--output-format stream-json --verbose`，否则无法判断是在干活还是挂了。

## 与库内其他笔记的关系

- 它是 [03_cwc-long-running-agents](03_cwc-long-running-agents_双语精读.md) 里那套机制的产品封装版——那个仓库就是把 `/goal` 拆开给你看。
- 它产品化的是 [21_harness-design-long-running-apps](../Anthropic/Engineering全集_逐句对照/21_harness-design-long-running-apps_直观图解与学习笔记.md) 的**冲刺契约**与**评估器外循环**。
- 与 [22_claude-code-auto-mode](../Anthropic/Engineering全集_逐句对照/22_claude-code-auto-mode_逐句对照.md) 是正交互补关系，无人值守长跑必须两者同时配。
