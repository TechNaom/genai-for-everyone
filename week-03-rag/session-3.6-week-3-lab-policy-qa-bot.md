# Session 3.6 — Week 3 Lab: Building a Company Policy Q&A Bot

## The Monday morning test

Imagine it's your first week at a new job. You don't know the company's
remote work rules, you're not sure how to expense a client dinner, and
you have no idea whether your laptop needs a password rotation every
month or every six. In most companies, the honest answer to "where do I
find this out" is: *ask around, dig through a shared drive, hope someone
remembers, and probably get a slightly wrong answer from three different
people.*

This is, by a wide margin, the single most common reason companies build
a RAG system. Not chatbots that write poetry. Not agents that browse the
web. A bot that can correctly answer "how many sick days do I get" by
pulling from the actual HR policy document and saying exactly where it
got the answer from. It's unglamorous, and it's also probably the
single most economically valuable application of everything you've
learned this week.

That's what you're building today. Not a new concept — you've already
learned every piece. Today is about **putting them together and finding
out what breaks when you do.**

## What "putting it together" actually means

Here's the arc of the week, compressed:

- **3.1** asked: does this problem even need retrieval, or is it better
  solved another way?
- **3.2** showed you that text can become a vector, and that vectors
  close together mean "about the same topic."
- **3.3** showed you how to chunk a document and search those chunks by
  similarity.
- **3.4** showed you how to take retrieved chunks, hand them to a model
  with strict citation instructions, and verify the model actually
  cited what it claimed to.
- **3.5** showed you the ways this breaks — bad chunking, retrieval
  misses, too much irrelevant context, no re-ranking — and how a real
  engineer goes about fixing each one.

Today's lab does something the earlier sessions deliberately avoided
doing: it gives you **more than one source document.** Sessions 3.3 and
3.4 worked with a single, self-contained company handbook. That's a
reasonable place to start, but it hides a problem that shows up almost
immediately in real RAG systems: **which document should answer this
question?**

## Why multiple documents change everything

Think about how policy documents actually get written inside a real
company. The remote work policy was probably written by the People
team. The expense policy was probably written by Finance, possibly a
year later, by someone who had never read the remote work policy. The
IT security policy was written by a different team entirely, on a
different schedule, possibly referencing "equipment" or "devices" in a
totally different sense than the other two documents do.

These documents will **overlap**. They'll sometimes **cross-reference**
each other ("see the Remote Work Policy for stipend details"). And they
were never designed, as a set, to be machine-searchable. Your retrieval
system has to cope with all of that — and a system that worked
perfectly on one tidy handbook can fail in genuinely surprising ways
the moment you add a second document.

In today's lab, you'll build a retrieval system over four policy PDFs:
remote work, expenses, leave, and IT security. And you're going to hit
a real bug — one that was discovered by actually running this code
against actual generated PDFs, not invented to make a point.

## The bug you're going to find

Here's the question that breaks things:

> "What is the home office equipment stipend amount?"

The correct answer — a one-time $500 stipend — lives in the Remote Work
Policy, under a section called "Home Office Equipment Stipend." It's
right there, clearly labeled, easy for a human to find in about four
seconds.

But if you chunk that document the same way you did in Session 3.3 —
splitting on blank lines between paragraphs — something unexpected
happens. The retrieval system pulls up the **Expense Policy** instead,
specifically a short section about equipment procurement that happens
to mention the word "stipend" once, in passing, as a cross-reference.

Why? Two things are happening at once, and you need to find both.

**The first problem is upstream of anything you'd normally think to
check.** PDF text extraction doesn't reliably preserve the blank lines
that visually separated sections in the original document. When you
pull text out of a PDF with a library like `pypdf`, you typically get a
single newline between lines of text — but not necessarily a blank line
between Section 1 and Section 2, even though they were visibly separated
on the page. If your chunker's whole strategy is "split on blank lines,"
and there *are* no blank lines in the extracted text, the splitter finds
exactly one giant "paragraph": the entire five-section document. No
amount of fiddling with `target_words` fixes this, because the chunker
never even gets a second candidate paragraph to consider starting a new
chunk with. The chunk boundaries simply don't move.

**The second problem is what that giant chunk does to your vector.**
With Eligibility, Remote Work Days, Core Hours, the Stipend section, and
International Remote Work all crammed into one 220-word chunk, the word
"stipend" is just a handful of words out of two hundred. Its weight in
the bag-of-words vector gets diluted by everything else jammed in
alongside it. Meanwhile, the Expense Policy's "Equipment Purchases"
section is short, tightly focused, and happens to contain the word
"stipend" as a one-line cross-reference. A short, hyper-focused chunk
scores *higher* on cosine similarity for a stipend-related query than a
diluted, multi-topic chunk does — even though the short chunk doesn't
actually contain the dollar amount you're looking for.

