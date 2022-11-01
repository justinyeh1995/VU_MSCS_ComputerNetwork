

####################################################

# Author: Aniruddha Gokhale

# Vanderbilt University

# Created: Fall 2022

#

# Purpose:

# To show how we might start timers for each packet of our sliding window and then

# stop the timer before it expires for packets whose ACK is received before timer expiry

#

####################################################

#

# In this code we use concurrent.futures to exploit asynchronous execution of callables

# Using futures, we create as many threads as the size of the Sliding Window. Within

# that thread, we could have used a time.sleep () call to simulate a timer but once

# started, there is no way to cancel it. So we instead use threading.Event and issue

# a wait () call on it.

#

import time

import concurrent.futures

from threading import Event

import random

​

####################################################

#  timer method

####################################################

def timer (ev, seq, timeout):

  # This is our callable method invoked when the submit method of futures is invoked

  # The ev parameter is the Event on which the wait is invoked for the desired timeout

  # seq is our sequence number

  print ("Timer for seq: {} sleeping for {} seconds".format (seq, timeout))

  start_time = time.time ()

  ev.wait (timeout)

  elapsed_time = time.time () - start_time

  # Here we print how much time has elapsed (just as a debugging output to check

  # that in some cases the timer is cancelled early)

  print ("seq {}'s timer method ended after {} seconds".format (seq, elapsed_time))

​

  # return the seq number

  return seq, elapsed_time

​

###############################################

# Main part of the code

###############################################

​

​

# Note that this code in reality is not doing any networking code. But we are

# making it look like this sort of logic can be used in the timer handling

​

WINDOW_SIZE = 5

# create as many event objects as window size

event_list = [Event () for i in range (WINDOW_SIZE)]  

​

# Now, create as many concurrent threads as the window size.  The example in

# the Python documentation says that using the "with" stmt as below

# helps ensure threads are cleaned up properly. We use ThreadPoolExecutor and

# not a ProcessPoolExecutor

with concurrent.futures.ThreadPoolExecutor (max_workers=WINDOW_SIZE) as executor:

  print ("Invoke submit with {} workers".format (WINDOW_SIZE))

  # The submit method returns a future obj which can be queried for results.

  # The first param to submit is the function to execute followed by as many

  # arguments we needed to send. Here we invoke the timer method, and then

  # pass individual event objects that we created above for a fake packet with

  # monotonically increasing sequence numbers

  #

  # What is returned below is a dictionary object with sequence of tuples <future, seq>

  future_objs = {executor.submit (timer, event_list[seq], seq, 20): seq for seq in range (WINDOW_SIZE)}

​

​

  # Now think as if we are sending as many packets as our window size to our server

  # and then wait to receive ACKs. To mimic this behavior, we just sleep for a short

  # amount of time compared to the timer.

  print ("Starting local timer to mimic sending and waiting for reply to show up")

  time.sleep (5)

​

  # Now use random number logic to mimic delayed/lost ACK. For others, we

  # stop their corresponding timer. Say 3 of 5 ACKS received in time.

  # What we get below is a subset of the event list. Everything in this subset, we

  # cancel the timer.

  ev4acks_rcvd = random.sample (event_list, k=3)

​

  # now cancel timers for acks received

  print ("Main thread woken up; let us cancel timers for successful acks received")

  for ev in ev4acks_rcvd:

    ev.set ()  # the set method lets the waiting event object to cancel the wait

​

  # We will see below that some futures are completed because their callable function

  # returns after cancelling the timer. Others will return after the entire timeout is over

  for future in concurrent.futures.as_completed(future_objs):

    seq = future_objs[future]  # since this is a dictionary, we use the key to get the val

    try:

      data = future.result()  # obtain the return value of the callable which are actually

                                         # two values: the seq num and the elapsed time. From this

                                         # we know which timers were cancelled and which expired

                                         # due to no ACK received.

    except Exception as exc:

      print('%r generated an exception: %s' % (seq, exc))

    else:

      print ("after completion, seq = {}, elapsed time in timer method = {}".format (data[0], data[1]))


