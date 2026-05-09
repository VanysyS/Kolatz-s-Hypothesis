import time
import numpy as np
from numba import njit
from concurrent.futures import ThreadPoolExecutor

# Функція з відключеним GIL що рахує кроки до 1
@njit(nogil=True)
def dojob(numbers_chunk):
    size = len(numbers_chunk)
    chunk_steps = np.zeros(size)

    for i in range(size):
        smth = numbers_chunk[i]
        count = 0
        while smth != 1:
            count += 1
            if smth % 2 == 0:
                smth = smth // 2
            else:
                smth = 3 * smth + 1
        chunk_steps[i] = count

    return chunk_steps


if __name__ == '__main__':
    N = 10_000_000
    NUM_THREADS = 100 # кс-ть потоків
    numbers = np.random.randint(2, N, N) # Числа генеруються від 2 до N, а наступна N розмірність масиву
    start_time = time.time()

    # Розбиття масиву на рівні частини
    chunks = np.array_split(numbers, NUM_THREADS)
    futures = []

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        for chunk in chunks:
            futures.append(executor.submit(dojob, chunk)) # Викликає функцію dojob та закидує результат у futures

    # З'єднує всі futures
    all_steps = np.concatenate([f.result() for f in futures])

    end_time = time.time()
    # шукаю середнє як суму усіх кроків / на кількість чисел
    average = sum(all_steps) / N

    print(f"Перші 20 результатів для перевірки: {list(all_steps)}")
    print(f"Середня кількість кроків: {average}")
    print(f"Загальний час виконання: {end_time - start_time:.4f} секунд")