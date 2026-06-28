# Session 4.2 Quiz — Answer Key

---

**1. Answer: B**

A model "calling a tool" means it generates a structured request — naming the tool and the specific arguments it wants to use — and stops there. The model never executes anything itself; it has no code execution environment, no hands, no permissions. Your application is entirely responsible for actually running the real function and reporting the result back. This is the central reframe the session opens with: tool calling is a communication protocol between a model that can reason but can't act, and code that can act but can't decide when to.

---

**2. Answer: A**

A tool's description is the single highest-leverage part of its definition because the model reads it to decide both what the tool does and, just as importantly, when it's appropriate to use it — exactly the same kind of work a prompt does for the model's overall behavior. It is not the tool's source code (the model never sees the implementation at all), it is not purely cosmetic (vague descriptions produce unreliable tool-calling behavior), and it's read by the model, not shown to the end user.

---

**3. Answer: B**

The model processes the conversation sequentially, the same way it reads any other context. If a tool's result doesn't directly follow the tool-use request that produced it, the model has no reliable mechanism to connect the result to the right call — especially once multiple tool calls might be in flight. This is a structural requirement of how the conversation history is read, not a billing rule, an expiration policy, or something specific to one particular tool.

---

**4. Sample answer:**

The first place to look is the tool's description and input schema, not the model itself. A model decides to call a tool through the same next-token-prediction process behind all of its other output — there's no separate "decision module" to debug. Unreliable or unexpected tool-calling behavior is almost always a sign that the tool's description is vague about when to use it, or that the schema doesn't clearly specify what's expected, the same way a vague prompt produces a vague or inconsistent response. Concluding "the model is unreliable" skips past the much more common and far more fixable explanation: the tool's specification under-determined the behavior, the same way an under-specified prompt does.

---

**5. Answer: C**

`weather_lookup` should return an explicit, honest error result (such as a dict with an "error" key) when it has no data for a requested city, so the model can see exactly what happened and respond accordingly — for example, telling the user honestly that weather data isn't available rather than guessing. Raising an exception risks crashing the whole interaction, silently returning nothing leaves the model with no information to react to, and guessing a forecast would mean fabricating data the tool was specifically built to provide accurately — exactly the kind of confident-but-wrong behavior this course has warned against since Session 3.1.

---

**6. Sample answer:**

Session 4.1's plan-act-observe loop was demonstrated with a scripted, hand-authored policy standing in for the model's decisions — the tools themselves were real and executable, but the *choice* of when to call them was written in advance by a human, not actually decided by a live model. Session 4.2 changes exactly the "act" step (and, as a direct consequence, "plan" and "observe" too) from simulated to real: an actual LLM now reads the live conversation and genuinely decides, on its own, whether a question needs a tool, which tool, and with what arguments — with your code handling execution and feeding the real result back, completing a loop that's now driven by the model's actual decisions rather than a stand-in for them.
