# 从模型到 Agent：为 Responses API 配备计算机环境

- 英文标题：From model to agent: Equipping the Responses API with a computer environment
- 发布日期：2026-03-11
- 类型：最新 / Agent loop / 计算机环境
- [OpenAI 官方原文](https://openai.com/index/equip-responses-api-computer-environment/)

> 本文是中文精读与转述，不是逐句全文翻译。

## 一句话摘要

模型只会提出动作；把它变成 Agent，需要一个循环替它执行动作、把结果送回模型，并提供文件系统、受限网络、持久数据、技能和上下文压缩。

## 中文章节导读

- The shell tool：Shell 工具
- Orchestrating the agent loop：编排 Agent 循环
- When the context window gets full: compaction：上下文满时的压缩
- Container context：容器中的文件、数据库与网络上下文
- Agent skills：可复用的 Agent 技能
- How agents are made：Agent 是怎样组装出来的

## 核心内容

### 1. “模型使用工具”本质上只是提出工具调用

模型不会亲自执行命令。它生成结构化动作，Responses API 或客户端 harness 执行该动作，再把 stdout、文件变化或工具结果放入下一轮上下文。这个闭环持续到模型不再请求工具并返回最终结果。

### 2. 计算机环境扩大了模型可完成任务的范围

只有提示词时，模型只能使用训练所得知识和当前上下文。提供 shell、文件系统和可选的 SQLite 等结构化存储后，它可以处理大文件、运行不同语言的程序、请求 API、保存中间产物，并生成可下载的报告、表格或代码。

### 3. 并行执行与输出限额同时重要

模型可以在同一步提出多条命令，由不同容器会话并行执行。另一方面，原始终端日志可能迅速吞噬上下文，因此每个命令需要输出上限和截断标记，只保留足以支持下一步判断的开头与结尾。

### 4. 长任务依靠 compaction 与外部状态

上下文窗口接近上限时，原生 compaction 把历史压缩成更短状态。更重要的是，中间数据应留在文件或数据库中，而不是反复复制进消息历史。上下文保存“索引和决策”，工作区保存“重量级事实和产物”。

### 5. Skills 是版本化的工作方法

技能包把说明、脚本和资源打成可复用 bundle。系统先把技能放入容器并在上下文中提供元数据，模型再按需逐步读取，而不是一开始把全部内容塞进上下文。这是 progressive disclosure 的具体实现。

## 文章给出的组装公式

可以把全文压缩成：

`Responses API 编排 + Shell 可执行动作 + Hosted container 持久运行上下文 + Skills 复用流程 + Compaction 延长任务`

## 可直接带走的工程原则

- 工具输出默认设置大小上限，并让截断对模型可见。
- 大对象落盘，只在上下文中保留路径、摘要、schema 和下一步。
- 网络访问采用 allowlist 或代理，不让生成代码直接接触长期凭据。
- 并行适用于彼此独立的搜索、读取和验证；共享可变状态的命令仍需排序。
- 技能、容器镜像与任务输入都要版本化，才能重放和比较 Agent 行为。

## 为什么值得读

这是理解“Responses API 为什么不仅是文本生成接口”的最好官方文章之一。它把 Agent 从抽象概念还原成一个可运行的系统数据流。

