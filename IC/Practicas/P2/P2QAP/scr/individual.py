import math
import random


class Individual:

    def __init__(self, size):
        self.INDIVIDUAL_MUTATION_PROBABILITY = 0.5
        self.GENE_MUTATION_PROBABILITY       = 0.05

        self.size    = size
        self.fitness = math.inf
        self.generate_random_chromosome( size )


    def generate_random_chromosome(self, size):
        self.chromosomes = list(range(size))
        random.shuffle(self.chromosomes)


    def mutate(self):
        if self.INDIVIDUAL_MUTATION_PROBABILITY > random.random():
            for chromosome in self.chromosomes:
                if self.GENE_MUTATION_PROBABILITY > random.random():
                    index1, index2 = random.sample(range(0, self.size), 2)
                    self.swap( index1, index2 )


    def swap(self, index1, index2):
        val1 = self.chromosomes[index1]
        val2 = self.chromosomes[index2]
        self.chromosomes[index1] = val2
        self.chromosomes[index2] = val1


    def __str__(self):
        return str(self.chromosomes)


    def __eq__(self, other):
        if not isinstance(other, Individual):
            return False

        equal_size = self.size == other.size
        equal_chrom = set(self.chromosomes) == set(other.chromosomes)

        return equal_size and equal_chrom


    def __lt__(self, other):
        if not isinstance(other, Individual):
            return False

        return self.fitness < other.fitness


    def __gt__(self, other):
        if not isinstance(other, Individual):
            return False

        return self.fitness > other.fitness
