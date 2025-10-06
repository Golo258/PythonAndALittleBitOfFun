import re
import inspect

"""
    Regex always works on string and pattern
    It try to adjust pattern to the string
    
    
"""


class RegexPlayground(object):

    def __init__(self, text):
        self.example_text = text

    """
        Check if text begins with the pattern
        Match is not looking forward, only the beginning
    """

    def match_example(self):
        text_match = re.match(r"Ola", self.example_text)
        self.log_current_method()
        self.show_match_object(text_match)
        # try with something else then iin the beginning
        forward_match = re.match(r"but", self.example_text)
        assert forward_match is None

    """
        Search is looking the first occurrence of an pattern
            whenever in the text 
        not like a match only at the beginning
    """

    def search_example(self):
        search_match = re.search(r"have", self.example_text)
        self.log_current_method()
        self.show_match_object(search_match)

    """
        Returns list of every match in the given text
            not a match group but real result of pattern 
    """

    def findall_example(self):
        matching_list = re.findall(r"\d+", self.example_text)
        self.log_current_method()
        print(f"{matching_list=}")

    """
        The same thing as findall returns every match in text
            but not list, it returns Match Object Iterator
        with which you can take the position, group etc.
    """

    def find_iter_example(self):
        patterns_iterator = re.finditer(r"\d+", self.example_text)
        self.log_current_method()
        for iter_match in patterns_iterator:
            self.show_match_object((iter_match))

    """
        Helper to inspect current function name
    """

    def log_current_method(self):
        print(f"➡️ {inspect.currentframe().f_back.f_code.co_name}()")

    """
        Each match and search returns Match Object 
            with some interesting information
        Lets'show it all
    """

    def show_match_object(self, match_object):
        print(
            f"{match_object.group()=}\n"  # whole matched text
            # f"{match_object.group(1)=}\n" #  specific group of matched text
            f"{match_object.groups()=}\n"  # all groups
            f"{match_object.span()=}\n"  # tuple(start, end)
            f"{match_object.start()=}\n"  # indexes of start 
            f"{match_object.end()=}\n"  # and end of match 
            f"{match_object.pos=}{match_object.endpos=}\n"
        )

    """
        There are some flags -- optional parameters
            which change way of matching text
    """

    def flags_example(self):
        ignore_case = re.IGNORECASE | re.I
        start_end_on_multiline = re.MULTILINE | re.M
        adjust_everything = re.DOTALL | re.S

        case_text_example = "HEllO\nHow are ya"
        print(re.search(r"hello", case_text_example, re.IGNORECASE))
        print(re.search(r".+", case_text_example, re.DOTALL))

    def capturing_groups(self):
        self.log_current_method()
        groups_match = re.search(
            r"(\w+)\s+ma\s+(\w+)",
            "Ala ma kota"
        )
        print(f"Always the whole matched text: {groups_match.group(0)}\n"
              f"First groups in the brackets {groups_match.group(1)}\n"
              f"Second groups in the brackets {groups_match.group(2)}\n"
              f"All groups: {groups_match.groups()}\n"
              f"Groups positions: {groups_match.span(1)}\n"
              f"Groups positions: {groups_match.span(2)}\n"
       )
        # giving labels to group
        labeled = re.search(
            r"(?P<who>\w+) ma (?P<what>\w+)",
            "Ala ma kota"
        )
        print(f"Who?: {labeled.group("who")}\n"
            f"What?: {labeled.group("what")}"
        )

if __name__ == "__main__":
    example_text = "Ola has a cat, but Ola doesnt have guitar 12"
    numeric_example = "id:161276, test: 45125"
    playground = RegexPlayground(example_text)
    playground.match_example()
    playground.search_example()
    numeric_playground = RegexPlayground(numeric_example)
    numeric_playground.findall_example()
    numeric_playground.find_iter_example()
    playground.flags_example()
    playground.capturing_groups()
