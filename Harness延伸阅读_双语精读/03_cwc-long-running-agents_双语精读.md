# 03_cwc-long-running-agents_长时程智能体官方参考实现

> 原文：https://github.com/anthropics/cwc-long-running-agents
> 来源：Anthropic 官方 GitHub（Code with Claude 2026 活动示例代码）｜性质：参考实现，官方声明**不维护、不接受贡献**

## 📌 本篇速览

- 📅 2026-05（Code with Claude 2026）
- ⭐ ★★★★★ **必读，且是唯一可以直接抄代码的一篇** —— 它把 `/goal` 内部的三套机制拆出来变成你自己能装的 hook。综述里 default-FAIL 契约、证据门控、agent 自维护交接这三条，源头就是这个仓库。
- 🏷 default-FAIL contract、evidence gating、fresh-context evaluator、PROGRESS.md handoff、kill-switch、STEER.md
- 🗂 [返回专题目录](00_目录.md)　·　🔗 [Harness 最佳实践现状综述](../02_Agent-Harness最佳实践现状综述_2026-08.md)

> 本文是双语精读与转述，不是逐句全文翻译；英文保留关键术语与短表述，完整正文请点原文链接。

## 一句话摘要

把 Claude Code `/goal` 命令内部藏着的三套机制——**「没证据不许说成功」的结构性强制、「独立上下文的只读评审者」、「智能体自己维护的交接文档」**——拆成独立的 shell hook 和 subagent，任何项目 `cp -r` 就能装上。

## 核心内容

### 1. 三个质量循环原语（Three quality-loop primitives）

#### 原语一：Default-FAIL 契约（Default-FAIL Contract）

契约文件 `test-results.json` 里每个功能**初始都是 `false`**：

```json
{ "feature-1": { "passes": false }, "feature-2": { "passes": false } }
```

智能体**必须先用 Read 工具打开证据文件**，才被允许把某个功能翻成 `true`。两个 hook 配合完成强制：

| 文件 | 作用 |
|---|---|
| `hooks/track-read.sh` | 记录智能体每次读取证据文件（截图、console 日志、结果文件）|
| `hooks/verify-gate.sh` | 拦截对结果文件的 Write；`.evidence-reads` 计数器为 0 就**拒绝写入** |
| `.evidence-reads` | 内部计数器，**每次通过门控的写入后清零** |

原文把这条原则叫 **evidence-first principle**：*claimed success is backed by observed proof*（宣称的成功必须有观察到的证据支撑）。

> 官方自己标注了局限：*"The shipped hook is intentionally simple"* —— 生产环境的缺口（证据过期、文件内容校验）写在 `verify-gate.sh` 的注释里，需要自己补。

#### 原语二：Fresh-context evaluator（独立上下文评审者）

`agents/evaluator.md` 定义一个**没有 Write / Edit 工具**的子智能体，从一个**从未见过构建过程**的上下文窗口里审查 diff 与截图，只返回 `PASS` 或 `NEEDS_WORK` + 具体发现。

调用方式：

```bash
claude --agent evaluator -p "<review prompt>"
```

关键闭环设计：**`NEEDS_WORK` 的 findings 直接成为下一次 builder 会话的开场提示词**——评审结果不是报告，是下一轮的输入。

#### 原语三：Agent-maintained handoff（智能体自维护交接）

- 智能体自己往 `PROGRESS.md` 写会话笔记，**每次会话开始重读**；
- 在有意义的检查点 git commit，让 `git log` 成为持久记录；
- `hooks/commit-on-stop.sh` 作为兜底（backstop），会话结束时把未提交的工作提交掉。

### 2. 两个运维控制 hook（Operator controls）

| Hook | 行为 |
|---|---|
| `hooks/kill-switch.sh` | 项目根目录存在 `AGENT_STOP` 文件时，**halts every tool call** —— `touch AGENT_STOP` 即停 |
| `hooks/steer.sh` | 把根目录的 `STEER.md` **一次性**送到智能体面前，实现不重启的中途转向 |

### 3. 完整文件结构

```
claude-code-config/.claude/
├── CLAUDE.md                 # builder 的系统提示（含会话范围界定与交接指令）
├── agents/evaluator.md       # 独立评审子智能体（无 Write/Edit 工具）
├── hooks/
│   ├── track-read.sh         # 记录证据文件读取
│   ├── verify-gate.sh        # 无证据读取则拒绝写结果文件
│   ├── commit-on-stop.sh     # 会话结束兜底提交
│   ├── kill-switch.sh        # AGENT_STOP 急停
│   └── steer.sh              # 注入 STEER.md 中途转向
├── PROGRESS.md               # 智能体会话笔记（每次会话重读）
└── .evidence-reads           # 证据读取计数器
```

**安装三步**：

