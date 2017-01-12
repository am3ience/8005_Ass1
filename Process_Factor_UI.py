# -----------------------------------------------------------------------------
# FUNCTION:       process_factoring
#
# DATE:           January 09, 2017
#
# DESIGNERS:      Paul Cabanez
#
# PROGRAMMERS:    Paul Cabanez
#
# NOTES:
#
#
#
#
#
# ----------------------------------------------------------------------------*/


import math
import time
import multiprocessing
import os
from Tkinter import *


def worker(nums, out_q):
    """ The worker function, invoked in a process. 'nums' is a
        list of numbers to factor. The results are placed in
        a dictionary that's pushed to a queue.
    """
    outdict = {}
    for n in nums:
        outdict[n] = primes2(n)
    out_q.put(outdict)

def primes2(n):
    primfac = []
    num = n
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            primfac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
        primfac.append(n)
    myfile = open('processresults.txt', 'a')
    myfile.write("\n" + str(num) + ":" + str(primfac) + "\n")
    return primfac

def process_factor():
    millis_start = int(round(time.time() * 1000))

    numbers = entry_1.get()
    nums = map(int, numbers.split())

    numbprocs = entry_2.get()
    nprocs = int(numbprocs)

    # Each process will get 'chunksize' nums and a queue to put his out
    # dict into
    out_q = multiprocessing.Queue()
    chunksize = int(math.ceil(len(nums) / float(nprocs)))
    procs = []

    for i in range(nprocs):
        p = multiprocessing.Process(target=worker, args=(nums[chunksize * i:chunksize * (i + 1)], out_q))
        procs.append(p)
        p.start()

    # Collect all results into a single result dict. We know how many dicts
    # with results to expect.
    resultdict = {}
    for i in range(nprocs):
        resultdict.update(out_q.get())

    # Wait for all worker processes to finish
    for p in procs:
        p.join()

    millis_end = int(round(time.time() * 1000))

    millis = millis_end - millis_start

    myfile = open('processresults.txt', 'a')
    myfile.write("it took " + str(millis) + " milliseconds to calculate the prime numbers.")

    text_1.insert(INSERT, resultdict)

    os.startfile("processresults.txt")

if __name__ == '__main__':

    root = Tk()
    root.title("Threads")

    label_1 = Label(root, text="Type in a list of number separated by spaces: ")

    entry_1 = Entry(root)

    label_2 = Label(root, text="Type in how many processes you want to run: ")

    entry_2 = Entry(root)

    button_1 = Button(root, text="Enter", command=lambda: process_factor())

    text_1 = Text(root)

    label_1.grid(row=0)
    label_2.grid(row=1)
    entry_1.grid(row=0, column=1)
    entry_2.grid(row=1, column=1)
    button_1.grid(row=1, column=2)
    text_1.grid(row=2, columnspan=3)

    root.mainloop()
