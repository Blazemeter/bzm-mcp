from tools.utils import validate_required_args


def test_validate_required_args_returns_error_for_missing_keys():
    result = validate_required_args("read", {}, ["project_id"])
    assert result is not None
    assert result.error is not None
    assert "Missing required args for action 'read'" in result.error
    assert "project_id" in result.error
    assert "within 'args'" in result.error


def test_validate_required_args_accepts_present_keys():
    result = validate_required_args("read", {"project_id": 123}, ["project_id"])
    assert result is None
