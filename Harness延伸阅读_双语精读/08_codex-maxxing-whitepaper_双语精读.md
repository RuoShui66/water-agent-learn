# 08_Codex-maxxing for long-running work_为长时程工作「榨干」Codex（OpenAI 白皮书）

> 原文：https://openai.com/index/codex-maxxing-long-running-work/
> PDF 全文：https://cdn.openai.com/pdf/8a9f00cf-d379-4e20-b06f-dd7ba5196a11/OAI_WhitePaper_Codex-maxxing26.pdf
> 来源：OpenAI 官方白皮书（27 页）｜发布日期：2026-06-22｜取材自创作者 **Jason Liu** 的日常工作流

## 📌 本篇速览

- 📅 2026-06-22
- ⭐ ★★★★☆ **值得读，但要知道它是什么** —— 这**不是一篇工程架构论文**，而是一份**工作流实践指南**（10 个 section，图文为主）。它的价值在于展示 OpenAI 侧对长时程的产品答案：把 harness 提到**工作区层**。「弱目标 vs 强目标」那一节和 Anthropic 的冲刺契约是同一件事的不同措辞。
- 🏷 durable threads、memory vault、thread automations、steering、side panel、strong goal
- 🗂 [返回专题目录](00_目录.md)　·　🔗 [Harness 最佳实践现状综述](../02_Agent-Harness最佳实践现状综述_2026-08.md)

> 本文是双语精读与转述，不是逐句全文翻译；英文保留关键术语与短表述，完整正文请点原文链接。

## 一句话摘要

把 Codex 从「一次性提示-响应工具」变成**工作可以持续存在的地方**（*gives work somewhere to live*）——靠 durable threads、memory vault、thread automations、steering、side panel 这五件套，把单次提示变成一个**运转的循环**（operating loop）。

## 核心内容

白皮书共 10 节，按「让工作有地方待 → 把思考灌进去 → 给它记忆和工具 → 让它自己回来 → 定可验证的目标」的顺序展开。

### 1. Durable threads（持久线程）：给工作一个安身之处

对于重要的工作流，**一个 pinned thread 可以成为工作的家**——上下文、偏好、旧决策、未闭合的循环都在这里累积。

白皮书举的五个持久线程例子：社交反馈监控、开源项目维护（issues / 维护者 / 贡献模式 / release notes）、OpenAI CLI（命令 / 约定 / 仓库结构 / 评审偏好）、Agents SDK、**Chief of Staff**（消息 / 跟进 / 会议 / 未闭环事项）。

⚠️ **官方明确写出的权衡**：

> 长线程携带上下文，**运行成本可能高于一个全新的短线程**。对重要工作流，连续性值得这个代价。

### 2. Voice input（语音输入）：把「乱的那版想法」交给模型

论点不是速度，而是**语音输入常常包含未经编辑的原始版本**：记不全的名字、松散的方向、不确定性——那些打字很别扭、但说出来很自然的东西。

> *"A lot of plans get better when the model has access to the messy version of what you think."*
> 当模型能拿到你脑子里那个**乱糟糟的版本**时，很多计划会变得更好。

会议记录、通话转写、走廊对话的语音笔记都可以当起始素材。

### 3. Steering（转向）：在它干活的时候塞下一条指令

**Steering = 在 Codex 已经在工作时追加下一条指令**：修正方向、补充上下文、批准下一步、或在某次工具调用后排队下一个动作。

白皮书给的语气示例：「这个改小点」「这段文案不对」「这两个东西之间的间距感觉不对」「做完之后开个 PR」「等预览部署完成」「在发布任何东西之前先给我看预览链接」。

> 📌 这与 Anthropic 侧 `STEER.md` 是同一个需求的两种实现：**长跑必须有不重启的转向通道**。

### 4. Memory（记忆）：让记忆成为可评审的东西

核心主张：**有用的上下文应该变成你能打开、编辑、diff、复用的东西**（*something you can open, edit, diff, and reuse*）。

**一条要记牢的边界划分**：

> **Repositories hold code. The vault holds rolling context around the work.**
> 仓库装代码，vault 装工作周边的滚动上下文。

vault 里装的是：人、决策、未闭环事项、日常笔记、项目状态——那些否则会在线程之间丢失的细节。

**当 vault 存在 GitHub 里时，diff 就成了记忆的评审面（review surface）**：你能看见 Codex 认为什么重要到值得写下来。

白皮书给的记忆指令模板（Memory instruction）：

- 有人被提到时，更新相关的人物笔记
- 项目推进时，更新项目页
- 循环闭合时，标记为已关闭
- 做出决策时，写下决策**以及它为什么重要**

原则一句话：**长线程不应该在对话历史里静悄悄地攒模糊印象，它们应该记录「什么变了」。**

### 5. Computer and browser use：决定这个线程能碰什么

按「能碰的表面」分类，这个分法本身值得记：

| 表面 | 用途 |
|---|---|
| `$browser` | 本地 web 界面、预览、批注 |
| `@computer` | 只能靠点击完成的 GUI 工作 |
| `@chrome` | **已登录的浏览器会话**、已认证的标签页 |
| Connectors | Slack、Gmail、Calendar、GitHub 等工作面 |
| Skills | 可复用、可重复的工作流 |

选型规则：迭代本地应用用 browser；依赖登录态或多个已认证标签用 Chrome；只能通过桌面应用完成的用 computer use，且**配清晰权限与评审**。

