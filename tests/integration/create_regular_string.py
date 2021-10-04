import re


def unificate(string):
    string = "\n" + string + "\n"
    patterns = {
        "\n": r" *[(\r\n)\n]+",
        " ": r"[\t ]+",
        "": r"\x0c",
    }
    for symbol, pattern in patterns.items():
        parts = re.split(pattern, string)
        string = symbol.join(parts)

    return string