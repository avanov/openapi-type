from pathlib import Path

TESTS_ROOT             = Path(__file__).parent.absolute()
SPEC_EXAMPLES_DIR      = TESTS_ROOT.parent / "specification" / "examples" / "v3.0"
CUSTOM_EXAMPLES_DIR    = TESTS_ROOT / "custom_examples"

SPECS = [
    (x, SPEC_EXAMPLES_DIR / f"{x}.json") for x in [
        'petstore',
        'petstore-expanded',
        'api-with-examples',
        'callback-example',
        'link-example',
        'uspto',
    ]
] + [
    (x, CUSTOM_EXAMPLES_DIR / f"{x}.json") for x in [
        "one",
        "petstore"
    ]
]
