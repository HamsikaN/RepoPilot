from zip_safety import find_unsafe_names, is_safe_member_name


def test_normal_paths_are_safe():
    assert is_safe_member_name("app/main.py")
    assert is_safe_member_name("README.md")
    assert is_safe_member_name("my..file.py")


def test_parent_traversal_is_unsafe():
    assert not is_safe_member_name("../../x.py")
    assert not is_safe_member_name("app/../../x.py")
    assert not is_safe_member_name("..\\..\\x.py")


def test_absolute_paths_are_unsafe():
    assert not is_safe_member_name("/etc/passwd")
    assert not is_safe_member_name("C:/Windows/x.py")


def test_empty_and_null_names_are_unsafe():
    assert not is_safe_member_name("")
    assert not is_safe_member_name("a\x00b.py")


def test_find_unsafe_names_returns_only_bad_ones():
    names = ["ok.py", "../bad.py", "dir/fine.py"]
    assert find_unsafe_names(names) == ["../bad.py"]