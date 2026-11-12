# Capstone 2: Autonomous Invoice Processing Agent

## Architecture & Guardrails
- **Boss/Workers Pattern:** Orchestrates specialized validation agents.
- - **Guardrails:** Human-in-the-Loop (HITL) approval gate, Least Privilege tool access, and immutable Audit Trail.

## Security & Testing Proof
- All 10/10 adversarial security attacks successfully blocked (see `day9/test_results.txt`).

## Model Evaluation Summary
- Evaluated across 20 labelled invoices (see `day9/eval.md`). 
- **Chosen Model:** Haiku 5.5 for optimal speed-to-cost ratio in high-throughput production.

## How to Run Tests & Evals
```bash
python3 -m pytest day9/tests/test_attacks.py -v
python3 day9/eval_models.py
