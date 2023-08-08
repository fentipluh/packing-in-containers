import numpy as np
from ortools.linear_solver import pywraplp
import time

start = time.time()

def solve_bin_packing(container_size, item_sizes):
    n_items = len(item_sizes)

    solver = pywraplp.Solver.CreateSolver('SCIP')

    # 1. Создаем переменные
    x = {}
    for i in range(n_items):
        for j in range(n_items):
            x[(i, j)] = solver.IntVar(0, 1, f'x_{i}_{j}')

    # 2. Создаем ограничения
    # 2.1. Каждый предмет должен быть упакован в один контейнер
    for i in range(n_items):
        solver.Add(sum(x[i, j] for j in range(n_items)) == 1)

    # 2.2. Размер контейнера не должен быть превышен
    for j in range(n_items):
        solver.Add(sum(x[i, j] * item_sizes[i] for i in range(n_items)) <= container_size)

    # 3. Создаем функцию цели
    objective = solver.Objective()
    for i in range(n_items):
        for j in range(n_items):
            objective.SetCoefficient(x[i, j], i)
    objective.SetMinimization()

    # 4. Решаем задачу
    status = solver.Solve()

    # 5. Выводим решение
    if status == pywraplp.Solver.OPTIMAL:
        containers = [[] for _ in range(n_items)]
        for j in range(n_items):
            for i in range(n_items):
                if x[(i, j)].solution_value() > 0:
                    containers[j].append(i)
        return [container for container in containers if container]
    else:
        return None

read=open('item_size.txt')
items_sizes=np.loadtxt('items.txt')
n_items= int(read.readline())
container_size=int(read.readline())

containers = solve_bin_packing(container_size, items_sizes)

if containers is not None:
    for i, container_items in enumerate(containers):
        print(f'Container {i}: {container_items}')
else:
    print('Could not find a solution')

end = time.time() - start  ## собственно время работы программы

print(end)