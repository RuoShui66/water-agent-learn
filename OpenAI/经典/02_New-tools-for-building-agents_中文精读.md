# 构建 Agent 的新工具

- 英文标题：New tools for building agents
- 发布日期：2025-03-11
- 类型：经典 / 平台演进 / Agent 基础设施
- [OpenAI 官方原文](https://openai.com/index/new-tools-for-building-agents/)

> 本文是中文精读与转述，不是逐句全文翻译。

## 一句话摘要

这篇发布文确立了 OpenAI 现代 Agent 平台的基本方向：以 Responses API 作为统一调用原语，提供内置搜索、文件检索和计算机使用工具，再由 Agents SDK 负责编排、交接、护栏和追踪。

## 为什么它重要

2025 年以前，开发者通常要把多轮模型调用、工具执行、状态保存、检索和观察性拼在一起。OpenAI 在这篇文章中把它们定义为一套彼此配合的 Agent building blocks，也明确将 Agent 描述为“代表用户独立完成任务的系统”。

## 四个核心发布

### Responses API

把 Chat Completions 的简洁调用方式与工具使用能力结合起来。一次响应可以包含模型消息、工具调用、工具结果等不同 item，并支持流式事件和更长的多步过程。

### Built-in tools

- Web search：为需要最新信息的任务访问公开网页；
- File search：从用户或组织文件中检索上下文；
- Computer use：通过界面操作没有合适 API 的系统。

内置工具降低了自行接入第三方搜索、向量存储或浏览器控制的基础设施成本。

### Agents SDK

SDK 把 Agent、工具、handoff、guardrail 和 tracing 变成明确原语。它继承并发展了早期实验项目 Swarm 中的轻量多 Agent 思想。

### Tracing and observability

多步 Agent 的失败往往发生在中间工具选择或参数上，只看最终答案无法诊断。Trace 让开发者看到每一轮模型调用、工具执行和交接，为调试与 eval 提供数据。

## 需要用历史眼光阅读的地方

这是一篇平台发布文章，不是当前 API 参考。到 2026 年，OpenAI 又加入 shell、托管计算环境、skills、compaction 和新的 Agents SDK 沙箱能力。因此：

- 用它理解架构转折与核心概念；
- 用本阅读包中的《From model to agent》和《The next evolution of the Agents SDK》理解当前运行时方向；
- 实际写代码时再查最新官方开发文档，不要直接照抄发布时的版本细节。

## 可直接带走的工程原则

- 将工具调用保存成结构化 trace，不要只留聊天文本。
- 优先使用统一 item/event 模型表达长流程，避免把工具结果拼成不可解析字符串。
- Handoff 需要显式记录控制权从谁转给谁、携带了什么上下文。
- 内置工具减少集成工作，但权限、数据边界和结果验证仍由应用负责。
- Agent 平台应同时提供执行能力与可观测性；只提供前者无法进入生产。

## 为什么是经典

这篇文章是 OpenAI 从“模型 API”走向“Agent 平台”的分水岭，后续计算机环境、Agents SDK 和托管执行能力都沿着这里确定的方向扩展。

