# MCP 2026-07-28 spec: stateless core, coming to Claude by Anthropic

> URL: https://claude.com/blog/bringing-mcp-2026-07-28-to-claude
> Date: Jul 28, 2026
> og:description: 
> og:image: 

---

The fifth spec release of the Model Context Protocol, [**MCP 2026-07-28**](https://modelcontextprotocol.io/specification/2026-07-28)**,** is live today. The latest spec moves MCP to a stateless core, while hardening authorization and graduating official extensions. Support is being rolled out across Claude products.

## **What's new in MCP**‍

MCP recently surpassed 400M monthly SDK downloads, a 4x increase this year, and has become the industry standard for connecting AI agents to applications. MCP 2026-07-28 is one of the most significant spec releases to date:**Stateless core.** MCP moves from a bidirectional stateful protocol to a request/response model. Servers can now deploy on serverless and edge infrastructure. This simplifies the experience of building MCP servers for Claude and scaling their usage as they grow in adoption.

**Standardized extensions.** [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview) and [Tasks](https://modelcontextprotocol.io/extensions/tasks/overview) now ship under a versioned extensions framework, giving developers a formal path to add capabilities like interactive UIs and long-running work without changing the core protocol.

**Auth hardening.**Authorization now aligns with production OAuth 2.0 and OIDC deployments, so MCP servers connect to enterprise identity systems like Entra or Okta without workarounds.

Companies across the ecosystem have been building on the new spec alongside the MCP community since beta:

See the [MCP 2026-07-28 release announcement](https://blog.modelcontextprotocol.io/posts/2026-07-28/) for full details on the new spec.

## ‍**Advancing MCP in Claude**‍

Claude now lists over 950 MCP servers in the [connectors directory](https://claude.ai/directory/connectors), used by millions of people every day. This year we shipped support for new protocol extensions alongside features that make MCP easier to build on and deploy:

[MCP Apps](https://claude.com/blog/interactive-tools-in-claude) let servers render interactive UI directly in the conversation. Users can see what a connector is doing and work with it inline, without switching tabs.

[Enterprise-managed auth](https://claude.com/blog/enterprise-managed-auth) lets admins provision MCP connectors for their whole organization through their identity provider. Admins authorize a connector once, users inherit access through their existing IdP groups, and it's connected on first login: zero-touch setup for the end user.

[Observability for developers building connectors](https://claude.com/blog/observability-for-developers-building-connectors) gives published connectors in our directory a dashboard showing how they perform across Claude product surfaces. Developers can use it to track adoption, diagnose errors and latency, and break down usage by product.

[MCP tunnels (research preview)](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview) connect Claude to MCP servers inside a private network without exposing them to the public internet. Teams can bring internal tools to Claude with no inbound firewall rules, no public endpoints, and no IP allowlisting on the origin.

The stateless core, standardized extensions, and hardened auth in 2026-07-28 will help developers bring more applications to Claude, with a lower-friction, more consistent end-user experience. We'll continue investing in MCP as an open standard alongside the community, and in the Claude features that make MCP more accessible and effective in production.

## ‍**Getting started**

**‍**Explore the [spec](https://modelcontextprotocol.io/specification/2026-07-28/) and [SDKs](https://modelcontextprotocol.io/docs/sdk) to get started. Support is rolling out across Claude products soon. If you’re planning to submit your MCP server to Claude’s [connectors directory](https://claude.ai/directory/connectors), you can learn more [here](https://claude.com/docs/connectors/building/submission).
