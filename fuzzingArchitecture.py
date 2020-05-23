#!/usr/bin/python3
from functions import *
from fuzzingbook import *


'''
Runner Classes!
'''

# Runner base class
class Runner(object):
    # test outcomes
    UNRESOLVED = 'UNRESOLVED'
    FAILED = 'FAILED'
    PASS = 'PASS'

    def __init__(self):
        pass

    def run(self, input_):
        return (input_, Runner.UNRESOLVED)


class PrintRunner(Runner):
    def run(self, input_):
        '''
        Oracle!
        '''
        if '*' in input_:
            return (input_, Runner.PASS)
        else:
            return (input_, Runner.FAILED)


class Fuzzer(object):
    def __init__(self):
        pass

    def fuzz(self):
        '''return fuzzing input to the runner!'''
        '''
        Here we have separated the actual fuzzing test input generator from this fuction
        , because for each experiment we may need an specific generator, not just any random 
        input generator
        '''
        # for now let's just use the random input generator "fuzzer"
        fuzzing_input = fuzzer(max_length=10)
        return fuzzing_input
    
    def run(self):
        # for now let's just use print runner
        runner = PrintRunner()
        input_ = self.fuzz()
        result, outcome = runner.run(input_)
        return (result, outcome)
    
    def runTrial(self, trails=10):
        output = list()
        for i in range(0, 10):
            output.append(self.run())

        return output

myFuz = Fuzzer()
output = myFuz.runTrial(trails=7)
print(output)