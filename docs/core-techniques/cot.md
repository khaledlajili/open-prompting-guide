---
sidebar_position: 2
---

# Chain-of-Thought Prompting

You've seen how examples can shape what a model says.  
But what if your task is about thinking?

Imagine you ask the model:
```
A train leaves City A at 8 AM traveling 60 km/h.
Another leaves City B at 9 AM traveling 80 km/h toward City A.
The cities are 300 km apart. When do they meet? Give the result directly.
```

The model might instantly answer:
> They meet at 11:30 AM.

Confident — but wrong. It skipped the math.

If instead you prompt:
```
A train leaves City A at 8 AM traveling 60 km/h.
Another leaves City B at 9 AM traveling 80 km/h toward City A.
The cities are 300 km apart. When do they meet? Let's think step by step.
```

The model starts to reason:

> 1. The first train travels 60 km in the first hour.<br />
> 2. At 9 AM, 240 km remain between them.<br />
> 3. Their combined speed is 140 km/h → 240 / 140 ≈ 1.71 hours.<br />
> 4. 1 h 43 min after 9 AM → 10:43 AM.

This time, it's correct — because you asked it to think out loud.

Sometimes, clarity and examples aren't enough — you need the model to show its reasoning before answering, turning opaque guesses into transparent, verifiable steps.

That's where **Chain-of-Thought** comes in.

---

## 1. What Is Chain-of-Thought Prompting

**Chain-of-Thought (CoT) prompting** means asking a model to break down its reasoning into **intermediate steps** before giving a final answer.

Instead of jumping straight to a conclusion, the model:
1. Shows each step of its thinking
2. Explains how one step leads to the next
3. Arrives at an answer through visible logic

Think of it like showing your work in math class — the teacher wants to see *how* you got the answer, not just the answer itself.

**Why does this matter?**

Language models predict what comes next based on patterns, but they don't actually "understand" logic the way humans do. When you ask them to think step-by-step, you force them to follow a more structured reasoning process — which often leads to more accurate answers, transparent reasoning you can verify, and logic you can check at each step.

:::tip Key insight
CoT prompting doesn't make the model smarter — it changes *how* the model generates its answer, encouraging a more methodical approach that reduces errors.
:::

---

## 2. CoT Prompting Techniques

There are three main ways to implement Chain-of-Thought prompting, each with different levels of control and guidance.

### Zero-Shot CoT: "Let's think step by step"

**Zero-shot CoT** means asking the model to reason step-by-step **without giving it any examples**.

All you do is add a simple phrase like "Let's think step by step," "Break this down into steps," or "Explain your reasoning."

**Example:**
```
Question: If a bakery makes 48 cupcakes and packages them in boxes of 6, 
how many boxes can they fill?
Let's think step by step.
```

**Model's response:**

> Step 1: We have 48 cupcakes total.<br />
> Step 2: Each box holds 6 cupcakes.<br />
> Step 3: To find the number of boxes, divide: 48 ÷ 6 = 8.<br />
> **Answer:** They can fill 8 boxes.

The model decides *how* to break down the reasoning on its own.

---

### Few-Shot CoT: Teaching by Example

**Few-shot CoT** means showing the model **examples of step-by-step reasoning** before asking it to solve a new problem.

You provide two to five demonstrations that include both the reasoning steps *and* the final answer.

**Example:**
```
Q: A store has 15 apples. They sell 7 and buy 12 more. How many apples do they have?
A: Start with 15 apples. Sell 7: 15 - 7 = 8. Buy 12 more: 8 + 12 = 20.
Answer: 20 apples.

Q: A library has 32 books. They donate 8 and receive 15 more. How many books do they have?
A: Start with 32 books. Donate 8: 32 - 8 = 24. Receive 15 more: 24 + 15 = 39.
Answer: 39 books.

Now solve this:
Q: A classroom has 20 pencils. Students use 9 and the teacher adds 6 more. 
How many pencils are there?
```

**Model's response:**

> A: Start with 20 pencils. Students use 9: 20 - 9 = 11. Teacher adds 6: 11 + 6 = 17.<br />
> **Answer:** 17 pencils.


The model learns your reasoning *style* and *structure* from the examples and applies it to the new problem.

**Tips for good Few-Shot CoT examples:**
- Use two to five diverse examples (not too similar to each other)
- Show clear, logical steps in each example
- Keep the reasoning concise but complete
- Make sure your examples actually lead to the correct answer

---

### Guided CoT: Providing a Reasoning Framework

**Guided CoT** means explicitly telling the model **what steps to follow** when reasoning through a problem.

You provide an outline or template of the reasoning process:

**Example:**
```
Question: A rectangular garden is 12 meters long and 8 meters wide. What is its area?

Use this reasoning structure:
1. List what we know
2. Determine the formula needed
3. Perform the calculation
4. State the final answer
```

**Model's response:**

> 1. What we know: Length = 12 meters, Width = 8 meters<br />
> 2. Formula needed: Area of rectangle = Length × Width<br />
> 3. Calculation: 12 × 8 = 96<br />
> 4. **Final answer:** The garden's area is 96 square meters.


