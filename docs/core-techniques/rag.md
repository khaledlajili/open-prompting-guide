---
sidebar_position: 8
---

# Retrieval-Augmented Generation (RAG)

Language models are powerful, but their knowledge is limited to what they learned during training. When a question requires up-to-date, specialized, or highly specific information, the model can guess — and sometimes invent facts.

How can you give a language model direct access to dynamic, external knowledge sources without retraining the entire model?

That's the idea behind **Retrieval-Augmented Generation (RAG)** — an approach that combines information retrieval with language generation to produce answers grounded in external knowledge.

---

## 1. What Is Retrieval-Augmented Generation?

**Retrieval-Augmented Generation (RAG)** is an approach that combines a retrieval system with a language model to generate responses using relevant information from an external knowledge source.

Instead of relying only on what it memorized during training, the model receives additional information retrieved from sources such as documents, databases, or knowledge bases.

A typical RAG system follows three main steps:

1. **Retrieve** — Find information relevant to the user's question from an external knowledge source.
2. **Augment** — Add the retrieved information to the original prompt as additional context.
3. **Generate** — Ask the language model to produce an answer using the provided context.

---

## 2. How the RAG Pipeline Works

A standard RAG architecture operates in three core phases:

### Phase 1: Indexing (Offline Preparation)

Before any questions are asked, your data source needs to be prepared:
1. **Chunking:** Large documents are split into smaller, manageable text segments (e.g., paragraphs or sentences).   
2. **Embedding:** An embedding model converts each text chunk into a vector (numerical representation of semantic meaning).   
3. **Storage:** The vectors are stored in a vector database (such as FAISS, Pinecone, or Chroma) for fast similarity search.   

### Phase 2: Retrieval (At Query Time)

When a user asks a question:   

1. The system converts the user's query into an embedding vector.   
2. It compares the query vector against the vector database.   
3. It retrieves the top most relevant text chunks (supporting documents).

### Phase 3: Generation (Contextual Fusion)

1. The retrieved text chunks are formatted and concatenated with the original user query inside a structured prompt template.
2. The combined prompt is sent to the LLM.   
3. The LLM generates a grounded response based only on the provided context.

---

## 3. RAG vs. Fine-Tuning: When to Use Which?

Developers often wonder whether they should fine-tune a model or build a RAG pipeline. They serve entirely different purposes:

| Feature | Fine-Tuning | Retrieval-Augmented Generation (RAG)                                 |
|--|--|----------------------------------------------------------------------|
|Primary Goal|Teaches the model how to speak (style, tone, format, domain syntax).| Teaches the model facts (supplies external, up-to-date information). |
|Data Updates|Difficult and expensive (requires retraining model weights).| Instant and cheap (just add/update documents in the database).       |
|Hallucination Risk|Still prone to hallucinations if asked about unseen facts.| Significantly reduced because answers are grounded in retrieved text. |
|Traceability|Hard to trace where an answer came from.| High traceability (you can cite the exact source document/chunk).    |

:::tip The Sweet Spot
In modern AI architectures, you often combine both: fine-tune an open-source model to follow a precise company persona or format, and use RAG to feed it real-time factual data.
:::

--- 

## 5. RAG vs. Generated Knowledge Prompting

You've already learned Generated Knowledge Prompting, which also gives a model additional information before it answers.

The two approaches may seem similar, but they obtain that information in different ways.

**Generated Knowledge Prompting** asks the model to generate relevant information from what it knows.

**Retrieval-Augmented Generation** retrieves relevant information from an external knowledge source.

---

## 6. When to Use RAG

|Situation| Why RAG helps                                   |
|--|-------------------------------------------------|
|Questions that need up-to-date facts| External knowledge can be refreshed easily      |
|Domain-specific or specialized topics| You can connect the model to your own documents |
|High need for factual accuracy| Retrieved evidence reduces unsupported claims   |
|Applications where knowledge changes| Avoids expensive full-model retraining          |

RAG is less necessary for pure reasoning tasks, creative writing, or questions the model already answers reliably from its training data.

---

## 7. Try It Yourself

**Task:** Design a RAG-infused prompt structure that forces an LLM to answer a question using only the retrieved context provided.

**User Query:** 
```text
What is our company's remote work policy regarding international travel?
```

**Retrieved Document Chunk:**
```text
Employees are permitted to work remotely from any location within their home country for up to 90 days per calendar year. International remote work is strictly restricted due to tax and compliance regulations, requiring explicit VP approval at least 30 days in advance.
```

Create a prompt template that takes the retrieved document chunk and the query, and ensures the model does not hallucinate rules outside of the text.

<details>
<summary><strong>Example Answer</strong></summary>

<div>

**RAG prompt:**

```text
You are a helpful HR assistant. Answer the user's question using ONLY the provided context below. If the answer cannot be found entirely within the context, state "I cannot answer this based on current company policies." Do not assume or extrapolate.

Context:
"Employees are permitted to work remotely from any location within their home country for up to 90 days per calendar year. International remote work is strictly restricted due to tax and compliance regulations, requiring explicit VP approval at least 30 days in advance."

User Query: 
"What is our company's remote work policy regarding international travel?"

Answer:
```

**Expected model response:**

> International remote work is strictly restricted due to tax and compliance regulations. It requires explicit VP approval at least 30 days in advance.

</div>
</details>

---
## What's Next

You've now learned how to connect a language model to external knowledge sources through Retrieval-Augmented Generation.

The key is to **retrieve relevant information, provide it as context, and use it to generate a grounded answer**.

But retrieving information is only one way to extend what a model can do. Some tasks also require calculations, database queries, or other tool executions as part of the solution.

That's where **Automatic Reasoning and Tool-use (ART)** comes in — a framework that combines multi-step reasoning with external tools to solve tasks more systematically.