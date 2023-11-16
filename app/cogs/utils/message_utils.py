def join_texts(*args: str, separator: str = "\n") -> str:
    """Joins multiple texts passed as args into one.

    Returns:
        str: a joined string.
    """

    return f"{separator}".join(args)
