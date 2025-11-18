# tests/test_project_setup.py
def test_project_structure():
    import pathlib
    import src

    # Verify src directory exists and is importable
    assert pathlib.Path("src").exists()
    assert src.__file__ is not None