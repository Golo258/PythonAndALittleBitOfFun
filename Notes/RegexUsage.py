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

    """
        Meta znaki mają specjalne zastosowanie i steruja działaniem wzorca
            jeśli literalnie go chcemy zinterpretować to robimy \
            np \.
        1. kotwice - start i koniec regexa
            ^ - poczatek lini
            $ - koniec lini 
        2. Ilość 
            * - 0 lub wiecej            a*       '' a aaaa
            + - 1 lub wiecej            a+        a aaaa
            ? - 0 lub 1                 a?        '' a 
            {x}  - dokladnie x razy      a{3}       aaa 
            {x,} -  co najmniej x razy   a{3,}      aa aaa aaaaaaa
            {n,m} - od n do m razy      a{1,3}      a aa aaa
        3. Zbiory znaków
            [] - podaje sie jakie znaki są dozwolone
            [abc]      albo a,b, albo c         a b c 
            [a-z]      tylko małe litery       a b g l
            [A-Z]      tylko duze litery       A B C Z
            [0-9]       cyfra                   0..9
            [^0-9]      wszystko opróćz cyfry       a # Z
            ^ - jest zaprzeczeniem w tym przypadku
        4. kropka
            . - dopasowuje dowolny znako oprócz nowej lini
        5. | - alternatywa
            albo ten pattern albo inny
            
        6. () - grupowanie
            nawiasy logiczne wewnątrz regexa
            grupuje elementy, żeby mógłzastosować kwantyfikator * + {}
            doo całej sekwencji
        
        7. \ - ucieczka
            raktowanie znaku dosłownie
            \. - dopasuj dosłownie kropke w regexie
            \\d - dosłownie słowo z \domek
            
             
    """
    def meta_signs_remainder(self):
        def start_meta_example():
            print("start meta example")
            print(re.findall(f"^Uszanowanie", "Uszanowanie co tam"))
            print(re.findall(f"^Uszanowanie", "Witam, Uszanowanie co tam"))

        def end_meta_example():
            print("end meta example")
            print(re.findall(f"co tam$", "Uszanowanie co tam"))
            print(re.findall(f"co tam$", "Uszanowanie co tam u ciebie"))

        def amount_example():
            print("amount example")
            text = "UszaNOWANIE, czy masz #13 pln ?"
            print(
                re.findall(r"[a-z]", text), "\n",
                re.findall(r"[A-Z]", text), "\n",
                re.findall(r"[0-9]", text), "\n",
                re.findall(r"[^0-9]", text), "\n",
                re.findall(r"[alock]", text), "\n",
            )

        """
            4. kropka
            . - dopasowuje dowolny znako oprócz nowej lini
        """
        def dot_example():
            print("dot example")
            print(re.findall(
           r"h.{2}t", "hot, hat, halt, shot, host"
            ))

        """
          5. | - alternatywa
            albo ten pattern albo inny
        """
        def alternative_example():
            print("dot example")
            print(re.findall(
                r"szach|mat", "koń, królowa, szach, król, goniec, mat"
            ))

        """
           6. () - grupowanie
            nawiasy logiczne wewnątrz regexa
            grupuje elementy, żeby móc zastosować ilościowe * + {}
            do danej sekwencji
        """
        def grouping_example():
            print("grouping example")
            #  dopasowuje dana grupe 1 albo wiecej razy
            print(
                re.findall(r"(ab)+", "ababbacaba"),
                re.findall(r"(ab|ca)+", "ababbacaba")
            )

        def escape_example():
            print("escape example")
            print(
                re.findall(r"\d+", "123"),
                re.findall(r"\\d", "d\dd")
            )

        start_meta_example()
        end_meta_example()
        amount_example()
        dot_example()
        alternative_example()
        grouping_example()
        escape_example()
    """
        Klasy znaków:
            Wzór         Znaczenie                    Przykład
            \d         cyfra [0-9]                 5,7,3 
            \D          nie cyfra                 a # x
            \w      znak słowa [azAZ0-9_]           a Z 6 _ - praktycznie wszystko
            \W       nie znak słowa         wszystko co nie nalezy do \w
            \s        biały znak (spacja,tab..)        \n \t ""
            \S         nie biały znak           wszystko oprócz \s
    """
    def special_signs_remainder(self):
        def w_class_example():
            text = "ID123 abc 99 END"
            print(re.findall(r"\w+", text))



        w_class_example()


if __name__ == "__main__":
    example_text = "Ola has a cat, but Ola doesnt have guitar 12"
    numeric_example = "id:161276, test: 45125"
    playground = RegexPlayground(example_text)
    playground.match_example()
    playground.search_example()
    numeric_playground = RegexPlayground(numeric_example)
    numeric_playground.findall_example()
    numeric_playground.find_iter_example()
    print("*" * 100)
    playground.flags_example()
    print("*" * 100)
    playground.capturing_groups()
    print("*" * 100)
    playground.meta_signs_remainder()
    print("*" * 100)
    playground.special_signs_remainder()