**Skills 的定位**：一个工作流跑通之后，把指令、参考资料、脚本打包，**让 Codex 不必每次重学**。

### 6. Remote control（远程控制）：让长循环可携带

Codex 在你文件、权限、本地配置所在的那台机器上继续工作，你可以**从另一台设备**签入、查看它发现了什么、回答问题、批准下一步或改变方向。

> **Remote control is not a reason to skip reviews.**（远程控制不是跳过评审的理由。）它只是让你**保持足够的注意力去解锁下一步**。

### 7. Thread automations（线程自动化）：让它自己回来

这是本篇最有产品辨识度的一节。对比：

| 普通提示词 | 线程自动化 |
|---|---|
| *Do this now.*（现在做这个） | *Keep checking this and move it forward when something changes.*（持续检查，有变化就推进）|

**Thread automations 是挂在当前线程上的、心跳式的周期性唤醒（heartbeat-style recurring wake-up calls）**——让 Codex 按某个节奏回到**同一个对话**，从而保住上下文而不是每次从零开始。

特性：一个线程可以有多个 schedule；可以一直跑到某个条件满足；可以随任务变化调整节奏。

官方示例：

> 每 30 分钟检查 Slack 和 Gmail 里可能需要处理的未回复消息。研究上下文并起草回复，但**未经批准不要发送任何东西**。

### 8. 三个循环示例

三个例子的共同结构值得注意——**每个都明确划分了「Codex 准备什么」与「你决定什么」**：

| 循环 | Codex 准备 | 你决定 |
|---|---|---|
| **Chief of Staff**（按时查 Slack/Gmail、找上下文、起草回复） | 未读消息、相关上下文、回复草稿、需要判断的问题 | 批准、语气、时机、最终决定 |
| **Monitor for feedback**（盯 Slack 动画反馈、更新 Remotion 工程、重新渲染） | 反馈摘要、更新后的渲染、修订说明、下一个评审链接 | 创意判断、最终批准、发布决定 |
| **Get a refund**（检查客服是否接入，对话变化时准备下一条回复） | 状态检查、回复草稿、有用证据、建议的下一步 | **同意、批准、任何不可逆动作** |

> 📌 **这三张表就是「无人值守的边界」的最佳表达**：智能体做准备工作，**不可逆动作永远留给人**。

### 9. Goals（目标）：设 Codex 能验证的目标 ★

这一节和 Anthropic 的 `/goal` 四件套是同一件事：

| 弱目标（Weak goal） | 强目标（Strong goal） |
|---|---|
| 「实现这个 Markdown 文件里的计划。」 | 「移植这个库，**保持公共 API 兼容**，**用原始单元测试作为成功检查**。当同样的测试通过且差异有文档记录时，工作即可评审。」 |

判据：**强目标给 Codex 一个可以对照测试的东西**——期望行为、评审标准、约束，或一个清晰的 definition of done。

**Rich → Rust 迁移案例**把这一点具体化：目标不只是移植这个库，而是**以能通过原始单元测试的方式移植**。那套测试给了这次运行一个真实的标准——**在新实现通过同样的测试之前，工作就没做完**。

### 10. Side panel（侧边栏）：让产物成为循环的一部分

侧边栏容易被当成预览界面，但那低估了它——**它是 Codex 从聊天界面变成工作发生地的地方**。

- **Inspect artifacts**：Markdown（可带评论评审）、电子表格（渲染公式、支持单元格编辑）、CSV（变成表格而非裸文本）、PDF（直接渲染）、幻灯片（可创建可评审）
- **Operate web surfaces**：内置浏览器让 `index.html`、Storybook、Remotion Studio、Slidev、Streamlit、Jupyter 变得可用——**最小版本往往就够了**，一个带 JS 和 CSS 的 `index.html` 就能成为交互与评审的活界面
- **Review changes**：你和 Codex 看着同一个对象，**评论变成指令，产物变成上下文**

## 可直接带走的工程结论

1. **给重要工作流一个常驻线程**，但要意识到长线程比短线程贵——连续性是要付费的。
2. **记忆要可 diff**。「存在 GitHub 里的 vault，diff 就是记忆的评审面」是本篇最好的一句设计。
3. **代码归仓库，滚动上下文归 vault**——不要混在一起。
4. **记忆指令要写成事件触发的更新规则**（人被提到 → 更新人物笔记；决策做出 → 写下决策和原因），而不是「记住重要的事」。
5. **长跑必须有不重启的转向通道**（steering / `STEER.md`）。
6. **周期性唤醒要回到同一个线程**，不要每次开新的——保上下文就是保成本和保连贯性。
7. **强目标 = 可对照测试的东西**，弱目标 = 「实现这个计划」。与 `/goal` 的四件套完全同构。
8. **不可逆动作永远留在人这一侧**——三个循环示例都显式画了这条线。

## 与库内其他笔记的关系

- 它是 OpenAI 侧「harness 提到工作区层」的产品化终点，前篇（方法论层）见 [OpenAI 04_Harness-engineering](../OpenAI/最新/04_Harness-engineering_中文精读.md)。
- 「强目标」一节与 [04_`/goal` 官方文档](04_goal-command-docs_双语精读.md) 的条件四件套是同一设计的两种表述。
- durable threads + memory vault 对应 Anthropic 的 session 日志 + 记忆层，见 [23_managed-agents](../Anthropic/Engineering全集_逐句对照/23_managed-agents_直观图解与学习笔记.md)。
- thread automations 对应 Claude Code 的 `/loop` 与 scheduled tasks。
