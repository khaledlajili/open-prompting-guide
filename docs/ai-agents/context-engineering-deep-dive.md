---
sidebar_position: 4
---

# Context Engineering Deep Dive: Building a Deep Research Agent

You've learned how context engineering helps AI agents follow instructions, use tools, manage information, and handle unexpected situations.

But knowing these principles is only the beginning. **How do you apply them when building an agent that performs multiple searches, manages tasks, and produces a complete research report?**

Imagine building a deep research agent. It receives a question, plans several searches, collects information, and combines its findings into a report.

Your first version might work well on simple questions but fail on more complex ones. It might skip searches, forget to update task statuses, or produce incomplete reports.

Improving the system requires more than repeatedly adding instructions to the system prompt. You must also examine the agent's architecture, tool definitions, communication between components, and execution state.

In this guide, you'll explore these challenges by developing a deep research agent step by step.

## 1. Why Context Engineering Requires Iteration

When building an AI agent, your first implementation is rarely perfect.

Even if your initial system prompt looks clear, the agent may interpret instructions differently than expected. Tools may return unexpected results, and the amount of information accumulated during execution may become difficult to manage.

Building a reliable agent often requires repeatedly refining several components:

- **System prompts:** Defining the agent's responsibilities, rules, and expected behavior.
- **Tool definitions:** Explaining what each tool does, when it should be used, and what information it requires.
- **Agent architecture:** Deciding which responsibilities belong to which components.
- **Input and output formats:** Defining how information moves between tools and agents.
- **Execution tracking:** Ensuring that tasks, results, and failures are recorded consistently.

Consider a research agent that creates three search tasks but executes only two.

You might initially respond by adding another instruction to the system prompt. That could help, but it might not address the underlying problem.

Perhaps the agent is responsible for too many operations, its task tracker is difficult to manage, or it receives so much information that important requirements become harder to follow.

**The key principle is to investigate why the system fails before deciding what to change.**

Sometimes the solution is a clearer instruction. In other situations, you may need better tool descriptions, more explicit task tracking, or a different architecture.

## 2. Designing the Research Agent's Architecture

Let's start with the system we're trying to build.

The user provides a research question, and the system must investigate it using web searches before producing a report.

For example:

> Research the current challenges facing small businesses adopting cloud-based software.

The agent must understand the request, identify the main research questions, execute searches, track progress, and synthesize the results.

There are several ways to organize this process.

### The Initial Design: One Agent Does Everything

In a simple implementation, a single agent handles the entire task.

It might be responsible for:

1. Planning the research.
2. Creating and updating search tasks.
3. Calling web search tools.
4. Saving findings to memory or a spreadsheet.
5. Checking which tasks remain incomplete.
6. Writing the final report.

This design is straightforward because one agent controls the entire process.

However, it also creates several potential problems.

**Too many responsibilities**

The agent must switch between planning, searching, tracking progress, and writing. Each responsibility introduces additional instructions and decisions.

**Growing context**

As the research progresses, the conversation may accumulate task descriptions, tool results, source summaries, and previous decisions.

**Forgotten operations**

The agent might collect useful search results but forget to update the task tracker. It might create a task without executing it or begin writing the report before all important questions have been investigated.

**Inconsistent behavior**

The agent might follow the intended process for one topic but behave differently when the research question becomes more complicated.

These problems do not mean that single-agent systems are inherently unreliable. For smaller tasks, one agent may be entirely sufficient. The difficulty arises when its responsibilities and accumulated context become too complex to manage reliably.

### The Improved Design: Separate Planning from Searching

One way to improve the architecture is to introduce a dedicated **Search Worker Agent**.

Instead of requiring one agent to perform every operation, divide the responsibilities between two agents.

The **Deep Research Agent** acts as the orchestrator. It interprets the user's request, creates the research plan, delegates searches, tracks progress, and produces the final report.

The **Search Worker Agent** focuses on executing an individual search task and returning useful findings.

The overall process becomes:

1. The user submits a research question.
2. The Deep Research Agent identifies the research questions and creates a plan.
3. The agent records the planned tasks in the task tracker.
4. It sends each search task to the Search Worker Agent.
5. The worker performs the search and returns the findings.
6. The Deep Research Agent records the result and updates the task status.
7. The orchestrator verifies completion and prepares the final report.

