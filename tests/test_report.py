import os
from utils.reporting import save_report


def test_save_report(tmp_path):
    os.chdir(tmp_path)
    save_report("123", "Test Topic", "# Content")
    filename = tmp_path / "report_123.md"
    assert filename.exists()
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    assert "# Relatório de Inteligência: Test Topic" in content
    assert "# Content" in content
