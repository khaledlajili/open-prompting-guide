---
sidebar_position: 9
---

# Automatic Reasoning and Tool-use (ART)

You’ve learned how to break tasks into linear pipelines, explore branching thoughts, and ground models using external knowledge through RAG.

Many real tasks, however, also require using tools — calculators, search engines, code interpreters, or APIs. Manually writing demonstrations that interleave reasoning and tool use for every new task is time-consuming.

What if a model could automatically select the right tools and generate its own multi-step reasoning program in a zero-shot fashion?

This is the core idea behind **Automatic Reasoning and Tool-use (ART)**

---

## 1. What Is Automatic Reasoning and Tool-use (ART)?

**ART** is a framework that uses a frozen language model to automatically generate intermediate reasoning steps as a program, seamlessly interleaving multi-step reasoning with external tool calls.   

Instead of writing custom scripts for every new task, ART leverages a task library containing task-specific demonstrations of reasoning and tool use. When given a brand-new problem, ART automatically selects relevant examples and guides the model through a structured execution loop.   

:::info Automated Interleaving
ART bridges the gap between static text reasoning and dynamic tool execution, allowing language models to decide when to think, when to call a tool, and how to incorporate tool outputs back into the reasoning chain.
:::

---

## 2. How ART Works

At a high level the process looks like this:

1. **Select demonstrations:** From a library of previous tasks, ART retrieves examples that show useful patterns of reasoning and tool use.

2. **Generate a reasoning program:** The model produces a sequence of steps, written in a form that can include tool calls.

3. **Pause and call tools:** When the generation reaches a tool call, the system executes the tool and feeds the output back into the model.

4. **Resume and finish:** The model continues from the tool result and produces the final answer.

---

## 3. Key Characteristics and Advantages

|Feature|Manual Tool-Use Scripting|Automatic Reasoning and Tool-use (ART)|
|---|---|---|
|Demonstrations|Hand-crafted for each specific task.|Automatically selected from a task library.|
|Extensibility|Hard to scale; requires rewriting code for new tools.|Highly extensible; humans can easily add new tools or fix reasoning steps in the library.|
|Generalization|Rigid execution paths.|Zero-shot generalization to unseen tasks across benchmarks like BigBench and MMLU.|
|Human-in-the-Loop|Difficult to intervene mid-execution.|Allows seamless human feedback to correct intermediate reasoning errors.|

:::tip Extensibility via Libraries
Because ART relies on a modular task and tool library, you don't need to retrain the underlying model to teach it new tricks. You simply update the library with examples of the new tool in action.
:::

---

## 6. Try It Yourself

**Task:** Design a pseudo-code or step-by-step ART program template for a model that needs to calculate the distance between two cities and check current weather conditions using external tools.

Available Tools:

- **Calculator(expression):** Solves math expressions.
- **WeatherAPI(city):** Fetches current temperature.
- **MapDistance(city1, city2):** Returns distance in miles.

Create a structured prompt template that shows how ART interleaves text reasoning with these tool calls.

<details>
<summary><strong>Example Answer</strong></summary>

**ART Program Template:**

```
Task: Calculate travel time for a 60 mph road trip from Paris to Brussels and check arrival weather.

Execution Program:
Step 1: [Reasoning] Identify the two locations needed for distance calculation.
Step 2: [Tool Call] distance = MapDistance("Paris", "Brussels")
[Pause & Inject Output]: distance = 193 miles

Step 3: [Reasoning] Calculate travel time assuming an average speed of 60 mph.
Step 4: [Tool Call] hours = Calculator(193 / 60)
[Pause & Inject Output]: hours = 3.21 hours

Step 5: [Reasoning] Check destination weather for packing recommendations.
Step 6: [Tool Call] weather = WeatherAPI("Brussels")
[Pause & Inject Output]: weather = 14°C, rainy

Step 7: [Final Answer Synthesis] The drive is 193 miles, takes about 3.2 hours at 60 mph, and the weather in Brussels is 14°C and rainy. Pack an umbrella!
```

</details>

---
## What's Next

You've now learned how **Automatic Reasoning and Tool-use (ART)** combines multi-step reasoning with external tool execution.

The key idea is to **select relevant demonstrations, generate intermediate steps, and incorporate tool outputs into the ongoing process**.

But building effective AI systems also depends on the instructions that guide their behavior. Manually writing and testing different prompts can become time-consuming.

That's where **Automatic Prompt Engineer (APE)** comes in — a framework that automatically generates, evaluates, and selects instructions to improve performance on a given task.