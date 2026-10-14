---
sidebar_position: 6
---

# Deep Agents

You've learned how function calling allows AI agents to interact with external tools, how context engineering improves their behavior, and how multiple agents can collaborate on complex tasks.

But what happens when a task becomes so large that a simple agent struggles to manage it?

Imagine asking an AI assistant to research an entire industry, compare competitors, analyze market trends, examine dozens of sources, and produce a comprehensive report. The agent must plan its work, keep track of progress, remember important findings, and verify its conclusions.

A basic agent that handles everything in one continuous interaction may lose track of important details, repeat previous work, or overlook unfinished tasks.

To handle these challenges, developers are exploring more sophisticated agent architectures known as **Deep Agents**.

In this guide, you'll learn what Deep Agents are, how they approach complex tasks, and how planning, specialized agents, persistent memory, context engineering, and verification work together to improve reliability.

## 1. What Are Deep Agents?

**Deep Agents are AI agent systems designed to handle complex, multi-step tasks by combining structured planning, persistent context, specialized execution, and verification.**

Unlike a simple agent that responds to a request with a single tool call or a short sequence of actions, a Deep Agent is designed to coordinate a larger body of work toward a long-term goal.

For example, a basic research agent might search for information about a company and summarize the results.

A Deep Agent could approach the same task by:

1. Breaking the research question into smaller tasks.
2. Creating a structured plan and tracking its progress.
3. Delegating searches to specialized sub-agents.
4. Saving findings and intermediate work outside the immediate conversation.
5. Investigating gaps or conflicting information.
6. Checking whether the research objectives have been met.
7. Combining the results into a coherent final report.

The difference is not simply the number of steps involved. It is how the system **organizes, coordinates, remembers, and verifies its work over an extended task**.

The term *Deep Agents* describes an emerging approach to agent design rather than one universally standardized architecture. Different implementations may combine these capabilities in different ways.

### Shallow Agents vs. Deep Agents

For learning purposes, it helps to compare two broad approaches.

| Aspect | Simpler Agent Systems | Deep Agent Systems |
| --- | --- | --- |
| **Planning** | May handle a short sequence of actions | Maintain structured plans for larger tasks |
| **Task management** | Often relies on the immediate interaction | Tracks progress across multiple subtasks |
| **Execution** | May handle most work in one agent | Can delegate work to specialized sub-agents |
| **Memory** | Often relies heavily on the current context | Can store intermediate work in external memory |
| **Context management** | May accumulate information in one conversation | Can organize, retrieve, and summarize relevant context |
| **Verification** | May rely mainly on the final response | Can include dedicated checks and evaluation stages |
| **Best suited for** | Straightforward, bounded tasks | Complex tasks involving many dependent operations |

This comparison describes common design tendencies, not strict categories. A simple architecture can still be reliable, and a complex architecture can still fail.

The objective is not to make every agent deep. It is to provide the structure required by tasks that cannot be handled reliably through a simpler approach.

## 2. Planning: Turning Large Goals into Manageable Tasks

One of the most important characteristics of a Deep Agent is its ability to maintain a structured plan.

When a task involves many operations, the agent needs more than a general instruction to complete the work. It needs to understand what must be accomplished, which steps are necessary, and what remains unfinished.

Consider this request:

> Research the market for cloud-based business software and prepare a report for small-business owners.

This request contains several distinct objectives. The agent may need to examine market trends, identify customer challenges, compare competing products, and summarize the opportunities.

Attempting to complete everything without a plan makes it easier to overlook important questions.

### Create a Structured Plan

The agent could begin by creating a task list:

| Task ID | Task | Status |
| --- | --- | --- |
| 1 | Identify major market trends | `todo` |
| 2 | Investigate small-business needs | `todo` |
| 3 | Compare competing products | `todo` |
| 4 | Identify adoption barriers | `todo` |
| 5 | Synthesize the findings into a report | `todo` |

As the work progresses, the agent updates the status of each task.

For example, after completing the first search, the agent records its findings and marks the corresponding task as completed.

The plan becomes a representation of the work that has been completed and the work that remains.

### A Plan Should Evolve

A Deep Agent should not necessarily treat its initial plan as an unchangeable sequence.

Suppose the competitor research reveals that most products target large enterprises rather than small businesses. This finding may suggest that the agent should investigate affordable alternatives or products designed for smaller companies.

The agent can update its plan to address the newly discovered question.

Similarly, if a search fails, it can retry, use another source, or record that the information could not be obtained.

This ability to revise a plan is particularly useful for tasks where the correct next step depends on what the agent discovers.

