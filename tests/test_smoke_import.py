import importlib


def test_import_calculator_module():
    module = importlib.import_module("calculator")
    assert module is not None


def test_has_calculator_engine_class():
    module = importlib.import_module("calculator")
    assert hasattr(module, "CalculatorEngine"), (
        "CalculatorEngine-Klasse fehlt im calculator-Modul"
    )
