# dissimilarity.py

import numpy as np

# Return a frobenius matrix norm
def frobenius(matrix1, matrix2):
    a = matrix1 - matrix2

    summa = 0
    similarity = 0
    for row in a:
        for el in row:
            summa = summa + (el*el)

    dissimilarity = np.sqrt(summa)
    #dissimilarity = np.linalg.norm(a, 'fro')

    return dissimilarity