# Week 3 Interview Questions: Embeddings & RAG

**Topic:** Working with Data, Embeddings, and Retrieval-Augmented Generation  
**Format:** Open-ended technical questions designed for real interviews  
**Difficulty:** Intermediate (assumes understanding of Sessions 3.1–3.6)

---

## Question 1: Embeddings Fundamentals

**The Question:**
"Explain what an embedding is and why they're useful for AI systems. Give a concrete example of how you'd use embeddings to solve a real-world problem."

**What a strong answer includes:**
- ✅ Definition: Embeddings convert text/data into numerical vectors that capture semantic meaning
- ✅ Why: Enable similarity comparisons, clustering, and semantic search (not just keyword matching)
- ✅ Concrete example: E.g., "I'd embed customer reviews, find similar ones, and cluster by theme" OR "embed search queries and documents to find relevant results"
- ✅ Mentions distance metrics: Cosine similarity to measure how "close" embeddings are
- ✅ Notes a limitation: All embeddings from the same model; can't directly compare embeddings from different models

**Red flags in weak answers:**
- "Embeddings are just random numbers"
- "They're only for images"
- No concrete example
- Confuses embeddings with training

**Follow-up if they nail it:**
"What happens if two very different concepts have similar embeddings? How would you debug that?"

---

## Question 2: Chunking Strategies in RAG

**The Question:**
"You're building a RAG system over a 500-page legal document. How would you chunk it, and what trade-offs would you consider?"

**What a strong answer includes:**
- ✅ Acknowledges the problem: Large documents need splitting for retrieval and context window limits
- ✅ Mentions strategies: Fixed-size chunks (e.g., 512 tokens), semantic boundaries (paragraphs, sections), or hybrid
- ✅ Trade-offs:
  - Small chunks: More precise retrieval, but lose context
  - Large chunks: Preserve context, but might retrieve irrelevant material
  - Overlapping chunks: Smoother handoff, but redundant storage
