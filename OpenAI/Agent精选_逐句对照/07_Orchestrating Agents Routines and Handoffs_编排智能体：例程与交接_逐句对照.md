# 07_Orchestrating Agents: Routines and Handoffs_编排智能体：例程与交接

> 原文：https://cookbook.openai.com/examples/Orchestrating_agents
> 来源：OpenAI Cookbook
> 版式说明：逐句中英对照——每一句（或一小段连续的）英文下面紧跟中文翻译；关键术语首次出现时在译文中保留英文原词，便于对照记忆。代码块一律原样保留、不翻译；每个代码块之后附一条 `> 说明：` 引用块，简述该段代码在做什么。

---

When working with language models, quite often all you need for solid performance is a good prompt and the right tools.

在使用语言模型时，很多情况下只要有一个好的提示词（prompt）和合适的工具，就足以获得可靠的表现。

However, when dealing with many unique flows, things may get hairy.

然而，当要应对大量各不相同的流程时，事情就会变得棘手。

This cookbook will walk through one way to tackle this.

本篇 cookbook 会带你走一遍解决这个问题的一种思路。

We'll introduce the notion of **routines** and **handoffs**, then walk through the implementation and show how they can be used to orchestrate multiple agents in a simple, powerful, and controllable way.

我们会先引入**例程（routine）**和**交接（handoff）**这两个概念，然后逐步实现它们，并演示如何用它们以一种简单、强大且可控的方式来编排多个智能体（agent）。

