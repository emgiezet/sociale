---
day: 41
title: "RAPTOR: Hierarchical Retrieval for Documents That Flat Chunking Can't Handle"
pillar: Educator
language: en
image: ../../images/day-41.jpg
image_unsplash_query: "tree hierarchy architecture document structure layers"
---

# RAPTOR: Hierarchical Retrieval for Documents That Flat Chunking Can't Handle

Every chunking strategy I described on day 38 has the same fundamental limitation: it produces a flat list of equally-weighted chunks. The retriever has no concept of what's general versus specific, no awareness that three chunks from three different sections might collectively answer a question that none of them can answer individually.

This is a real problem for complex documents — insurance policies, legal contracts, regulatory texts — where meaning is distributed across sections and where cross-references between parts are load-bearing.

RAPTOR was designed to solve exactly this. Let me show you how it works, when it helps, and how we implemented it.

## The Flat Chunking Problem in Practice

Here's a concrete example. A user asks: "How does the force majeure clause affect claims procedures and liability exclusions?"

This question requires information from at least three sections of a typical insurance policy:
1. **Definitions section:** What constitutes force majeure under this policy?
2. **Scope of coverage / exclusions:** What liability is excluded in force majeure events?
3. **Claims procedures:** What must the policyholder do when reporting a force majeure claim?

With flat chunking, the retriever will return the 5 chunks most similar to the query embedding. In practice, this typically returns 1-2 of the 3 required sections — the others might not score high enough in similarity because they don't individually mention "force majeure" in the context of the specific sub-question being asked.

The LLM then answers from incomplete context. In our testing, on queries requiring multi-section synthesis, flat chunking resulted in complete, accurate answers only about 45% of the time. The model either gave partial answers or hallucinated connections between sections it hadn't seen.

RAPTOR addresses this through a tree structure that makes different levels of abstraction available to the retriever.

## How RAPTOR Works

RAPTOR — Recursive Abstractive Processing for Tree-Organized Retrieval — was proposed by Sarthi et al. in 2024. The architecture has three phases: tree construction, multi-level indexing, and retrieval.

### Phase 1: Tree Construction

**Step 1: Leaf node chunking**
Start with the standard chunking approaches from day 38. These leaf chunks (typically 256–512 tokens) form the bottom of the tree.

**Step 2: Embedding**
Embed all leaf chunks using your embedding model.

**Step 3: Clustering**
Cluster the embedded chunks into semantically related groups. The original RAPTOR paper uses Gaussian Mixture Models (GMM) with soft assignment — each chunk can belong to multiple clusters with different probabilities. This is important because a definition chunk might be relevant to multiple sections.

The number of clusters is typically set proportional to the square root of the number of chunks (heuristic: `n_clusters = max(1, int(sqrt(n_chunks) / 2))`).

**Step 4: Summarization**
For each cluster, use an LLM to generate a summary of all the chunks in the cluster. This summary is a new node at a higher level of the tree.

**Step 5: Recurse**
Embed the summaries, cluster them, summarize the clusters again. Repeat until you have a single root node — a summary of the entire document.

For a 50-page insurance policy with ~200 leaf chunks, you might end up with:
- Level 0 (leaves): 200 chunks
- Level 1 (section summaries): ~15 summaries
- Level 2 (part summaries): ~5 summaries
- Level 3 (root): 1 full-document summary

### Phase 2: Multi-Level Indexing

All nodes at all levels go into the vector store. You're not choosing between levels — you're indexing everything.

Each node gets metadata indicating its tree level, its parent node(s), and its child nodes. This lets you navigate the hierarchy after retrieval.

### Phase 3: Retrieval

**Collapsed tree retrieval** (simpler): Search across all nodes at all levels simultaneously. Let the similarity scores determine which level is retrieved. For a broad conceptual question, the high-level summaries tend to win. For a specific factual question, the leaf chunks tend to win.

**Tree traversal** (more controlled): Start at the root. At each level, retrieve the top-k nodes and descend into their children for more detail. Stop when you've reached the required depth or when similarity scores start dropping.

For our insurance document use case, collapsed tree retrieval worked better in practice — it was simpler, produced consistent results, and the hierarchical index naturally surfaced the right abstraction level for different query types.

## Python Implementation

Here's the core RAPTOR implementation we use:

