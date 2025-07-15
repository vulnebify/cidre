import subprocess


def test_help_output():
    result = subprocess.run(["cidre", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "usage: cidre [-h] {cidr,firewall} ..." in result.stdout


def test_cidr_pull():
    result = subprocess.run(["cidre", "cidr", "pull"], capture_output=True, text=True)
    assert result.returncode == 0
    assert (
        "💡 Pulling ranges from RIRs to compile CIDRs with disabled merging..."
        in result.stdout
    )
    assert "Pulling complete ✅" in result.stdout


def test_cidr_pull_with_merging():
    result = subprocess.run(
        ["cidre", "cidr", "pull", "--merge"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert (
        "💡 Pulling ranges from RIRs to compile CIDRs with enabled merging..."
        in result.stdout
    )
    assert "Pulling complete ✅" in result.stdout


def test_cidr_count():
    result = subprocess.run(
        ["cidre", "cidr", "pull", "--merge"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    result = subprocess.run(
        ["cidre", "cidr", "count"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "US: " in result.stdout
    assert "RU: " in result.stdout
