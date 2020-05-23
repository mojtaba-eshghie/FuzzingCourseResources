#!/usr/bin/python3

'''
we either have error codes or exception errors!
'''
from functions import fuzzer
from fuzzingbook.ExpectError import ExpectError
import random
import fuzzingbook




secrets = ("<space for reply>" + fuzzer(100)
     + "<secret-certificate>" + fuzzer(100)
     + "<secret-key>" + fuzzer(100) + "<other-secrets>")


uninitialized_memory_marker = "deadbeef"
while len(secrets) < 2048:
    secrets += uninitialized_memory_marker


with ExpectError():
    for i in range(10):
        #s = fuzzingbook.heartbeat(fuzzer(), random.randint(1, 500), memory=secrets)

        '''
        This assersion is added to check if there is not going to be any  access
        to the places of the memory that is not initialized (if such an access is happens,
        it means that other probably important parts are already read, since the uninitialized
        parts are at the end of everything here)
        This assersion is more inclusive than the next one (in our case)
        '''
        #assert not s.find(uninitialized_memory_marker)

        '''
        The intuition here is to find the places of the memory that should not be
        spit out to the person sending request to this function, so we mark them by
        something, and before returning anything to the requester we try to detect if we have
        indeed accessed one of these regions)
        '''
        #assert not s.find("secret")


myList = ['mojtaba', 'mahshid', 'leyla']
repr(myList)
print(myList)



