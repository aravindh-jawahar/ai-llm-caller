"""Pydantic v2 validation topics, one module per concept.

Each module builds on the Person/Customer models and follows the same rhythm:
when-it-matters → a passing case → a failing case (real ValidationError) →
a "your turn" exercise (as a comment at the bottom).

Run one:   uv run python -m examples.data_model_and_validations.topics.t01_field_constraints
Run all:   uv run python -m examples.data_model_and_validations.topics.run_all
"""
