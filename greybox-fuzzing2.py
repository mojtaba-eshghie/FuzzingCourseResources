#!/usr/bin/python3


class Seed(object):    
    def __init__(self, data):
        """Set seed data"""
        self.data = data
        
    def __str__(self):
        """Returns data as string representation of the seed"""
        return self.data
    __repr__ = __str__

class PowerSchedule(object):    
    def assignEnergy(self, population):
        """Assigns each seed the same energy"""
        for seed in population:
            seed.energy = 1

    def normalizedEnergy(self, population):
        """Normalize energy"""
        energy = list(map(lambda seed: seed.energy, population))
        sum_energy = sum(energy)  # Add up all values in energy
        norm_energy = list(map(lambda nrg: nrg/sum_energy, energy))
        return norm_energy
    
    def choose(self, population):
        """Choose weighted by normalized energy."""
        import numpy as np

        self.assignEnergy(population)
        norm_energy = self.normalizedEnergy(population)
        seed = np.random.choice(population, p=norm_energy)
        return seed

population = [Seed("A"), Seed("B"), Seed("C")]

schedule = PowerSchedule()
hits = {
    "A" : 0,
    "B" : 0,
    "C" : 0
}

# Let's see in 10000 trials how much each seed may be chosen to manipulate (mutate)
for i in range(10000):
    seed = schedule.choose(population)
    hits[seed.data] += 1

print(hits)