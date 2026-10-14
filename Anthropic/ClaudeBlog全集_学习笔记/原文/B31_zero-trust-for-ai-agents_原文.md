# Zero Trust for AI agents by Anthropic

> URL: https://claude.com/blog/zero-trust-for-ai-agents
> Date: May 27, 2026
> og:description: 
> og:image: 

---

Frontier AI models are compressing the timeline between vulnerability and exploit from months to hours. Defenders who adopt these tools find and fix bugs faster; attackers who adopt them, or who simply wait for defenders' patches and reverse-engineer them into exploits, move faster too. This is not a future concern: models can already find serious vulnerabilities that traditional tooling and human reviewers have missed for years.

This acceleration matters twice for any organization deploying agents. The infrastructure your agents run on is exposed to AI-accelerated offense like the rest of your estate, and the agents themselves introduce autonomy to interpret goals, select tools, and execute multi-step operations. Traditional access controls won't prevent agents from misusing legitimate permissions, and monitoring needs to account for attacks designed to succeed through persistence rather than exploitation.

[Zero Trust](https://en.wikipedia.org/wiki/Zero_trust_architecture)—trust nothing, verify everything, and assume breach has already occurred—gives security leaders a proven foundation to address this. But the principles need new shape for agentic systems: identities that are cryptographically rooted, permissions scoped per task, memory protected against poisoning, and defensive operations that run at the speed of autonomous attackers.

To help security and risk leaders build for this shift, we put together a practical framework for deploying autonomous AI agents in the enterprise.

In this guide, we share:

- The security considerations unique to agentic systems, including tool access, autonomous decision-making, context persistence, and multi-agent coordination

- The current threat landscape for agents, including prompt injection, tool poisoning, identity and privilege abuse, memory poisoning, and supply chain attacks

- A three-tier Zero Trust framework (Foundation, Advanced, and Optimized) mapped to organizational maturity and risk tolerance

- An eight-phase implementation workflow covering identity, access scoping, sandboxing, input and output controls, and memory safeguards

- How to run agentic security operations (Agentic SOAR) fast enough to contend with AI-accelerated attackers

- Compliance alignment for regulated industries including healthcare, finance, and government

The organizations best positioned for this shift will be the ones whose fundamentals are strong enough that AI-assisted scanning finds fewer bugs in the first place, and whose agent deployments are architected for breach from day one.

Check it out, [here](https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/6a1611a04085d7cd3dadc924_Claude-eBook-Zero-Trust-for-AI-Agents-05182026.pdf).

Get started with [Claude Security](https://www.anthropic.com/product/security) today.
