import itertools
import time
from itertools import zip_longest
from os import times

from sub_python_notes.logger import  logger

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
#-----------------------------------
"""
   ITERATOR -
       obiekt którego elementy można pobierać po kolei
       musi miec dwie metody:
           __iter__ - zwraca samego siebie (jest iterowalny)
           --next__ - zwraca kolejny element, rzuca StopIteration
"""
def iterator_example():
    numbers = iter([10, 20, 30])
    logger.debug(next(numbers))
    logger.debug(next(numbers))
    logger.debug(next(numbers))
    try:
        logger.debug(next(numbers))
    except StopIteration as si:
        logger.error(si)


"""
    GENERATOR - to iterator, któy pisze sie za pomocą yield w funckji
        to rodzaj iterator, prostrszy to stworzenia
        nie trzeba implementować funkcji iter i next
    Każdy generator jest iteratorem
"""
def generator_example():

    def simple_gen():
        yield 1
        yield "abc"
        yield True

    gen = simple_gen()
    logger.info(next(gen))
    logger.info(next(gen))
    logger.info(next(gen))
    # logger.info(next(gen)) Stop Iteration

"""
    ITERABLE - to obiekt po którym można iterować
        taki który potrafi utworzydc iteratora
            żeby coś było iterable musi mieć metode __iter__
        nie posiada __next - jest źródłem danych 
    Na przykłąd listy stringi słowniki tuple itp
"""
def iterable_example():
    listy= [1, 2, 3]
    stringi= "hello"
    tuple= (1, 2)
    dict= {"a": 1, "b": 2}
    sety= {1, 2, 3}

import itertools
class IterToolsLibExplanation(object):
    """
        Praca z listami, generatorami,iterowalnymi rzeczami
        itertools działa leniwie - generuje dane na bieżaco
            3 grupy funkcji:
            - nieskończone iteratory, lecą aż je zatrezymasz
            - skonczone iteratory - biorą coś i robią z tym dane rzecz
            - kombinatoryka - tworzyą permutacje, kombinacje itp

    """


    def infinity_iterator(self):
        # count
        for index in itertools.count(10, 2):
            logger.info(index)
            if index > 20:
                break

        # cicle - zapelta sekwencje
        for color in itertools.cycle(["red", "green", "blue"]):
            logger.debug(color)
            if color == "blue":
                break

        # repeat - potwarza wiele razy daną sekwencje
        # jesli nie podamy times to bedzie potwarzał w nieskonczoność
        for sequence in itertools.repeat("---", times=5):
            logger.debug(sequence)

    def finite_iterator(self):
        """
            chain(*iterables) - łączy kilka kolekcji
                -iterowalnych obiektów
            działa też na generatorach
        """
        for iter_obj in itertools.chain(
            [1, 2], ['a', 'b'], [True]
        ):
            logger.info(f"{iter_obj},Type: {type(iter_obj)}")

        """
            islice (iterable, start, stop, step)
                - lazy slice
            wycinanie jak w list[start:stop:step] 
                tylko że działa na dowolnym iteratorze
        """
        for obj in itertools.islice(itertools.count(), 5, 10):
            logger.debug(obj)

        """
            startmap(func, iterable_of_tuples)
                mapowanie argumentów wzgledem funkcji:
                map(), rozpakowuje krotki argumentów jako argumenty funkcji
                
                każdy argument musi byc krotką /listą
        """
        def multiply(a, b, c=None):
            if c:
                return a * b * c
            else:
                return a * b
        data = [(2, 3), (4, 5, 12), (6, 7)]
        logger.info(
            list(
                itertools.starmap(multiply, data)
            )
        )
        # lepszy przykład
        def format_price(name, price):
            return f"{name}: {price:.2f} zł"

        products = [("Jabłko", 1.99), ("Banan", 3.49), ("Kiwi", 4.25)]
        for line in itertools.starmap(format_price, products):
            logger.debug(line)

        """
            tee(itearble, n=2)
                tworzy n niezależnych iteratorów
                które czytają te same dane z jednego źródła (iterable)
                                
        """

        data = [1, 2, 3]
        a, b = itertools.tee(data)
        logger.info(list(a))
        logger.info(list(b))


        """
            zip_longest - jak zipowanie danych
                tylko nie konczy sie po krótszej liście
        """
        longest = [1, 2 ,3]
        shortest = ["a", "b"]
        logger.debug(
            list(itertools.zip_longest(
                longest, shortest, fillvalue='?#')
            )
        )

    def combinatorics_example(self):
        """
            produkt - wszystkie możliwe kobinacje elementów
            iloczyn kartezjański
        """
        logger.info(
            list(itertools.product([1, 2], ['a', 'b']))
        )
        """
            permutations(iterable, r=None)
            permutacje - wszystkie możliwe ułożenia elemnentów
        """
        logger.info(
            list(itertools.permutations("abc", 2))
        )
#--------------
fun = FuncToolsExample()
fun.runner()
#--------------
iterator_example()
generator_example()
#--------------
iter_tool_Lib = IterToolsLibExplanation()
iter_tool_Lib.infinity_iterator()
iter_tool_Lib.finite_iterator()
iter_tool_Lib.combinatorics_example()
#--------------