```python
from anthropic import Anthropic
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import normalize
import json

client = Anthropic()

def summarize_cluster(chunks: list[str], level: int) -> str:
    """Use LLM to summarize a cluster of document chunks."""
    combined_text = "\n\n---\n\n".join(chunks)
    
    level_instruction = {
        1: "These are related sections from an insurance policy document.",
        2: "These are summaries of related sections from an insurance policy.",
        3: "These are high-level summaries. Create an executive summary.",
    }.get(level, "These are document sections.")
    
    prompt = f"""{level_instruction}

Create a concise summary (150-250 words) that captures the key points, 
any cross-references between sections, and the main rules or conditions described.
Focus on information that would help answer user questions about the document.

Document sections:
{combined_text}

Summary:"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def build_raptor_tree(
    chunks: list[str],
    embeddings: list[list[float]],
    max_levels: int = 3,
    min_cluster_size: int = 3
) -> list[dict]:
    """
    Build the RAPTOR tree structure.
    Returns all nodes (leaves + summaries) at all levels.
    """
    all_nodes = []
    
    # Level 0: leaf chunks
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        all_nodes.append({
            "id": f"L0-{i}",
            "level": 0,
            "text": chunk,
            "embedding": emb,
            "children": [],
            "parent": None
        })
    
    current_level_nodes = all_nodes.copy()
    
    for level in range(1, max_levels + 1):
        if len(current_level_nodes) < min_cluster_size:
            break
        
        # Get embeddings for current level
        level_embeddings = np.array([n["embedding"] for n in current_level_nodes])
        level_embeddings_normalized = normalize(level_embeddings)
        
        # Determine number of clusters
        n_clusters = max(1, int(np.sqrt(len(current_level_nodes)) / 2))
        
        if n_clusters == 1:
            # Create single root summary
            cluster_texts = [n["text"] for n in current_level_nodes]
            summary = summarize_cluster(cluster_texts, level)
            # (embed summary and add to all_nodes...)
            break
        
        # Fit GMM
        gmm = GaussianMixture(n_components=n_clusters, random_state=42)
        gmm.fit(level_embeddings_normalized)
        
        # Soft assignment: each node can belong to multiple clusters
        probs = gmm.predict_proba(level_embeddings_normalized)
        threshold = 0.1  # node belongs to cluster if probability > threshold
        
        new_level_nodes = []
        
        for cluster_idx in range(n_clusters):
            # Get nodes in this cluster
            cluster_node_indices = [
                i for i, p in enumerate(probs[:, cluster_idx]) 
                if p > threshold
            ]
            
            if len(cluster_node_indices) < 2:
                continue
            
            cluster_nodes = [current_level_nodes[i] for i in cluster_node_indices]
            cluster_texts = [n["text"] for n in cluster_nodes]
            
            # Generate summary
            summary_text = summarize_cluster(cluster_texts, level)
            
            # Embed the summary (use your embed_text function from day 40)
            summary_embedding = embed_text(summary_text)
            
            # Create summary node
            summary_node = {
                "id": f"L{level}-{cluster_idx}",
                "level": level,
                "text": summary_text,
                "embedding": summary_embedding,
                "children": [n["id"] for n in cluster_nodes],
                "parent": None
            }
            
            # Update children's parent reference
            for n in cluster_nodes:
                n["parent"] = summary_node["id"]
            
            all_nodes.append(summary_node)
            new_level_nodes.append(summary_node)
        
        current_level_nodes = new_level_nodes
    
    return all_nodes

def raptor_retrieve(query: str, all_nodes: list[dict], top_k: int = 5) -> list[dict]:
    """
    Collapsed tree retrieval: search all nodes at all levels simultaneously.
    """
    query_embedding = np.array(embed_text(query))
    
    # Calculate similarity scores for all nodes
    scored_nodes = []
    for node in all_nodes:
        node_emb = np.array(node["embedding"])
        # Cosine similarity
        similarity = np.dot(query_embedding, node_emb) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(node_emb) + 1e-10
        )
        scored_nodes.append((similarity, node))
    
    # Sort by similarity and return top-k
    scored_nodes.sort(key=lambda x: x[0], reverse=True)
    return [node for _, node in scored_nodes[:top_k]]
```

**Usage:**

```python
# Build the tree (done once at indexing time)
leaf_chunks = [...]  # your chunks from day 38
leaf_embeddings = [embed_text(chunk) for chunk in leaf_chunks]

raptor_nodes = build_raptor_tree(leaf_chunks, leaf_embeddings)

# At query time
query = "How does force majeure affect claims procedures and liability exclusions?"
results = raptor_retrieve(query, raptor_nodes, top_k=5)

# The results may include a mix of leaf chunks and summaries
for node in results:
    print(f"Level {node['level']}: {node['text'][:100]}...")
```

## Architecture Diagram (Text Representation)

