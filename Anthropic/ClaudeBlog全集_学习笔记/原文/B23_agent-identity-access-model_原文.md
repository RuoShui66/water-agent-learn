# Agent identity: a new access model for autonomous, team-wide AI by Anthropic

> URL: https://claude.com/blog/agent-identity-access-model
> Date: Jun 24, 2026
> og:description: 
> og:image: 

---

For an AI agent to do its best work on a human-agent team, it needs access to the same tools, documents, and context humans have.

In a “single player” AI experience (where one person chats with one assistant), that’s straightforward: you connect your own accounts and the agent acts on your behalf. But in a “multiplayer” AI experience like [Claude Tag](http://anthropic.com/news/introducing-claude-tag), Claude sits in a shared channel alongside many people at once, and it draws on the tools and context that belong to the *workspace*, rather than any one individual.

To make multiplayer experiences work, Claude needs its own accounts for those tools, set up by an admin and tied to the workspace. We call this access model ***agent identity***.

In this post, we explain how agent identity works, how it moves permissions from per-user to per-channel, and how to scope it well in your own workspace.

## **Why “act as the user” breaks down**

When you use AI as a personal assistant, you can connect platforms like Google Drive, GitHub, and your calendar, and let the model use *your* access permissions to read and write in them.

This model doesn’t work for Claude Tag for two reasons:

- **Increasing agent autonomy.** The length of a task that an AI agent can reliably complete on its own has been [doubling roughly every four months](https://www.anthropic.com/institute/recursive-self-improvement). Agents now schedule their own tasks for later and respond to events long after the person who asked has logged off. While users set up routines that trigger them to act given certain situations, the agent works largely autonomously.

- **Multiplayer teams.** Claude Tag places Claude in shared spaces where  teams are already working—e.g., a channel where three engineers and a PM are debugging together. But when more than one person is steering, whose permissions apply? There’s no single choice of person that’d be right all of the time. This gives admins the ability to define what an agent can do in Slack independent from the humans involved, and a distinct tracking of what is done in Slack.

### Claude acts as itself

In a channel where Claude Tag is active, Claude isn’t acting on behalf of a single user. It has its own account in each system it touches: it posts in Slack as the Claude app, opens pull requests as the Claude GitHub App, and queries your warehouse under a service account provisioned by an admin.

And because there are no personal user credentials in play, a shared channel can never become a side door into someone’s private documents.

### Inheriting permissions

In the agent identity model, admins define an identity—the baseline set of connections and skills Claude holds everywhere—at the workspace level, and every channel inherits it by default. Then, where it makes sense, they can override it at the channel level, such as by granting the engineering channel access to GitHub and the data warehouse, or confining a CRM connection to a single private channel.

In addition to credentials, admins also define:

- **Repository access:** which repos Claude can read and write to.

- **Connectors:** the tools and API keys that Claude uses to do its job. Across an organization, different API keys can connect to the same service at different permission levels (e.g., Claude might be given read-only warehouse access in a general channel, and write access in the data team’s private one).

- **Skills and plugins:** folders of instructions, scripts, and resources Claude loads dynamically to improve performance on specialized tasks.

- **Standing instructions:** custom instructions and context for each channel.

Because this model works around distinct Claude identities, revoking the identity ends Claude’s access everywhere that the identity was used. This takes much less effort to manage than auditing individual agent actions across dozens of user accounts.

## How the agent identity model works

Agent identity replaces the question “what can this user do?” with “what can this agent do in this compartment?” That’s a departure from per-user Access Control Lists: it means that a channel member without direct access to the repo can ask Claude to read that repo, if the channel’s profile grants Claude that permission.

This is unusual, but we think it is a necessary step toward an access model that works for autonomous, multiplayer agents. Below, we sketch out how to think about setting those boundaries.

### How identity boundaries work

Claude Tag creates a distinct identity for each private channel; public channels in a workspace share a workspace-level identity. Claude's identity in a legal channel can't reach code that wasn't granted there, and its identity in an engineering channel can't read legal documents that weren't granted there. Memory and access respect those boundaries: what Claude learns in a private channel never appears in the wider workspace.

The identity belongs to the channel, so anyone in it can tag Claude by default, and admins can scope each channel's profile to the least-privileged member. On Enterprise plans, role-based access control lets admins go further and decide which members can invoke Claude at all, so a channel governs both what the agent can reach and who can ask.

### Broad default access to tools and context

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a3a0eae87418506ee6e5b08_agent-access-scoping%20(2).jpg)

*图注：How teams scope Claude's tool access in Claude Tag: broad, low-risk integrations run in shared channels under an agent identity, while personal or team-specific tools stay in DMs and run as the user.*

Running Claude Tag inside Anthropic, we found that its value compounds with tool and context access. Each connected system makes every other one more useful, because Claude can combine context across them—pulling a thread from Slack, a doc from Drive, a ticket from a tracker, and a query from a warehouse into one answer that no single tool could provide.

The teams that get the most out of Claude are the ones that grant it generous access from the start, and pare access back depending on their organization’s admin preferences. Agent identity gives admins broad enough scope for Claude to do useful cross-system work, with boundaries firm enough that the access never travels somewhere it wasn’t granted. Our advice is to start with a baseline profile in a few channels, read the audit trail, and then extend access where the work justifies it, one deliberate grant at a time.

For organizations that require even more granularity, admins can disable Claude Tag in specific channels. Admins can also apply role-based access controls (RBAC) to limit access to Claude Tag to specific users.

### Direct messages

With Claude Tag, direct messages work differently than in shared channels. DMs run on users’ individual claude.ai accounts—their connectors, credentials, and name on the result. This makes DMs the right place to work with Claude on tasks and with tools that should never live in a channel, like email drafts or software only you have a license for.

### Security and audit

When an admin adds a connection to a channel's profile, the credential is stored independently and mapped to that channel's identity, then injected at the network boundary at request time. Outbound traffic to any host an admin hasn't allowed is blocked outright. On the audit side, every routine, memory write, and network call made with agent credentials is recorded, and because Claude acts under its own service accounts, those actions also land in each connected system's own logs.

## What’s next

Agent identity is the foundation of Claude Tag's access model. In the future, we plan to strengthen our Claude Tag’s security offerings to include just-in-time credential grants—so that a user can approve a single sensitive action in the moment without permanently widening the agent's scope—and an identity-aware overlay for organizations with more complex clearance structures. This will add user-level checks on top of an agent’s scope, so Claude only acts when both the channel's profile and the requesting user's own permissions allow it.

The shift from single player to multiplayer AI in products like Claude Tag makes long-running, team-based work possible. Agent identity ensures that Claude’s access to tools is broad enough to be useful, but scoped enough to be secure at enterprise scale.

[**Learn more**](https://www.claude.com/tag)**about Claude Tag.**

*This article was written by Noah Zweben, a member of technical staff on the Claude Code team.*
