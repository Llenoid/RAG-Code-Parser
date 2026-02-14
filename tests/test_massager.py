from pandas import DataFrame
import pytest
from src.parser import CParser
from src.massager import DataMassager

@pytest.fixture
def parser():
    return CParser()

def get_chunks():
    chunks = [
    "int calculate_sum(int a, int b) { return a + b; }",
    "int get_x(){return x;}",
    "void clear(){}",
    "void process() { if(true) { do_thing(); } else { stop(); } }"
    ]
    return chunks

def test_massager_filters_short_functions():
    chunks = get_chunks()
    massager = DataMassager(chunks)

    massager.to_dataframe()
    massager.clean()
    massager.add_metadata()
    data_frame = massager.df

    expected_count = 3
    assert len(data_frame) == expected_count
    assert "token_count" in data_frame.columns
    assert "calculate_sum" in data_frame["text"].iloc[0]
