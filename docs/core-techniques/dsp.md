---
sidebar_position: 12
---

# Directional Stimulus Prompting (DSP)

You’ve learned how to optimize prompts automatically using frameworks like APE, select high-value annotations with Active-Prompt, and ground model responses using external tools or RAG.

However, when working with large, black-box language models (like commercial LLMs that you cannot fine-tune directly), guiding them toward a specific, nuanced output — such as incorporating particular keywords, following subtle style constraints, or steering summarization focus — can be extremely difficult with static prompts.

How can you dynamically guide a frozen black-box model for every unique input instance without altering its internal weights?

This is the idea behind **Directional Stimulus Prompting (DSP)**.

---

## 1. What Is Directional Stimulus Prompting?

Directional Stimulus Prompting is a framework that uses a small tunable policy model to generate a “stimulus” (a short hint) which is then added to the prompt of a larger, frozen language model.

The process works as follows:

1. A small policy language model generates a directional hint based on the input.
2. The hint is inserted into the prompt given to the main (black-box) LLM.
3. The main LLM produces the final output, guided by both the original instruction and the hint.

The policy model can be optimized (for example with reinforcement learning) so that the hints it produces lead to better results from the main model.

:::info The Policy-Model Approach
Think of the small policy model as an expert coach whispering brief, targeted hints into the ear of a massive model, telling it what focus areas or keywords to emphasize in its response.
:::

---

## 2. How Directional Stimulus Prompting Works

DSP connects stimulus generation, target-model inference, and evaluation in a learning process.

### Step 1: Provide the Original Input

For example, a system might receive a business report containing information about revenue, costs, customer feedback, and future plans.

The system also needs a clear task, such as producing a concise summary.

### Step 2: Generate a Directional Stimulus

The policy language model receives the input and generates a stimulus intended to guide the target model toward the desired output.

For a business report, the stimulus might be: revenue trends, profitability, operating costs, business risks

For another report, the stimulus could emphasize customer satisfaction, product quality, and delivery performance.

The policy model is trained to discover which stimuli are useful for the task. The hints are not simply selected randomly or manually rewritten for every input.

### Step 3: Combine the Stimulus with the Input

The original input and generated stimulus are provided to the target model.

Conceptually, the target model receives something like:

```text
Task:
Summarize the following business report.

Focus on these aspects:
revenue trends, profitability, operating costs, business risks

Report:
[Original report]
```

The target model uses the hints alongside the original report to generate its summary.

The example above illustrates how a stimulus can be incorporated into a prompt. It is not the exact format required by the original DSP implementation.

### Step 4: Evaluate the Output

Next, evaluate the target model's output against the task's objectives.

For a summarization task, evaluation might consider whether the summary captures important information from a reference summary. Other measures can assess relevance, completeness, or human preferences.

The evaluation provides feedback about whether the generated stimulus helped produce a better result.

### Step 5: Improve the Policy Model

The policy model can be optimized using supervised fine-tuning or reinforcement learning.

In a reinforcement-learning setup, the system uses rewards derived from the target model's output to update the policy model. Stimuli that lead to better results can therefore receive stronger reinforcement through the optimization process.

Over repeated training iterations, the policy model learns to generate more useful hints for different inputs.

---

## 3. Directional Stimulus Prompting vs. Standard Prompting

| Aspect | Standard Prompting | Directional Stimulus Prompting |
|--------|------------------|--------------------------------|
| Guidance | Relies on static instructions or manual cues. | Uses instance-specific, dynamic hints generated automatically. |
| Model Modification | None (static prompt text). | Small policy model is tuned via RL/SFT; target LLM stays frozen. |
| Flexibility | Rigid across different inputs; same prompt applies to all. | Highly adaptive; hints change per input instance to target specific weaknesses. |

---

## 4. When to Use Directional Stimulus Prompting

| Situation                              | Why it helps                                          |
|----------------------------------------|-------------------------------------------------------|
| You want better control over a frozen LLM | Hints steer the model without changing its weights   |
| Instance-specific guidance is useful   | Each input can receive its own tailored stimulus      |
| You can train a small policy model     | Optimization improves the quality of the generated hints |
| Summarization or generation tasks      | Originally shown effective for guiding summary style and content |

This approach is more involved than simple manual prompting, so it is most appropriate when the performance gain justifies the extra system complexity.

---

## 5. Try It Yourself

**Task:** Simulate a Directional Stimulus Prompt manually.

Suppose you want an LLM to summarize a long news article about renewable energy adoption, but you need to make sure the summary explicitly highlights two specific sub-topics: "government subsidies" and "supply chain bottlenecks".

Design a directional stimulus prompt template that accepts an article text along with these generated hints, steering the frozen LLM to integrate them naturally.

<details>
<summary><strong>Example Answer</strong></summary>

**DSP-style template:**

```
Article Text:
{{ article_text }}

Directional Hint / Focus Keywords:
- government subsidies
- supply chain bottlenecks

Instructions:
Write a concise 3-sentence summary of the article. You MUST naturally incorporate both directional hint topics into your summary. Do not list them out; weave them into the narrative flow.

Summary:
```

</details>

---
## What's Next

You've now learned how **Directional Stimulus Prompting (DSP)** uses generated hints to guide a language model toward specific aspects of an input or desired output.

The key is to **adapt the guidance to each input instead of relying only on a fixed prompt**.

However, better instructions and targeted hints cannot eliminate every computational error. When a task involves complex calculations or precise date arithmetic, a language model may still produce an incorrect result.

That's where **Program-Aided Language Models (PAL)** come in — a technique that lets a model generate a program and delegate the actual computation to an execution environment.