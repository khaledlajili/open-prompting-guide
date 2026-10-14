---
sidebar_position: 7
---

# Tree of Thoughts (ToT)

You’ve seen how Chain-of-Thought guides a model step by step, and how Self-Consistency samples multiple paths and votes on the answer.

But some problems need more than a single linear path or a simple majority vote. They require exploration, evaluation of intermediate ideas, and the ability to backtrack when a direction looks unpromising.

That's the idea behind **Tree of Thoughts (ToT)** — a framework that allows a model to explore multiple intermediate solutions instead of following just one path from beginning to end.

---

## 1. What Is Tree of Thoughts?

**Tree of Thoughts (ToT)** is a problem-solving framework that extends Chain-of-Thought prompting by allowing a model to explore, evaluate, and develop multiple candidate solutions.

Instead of generating a single line of reasoning from start to finish, ToT enables the model to:

1. **Branch out:** Generate multiple alternative paths or candidate thoughts at each step.

2. **Self-evaluate:** Assess the progress of each branch (e.g., determining if a path is sure, maybe, or impossible).

3. **Look ahead & Backtrack:** Combine model evaluations with search algorithms (like Breadth-First Search or Depth-First Search) to abandon dead ends and return to promising branches.

:::info Beyond Linear Thought
If Chain-of-Thought is a single path through a maze, Tree of Thoughts is systematically exploring the maze by marking dead ends and retracing steps until you find the exit.
:::

---

## 2. How Tree of Thoughts Works

### Simple ToT-Style Prompt

A practical way to use the idea without building a full search system is the multi-expert prompt:

```text
Imagine three different experts are answering this question.
All experts will write down 1 step of their thinking, then share it with the group.
Then all experts will go on to the next step, etc.
If any expert realises they're wrong at any point then they leave.
The question is: [your question]
```

This encourages the model to explore alternative lines of thought and abandon weak ones.

### Full Framework

In the complete ToT approach:

- You define how many candidate thoughts to generate at each step
- The model evaluates each candidate
- A search algorithm (BFS, DFS, or beam search) decides which branches to expand
- The process continues until a solution is found or a budget is reached

This version is more powerful but requires additional code and multiple model calls.

---

## 4. Search Strategies for Tree of Thoughts

### Breadth-First Search (BFS)

**Breadth-first search** explores multiple candidates at the same depth before moving further into their individual branches.

This approach is useful when comparing alternatives at each stage is important.

### Depth-First Search (DFS)

**Depth-first search** follows one candidate through several steps before returning to explore another branch.

If a path fails, the search returns to an earlier decision and tries another route.

### Beam Search

**Beam search** keeps only a limited number of the most promising candidates at each stage.

For example, if the beam width is three, the search retains at most three candidates for further exploration at a given stage.

This reduces the number of branches that need to be explored.

| Strategy | How It Explores | Main Trade-off |
|---|---|---|
| **Breadth-First Search** | Explores several candidates at the same depth. | Can use substantial resources when many branches exist. |
| **Depth-First Search** | Follows one branch deeply before trying another. | Can spend too much time on an unproductive path. |
| **Beam Search** | Keeps a limited number of the most promising candidates. | May discard a path that eventually leads to the best solution. |

---

## 6. When Tree of Thoughts Works Best

Tree of Thoughts is particularly useful for problems where the next step depends on the choices made earlier.

### Tasks Where ToT Can Help

**Mathematical Puzzles**

Problems such as the Game of 24, where different combinations of operations need to be explored.

```text
Find an expression that uses the numbers 2, 3, 4, and 6
exactly once to obtain 24.
```

**Planning**

Tasks where several possible plans must be compared before selecting one.

```text
Create three possible approaches for completing a project
within two weeks. Evaluate their risks and feasibility,
then develop the strongest plan.
```

**Strategic Decisions**

Problems where an early decision affects the possibilities available later.

```text
Compare several strategies for launching a new product
with a limited budget. Evaluate the likely trade-offs
and develop the most promising approach.
```

**Complex Constraint Problems**

Tasks where a solution must satisfy several rules simultaneously.

```text
Create a weekly schedule for five employees while respecting
their availability, required working hours, and staffing needs.
Explore different schedules and check each against the constraints.
```

### When ToT May Be Less Effective

Tree of Thoughts is usually overkill for simple questions or tasks that a single Chain-of-Thought already handles well. It also costs more tokens and time because it generates and evaluates many intermediate steps.

---

## 7. Try It Yourself

**Task:** Solve the following mathematical puzzle using a Tree of Thoughts approach.

**Problem:**
Use the numbers 2, 3, 4, and 6 exactly once to obtain 24.
You may use addition, subtraction, multiplication, division, and parentheses.

<details>
<summary><strong>Example Answer</strong></summary>

<div>

```text
Solve the Game of 24 using the numbers 2, 3, 4, and 6.

Rules:
- Use each number exactly once.
- You may use +, -, *, /, and parentheses.

Apply a Tree of Thoughts approach:

1. Generate three possible first operations.
2. Evaluate their potential to reach 24.
3. Expand promising candidates into further operations.
4. Backtrack when a candidate cannot lead to a valid solution.
5. Verify the final expression.

Show the main branches briefly and explain why the
successful path works.
```

**Expected model response:**

> Let's explore three possible first operations:<br />
> 1. **Branch A:** (6 x 4 = 24). The target is reached, but 2 and 3 remain unused. Backtrack.<br />
> 2. **Branch B:** (6 x 3 = 18). Adding the remaining numbers gives (18 + 4 + 2 = 24). Success!<br />
> 3. **Branch C:** (4 x 3 = 12). Multiplying the remaining numbers gives (6 x 2 = 12), so (12 + 12 = 24). Success!<br />
> **Final solutions:** [6 x 3 + 4 + 2 = 24] and [4 x 3 + 6 x 2 = 24].

</div>
</details>

---
## What's Next

You've now learned how a model can explore multiple possible solutions, evaluate intermediate ideas, and backtrack when an approach fails.

Unlike a single chain of reasoning, **Tree of Thoughts** helps organize and evaluate alternative paths toward a solution.

But exploring different approaches isn't always enough. Sometimes, a model needs reliable information from external sources before it can produce a good answer.

That's where **Retrieval-Augmented Generation (RAG)** comes in — an approach that retrieves relevant information and provides it as context for generating an answer.