This architecture separates planning and coordination from search execution.

### Why Does This Help?

**1. Clearer responsibilities**

Each agent has a narrower role. The orchestrator can focus on planning and synthesis, while the worker concentrates on gathering relevant information.

**2. Easier debugging**

You can investigate whether a failure occurred during planning, search execution, result processing, or task tracking.

**3. More focused context**

The search worker does not need the complete conversation history or every detail of the research plan. It mainly needs the specific query and instructions required to execute it.

**4. Flexible model selection**

Different agents can use different models depending on their requirements. A reasoning-intensive orchestration task may justify a more capable model, while a straightforward search task may work well with a faster, less expensive model.

The ideal model depends on the task, quality requirements, cost, and available alternatives. Assigning a separate agent does not automatically improve performance; the additional coordination must provide enough value to justify its cost and complexity.

**Important:** A multi-agent architecture does not eliminate the need for good context engineering. It changes how you distribute responsibilities and information so that each component can perform its role more effectively.

## 3. Engineering the Main Agent's System Prompt

With the architecture defined, let's examine the instructions that guide the Deep Research Agent.

A useful system prompt should establish the agent's role, explain the main process, provide essential context, and describe how to use available tools.

### Part 1: Define the Agent's Role

Start by describing what the agent is responsible for.

**Example:**

```text
You are a deep research agent responsible for planning and coordinating
research tasks to produce comprehensive, evidence-based reports.

You create a research plan, delegate search tasks to the available
Search Worker Agent, track execution, evaluate the findings, and
synthesize the results into a final report.
```

This instruction establishes the agent's main responsibility.

Notice that it describes the orchestrator's role without requiring it to perform every search itself.

A clear role definition helps establish which operations belong to the main agent and which should be delegated.

### Part 2: Define the Research Process

Next, explain how the agent should approach a research request.

**Example:**

```text
GENERAL INSTRUCTIONS

1. Analyze the user's research question and identify the main
   information needs.

2. Create distinct search tasks that collectively address those needs.

3. Record each task in the task tracker before executing it.

4. Delegate each search task to the Search Worker Agent.

5. Review the worker's response and record the findings.

6. Update the task status after processing the result.

7. Verify that all important research questions are addressed or
   explicitly identified as unresolved.

8. Synthesize the findings into a structured research report.
```

The instructions describe the major stages without unnecessarily defining every internal decision.

However, the number of searches still needs to be specified according to your requirements.

A short factual query may need only one or two searches. A broad investigation may require several more. The objective is to create enough distinct tasks to cover the research question adequately.

If a particular application requires a fixed number of searches, make that requirement explicit rather than leaving it ambiguous.

### Part 3: Provide Essential Context

Research depends on time-sensitive information. A query about the latest developments cannot be handled in exactly the same way as a question about historical events.

Providing the current date can help the agent interpret temporal expressions and choose relevant search periods.

For example, in a system that supports dynamic date injection:

```text
For temporal context, today's date is:
{{ $now.format('yyyy-MM-dd') }}
```

This example uses an n8n expression to insert the current date into the prompt.

Other orchestration platforms may use different syntax.

Including the date is useful for queries involving phrases such as:

- Latest developments
- Recent research
- Current market conditions
- Events during the past year

However, the date alone does not make the agent's information current. The agent still needs suitable search tools, appropriate date filters when available, and a process for checking when its sources were published.

## 4. Defining Tools Clearly

Giving an agent access to a tool is not the same as explaining how to use it effectively.

A tool's technical definition may specify its name, parameters, and expected return type. These details are necessary, but the agent may also need instructions explaining the tool's purpose and role in the larger process.

Imagine your research agent has access to three tools:

| Tool | Purpose |
| --- | --- |
| `delete_task` | Removes existing task entries from the tracker when appropriate |
| `append_update_task` | Creates a task or updates its stored information |
| `Search Worker Agent` | Executes a research search and returns findings |

The exact tool names depend on the implementation. What matters is that the agent understands the purpose of each tool and the conditions under which it should be used.

### Example: Tool Usage Instructions