### Why Planning Matters

Structured planning helps an agent:

- Keep track of outstanding work.
- Avoid repeatedly performing completed tasks.
- Identify dependencies between subtasks.
- Recover from failures.
- Determine when the overall objective has been satisfied.

However, a task list alone does not guarantee successful execution. The system must also track task state correctly and verify that completed tasks actually produced the expected results.

**The key idea:** A plan turns a broad objective into manageable work that the agent can track, execute, and revise.

## 3. Orchestrator and Sub-Agent Architecture

As tasks become more complex, one agent may have too many responsibilities to manage efficiently.

Imagine a research agent that must plan searches, operate tools, organize files, summarize findings, check sources, track task statuses, and write a report.

Every responsibility introduces additional instructions and information. As the task progresses, the agent's context can grow substantially.

One approach is to divide the work among an **orchestrator** and several **specialized sub-agents**.

### What Is an Orchestrator?

An **orchestrator** coordinates the overall task.

It understands the user's goal, creates the plan, determines which work should be delegated, tracks progress, and combines the results into a final response.

It does not necessarily perform every operation itself.

### What Are Sub-Agents?

**Sub-agents** are agents assigned specific responsibilities within the larger task.

For example, a research system might include:

| Agent | Responsibility |
| --- | --- |
| **Research Orchestrator** | Plans the investigation, delegates tasks, and coordinates execution |
| **Search Agent** | Searches for relevant information and returns findings |
| **Analysis Agent** | Examines collected information and identifies patterns |
| **Verification Agent** | Checks claims, evidence, and task completion |
| **Writing Agent** | Organizes verified findings into a report |

Each sub-agent receives the information needed for its assigned task and returns results to the orchestrator.

This separation allows different agents to use different instructions, tools, and models according to their responsibilities.

### How Do They Work Together?

Consider a user who asks for a report comparing three competitors.

The process could follow this sequence:

1. The orchestrator identifies the information needed for each competitor.
2. It creates research tasks and assigns them to search agents.
3. The search agents collect information and return their findings.
4. The orchestrator combines the results and identifies missing information.
5. An analysis agent compares the competitors using the collected evidence.
6. A verification agent checks important claims and identifies unsupported conclusions.
7. The orchestrator integrates the verified results into the final report.

The orchestrator remains responsible for the overall objective, while the sub-agents focus on their individual tasks.

### Why Separate Responsibilities?

This architecture offers several potential benefits.

**Focused responsibilities**

A search agent does not need to manage the entire research plan. It can concentrate on finding and summarizing relevant sources.

**More manageable context**

Each agent can work with a smaller, task-specific context instead of receiving the entire conversation history.

**Flexible model selection**

A planning task may require stronger reasoning capabilities, while a straightforward search or classification task may work well with a faster, less expensive model.

**Independent evaluation**

Different components can be tested separately. If search quality is poor, you can investigate the search agent without immediately redesigning the entire system.

### Do You Always Need Multiple Agents?

No.

Multi-agent architectures introduce coordination overhead. The orchestrator must delegate tasks, process outputs, manage failures, and reconcile potentially conflicting findings.

A single agent may be simpler and more cost-effective for tasks that do not require specialized responsibilities.

Use sub-agents when dividing the work provides a meaningful benefit, such as reducing context complexity, enabling independent research, or supporting specialized execution.

**The key idea:** An orchestrator coordinates the overall goal, while specialized sub-agents handle focused parts of the work.

## 4. Context Retrieval and Persistent Memory

Long-running tasks create a memory challenge.

As an agent searches for information, it accumulates findings, intermediate results, tool outputs, and decisions. Keeping everything in one conversation can make the context increasingly large and difficult to manage.

Deep Agents can address this problem by storing important information outside the immediate conversation.

### What Is Persistent Memory?

**Persistent memory** is information stored so that the system can retrieve and reuse it beyond the immediate model interaction.

Depending on the application, the stored information might include:

- Research notes and summaries.
- Task lists and execution status.
- Source references and extracted evidence.
- Intermediate analysis results.
- Files created during execution.
- Relevant information from previous interactions.

For example, a research agent might save a summary of the competitor analysis to a file rather than repeatedly including every original search result in its context.

Later, when the agent needs to compare pricing, it can retrieve the relevant findings and continue working.

### Different Ways to Store Information

There are several ways to provide external memory.

**Files and documents**

Useful for research notes, reports, code, structured plans, and other intermediate work.

**Databases**

Useful for structured information such as task status, customer records, and execution history.

**Vector databases**

Useful for retrieving relevant passages or documents based on semantic similarity.

