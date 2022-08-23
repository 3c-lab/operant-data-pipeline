import pytest

import datetime

from ingestion.subject import Subject

def format_date():

    return ''

def test_format_comma_separated_string():
    # subject = Subject()

    str_val = Subject.format_multiple_values_into_array('Andrew,Yunyi')
    num_val = Subject.format_multiple_values_into_array('123456789,987654321')
    
    assert str_val == f"{{\"Andrew\",\"Yunyi\"}}"
    assert num_val == f"{{\"123456789\",\"987654321\"}}"

    print(str_val)
    print(num_val)

def test_format_date():

    date = datetime.datetime(2022, 1, 1)
    processed_date = Subject.format_date(date)

    assert processed_date == '01/01/2022 00:00:00'

    print(processed_date)



