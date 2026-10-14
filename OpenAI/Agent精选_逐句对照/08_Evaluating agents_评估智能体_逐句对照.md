# 08_Evaluating agents_评估智能体

> 原文：https://cookbook.openai.com/examples/agents_sdk/evaluate_agents
> 来源：OpenAI Cookbook
> 版式说明：逐句中英对照——每一句（或一小段连续的）英文下面紧跟中文翻译；关键术语首次出现时在译文中保留英文原词，便于对照记忆。代码块原样保留、不翻译。

---

# Evaluating Agents with Langfuse｜用 Langfuse 评估智能体

In this cookbook, we will learn how to **monitor the internal steps (traces) of the [OpenAI agent SDK](https://github.com/openai/openai-agents-python)** and **evaluate its performance** using [Langfuse](https://langfuse.com/docs).

在本篇 cookbook（实操手册）中，我们将学习如何用 [Langfuse](https://langfuse.com/docs) 来**监控 [OpenAI agent SDK](https://github.com/openai/openai-agents-python) 的内部步骤（即追踪记录，trace）**，并**评估（evaluate）它的表现**。

This guide covers **online** and **offline evaluation** metrics used by teams to bring agents to production fast and reliably.

本指南会介绍各团队用来把智能体快速、可靠地推上生产环境的**在线评估**（online evaluation）与**离线评估**（offline evaluation）指标。

To learn more about evaluation strategies, check out this [blog post](https://langfuse.com/blog/2025-03-04-llm-evaluation-101-best-practices-and-challenges).

想进一步了解评估策略，可以看这篇[博客文章](https://langfuse.com/blog/2025-03-04-llm-evaluation-101-best-practices-and-challenges)。

**Why AI agent Evaluation is important:**

**为什么 AI 智能体评估很重要：**

- Debugging issues when tasks fail or produce suboptimal results

- 当任务（task）失败或产出结果不理想时，可以定位并调试问题

- Monitoring costs and performance in real-time

- 实时监控成本与性能

- Improving reliability and safety through continuous feedback

- 通过持续反馈提升可靠性与安全性

<br>

<div style="position: relative; padding-top: 69.85769728331177%;">
  <iframe
    src="https://customer-xnej9vqjtgxpafyk.cloudflarestream.com/e335d35a0a762b76055f3e0b977f3380/iframe?muted=true&loop=true&autoplay=true&poster=https%3A%2F%2Fcustomer-xnej9vqjtgxpafyk.cloudflarestream.com%2Fe335d35a0a762b76055f3e0b977f3380%2Fthumbnails%2Fthumbnail.jpg%3Ftime%3D%26height%3D600&controls=false"
    loading="lazy"
    style="border: white; position: absolute; top: 0; left: 0; height: 100%; width: 100%; border-radius: 10px;"
    allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture;"
    allowfullscreen="true"
  ></iframe>
</div>

## Step 0: Install the Required Libraries｜第 0 步：安装所需的依赖库

Below we install the `openai-agents` library (the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)), the `pydantic-ai[logfire]` OpenTelemetry instrumentation, `langfuse` and the Hugging Face `datasets` library

下面我们会安装 `openai-agents` 库（即 [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)）、`pydantic-ai[logfire]` 这个 OpenTelemetry 埋点（instrumentation）组件、`langfuse`，以及 Hugging Face 的 `datasets` 库。

```python
%pip install openai-agents nest_asyncio "pydantic-ai[logfire]" langfuse datasets
```

## Step 1: Instrument Your Agent｜第 1 步：为智能体加上埋点

In this notebook, we will use [Langfuse](https://langfuse.com/) to trace, debug and evaluate our agent.

在这个 notebook 里，我们会用 [Langfuse](https://langfuse.com/) 来追踪、调试和评估我们的智能体。

**Note:** If you are using LlamaIndex or LangGraph, you can find documentation on instrumenting them [here](https://langfuse.com/docs/integrations/llama-index/workflows) and [here](https://langfuse.com/docs/integrations/langchain/example-python-langgraph).

**注意：** 如果你用的是 LlamaIndex 或 LangGraph，对应的埋点文档分别在[这里](https://langfuse.com/docs/integrations/llama-index/workflows)和[这里](https://langfuse.com/docs/integrations/langchain/example-python-langgraph)。

```python
import os
import base64

# Get keys for your project from the project settings page: https://cloud.langfuse.com
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..." 
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..." 
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com" # 🇪🇺 EU region
# os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com" # 🇺🇸 US region

# Build Basic Auth header.
LANGFUSE_AUTH = base64.b64encode(
    f"{os.environ.get('LANGFUSE_PUBLIC_KEY')}:{os.environ.get('LANGFUSE_SECRET_KEY')}".encode()
).decode()
 
# Configure OpenTelemetry endpoint & headers
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = os.environ.get("LANGFUSE_HOST") + "/api/public/otel"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

# Your openai key
os.environ["OPENAI_API_KEY"] = "sk-proj-..."
```

With the environment variables set, we can now initialize the Langfuse client.

环境变量设置好之后，我们就可以初始化 Langfuse 客户端了。

`get_client()` initializes the Langfuse client using the credentials provided in the environment variables.

`get_client()` 会使用环境变量里提供的凭据来初始化 Langfuse 客户端。

```python
from langfuse import get_client
 
langfuse = get_client()
 
# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")
```

Pydantic Logfire offers an instrumentation for the OpenAI Agents SDK.

Pydantic Logfire 为 OpenAI Agents SDK 提供了一套现成的埋点方案。

We use this to send traces to the [Langfuse OpenTelemetry Backend](https://langfuse.com/docs/opentelemetry/get-started).

我们用它把追踪记录发送到 [Langfuse OpenTelemetry Backend](https://langfuse.com/docs/opentelemetry/get-started)（Langfuse 的 OpenTelemetry 后端）。

```python
import nest_asyncio
nest_asyncio.apply()
```

```python
import logfire

# Configure logfire instrumentation.
logfire.configure(
    service_name='my_agent_service',

    send_to_logfire=False,
)
# This method automatically patches the OpenAI Agents SDK to send logs via OTLP to Langfuse.
logfire.instrument_openai_agents()
```

## Step 2: Test Your Instrumentation｜第 2 步：测试埋点是否生效

Here is a simple Q&A agent.

下面是一个简单的问答智能体。

We run it to confirm that the instrumentation is working correctly.

我们运行它，以确认埋点工作正常。

If everything is set up correctly, you will see logs/spans in your observability dashboard.

如果一切配置无误，你会在自己的可观测性面板里看到日志和跨度（span）。

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a senior software engineer",
    )

    result = await Runner.run(agent, "Tell me why it is important to evaluate AI agents.")
    print(result.final_output)

loop = asyncio.get_running_loop()
await loop.create_task(main())

langfuse.flush()
```

Check your [Langfuse Traces Dashboard](https://cloud.langfuse.com/traces) to confirm that the spans and logs have been recorded.

打开你的 [Langfuse Traces Dashboard](https://cloud.langfuse.com/traces)（Langfuse 追踪记录面板），确认跨度和日志已经被记录下来。

Example trace in Langfuse:

Langfuse 中的追踪记录示例：

![Example trace in Langfuse](images/08-01.png)

_[Link to the trace](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/0195948781a9f0d78fd5e067154aa508?timestamp=2025-03-14T12%3A01%3A03.401Z&observation=64bcac3cb82d04e9)_

_图注：[该追踪记录的链接](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/0195948781a9f0d78fd5e067154aa508?timestamp=2025-03-14T12%3A01%3A03.401Z&observation=64bcac3cb82d04e9)_

## Step 3: Observe and Evaluate a More Complex Agent｜第 3 步：观测并评估一个更复杂的智能体

Now that you have confirmed your instrumentation works, let's try a more complex query so we can see how advanced metrics (token usage, latency, costs, etc.) are tracked.

既然已经确认埋点可用，我们就来试一个更复杂的查询，看看进阶指标（token 用量、延迟、成本等）是如何被追踪的。

```python
import asyncio
from agents import Agent, Runner, function_tool

# Example function tool.
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)

async def main():
    result = await Runner.run(agent, input="What's the weather in Berlin?")
    print(result.final_output)

loop = asyncio.get_running_loop()
await loop.create_task(main())
```

### Trace Structure｜追踪记录的结构

Langfuse records a **trace** that contains **spans**, which represent each step of your agent's logic.

Langfuse 会记录一条**追踪记录**（trace），其中包含若干**跨度**（span），每个跨度对应智能体逻辑中的一个步骤。

Here, the trace contains the overall agent run and sub-spans for:

在这个例子里，追踪记录包含智能体的整体运行过程，以及下面这些子跨度：

- The tool call (get_weather)

- 工具调用（get_weather）

- The LLM calls (Responses API with 'gpt-4o')

- LLM 调用（使用 'gpt-4o' 的 Responses API）

You can inspect these to see precisely where time is spent, how many tokens are used, and so on:

你可以逐个查看它们，精确了解时间花在了哪里、用掉了多少 token 等等：

![Trace tree in Langfuse](images/08-02.png)

_[Link to the trace](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/019594b5b9a27c5d497b13be71e7f255?timestamp=2025-03-14T12%3A51%3A32.386Z&display=preview&observation=6374a3c96baf831d)_

_图注：[该追踪记录的链接](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/019594b5b9a27c5d497b13be71e7f255?timestamp=2025-03-14T12%3A51%3A32.386Z&display=preview&observation=6374a3c96baf831d)_

## Online Evaluation｜在线评估

Online Evaluation refers to evaluating the agent in a live, real-world environment, i.e. during actual usage in production.

在线评估指的是在真实运行的线上环境中评估智能体，也就是在生产环境的实际使用过程中进行评估。

This involves monitoring the agent's performance on real user interactions and analyzing outcomes continuously.

这需要持续监控智能体在真实用户交互中的表现，并不断分析结果。

We have written down a guide on different evaluation techniques [here](https://langfuse.com/blog/2025-03-04-llm-evaluation-101-best-practices-and-challenges).

我们把各种评估技术整理成了一份指南，放在[这里](https://langfuse.com/blog/2025-03-04-llm-evaluation-101-best-practices-and-challenges)。

### Common Metrics to Track in Production｜生产环境中常见的追踪指标

1. **Costs** — The instrumentation captures token usage, which you can transform into approximate costs by assigning a price per token.

1. **成本（Costs）** —— 埋点会捕获 token 用量，你只要给每个 token 设定单价，就能换算出大致的成本。

2. **Latency** — Observe the time it takes to complete each step, or the entire run.

2. **延迟（Latency）** —— 观测完成每一步、或整次运行所耗费的时间。

3. **User Feedback** — Users can provide direct feedback (thumbs up/down) to help refine or correct the agent.

3. **用户反馈（User Feedback）** —— 用户可以直接给出反馈（点赞／点踩），帮助你打磨或纠正智能体。

4. **LLM-as-a-Judge** — Use a separate LLM to evaluate your agent's output in near real-time (e.g., checking for toxicity or correctness).

4. **LLM 充当评委（LLM-as-a-Judge）** —— 用另一个独立的 LLM 近乎实时地评估智能体的输出（例如检查有害内容或正确性）。

Below, we show examples of these metrics.

下面我们给出这些指标的示例。

#### 1. Costs｜1. 成本

Below is a screenshot showing usage for `gpt-4o` calls.

下面这张截图展示了 `gpt-4o` 调用的用量情况。

This is useful to see costly steps and optimize your agent.

它能帮你看出哪些步骤开销大，从而优化智能体。

![Costs](images/08-03.png)

_[Link to the trace](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/019594b5b9a27c5d497b13be71e7f255?timestamp=2025-03-14T12%3A51%3A32.386Z&display=preview&observation=6374a3c96baf831d)_

_图注：[该追踪记录的链接](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/019594b5b9a27c5d497b13be71e7f255?timestamp=2025-03-14T12%3A51%3A32.386Z&display=preview&observation=6374a3c96baf831d)_

#### 2. Latency｜2. 延迟

We can also see how long it took to complete each step.

我们也能看到每一步各花了多长时间。

In the example below, the entire run took 7 seconds, which you can break down by step.

在下面这个例子里，整次运行耗时 7 秒，你可以按步骤拆解这段时间。

This helps you identify bottlenecks and optimize your agent.

这有助于你找出瓶颈并优化智能体。

![Latency](images/08-04.png)

_[Link to the trace](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/019594b5b9a27c5d497b13be71e7f255?timestamp=2025-03-14T12%3A51%3A32.386Z&display=timeline&observation=b12967a01b3f8bcb)_

_图注：[该追踪记录的链接](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/019594b5b9a27c5d497b13be71e7f255?timestamp=2025-03-14T12%3A51%3A32.386Z&display=timeline&observation=b12967a01b3f8bcb)_

#### 3. Additional Attributes｜3. 附加属性

Langfuse allows you to pass additional attributes to your spans.

Langfuse 允许你给跨度传入额外的属性。

These can include `user_id`, `tags`, `session_id`, and custom `metadata`.

这些属性可以包括 `user_id`、`tags`、`session_id` 以及自定义的 `metadata`。

Enriching traces with these details is important for analysis, debugging, and monitoring of your application's behavior across different users or sessions.

用这些细节丰富追踪记录，对于分析、调试和监控应用在不同用户或会话下的行为都很重要。

In this example, we pass a [user_id](https://langfuse.com/docs/tracing-features/users), [session_id](https://langfuse.com/docs/tracing-features/sessions) and [trace_tags](https://langfuse.com/docs/tracing-features/tags) to Langfuse.

在这个例子中，我们向 Langfuse 传入了 [user_id](https://langfuse.com/docs/tracing-features/users)、[session_id](https://langfuse.com/docs/tracing-features/sessions) 和 [trace_tags](https://langfuse.com/docs/tracing-features/tags)。

```python
input_query = "Why is AI agent evaluation important?"

with langfuse.start_as_current_span(
    name="OpenAI-Agent-Trace",
    ) as span:
    
    # Run your application here
    async def main(input_query):
            agent = Agent(
                name = "Assistant",
                instructions = "You are a helpful assistant.",
            )

            result = await Runner.run(agent, input_query)
            print(result.final_output)
            return result

    result = await main(input_query)
 
    # Pass additional attributes to the span
    span.update_trace(
        input=input_query,
        output=result,
        user_id="user_123",
        session_id="my-agent-session",
        tags=["staging", "demo", "OpenAI Agent SDK"],
        metadata={"email": "user@langfuse.com"},
        version="1.0.0"
        )
 
# Flush events in short-lived applications
langfuse.flush()
```

![Example trace in Langfuse](images/08-05.png)

#### 4. User Feedback｜4. 用户反馈

If your agent is embedded into a user interface, you can record direct user feedback (like a thumbs-up/down in a chat UI).

如果你的智能体嵌在某个用户界面里，你可以直接记录用户反馈（比如聊天界面里的点赞／点踩）。

Below is an example using `IPython.display` for simple feedback mechanism.

下面是一个用 `IPython.display` 实现的简易反馈机制示例。

In the code snippet below, when a user sends a chat message, we capture the OpenTelemetry trace ID.

在下面的代码片段中，当用户发送一条聊天消息时，我们会捕获 OpenTelemetry 的 trace ID（追踪 ID）。

If the user likes/dislikes the last answer, we attach a score to the trace.

如果用户对上一条回答点赞或点踩，我们就给这条追踪记录附上一个分数。

```python
from agents import Agent, Runner, WebSearchTool
from opentelemetry.trace import format_trace_id
import ipywidgets as widgets
from IPython.display import display
from langfuse import get_client
 
langfuse = get_client()

# Define your agent with the web search tool
agent = Agent(
    name="WebSearchAgent",
    instructions="You are an agent that can search the web.",
    tools=[WebSearchTool()]
)

def on_feedback(button):
    if button.icon == "thumbs-up":
      langfuse.create_score(
            value=1,
            name="user-feedback",
            comment="The user gave this response a thumbs up",
            trace_id=trace_id
        )
    elif button.icon == "thumbs-down":
      langfuse.create_score(
            value=0,
            name="user-feedback",
            comment="The user gave this response a thumbs down",
            trace_id=trace_id
        )
    print("Scored the trace in Langfuse")

user_input = input("Enter your question: ")

# Run agent
with langfuse.start_as_current_span(
    name="OpenAI-Agent-Trace",
    ) as span:
    
    # Run your application here
    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

    result = await main(user_input)
    trace_id = langfuse.get_current_trace_id()

    span.update_trace(
        input=user_input,
        output=result.final_output,
    )

# Get feedback
print("How did you like the agent response?")

thumbs_up = widgets.Button(description="👍", icon="thumbs-up")
thumbs_down = widgets.Button(description="👎", icon="thumbs-down")

thumbs_up.on_click(on_feedback)
thumbs_down.on_click(on_feedback)

display(widgets.HBox([thumbs_up, thumbs_down]))

# Flush events in short-lived applications
langfuse.flush()
```

User feedback is then captured in Langfuse:

随后，用户反馈就会被 Langfuse 捕获：

![User feedback is being captured in Langfuse](images/08-06.png)

#### 5. LLM-as-a-Judge｜5. LLM 充当评委

LLM-as-a-Judge is another way to automatically evaluate your agent's output.

LLM-as-a-Judge 是另一种自动评估智能体输出的方式。

You can set up a separate LLM call to gauge the output's correctness, toxicity, style, or any other criteria you care about.

你可以额外设置一次 LLM 调用，用来衡量输出的正确性、有害程度、风格，或任何你关心的标准。

**Workflow**:

**工作流程**：

1. You define an **Evaluation Template**, e.g., "Check if the text is toxic."

1. 你先定义一个**评估模板**（Evaluation Template），例如"检查这段文本是否含有害内容"。

2. You set a model that is used as judge-model; in this case `gpt-4o-mini`.

2. 你指定一个模型作为评委模型（judge-model），本例中用的是 `gpt-4o-mini`。

2. Each time your agent generates output, you pass that output to your "judge" LLM with the template.

2. 每当智能体产生输出，你就把这份输出连同模板一起交给"评委"LLM。

3. The judge LLM responds with a rating or label that you log to your observability tool.

3. 评委 LLM 会返回一个评分或标签，你把它记录到可观测性工具里。

Example from Langfuse:

来自 Langfuse 的示例：

![LLM-as-a-Judge Evaluation Template](images/08-07.png)
![LLM-as-a-Judge Evaluator](images/08-08.png)

```python
# Example: Checking if the agent’s output is toxic or not.
from agents import Agent, Runner, WebSearchTool

# Define your agent with the web search tool
agent = Agent(
    name="WebSearchAgent",
    instructions="You are an agent that can search the web.",
    tools=[WebSearchTool()]
)

input_query = "Is eating carrots good for the eyes?"

# Run agent
with langfuse.start_as_current_span(name="OpenAI-Agent-Trace") as span:
    # Run your agent with a query
    result = Runner.run_sync(agent, input_query)

    # Add input and output values to parent trace
    span.update_trace(
        input=input_query,
        output=result.final_output,
    )
```

You can see that the answer of this example is judged as "not toxic".

可以看到，本例中的回答被判定为"无害"（not toxic）。

![LLM-as-a-Judge Evaluation Score](images/08-09.png)

#### 6. Observability Metrics Overview｜6. 可观测性指标总览

All of these metrics can be visualized together in dashboards.

上面这些指标都可以汇总到面板里一起可视化。

This enables you to quickly see how your agent performs across many sessions and helps you to track quality metrics over time.

这样你就能快速看清智能体在大量会话中的表现，并随时间跟踪质量指标的变化。

![Observability metrics overview](images/08-10.png)

## Offline Evaluation｜离线评估

Online evaluation is essential for live feedback, but you also need **offline evaluation**—systematic checks before or during development.

在线评估对于获取实时反馈必不可少，但你同样需要**离线评估**——也就是在开发之前或开发过程中做的系统性检查。

This helps maintain quality and reliability before rolling changes into production.

它能帮你在把改动推向生产环境之前，先守住质量和可靠性。

### Dataset Evaluation｜数据集评估

In offline evaluation, you typically:

在离线评估中，你通常会：

1. Have a benchmark dataset (with prompt and expected output pairs)

1. 准备一个基准数据集（benchmark dataset，包含提示词与期望输出的配对）

2. Run your agent on that dataset

2. 在这个数据集上运行你的智能体

3. Compare outputs to the expected results or use an additional scoring mechanism

3. 把输出与期望结果做比对，或者使用额外的评分机制

Below, we demonstrate this approach with the [search-dataset](https://huggingface.co/datasets/junzhang1207/search-dataset), which contains questions that can be answered via the web search tool and expected answers.

下面我们用 [search-dataset](https://huggingface.co/datasets/junzhang1207/search-dataset) 来演示这套做法，这个数据集包含可以通过网页搜索工具回答的问题，以及对应的期望答案。

```python
import pandas as pd
from datasets import load_dataset

# Fetch search-dataset from Hugging Face
dataset = load_dataset("junzhang1207/search-dataset", split = "train")
df = pd.DataFrame(dataset)
print("First few rows of search-dataset:")
print(df.head())
```

Next, we create a dataset entity in Langfuse to track the runs.

接下来，我们在 Langfuse 里创建一个数据集实体（dataset entity），用来跟踪各次运行。

Then, we add each item from the dataset to the system.

然后，把数据集中的每一条样本都加入系统。

```python
from langfuse import get_client
langfuse = get_client()

langfuse_dataset_name = "search-dataset_huggingface_openai-agent"

# Create a dataset in Langfuse
langfuse.create_dataset(
    name=langfuse_dataset_name,
    description="search-dataset uploaded from Huggingface",
    metadata={
        "date": "2025-03-14",
        "type": "benchmark"
    }
)
```

```python
for idx, row in df.iterrows():
    langfuse.create_dataset_item(
        dataset_name=langfuse_dataset_name,
        input={"text": row["question"]},
        expected_output={"text": row["expected_answer"]}
    )
    if idx >= 49: # For this example, we upload only the first 50 items
        break
```

![Dataset items in Langfuse](images/08-11.png)

#### Running the Agent on the Dataset｜在数据集上运行智能体

We define a helper function `run_openai_agent()` that:

我们定义一个辅助函数 `run_openai_agent()`，它会：

1. Starts a Langfuse span

1. 开启一个 Langfuse 跨度

2. Runs our agent on the prompt

2. 用该提示词运行我们的智能体

3. Records the trace ID in Langfuse

3. 在 Langfuse 中记录 trace ID

Then, we loop over each dataset item, run the agent, and link the trace to the dataset item.

然后，我们遍历数据集中的每一条样本，运行智能体，并把追踪记录关联到对应的样本上。

We can also attach a quick evaluation score if desired.

如果需要，还可以顺手附上一个快速评估分数。

```python
from agents import Agent, Runner, WebSearchTool
from langfuse import get_client
 
langfuse = get_client()
dataset_name = "search-dataset_huggingface_openai-agent"
current_run_name = "qna_model_v3_run_05_20" # Identifies this specific evaluation run

agent = Agent(
    name="WebSearchAgent",
    instructions="You are an agent that can search the web.",
    tools=[WebSearchTool(search_context_size= "high")]
)
 
# Assume 'run_openai_agent' is your instrumented application function
def run_openai_agent(question):
    with langfuse.start_as_current_generation(name="qna-llm-call") as generation:
        # Simulate LLM call
        result = Runner.run_sync(agent, question)
 
        # Update the trace with the input and output
        generation.update_trace(
            input= question,
            output=result.final_output,
        )

        return result.final_output
 
dataset = langfuse.get_dataset(name=dataset_name) # Fetch your pre-populated dataset
 
for item in dataset.items:
 
    # Use the item.run() context manager
    with item.run(
        run_name=current_run_name,
        run_metadata={"model_provider": "OpenAI", "temperature_setting": 0.7},
        run_description="Evaluation run for Q&A model v3 on May 20th"
    ) as root_span: # root_span is the root span of the new trace for this item and run.
        # All subsequent langfuse operations within this block are part of this trace.
 
        # Call your application logic
        generated_answer = run_openai_agent(question=item.input["text"])

        print(item.input)
```

You can repeat this process with different:

你可以换用不同的配置反复跑这个流程：

- Search tools (e.g. different context sized for OpenAI's `WebSearchTool`)

- 搜索工具（例如给 OpenAI 的 `WebSearchTool` 设不同的上下文规模）

- Models (gpt-4o-mini, o1, etc.)

- 模型（gpt-4o-mini、o1 等）

- Tools (search vs. no search)

- 工具（带搜索 vs. 不带搜索）

Then compare them side-by-side in Langfuse.

然后在 Langfuse 里把它们并排对比。

In this example, I did run the agent 3 times on the 50 dataset questions.

在这个例子中，我在这 50 道数据集问题上把智能体跑了 3 次。

For each run, I used a different setting for the context size of OpenAI's `WebSearchTool`.

每一次运行，我都给 OpenAI `WebSearchTool` 的上下文规模换了一个设置。

You can see that an increased context size also slightly increased the answer correctness from `0.89` to `0.92`.

可以看到，增大上下文规模也让答案正确率从 `0.89` 小幅提升到了 `0.92`。

The `correct_answer` score is created by an [LLM-as-a-Judge Evaluator](https://langfuse.com/docs/scores/model-based-evals) that is set up to judge the correctness of the question based on the sample answer given in the dataset.

`correct_answer` 这个分数由一个 [LLM-as-a-Judge Evaluator](https://langfuse.com/docs/scores/model-based-evals)（LLM 评委式评分器）生成，它被配置为依据数据集中给出的参考答案来判断作答是否正确。

![Dataset run overview](images/08-12.png)
![Dataset run comparison](images/08-13.png)