**Conversation or task state**

Useful for preserving the current objective, completed steps, pending work, and other information needed to resume execution.

These approaches solve different problems. A vector database is not a replacement for a structured task tracker, and a task tracker is not necessarily the best place to store large documents.

The appropriate storage depends on what information must be preserved and how it needs to be retrieved.

### Context Retrieval

Storing information is only half of the problem. The agent must also retrieve the appropriate information when needed.

Suppose a research agent has collected information about ten competitors. When investigating one competitor's pricing, it should retrieve the relevant notes rather than loading every finding from the entire investigation.

The system can retrieve information using several approaches.

**Keyword search** finds information containing specific terms.

**Semantic search** finds information related to a query based on meaning rather than exact wording.

**Structured lookup** retrieves information using identifiers, filters, or predefined database queries.

A more advanced system can combine these approaches and select an appropriate retrieval strategy for the task.

For example, it might use a structured query to retrieve the current status of a research task, then use semantic search to locate relevant evidence in previously collected documents.

### Memory Requires Careful Management

Persistent storage does not automatically make an agent more reliable.

Stored information can become outdated, incomplete, duplicated, or associated with the wrong task.

A good memory design should distinguish between current state, historical findings, verified facts, and unresolved assumptions.

It should also preserve relevant source references and update information when newer evidence changes an earlier conclusion.

**The key idea:** Persistent memory allows an agent to preserve important work, while context retrieval helps it access the information needed for the current step without carrying everything into every model interaction.

## 5. Context Engineering for Deep Agents

You've already learned that context engineering involves designing the information available to an AI agent.

For a Deep Agent, context engineering becomes especially important because the system may involve multiple agents, numerous tools, persistent memory, and long-running task plans.

The challenge is not simply writing a detailed system prompt. It is deciding which information each component needs, how instructions should be organized, and how context should change as the work progresses.

### Make Instructions Explicit

The orchestrator should know when to create a plan, when to delegate work, and how to track results.

A search agent should know what information to collect, which tools it can use, and what its response must contain.

A verification agent should know what evidence to check and how to report unsupported claims.

For example, an orchestrator might follow these instructions:

```text
ORCHESTRATION RULES

1. Break complex requests into manageable tasks.
2. Record tasks before delegating them.
3. Delegate specialized work to the appropriate sub-agent.
4. Provide each sub-agent with only the context needed for its task.
5. Record and review each returned result.
6. Revisit the plan when new information changes the required work.
7. Verify that important tasks are completed or explicitly
   identified as unresolved before returning the final result.
```

These instructions describe expectations that the orchestrator can apply across different research tasks.

### Define How Agents Collaborate

When several agents work together, the system needs clear communication rules.

For example, each sub-agent might be required to return:

- Its task identifier.
- Its completion status.
- Its findings.
- Supporting sources or evidence.
- Any errors or limitations.
- Questions that require further investigation.

A consistent response format makes it easier for the orchestrator to integrate the results.

It is also important to define what happens when agents disagree. The orchestrator should not automatically accept whichever answer appears most confident. Conflicting claims may require additional evidence or independent verification.

### Manage Context Deliberately

Deep Agents should not receive every available instruction and every stored result by default.

Instead, provide the context that is relevant to the current operation.

A search agent might need a query, a source restriction, and an expected output format. It usually does not need the complete research conversation.

The orchestrator, by contrast, needs enough information to understand the overall objective and integrate the results.

This approach keeps responsibilities distinct and makes context easier to maintain.

### Keep Instructions Consistent

Context often comes from several places: system prompts, task-specific instructions, tool descriptions, retrieved documents, and stored state.

These sources should not contradict one another.

For example, the system prompt might require the agent to verify every source, while a task instruction tells it to produce the final report immediately after the first search.

Such conflicts can lead to unpredictable behavior.

Review the entire context design, not just the main prompt, when investigating inconsistent results.

**The key idea:** Context engineering makes sure each component has the relevant instructions and information needed to perform its responsibilities effectively.

## 6. Verification: Checking the Agent's Work

A Deep Agent may perform many operations and produce a detailed result, but complexity does not guarantee correctness.

The system might retrieve inaccurate information, misinterpret a source, overlook a required task, or combine findings into an unsupported conclusion.

This is why **verification** is an important part of the architecture.

Verification involves checking whether the agent's outputs and actions satisfy the required standards.

### What Should Be Verified?

Different tasks require different forms of verification.

For a research agent, you might check:

