# B33_MCP 2026-07-28 spec: stateless core, coming to Claude_MCP 2026-07-28 规范：无状态核心，登陆 Claude

> 原文：https://claude.com/blog/bringing-mcp-2026-07-28-to-claude
> 来源：Anthropic Claude Blog（分类：Platform ｜ 产品：MCP）｜发布日期：2026-07-28
> 原文存档：[Markdown](原文/B33_bringing-mcp-2026-07-28-to-claude_原文.md)
> 关联：完整规范见 [MCP 2026-07-28 release announcement](https://blog.modelcontextprotocol.io/posts/2026-07-28/)；本篇是 Claude 侧的采纳公告。

## 📌 本篇速览

- 📅 2026-07-28　｜　⏱ 原文约 510 词（逐句精读约 8 分钟）
- 🏷 stateless core、请求/响应模型、扩展框架（MCP Apps / Tasks）、OAuth 2.0/OIDC、MCP tunnels
- 🗂 [返回目录](00_目录与阅读进度.md)

MCP 第五版规范（2026-07-28）的 Claude 采纳公告——**⚠️ 直接修正 Engineering 13 的旧结论**：协议从双向有状态改为**请求/响应的无状态核心**，远程 server 不再需要 sticky session / 共享 session store，可部署到 serverless 和边缘基础设施。三大变化：① **stateless core**；② **标准化扩展框架**——MCP Apps（交互式 UI）和 Tasks（长时任务）以版本化扩展形式发布，加能力不动核心协议；③ **auth 加固**——对齐生产级 OAuth 2.0 / OIDC，直连 Entra、Okta 等企业身份系统。生态数据：MCP 月 SDK 下载超 4 亿（年内 4 倍——注意与 B30 的 3 亿构成时间序列）；Claude 目录 950+ servers。Claude 侧年内配套：MCP Apps 内联 UI、企业托管授权（IdP 组继承、零接触配置）、连接器观测面板、MCP tunnels（私网连接，仅出站）。

---

The fifth spec release of the Model Context Protocol, **MCP 2026-07-28,** is live today.

模型上下文协议的第五个规范版本 **MCP 2026-07-28** 今天上线。

The latest spec moves MCP to a stateless core, while hardening authorization and graduating official extensions.

最新规范把 MCP 迁移到无状态核心，同时加固授权机制、让官方扩展毕业转正。

Support is being rolled out across Claude products.

支持正在 Claude 各产品中陆续推出。

## What's new in MCP

## MCP 有什么新变化

MCP recently surpassed 400M monthly SDK downloads, a 4x increase this year, and has become the industry standard for connecting AI agents to applications.

MCP 最近突破每月 4 亿次 SDK 下载——年内翻了 4 倍——已成为连接 AI 智能体与应用的行业标准。

MCP 2026-07-28 is one of the most significant spec releases to date:

MCP 2026-07-28 是迄今最重要的规范发布之一：

**Stateless core.**

**无状态核心。**

MCP moves from a bidirectional stateful protocol to a request/response model.

MCP 从双向有状态协议转为请求/响应模型。

Servers can now deploy on serverless and edge infrastructure.

服务器现在可以部署在 serverless 和边缘基础设施上。

This simplifies the experience of building MCP servers for Claude and scaling their usage as they grow in adoption.

这简化了为 Claude 构建 MCP 服务器、以及随采用增长扩展用量的体验。

**Standardized extensions.**

**标准化扩展。**

MCP Apps and Tasks now ship under a versioned extensions framework, giving developers a formal path to add capabilities like interactive UIs and long-running work without changing the core protocol.

MCP Apps 和 Tasks 现在以版本化扩展框架的形式发布——开发者有了添加交互式 UI、长时任务等能力的正式路径，而不用改动核心协议。

**Auth hardening.**

**授权加固。**

Authorization now aligns with production OAuth 2.0 and OIDC deployments, so MCP servers connect to enterprise identity systems like Entra or Okta without workarounds.

授权现已对齐生产级 OAuth 2.0 与 OIDC 部署——MCP 服务器无需变通手段即可连接 Entra、Okta 这类企业身份系统。

Companies across the ecosystem have been building on the new spec alongside the MCP community since beta.

自 beta 以来，生态各公司一直与 MCP 社区一起在新规范上构建。

See the MCP 2026-07-28 release announcement for full details on the new spec.

新规范完整细节见 MCP 2026-07-28 发布公告。

## Advancing MCP in Claude

## 在 Claude 中推进 MCP

Claude now lists over 950 MCP servers in the connectors directory, used by millions of people every day.

Claude 的连接器目录现已收录 950 多个 MCP 服务器，每天被数百万人使用。

This year we shipped support for new protocol extensions alongside features that make MCP easier to build on and deploy:

今年我们在支持新协议扩展的同时，也发布了让 MCP 更易构建和部署的特性：

MCP Apps let servers render interactive UI directly in the conversation.

MCP Apps 让服务器把交互式 UI 直接渲染进对话。

Users can see what a connector is doing and work with it inline, without switching tabs.

用户能看到连接器在做什么、内联与之协作，无需切换标签页。

Enterprise-managed auth lets admins provision MCP connectors for their whole organization through their identity provider.

企业托管授权让管理员通过身份提供商为整个组织开通 MCP 连接器。

Admins authorize a connector once, users inherit access through their existing IdP groups, and it's connected on first login: zero-touch setup for the end user.

管理员授权一次，用户经由现有 IdP 组继承访问权、首次登录即连——对最终用户是零接触配置。

Observability for developers building connectors gives published connectors in our directory a dashboard showing how they perform across Claude product surfaces.

面向连接器开发者的可观测性，为目录中已发布的连接器提供仪表盘，展示其在 Claude 各产品表面的表现。

Developers can use it to track adoption, diagnose errors and latency, and break down usage by product.

开发者可用它追踪采用情况、诊断错误与延迟、按产品拆分用量。

MCP tunnels (research preview) connect Claude to MCP servers inside a private network without exposing them to the public internet.

MCP 隧道（研究预览）把 Claude 连到私有网络内的 MCP 服务器，而无需将其暴露到公网。

Teams can bring internal tools to Claude with no inbound firewall rules, no public endpoints, and no IP allowlisting on the origin.

团队可以把内部工具带给 Claude：不开入站防火墙规则、无公共端点、源站无需 IP 白名单。

The stateless core, standardized extensions, and hardened auth in 2026-07-28 will help developers bring more applications to Claude, with a lower-friction, more consistent end-user experience.

2026-07-28 的无状态核心、标准化扩展与加固授权，将帮助开发者把更多应用带给 Claude——最终用户体验摩擦更低、更一致。

We'll continue investing in MCP as an open standard alongside the community, and in the Claude features that make MCP more accessible and effective in production.

我们会与社区一起持续投入 MCP 这个开放标准，以及让 MCP 在生产中更易用、更有效的 Claude 特性。

## Getting started

## 快速上手

Explore the spec and SDKs to get started.

查阅规范和 SDK 即可开始。

Support is rolling out across Claude products soon.

Claude 各产品的支持即将陆续推出。

If you're planning to submit your MCP server to Claude's connectors directory, you can learn more here.

计划把你的 MCP 服务器提交到 Claude 连接器目录的话，详情见文档。

---

## 术语中英对照表

| 英文 | 中文 | 备注 |
|---|---|---|
| stateless core | 无状态核心 | 双向有状态 → 请求/响应；serverless/边缘可部署 |
| versioned extensions framework | 版本化扩展框架 | MCP Apps / Tasks 的转正机制；加能力不动核心 |
| Tasks | 任务扩展 | 长时运行工作的协议级支持 |
| OAuth 2.0 / OIDC alignment | 授权对齐 | 直连 Entra/Okta 等企业 IdP |
| enterprise-managed auth | 企业托管授权 | 管理员授权一次、IdP 组继承、零接触 |
| MCP tunnels | MCP 隧道 | 仅出站连接私网 server |
| 400M monthly SDK downloads | 月下载 4 亿 | 与 B30 的 3 亿构成增长时间序列 |