```
                     [Document Root Summary]
                           Level 3
                    /           |           \
        [Part A Summary]  [Part B Summary]  [Part C Summary]
                           Level 2
           /    \              |           /      \
   [Sec 1.1] [Sec 1.2]   [Sec 2.1]  [Sec 3.1] [Sec 3.2]
                           Level 1
    /  |  \   / | \        / | \      / | \    / | \
   C1  C2 C3 C4 C5 C6    C7 C8 C9  C10 C11 C12 ...
                           Level 0 (Leaf Chunks)
```

When a user asks a multi-section synthesis question, the retriever returns Level 2 or 3 nodes. When asking a specific factual question, it returns Level 0 nodes. The collapsed tree search handles this automatically through similarity scoring.

## Real Insly Example: Force Majeure Query

**Query:** "How does the force majeure clause affect claims procedures and liability exclusions?"

**Flat chunking result (top 5):**
- Chunk from §7.3: force majeure definition (leaf, 280 tokens)
- Chunk from §7.1: general exclusion list header (leaf, 220 tokens)  
- Chunk from §7.4: weather event exclusions (leaf, 310 tokens)
- Chunk from §1.1: general introduction (leaf, 180 tokens) — false positive
- Chunk from §12.2: claims form submission deadline (leaf, 195 tokens) — partially relevant

Result: the model got the definition and some exclusions, but missed the claims procedure interaction entirely. Incomplete answer.

**RAPTOR result (top 5):**
- Level 2 summary: "Part II — Exclusions and Force Majeure" (covers §§7-9, all exclusion scenarios and their interaction with claims)
- Level 0 chunk from §7.3: force majeure definition
- Level 0 chunk from §13.4: force majeure-specific claims procedure
- Level 1 summary: "Section 7 — Liability Exclusions" (broader exclusion context)
- Level 0 chunk from §7.5: documentation requirements for excluded events

Result: the model had both the specific clauses and the synthesized context. Complete, accurate answer with cross-references to the relevant paragraphs.

**Recall@5 improvement:** on multi-section synthesis questions in our test set, RAPTOR improved recall from 0.51 (flat chunking) to 0.82. That's a 31-point improvement specifically for complex, context-dependent questions.

On simple factual questions, RAPTOR performed equivalently to flat chunking — the extra tree levels didn't hurt retrieval of specific facts.

## Trade-Offs: When RAPTOR Is Worth It

**RAPTOR makes sense when:**
- Documents are long (20+ pages) with interconnected sections
- Users frequently ask questions that require synthesizing multiple sections
- Document structure has meaningful hierarchy (parts, sections, subsections)
- You have budget for longer indexing time (significant LLM calls during tree construction)

**RAPTOR is overkill when:**
- Documents are short or have simple, self-contained sections
- Use case is primarily simple factual lookup (FAQ style)
- Index must rebuild frequently (RAPTOR indexing is expensive)
- Budget is tight — summarizing a 200-chunk document requires ~50-100 LLM calls just for tree construction

**The indexing cost for a 200-chunk document:**
- Level 1 summaries (~15 clusters × ~200 tokens each): ~3,000 tokens output, ~10,000 tokens input ≈ $0.18
- Level 2 summaries (~5 clusters × ~200 tokens each): ~1,000 tokens output, ~3,500 tokens input ≈ $0.06
- Level 3 root: ~200 tokens output, ~1,000 tokens input ≈ $0.02

**Total tree construction cost: ~$0.26 per document**

For a corpus of 10,000 policy documents, building the full RAPTOR tree costs approximately $2,600 — once. Rebuilding on chunking strategy changes is the expensive part, which is why getting your chunking right (day 38) before adding RAPTOR matters.

## Connecting It All: The Full RAG Stack

After five days of the RAG Deep Dive and the start of RAG Masterclass:

- **Day 37:** Choose models based on your data, not benchmarks
- **Day 38:** Invest in data preparation — it's 60% of the work
- **Day 39:** Model your costs before committing to an architecture
- **Day 40 (HyDE):** Bridge the semantic gap between user language and document language
- **Day 41 (RAPTOR):** Build hierarchy for documents that require multi-section synthesis

A mature RAG pipeline for complex documents like insurance policies layers these techniques: parent-child chunking (day 38) at the leaf level, RAPTOR hierarchy above it, HyDE at query time, with reranking on the final candidate set. The result is a retrieval system that can handle both specific factual queries and complex synthesis questions reliably.

The techniques aren't mutually exclusive. They compose.

---

*Day 41 of the RAG Masterclass series. Next: evaluation — how to measure whether your RAG improvements are actually improvements.*
