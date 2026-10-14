---
sidebar_position: 5
---

# Function Calling in AI Agents

You've learned how context engineering helps AI agents use instructions, tools, and memory more effectively. You've also explored how separating responsibilities can make complex agentic systems easier to manage and debug.

But how does an AI agent actually interact with an external tool?

Imagine asking an AI assistant, "What is the weather in Paris right now?"

A language model can understand your question, but it cannot retrieve live weather conditions from its training data alone. It needs access to an external service that provides current weather information.

The model must identify the appropriate tool, provide the required information, receive the result, and use that result to answer your question.

This is where **function calling** comes in.

In this guide, you'll learn how function calling works, how tool definitions influence an agent's behavior, how actions and observations form an agent loop, and how to debug common problems.

## 1. What Is Function Calling?

**Function calling**, also known as **tool calling**, is a capability that allows a language model to request the execution of predefined functions or tools.

These tools can connect the model to external resources such as:

- APIs that provide current information.
- Databases that store application data.
- Search engines that retrieve relevant documents.
- Calculators that perform precise computations.
- Software applications that perform actions on behalf of a user.

The model does not need to implement these capabilities itself. Instead, it can select an available tool and produce a structured request describing how that tool should be used.

However, there is an important distinction:

**Function calling does not automatically execute the function. It allows the model to request a function call, which the surrounding application can then execute.**

Consider the weather example.

The user asks:

> What is the weather in Paris right now?

The process might look like this:

1. The model identifies that the request requires current weather information.
2. It selects a tool named `get_current_weather`.
3. It generates the required arguments, specifying Paris as the location.
4. The application receives the tool call and executes the corresponding function.
5. The weather service returns the current conditions.
6. The application passes the result back to the model.
7. The model uses the result to formulate a response.

The final answer might be:

> It is currently 18°C in Paris, with cloudy skies.

The temperature and conditions in this example are illustrative, not live weather data.

Without function calling, the model would need to rely on information already available in its context. With function calling, it can request information from an external source and incorporate the returned result into its response.

## 2. How Function Calling Powers AI Agents

Function calling connects a model's ability to interpret requests with the actions that an application can perform.

To understand how this works, let's examine the complete process.

### Step 1: The User Sends a Request

The process begins with a user asking a question or requesting an action.

For example:

```text
User: What is the weather in Paris?
```

The application receives the request and prepares the information that will be sent to the model.

### Step 2: The Application Assembles the Context

The model needs information about the conversation and the tools available to it.

Depending on the implementation, the context may include:

- System instructions defining the model's role.
- The user's current request.
- Relevant conversation history.
- Tool definitions describing available functions.
- Other task-specific information.

For example, the application might tell the model that it has access to a `get_current_weather` function and explain what information that function requires.

These definitions help the model determine which tool is appropriate for the request.

The application does not necessarily include the entire history of every interaction. It provides the context available for that particular model call, which may be assembled, summarized, or limited by the implementation.

### Step 3: The Model Selects a Tool

The model evaluates the request and determines whether a tool is needed.

If it decides that a function call is appropriate, it returns a structured tool request.

For example:

```json
{
  "name": "get_current_weather",
  "arguments": {
    "location": "Paris",
    "unit": "celsius"
  }
}
```

This structure identifies the function and provides its arguments.

**At this point, the model has requested a function call. The weather service has not necessarily been contacted yet.**

The application must still receive and execute the request.

### Step 4: The Application Executes the Function

The application interprets the model's request and invokes the corresponding implementation.

For example, the application might call a weather API with the location `Paris` and request the temperature in Celsius.

The actual implementation could use an HTTP request, a software library, or another mechanism. The model does not need to know the internal details as long as the tool interface is clearly defined.

The application should also validate the requested function and its arguments before execution, particularly when the tool can modify data or perform consequential actions.

### Step 5: The Tool Returns an Observation

After execution, the tool returns its result.

For example:

```json
{
  "location": "Paris",
  "temperature": 18,
  "unit": "celsius",
  "conditions": "Cloudy"
}
```

