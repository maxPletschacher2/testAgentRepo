import importlib


def test_import_calculator_module():
    module = importlib.import_module("calculator")
    assert module is not None


def test_has_calculator_engine_class():
    module = importlib.import_module("calculator")
    # Die Engine-Klasse sollte im Modul verfügbar sein (wird auch von bestehenden Tests genutzt)
    assert hasattr(module, "CalculatorEngine"), "CalculatorEngine-Klasse fehlt im calculator-Modul"
