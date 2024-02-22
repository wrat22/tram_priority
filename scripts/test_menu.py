from menu import validate_option


def test_validate_option(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '2')
    assert validate_option(["1", "2", "3", "4", "5"]) == "2"

    monkeypatch.setattr('builtins.input', lambda _: '3')
    assert validate_option(["1", "2", "3", "4", "5"]) == "3"

    monkeypatch.setattr('builtins.input', lambda _: '4')
    assert validate_option(["1", "2", "3", "4", "5"]) == "4"

    monkeypatch.setattr('builtins.input', lambda _: '5')
    assert validate_option(["1", "2", "3", "4", "5"]) == "5"

    monkeypatch.setattr('builtins.input', lambda _: '6')
    assert validate_option(["1", "2", "3", "4", "5"]) == None

    monkeypatch.setattr('builtins.input', lambda _: '7')
    assert validate_option(["1", "2", "3", "4", "5"]) == None


