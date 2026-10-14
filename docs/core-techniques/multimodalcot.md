---
sidebar_position: 16
---

# Multimodal Chain-of-Thought Prompting

You’ve learned how to guide models using text-based Chain-of-Thought (CoT) reasoning, ReAct loops, and verbal reflection.

What happens when a question requires a model to interpret an image, read a scientific chart, solve a geometry diagram, or analyze a visual artifact alongside text? If you strip away the visual context, text-only reasoning collapses.

How can we bridge the gap between visual perception and language reasoning in prompts?

This is the core idea behind **Multimodal Chain-of-Thought Prompting**.

---

## 1. What Is Multimodal CoT

**Multimodal CoT** is a prompting and modeling approach that incorporates both language and visual inputs into the reasoning process.

Instead of generating an answer directly from mixed text and image inputs, it separates the work into two stages:

1. **Rationale Generation** — The model produces a step-by-step explanation using both the text and the visual information.
2. **Answer Inference** — The model uses the generated rationale (along with the original inputs) to produce the final answer.

This separation helps the model build a clearer intermediate representation before committing to an answer.

---

## 2. How Multimodal CoT Works

### Step 1: Process Textual and Visual Information

The model receives the question together with the relevant image.

For example:

**Question:**

A 2 kg object rests on a frictionless incline. Using the angle shown in the diagram, calculate the component of gravitational force acting parallel to the incline.

**Image:**

A diagram showing a block on a frictionless inclined plane. The angle between the plane and the horizontal is 30°.

To solve the problem, the model needs to use information from both sources:

- The text provides the object's mass and describes the required calculation.
- The diagram provides the incline angle.

Neither the text nor the visual information necessarily provides everything needed by itself.

### Step 2: Generate a Rationale

An illustrative rationale might be:

```text
The diagram shows an incline angle of 30 degrees.

The object has a mass of 2 kg, and gravitational acceleration
is approximately 9.8 m/s².

The gravitational force has magnitude:

F = mg = 2 × 9.8 = 19.6 N.

The component of gravity parallel to the incline is:

F_parallel = mg × sin(θ).

Using θ = 30 degrees:

F_parallel = 19.6 × sin(30°)
           = 19.6 × 0.5
           = 9.8 N.
```

The rationale connects visual observations with information from the question and the relevant physical relationship.

### Step 3: Perform Answer Inference

Conceptually, the second stage receives:

- The original question.
- The original image.
- The rationale generated during the first stage.

The model uses these together to determine the requested result.

### Step 4: Return the Final Answer

The final response should communicate the result clearly and include an appropriate explanation when useful.

---

## 4. Try It Yourself

Suppose you have an image of a simple circuit diagram and the following question:

```text
In the circuit shown, if the switch is closed, will the light bulb turn on? 
Explain your reasoning.
```

**Task:** Write a two-stage Multimodal CoT-style prompt that first asks for a rationale and then asks for the final answer.

<details>
<summary><strong>Example Answer</strong></summary>

**Stage 1 – Rationale Generation:**
```text
Look at the circuit diagram and the question. 
Generate a step-by-step explanation of how the circuit works and what happens when the switch is closed. 
Use both the visual information and the question.
```

**Stage 2 – Answer Inference:**
```text
Using the circuit diagram, the question, and the rationale below, 
give a clear final answer (Yes or No) and a short confirmation of your reasoning.

Rationale:
[insert generated rationale here]
```
</details>

---

## What’s Next

Multimodal CoT shows how chain-of-thought reasoning can be extended beyond text to include visual information.

You now have techniques that cover text-based reasoning, tool use, retrieval, program generation, self-improvement, and multimodal reasoning.

In practice, match the method to the input: use standard CoT for text-only problems, and multimodal approaches when images or diagrams are essential to solving the task.