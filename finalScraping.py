"""import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import multiprocessing

def square(n):
    return n * n

def cube(n):
    return n * n * n

if __name__ == "__main__":
    numbers = [1, 2, 8 ]
    pool = multiprocessing.Pool(processes=2)  # Create a pool of 2 processes

    results = []
    results1 = []

    # Apply the square and cube functions to each number
    for n in range(2):
        result_square = pool.apply_async(square, (n,))
        result_cube = pool.apply_async(square, (n,))
        
        results = result_square.get()
        results1 = result_square.get()
        results2 = result_square.get()

    pool.close()
    pool.join()

    # Remove duplicates from results and results1
    numbers = list(set(numbers + results + results1))

    print(results)
    print(results1)
    print(numbers)
    """
import multiprocessing
import random

def square(n):
    return (n * n * n) + random.random()

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 4)
    
    results = []
    for n in range(4):
        result = pool.apply_async(square, (n,))
        results.append(result)

    result = [res.get() for res in results]
    result1 = result[0]
    result2 = result[1]
    result3 = result[2]
    result4 = result[3]

    pool.close()
    pool.join()
    
    print(result)
    print(result1)    
    print(result2)    
    print(result3)    
    print(result4)