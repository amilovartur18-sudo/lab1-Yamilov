"""Тесты CLI (через main, без настоящего subprocess по возможности)."""

import subprocess
import sys

from toolkit.__main__ import main
from toolkit.errors import ToolkitError


def test_help_exit_code_zero() -> None:
    """--help завершается с кодом 0."""
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "calc" in result.stdout or "convert" in result.stdout


def test_calc_success_via_main() -> None:
    """Успешный calc через main() возвращает 0."""
    code = main(["calc", "2+3*4"])
    assert code == 0


def test_user_error_returns_code_2(capsys) -> None:
    """Пользовательская ошибка → stderr и код 2."""
    code = main(["calc", "1/0"])
    captured = capsys.readouterr()
    assert code == 2
    assert captured.err != ""
    err = captured.err.lower()
    assert "error" in err or "ноль" in err or "дел" in err


def test_kernel_has_no_input_print() -> None:
    """Ядро не вызывает ввод/вывод — только считает и бросает исключения."""
    import ast
    from pathlib import Path

    root = Path(__file__).resolve().parents[1] / "src" / "toolkit"
    for name in ("calculator.py", "converter.py"):
        tree = ast.parse((root / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in {"input", "print"}
    assert issubclass(ToolkitError, Exception)
