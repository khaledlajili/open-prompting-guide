---
sidebar_position: 5
---

# Generated Knowledge Prompting

You’ve learned how to guide reasoning step-by-step and sample multiple pathways for accuracy. But what happens when a model fails simply because it makes a wrong factual assumption?

Imagine you ask:

```text
Part of golf is trying to get a higher point total than others. Yes or No?
```

The model might confidently answer:

> Yes.

But that's incorrect. In golf, players generally aim to complete the course using the fewest strokes. The player with the lowest total score wins.

The problem is that the model didn't use the relevant knowledge needed to answer the question correctly.

What if, instead of asking for an answer immediately, you first asked the model to generate relevant knowledge about the topic?

That's the idea behind **Generated Knowledge Prompting**.

---

## 1. What Is Generated Knowledge Prompting

**Generated Knowledge Prompting** is a technique that asks a language model to generate relevant information about a topic before using that information to answer.

Instead of answering immediately, the process splits the task into two stages:

1. **Knowledge Generation** — Prompt the model to produce relevant facts, rules, or background information about the topic.
2. **Knowledge Integration** — Combine the original question with the newly generated knowledge to produce the final answer.

---

## 2. How Generated Knowledge Prompting Works

### Step 1: Generate Knowledge

Provide a few examples showing how to generate helpful background context for various statements, followed by your target query.

**Prompt:**

```text
Input: Greece is larger than Mexico.
Knowledge: Greece is approximately 131,957 sq km, while Mexico is approximately 1,964,375 sq km, making Mexico much larger than Greece.

Input: Part of golf is trying to get a higher point total than others.
Knowledge:
```

**Model's Generated Knowledge:**

> The objective of golf is to complete a set of holes in the fewest number of strokes. Each stroke counts as a point/score, and the player with the lowest total score wins the game.

### Step 2: Integrate Knowledge & Answer

Now, feed the generated knowledge back to the model along with the original question.

**Prompt:**

```text
Question: Part of golf is trying to get a higher point total than others. Yes or No?

Knowledge: The objective of golf is to complete a set of holes in the fewest number of strokes. Each stroke counts as a point/score, and the player with the lowest total score wins the game.

Explain and Answer:
```

**Model response:**

> No. The objective of golf is not to get a higher point total than others. The goal is to complete the course in the fewest strokes possible, so the player with the lowest score wins.

---

## 3. When to Use Generated Knowledge Prompting

Generated Knowledge Prompting is most useful when the answer depends on information that the model needs to identify and consider explicitly.

### Tasks Where It Can Help

| Situation                                                                                                              | Why it helps  |
|------------------------------------------------------------------------------------------------------------------------|---------------|
| Commonsense reasoning                                                                                                  | Supplies missing real-world facts |
| Questions that rely on specific knowledge | Reduces reliance on the model’s internal (and sometimes flawed) knowledge    |
| Tasks where the model often makes confident but wrong assumptions | Gives it a chance to correct itself before answering |

### When It May Be Less Effective

Generated Knowledge Prompting may be less useful when:

- The task is simple and the answer is already obvious.
- The model generates incorrect or misleading information.
- The question requires recent or specialized facts that the model does not reliably know.
- The generated information is too broad or unrelated to the question.

In these situations, generating more information can introduce additional errors rather than improve the answer.

:::warning More knowledge does not always mean a better answer
The model may generate plausible-sounding information that is incorrect. If the final answer depends on that information, the mistake can carry through to the conclusion.
:::

---

## 4. Try It Yourself

**Task:** Create a knowledge-generation prompt, then use the generated knowledge to answer this question:

```text
A bat is a kind of bird. True or False?
```

<details>
<summary><strong>Example Answer</strong></summary>

<div>

**Step 1: Generate Knowledge**

```text
Input: A whale is a fish.
Knowledge: Whales are mammals. They breathe air, give live birth, and nurse their young.

Input: A tomato is a vegetable.
Knowledge: Botanically, a tomato is a fruit because it develops from the flower of the plant and contains seeds.

Input: A bat is a kind of bird.
Knowledge:
```

**Possible model response:**

> Bats are mammals, not birds. They have fur, give live birth, and produce milk for their young. Birds have feathers and lay eggs.

---

**Step 2 – Final prompt:**

```text
Question: A bat is a kind of bird. True or False?

Knowledge: Bats are mammals, not birds. They have fur, give live birth, and produce milk for their young. Birds have feathers and lay eggs.

Explain and Answer:
```

**Expected model response:**

> False

</div>
</details>

---

## What's Next

You've now learned how to improve a model's answers by generating relevant knowledge before asking it to solve a problem.

The key is to **generate useful information first, then use it to guide the final answer**.

But remember: generated knowledge can be wrong, so important facts should always be checked before you rely on them.

You've now explored several ways to guide a model: clearer instructions, examples, structured reasoning, abstract frameworks, multiple attempts, and additional knowledge.

The next step is to practice combining these techniques and discover which approaches work best for different tasks.