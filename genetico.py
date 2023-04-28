import random
import os
from mochila import BACKPACK

class CHROMOSOME:
#----- CONSTRUCTOR -----
    # SIZE  : cantidas de objetos
    def __init__(self,size) -> None:
        self.size            = size
        self.chromosome      = []

#----- GENERA '0,1' GENES AL CROMOSOMA -----
    def GegerateChromosome(self):
        self.chromosome = [random.randint(0,1) for i in range(self.size)]
        return self.chromosome
    

class GENETIC:
#----- CONSTRUCTOR -----
    # population_size    : Tamaño de la población
    # number_Generations : Numero de poblaciones generaciones
    # BACKPACKLIST       : lista de la mochila
    # WEIGHT             : PESO 
    # COSST              : calorias o costo
    def __init__(self,number_Generations,population_size,backpackList,weight,cosst,aprox) -> None:
        self.number_Generations = number_Generations
        self.population_size    = population_size
        self.backpackList       = backpackList
        self.weight             = weight 
        self.cosst              = cosst
        self.population         = []
        self.fitness            = []
        self.fitness2           = []
        self.aprox              = aprox

#----- GENERA TAMAÑO DE LA POBLACIÓN -----
    def GeneratePopulation(self):
        for i in range(self.population_size):
            chromosome           = CHROMOSOME(len(self.backpackList))
            chromosomesIndividuo = chromosome.GegerateChromosome()
            self.population.append(chromosomesIndividuo)

#----- ORDENAMIENTO DE MAYOR A MENOR -----
    def MajorMinor(self):
        self.fitness2 = sorted(self.fitness2, key=lambda fitness: fitness[1],reverse=True)

#----- ORDENAMIENTO DE MENOR A MAYOR -----
    def MinorMajor(self):
        self.fitness2 = sorted(self.fitness2, key=lambda fitness: fitness[0])

#----- OBTENER LA MEJOR MOCHILA VALIDADA POR EL PESO Y CALORIAS O COSTO -----
    def MinorBackPack(self):
        #proxweight    = self.weight - (self.weight * self.aprox)
        #proxcosst     = self.cosst - (self.cosst * self.aprox)
        self.fitness2 = []
        for chromosome in self.fitness:
            if (chromosome[1] <= self.weight and self.cosst <= chromosome[2]):
                self.fitness2.append(chromosome)

#----- OBTENEMOS LA MEJOR OPCIÓN DE LA POBLACIÓN -----
    def Fitness(self):
        """backpack     = BACKPACK(self.size,self.weight,self.fileTxt)
        backpack.ReadTxt()
        backpackList = backpack.Objects()"""
        sum_cost     = 0
        sum_weight   = 0
        self.fitness = []
        for chromosome in self.population:
            for i in range(len(chromosome)):
                if chromosome[i] == 1:
                    sum_cost   += int(self.backpackList[i][1]) 
                    sum_weight += int(self.backpackList[i][0])
            self.fitness.append([chromosome,sum_weight,sum_cost])
            sum_cost     = 0
            sum_weight   = 0

#----- REGRESA LA MEJOR OPCIÓN DE LA POBLACIÓN -----
    def GetFitness(self):
        return self.fitness2[0]
    
#----- MUTACIÓN DE LA NUEVA POBLACIÓN -----
    def Mutation(self):
        mutationRandom = random.randint(0,len(self.population)-1)
        for i in range(len(self.population)):
            if mutationRandom == i:
                for j in range(len(self.population[i])):
                    if self.population[i][j] == 1:
                        self.population[i][j] = 0
                    else:
                        self.population[i][j] = 1

#----- GENERAR CORTE DE CRUCE DE LOS CROMOSOMA y GENERAR LA NUEVA POBLACIÓN ------
    def NewPopulatio(self):
        counter       = 0
        newpopulation = []
        self.population = []

        if len(self.fitness) % 2 != 0:
            self.fitness.pop()

        while counter < len(self.fitness):
            if (counter % 2) == 0:
                cross = random.randint(2,len(self.fitness[0][0])-1)
                half1 = len(self.fitness[counter][0]) // cross
                half2 = len(self.fitness[counter+1][0]) // cross
                newpopulation.append(self.fitness[counter][0][:half1] + self.fitness[counter+1][0][half2:])
                newpopulation.append(self.fitness[counter+1][0][:half2] + self.fitness[counter][0][half1:])
            counter += 1
        self.population = newpopulation


def main():
    # population_size    : Tamaño de la población
    # number_Generations : Numero de poblaciones generaciones
    # WEIGHT             : Peso maximo de la mochila
    # FILETXT            : archivo txt
    population_size    = 500
    number_Generations = 200
    weight             = 80
    cosst              = 20
    fileTxt            = 'mochila.txt'
    generations        = 0
    rateMutation       = 0.1
    numberMutation     = int(rateMutation * population_size)
    aprox              = 0.3
    bestIndividuo      = []

    if (population_size % 2) == 0 and os.path.isfile(fileTxt):
        backpack     = BACKPACK(fileTxt)
        backpack.ReadTxt()
        backpackList = backpack.Objects()

        genetic = GENETIC(number_Generations,population_size,backpackList,weight,cosst,aprox)
        # SE GENERA LA PRIMERA POBLACIÓN
        genetic.GeneratePopulation()
        # SE PREPARA PARA OBTENER EL MEJOR DE LA POBLACIÓN
        genetic.Fitness()

        genetic.MinorBackPack()
        # ORDENAMOS DEL MEJOR AL MENOS MEJOR DE LA POBLACIÓN
        genetic.MinorMajor()
        genetic.MajorMinor()
        # REGRESAMOS EL MEJOR DE LA POBLACIÓN
        bestIndividuo.append([genetic.GetFitness(),generations])

        while generations < number_Generations-1:
            generations += 1
            # SE GENERA LA NUEVAS POBLACIONES
            genetic.NewPopulatio()
            # SE VERIFICA Y SE REALIZÁ LA TASA DE MUTACIÓN
            if numberMutation != 0:
                for i in range(numberMutation):
                    genetic.Mutation()
            # SE PREPARA PARA OBTENER EL MEJOR DE LA POBLACIÓN
            genetic.Fitness()

            genetic.MinorBackPack()
            # ORDENAMOS DEL MEJOR AL MENOS MEJOR DE LA POBLACIÓN
            genetic.MinorMajor()
            genetic.MajorMinor()
            # REGRESAMOS EL MEJOR DE LA POBLACIÓN
            bestIndividuo.append([genetic.GetFitness(),generations])
            # REALIZAMOS LA VALUACIÓN PARA OBTENER EL MEJOR DE LA POBLACIÓN
            bestIndividuo = sorted(bestIndividuo, key=lambda fitness: fitness[0][0][1])
            bestIndividuo = sorted(bestIndividuo, key=lambda fitness: fitness[0][0][2],reverse=True)
            # SE REMPLAZA O PERMANECE EL MEJOR INDIVIDUO DE LAS POBLACIONES
            bestIndividuo.pop()
        
        print('SOLUCIÓN:',bestIndividuo[0][0][0])
        print('PESO: ',bestIndividuo[0][0][1])
        print('COSTO: ',bestIndividuo[0][0][2])
        print('GENERACIÓN: ',bestIndividuo[0][1])
    else:
        print("ERROR: LA POBLACIÓN DEBE SER PAR O EL ARCHIVO NO EXISTE")


if __name__ == "__main__":
    main()