```bash
cp -r claude-code-config/.claude /path/to/your/project/
chmod +x /path/to/your/project/.claude/hooks/*.sh
```

然后按项目改写：建自己的 `test-results.json`、把 hook 里的 `RESULTS_FILE` 指向真实结果文件、改 `track-read.sh` 的证据文件匹配模式、把验收标准写进 `agents/evaluator.md`。

> ⚠️ **必须在含 `.claude/` 的那一层目录运行**——hooks 不会从子目录加载。

### 4. 两种跑法：`/goal` vs 自建 wrapper

**跑法 A：`/goal`（一行搞定）**

```
/goal every feature in PROGRESS.md is implemented, committed, and its tests pass
```

**跑法 B：自建 wrapper 循环（完全控制）**

```bash
while grep -q '"passes": false' test-results.json; do
  claude -p "Read PROGRESS.md and build the next unfinished feature per CLAUDE.md."
  VERDICT=$(claude --agent evaluator -p "Review the most recent commit against its spec.")
  [ "$(echo "$VERDICT" | head -1)" = "PASS" ] || echo "$VERDICT" > NEXT_FINDINGS.md
done
```

每一轮跑在全新上下文里；退出条件是契约完成、连续无变化、或预算耗尽。

官方给的对照表：

| 方面 | `/goal` | 自建 `evaluator.md` + wrapper |
|---|---|---|
| 谁跑循环 | 内置 fast model | 你自己的代码 |
| 谁判「做完」 | 独立 fast model 检查你的条件 | 你的 `evaluator.md`（无 Write/Edit） |
| 能跑在哪 | 交互式、headless、Remote Control | Claude Code hooks、headless wrapper、Agent SDK |
| 配置成本 | 一行 | 拷配置 + 建契约文件 + 写 wrapper |

### 5. 实时监控三条命令

```bash
watch -n 2 'tail -20 PROGRESS.md'              # 智能体的笔记
watch -n 5 'git log --oneline -8'              # 已保存的工作
watch -n 2 'wc -l < .claude/.evidence-reads'   # 证据读取数（门控写入后清零）
```

### 6. 模型升级后的消融指令（Re-simplify on model upgrades）

这是综述里「脚手架即技术债」最硬的官方出处，README 把它写成了操作步骤：

> 每次模型发布后，**一次注释掉一块 harness**。新模型漂移更少、自我界定范围的能力更强，`CLAUDE.md` 里的很多构造可能已经没必要了。要系统性地测——**「什么是承重的」会随能力变化**（*what's "load-bearing" changes with capability*）。

### 7. Going Further 里点名的进阶模式

- **Unattended loop**：外层脚本限制单次会话长度并自动启动下一轮
- **Planner agent**：第一次会话把简报展开成 `BUILD_PLAN.md` 供循环消费
- **Sprint contracts**：把每个功能的「done」定义写进 hook 会强制的文件里
- **Grading rubrics**：功能性 / 设计 / 工艺三维评分 + few-shot 示例
- **Browser-verified evaluator**：评审者**直接打开运行中的应用**，而不是信任截图（接 Playwright MCP 或 Claude in Chrome）
- **Hosted runtime**：交给 Claude Managed Agents 托管循环、沙箱与调度

## 可直接带走的工程结论

1. **「做完」必须是一个默认 false 的文件状态，不是模型的一句话**——把乐观偏差堵在文件系统层，而不是提示词层。
2. **门控要卡在「写入前有没有读过证据」**，这是可机械校验的；「你要认真验证」是不可校验的。
3. **评审者要剥夺写权限**——`agents/evaluator.md` 无 Write/Edit 不是省事，是防止它顺手把问题改掉从而失去评审独立性。
4. **评审结论要当成下一轮的输入提示词**，不要当成给人看的报告。
5. **急停要用文件而不是信号**（`touch AGENT_STOP`）——无人值守时人可能只有手机。
6. **中途转向要有专门通道**（`STEER.md`），否则唯一的转向方式是重启，等于丢掉全部上下文。
7. **模型升级后逐个注释组件**，官方明确承认很多构造会过期。

## 与库内其他笔记的关系

- 它是 [21_harness-design-long-running-apps](../Anthropic/Engineering全集_逐句对照/21_harness-design-long-running-apps_直观图解与学习笔记.md) 三角色架构的可执行版本，但把 planner 降格成了「进阶模式」之一。
- 它的 `PROGRESS.md` 直接继承 [15_effective-harnesses](../Anthropic/Engineering全集_逐句对照/15_effective-harnesses-for-long-running-agents_直观图解与学习笔记.md) 的 `claude-progress.txt`。
- 它是 [04_`/goal` 官方文档](04_goal-command-docs_双语精读.md) 的「拆开看内部」版本——同一套机制的两种交付形态。
- 托管化终点见 [01_New in Claude Managed Agents](01_new-in-claude-managed-agents_双语精读.md)。
