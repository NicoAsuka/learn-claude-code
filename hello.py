"""A simple greeting module."""


def greet(name: str) -> str:
    """Return a greeting message for the given name.

    Args:
        name: The name of the person to greet.

    Returns:
        A greeting string.
    """
    return f"Hello, {name}!"


def main() -> None:
    """Run the greeting demo."""
    print(greet("World"))


if __name__ == "__main__":
    main()
