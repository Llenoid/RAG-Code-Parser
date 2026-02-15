import numpy as np
import numpy.typing as npt

class Searcher:
    def __init__(self, collections: npt.NDArray[np.float64]) -> None:
        self.collections = collections

    def search(self, query: npt.NDArray[np.float64]) -> np.intp:
        if self.collections.size == 0:
            return -1

        similarities = np.dot(self.collections, query)

        best_index = np.argmax(similarities)
        return best_index
