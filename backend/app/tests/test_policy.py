from app.tools import policy


def test_requires_approval_sensitive():
    assert policy.requires_approval("terminal.run", {}) is True
    assert policy.requires_approval("filesystem.read", {}) is True


def test_requires_approval_safe():
    assert policy.requires_approval("todo.add", {}) is False
