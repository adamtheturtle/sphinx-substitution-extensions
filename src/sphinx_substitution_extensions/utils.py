def exists_dependency(
    name: str,
) -> bool:
    try:
        __import__(name)
    except ImportError as e:
        return False
    return True