This technique gives you **maximum control** over how the model structures its reasoning — useful when you need a consistent approach across many similar problems or want to enforce a specific methodology (like a scientific method, troubleshooting checklist, or decision framework).

---

### When to Use Each Technique

| Technique         | Best For                                                                   |
|-------------------|----------------------------------------------------------------------------|
| **Zero-Shot CoT** | Quick reasoning tasks, initial testing, straightforward problems           |
| **Few-Shot CoT**  | Tasks needing specific style or format, consistent outputs, complex reasoning |
| **Guided CoT**    | Standardized processes, compliance needs, enforcing methodology            |

:::info Start simple, add control as needed
Start with **Zero-Shot CoT** to see if simple reasoning helps. If you need more control or consistency, move to **Few-Shot CoT**. Use **Guided CoT** when you must enforce a specific reasoning process or need reproducible, auditable steps.
:::

---

## 3. When Chain-of-Thought Works Best

### Tasks Where CoT Helps Most

**Math Problems**  
Questions that involve arithmetic or formulas. Writing out the steps prevents calculation mistakes.
```
A pair of shoes costs $60. There's a 25% discount. What's the final price?
```

**Word Problems**  
Real-world stories that hide a math or logic question. Step-by-step reasoning helps extract the numbers and operations correctly.
```
Emma has 10 apples, gives away 3, then buys 5 more. How many apples now?
```

**Logic & Deduction**  
Situations that require applying rules carefully. CoT ensures the model checks every condition before concluding.
```
If all cats are mammals and some mammals are pets, are all cats pets?
```

**Multi-Step Decisions**  
Choosing between options using several criteria. Listing pros, cons, and trade-offs makes reasoning transparent.
```
Laptop A is cheaper but heavier. Laptop B is lighter but costs more. 
Which should I buy for travel?
```

**Planning Tasks**  
Creating or organizing a sequence of actions. CoT turns vague goals into clear, ordered steps.
```
Plan a weekend trip: choose location → book stay → plan meals → pack essentials.
```

**Cause-and-Effect Reasoning**  
Understanding what happens when something changes. Describing the chain of causes improves logical flow.
```
If it rains tomorrow, what might happen to the outdoor concert?
```

---

### Tasks Where CoT Usually Doesn't Help

**Simple factual recall** — The model just needs to remember a fact, like "What's the capital of France?"

**Creative writing** — Step-by-step logic can make stories or poems sound mechanical, like "Write a poem about space exploration."

**Definition or lookup tasks** — There's no reasoning, just providing a known answer, like "What does 'photosynthesis' mean?"

---

## 4. Try It Yourself

### Task 1: Few-Shot CoT

You want the model to classify customer reviews as Positive or Negative, and explain why in one sentence.

Create a few-shot prompt with two examples, then ask it to classify this new review:
```
The delivery was fast but the product quality disappointed me.
```

Your prompt should teach the model to:
- State the classification clearly
- Explain the reasoning in one sentence
- Consider both positive and negative aspects

---

### Task 2: Guided CoT

You need the model to help calculate how much paint someone needs to buy for their room.

The problem is:
```
My bedroom is 4 meters long and 3 meters wide, with walls that are 2.5 meters tall. 
One paint can covers 10 square meters. How many cans do I need?
```

Create a guided prompt that gives the model a clear step-by-step structure to follow when solving this paint calculation problem. Think about what steps are needed to go from room dimensions to number of paint cans.

<details>
<summary><strong>Example Answers</strong></summary>

<div>

**Task 1: Few-Shot CoT**
```
Review: "Great features but the app crashes frequently."
Classification: Negative
Reasoning: Despite acknowledging good features, the frequent crashes are a critical 
usability issue that outweighs the positives.

Review: "Exactly what I needed, works perfectly!"
Classification: Positive
Reasoning: Completely satisfied with both functionality and performance, with no 
mentioned drawbacks.

Now classify this:
Review: "The delivery was fast but the product quality disappointed me."
```

**Expected model response:**

> Classification: Negative<br />
> Reasoning: While fast delivery is positive, the disappointment with product quality is the primary concern and determines overall satisfaction.


---

**Task 2: Guided CoT**
```
Problem: "My bedroom is 4 meters long and 3 meters wide, with walls that are 2.5 meters 
tall. One paint can covers 10 square meters. How many cans do I need?"

Solve this step by step:
1. Calculate the wall area (perimeter × height)
2. Divide by coverage per can
3. Round up to whole cans needed
```

**Expected model response:**

> 1. Wall area: Perimeter = 2(4 + 3) = 14 meters. Area = 14 × 2.5 = 35 square meters.<br />
> 2. Cans needed: 35 ÷ 10 = 3.5 cans.<br />
> 3. Round up: You need 4 cans (since you can't buy partial cans).


</div>
</details>

---

## What's Next

You've now learned how to guide a model through step-by-step reasoning using examples or structured frameworks.

But sometimes, instead of showing the model specific examples or reasoning steps, you can describe the underlying structure of the task itself.

That's where **Meta Prompting** comes in — a technique that focuses on abstract patterns and reusable structures to guide the model's responses.