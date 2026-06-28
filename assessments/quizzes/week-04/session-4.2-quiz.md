# Session 4.2 Quiz — Function/Tool Calling

*6 questions. Mixed multiple-choice and short-answer.*

---

**1.** When a model "calls a tool," what is actually happening?

A) The model directly executes the function's code on Anthropic's servers
B) The model generates a structured request naming the tool and its arguments; your application is responsible for actually running it
C) The tool's code gets temporarily copied into the model's weights
D) The model writes and runs a new Python script from scratch

---

**2.** A tool's description is described in the session as functioning like a kind of prompt. What is it actually doing?

A) It tells the model when and why to use this specific tool, alongside what it does
B) It contains the tool's actual source code for the model to read
C) It's purely cosmetic and has no effect on the model's behavior
D) It is shown to the end user, not the model

---

**3.** Why must a tool_result message immediately follow its corresponding tool_use message in the conversation, with nothing in between?

A) The Anthropic API charges extra for messages out of order
B) The model is reading the conversation sequentially; without the result directly following the request, there's no reliable way for it to connect the two
C) Tool results expire after one message
D) This is only a requirement for the calculator tool specifically

---

**4. Short answer.** A team's tool-calling agent intermittently calls the wrong tool, or doesn't call a tool when it clearly should. Explain where you'd look first to fix this, and why that's the right starting point rather than concluding the model itself is unreliable.

---

**5.** In the session's weather/calculator example, what should `weather_lookup` do if it's asked about a city not in its database?

A) Raise an exception so the program crashes immediately
B) Silently return nothing
C) Return an explicit error result (e.g. a dict with an "error" key) so the model can see the lookup failed and respond honestly
D) Guess a plausible weather forecast based on the city's general climate

---

**6. Short answer.** Explain the relationship between Session 4.1's plan-act-observe loop and what this session actually built. Specifically: which part of the loop did 4.1 simulate, and what changed about it in 4.2?
