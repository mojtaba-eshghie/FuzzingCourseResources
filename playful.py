#!/usr/bin/python3


from fuzzingbook import *
import random



class PoliceOfficer:
    def __init__(self, name='', age=17):
        assert name, 'Please give a full name to this officer'
        assert name.find(' ') is not -1, 'Please enter the full given name + family name'
        assert age >= 18, 'Sorry, you can join police after you get to 18'
    
    def setMaritalStatus(self, isMarried=False, hasChildren=False, numberOfChildren=0):
        assert numberOfChildren >= 0, 'Enter a value above or equal to zero'
        self.numberOfChildren = numberOfChildren
        self.isMarried = isMarried
        self.hasChildren = hasChildren
    
    def checkEverything(self):
        assert (self.numberOfChildren==0 and self.hasChildren is False) or (self.numberOfChildren > 0 and self.hasChildren is True)

    def registerOfficer(self):
        self.checkEverything()
        '''
        Now, here, you can add the registeration code!
        '''
        print('officer successfully resitered!')

newOfficer = PoliceOfficer('mojtaba esh', age=18)
newOfficer.setMaritalStatus()
newOfficer.registerOfficer()