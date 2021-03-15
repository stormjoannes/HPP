from typing import List
import threading
import logging
import time
import concurrent.futures
import random

def list_generator(lenList):
    shuffled_list = []
    for i in range(lenList):
        n = random.randint(0,999)
        shuffled_list.append(n)
    return shuffled_list


class mergeClass(object):
    def __init__(self, unsortedList: [int], workers: int):
        self.value = unsortedList
        self.dividable = workers
        self._lock = threading.Lock()
        self.workers = workers

    def merge(self, name, xs, status):
        """In place merge sort of array without recursive. The basic idea
        is to avoid the recursive call while using iterative solution.
        The algorithm first merge chunk of length of 2, then merge chunks
        of length 4, then 8, 16, .... , until 2^k where 2^k is large than
        the length of the array
        """
        logging.info(f"Thread %s: starting {status} ", name)

        unit = 1
        while unit <= len(xs):
            h = 0
            for h in range(0, len(xs), unit * 2):
                l, r = h, min(len(xs), h + 2 * unit)
                mid = h + unit
                # merge xs[h:h + 2 * unit]
                p, q = l, mid
                while p < mid and q < r:
                    # use <= for stable merge merge
                    if xs[p] <= xs[q]:
                        p += 1
                    else:
                        tmp = xs[q]
                        xs[p + 1: q + 1] = xs[p:q]
                        xs[p] = tmp
                        p, mid, q = p + 1, mid + 1, q + 1

            unit *= 2

        logging.info(f"Thread %s: finishing {status} ", name)

    def split(self):
        local_copy = self.value
        self.value = []

        while self.dividable > 0:
            indexPart = int(len(local_copy) / self.dividable)
            partOfList = local_copy[:indexPart]
            self.dividable -= 1
            local_copy = local_copy[indexPart:]
            self.value.append(partOfList)

    def join(self):
        """Merge sort merging function."""
        self.value = sum(self.value, [])
        self.merge('main', self.value, 'join')

def calcTime(begin, beginTime):
    if begin:
        beginTime = time.time()
        return beginTime
    else:
        endTime = time.time()
        return endTime - beginTime


amountWorkers = 8
len_random_list = 10000
unsortedList = list_generator(len_random_list)

if __name__ == "__main__":
    beginTime = calcTime(True, 0)

    currentList = mergeClass(unsortedList, amountWorkers)
    logging.info(f"Updating. Amount of cores: {amountWorkers}.")

    with concurrent.futures.ThreadPoolExecutor(max_workers=amountWorkers) as executor:
        currentList.split()
        for index in range(amountWorkers):
            executor.submit(currentList.merge, index, currentList.value[index], 'update')

    endTime = calcTime(False, beginTime)

    currentList.join()

    logging.info(f"Updating. Time in seconds: {endTime}\n")