
from Gen_Algorithm import GAs
from individual import Individual

class Standard(GAs):
    

    def __init__(self):
        super(Standard, self).__init__()


    def execute(self, datafile):
        best_one = super().execute( datafile )
        super().print_result( best_one )
        

        return best_one


    def calculate_fitness(self, generation):
        for individual in generation:
            individual.fitness = super().calculate_individual_fitness(individual)