```text
TOOL USAGE

Task management:
- Use the task management tools to maintain the research plan.
- Start each new research request with a clean task list, but only
  clear entries belonging to the current research session.
- Create the task entries before delegating searches.
- Use only the permitted task status values.
- Update the relevant task after processing the worker's response.

Search execution:
- Delegate search tasks to the Search Worker Agent.
- Provide the actual search query and any required search constraints.
- Review the returned findings before recording the task as completed.
- Do not mark a search as successful when the worker reports a failure.

Final report:
- Verify task statuses before writing the report.
- Identify important information gaps.
- Do not present unverified findings as established facts.
```

These instructions explain how tool usage fits into the overall process.

For example, the agent should not mark a search as completed simply because it called the worker. It should examine the response and determine whether the task was actually completed.

### Why Explicit Status Values Matter

Suppose the task tracker accepts these status values:

```text
todo
in_progress
done
failed
```

Without an explicit definition, the agent might use `pending`, `completed`, `finished`, or `success` interchangeably.

That can create problems when another component expects a specific value.

Define what each allowed value means:

| Status | Meaning |
| --- | --- |
| `todo` | The task has been created but has not started. |
| `in_progress` | The task is currently being executed. |
| `done` | The task was completed successfully and its result was recorded. |
| `failed` | The task could not be completed after the permitted recovery attempts. |

If your system uses these values, instruct the agent to use them exactly as written.

A task should not be marked `done` if the search failed or its result has not been recorded.

**A practical lesson:** When an agent interacts with software, important expectations should be reflected in both the instructions and the actual tool or data design.

Where possible, enforce valid status values, required fields, and access permissions through the implementation itself instead of relying entirely on the model to follow instructions.

## 5. Choosing Between Flexible and Strict Instructions

One important design decision is how much freedom the agent should have when carrying out a research plan.

Consider two different approaches.

### Approach A: Flexible Execution

A flexible agent can consolidate redundant tasks, adjust its plan, or decide that a planned search is unnecessary.

For example:

```text
Execute the research plan efficiently.

If two search tasks substantially overlap, you may consolidate them
before execution and record the reason.

If new information makes a planned task unnecessary, explain why
and update the task tracker accordingly.

Do not silently skip tasks or leave task statuses unresolved.
```

This approach allows the agent to adapt its process to the research question.

It can reduce unnecessary searches, avoid duplicate work, and make more efficient use of resources.

However, the agent must still account for every task and demonstrate that the research objectives have been addressed.

### Approach B: Strict Execution

A strict agent must execute every task in the approved plan.

For example:

```text
STRICT EXECUTION RULES

- Execute a search for every approved search task.
- Do not skip or consolidate tasks during execution.
- Record the search result or failure for every task.
- Do not mark a task as done unless its search was completed
  successfully and the result was recorded.
- Verify that every approved task has reached a final status
  before preparing the report.
```

This approach is appropriate when completeness is more important than avoiding duplicate work.

For example, a research procedure may require independent searches to examine several specified topics separately, even when some findings overlap.

### Which Approach Should You Choose?

Neither approach is universally better.

| Consideration | Flexible Execution | Strict Execution |
| --- | --- | --- |
| **Adaptability** | Higher | Lower |
| **Task completeness** | Requires careful validation | Easier to enforce for approved tasks |
| **Efficiency** | Can avoid redundant work | May perform unnecessary searches |
| **Control** | More decisions delegated to the agent | Execution requirements are more explicit |
| **Best suited for** | Exploratory research | Fixed research procedures |

You should also avoid giving contradictory instructions.

For example, telling the agent to execute exactly five searches while also allowing it to skip any search it considers unnecessary creates ambiguity about the actual requirement.

Decide whether the number of searches is mandatory, a planning guideline, or a minimum coverage target. Then express that decision consistently throughout the prompt and workflow.

**A useful rule:** Be strict about the outcomes and constraints that genuinely matter, while allowing flexibility in areas where different approaches can achieve the same result.

## 6. Improving Research Task Planning

A research agent's results depend heavily on the quality of its search plan.

A broad request such as "Research AI agents" is not a particularly useful search task. It could refer to architecture, planning, memory, tool use, evaluation, applications, or several other subjects.

The orchestrator should break the request into distinct information needs before delegating searches.

### Example: Weak vs. Better Task Decomposition

**Weak plan:**

