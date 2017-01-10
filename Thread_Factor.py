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
import datetime
import time
import multiprocessing


# returns the prime numbers of a given number (decomposition)
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
    myfile = open('threadresults.txt', 'a')
    myfile.write("\n" + str(num) + ":" + str(primfac) + "\n")
    return primfac




def threaded_factorizer(nums, nthreads):
    millis_start = int(round(time.time() * 1000))
    def worker(nums, outdict):
        """ The worker function, invoked in a thread. 'nums' is a
            list of numbers to factor. The results are placed in
            outdict.
        """
        for n in nums:
            outdict[n] = primes2(n)

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
    # print {k: v for out_d in outs for k, v in out_d.iteritems()}

    millis_end = int(round(time.time() * 1000))

    millis = millis_end - millis_start

    myfile = open('threadresults.txt', 'a')
    myfile.write("it took " + str(millis) + " milliseconds to calculate the prime numbers.")
    print "Finished!"

if __name__ == '__main__':

    threaded_factorizer((400243534500, 100345345000, 600034522000, 9000045346435345000), 4)
