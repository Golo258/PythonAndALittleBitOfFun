


"""
    Uruchamianie testów:
        z danego pliku: 
            pytest tests/test_example.py
            
        konkretnego testu:
            pytest test_file.py::nazwa_testu
            
            
        wszystkich testów z klasy:
            pytest tests/test_example.py::TestMath
            
    pytest -v tests/test_example.py
        -verbose - dokładniejsze logi co sie dzieje
        -s - pokazuje logi
        
        albo jak całość z logging
        --log-cli-level=DEBUG        

"""
import pytest
import logging
import tempfile
import os

def test_addition():
    # Arrange
    a, b = 2, 3
    # Act
    result = a + b
    # Assert
    assert result == 5
    

"""
    Przechwytywanie wyjątków
    def test_raise_division():
        with pytest.raises(Exception):
            funckcja(params)
"""

def div(a, b):
    return a / b

def test_raise_zero_division():
    logging.debug("SIemano")
    with pytest.raises(ZeroDivisionError):
        div(1,0)

"""
    Assertowanie zmiennych w testach:
        assert result == 5
            != różne 
             i inne operacje liczbowe
             
    Marek, jak ja go lubie
    parametryzacja -- jedna funkcja <-> wiele przypadków
        dodanie wielu scenariuszy
"""

@pytest.mark.parametrize("value, expected", [
    (2, 5),
    (3,12),
    (0,5)
])
def test_sum_param(value, expected):
    assert isinstance(value, int)
    assert value != expected
    assert expected >= value
    
#  skippowanie testu
@pytest.mark.skip(reason="test is not ready yet")
def test_not_ready():
    assert False
    
# test możę ale nie musi sie wywalić
@pytest.mark.xfail(reason="bug can occured in function sum()")
def test_known_bug():
    assert 1 + 1 == 3
    
"""
# grupowanie testów slow / db /api
@pytest.mark.slow
def test_big_data():
    logging.debug("Only big data in here")
    # python -m slow
"""

@pytest.fixture
def example():
    logging.error("example")

""" 
    czyli dana fixtura wykona sie przed danym testem
    wykonuje sie przed testem np połączenie z bazą czy inne 
    nie używamy fixtury jako zmienna albo coś jako parametr tylko cos 
    sie wykonuje przed -- cos co jest zdefinowane w fixture
"""
@pytest.mark.usefixtures("example")
def test_show_example():
    logging.debug("before example")
    
"""
    Fixture:
        przygotowywanie wcześniej danych do testu
            np: utworzenie pliku, połączenie do bazy, ustawienie zmiennej
        tworzenie:
            @pytest.fixtuire
            
        można łączyć je jak w tym przykładzie 
            db_path → db_file → db_connection → user_repo.
        domyślnie fixture działą per test - tworzy sie od nowa dla każdego testu
        
        fixture(scope=) / ustawia zasieg 
            function - nowe przy kadzym tescie
            module - nowe dla całego modułu
            session - raz na całą sesje pytest -wszystkie testy
            
        @pytest.fixture(params=[1, 2, 3])
            tak samo jak parametirse
            
        autouse=True -- automatycznie attachuje do wszystkich testów
"""

@pytest.fixture
def ue_db_path():
    return os.path.join(tempfile.gettempdir(), "ue.db")

@pytest.fixture
def db_text_file(ue_db_path):
    with open(ue_db_path, "w") as db_file:
        db_file.write("ue=1..10")
        return db_file.name
    
    
def test_connection(db_text_file):
    logging.debug(db_text_file)
    with open(db_text_file) as file:
        content = file.read()
        
    assert content == "ue=1..10"
    
# params
@pytest.fixture(params=[1,2,3]) # kilka razy dla każdej wartości z listy
def number(request):
    return request.param

def test_is_positive(number):
    assert number > 0
    
"""
    yield normalnie
        funkcja staje sie generatoem
        nie oddaje od razu wszystkie, 
        daje 1 na poczatku i potem funckja sama musi sobie albo to zabrać
        poprzez iteracje albo poprzez next()

    yield w tescie:
        1. przed yieldem - jest setup testu - przygotowanie danych
        2. yield cos - oddaje dane przygotowane do testu
        3. po yieldzie - teardown - sprzatnie po teście
        

"""
def numbers():
    yield 1
    yield 2 
    yield 3

def test_show_numbers():
    for number in numbers():
        logging.debug(f"{number=}")    
    

class Customer:
    
    def __init__(self, name, records):
        self.name = name
        self.records = records
    
    def __str__(self):
        return f"Customer: {self.name}, {self.records}"
        

@pytest.fixture
def make_customer_record():
    
    # setup
    created_records = []
    
    def _make_record(customer_name):
        record = Customer(customer_name, [])
        created_records.append(record)
        return record
    
    # passing to test
    yield _make_record
    
    # cleanup - teardown
    for record in created_records:
        created_records.remove(record)
        logging.debug(f"removing: {record}")
        
def test_customer_records(make_customer_record):
    customer_1 = make_customer_record("Lisa")
    customer_2 = make_customer_record("Mike")
    customer_3 = make_customer_record("Meredith")
    
    assert [c.name for c in (customer_1, customer_2, customer_3)] == ["Lisa", "Mike", "Meredith"]
    assert all(isinstance(c.records, list) and not c.records for c in (customer_1, customer_2, customer_3))
    
# mockowanie unittest.mock -- o co w tym chodzi
"""
    Podmiana realnej funckji która coś robi
        np: otwiera baze danych | robi request do APi
        i trwa ona długo lub ma realne skutki
    
    na sztuczną wersje (mock) - która zachowuje sie jak chcesz
    unittest.mock - standardowa biblioteka 
    
    patch -- tymczasowa podmiana obiektu
    Mock - obiekt udający coś innego
    MagicMock - jak Mock, ale ogarnia wiecej rzeczy automatycznie 
"""
# przykladowa funkcja do przetestowania
import requests
def get_status(url):
    response = requests.get(url)
    logging.debug(f"{response=}")
    logging.debug(f"{response.status_code=}")
    return response.status_code

from unittest.mock import patch

def test_get_status():
    with patch("requests.get") as mock_get: # podmienia funkcje request.get
        mock_get.return_value.status_code = 200 # mowi co ma robić
        #mock_get to jest uchwyt do mocka - obiektu podmianki
        #return_value to to co zwróci funkcji request.get()
        # co można jeszcze zrobić oprócz return value
        
        # symulowanie wyjatku
        # mock_get.side_effect = requests.exceptions.Timeout        
        assert get_status("https://example.com")

# test bez mocka musiałby realnie coś sciągnąć z neta


# debuowanie testów 
