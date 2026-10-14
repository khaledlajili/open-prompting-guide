---
sidebar_position: 11
---

# Active-Prompt

You’ve learned how techniques like Few-Shot CoT rely on human-annotated step-by-step examples to guide language models through complex reasoning tasks.

However, standard few-shot methods use a fixed, static set of examples chosen arbitrarily by humans. The problem is that these fixed examples might not be the most effective demonstrations for every task, nor do they address the specific edge cases where the model struggles most.

How can we automatically identify which questions a model is most confused about so we only annotate the most helpful examples?

This is the idea behind **Active-Prompt**: use the model's uncertainty to decide which examples deserve human attention.

---

## 1. What Is Active-Prompt?

**Active-Prompt** is an adaptive prompting framework that uses uncertainty estimation to select the most informative questions for human annotation. Inspired by active learning in traditional machine learning, it ensures that human effort is spent annotating only the examples that provide the highest value to the model.

Instead of randomly choosing or hand-picking a fixed set of exemplars, the approach:

1. Lets the model answer a pool of training questions multiple times
2. Measures how uncertain the model is on each question
3. Asks humans to annotate only the most uncertain questions with step-by-step reasoning
4. Uses those newly annotated examples as the final CoT demonstrations

---

## 2. How Active-Prompt Works

The process can be summarized in four steps:

1. **Generate multiple answers:** For each training question, the model produces *k* different answers (with or without existing CoT examples).

2. **Measure uncertainty:** An uncertainty score is calculated for each question. A common way is to look at disagreement among the *k* answers — the more the answers differ, the higher the uncertainty.

3. **Select questions for annotation:** The questions with the highest uncertainty are chosen for human annotation.

4. **Use the new exemplars:** Humans write Chain-of-Thought reasoning for the selected questions. These annotated examples are then used to prompt the model on the actual test questions.

:::info The key idea
Active-Prompt uses **model uncertainty to guide human annotation**. Instead of choosing examples randomly or relying only on intuition, it prioritizes questions where the model's answers disagree.
:::

---

## 3. A Simple Example

Imagine you're developing an AI assistant for a business that answers numerical questions about sales and inventory.

You have a collection of 100 questions but only enough time to annotate a small number of them manually.

You could randomly select 10 questions and write detailed Chain-of-Thought explanations for each one.

Alternatively, you could use an Active-Prompt-style approach.

### Without Active-Prompt

1. Select 10 questions.
2. Write human explanations for those questions.
3. Add the examples to the prompt.
4. Evaluate the model's performance.

The selected questions might be easy ones that the model already solves reliably.

### With Active-Prompt

1. Generate multiple answers for the questions in the pool.
2. Measure the disagreement between answers.
3. Select the questions with the highest estimated uncertainty.
4. Ask a human to annotate their solutions.
5. Include the annotated examples in the prompt.
6. Evaluate the model on a separate set of questions.

This approach directs annotation effort toward questions where the model's behavior appears less reliable.

The difference is not that Active-Prompt removes the need for human expertise. Instead, **it helps decide where that expertise should be applied**.

---
## 3. When to Use Active-Prompt

| Situation                              | Why Active-Prompt helps                               |
|----------------------------------------|-------------------------------------------------------|
| You are building CoT prompts for a new task | Helps find the most informative examples to annotate |
| Annotation budget is limited           | Directs human effort to the questions that matter most |
| Model performance varies a lot across examples | Uncertainty scoring identifies difficult cases       |
| You want better task adaptation        | Produces exemplars more suited to the target task     |

---

## 6. Try It Yourself

**Task:** Simulate the uncertainty selection phase of Active-Prompt to identify which question needs human CoT annotation.

**Scenario:** We queried an LLM 4 times for three different math questions. Below are the generated final answers for each run.

| Question                                                                                   | 1 | 2 | 3  | 4 |
|--------------------------------------------------------------------------------------------|---|---------|----------|---|
| What is 12 x 15?                                                                           | 180 | 180     | 180      | 180 |
| A store gives a 20% discount on a $50 shirt, then adds 8% tax. What is the final price?                 | 43.20 | 43.20   | 40.00    | 43.20 |
| A train leaves Station A at 60 mph. An hour later, a second train leaves at 80 mph. How long until the second train catches up?          | 3 hours | 4 hours | 2.5 hours | 3 hours |
| A customer buys 3 items at 12 DT each and receives a 5 DT discount. What is the final price? | 31 DT | 36 DT   | 31 DT    |

Identify which question has the highest uncertainty and requires a human-annotated CoT exemplar.

<details>
<summary><strong>Example Answer</strong></summary>

**Uncertainty Analysis:**

> Question 1: 100% agreement (180). Zero Uncertainty.<br />
> Question 2: 75% agreement (43.20 vs 40.00). Low Uncertainty.<br />
> Question 3: High disagreement (3 hours, 4 hours, 2.5 hours). Highest Uncertainty.

**Selection:** Question 3 should be selected for human annotation.

**Human Annotation Step:** 
> The human annotator creates a step-by-step exemplar for Question 3:<br />
> 1. Train 1 travels 60 miles in the first hour.<br />
> 2. The relative speed closing the gap is 80 - 60 = 20 mph.<br />
> 3. Time to close 60 miles: 60 / 20 = 3 hours.

Adding this exemplar to the prompt will help the model master relative speed problems moving forward!

</details>

---
## What's Next

You've now learned how **Active-Prompt** uses uncertainty to identify difficult questions and direct human annotation toward the examples most likely to help.

The key is to **spend annotation effort where the model needs the most guidance**, rather than treating every example equally.

But sometimes, the challenge isn't selecting better examples. It's guiding a model toward particular information, keywords, or aspects of an input without changing the main model's parameters.

That's where **Directional Stimulus Prompting (DSP)** comes in — a framework that generates targeted hints to steer a language model toward the desired output.