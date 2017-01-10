# -----------------------------------------------------------------------------
# FUNCTION:       thread_factoring
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
import multiprocessing


# returns the prime numbers of a given number (decomposition)
def primes(n):
    result = []
    for i in range(2, n + 1):  # test all integers between 2 and n
        s = 0;
        while n / i == floor(n / float(i)):  # is n/i an integer?
            n = n / float(i)
            s += 1
        if s > 0:
            for k in range(s):
                result.append(i)  # i is a pf s times
            if n == 1:
                return result


def threaded_factorizer(nums, nthreads):
    def worker(nums, outdict):
        """ The worker function, invoked in a thread. 'nums' is a
            list of numbers to factor. The results are placed in
            outdict.
        """
        for n in nums:
            outdict[n] = primes(n)

    # Each thread will get 'chunksize' nums and its own output dict
    chunksize = int(math.ceil(len(nums) / float(nthreads)))
    threads = []
    outs = [{} for i in range(nthreads)]

    for i in range(nthreads):
        # Create each thread, passing it its chunk of numbers to factor
        # and output dict.
        t = threading.Thread(
                target=worker,
                args=(nums[chunksize * i:chunksize * (i + 1)],
                      outs[i]))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Merge all partial output dicts into a single dict and return it
    # return {k: v for out_d in outs for k, v in out_d.iteritems()}
    print {k: v for out_d in outs for k, v in out_d.iteritems()}
    print chunksize

threaded_factorizer((400, 50, 60, 90), 2)