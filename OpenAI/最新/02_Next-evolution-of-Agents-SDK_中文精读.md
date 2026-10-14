# Agents SDK 的下一阶段

- 英文标题：The next evolution of the Agents SDK
- 发布日期：2026-04-15
- 类型：最新 / Agent runtime / 沙箱
- [OpenAI 官方原文](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)

> 本文是中文精读与转述，不是逐句全文翻译。

## 一句话摘要

新版 Agents SDK 把“模型原生 harness”和“受控计算沙箱”组合起来，并把两者解耦：harness 管推理、工具和状态，sandbox 管文件、命令和依赖，从而获得安全、持久和可扩展的长任务执行。

## 中文章节导读

- A more capable harness for the agent loop：能力更完整的 Agent 循环框架
- Native sandbox execution：原生沙箱执行
- Separating harness from compute for security, durability, and scale：为安全、持久性与扩展性分离 harness 和计算资源

## 核心内容

### 1. Agent 的产品差异在领域逻辑，底层循环可以标准化

复杂 Agent 普遍需要指令、工具调用、审批、追踪、交接、恢复、记忆与上下文管理。OpenAI 的方向是把这些重复基础设施沉入 SDK，让开发者集中于领域数据、工具和成功标准。

### 2. Harness 与 sandbox 是两个不同的安全域

Harness 负责调用模型、解释模型输出、调度工具和保存运行状态。Sandbox 负责实际读取文件、运行命令和执行模型生成的代码。二者分离后，API 密钥与业务凭据可以留在编排层，不进入不可信代码所在的执行环境。

### 3. 状态外置才能做到真正的长任务恢复

如果所有状态都只存在某个容器内，容器过期或崩溃就意味着任务丢失。文章提出通过快照与 rehydration 在新容器中恢复工作区，使一次运行不再绑定某台“宠物服务器”。

### 4. 分离也带来扩展能力

一个 Agent 运行可以按需使用一个或多个沙箱；不同子任务可隔离到不同执行环境；多个子 Agent 可以并行工作。计算资源因此按需求启动，而不必与每个会话永久绑定。

### 5. Model-native 不等于封闭

OpenAI 强调 harness 会针对模型自然工作方式提供合适原语，但仍允许开发者替换工具、记忆和沙箱环境。目标是减少通用框架与模型能力之间的错配，同时保留产品级定制。

## 可直接带走的工程原则

- 明确画出控制面与执行面：模型调用和凭据属于控制面，生成代码属于执行面。
- 把运行状态、会话事件与产物持久化到沙箱之外。
- 容器应可被丢弃和重建；不要把恢复逻辑建立在“修好原容器”上。
- 给并行子任务使用独立沙箱，避免文件、依赖和权限互相污染。
- 评测时把“模型 + harness + 工具 + 环境”作为整体，而不是只比较模型名称。

## 与 Anthropic 的呼应

Anthropic《Scaling Managed Agents》几乎从另一侧推导出同样结构：把 session、harness 和 sandbox 虚拟化成稳定接口，让“大脑”和“手”能够分别失败、替换和扩展。

