# Freelancer Invoice Q&A Bot

## What this does
Solo freelancers juggling 5-15 clients a month often lose track of overdue invoices and payment terms. This project answers questions like "which invoices are overdue?" grounded in the freelancer's own uploaded invoice documents, with citations — for a solo user, no team features.

## See it work
![demo screenshot](docs/demo.png)

A live example: ask "what are Acme Corp's payment terms?" and get an answer citing the specific invoice, not a guess.

## Techniques used
- **RAG** (Week 3): grounds every answer in the actual uploaded invoice documents rather than letting the model guess at figures
- **Evaluation + safety** (Week 5): a 10-question golden dataset plus a red-team pass specifically checking for hallucinated dollar amounts

## Eval results
90% accuracy on the golden dataset (9/10), zero hallucinated dollar amounts across 5 red-team attempts.

## How to run it
```bash
pip install -r requirements.txt
python3 app.py
```
See `DEPLOY.md` for environment variables and free-tier hosting options.
