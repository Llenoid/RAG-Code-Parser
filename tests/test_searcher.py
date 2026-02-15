import numpy as np
from src.searcher import Searcher

def test_searcher_finds_most_similar():
    collection = np.array([[1.0, 0.0], [0.0, 1.0]])
    query = np.array([0.9, 0.1])

    searcher = Searcher(collection)
    best_index = searcher.search(query)

    assert best_index == 0

def test_searcher_exact_match():
    collection = np.array([[1.0, 0.0], [0.0, 1.0]])
    query = np.array([1.0, 0.0])

    searcher = Searcher(collection)
    best_index = searcher.search(query)

    assert best_index == 0

def test_searcher_negative_similarity():
    collection = np.array([[1.0, 0.0], [0.0, 1.0]])
    query = np.array([-1.0, 0.0])

    searcher = Searcher(collection)
    best_index = searcher.search(query)

    assert best_index == 1

def test_searcher_tie_breaker():
    collection = np.array([[0.0, 1.0], [0.0, 1.0]])
    query = np.array([0.0, 1.0])

    searcher = Searcher(collection)
    best_index = searcher.search(query)

    assert best_index == 0

def test_searcher_empty_collection():
    collection = np.array([]).reshape(0, 2)
    query = np.array([1.0, 0.0])
    
    searcher = Searcher(collection)
    best_index = searcher.search(query)
    
    assert best_index == -1