In agent terminology, this returned information is often called an **observation**.

An observation tells the agent what happened after an action was attempted.

A successful search might return relevant documents. A calculator might return a numerical result. A database query might return a collection of records.

A tool can also return an error or indicate that no results were found.

### Step 6: The Result Returns to the Model

The application adds the tool result to the conversation or execution context and sends it back to the model.

The model can then interpret the result and decide what to do next.

For the weather example, it may now have enough information to answer the user.

For a more complicated task, it might need another tool call.

### Step 7: The Model Produces a Response

Once the model has sufficient information, it can generate a final response based on the user's request and the available observations.

For example:

```text
The current weather information for Paris reports
a temperature of 18°C with cloudy conditions.
```

This response illustrates how the tool result could be communicated to the user. A production system should preserve appropriate timestamps and distinguish current observations from stale or unavailable data.

### The Complete Flow

The entire process can be summarized as:

**User Request → Context Assembly → Tool Selection → Tool Execution → Observation → Model Response**

If the task requires additional operations, the process can repeat.

For example, an agent researching a company might search the web, inspect a promising result, retrieve another source, compare findings, and then produce a summary.

The important point is that the model and its tools play different roles: the model requests and interprets actions, while the application executes the corresponding functions.

## 3. The Role of Tool Definitions

An agent cannot reliably select an appropriate tool unless it has enough information about the available options.

This is why **tool definitions** are an important part of function calling.

A tool definition describes a function's identity, purpose, and expected inputs. Depending on the interface, it may also describe output constraints or other metadata.

A typical tool definition contains three essential elements:

| Element | Purpose |
| --- | --- |
| **Name** | Identifies the function the model can request. |
| **Description** | Explains what the function does and when it should be used. |
| **Parameters** | Defines the inputs the function expects, including their types and constraints. |

Let's examine each element.

### The Name

A function name should describe its purpose clearly.

For example:

```text
get_current_weather
```

This is more informative than a vague name such as:

```text
execute_function
```

Clear naming helps distinguish tools when an agent has several functions available.

### The Description

The description explains what a function does and when it is appropriate to use it.

Consider these two descriptions.

**Weak description:**

```text
Get weather.
```

**Better description:**

```text
Retrieve current weather conditions for a specified location.
Use this tool when the user asks about present weather conditions
and live weather information is required.
```

The second description provides useful context for tool selection.

This becomes especially important when multiple tools have similar purposes. For example, an agent might have access to both a current-weather tool and a historical-weather tool.

Their descriptions should make the difference clear.

### The Parameters

Parameters define the information a function needs to execute.

For example, a weather tool may require a location and optionally accept a temperature unit.

A parameter definition can specify:

- The parameter's name.
- Its data type.
- A description of what it represents.
- Whether it is required.
- Permitted values, where applicable.

Constraints help reduce ambiguity and make the tool interface more predictable.

### A Complete Tool Definition

