---
sidebar_position: 15
---

# Reflexion

You've learned how ReAct allows a language model to interleave reasoning and actions. However, when the model makes a mistake, it usually starts the next attempt from scratch.

What if we can add a self-improvement loop. After each attempt, the model reflects on what went wrong and stores that linguistic feedback in memory. On the next try, it uses this reflection to avoid repeating the same mistakes.

This is the idea behind **Reflexion**.

---

## 1. What Is Reflexion?

**Reflexion** is a framework that reinforces language-based agents through linguistic feedback (often called verbal reinforcement learning).

Instead of updating model weights via traditional scalar rewards, Reflexion converts environment feedback (success, failure, errors, or test results) into verbal self-reflection. This self-reflection is stored in the agent's memory and provided as context in subsequent trials, allowing the agent to rapidly and effectively learn from prior mistakes.

---

## 2. How Reflexion Works

Reflexion consists of three main components:

1. **Actor**  
   Generates actions and reasoning (often using CoT or ReAct). It produces a trajectory by interacting with the environment.

2. **Evaluator**  
   Scores the trajectory. The score can come from a rule-based heuristic, an LLM judge, or task-specific feedback.

3. **Self-Reflection**  
   Turns the evaluation and the trajectory into linguistic feedback. This reflection is stored in memory and used to guide the next attempt.

The typical cycle is:

1. Generate a trajectory (Actor)
2. Evaluate the result (Evaluator)
3. Produce a self-reflection
4. Store the reflection in memory
5. Generate a new trajectory that takes the reflection into account

Over multiple trials, the agent improves by learning from its own past mistakes in natural language form.

---

## 3. When to Use Reflexion

| Situation                              | Why Reflexion helps                                      |
|----------------------------------------|----------------------------------------------------------|
| Tasks that benefit from trial and error | The agent can improve across multiple attempts           |
| Fine-tuning is impractical             | Learning happens through memory, not weight updates      |
| Nuanced feedback is useful             | Verbal reflections are more specific than scalar rewards |
| Interpretability matters               | Reflections provide an explicit record of what the agent learned |

Reflexion has shown strong results on sequential decision-making (AlfWorld), multi-hop reasoning (HotPotQA), and code generation (HumanEval, MBPP).

---

## 4. Try It Yourself

Suppose an agent tried to answer a multi-hop question and failed because it searched for the wrong entity.

**Task:** Write a short self-reflection the agent could store in memory to improve on the next attempt.

<details>
<summary><strong>Example Answer</strong></summary>


```text
I failed because I searched for the wrong person. 
Next time I should first confirm the full name and role of the entity mentioned in the question before searching for related facts.
```

On the next trial, this reflection would be added to the prompt so the agent can avoid the same mistake.

</details>

---
## What's Next

You've now learned how **Reflexion** helps language-model agents improve across repeated attempts by evaluating their results, generating verbal feedback, and storing reflections in memory.

The key is to **turn experience into reusable feedback that can guide future attempts**.

So far, however, we've focused primarily on tasks where the essential information can be represented in text. What happens when solving a problem also requires interpreting an image, diagram, or other visual input?

That's where **Multimodal Chain-of-Thought Prompting** comes in — an approach that combines visual information and language-based reasoning to help models solve tasks involving multiple modalities.