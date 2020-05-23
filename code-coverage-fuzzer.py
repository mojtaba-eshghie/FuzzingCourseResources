#!/usr/bin/python3

from fuzzingbook.Fuzzer import fuzzer
from fuzzingbook import *
from fuzzingbook.Coverage import Coverage, cgi_decode
import matplotlib.pyplot as plt

sample_string = fuzzer(15) 
print(sample_string)

def returnMaxCoverageSet():
    """
    Returns the maximum possible (best case) of coverage in an execution
    Acheived by giving the best input (input that is generated according to
    needs of certain branches to be met, so that they are going to be met as well.)
    """
    
    with Coverage() as max_coverage:
        # These three assertions (that call cgi_decode) will go through all three braches
        # that make up our most important part of function
        assert cgi_decode('+') == ' '
        assert cgi_decode('%20') == ' '
        assert cgi_decode('abc')  == 'abc'

        try:
            cgi_decode('%?a')
            assert False
        except ValueError:
            pass
    
    return max_coverage.coverage()
    

def execute_trials(trails=100):
    all_coverage = set()
    comulative_coverage = list()
    for trial in range(0, trails):
        string = fuzzer(15)
        with Coverage() as local_covage:
            try:
                cgi_decode(string)
            except:
                # just pass if the string has invalid sequence of chars, we just
                # want to find about the lines and eventually paths, not that what really happens (at this stage of testing)
                pass
        
        all_coverage |= local_covage.coverage()
        comulative_coverage.append(len(all_coverage))
        
    return comulative_coverage
    

def plot_the_coverage_CDF(comulative_coverage=[]):
    assert comulative_coverage is not []
    plt.plot(comulative_coverage)
    plt.title('Coverage of cgi_decode() with random inputs')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered')
    plt.show()


def execute_averaged_operations(runs_average = 10):
    all_results = list()
    for trial_number in range(1, 101):
        trial_results = []
        for i in range(0, 10):
            result = execute_trials()
            print(result)
            trial_results.append(result)
        all_results.append(trial_results)
    

    for trial_number in range(1, 101):
        temp = 0
        for i in range(0, 10):
            for j in range(0, 100):
                temp = all_results[i][j] + temp
            temp = temp / 10



'''
with Coverage() as cov:
    cgi_decode(sample_string)
print(cov.coverage())
'''



#plot_the_coverage_CDF(execute_trials())
execute_averaged_operations()




