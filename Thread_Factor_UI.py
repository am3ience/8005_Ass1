# -----------------------------------------------------------------------------
# FUNCTION:       thread_factoring
#
# DATE:           January 09, 2017
#
# DESIGNERS:      Paul Cabanez
#
# PROGRAMMERS:    Paul Cabanez
#
# NOTES: program that utilizes threads to do mathematical computations
#
#
#
#
#
# ----------------------------------------------------------------------------*/

import math
import threading
import time
import os
from Tkinter import *


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

    # writes to the text file the results
    myfile = open('threadresults.txt', 'a')
    myfile.write("\n" + str(num) + ":" + str(primfac) + "\n")
    return primfac

# main function
def threads_factor():

    # gets beginning time of execution in milliseconds
    millis_start = int(round(time.time() * 1000))

    numbers = entry_1.get()
    nums = map(int, numbers.split())

    numbthreads = entry_2.get()
    nthreads = int(numbthreads)

    """ The worker function, invoked in a thread. 'nums' is a
    list of numbers to factor. The results are placed a list."""
    def worker(nums, outdict):

        for n in nums:
            outdict[n] = primes2(n)

    # Each thread will get a chunksize nums
    chunksize = int(math.ceil(len(nums) / float(nthreads)))
    threads = []
    outs = [{} for i in range(nthreads)]

    for i in range(nthreads):
        # Create each thread, passing it its chunk of numbers to factor
        t = threading.Thread(target=worker, args=(nums[chunksize * i:chunksize * (i + 1)], outs[i]))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # gets end time of execution  in milliseconds
    millis_end = int(round(time.time() * 1000))

    # minus the end and start time for overall time to run the code
    millis = millis_end - millis_start

    # write to the text file how long it took
    myfile = open('threadresults.txt', 'a')
    myfile.write("it took " + str(millis) + " milliseconds to calculate the prime numbers.")

    text_1.insert(INSERT, {k: v for out_d in outs for k, v in out_d.iteritems()})

    os.startfile("threadresults.txt")

if __name__ == '__main__':

    # UI code
    root = Tk()
    root.title("Threads")

    label_1 = Label(root, text="Type in a list of number separated by spaces: ")

    entry_1 = Entry(root)

    label_2 = Label(root, text="Type in how many threads you want to run: ")

    entry_2 = Entry(root)

    button_1 = Button(root, text="Enter", command=lambda: threads_factor())

    text_1 = Text(root)

    label_1.grid(row=0)
    label_2.grid(row=1)
    entry_1.grid(row=0, column=1)
    entry_2.grid(row=1, column=1)
    button_1.grid(row=1, column=2)
    text_1.grid(row=2, columnspan=3)

    root.mainloop()