- Whether important claims have supporting sources.
- Whether the sources actually support those claims.
- Whether publication dates and other relevant details are accurate.
- Whether conflicting findings have been acknowledged.
- Whether all required research questions have been addressed.
- Whether the final report follows the requested format.

For a coding agent, verification might involve running tests, checking program behavior, and examining whether the implementation satisfies the requirements.

For a customer support agent, it might involve checking the relevant account records and confirming that the proposed action follows the applicable policy.

Verification should be tailored to the task rather than treated as a generic instruction to "check your work."

### Automated Verification

A system can use tools or specialized evaluation components to check outputs.

For example, a research report verifier might examine whether each major factual claim includes a source reference and whether the references can be retrieved.

An LLM-based evaluator can also assess qualities such as relevance, completeness, and consistency against an explicit rubric.

This approach is sometimes called **LLM-as-a-Judge**.

However, a language model evaluating another language model is not an infallible source of truth. The evaluator may repeat similar mistakes or approve a convincing but incorrect claim.

Whenever possible, combine model-based evaluation with external evidence, deterministic checks, or tests.

### Human Verification

Some decisions require human judgment or authorization.

For example, an agent might prepare a financial analysis, but an analyst should review the result before it is used to make a consequential decision.

Likewise, an agent that proposes a significant account change may need explicit approval before executing it.

Human review is particularly useful when errors have substantial consequences, the evidence is ambiguous, or the system operates outside its validated conditions.

### Verification Should Influence What Happens Next

Verification is more useful when its results can guide further work.

Suppose a verification agent discovers that two important claims in a research report lack reliable evidence.

Instead of simply labeling the report as incorrect, the system can send those claims back for further investigation.

The orchestrator may create additional search tasks, retrieve alternative sources, and update the report before running verification again.

The process becomes:

1. Produce an initial result.
2. Verify the result against defined requirements.
3. Identify failures or missing evidence.
4. Perform additional work where necessary.
5. Verify the revised result.

This does not mean every result must pass through endless review. Systems should define appropriate retry limits and clear completion criteria.

**The key idea:** Verification turns quality checks into a deliberate part of the execution process instead of relying entirely on the agent's confidence in its own answer.

## 7. Putting the Components Together

Let's combine these ideas in a practical example.

Imagine you're building a Deep Agent to power a customer support system for an online learning platform.

Students may ask about courses, payment issues, enrollment, certificates, or technical problems.

Some requests are straightforward. Others require the system to consult several sources, investigate an issue, and coordinate multiple actions.

### The Architecture

The system could contain the following components:

| Component | Responsibility |
| --- | --- |
| **Orchestrator** | Understands the request, creates the plan, and coordinates the work |
| **Knowledge Retrieval Agent** | Searches approved course documentation and support articles |
| **Account Lookup Tool or Agent** | Retrieves authorized enrollment and account information |
| **Analysis Component** | Uses the collected information to determine the likely answer or next step |
| **Verification Component** | Checks the proposed response against the available evidence and applicable rules |
| **Persistent Storage** | Maintains task state, relevant notes, and execution records |

Not every component needs to be a separate agent. A database lookup may be better implemented as an ordinary function, while a specialized agent may be useful for interpreting a complex collection of documents.

The architecture should reflect the actual requirements rather than turning every operation into an agent.

### A Request in Action

Suppose a student asks:

> I completed a course, but I can't find my certificate. Can you help me?

The system might proceed as follows.

**Step 1: Understand the request**

The orchestrator identifies that the student needs help locating a course certificate.

**Step 2: Plan the investigation**

It determines that it may need to review the certificate instructions and check the student's enrollment or completion status.

**Step 3: Retrieve relevant information**

The knowledge retrieval component searches approved documentation for the certificate requirements and delivery process.

**Step 4: Check authorized account information**

If the system has permission to access the student's account, it retrieves the relevant course completion status.

**Step 5: Evaluate the findings**

The orchestrator determines whether the available information explains the problem.

If the student has not completed the required steps, the response might explain what remains. If the completion requirements are satisfied but the certificate is missing, the issue may require further investigation.

**Step 6: Verify the response**

The system checks that its answer is consistent with the documentation and retrieved account information.

**Step 7: Respond or escalate**

The agent provides an evidence-based response or routes the unresolved issue to a human support representative.

Throughout the process, the system can record task progress and preserve relevant information needed to resume the investigation.

### Why This Is More Than a Chatbot

A basic chatbot might respond with general advice about downloading a certificate.

The Deep Agent architecture can coordinate several operations to investigate the student's actual situation, while using tools and documented policies to guide its response.

However, the architecture does not guarantee a correct result. The quality of the outcome still depends on the retrieved information, tool reliability, permissions, instructions, and verification process.

