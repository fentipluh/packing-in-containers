import numpy as np
import time

start = time.time()

def first_fit_decreasing(items, container_size):
    sorted_items = sorted(items, reverse=True)
    containers = []
    for item in sorted_items:
        for container in containers:
            if sum(container) + item <= container_size:
                container.append(item)
                break
        else:
            containers.append([item])
    return containers

read=open('item_size.txt')
items_sizes=np.loadtxt('items.txt')
n_items= int(read.readline())
container_size=int(read.readline())

containers = first_fit_decreasing(items_sizes, container_size)

for i, container in enumerate(containers):
    print(f"Контейнер {i+1}: {container}")

end = time.time() - start  ## собственно время работы программы

print(end)