```text
Task 1: Research AI agents.
Task 2: Search for AI agents.
Task 3: Find information about AI agents.
```

These tasks overlap heavily and do not establish clear research objectives.

**Better plan:**

```text
Task 1: Identify the main architectural patterns used to build
AI agents and explain how they differ.

Task 2: Investigate common reliability challenges in agentic systems,
including tool execution, planning, and context management.

Task 3: Find recent evaluations or case studies that report how
agentic systems perform on complex tasks.
```

The improved plan assigns each task a distinct purpose.

The exact searches will depend on the user's request, but the tasks should collectively cover the most important questions.

### Add Metadata to Search Tasks

As your research system becomes more sophisticated, a search query alone may not contain enough information to guide execution.

You can extend each task with useful metadata.

For example:

| Field | Purpose | Example |
| --- | --- | --- |
| `task_id` | Identifies the task | `task_001` |
| `query` | Contains the actual search request | `AI agent evaluation methods` |
| `search_type` | Suggests the appropriate source category | `academic` |
| `date_range` | Specifies a requested time period | `past_year` |
| `domain_focus` | Identifies the research subject | `AI research` |
| `priority` | Helps determine execution order | `high` |
| `status` | Tracks task progress | `todo` |

Not every field is necessary for every project.

For example, a general research assistant may not need a priority field for a small query. A system that performs academic research or monitors recent developments may benefit from source types and date filters.

The important point is that task metadata should support actual execution. Adding fields that the agent and tools do not use only creates unnecessary complexity.

### Specify Date Ranges Carefully

Temporal instructions are particularly important for research.

Consider these requests:

- Find today's announcements.
- Review developments from the past month.
- Compare research published during the past year.
- Investigate how the industry changed between 2020 and 2024.

They require different interpretations of time.

Your system should define how time expressions are converted into search constraints and how explicit dates are represented.

For example:

```text
DATE RANGE RULES

- Use the current date as the reference point for relative periods.
- Interpret "past month" as the preceding calendar-length month
  unless the application defines a different convention.
- Represent explicit start and end dates in YYYY-MM-DD format.
- Do not invent date ranges when the user's intent is unclear.
- If the selected search tool does not support the requested
  date constraints, explain the limitation or use an appropriate
  alternative when available.
```

The exact rules should match your application's requirements. The main objective is to make the interpretation consistent and testable.

## 7. Designing Communication Between Agents

When an agent delegates work to another agent, you must determine what information the worker needs and what it should return.

Sending the entire conversation history to every sub-agent may seem convenient, but it can increase context length and introduce irrelevant details.

A better design is to provide each worker with the smallest amount of information needed to complete its task reliably.

### What Should the Search Worker Receive?

For a basic search task, the worker might need:

- The search query
- The purpose of the search
- Any required date or source restrictions
- Instructions for handling failures
- The expected output format

It generally does not need the orchestrator's entire conversation history, unrelated search results, or the complete research report.

For example:

```text
SEARCH TASK

Query:
Recent studies evaluating the reliability of AI agents.

Objective:
Identify relevant studies and summarize their findings.

Requirements:
- Prefer relevant primary sources when available.
- Record publication dates and source references.
- Distinguish reported findings from your own interpretation.
- Report search failures or limitations explicitly.
```

This gives the worker enough context to perform the task without transferring unnecessary information.

### What Should the Worker Return?

The orchestrator needs more than an unstructured paragraph if it must update task statuses and synthesize multiple results.

Define a consistent response format.

For example:

```json
{
  "status": "done",
  "query": "Recent studies evaluating the reliability of AI agents",
  "findings": [
    {
      "summary": "Summary of a relevant finding",
      "source": "https://example.com/research",
      "published_date": "2026-04-15"
    }
  ],
  "limitations": [],
  "error": null
}
```

This is an illustrative response structure, not a claim about any particular tool's actual output.

In a real implementation, validate the output against a schema. For example, `status` should accept only permitted values, and the orchestration system should verify that required fields are present.

A worker should never invent a source URL or publication date to satisfy the format. When information is unavailable, the response should represent that uncertainty explicitly.

### Why Standardized Communication Helps

Consistent inputs and outputs make it easier for the orchestrator to:

- Update the correct task.
- Distinguish successful searches from failures.
- Combine findings from multiple workers.
- Identify missing information.
- Debug unexpected results.

