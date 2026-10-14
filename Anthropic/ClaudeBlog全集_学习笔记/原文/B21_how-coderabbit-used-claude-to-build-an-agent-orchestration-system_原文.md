# How CodeRabbit used Claude to build an agent orchestration system by Anthropic

> URL: https://claude.com/blog/how-coderabbit-used-claude-to-build-an-agent-orchestration-system
> Date: May 27, 2026
> og:description: 
> og:image: 

---

*In our series,* ***How startups build with Claude***, we highlight how startups are transforming their industries with AI. In this article, we share how CodeRabbit built an agent orchestration layer that plans before AI generates code.

| The quick pitch |
|---|
| Name | CodeRabbit |
| Founded | 2023 |
| Founders | Harjot Gill, CEO |
| Stack | Claude Platform, Claude Code |
| Scale | Reviews 2 million PRs per week across 15,000+ customers |

AI coding tools have collapsed the time between idea and working prototype. CodeRabbit, an AI code review platform, has noticed a different trend climbing alongside that throughput: code that compiles and passes tests but doesn't do what the team actually meant to build.

David Loker, VP of AI at CodeRabbit, locates the cause upstream of the model. Experienced developers often assume coding agents understand the same context they do, so they don’t write down requirements that feel obvious to them. The coding agent then fills the gaps with whatever it considers plausible.

To close that gap, CodeRabbit used Claude to design and build an agent orchestration system that runs a structured planning phase before any code is generated. The team's working thesis is that planning quality determines output quality, and the cheaper code generation gets, the more expensive it becomes to move in the wrong direction.

## **Addressing the internal knowledge gap in AI coding**

When the CodeRabbit team studied AI-generated pull requests across their customer base, the most frequent failure mode was code that compiled and passed tests, yet still didn't solve the problem it was built to solve.

"As we gain experience as developers, we internalize knowledge," Loker says. "All those things are in our head, and we assume other developers know them too. But then we make that assumption of the AI system as well, that it also implicitly understands. We're not even aware that we're assuming those things."

Vague prompts force the underlying system to fill gaps with whatever it considers plausible. That guess often diverges from what the developer had in mind.

Loker offers a personal example. While building a memory system on a side project, he spent hours iterating with a coding agent until everything ran. When he asked the agent how to use it, the instructions told him to pass in a user token. There was no login page. He had specified that the system required users but never said users needed a way to sign in. The agent filled the gap, and hours of work landed in a product missing a front door.

"What ends up happening is you build a lot more stuff on top of it, then much later you find there's a problem," Loker says. "In AI workflows, late validation can be very expensive."

## **An orchestration layer that runs before AI coding solutions**

CodeRabbit's response was to insert a planning system in front of code generation. It coordinates multiple Claude models to analyze requirements and surface assumptions before producing a structured execution plan that defines what should be built and what constraints it needs to satisfy.

"This planning system is not meant to replace Claude Code's Plan Mode," Loker says. "It's a higher level orchestration that happens before Claude Code, to point it in a really narrow and right direction where everything that needs to be explicit is made explicit, and we are aware of all assumptions that are being made."

The output is a collaborative product requirements document (PRD): a plan created with full context, validated by stakeholders across the team, and reviewed before implementation starts. Claude Code picks up that plan and uses it to generate a fine-grained implementation plan. The plan becomes a shared artifact that captures what was decided and why, which not only helps teams avoid rework and validate later that the output matched the original intent, but also onboard new engineers.

## **Routing across the Claude model family**

CodeRabbit matches each model tier to task complexity to optimize for cost and latency. Opus drives the orchestration loop and the higher-level strategic work of understanding the problem and setting overall direction. Sonnet takes that output and sequences it into structured planning steps. Haiku handles narrowly scoped operations like context distillation and targeted tool use, where the question is specific enough that a smaller model can answer it well.

"If Haiku does as well as Sonnet on a given task, we use Haiku," Loker says. "If the evaluation harness tells us the plan quality improves when we give Opus more room, we give it more room. We don't guess."

## **Building an eval harness for plan quality**

CodeRabbit had a mature evaluation system for code review, but nothing for evaluating planning output. Building that infrastructure became its own project.

The system started with hand-tuned examples and manual inspection. The team developed a library of LLM judges that scored specific dimensions of plan quality. Because plans eventually produce code, the team could also measure whether the generated code worked, whether it contained extra scope, and how many tokens it took to get there. Running the same task with and without the planning step gave them a way to isolate the value of planning itself.

"We didn't realize what the right level of detail was going to be for that plan," Loker says. Plans that were too granular went stale the moment the codebase shifted. Plans that were too high-level left room for the agent to fill in assumptions, which was the original problem the planning layer was meant to solve. Finding the working level of abstraction took iteration, which is what the eval harness made possible.

## **Catching errors before any code gets written**

In an AI-native coding workflow, many of the decisions that used to surface during code review are now made earlier, in the planning layer. Building a plan that the team can review and align on before code generation starts catches mistakes early.

"What we've built, using the Claude ecosystem, is a team-wide planning system," Loker says. "The plan itself becomes a quality gate. If we can make sure the quality of that plan is really good upfront, the downstream effect is very pronounced. You end up with a lot better code at the end of it."

| Best practices from the CodeRabbit team |
|---|
| What outcome are you actually trying to create, and how do you measure? | Be explicit not just in specifications to the AI but also define what you want in the MPP (maximum possible product). |
| What assumptions are still implicit? | Ask Claude: what is missing? Are there any parts of the plan that are coming out as implicit assumptions instead of explicit specifications? |
| What workflows or edge cases are easy to forget? | Ask Claude to help identify places or cases that you may not have taken into account. |
| How will you know the output matches intent before rollout? | Create a record of work: a chronicle of planning artifacts that is saved and reused. |

**Build your startup on the**[**Claude Platform**](https://platform.claude.com/login?returnTo=%2F%3F)**.**
