import pytest
from src.parser import CParser

@pytest.fixture
def parser():
    return CParser()

def test_nested_logic(parser):
    input_str = "void func() { if(1) { return; } }"
    result = parser.parse_string(chunk=input_str)
    assert len(result) == 1
    assert "void func()" in result[0]

def test_empty_input(parser):
    result = parser.parse_string(chunk="")
    assert len(result) == 0

def test_no_braces(parser):
    result = parser.parse_string(chunk="int x = 5;")
    assert result == []