## 8. When Should You Build a Deep Agent?

Deep Agent architectures are useful for some demanding tasks, but they are not the right choice for everything.

### Use a Deep Agent When...

- The task involves many interdependent subtasks.
- The execution plan may need to change as new information is discovered.
- The system must preserve substantial intermediate work.
- Different subtasks benefit from specialized capabilities.
- The final result requires independent verification.
- The task may need to recover from failures and resume unfinished work.

Examples include deep research, complex coding projects, extensive data analysis, and support investigations that involve multiple information sources.

### A Simpler Agent May Be Better When...

- The task has only a few steps.
- The required tools and execution path are straightforward.
- Most operations can be completed within a short interaction.
- Additional planning and delegation would add unnecessary overhead.
- The task does not require substantial persistent memory.

For example, an agent that retrieves a shipping status and explains it probably does not need a planner, several sub-agents, an external memory system, and a dedicated verification agent.

A direct tool call with appropriate validation may be sufficient.

### Consider the Trade-Offs

Deep Agent architectures can improve organization and support more complex work, but they also introduce costs and failure modes.

| Benefit | Potential Trade-Off |
| --- | --- |
| Structured planning | Maintaining and updating the plan introduces additional work |
| Specialized agents | Delegation and coordination increase complexity |
| Persistent memory | Storage, retrieval, and stale information require management |
| Richer context | More context can increase latency and token costs |
| Dedicated verification | Additional checks require time and resources |
| Flexible execution | More decisions create more opportunities for unexpected behavior |

The goal is to choose an architecture that matches the task's complexity and reliability requirements.

**Start simple and introduce additional components only when they solve a demonstrated problem.**

## 9. Try It Yourself

**Task:** Imagine you're building an AI system that investigates why a small business's sales dropped during the previous month.

The system has access to sales records, product information, customer feedback, and external market research.

Your first version is a simple agent that receives the question, performs a few searches, and generates a report.

However, the agent sometimes overlooks relevant data, repeats its searches, and makes unsupported claims about why sales declined.

Design a Deep Agent architecture to improve the system.

Answer the following questions:

1. How would the agent break down the investigation into tasks?
2. Which responsibilities should belong to the orchestrator, and which could be delegated to specialized components?
3. What information should be stored in persistent memory?
4. How should the system retrieve information when it needs to revisit a previous finding?
5. What should the verification component check before the final report is submitted?
6. How would the system handle missing data or conflicting evidence?

<details>
<summary><strong>Example Answer</strong></summary>
<div>

**1. Create a structured research plan**

The orchestrator could create tasks to examine changes in total revenue, product-level sales, customer feedback, and relevant market conditions.

It would record each task's status and update the plan as new findings reveal additional questions.

**2. Separate responsibilities**

The orchestrator would coordinate the investigation and integrate the results.

Specialized components could retrieve sales data, analyze product performance, summarize customer feedback, and research external market conditions.

A separate verification component could check important claims before the report is finalized.

**3. Store useful information**

Persistent storage could contain the research plan, task statuses, relevant data summaries, source references, calculations, and unresolved questions.

The system should distinguish verified findings from assumptions and hypotheses.

**4. Retrieve previous findings**

The agent could use structured queries to retrieve task statuses and sales metrics, then use keyword or semantic search to locate relevant research notes.

This allows it to revisit useful findings without repeating the entire investigation.

**5. Verify the final report**

The verification component should check whether calculations match the underlying data, important claims have supporting evidence, alternative explanations have been considered, and the report clearly distinguishes facts from hypotheses.

**6. Handle uncertainty**

If data is missing, the system should identify the limitation and investigate alternative sources when appropriate.

If evidence conflicts, it should compare the reliability and relevance of the sources instead of selecting whichever explanation appears most convincing.

If the available evidence does not establish why sales declined, the final report should present plausible explanations as hypotheses rather than confirmed causes.

</div>
</details>

## What's Next

You've now learned how Deep Agents combine structured planning, orchestration, specialized sub-agents, persistent memory, context engineering, and verification to manage complex tasks.

The key takeaway is that **a Deep Agent is not simply an agent that performs more tool calls; it is a system designed to organize, preserve, coordinate, and verify work across a long-running task**.

These capabilities can make sophisticated AI applications more manageable, but they also require deliberate architectural choices and careful evaluation.

As you continue building agentic systems, pay particular attention to how you verify intermediate results and final outputs. Reliable execution is not just about completing a task—it's about establishing that the result satisfies the requirements and is supported by appropriate evidence.