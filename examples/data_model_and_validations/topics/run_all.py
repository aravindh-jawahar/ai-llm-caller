"""Run every validation topic in order.

    uv run python -m examples.data_model_and_validations.topics.run_all
"""

from examples.data_model_and_validations.topics import (
    t01_field_constraints,
    t02_enums,
    t03_custom_validators,
    t04_annotated_types,
    t05_serializers_computed,
    t06_model_config,
    t07_alias_populate,
    t08_strict_vs_coercion,
    t09_error_handling,
    t10_type_adapter,
)

TOPICS = [
    t01_field_constraints,
    t02_enums,
    t03_custom_validators,
    t04_annotated_types,
    t05_serializers_computed,
    t06_model_config,
    t07_alias_populate,
    t08_strict_vs_coercion,
    t09_error_handling,
    t10_type_adapter,
]


def main() -> None:
    for topic in TOPICS:
        topic.run()
        print()


if __name__ == "__main__":
    main()
