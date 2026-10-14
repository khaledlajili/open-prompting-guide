---
sidebar_position: 14
---

# ReAct Prompting

You’ve learned how to guide models through step-by-step text reasoning, ground them with external facts using RAG, and even let them write code execution scripts using PAL.

However, what happens when a task requires a continuous, dynamic loop where a model needs to think, search the real world, observe the results, update its plan, and search again before finally answering?

This synergy between thinking and doing is captured in **ReAct (Reasoning and Acting)**.

---

## 1. What Is ReAct?

**ReAct** is a prompting framework that instructs language models to generate both verbal reasoning traces ("Thoughts") and task-specific actions in an interleaved manner.

The central idea is that reasoning and acting can support one another:

- **Reasoning** helps the model understand the problem, plan its next step, interpret observations, and adjust its approach.
- **Acting** allows the model to interact with external tools and environments to retrieve information or perform operations.

After each action, the model receives an **Observation** and uses it to update its reasoning. This loop continues until the model decides it has enough information to answer.

The combination of reasoning and acting helps the model create better plans, recover from mistakes, and ground its answers in external information.

---

## 2. How ReAct Works

ReAct commonly represents a task-solving process using three elements: **Thought, Action, and Observation**.

These elements repeat until the system has enough information to complete the task.

### Step 1: Thought

The model identifies what it needs to accomplish and determines a useful next step.

A thought can help the model break a problem into smaller tasks, choose an appropriate tool, and adapt when new information becomes available.

### Step 2: Action

The model selects an action that interacts with an available tool or environment.

An action might involve:

- Searching the web.
- Looking up information in a database.
- Calling an API.
- Running a calculation.
- Interacting with an application.
- Performing an operation in a simulated environment.

### Step 3: Observation

After the action executes, the environment returns an observation.

An observation contains the result of the action, such as a search result, database record, calculation, or status message.

### Step 4: Repeat the Cycle

The model interprets the observation and determines what to do next.

The system then executes another action and receives another observation.

This cycle can repeat as necessary. The model may change its plan when a tool returns unexpected results or when additional information is required.

### Step 5: Produce the Final Answer

Once sufficient information has been collected, the model produces its answer.


:::info ReAct vs. ART

ART also combines reasoning and tool use. It emphasizes selecting demonstrations from a task library and using them to guide the model's reasoning and tool calls.

ReAct emphasizes the interleaving of reasoning, actions, and observations during task execution.

The techniques overlap conceptually, but their frameworks and implementation details differ.
:::

---

## 3. Try It Yourself

**Task:** Write a short ReAct-style trajectory for this question. You can use a Search action and a Calculator action.

```text
Who directed the movie Inception, and what is the square root of the year it was released?
```

<details>
<summary><strong>Example Answer</strong></summary>

**ReAct-style trajectory:**

```text
Thought 1: I need to find the director of Inception and the year it was released.
Action 1: Search[Inception director and release year]
Observation 1: Inception was directed by Christopher Nolan and released in 2010.

Thought 2: Now I need the square root of 2010.
Action 2: Calculator[sqrt(2010)]
Observation 2: 44.833

Thought 3: I have both pieces of information.
Action 3: Finish[Christopher Nolan directed Inception. The square root of 2010 is approximately 44.83.]
```

</details>

---
## What's Next

You've now learned how **ReAct (Reasoning and Acting)** combines reasoning with actions and observations in an iterative problem-solving loop.

The key is to **use feedback from each action to determine what to do next**, rather than following a fixed sequence of steps.

But even when an agent interacts with its environment, it can repeat the same mistakes across multiple attempts. How can it use feedback from previous failures to improve its next attempt?

That's where **Reflexion** comes in — a framework that uses verbal self-reflection and memory to help agents learn from previous experiences without updating their model weights.