**The principle is simple:** Each agent should receive the context it needs and return information that the next component can reliably use.

## 8. Managing Context Length

During a long research process, an agent's context can grow substantially.

Every search may add new findings, source details, task updates, and messages from other agents. Eventually, the accumulated information can become unnecessarily large.

This creates several potential problems:

- Important instructions may become harder to locate among irrelevant details.
- Repeated information consumes context that could be used for new findings.
- Large worker responses can make orchestration more expensive.
- Previous tasks may remain in context even after their details are no longer useful.

Here are four practical strategies.

### Strategy 1: Separate Responsibilities

Using dedicated workers can prevent every agent from accumulating the complete context of the entire system.

The search worker handles its assigned search. The orchestrator maintains the broader research plan.

Use this separation when the improvement in focus and context management justifies the additional orchestration complexity.

### Strategy 2: Summarize Results

Instead of carrying complete search-result payloads through every subsequent step, extract the most relevant findings and preserve their source references.

For example, a worker might return:

```text
Finding:
Several studies identify tool reliability as an important challenge
for multi-step AI agents.

Evidence:
- Source A: Relevant evaluation results.
- Source B: Discussion of tool-use failures.

Limitations:
The available sources do not establish that the same failure rate
applies across all agent architectures.
```

A concise summary preserves the important information while avoiding unnecessary detail.

However, summarization must not remove evidence needed for later verification. Keep links, identifying details, and relevant quotations or data when they are necessary to support the final report.

### Strategy 3: Track State Externally

Use a spreadsheet, database, or other persistent store to record task status and important findings.

The agent can retrieve the relevant state when needed rather than relying exclusively on the full conversation history.

External storage also makes it easier to inspect execution after a failure.

### Strategy 4: Reset Context at Appropriate Boundaries

If the system handles multiple independent research requests, distinguish information belonging to one request from information belonging to another.

For example, a new research session should not accidentally inherit unfinished tasks from a previous user's investigation.

Clear or isolate session-specific state at appropriate boundaries, while preserving any longer-term memory that the application genuinely needs.

Be careful when deleting task records: remove only the entries belonging to the intended session, not unrelated work.

## 9. Adding Error Handling

Even a carefully designed search agent will encounter failures.

A source may be unavailable, an API may return an error, or a worker may produce an incomplete response.

Your instructions should explain how the system should respond instead of assuming that every operation will succeed.

For example:

```text
ERROR HANDLING

- If the Search Worker Agent fails, retry once with a revised query
  when an alternative query is likely to help.
- If the retry fails, record the failure and its reason.
- Mark an unsuccessful task as "failed", using the permitted status.
- Continue with independent tasks when doing so remains useful.
- Do not report a failed search as successfully completed.
- If a critical failure prevents a reliable report, notify the user
  and explain what remains incomplete.
- Before submitting the report, check whether unresolved failures
  materially affect its conclusions.
```

These instructions establish a recovery strategy without requiring the entire process to stop whenever a single search fails.

However, retrying is not always appropriate. A permission error, invalid credential, or unavailable service may require intervention rather than another identical request.

The system should also distinguish between a tool call that failed and a search that succeeded but found no relevant information. Those are different outcomes and should be recorded accordingly.

For reliable implementations, combine prompt-level instructions with programmatic error handling, retry limits, timeouts, and validation.

## 10. The Context Engineering Improvement Cycle

The architecture and prompt we've designed are starting points, not final solutions.

You need to test the agent and refine it according to its observed behavior.

A practical development cycle looks like this:

**Step 1: Build the initial system.**

Create the orchestrator, search worker, available tools, and task tracker. Begin with clear but relatively simple instructions.

**Step 2: Test different research questions.**

Use a range of inputs, from narrow factual questions to broad research topics.

Include cases where sources are unavailable, tasks overlap, or search results are incomplete.

**Step 3: Observe the execution.**

Examine task creation, tool calls, returned results, task status changes, and the final report.

**Step 4: Identify the underlying issue.**

Determine whether the failure came from unclear instructions, poor task decomposition, tool problems, inconsistent data, or excessive context.

**Step 5: Make a targeted improvement.**

Change the relevant prompt, tool definition, data schema, or architectural component.

