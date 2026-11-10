def is_safe_member_name(name: str) -> bool:
    """Return True if a ZIP entry name is safe to extract."""
    if not name or "\x00" in name:
        return False

    normalized = name.replace("\\", "/")

    if normalized.startswith("/"):
        return False
    if len(normalized) >= 2 and normalized[1] == ":":
        return False
    if ".." in normalized.split("/"):
        return False

    return True


def find_unsafe_names(names: list[str]) -> list[str]:
    return [name for name in names if not is_safe_member_name(name)]