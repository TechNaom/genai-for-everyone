# Answer Key — Session 6.2 Quiz

**1.** Generating tokens (output) requires the model to run its full forward pass token by token, which is more compute-intensive than processing tokens it's already been given (input). Providers price to reflect that compute difference — output is typically 3-5x the price of input.

**2.** Prompt caching. If the same 2,000-token prefix appears in every request, caching lets you pay full price for it once and a much smaller fraction on every subsequent request that reuses that exact prefix — turning a cost that scales with request volume into something close to a one-time cost.

**3.** False. Batch APIs trade turnaround time (minutes to hours) for a steep discount, which is only acceptable for workloads that don't need an instant response — nightly processing, bulk classification, report generation. A live chat interface needs real-time responses.

**4.** Model routing — send simple requests (e.g., yes/no, short lookups) to a cheaper/smaller model and reserve the expensive model for genuinely complex requests. This is usually the single biggest lever because most real traffic in a support context skews toward simple questions, so most of the expensive-model spend is unnecessary.

**5.** Tokens in and out per request, dollar cost per request, and latency per request (ideally broken down by where the time goes: network, model inference, your own processing).

**6.** Both. More output tokens directly costs more money (output tokens are the expensive ones), and generating 400 tokens takes longer than generating 50, so it's also slower for the user waiting on the response. Constraining requested length (e.g., "in 2 sentences," "50 words max") addresses both at once.

**7.** Because the "obvious" fix (e.g., switching to a cheaper model everywhere, or aggressively truncating prompts) can quietly break quality or correctness in ways that aren't visible until a user complains — and without a measured baseline (tokens/cost/latency per request), you can't tell afterward whether your change actually helped, hurt, or did nothing. Optimizing without measuring risks solving a problem you don't actually have while breaking something you didn't notice you had.