Avoid changing several unrelated elements at once when doing so would make the results difficult to interpret.

**Step 6: Run the tests again.**

Compare the updated agent's behavior with its previous performance. Check whether the original problem has been resolved and whether new problems have appeared.

**Step 7: Repeat.**

Continue improving the system as you discover new failure patterns.

### What Should You Measure?

You can track several indicators to assess whether the agent is becoming more reliable.

| Metric | What to Check |
| --- | --- |
| Task completion | Were all required research tasks completed or explicitly accounted for? |
| Status correctness | Do task statuses accurately represent what happened? |
| Search quality | Were the searches relevant to the assigned questions? |
| Report completeness | Does the final report address the important research questions? |
| Error handling | Were failures recorded and handled appropriately? |
| Efficiency | How many tool calls, retries, tokens, and model operations were required? |

A system that completes every task but generates a poor report is not successful. Likewise, an agent that produces a good report by silently skipping required operations may violate the intended process.

Evaluate both the final result and the execution that produced it.

## 11. Try It Yourself

**Task:** Imagine you've built a deep research agent with a single orchestrator that plans searches, executes them, manages a spreadsheet, and writes the final report.

During testing, you discover four problems:

- The agent creates five tasks but executes only three.
- It sometimes uses inconsistent task statuses such as `completed`, `done`, and `finished`.
- Its context grows so large that it begins repeating searches and overlooking previous findings.
- When a search fails, the final report does not mention the missing information.

Design an improved system.

Your solution should address:

1. Whether you would keep one agent or introduce a dedicated search worker.
2. Which responsibilities belong to the orchestrator and which belong to the worker.
3. What instructions and task status values you would define.
4. What information the worker should receive and return.
5. How you would manage context length and handle failures.
6. How you would test whether the revised system is more reliable.

<details>
<summary><strong>Example Answer</strong></summary>
<div>

**1. Improve the architecture**

I would introduce a dedicated search worker if the orchestrator's combined responsibilities were contributing to missed tasks or excessive context.

The orchestrator would plan the research, maintain task state, evaluate findings, and prepare the report. The worker would execute an assigned search and return structured findings.

For a small research application, I would first consider whether clearer instructions and better state tracking could solve the problems without adding a second agent.

**2. Define responsibilities**

The orchestrator would create the research plan, record tasks before execution, delegate searches, process responses, update task statuses, and verify completion.

The worker would receive a search query, execute the search using its available tools, summarize relevant findings, and report any failures.

**3. Standardize instructions and statuses**

I would define a fixed set of permitted status values:

- `todo`: The task has not started.
- `in_progress`: The task is being executed.
- `done`: The task completed successfully and its results were recorded.
- `failed`: The task could not be completed after the permitted recovery attempts.

Before submitting the report, the orchestrator would verify that every important task has an appropriate final status.

**4. Standardize communication**

The worker would receive only the search query, relevant constraints, and instructions needed for the assigned task.

It would return a structured response containing its status, findings, source references, and any limitations or errors.

The system would validate the response before updating the tracker.

**5. Manage context and errors**

I would store task state outside the conversation, summarize findings while preserving their source references, and avoid repeatedly passing irrelevant history to the worker.

If a search failed, the system would retry once with a revised query when appropriate. If it failed again, the tracker would record the failure, and the orchestrator would decide whether the remaining research could continue reliably.

The final report would explicitly identify any important unresolved questions.

**6. Evaluate the changes**

I would test the system using research questions that include overlapping tasks, unavailable sources, incomplete results, and different levels of complexity.

I would compare task completion, status correctness, search quality, report completeness, and execution cost before and after the changes.

The goal would be to improve reliability while keeping the architecture and context no more complicated than necessary.

</div>
</details>

## What's Next

You've now explored how context engineering applies to a real agent architecture, from separating responsibilities and defining tools to managing task state, controlling context growth, and handling failures.

The key takeaway is that **reliable AI agents emerge from the combination of clear context, focused responsibilities, well-defined interfaces, and systematic testing**. A longer system prompt alone cannot compensate for an architecture that makes important operations difficult to track or validate.

As you build more advanced agentic systems, these principles will help you decide where to introduce additional components, which information to preserve, and how to evaluate whether your design is actually improving performance.