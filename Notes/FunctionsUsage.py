import time

from Logger import  logger
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

"""
  Keyowrd-only arguments 
    wymusza podanie nazwy argumentu po następnym arugmentcie
    jak dajemy * przed subject, to potem on musi być
    arugmentem nazwanym
    
"""
def send_email(to, *, subject="No subject", receiver="user@gmail.com"):
    pass


# send_email("fasfa", "aspfmapos") -> typeError
send_email(
    "anna",
    subject="any",
    receiver="you@tube.com"
)

"""
    Dekoratory:
        funkcja która opakowuje inne funkcje 
        dodając do niej dodatkowe zachowanie
        bez zmieniania jej kodu
        
"""
from functools import wraps

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling @{func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper

@log
@timer
def greet(name):
    logger.info(f"Hello {name}")

greet("Manny")

from functools import lru_cache
"""
    LRU- Least Recently Used
    dekorator który pamieta wyniki wywołań funckji (cache)
    jesli cache sie zapłeni usuwa najrzadsze uzywane wyniki
    
    Funkcja nie musi liczyć tego samego wiele razy
    
"""
@lru_cache(maxsize=32)
@timer
def get_users_data(user_id: int):
    print(f"Fetching data for {user_id}")
    return {"id": user_id, "name": f"User{user_id}"}

get_users_data(1)  # Fetching data for 1
get_users_data(1)  # z cache, już nic nie fetchuje


"""
     użyteczne biblioteki
        functools - dekoratory, cache, partial
        itertools - kombinatoryka, filtorwanie, mapowanie
        typing - typy, Union, Otional, Literal
        dataclasess - nowoczesny sposób na klasy 
        
"""
