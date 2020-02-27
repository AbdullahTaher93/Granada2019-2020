

import os
import sys
import random
from copy import deepcopy

from individual import Individual


class GAs:
    

    def __init__(self):
        
    
        
        self.problem_size    = -1
        self.Array_of_Flow     = []
        self.Array_of_disances = []

        
        

        

        #save best generation
        self.bests = []

        self.GENERATION_SIZE       = 60
        self.NUMBER_OF_GENERATIONS = 100
        self.MAX_NUMBER_REPETITION_BEST_ONE = 20
        self.last_best_one = Individual(0)
        self.repetition_best_one = 0


    def load(self, filename):
       #load data and save Flows and distance
        self.filename = filename
        datafile = os.path.join('', self.filename)

        if os.path.isfile( datafile ):
            with open( datafile, 'r' ) as f:
                lines = f.readlines()
                lines = [line.split() for line in lines]
                lines = [list(map(int, line)) for line in lines if line != []] # avoids empty lines

                self.Size_Of_Problem = int(lines[0][0])

                assert(len(lines) == self.Size_Of_Problem*2+1) # checks the file has a correct structure

                self.Array_of_Flow = lines[1:self.Size_Of_Problem+1]
                self.Array_of_disances = lines[self.Size_Of_Problem+1:]

        else:
            raise FileNotFoundError("Cannot find file {}".format( datafile ))


    def Create_Generation(self):
    
        #Creates a generation with random indiniduals
        generation = []
        for i in range(self.GENERATION_SIZE):
            generation.append( Individual( self.Size_Of_Problem ) )

        return generation


    def binary_tournament(self):
        
        #selects 2 indeivduals from generation
        rand_numb1, rand_numb2 = random.sample(range(0, self.GENERATION_SIZE), 2)

        individ1 = self.current_generation[rand_numb1]
        individ2 = self.current_generation[rand_numb2]

        return min([individ1, individ2])


    def CrossOver_Of_Generation(self, parent1, parent2):
        
        slice_index = random.randint(1, self.Size_Of_Problem-1)

        child1_chrom = self.CrossOver_Of_Chromosomes(slice_index,
                                                  parent1.chromosomes,
                                                  parent2.chromosomes)
        child2_chrom = self.CrossOver_Of_Chromosomes(slice_index,
                                                  parent2.chromosomes,
                                                  parent1.chromosomes)

        assert(len(child1_chrom) == len(child2_chrom) == self.Size_Of_Problem)

        child1 = Individual( self.Size_Of_Problem )
        child1.chromosomes = child1_chrom

        child2 = Individual( self.Size_Of_Problem )
        child2.chromosomes = child2_chrom

        return child1, child2


    def CrossOver_Of_Chromosomes(self, slice_index, parent1, parent2):
        
        child = parent1[:slice_index]

        index = slice_index
        while len(child) < self.Size_Of_Problem:
            if parent2[index] not in child:
                child.append(parent2[index])

            index += 1
            if index >= self.Size_Of_Problem:
                index = 0

        return child


    def execute(self, datafile):
        
        print("Executing algorithm with file {}".format(datafile))

        self.load( datafile )

        self.current_generation = self.Create_Generation()
        self.Calculate_Fitness( self.current_generation )

        for i in range( self.NUMBER_OF_GENERATIONS ):
            print("Executing generation {}/{}... Best {}".format(i+1, self.NUMBER_OF_GENERATIONS, self.last_best_one.fitness), end="\r")

            new_generation = []
            for j in range( 0, int(self.GENERATION_SIZE), 2 ): # step = 2
                parent1 = self.binary_tournament()

                parent2 = None
                while parent1 != parent2:
                    parent2 = self.binary_tournament()

                child1, child2 = self.CrossOver_Of_Generation(parent1, parent2)

                child1.mutate()
                child2.mutate()

                new_generation.append( child1 )
                new_generation.append( child2 )

            
            old_best = min( self.current_generation )
            new_worst = max( new_generation )
            new_worst_index = new_generation.index( new_worst )
            new_generation.pop( new_worst_index )
            new_generation.append( old_best )
            self.current_generation = new_generation

            self.Calculate_Fitness( self.current_generation )

           
            best_one = min( self.current_generation )
            self.check_best_one_from_generation( best_one )

            self.bests.append(best_one)

        best_one = min( self.current_generation )
        return best_one


    def Calculate_Fitness(self, generation):
       
        raise NotImplementedError


    def calculate_individual_fitness(self, individual):
       
        new_fitness = 0
        for i in range(self.Size_Of_Problem):
            for j in range(self.Size_Of_Problem):
                chrom_i = individual.chromosomes[i]
                chrom_j = individual.chromosomes[j]

                new_fitness += self.Array_of_Flow[i][j] * \
                               self.Array_of_disances[chrom_i][chrom_j]

       
        return new_fitness


    def greedy_optimization(self, individual):
    
        S = deepcopy( individual )
        S.fitness = self.calculate_individual_fitness( S )

        best = deepcopy( S )

        for i in range( S.size ):
            for j in range(i + 1, S.size):
                T = deepcopy( S )
                T.chromosomes[i] = S.chromosomes[j]
                T.chromosomes[j] = S.chromosomes[i]

                self.Calculate_Fitness_after_swap( S, T, i, j )

                if T < S:
                    S = deepcopy( T )

        return S


    def Calculate_Fitness_after_swap(self, S, T, i, j):
        
        new_fitness = T.fitness
        chrom_S_i = S.chromosomes[i]
        chrom_S_j = S.chromosomes[j]
        chrom_T_i = T.chromosomes[i]
        chrom_T_j = T.chromosomes[j]

        for k in range(self.Size_Of_Problem):
            chrom_S_k = S.chromosomes[k]
            chrom_T_k = T.chromosomes[k]

            # recalculate i
            new_fitness -= self.Array_of_Flow[i][k] * \
                           self.Array_of_disances[chrom_S_i][chrom_S_k]

            new_fitness -= self.Array_of_Flow[i][k] * \
                           self.Array_of_disances[chrom_T_i][chrom_T_k]

            # recalculate j
            new_fitness -= self.Array_of_Flow[j][k] * \
                           self.Array_of_disances[chrom_S_j][chrom_S_k]

            new_fitness += self.Array_of_Flow[j][k] * \
                           self.Array_of_disances[chrom_T_j][chrom_T_k]

            # recalculate the rest of the values of the loop
            if k not in [i, j]:
                # recalculate i
                new_fitness -= self.Array_of_Flow[k][i] * \
                               self.Array_of_disances[chrom_S_k][chrom_S_i]

                new_fitness += self.Array_of_Flow[k][i] * \
                               self.Array_of_disances[chrom_T_k][chrom_T_i]

                # recalculate j
                new_fitness -= self.Array_of_Flow[k][j] * \
                               self.Array_of_disances[chrom_S_k][chrom_S_j]

                new_fitness += self.Array_of_Flow[k][j] * \
                               self.Array_of_disances[chrom_T_k][chrom_T_j]


    def check_best_one_from_generation(self, best_one):
        
        if best_one == self.last_best_one:
            self.repetition_best_one += 1
            if self.repetition_best_one > self.MAX_NUMBER_REPETITION_BEST_ONE:
                print("\nStuck population! Best one {}. Reinitialising...".format(best_one.fitness))
                self.reinitialise_population( best_one )
                self.repetition_best_one = 0

        else:
            self.repetition_best_one = 0

        self.last_best_one = best_one


    def reinitialise_population(self, best_one):
      
        self.current_generation = self.Create_Generation()
        self.Calculate_Fitness( self.current_generation )
        self.current_generation.pop(0)
        self.current_generation.append(best_one)


    def print_result(self, best_one):
        print("----------------------------------------------")
        print("Problem size: ", self.Size_Of_Problem)
        print("Number of generations: ", self.NUMBER_OF_GENERATIONS)
        print("Generation size: ", self.GENERATION_SIZE)
        print("Fitness of the final best individual: ", best_one.fitness)
        print("Chromosomes:\n", best_one.chromosomes )