Finally, we provide a sample repo, [Swarm](https://github.com/openai/swarm), that implements these ideas along with examples.

最后，我们提供了一个示例仓库 [Swarm](https://github.com/openai/swarm)，它实现了这些理念并附带了示例。

Let's start by setting up our imports.

我们先从导入依赖开始。

```python
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
import json


client = OpenAI()
```

> 说明：导入 OpenAI SDK、用于定义数据模型的 Pydantic、类型标注与 JSON 解析所需的模块，并创建一个全局的 `client` 供后续所有示例调用模型。

# Routines｜例程

The notion of a "routine" is not strictly defined, and instead meant to capture the idea of a set of steps.

「例程（routine）」这个概念并没有严格的定义，它想表达的其实就是「一组步骤」这个朴素的想法。

Concretely, let's define a routine to be a list of instructions in natural language (which we'll represent with a system prompt), along with the tools necessary to complete them.

具体一点说，我们把例程定义为：一份用自然语言写的指令清单（我们会用系统提示词 system prompt 来承载它），外加完成这些指令所需要的工具。

Let's take a look at an example.

我们来看一个例子。

Below, we've defined a routine for a customer service agent instructing it to triage the user issue, then either suggest a fix or provide a refund.

下面我们为一个客服智能体定义了一段例程，指示它先对用户问题做分诊（triage），然后要么给出修复建议，要么提供退款。

We've also defined the necessary functions `execute_refund` and `look_up_item`.

我们同时还定义了必需的两个函数 `execute_refund` 和 `look_up_item`。

We can call this a customer service routine, agent, assistant, etc – however the idea itself is the same: a set of steps and the tools to execute them.

你可以把它叫做客服例程、智能体、助手等等——但概念本身是同一个：一组步骤，加上执行这些步骤所需的工具。

```python
# Customer Service Routine

system_message = (
    "You are a customer support agent for ACME Inc."
    "Always answer in a sentence or less."
    "Follow the following routine with the user:"
    "1. First, ask probing questions and understand the user's problem deeper.\n"
    " - unless the user has already provided a reason.\n"
    "2. Propose a fix (make one up).\n"
    "3. ONLY if not satisfied, offer a refund.\n"
    "4. If accepted, search for the ID and then execute refund."
    ""
)

def look_up_item(search_query):
    """Use to find item ID.
    Search query can be a description or keywords."""

    # return hard-coded item ID - in reality would be a lookup
    return "item_132612938"


def execute_refund(item_id, reason="not provided"):

    print("Summary:", item_id, reason) # lazy summary
    return "success"
```

> 说明：用一段系统提示词把「追问 → 提修复方案 → 不满意才退款 → 查 ID 后执行退款」这四步流程写成例程，并配上两个占位实现的工具函数：`look_up_item` 返回写死的商品 ID，`execute_refund` 打印摘要后返回成功。

The main power of routines is their simplicity and robustness.

例程最主要的威力在于它的简单和健壮。

Notice that these instructions contain conditionals much like a state machine or branching in code.

注意这些指令里包含了条件判断，很像状态机或者代码中的分支。

LLMs can actually handle these cases quite robustly for small and medium-sized routines, with the added benefit of "soft" adherence – the LLM can naturally steer the conversation without getting stuck in dead-ends.

对于中小规模的例程，大语言模型（LLM）其实能相当稳健地处理这类情况，而且还额外带来了「柔性」遵循的好处——LLM 可以自然地引导对话走向，而不会卡进死胡同。

## Executing Routines｜执行例程

To execute a routine, let's implement a simple loop that:

要执行一段例程，我们来实现一个简单的循环，它会：

1. Gets user input.

1. 获取用户输入。

1. Appends user message to `messages`.

1. 把用户消息追加到 `messages` 里。

1. Calls the model.

1. 调用模型。

1. Appends model response to `messages`.

1. 把模型的回复追加到 `messages` 里。

```python
def run_full_turn(system_message, messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_message}] + messages,
    )
    message = response.choices[0].message
    messages.append(message)

    if message.content: print("Assistant:", message.content)

    return message


messages = []
while True:
    user = input("User: ")
    messages.append({"role": "user", "content": user})

    run_full_turn(system_message, messages)
```

> 说明：`run_full_turn` 把系统提示词拼到历史消息前面调一次模型，打印并记录回复；外层 `while` 循环不断读取用户输入，构成一个最朴素的多轮对话循环——此时还完全没有处理工具调用。

As you can see, this currently ignores function calls, so let's add that.

可以看到，目前这份代码完全忽略了函数调用（function call），下面我们把它补上。

Models require functions to be formatted as a function schema.

模型要求函数以「函数 schema（function schema）」的格式来描述。

For convenience, we can define a helper function that turns python functions into the corresponding function schema.

为了方便，我们可以定义一个辅助函数，把 Python 函数自动转换成对应的函数 schema。

```python
import inspect

def function_to_schema(func) -> dict:
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip(),
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }
```

> 说明：用 `inspect.signature` 反射读取函数签名，把 Python 类型标注映射成 JSON Schema 类型，函数名作为工具名、docstring 作为工具描述，没有默认值的参数进入 `required`，最终拼出模型可识别的工具 schema。

For example:

举个例子：

```python
def sample_function(param_1, param_2, the_third_one: int, some_optional="John Doe"):
    """
    This is my docstring. Call this function when you want.
    """
    print("Hello, world")

schema =  function_to_schema(sample_function)
print(json.dumps(schema, indent=2))
```

> 说明：拿一个带混合参数（无标注、有 `int` 标注、有默认值）的样例函数试跑上面的转换器，并打印生成的 schema，用来直观确认类型映射和 `required` 判定是否正确。

Now, we can use this function to pass the tools to the model when we call it.

现在，我们就可以用这个函数在调用模型时把工具传进去了。

```python
messages = []

tools = [execute_refund, look_up_item]
tool_schemas = [function_to_schema(tool) for tool in tools]

response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Look up the black boot."}],
            tools=tool_schemas,
        )
message = response.choices[0].message

message.tool_calls[0].function
```

> 说明：把两个 Python 函数批量转成 schema 后作为 `tools` 参数传给模型，用一句「查一下那双黑靴子」触发工具调用，并取出返回消息里第一个 `tool_call` 查看模型选中的函数和参数。

Finally, when the model calls a tool we need to execute the corresponding function and provide the result back to the model.

最后，当模型调用某个工具时，我们需要真正执行对应的函数，并把结果回传给模型。

We can do this by mapping the name of the tool to the python function in a `tool_map`, then looking it up in `execute_tool_call` and calling it.

做法是在一个 `tool_map` 里把工具名映射到对应的 Python 函数，然后在 `execute_tool_call` 中按名字查表并调用它。

Finally we add the result to the conversation.

最后再把执行结果添加回对话中。

```python
tools_map = {tool.__name__: tool for tool in tools}

def execute_tool_call(tool_call, tools_map):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"Assistant: {name}({args})")

    # call corresponding function with provided arguments
    return tools_map[name](**args)

for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools_map)

            # add result back to conversation 
            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)
```

> 说明：建立「函数名 → 函数对象」的反查表，`execute_tool_call` 解析模型给出的 JSON 参数并实际调用函数；随后把返回值包装成 `role="tool"`、带 `tool_call_id` 的消息追加进对话，让模型能看到执行结果。

In practice, we'll also want to let the model use the result to produce another response.

在实际应用中，我们还希望让模型基于这个结果再生成一次回复。

That response might _also_ contain a tool call, so we can just run this in a loop until there are no more tool calls.

而那次回复里*也可能*还包含工具调用，所以我们干脆把这个过程放进循环里跑，直到不再有工具调用为止。

If we put everything together, it will look something like this:

把所有东西拼起来，大致会是这个样子：

```python
tools = [execute_refund, look_up_item]


def run_full_turn(system_message, tools, messages):

    num_init_messages = len(messages)
    messages = messages.copy()

    while True:

        # turn python functions into tools and save a reverse map
        tool_schemas = [function_to_schema(tool) for tool in tools]
        tools_map = {tool.__name__: tool for tool in tools}

        # === 1. get openai completion ===
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_message}] + messages,
            tools=tool_schemas or None,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:  # print assistant response
            print("Assistant:", message.content)

        if not message.tool_calls:  # if finished handling tool calls, break
            break

        # === 2. handle tool calls ===

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools_map)

            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)

    # ==== 3. return new messages =====
    return messages[num_init_messages:]


def execute_tool_call(tool_call, tools_map):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"Assistant: {name}({args})")

    # call corresponding function with provided arguments
    return tools_map[name](**args)


messages = []
while True:
    user = input("User: ")
    messages.append({"role": "user", "content": user})

    new_messages = run_full_turn(system_message, tools, messages)
    messages.extend(new_messages)
```

> 说明：完整版的「一整轮」实现——内部 `while True` 反复「调模型 → 若有工具调用则执行并回填结果」，直到模型不再调用工具才跳出；函数只返回本轮新增的消息（`messages[num_init_messages:]`），由外层对话循环负责合并进总历史。

Now that we have a routine, let's say we want to add more steps and more tools.

现在我们已经有了一段例程，假设我们想再加入更多步骤和更多工具。

We can up to a point, but eventually if we try growing the routine with too many different tasks it may start to struggle.

在一定范围内是可以的，但如果不断往例程里塞进太多不同的任务，它最终会开始力不从心。

This is where we can leverage the notion of multiple routines – given a user request, we can load the right routine with the appropriate steps and tools to address it.

这时候我们就可以借助「多个例程」的思路——针对用户的请求，加载带有相应步骤和工具的那一段正确例程来处理它。

Dynamically swapping system instructions and tools may seem daunting.

动态地切换系统指令和工具，听起来可能有点吓人。

However, if we view "routines" as "agents", then this notion of **handoffs** allow us to represent these swaps simply – as one agent handing off a conversation to another.

但如果我们把「例程」看作「智能体」，那么**交接（handoff）**这个概念就能非常简洁地表达这种切换——即一个智能体把对话交接给另一个智能体。

# Handoffs｜交接

Let's define a **handoff** as an agent (or routine) handing off an active conversation to another agent, much like when you get transferred to someone else on a phone call.

我们把**交接（handoff）**定义为：一个智能体（或例程）把正在进行的对话移交给另一个智能体，就像你打电话时被转接给另一个人一样。

Except in this case, the agents have complete knowledge of your prior conversation!

只不过在这里，接手的智能体对你之前的对话内容了如指掌！

To see handoffs in action, let's start by defining a basic class for an Agent.

为了看到交接的实际效果，我们先从定义一个基础的 Agent 类开始。

```python
class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-4o-mini"
    instructions: str = "You are a helpful Agent"
    tools: list = []
```

> 说明：用 Pydantic 定义最小化的 `Agent` 数据类，把一个智能体收敛成四个字段：名字、使用的模型、系统指令（即例程本身）和它能用的工具列表。

Now to make our code support it, we can change `run_full_turn` to take an `Agent` instead of separate `system_message` and `tools`:

现在为了让代码支持它，我们可以把 `run_full_turn` 改成接收一个 `Agent`，而不是分开传 `system_message` 和 `tools`：

```python
def run_full_turn(agent, messages):

    num_init_messages = len(messages)
    messages = messages.copy()

    while True:

        # turn python functions into tools and save a reverse map
        tool_schemas = [function_to_schema(tool) for tool in agent.tools]
        tools_map = {tool.__name__: tool for tool in agent.tools}

        # === 1. get openai completion ===
        response = client.chat.completions.create(
            model=agent.model,
            messages=[{"role": "system", "content": agent.instructions}] + messages,
            tools=tool_schemas or None,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:  # print assistant response
            print("Assistant:", message.content)

        if not message.tool_calls:  # if finished handling tool calls, break
            break

        # === 2. handle tool calls ===

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools_map)

            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)

    # ==== 3. return new messages =====
    return messages[num_init_messages:]


def execute_tool_call(tool_call, tools_map):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"Assistant: {name}({args})")

    # call corresponding function with provided arguments
    return tools_map[name](**args)
```

> 说明：把上一版的三个参数收拢为一个 `agent` 对象——模型名取自 `agent.model`、系统提示词取自 `agent.instructions`、工具取自 `agent.tools`，循环逻辑本身完全没变，只是配置来源换成了智能体自身。

We can now run multiple agents easily:

现在我们可以轻松地运行多个智能体了：

```python
def execute_refund(item_name):
    return "success"

refund_agent = Agent(
    name="Refund Agent",
    instructions="You are a refund agent. Help the user with refunds.",
    tools=[execute_refund],
)

def place_order(item_name):
    return "success"

sales_assistant = Agent(
    name="Sales Assistant",
    instructions="You are a sales assistant. Sell the user a product.",
    tools=[place_order],
)


messages = []
user_query = "Place an order for a black boot."
print("User:", user_query)
messages.append({"role": "user", "content": user_query})

response = run_full_turn(sales_assistant, messages) # sales assistant
messages.extend(response)


user_query = "Actually, I want a refund." # implicitly refers to the last item
print("User:", user_query)
messages.append({"role": "user", "content": user_query})
response = run_full_turn(refund_agent, messages) # refund agent
```

> 说明：分别建一个退款智能体和一个销售智能体，先用销售智能体处理「下单买黑靴子」，再把同一份消息历史交给退款智能体处理「我要退款」——因为历史共享，退款智能体能隐式理解「那件商品」指的是刚才下单的靴子。

Great! But we did the handoff manually here – we want the agents themselves to decide when to perform a handoff.

很好！但这里的交接是我们手动完成的——我们希望智能体自己决定何时执行交接。

A simple, but surprisingly effective way to do this is by giving them a `transfer_to_XXX` function, where `XXX` is some agent.

一个简单却出奇有效的做法，是给它们一个 `transfer_to_XXX` 函数，其中 `XXX` 是某个智能体。

The model is smart enough to know to call this function when it makes sense to make a handoff!

模型足够聪明，知道在该做交接的时候去调用这个函数！

### Handoff Functions｜交接函数

Now that agent can express the _intent_ to make a handoff, we must make it actually happen.

现在智能体已经能表达做交接的*意图*了，我们还得让交接真正发生。

There's many ways to do this, but there's one particularly clean way.

实现方式有很多种，但其中有一种特别干净利落。

For the agent functions we've defined so far, like `execute_refund` or `place_order` they return a string, which will be provided to the model.

我们目前定义的这些智能体函数，比如 `execute_refund` 或 `place_order`，返回的都是字符串，这个字符串会被提供给模型。

What if instead, we return an `Agent` object to indicate which agent we want to transfer to? Like so:

那如果我们改成返回一个 `Agent` 对象，用它来表示我们想转交给哪个智能体，会怎么样呢？就像这样：

```python
refund_agent = Agent(
    name="Refund Agent",
    instructions="You are a refund agent. Help the user with refunds.",
    tools=[execute_refund],
)

def transfer_to_refunds():
    return refund_agent

sales_assistant = Agent(
    name="Sales Assistant",
    instructions="You are a sales assistant. Sell the user a product.",
    tools=[place_order],
)
```

> 说明：关键的一步转变——`transfer_to_refunds` 这个「工具」不返回字符串，而是直接返回 `refund_agent` 这个 `Agent` 对象，用返回值类型来承载「转交给谁」的信息。

We can then update our code to check the return type of a function response, and if it's an `Agent`, update the agent in use!

接着我们就可以更新代码，检查函数返回值的类型，如果它是一个 `Agent`，就切换当前正在使用的智能体！

Additionally, now `run_full_turn` will need to return the latest agent in use in case there are handoffs.

另外，由于可能发生交接，现在 `run_full_turn` 还需要把最新使用的智能体返回出来。

(We can do this in a `Response` class to keep things neat.)

（我们可以用一个 `Response` 类来包装，让代码保持整洁。）

```python
class Response(BaseModel):
    agent: Optional[Agent]
    messages: list
```

> 说明：定义一个返回值容器，把「本轮结束时当前是哪个智能体」和「本轮新增的消息」这两件事一起带回给调用方。

Now for the updated `run_full_turn`:

下面是更新后的 `run_full_turn`：

```python
def run_full_turn(agent, messages):

    current_agent = agent
    num_init_messages = len(messages)
    messages = messages.copy()

    while True:

        # turn python functions into tools and save a reverse map
        tool_schemas = [function_to_schema(tool) for tool in current_agent.tools]
        tools = {tool.__name__: tool for tool in current_agent.tools}

        # === 1. get openai completion ===
        response = client.chat.completions.create(
            model=agent.model,
            messages=[{"role": "system", "content": current_agent.instructions}]
            + messages,
            tools=tool_schemas or None,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:  # print agent response
            print(f"{current_agent.name}:", message.content)

        if not message.tool_calls:  # if finished handling tool calls, break
            break

        # === 2. handle tool calls ===

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools, current_agent.name)

            if type(result) is Agent:  # if agent transfer, update current agent
                current_agent = result
                result = (
                    f"Transfered to {current_agent.name}. Adopt persona immediately."
                )

            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)

    # ==== 3. return last agent used and new messages =====
    return Response(agent=current_agent, messages=messages[num_init_messages:])


def execute_tool_call(tool_call, tools, agent_name):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"{agent_name}:", f"{name}({args})")

    return tools[name](**args)  # call corresponding function with provided arguments
```

> 说明：交接的核心实现——用 `current_agent` 跟踪当前智能体，每轮都按它的指令和工具重新构造请求；一旦工具返回值是 `Agent` 类型就切换 `current_agent`，并把工具结果替换成一句「已转交给某某，立即代入该角色」的提示，最后通过 `Response` 把当前智能体一并返回。

Let's look at an example with more Agents.

我们来看一个包含更多智能体的例子。

```python
def escalate_to_human(summary):
    """Only call this if explicitly asked to."""
    print("Escalating to human agent...")
    print("\n=== Escalation Report ===")
    print(f"Summary: {summary}")
    print("=========================\n")
    exit()


def transfer_to_sales_agent():
    """User for anything sales or buying related."""
    return sales_agent


def transfer_to_issues_and_repairs():
    """User for issues, repairs, or refunds."""
    return issues_and_repairs_agent


def transfer_back_to_triage():
    """Call this if the user brings up a topic outside of your purview,
    including escalating to human."""
    return triage_agent


triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a customer service bot for ACME Inc. "
        "Introduce yourself. Always be very brief. "
        "Gather information to direct the customer to the right department. "
        "But make your questions subtle and natural."
    ),
    tools=[transfer_to_sales_agent, transfer_to_issues_and_repairs, escalate_to_human],
)


def execute_order(product, price: int):
    """Price should be in USD."""
    print("\n\n=== Order Summary ===")
    print(f"Product: {product}")
    print(f"Price: ${price}")
    print("=================\n")
    confirm = input("Confirm order? y/n: ").strip().lower()
    if confirm == "y":
        print("Order execution successful!")
        return "Success"
    else:
        print("Order cancelled!")
        return "User cancelled order."


sales_agent = Agent(
    name="Sales Agent",
    instructions=(
        "You are a sales agent for ACME Inc."
        "Always answer in a sentence or less."
        "Follow the following routine with the user:"
        "1. Ask them about any problems in their life related to catching roadrunners.\n"
        "2. Casually mention one of ACME's crazy made-up products can help.\n"
        " - Don't mention price.\n"
        "3. Once the user is bought in, drop a ridiculous price.\n"
        "4. Only after everything, and if the user says yes, "
        "tell them a crazy caveat and execute their order.\n"
        ""
    ),
    tools=[execute_order, transfer_back_to_triage],
)


def look_up_item(search_query):
    """Use to find item ID.
    Search query can be a description or keywords."""
    item_id = "item_132612938"
    print("Found item:", item_id)
    return item_id


def execute_refund(item_id, reason="not provided"):
    print("\n\n=== Refund Summary ===")
    print(f"Item ID: {item_id}")
    print(f"Reason: {reason}")
    print("=================\n")
    print("Refund execution successful!")
    return "success"


issues_and_repairs_agent = Agent(
    name="Issues and Repairs Agent",
    instructions=(
        "You are a customer support agent for ACME Inc."
        "Always answer in a sentence or less."
        "Follow the following routine with the user:"
        "1. First, ask probing questions and understand the user's problem deeper.\n"
        " - unless the user has already provided a reason.\n"
        "2. Propose a fix (make one up).\n"
        "3. ONLY if not satesfied, offer a refund.\n"
        "4. If accepted, search for the ID and then execute refund."
        ""
    ),
    tools=[execute_refund, look_up_item, transfer_back_to_triage],
)
```

> 说明：一个完整的三智能体拓扑——分诊智能体（Triage Agent）负责识别意图并转交，销售智能体和问题维修智能体各自持有业务工具，并且都带 `transfer_back_to_triage` 以便把超出职责范围的话题退回分诊；`escalate_to_human` 则是升级到人工的出口。注意每个 `transfer_to_XXX` 函数的 docstring 就是模型判断何时交接的依据。

Finally, we can run this in a loop (this won't run in python notebooks, so you can try this in a separate python file):

最后，我们可以把它放进循环里运行（这段代码在 Python notebook 里跑不了，你可以放到一个单独的 Python 文件中试试）：

```python
agent = triage_agent
messages = []

while True:
    user = input("User: ")
    messages.append({"role": "user", "content": user})

    response = run_full_turn(agent, messages)
    agent = response.agent
    messages.extend(response.messages)
```

> 说明：主循环从分诊智能体起步，每轮结束后用 `response.agent` 更新当前智能体、用 `response.messages` 累加对话历史——这样交接的结果就能跨轮次保持下来，形成一个可持续运行的多智能体对话系统。

# Swarm

As a proof of concept, we've packaged these ideas into a sample library called [Swarm](https://github.com/openai/swarm).

作为概念验证，我们把这些想法打包成了一个名为 [Swarm](https://github.com/openai/swarm) 的示例库。

It is meant as an example only, and should not be directly used in production.

它仅作为示例存在，不应直接用于生产环境。

However, feel free to take the ideas and code to build your own!

不过，欢迎你借鉴其中的思路和代码，构建属于你自己的实现！
