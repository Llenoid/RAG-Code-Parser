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

def test_comment_with_brace(parser):
    code = """
    void start() {
        // This closing brace } should not end the function
        do_work();
    }
    """
    result = parser.parse_string(chunk=code)
    # If the parser is working, it should find 1 complete function.
    # If it's broken, it might find 0 (thinks the function is still open)
    # or 2 (if it split at the comment brace).
    assert len(result) == 1

def test_string_with_brace(parser):
    code = 'void log() { printf("Opening brace { is here"); }'
    result = parser.parse_string(chunk=code)
    assert len(result) == 1

def test_nested_complex_mess(parser):
    code = 'void f() { if(1){ printf("}"); } // } \n }'
    result = parser.parse_string(chunk=code)
    assert len(result) == 1

def test_multiline_comment(parser):
    code = """
    void complex() {
        /* { 
        */
        success();
    }
    """
    result =  parser.parse_string(chunk=code)
    assert len(result) == 1
