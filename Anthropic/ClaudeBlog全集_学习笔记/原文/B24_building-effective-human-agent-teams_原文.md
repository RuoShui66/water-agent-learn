# Lessons from Anthropic on building effective human-agent teams by Anthropic

> URL: https://claude.com/blog/building-effective-human-agent-teams
> Date: Jun 24, 2026
> og:description: 
> og:image: 

---

Working with AI used to mean one person interfacing with a single chat window. Over time, AI has become increasingly capable at handling complex, long-running work, like coding, research, and financial analysis. With this, we’ve seen many new ways to use AI—from the terminal and IDE to spreadsheets and decks—but the work has still very much been a “single-player” experience: one human worked with one agent to accomplish individual tasks.

This is changing with the release of tools like [Claude Tag](https://www.anthropic.com/news/introducing-claude-tag). Now, humans and agents can work together in the same workspace, collaborating in service of goals shared by a team. Work now looks a lot more like a *multiplayer game*, with teams of humans setting the strategy, and Claude executing the work.

This involves some new ways of working. At Anthropic, we’ve been testing the technology required to make human-agent teams successful for the last several months. In this article, we explain what multiplayer agents are, and the lessons we’ve learned for building with them.

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a3c1e1e24f66edde9ee63db_Claude-Tag-v2%402x.png)

## **What are multiplayer agents?**

“Multiplayer agents” is how we refer here to AI models that work with many different humans at the same time. Much like regular agents, they have their own [memory](https://platform.claude.com/docs/en/managed-agents/memory) and [skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills). But in other respects they're quite different. They have their own [credentials](https://www.anthropic.com/engineering/managed-agents) and they live in places where work happens. At Anthropic, that's inside team collaboration tools like Slack.

Here’s an example of a human-agent team analyzing a dataset together in Slack:

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a3be9ec0c7dd123eea0fcea_85b9b96b.png)

For agents to productively participate in a team channel, they need specific capabilities:

