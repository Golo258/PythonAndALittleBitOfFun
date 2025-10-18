import time

from jedi.inference.gradual.annotation import find_unknown_type_vars

from Logger import  logger

#------------------------------------
# Basics
# snake_case function with arguments
def calculate_total(price, tax):
    """
        Doc string as function documentation,
         arguments and return type
    :param price:
    :param tax:
    :return:
    """
    pass


# type hints - typowanie, czytelnośc i listing
def sub_total(average: int, amount: int) -> int:
    """
        Małe funkcje, jedna rzecz do zrobienia
        jeśli są efekty uboczne to pisać dokumentacje
        o tym
    """
    return average * amount

# domyślne wartości, tylko nie mutowalne
def append_item(item: str, items: list = None):
    if items is None:
        items = None
    items.append(item)
    return items

#------------------------------------

"""
    flexible arguments - *args, **kwargs
        * - pozycjonalne argumenty dowolnej liczby
        zbiera wszystkie dodatkowe argumenty pozycyjne w krotke
            np:
            log_message("INFO", "Como", "estas")
            to msgs - ("Como", "estas")
            
        ** - argmentu nazwane dowolne liczby
            zbiera wszystkie dodatkowe argumenty nazwane
            key=value w słownik
            np:
            log_message("INFO", "Como", user="John", code=450)
            to extra = {"user":"John", "code": 450}
            

"""
def log_messae(level, *msgs, **extra):
    print(level, *msgs, extra)

#------------------------------------

"""
  Keyowrd-only arguments 
    wymusza podanie nazwy argumentu po następnym arugmentcie
    jak dajemy * przed subject, to potem on musi być
    arugmentem nazwanym
    
"""
def send_email(to, *, subject="No subject", receiver="user@gmail.com"):
    pass

#------------------------------------

# send_email("fasfa", "aspfmapos") -> typeError
send_email(
    "anna",
    subject="any",
    receiver="you@tube.com"
)

"""

"""
from functools import wraps

from functools import lru_cache
"""
    LRU- Least Recently Used
    dekorator który pamieta wyniki wywołań funckji (cache)
    jesli cache sie zapłeni usuwa najrzadsze uzywane wyniki
    
    Funkcja nie musi liczyć tego samego wiele razy
    
"""


"""
     użyteczne biblioteki
        functools - dekoratory, cache, partial
        itertools - kombinatoryka, filtorwanie, mapowanie
        typing - typy, Union, Otional, Literal
        dataclasess - nowoczesny sposób na klasy 
        
"""
import functools
class FuncToolsExample(object):

    """
        Dekoratory:
            funkcja która opakowuje inne funkcje
            dodając do niej dodatkowe zachowanie
            bez zmieniania jej kodu
    """
    def runner(self):
        """
            prepare_multiply() zwraca funkcje z ustawionym paramerem
            (12) od razu wywołuje metode z ostatnim atrbutem
        """
        self.greet("Manny")
        self.get_users_data(1)  # Fetching data for 1
        self.get_users_data(1)  # z cache, już nic nie fetchuje
        logger.debug(self.prepare_multiply()(12))
        named_partial = self.prepare_named_multiply()
        logger.debug(named_partial(1))

        self.reduce_explanation()


    def log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling @{func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    def timer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            logger.info(f"{func.__name__} took {end - start:.4f} seconds")
            return result

        return wrapper

    @log
    @timer
    def greet(self, name):
        logger.info(f"Hello {name}")

    @functools.lru_cache(maxsize=32)
    @timer
    def get_users_data(self, user_id: int):
        print(f"Fetching data for {user_id}")
        return {"id": user_id, "name": f"User{user_id}"}

    def multiply(self, axis_x, axis_y):
        return axis_x * axis_y

    def prepare_multiply(self):
        """
            Partial przygotowuje poczatek funckji
            z jakimś poczatkowym agumentem
            Oczekuje funkcji, i po przecinku argumentów
        :return:
        """
        return functools.partial(
            self.multiply, 5
        )

    def prepare_named_multiply(self):
        named_multiply_axis_y = functools.partial(
            self.multiply, axis_y=12
        )
        return named_multiply_axis_y

    def count_example(self, previous_obj, next_obj):
        numbers = list()
        add_new_number = lambda word: {
            "name": word[:-1],
            "value": int(word[-1:])
        }
        if isinstance(previous_obj, str):
            numbers.append(add_new_number(previous_obj))
        else:
            numbers = previous_obj

        numbers.append(add_new_number(next_obj))
        return numbers

    def reduce_explanation(self):
        """
            bierze liste elementów
            składa je do jednej wartości
            Bierze sobie dwa argumenty, poprzednich i nastepnik
            a następnie wykonuje operacje zscalania
                np dodawnaie, odejmowanie, modyfikacja stringów

            reduce(function, iterable, initalizer=None)
        :return:
        """
        numbers = list(range(0,12))
        total = functools.reduce(
            lambda previous_nr, next_nr: previous_nr + next_nr,
            numbers,
            1
        )
        logger.info(total)
        # list of string explanation
        # liczenie

        words = ["one1", "two2", "three3", "four4"]
        words_dir = functools.reduce(
            self.count_example,
            words
        )
        print(f"Words dir: {words_dir}")

fun = FuncToolsExample()
fun.runner()