import tempfile
import pathlib
import pytest
from inspectr.complexity import Complexity, Analyzer, main


def test_complexity_constant():
    c = Complexity.constant()
    assert c.expression == "O(1)"
    assert not c.is_approximate


def test_complexity_linear():
    c = Complexity.linear()
    assert c.expression == "O(n)"
    assert not c.is_approximate


def test_complexity_linear_coefficient():
    c = Complexity.linear(3)
    assert c.expression == "O(3n)"
    assert not c.is_approximate


def test_complexity_combine_sequential():
    c1 = Complexity.linear()
    c2 = Complexity.linear()
    result = c1.combine_sequential(c2)
    assert "n" in result.expression


def test_analyzer_simple_function():
    code = "def foo():\n    pass\n"
    analyzer = Analyzer()
    results = analyzer.analyze_file(code)
    assert len(results) == 1
    assert results[0].name == "foo"


def test_analyzer_for_loop():
    code = "def foo():\n    for i in range(10):\n        pass\n"
    analyzer = Analyzer()
    results = analyzer.analyze_file(code)
    assert len(results) == 1


def test_main_with_file(capsys):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("def foo():\n    pass\n")
        path = pathlib.Path(f.name)
    
    try:
        main([path])
        output = capsys.readouterr().out
        assert "Complexity Analysis" in output
        assert "foo" in output
    finally:
        path.unlink()


def test_main_nonexistent_file(capsys):
    path = pathlib.Path("/nonexistent/file.py")
    main([path])
    output = capsys.readouterr().out
    assert "does not exist" in output


def test_analyzer_syntax_error():
    code = "def broken(\n"
    analyzer = Analyzer()
    with pytest.raises(ValueError):
        analyzer.analyze_file(code)


def test_complexity_simplify():
    c = Complexity("O(n)+O(n)", False)
    simplified = c.simplify()
    assert simplified.expression != ""