Here is an illustrative function definition using a JSON-style schema and Python syntax:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": (
                "Retrieve current weather conditions for a location. "
                "Use this when the user asks about present weather "
                "conditions and live information is required."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": (
                            "The city or region to retrieve weather for, "
                            "such as Paris, France."
                        )
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": (
                            "Temperature unit for the returned result."
                        )
                    }
                },
                "required": ["location"]
            }
        }
    }
]
```

This example uses a common function-definition format. Exact syntax and supported schema features can vary across model providers and APIs.

Notice that the tool definition describes the interface, not the implementation of the weather service itself.

The actual function that contacts the weather API must exist in the application.

### Why Tool Definitions Matter So Much

Suppose an agent has access to these tools:

```text
search_web(query)
search_internal_documents(query)
get_customer_order(order_id)
update_customer_order(order_id, status)
```

If the descriptions are vague, the model may select the wrong tool or provide inappropriate arguments.

For example, a question about an internal company policy should usually be directed to the internal document search tool rather than a general web search.

You can reduce these mistakes by clearly explaining each tool's purpose and the conditions under which it should be used.

There is also a practical trade-off: tool definitions become part of the information supplied to the model. Providing many lengthy definitions can increase context size, token usage, cost, and latency.

**Aim for tool definitions that are concise but specific enough for the model to select and use each tool correctly.**

## 4. Understanding the Agent Loop: Actions and Observations

Function calling becomes particularly powerful when the model can use the result of one action to decide what to do next.

This repeated process is commonly called the **agent loop**.

At a high level, the loop contains four stages:

1. **Action:** The model requests an operation using an available tool.
2. **Environment response:** The application executes the operation and receives a result.
3. **Observation:** The result is made available to the model.
4. **Decision:** The model determines whether another action is necessary or whether it can respond to the user.

Let's examine a practical example.

### Example: Researching Recent Information

Suppose a user asks:

```text
Find recent announcements from OpenAI and summarize the main updates.
```

The agent has access to a `web_search` tool.

Its first action might be:

```text
Action:
web_search(
    query="OpenAI recent official announcements"
)
```

The search tool returns several results.

```text
Observation:
- An official announcement about a new product.
- A company update describing a new feature.
- A separate announcement about an API capability.
```

The agent now examines these observations.

It might determine that one result provides enough information for a simple answer. Alternatively, it may decide that additional searches are necessary to verify dates or investigate another announcement.

The process could continue:

```text
Action:
web_search(
    query="site:openai.com/index/ official API announcement"
)
```

The agent receives another observation and evaluates whether it has enough information to answer.

Once the relevant information has been collected, it synthesizes the findings into a response.

The example illustrates the interaction between the model and the tool. Actual search results depend on the query, available search service, and time of execution.

### Why the Loop Matters

A tool call is not always the end of a task.

The result of one operation can determine which operation should happen next.

For example, a customer support agent might:

1. Retrieve an order using its order ID.
2. Examine the delivery status.
3. Request tracking information if the order is delayed.
4. Determine whether the available evidence explains the delay.
5. Provide an answer or route the unresolved issue to a support representative.

The exact sequence depends on the information returned by the tools.

This is one of the key differences between a single tool call and an agent that uses tools iteratively.

### Does the Model Always Keep the Entire History?

Not necessarily.

For the agent to make decisions based on previous actions, the application must provide the relevant information from those actions.

Many implementations keep prior messages and tool results in the current context. Others may summarize earlier results, retrieve information from memory, or omit irrelevant history when preparing subsequent model calls.

The essential requirement is that the agent receives enough relevant context to make its next decision.

If important observations are omitted, the agent may repeat work, misunderstand the current state, or make a decision that conflicts with an earlier result.

## 5. Debugging Function Calls

Even when the overall design is sound, function calling can fail in several ways.

Perhaps the model chooses the wrong tool, supplies an invalid argument, or fails to recognize that external information is required.

Understanding the execution process makes these problems easier to investigate.

### Common Function Calling Problems

**Incorrect tool selection**

The model chooses an unsuitable tool for the task.

For example, it uses a web search instead of the internal knowledge base when answering a question about company-specific documentation.

**Incorrect arguments**

The model selects the correct tool but supplies incomplete or invalid parameters.

For example, it calls `get_customer_order` without an order ID.

**Insufficient tool instructions**

The available tools have vague descriptions, so the model cannot reliably distinguish when each tool should be used.

**Unexpected tool results**

The function returns an error, empty data, or a response that differs from what the agent expected.

**Incorrect observation handling**

The model receives the tool result but misinterprets it or ignores important information.

**Unnecessary tool calls**

The agent calls tools even when the requested task can be completed using the existing context, increasing latency and cost.

Each problem requires a different solution. Adding more instructions to the system prompt may help, but the underlying issue could also be a tool schema, implementation bug, validation failure, or incomplete execution history.

### Inspect Intermediate Steps

One of the most useful debugging techniques is to inspect the sequence of tool calls and results.

Some agent frameworks and workflow automation platforms provide intermediate execution logs or tracing features. Their exact names and capabilities depend on the platform.

The information worth examining includes:

- Which tool the model selected.
- The arguments passed to that tool.
- The tool's returned result.
- Any errors encountered.
- Whether the result was passed back to the model.
- What happened next in the execution flow.
- Token usage and execution time, when available.

For example, an execution trace might resemble the following:

```json
{
  "intermediateSteps": [
    {
      "action": {
        "tool": "web_search",
        "toolInput": {
          "query": "OpenAI official recent announcements"
        }
      },
      "observation": {
        "status": "success",
        "result_count": 3
      }
    },
    {
      "action": {
        "tool": "update_task_status",
        "toolInput": {
          "taskId": "search_1",
          "status": "done"
        }
      },
      "observation": {
        "status": "success",
        "message": "Task updated"
      }
    }
  ]
}
```

This is an illustrative trace structure, not the exact output format of a particular framework.

The first entry records a search operation and its result. The second records an update to the task tracker.

By examining the sequence, you can determine whether the agent selected the appropriate functions, whether they executed successfully, and whether their results were processed correctly.

### Trace the Failure to Its Source

Suppose the final report omits an important finding.

Rather than immediately changing the prompt, inspect the execution trace.

Did the agent create the relevant search task? Did it call the search tool? Did the search return useful information? Was the result passed back to the model? Was the task marked as completed correctly?

These questions help distinguish between a planning problem, a function calling problem, a tool implementation problem, and a result synthesis problem.

**The goal of debugging is to find the stage where the expected behavior diverged from the actual behavior.**

When possible, inspect the underlying model requests, tool responses, and execution logs rather than relying exclusively on a platform's simplified interface.

## 6. Best Practices for Function Calling

Reliable function calling requires good tool definitions, appropriate execution controls, and clear instructions.

Here are several practices to apply when building AI agents.

### Practice 1: Write Specific Tool Descriptions

Tool descriptions should communicate both what the function does and when the agent should use it.

**Weak:**

```text
Search the web.
```

**Better:**

```text
Search the web for information from external sources.