- ✅ Domain-aware thinking: For legal docs, respect sentence/paragraph/section boundaries (don't chunk mid-paragraph)
- ✅ Mentions metadata: Store source, page number, date for traceability

**Red flags in weak answers:**
- "Just split every 512 tokens"
- No mention of trade-offs
- Doesn't consider document structure
- No awareness of chunk overlap benefits

**Follow-up if they nail it:**
"Your retrieval is returning irrelevant sections. How would you fix it?"

---

## Question 3: Vector Database Selection

**The Question:**
"You're choosing a vector database for a production RAG system handling 10 million documents. What factors would you evaluate, and would you pick an open-source or managed solution?"

**What a strong answer includes:**
- ✅ Evaluation criteria:
  - Scale: Does it handle 10M+ vectors?
  - Latency: Query response time (milliseconds matter in prod)
  - Throughput: Concurrent queries per second
  - Cost: Per-query or per-month pricing?
  - Durability: Backups, replication, disaster recovery
  - Ease of updates: Can you re-embed and update vectors in place?
- ✅ Open vs. managed:
  - Open-source (Milvus, FAISS): More control, self-hosted, operational burden
  - Managed (Pinecone, Weaviate Cloud): Easier, but vendor lock-in and cost
- ✅ Mentions specific trade-offs: Managed = less ops work but higher per-query cost
- ✅ Practical consideration: Hybrid indexing (both dense + keyword search)

**Red flags in weak answers:**
- "Just pick Pinecone" (no reasoning)
- Doesn't mention latency/throughput trade-offs
- No cost consideration
- Confuses "good at scale" with "production-ready"

**Follow-up if they nail it:**
"Query latency is creeping up to 500ms. What are your options?"

---

## Question 4: RAG Failure Modes and Debugging

**The Question:**
"You deployed a RAG system, but it's returning irrelevant documents and the LLM is hallucinating facts not in the retrieved context. Walk me through how you'd debug and fix this."

**What a strong answer includes:**
- ✅ Diagnoses the problem:
  - Retrieval failure: Embeddings or chunking not capturing intent
  - Context quality: Retrieved docs are relevant but incomplete
  - LLM failure: Even good context, model still hallucinates
- ✅ Debugging approach:
  - Log retrieved documents and scores (is top-1 relevant?)
  - Inspect query embeddings vs. document embeddings (are they in the same space?)
  - Test retrieval in isolation (without LLM) to isolate the problem
  - Check chunking: Are you losing critical context due to chunk boundaries?
- ✅ Solutions:
  - Rerank results (semantic re-ranker after initial retrieval)
  - Re-chunk with larger context windows
  - Improve prompt: "Only cite facts from the retrieved context"
  - Add citation grounding: Require LLM to cite source

**Red flags in weak answers:**
- "Just increase chunk size" (no structured debugging)
- Doesn't isolate retrieval vs. LLM problem
- No mention of metrics (top-1 accuracy, MRR)
- Suggests retraining without understanding the actual failure

**Follow-up if they nail it:**
"You re-ranked and it helped, but recall dropped. Why, and how do you balance precision vs. recall?"

---

## Question 5: Citation and Grounding in RAG

**The Question:**
"How would you ensure that an LLM's responses in a RAG system are grounded in the retrieved documents and properly cited? What could go wrong?"

**What a strong answer includes:**
- ✅ Grounding techniques:
  - Strict prompt: "Only answer from the provided context. If not in context, say 'I don't know.'"
  - Retrieval quality: Better retrieval = more grounded responses
  - Citation format: Ask LLM to output "Fact X from Document Y, page Z"
  - Validation: Check if cited text actually exists in retrieved docs
- ✅ What can go wrong:
  - Hallucinated citations: LLM cites documents that weren't retrieved (citation hallucination)
  - Out-of-context citations: Correct fact, but misapplied
  - Missed citations: LLM uses facts but forgets to cite
  - Context length issues: Can't fit all retrieved context, so model picks and chooses
- ✅ Measurement: Compute "citation accuracy" = % of facts that are properly cited in retrieved docs

**Red flags in weak answers:**
- "Just tell the LLM to cite sources"
- Doesn't acknowledge hallucinated citations
- No validation mechanism
- No measurement strategy

**Follow-up if they nail it:**
"You have high citation accuracy but low answer quality. What's happening?"

---

## Question 6: Scaling RAG to New Domains

**The Question:**
"You successfully built a RAG system for customer support using our product docs. Now, you need to extend it to handle medical research papers. What changes would you make, and what could break?"

**What a strong answer includes:**
- ✅ Differences in domain:
  - Medical papers: Highly technical, structured (abstract/methods/results/conclusion), heavy jargon
  - Product docs: Customer-facing, variable structure, accessible language
- ✅ What might break:
  - Same embedding model: May not capture medical terminology as well
  - Chunking strategy: Medical papers benefit from section-aware chunking
  - Metadata: Citations, author, publication date matter more in research
  - Retrieval threshold: Science is more precise—false positives are costly
  - Evaluation: Different metrics (precision > recall for medical facts)
- ✅ Changes needed:
  - Test embedding model on medical domain (domain-specific models exist)
  - Adapt chunking to paper structure
  - Add metadata indexing (date, citation count, author)
  - Stricter citation requirements
  - Re-evaluate on domain-specific test set

**Red flags in weak answers:**
- "Just use the same system"
- Doesn't consider domain-specific jargon
- No mention of re-evaluation
- Treats all domains the same

**Follow-up if they nail it:**
"You evaluated on 100 medical papers and found 30% accuracy. Is that good? What would you do next?"

---

## Question 7: Bonus - Advanced: Cost Optimization

**The Question:**
"Your RAG system is costing $50k/month in embedding and LLM API calls. The system handles 100k queries/day. How would you optimize costs while maintaining quality?"

**What a strong answer includes:**
- ✅ Identifies cost drivers:
  - Embeddings: Each query embeds the search query + retrieval re-embeds docs
  - LLM calls: Each query calls the LLM once
  - Retrieval: Multiple retrievals per query can add up
- ✅ Optimization strategies:
  - Cache embeddings: Pre-embed all docs once, reuse
  - Batch processing: Embed multiple queries together
  - Model selection: Smaller embeddings (e.g., smaller fine-tuned model) for speed/cost
  - Cached retrievals: Common queries get pre-computed results
  - Hybrid search: Keyword search first (free), then semantic search only for top-k
  - Smaller LLM for summary: Use fast model to synthesize, only use GPT-4 if needed
- ✅ Metrics: Compute cost-per-query, monitor quality (don't sacrifice for cost)

**Red flags in weak answers:**
- "Just use a smaller model" (no cost/quality trade-off analysis)
- Doesn't identify where the money is going
- Suggests changes without measuring impact
- Implies you can't have both quality and low cost

**Follow-up if they nail it:**
"You optimized and cut costs by 40%, but user satisfaction dropped. Why, and what do you do?"

---

## Bonus: Rapid-Fire Technical Q&A

Use these for quick checks during the interview:

1. **"What's cosine similarity and why is it used for embeddings?"**  
   → Answer: Measures angle between vectors (0–1 scale), efficient, domain-agnostic

2. **"Why would you use a re-ranker after initial retrieval?"**  
   → Answer: Initial retrieval is fast but loose; re-ranker is precise but slower. Use both for speed + quality.

3. **"What happens if your retrieval returns an empty result?"**  
   → Answer: LLM hallucinates or says "not found." Should be handled in prompt/logic.

4. **"How do you know if your RAG system is better than a baseline LLM without RAG?"**  
   → Answer: A/B test: measure citation accuracy, fact correctness, user satisfaction.

5. **"What's the difference between sparse and dense retrieval?"**  
   → Answer: Sparse (keyword): fast, interpretable, misses semantic matches. Dense (embedding): semantic, slower, high-dimensional.

---

## Interview Tips

1. **Listen for depth:** Do they understand the *why*, not just the how?
2. **Trade-offs matter:** Good candidates acknowledge costs and benefits.
3. **Production thinking:** Ask "how would you measure this?" — strong candidates think about metrics.
4. **Question depth:** If they nail a question, dig deeper (see follow-ups).
5. **Real-world framing:** Use concrete scenarios, not abstract theory.

---

*Week 3 Interview Questions | GenAI for Everyone | Embeddings & RAG*