- [**Persistent memory,**](https://platform.claude.com/docs/en/managed-agents/memory) so they can remember goals and tune their execution towards them

- [**Credentials not tied to humans**](https://www.anthropic.com/engineering/managed-agents)**,** so they can operate within safe, predictable guardrails

- [**Ongoing broad access to information**](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)**,**so they can learn how the organization works and take action to execute tasks in service of the team’s goals

These capabilities amount to the technical foundation required for an agent to participate productively across a team of many humans. However, making human-agent teams *successful* requires more than this: teams need specific ways of working and shared norms, too.

## **Lesson 1: Work in public and give agents broad context**

Teams at Anthropic share information proactively and openly. This is especially true when agents are on the team, because agents build their understanding entirely from the text a team makes searchable: Slack, code, docs, and meeting notes. Private messages, hallway conversations, and restricted documents can’t provide agents with context. For an agent, if it’s not written down and accessible, it doesn’t exist.

Instead of deciding what information should be available to agents one doc or Slack channel at a time, we use clearly defined security boundaries that apply to entire Slack workspaces, as well as to meeting transcripts and doc libraries. Within the security boundary, context flows to every teammate—whether human or AI. Not only does this increase what agents and humans get access to, it also reduces confusion about what can be shared and with whom. Humans and agents alike find it difficult to navigate the soft boundaries of per-item sharing: *should this channel be public or private? Can I share this doc with that person? Is this agent allowed to see that thread?* A small number of clear, workspace-level boundaries removes decision fatigue from day-to-day work.

A high degree of transparency has a reward. For instance, agents that can read decisions from team meetings won't suggest tasks or projects that were deprioritized. Agents with access to product specs beyond their own team can recommend patterns that have succeeded for others. And because agents can read enormous volumes of text far faster than humans do, they routinely surface relevant work that humans would otherwise have missed. We lean on our agents heavily to stay informed and coordinated in a busy, fast-moving industry.

At Anthropic, working in public looks like:

- Choosing a handful of security boundaries at the company and creating workspaces and document sharing settings that match each security boundary

- Defaulting new communication channels to public within the organization, and ensuring decisions land in channels, docs, and meeting notes every time

- Writing artifacts and meeting notes so that agents can find them, since agents are now a primary consumer of team documentation

- Making sure AI has access to the right tools and information needed to get their job done

Defaulting information to be internally public can require cultural shifts. However, the difference between human-agent teams with context and those without is too stark to ignore.

Of course, some interactions are sensitive and will need to be private between a single human and AI. For those, with Claude Tag you can send @Claude a direct message, or you can use the existing [Claude.ai](http://claude.ai) and Claude Cowork applications. These tools give Claude access to private information via your personal MCP connectors, with the knowledge that your conversation and what you share with the agent will remain private.

## **Lesson 2: Every human and agent get a defined role with the right tools for the job**

Human-agent teams share one roster, one set of artifacts, and one working space. Agents have their own [credentials](https://www.anthropic.com/engineering/how-we-contain-claude), [skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), and tool access. Different agents also hold different roles: for instance, while one might own the data analysis for a project, another will hold and enforce the design standard, and a third will run research synthesis.

When a project kicks off, humans chat with the agents to figure out which roles to assign, and how the humans and agents will work together.

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a3bf2ac55e5efdefd1d06fb_LAUNCH%20ROOM.png)

Once the jobs for humans and agents are clear, an agent might spin up other agents to make sure that specific tasks are handled by the agents with the right memory and appropriate access. Importantly, they need access to all the tools required to accomplish the job: one that handles data analysis might need access to BigQuery, and one that performs QA might need access to the Playwright MCP.

Clearly defined roles and responsibilities set human-agent teams up for success. Humans often work in the same threads the agents do, but they hold the roles only humans can hold. This ensures everything works together and human judgment is applied to the most important decisions. Without clear roles, people end up running fleets of personal AIs on the side, duplicating work and fracturing the team's context. Metrics tracking is a common case: a multiplayer agent can do the job once and let everyone see the same numbers.

At Anthropic, having clearly defined roles on human-agent teams looks like:

- An agreed-upon task set: the team's humans and its agents agree on who does what

- Humans and agents working in the same shared threads, so anyone can pick up where anyone left off

- Humans and agents that have access to the right tools to accomplish their respective jobs

- Descriptions of agents’ roles and scopes

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a3be9ee0c7dd123eea0fd08_e35d445f.png)

*图注：*Claude agents share the day-to-day maintenance of a codebase, triaging feedback, planning, writing code, reviewing changes, and reporting status. Each owns a clear task and works on its own schedule; people set the goals and review output.**

An engineering team at Anthropic started creating rosters to help codify human and agent roles because it made driving their work much easier and more concrete. Some things that clicked for them early on:

- Specific roles also help humans easily track where responsibility for a task lies, whether that’s in individual tasks or an entire team’s set of responsibilities

- Writing [skill files](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) to define specific agents’ roles helps to make specialization easy, and allows people across the company to quickly stand up other agents of the same type

- The team adds new agents to focus on new areas when projects get more complex. For example, they added a release manager agent to deal with new software releases.

These methods let humans' mental model of a human-agent team scale as the number of agents grows.

## **Lesson 3: Set a north star to make agents more proactive**

Although some agents at Anthropic simply complete assigned tasks, the most important ones proactively suggest new projects and workstreams. This often happens when a team that has already given its agents rich context and clear roles adds another guide: a north star.

North stars are ambitious, wide-reaching goals that help teams decide which tasks and workstreams are the right ones. At Anthropic, humans always set the north star, grounding it in the mission and goals of the business.

Once a north star is clearly articulated in writing, humans share it with the agents on their team. Then, importantly, humans choose which agents should proactively suggest new workstreams to help achieve this long-term goal. (It’s unlikely that every agent on the team will have the prerequisite skills and trust to proactively suggest work successfully.)

For example, an internal tools team with a north star to “make product onboarding more helpful” saw an agent proactively recommended copy revisions to the onboarding flow error messages. These changes measurably increased onboarding success the following week.

At Anthropic, setting a north star looks like:

- Having humans discuss, debate, and document an ambitious north star goal for their human-agent team—one that’s rooted in the company’s mission and business goals

- Sharing the north star with agents on the team and explicitly naming which agents can proactively recommend new workstreams

- Keeping high-fidelity human time protected on the calendar, with meetings now focused on the most important work

A clear north star gives agents a consistent direction to work toward and meaningful opportunities to proactively support a team’s work.

## **Lesson 4: Build trust over time**

Teams at Anthropic grant agents autonomy in proportion to demonstrated reliability, then expand it deliberately. Engineers have successfully dispatched agents on their team to handle 500 bug fixes independently, but things certainly didn’t start off that way.

When a new human colleague joins the team, it takes time to assess their capabilities and develop strong working routines. It usually takes multiple feedback cycles to externalize all the tacit information about how tasks are best completed. The same is true for agents. Users have to experiment with giving agents many different tasks so they can learn what the agent is capable of, how to clearly describe the goal, what skill files it needs, and what prompts work best to elicit a desired behavior. It’s also important to retest tasks as models change and improve. Prompts may need re-wording and guardrails that used to be helpful may constrain a smarter model from pursuing more creative solutions.

Notably, we’ve found that the best long-running agents have many different ways to verify their work before a human looks at it. Code has tests, of course, but most other work can be verified as well. For example, technical docs can have rubrics and style guides applied to them. When humans set the bar and ensure all work assigned to an agent can be vetted, quality stays high and doesn’t drift from the original intention. Separately, as with humans, it often helps to give one agent the job of doing the task and another agent the job of checking the first agent’s work. This is often called the [“Doer-Verifier” agent harness](https://www.anthropic.com/engineering/harness-design-long-running-apps).

At Anthropic, building trust with agents over time looks like:

- Reviewing agent work manually in the beginning to vet quality, provide feedback, and design task verification checklists

- Telling the agent to use a “verifier” agent to check its work as part of the task

- Building reflection into the cycle and asking agents to review their own misses so work improves over time

- Tracking which kinds of tasks each agent has earned autonomy on and expanding scope per task type after repeated successes

One engineering leader at Anthropic took on a new team with a big backlog. To get a handle on it, he invited a few humans and a few agents to help him sort through the backlog and prioritize what was most important. One set of agents on the team read through all of the items in the backlog, figured out if anyone was working on the items, and assigned a complexity score to anything that was unowned. The other set read from the list, filtered to the medium and low complexity items, and created code changes. At the beginning, humans reviewed every decision made by an agent and marked any that required human input. Then the humans taught the agents to surface those decisions to humans directly, ensuring that decisions with hard tradeoffs always had a human in the loop.

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a3be9ee0c7dd123eea0fd03_9eb4409f.png)

Every week, the leader and his team asked the agents to compile a weekly report that included “lessons & missteps” so the agents would keep track of mistakes and avoid making them again in the future. Over time, the leader was able to give more and more complex code changes to his agents and spend less time guiding the agents’ day to day tasks.

And once the agents were more independent, the leader coached them to treat human attention as the scarce resource it is: to batch questions to be answered in a single pass, repeat key context to get a human up to speed quickly, and limit how many things each human sees at once.

Helping agents communicate well ensures that they remain helpful and effective. Some people have agents in their team with the sole role of deciding how to batch and elevate only the most important communication for human team members. Others set guardrails around how much work agents should do per day, so that humans are able to meaningfully engage with the work. Such guardrails ensure that humans maintain skills that are important to them, and that the number of items requiring human review stays sustainable.

## **Questions to ask**

As you’re laying the foundation for your human-agent teams, consider the following questions:

1. Is all the information and access that agents and humans need both public and broadly searchable?

2. Can you write down your team's roster (humans and agents), and say what each member owns?

3. Does every human and agent on the team have access to the right tools to perform their job?

4. Do you have rubrics or tests for humans and agents to verify key work products?

5. Does your team have a clear north star that everyone can reference?

## **Moving forward**

None of these patterns are new—at least not for humans. A strong north star, clear roles, strong documentation, a shared bar for quality, and room to learn from mistakes are the healthy team habits we’ve known for decades. Agents just make it even more important not to skip them.

The teams getting the most from their agents are the ones who are most intentional about applying these fundamentals.

**Acknowledgements**

This article was written by Kristen Swanson, a member of the Education team at Anthropic. She’d like to thank Matt Bell, Erik Olesund, Hasnain Lakhani, Shale Craig, Nolan Caudill, Mike Schiraldi, Aleks Todorova, and Molly Vorwerck for their contributions to this piece.

*Start building multiplayer agents using*[*agent teams*](https://code.claude.com/docs/en/agent-teams)*in Claude Code or by using*[*Claude Tag*](https://support.claude.com/en/articles/15594475-what-is-claude-tag)*.*
