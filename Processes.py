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

from math import floor
import math
import threading
import datetime
import time
from Queue import Queue

import multiprocessing

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
    myfile.write(str(num) + ":" + str(primfac) + "\n")
    return primfac

def mp_factorizer(nums, nprocs):
    def worker(nums, out_q):
        """ The worker function, invoked in a process. 'nums' is a
            list of numbers to factor. The results are placed in
            a dictionary that's pushed to a queue.
        """
        outdict = {}
        for n in nums:
            outdict[n] = primes2(n)
        out_q.put(outdict)

    # Each process will get 'chunksize' nums and a queue to put his out
    # dict into
    out_q = Queue()
    chunksize = int(math.ceil(len(nums) / float(nprocs)))
    procs = []

    for i in range(nprocs):
        p = multiprocessing.Process(
                target=worker,
                args=(nums[chunksize * i:chunksize * (i + 1)],
                      out_q))
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

    print resultdict

mp_factorizer((400243534500, 100345345000, 600034522000, 9000045346435345000), 4)