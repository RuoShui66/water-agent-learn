# Claude can now use tools by Anthropic

> URL: https://claude.com/blog/tool-use-ga
> Date: May 30, 2024
> og:description: 
> og:image: 

---

Tool use, which enables Claude to interact with external tools and APIs, is now generally available across the entire Claude 3 model family on the Anthropic Messages API, Amazon Bedrock, and Google Cloud's Vertex AI. With tool use, Claude can perform tasks, manipulate data, and provide more dynamic—and accurate—responses.

## Tool use

Define a toolset for Claude and specify your request in natural language. Claude will then select the appropriate tool to fulfill the task and, when appropriate, execute the corresponding action:

- **Extract structured data from unstructured text**: Pull names, dates, and amounts from invoices to reduce manual data entry.

- **Convert natural language requests into structured API calls**: Enable teams to self-serve common actions (e.g., "cancel subscription") with simple commands.

- **Answer questions by searching databases or using web APIs**: Provide instant, accurate responses to customer inquiries in support chatbots.

- **Automate simple tasks through software APIs**: Save time and minimize errors in data entry or file management.

- **Orchestrate multiple fast Claude subagents for granular tasks**: Automatically find the optimal meeting time based on attendee availability.

## Improved developer experience

To make it easier to leverage the intelligence of the Claude 3 models with tools, we’ve also built in features that help developers further customize the end-user experience.

- **Tool use with streaming reduces wait times to create more engaging interactions**: Streaming enables real-time responses in applications like customer support chatbots for smoother, more natural conversations.

- **Forced tool use allows developers to instruct Claude on tool selection**: Developers can specify which tools Claude should use or leave the choice with Claude, helping create more targeted and efficient applications.

- **Tools also work with images**: Claude can incorporate image inputs in live applications.

During our beta many developers used Opus to build sophisticated user-facing assistants. To further enhance this experience, Opus will now include <thinking> tags in its outputs, clarifying Claude’s reasoning and simplifying the debugging process for developers. Our Claude 3 models are currently unable to support parallel tool calls.

## Customer spotlight: StudyFetch

AI-native learning platform [StudyFetch ](https://www.claude.com/customers/studyfetch)uses Claude's tool use capabilities to power its personalized AI tutor, Spark.E. By integrating tools to track student progress, navigate course materials and lectures, and create interactive user interfaces, StudyFetch has created a more engaging educational environment for students globally.

"Claude with tool use is accurate and cost-effective, and now powers our live voice-enabled AI tutoring sessions. Within just a few days, we integrated tools into our platform,” said Ryan Trattner, CTO and Co-Founder at StudyFetch. “As a result, our AI tutor, Spark.E, acts agentically—displaying interactive UIs, tracking student progress in context, and navigating through lectures and materials. Since implementing Claude with tool use, we've observed a 42% increase in positive human feedback."

## Customer spotlight: Intuned

Intuned, the browser automation platform, uses Claude to power data extraction within their cloud platform. With AI-powered data extraction, Intuned is able to drastically improve the developer experience in building and executing more reliable browser automations.

"Claude 3 Haiku with tool use has been a game changer for us. After accessing the model and running our benchmarks on it, we realized the quality, speed, and price combination is unmatched,” said Faisal Ilaiwi, Co-Founder at Intuned. “Haiku is helping us scale our customers' data extraction tasks to a completely new level."

## Customer spotlight: Hebbia

[Hebbia ](https://www.claude.com/customers/hebbia)is building the AI knowledge worker for leading financial and legal services firms. They use Claude 3 Haiku to help power several complex, multi-step customer workflows.

"We leverage Claude 3 Haiku for generating live suggestions, automating prompt writing, and extracting key metadata from long documents,” shared Divya Mehta, Product Manager at Hebbia. “Claude 3 Haiku's tool use feature has unlocked capabilities and speed for our platform to generate reliable suggestions and prompts in real-time."

## Get started

You can get started with tool use today on the Anthropic Messages API, Amazon Bedrock, and Google Cloud's Vertex AI. To learn more, explore our [documentation](https://docs.anthropic.com/en/docs/tool-use), [tool use tutorial](https://github.com/anthropics/courses/tree/master/tool_use), and [Anthropic Cookbooks on tool use](https://platform.claude.com/cookbook/tool-use-calculator-tool).