This is exactly the "chunking errors" failure mode from Session 3.5,
showing up organically instead of being handed to you pre-broken.

## The fix isn't a number — it's a strategy

It would be tempting to "fix" this by just trying smaller and smaller
`target_words` values until something works. Don't — you tested that in
the lab and it does nothing, because the bug isn't about chunk *size*,
it's about the chunker never finding a second paragraph to split on in
the first place.

The actual fix is to stop assuming blank lines mean anything in
PDF-extracted text, and instead split on something that **is** reliably
present: the document's own numbered section headers. "1. Eligibility,"
"2. Remote Work Days," "3. Core Hours" — these patterns survive PDF
extraction intact, because they're literal text, not formatting
whitespace. Split on those instead, and each policy topic becomes its
own chunk, the stipend fact stops being diluted, and retrieval finds the
right document.

This is the deeper lesson of the whole week, stated plainly: **there is
no universal chunking strategy.** A strategy that's exactly right for
one document type (clean markdown with reliable blank-line paragraphs)
can be silently, catastrophically wrong for another (PDFs where layout
whitespace doesn't survive text extraction). Production RAG systems
don't pick one chunking function and apply it everywhere — they inspect
their actual source documents and choose a splitting strategy that
matches how those documents are really structured.

## Multi-document citation: a small but important upgrade

There's one more thing this lab adds that the earlier sessions didn't
need: every retrieved chunk now carries a **source document label**
alongside its content. When the bot answers a question, it doesn't just
cite "[1]" — it can tell you "[1] (Source: Remote Work Policy)." This
matters more than it might look like at first. If an employee asks
about VPN requirements and the bot's answer is grounded in the IT
Security Policy, that's reassuring. If it's somehow grounded in the
Leave Policy, something has clearly gone wrong, and you want that to be
*visible*, not buried inside an answer that merely says "[1]" and gives
no way to sanity-check where [1] came from.

This is a small design choice, but it's the kind of small choice that
separates a demo from something a real team would actually trust enough
to deploy. Citation grounding (from 3.4) plus source-document labeling
(new today) together let anyone — a user, a QA reviewer, you — catch a
wrong-document retrieval at a glance, instead of only discovering it
when someone acts on bad information.

## Points to remember

- The most common real-world RAG use case isn't exotic — it's exactly
  this: a Q&A bot over a company's own internal documents.
- Multiple source documents introduce a failure mode that single-document
  systems hide: retrieval can confidently return the *wrong document*,
  not just an imperfect chunk.
- PDF text extraction often does not preserve blank lines between
  sections, which silently breaks blank-line-based chunking — and no
  amount of adjusting `target_words` will fix a bug that's upstream of
  chunk size entirely.
- The fix for a chunking bug is rarely "try a different number." It's
  usually "look at how this specific document is actually structured,
  and split on something that survives whatever transformation your
  text went through to get to you."
- Tagging every retrieved chunk with its source document, and surfacing
  that tag in the final citation, makes wrong-document retrieval
  visible instead of silent.
- There is no single "correct" chunk size or chunking strategy that
  works for every document type. Production systems choose their
  strategy per document type, based on real inspection, not a default.

## Fill in the blanks

1. PDF text extraction libraries often do not preserve __________ between
   sections, which can break a chunker that assumes paragraphs are
   separated by blank lines.
2. In this lab's bug, the word "stipend" had its weight in the bag-of-
   -words vector __________ because it was crammed into one 220-word
   chunk alongside four unrelated sections.
3. The real fix for the bug was to split on __________ headers instead
   of blank lines, because that pattern survives PDF text extraction
   intact.
4. Adding a __________ label to every retrieved chunk lets a human catch
   a wrong-document retrieval at a glance, instead of discovering it only
   after acting on a bad answer.
5. The deeper lesson of this lab is that there is no single __________
   chunking strategy — production systems match their splitting approach
   to how their actual source documents are structured.

*(Answers: 1. blank lines, 2. diluted, 3. numbered section, 4. source
document / source, 5. universal / one-size-fits-all)*

## Interview questions to sit with

1. "You've built a RAG system that works perfectly in testing but starts
   returning wrong answers once you add a second source document. Walk
   me through how you'd debug that."
2. "Why might a chunking strategy that works well on Markdown
   documentation fail silently on PDF-sourced content?"
3. "What's the difference between a retrieval failure and a generation
   failure in a RAG system, and how would you tell which one you're
   looking at?"
4. "How would you design a RAG system's output so that a wrong-document
   retrieval is easy for a reviewer to catch, without requiring them to
   read the model's full reasoning?"
5. "If you had to support ten different internal documents instead of
   four, each maintained by a different team, what would you change
   about how you approach chunking?"

Next up: Week 4 — Tool Use, Agents & Automation. You've spent this week
teaching a model to *find and use* the right information. Next week,
you'll teach it to *take actions* in the world based on what it finds.
