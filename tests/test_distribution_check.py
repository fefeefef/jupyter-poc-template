"""Check that stale or missing build artifacts cannot pass the installation check."""

from pathlib import Path

import pytest

from scripts import check_distribution


@pytest.mark.parametrize("wheel_names", [[], ["first.whl", "second.whl"]])
def test_requires_one_unambiguous_wheel(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, wheel_names: list[str]
) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    for name in wheel_names:
        (dist / name).touch()
    monkeypatch.setattr(
        check_distribution, "__file__", str(tmp_path / "scripts/check_distribution.py")
    )
    with pytest.raises(SystemExit, match="Expected exactly one wheel"):
        check_distribution.main()
