import re


def findall(pattern, text):
    """
    Finds all occurrences of a pattern
    Does not show named groups
    Returns a list
    """
    reg = re.compile(pattern)
    return reg.findall(text)


def search_named_groups(pattern, text):
    reg = re.compile(pattern)
    match = reg.search(text)
    if match:
        return match.groupdict()
    return None


def search_groups(pattern, text):
    reg = re.compile(pattern)
    match = reg.search(text)
    if match:
        return match.groups()
    return None


"""
match vs search

re.match() function of re in Python will search the regular expression pattern and 
return the first occurrence. The Python RegEx Match method checks for a match only at 
the beginning of the string. So, if a match is found in the first line, it returns the 
match object. But if a match is found in some other line, the Python RegEx Match 
function returns null.

re.search() function will search the regular expression pattern and return the first 
occurrence. Unlike Python re.match(), it will check all lines of the input string. The 
Python re.search() function returns a match object when the pattern is found and “null” 
if the pattern is not found

"""

if __name__ == "__main__":
    # Findall examples
    print(findall("([0-9]+)([a-zA-Z]?)", "10R5L5R10L4R5L5"))
    print(findall("toto", "toto mange toto"))
    print(findall(r"(?P<word>\b\w+\b)", "(((( Lots of punctuation )))"))

    # Named group search
    print(search_named_groups(r"(?P<first>\w+) (?P<last>\w+)", "Jane Doe"))
    print(search_named_groups(r"(?P<first>\w+) (?P<last>\w+)", "1234"))
    print(
        search_named_groups(
            r"(?P<mode1>\d)?(?P<mode2>\d)(?P<mode3>\d)(?P<opcode>\d\d)", "1002"
        )
    )

    # Group by index search
    print(
        search_groups(
            r"(?P<mode1>\d)?(?P<mode2>\d)(?P<mode3>\d)(?P<opcode>\d\d)", "1002"
        )
    )
    print(search_groups(r"^([0-9]+)\*([\w]+)=(.*)$", "1*NHQH=3*NDMT"))
