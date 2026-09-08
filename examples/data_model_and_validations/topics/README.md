# Pydantic v2 validation — practice topics

Ten runnable modules, one concept each, built on the `Person`/`Customer` models.
Every module follows the same rhythm:

**when-it-matters → passing case → failing case (real `ValidationError`) → a "your turn" exercise** (a comment at the bottom of the file).

## Run

```bash
# all topics, in order
uv run python -m examples.data_model_and_validations.topics.run_all

# one topic
uv run python -m examples.data_model_and_validations.topics.t03_custom_validators
```

## The ladder

| # | Module | Concept |
|---|--------|---------|
| 1 | `t01_field_constraints` | `Field()` constraints — `min_length`, `ge/le`, `pattern` |
| 2 | `t02_enums` | `str`/`IntEnum` for fixed-choice fields |
| 3 | `t03_custom_validators` | `@field_validator`, `@model_validator` (before/after) |
| 4 | `t04_annotated_types` | `Annotated[...]` + `AfterValidator`/`BeforeValidator` |
| 5 | `t05_serializers_computed` | `@field_serializer`, `@computed_field` |
| 6 | `t06_model_config` | `ConfigDict`: `extra`, `str_strip_whitespace`, `validate_assignment`, `frozen` |
| 7 | `t07_alias_populate` | `alias`, `populate_by_name`, `AliasChoices` |
| 8 | `t08_strict_vs_coercion` | strict mode vs. default coercion |
| 9 | `t09_error_handling` | `ValidationError` → `e.errors()`, `e.json()` |
| 10 | `t10_type_adapter` | `TypeAdapter` for non-`BaseModel` types |

## How to practice

Each file ends with a `📝 YOUR TURN:` comment — a concrete task. Do those to
keep the hands-on loop; the surrounding code is the worked example to build on.
