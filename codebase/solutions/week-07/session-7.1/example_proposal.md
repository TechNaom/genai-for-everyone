# Capstone Proposal: Freelancer Invoice Q&A Bot

## Problem + user
Solo freelancers who invoice 5-15 clients a month and can't remember which invoices are overdue, what payment terms each client agreed to, or which invoices already got a follow-up email.

## Solution sketch
Freelancer uploads their invoice PDFs (or a CSV export). A RAG-based chatbot answers questions like "which invoices are overdue?" or "what are Acme Corp's payment terms?" grounded in the actual uploaded documents, with citations back to the specific invoice.

## Techniques used (and why)
RAG (Week 3) to ground answers in the actual invoice documents instead of guessing. Evaluation + safety (Week 5) to build a golden dataset of 10 realistic invoice questions and a red-team pass checking it doesn't hallucinate payment amounts. Deployment (Week 6) to wrap it as a simple Flask service with logging.

## Success criteria
Correctly answers at least 8/10 golden-dataset questions (grounded, citing the right invoice), and the red-team pass finds zero cases of a hallucinated dollar amount.

## Out of scope
No actual payment processing or client communication automation — read-only Q&A over already-uploaded documents. No multi-user accounts; single-freelancer use only for this capstone.
