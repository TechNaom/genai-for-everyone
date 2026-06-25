# Answer Key — Session 2.3 Quiz

**1.** B — Each generated reasoning step becomes part of the context window that subsequent tokens are predicted from, giving the model more relevant grounding for later steps than jumping straight to a final answer.

**2.** The honest limit: a beautifully formatted, step-by-step chain of reasoning can still arrive at a wrong conclusion. Visible reasoning improves the ODDS of correctness on many tasks, but it's not proof — fluency and structure are properties of the presentation, not guarantees about the underlying logic being sound.

**3.** B — Step-back prompting is most valuable when there's a real general framework or principle to surface before applying it to specifics, which is characteristic of comparisons and recommendations, not simple lookups or formatting tasks.

**4.** Divergent answers across runs are a signal that the model is genuinely uncertain or that the case is ambiguous/difficult for it — exactly the kind of case where a single confident-sounding response shouldn't be trusted at face value. You should treat the answer as unreliable and seek additional verification (human review, a different approach, more context) rather than picking one of the divergent answers and moving on.

**5.** Push back on the cost: self-consistency multiplies token cost and latency by the number of runs, and for a low-stakes, high-volume feature, that cost is rarely justified — the technique is meant for genuinely ambiguous or high-stakes cases, not as a default applied to every request. This connects directly to Session 1.3's cost/speed trade-off framework.

**6.** Push back gently: thoroughness and formatting quality are properties of presentation, not proof of correctness. A wrong answer can be presented just as beautifully and step-by-step as a correct one. The reasoning should actually be checked/verified, especially for anything important, rather than trusted because it looks rigorous.