Use this tool when the user asks about recent events, current
information, or facts that may have changed since the model's
training data.

Provide a focused query describing the information needed.
```

A specific description makes the tool easier to distinguish from alternatives.

### Practice 2: Explain Tool Usage in System Instructions

Tool definitions explain individual functions, but the system prompt can describe how those functions should work together.

For example:

```text
AVAILABLE TOOLS

- web_search:
  Use for current information from external sources.

- calculator:
  Use for arithmetic and numerical calculations that require
  precise results.

- internal_knowledge_base:
  Use for questions about internal company documentation.

TOOL SELECTION RULES

- Prefer the internal knowledge base for company-specific questions.
- Use web_search when current external information is needed.
- Use calculator for calculations that should not rely on
  language-model estimation.
- If a tool fails, evaluate whether a retry or an alternative
  approach is appropriate.
```

These instructions establish a basic tool-selection policy.

However, they should remain consistent with the actual capabilities available to the agent. A tool that is not registered or accessible cannot be used simply because the system prompt mentions it.

### Practice 3: Define Clear Parameter Constraints

Whenever possible, constrain tool parameters using appropriate types, required fields, enumerated values, and schema validation.

For example:

```json
{
  "unit": {
    "type": "string",
    "enum": ["celsius", "fahrenheit"],
    "description": "The temperature unit for the result."
  }
}
```

This restricts the permitted temperature units to two values.

Without such constraints, the model might produce values such as `"degrees"` or `"kelvin"` even if the underlying function supports only Celsius and Fahrenheit.

Schema constraints do not guarantee that every call will be valid in every implementation, so applications should validate arguments before executing the function.

### Practice 4: Handle Tool Failures Gracefully

Tools should return meaningful results when something goes wrong.

Consider a database search that returns no matching records.

Instead of returning an empty response with no explanation, the function could return a structured result:

```json
{
  "status": "success",
  "results": [],
  "message": "No matching records were found."
}
```

This tells the agent that the search executed successfully but did not find a match.

A different response should represent an actual execution failure:

```json
{
  "status": "error",
  "results": [],
  "message": "The database service is temporarily unavailable."
}
```

These outcomes should not be treated as equivalent.

An empty result may mean the requested information does not exist or that the query was too narrow. A tool error means the system could not reliably complete the operation.

Meaningful error messages help the agent decide whether to adjust its query, retry, use an alternative tool, or explain the limitation to the user.

### Practice 5: Validate Before Executing Actions

Function calling can retrieve information, but it can also trigger actions that affect external systems.

For example, a tool might send an email, update a customer's order, or delete a database record.

Before executing such operations, the application should verify that the requested action is permitted and that the arguments are valid.

For consequential or irreversible actions, additional safeguards may be necessary, such as explicit user confirmation or human approval.

Do not rely solely on the model's decision to determine whether an operation is safe to execute.

### Practice 6: Keep Tool Definitions Focused

A large collection of overlapping tools can make tool selection more difficult and increase the amount of context supplied to the model.

Prefer clear interfaces with distinct responsibilities.

For example, a customer support system might separate:

```text
get_order_status(order_id)
cancel_order(order_id)
update_delivery_address(order_id, address)
```

Each tool has a distinct purpose and a clear expected input.

The application should enforce authorization and business rules for every operation, regardless of which tool the model requests.

### Practice 7: Monitor Tool Usage

For an agent operating in a real application, track relevant execution metrics.

Useful measurements include:

- Tool selection accuracy.
- Invalid argument frequency.
- Tool execution success rate.
- Number of retries and repeated calls.
- Average response time.
- Token usage and execution cost.
- Frequency of unresolved requests.

These measurements help you identify patterns that are difficult to discover from final responses alone.

For example, frequent calls to an unsuitable tool may indicate unclear descriptions or an inadequate tool-selection policy. Repeated execution failures may instead point to an unstable API or a problem with the tool implementation.

Use the evidence to decide which component needs improvement.

## 7. Try It Yourself

**Task:** Imagine you're building an AI assistant for an online store.

The assistant has access to three functions:

```text
search_products(query)
get_order_status(order_id)
cancel_order(order_id)
```

The user asks:

> Find wireless headphones under 100 DT and tell me whether my order 4821 has shipped.

Answer the following questions:

1. Which function or functions should the agent call?
2. What arguments should it provide to each function?
3. In what form should the tool results be returned to the model?
4. What should happen if the order lookup fails?
5. Should the agent call `cancel_order` as part of this request? Explain why.

<details>
<summary><strong>Example Answer</strong></summary>
<div>

**1. Select the appropriate functions**

The agent should call `search_products` to find wireless headphones matching the user's budget and `get_order_status` to retrieve information about order 4821.

The user has not requested an order cancellation, so `cancel_order` is unnecessary.

**2. Provide suitable arguments**

The product search could use a query such as:

```json
{
  "query": "wireless headphones priced under 100 DT"
}
```

The order lookup could use:

```json
{
  "order_id": "4821"
}
```

Whether the order ID should be represented as a string or a number depends on the actual function schema.

**3. Return structured observations**

Each function should return the requested information in a format the application can validate and pass back to the model.

For the product search, that might include product names, prices, and relevant identifiers.

For the order lookup, the response might include the order's current status and the timestamp of the information, if available.

**4. Handle failures**

If the order lookup fails, the application should return an informative error instead of inventing a shipping status.

The agent could retry if appropriate or tell the user that the order status could not be retrieved.

**5. Avoid the cancellation function**

The user has not asked to cancel the order. Calling `cancel_order` would introduce an unintended action.

The agent should use only the tools necessary to fulfill the request and follow the application's authorization and confirmation rules for actions that modify an order.

</div>
</details>

## What's Next

You've now learned how function calling connects language models to external tools, how tool definitions guide function selection, and how actions and observations form an iterative agent loop.

The key takeaway is that **function calling is the interface between an LLM's decisions and the operations an application can actually execute**. Reliable agents need more than the ability to request tools: they also require well-designed tool definitions, validated arguments, meaningful observations, appropriate execution controls, and clear error handling.

Next, we'll explore **Agent Components** to examine how planning, tool utilization, and memory work together to support an agent's behavior.