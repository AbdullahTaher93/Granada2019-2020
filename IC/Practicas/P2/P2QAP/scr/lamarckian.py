from Gen_Algorithm  import GAs
from individual import Individual


class Lamarckian(GAs):
  

    def __init__(self):
        super(Lamarckian, self).__init__()


    def execute(self, datafile):
        best_one = super().execute( datafile )
        super().print_result( best_one )
        
        return best_one


    def calculate_fitness(self, generation):
        counter=0
        for individual in generation:
            counter += 1
            print("individual {}/{}".format(counter, len(generation)))
            individual = super().greedy_optimization( individual )
