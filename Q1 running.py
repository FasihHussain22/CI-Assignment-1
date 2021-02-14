import random

f = open("TSP data Qatar.txt", "r")
locations = {}
# locations = {1: (0,0), 2: (2,0), 3: (0,2), 4: (2,2), 5: (0,0), 6: (0,0), 7: (0,0)}

for x in f.readlines():
    temp = x.split()
    locations[int(temp[0])] = (float(temp[1]), float(temp[2]))
f.close()

class Individual:
    def __init__(self, size: int, sequence=None):
        """Creates a list of the given size, optionally intializing elements to value.

        Args:
        - size: number of items in gnome
        - sequence: a particular sequence, if it is not provided than a random sequence is initialized

        Returns:
        none
        """
        if sequence == None:
            self.gnome = list(range(1, size+1))
            random.shuffle(self.gnome)
        else:
            self.gnome = sequence
        self.fitness = 0
        for x in range(len(self.gnome)-1):
            self.fitness+=((locations[self.gnome[x]][0]-locations[self.gnome[x+1]][0])**2+(locations[self.gnome[x]][1]-locations[self.gnome[x+1]][1])**2)**0.5
        self.fitness += ((locations[self.gnome[0]][0]-locations[self.gnome[-1]][0])**2+(locations[self.gnome[0]][1]-locations[self.gnome[-1]][1])**2)**0.5

    def getFitness(self):
        """Returns the fitness of the gnome.

        Args:

        Returns:
        fitness of gnome
        """
        return self.fitness
    
    @staticmethod
    def crossover(parent1, parent2, mutation: float):
        """Returns an individual produced as the result of crossover

        Args:
        - parent1: an individual
        - parent2: an individual
        - mutation: probability of mutation

        Returns:
        Individual produced from crossover
        """
        child = list(parent1.gnome)
        randomNumber = random.randint(0,len(parent1.gnome)-1)
        for x in range(len(parent1.gnome)//2):
            child[(randomNumber+x)%len(parent1.gnome)] = -1
        count = 0
        i = 0
        while count != len(parent1.gnome)//2:
            if parent2.gnome[(randomNumber+i)%len(parent1.gnome)] not in child:
                child[(randomNumber+count)%len(parent1.gnome)] = parent2.gnome[(randomNumber+i)%len(parent1.gnome)]
                count += 1
            i += 1
        if mutation > random.uniform(0,1):
            index1 = random.randint(0,len(child)-1)
            index2 = random.randint(0,len(child)-1)
            child[index1], child[index2] = child[index2], child[index1]
        child = Individual(len(child), child)
        return child
    
    def __str__(self):
        """String representation of an individual

        Args:

        Returns:
        String representation of an individual
        """
        return "Fitness: "+str(round(self.fitness,2))+"\n"+" ".join([str(x) for x in self.gnome])

class EA:
    def __init__(self, size: int):
        """Initialize the population of the given size

        Args:
        - size: number of individuals in the population

        Returns:
        none
        """
        self.population = []
        for x in range(size):
            self.population.append(Individual(len(locations.keys())))
        # for x in self.population:
        #     print(x)
    
    def getAverageFitness(self):
        """Returns the average fitness of the population

        Args:

        Returns:
        average fitness of population
        """
        return round(sum(x.getFitness() for x in self.population)/len(self.population), 2)
    
    def getBestFitness(self):
        """Returns the best fitness of the population

        Args:

        Returns:
        best fitness of population
        """
        return round(min(x.getFitness() for x in self.population), 2)
    
    def selectionScheme(self, n, scheme):
        """Selects the parents for crossover

        Args:
        - n: number of selected parents
        - scheme: selection scheme for selecting parents
                - 1: Fitness Proportional Selection
                - 2: Rank Based Selection
                - 3: Binary Tournament
                - 4: Truncation
                - 5: Random
        
        Returns:
        returns n individuals of the population
        """
        selected = []
        if scheme == 1:
            totalFitness = 0
            maxFitness = -1
            minFitness = -1
            for x in self.population:
                totalFitness += x.getFitness()
                if x.getFitness() > maxFitness:
                    maxFitness = x.getFitness()
                if x.getFitness() < minFitness or minFitness == -1:
                    minFitness = x.getFitness()
            totalFitness = (maxFitness + minFitness)*len(self.population) - totalFitness
            # temp = []
            # for x in self.population:
            #     temp.append(maxFitness+minFitness-x.getFitness())
            # totalFitness = sum(temp)
            # print("Total Fitness:", totalFitness)
            for x in range(n):
                randomNumber = random.uniform(0,1)
                # randomNumber = 0.96
                currentSum = 0
                i = 0
                while currentSum < randomNumber:
                    currentSum += (maxFitness + minFitness - self.population[i].getFitness())/totalFitness
                    i += 1
                # print(i)
                selected.append(self.population[i-1])
        elif scheme == 2:
            totalRank = len(self.population)*(len(self.population)+1)/2
            temp = sorted(self.population, key=lambda x: x.getFitness())
            for x in range(n):
                randomNumber = random.uniform(0,1)
                # randomNumber = 0.946
                currentSum = 0
                i = 0
                while currentSum < randomNumber:
                    currentSum += (len(self.population)-i)/totalRank
                    i += 1
                # print(i-1)
                selected.append(temp[i-1])
        elif scheme == 3:
            # Select two using FPS then select the better one among them
            pass
        elif scheme == 4:
            selected = sorted(self.population, key=lambda x: x.getFitness())[:n]
        elif scheme == 5:
            for x in range(n):
                selected.append(self.population[random.randint(0,len(self.population)-1)])
        return selected
    
    def train(self, parentScheme, survivorScheme, mutation, offsprings, generations):
        print("Generation No.: 0","\t\tBSF:",self.getBestFitness(),"\t\t\tASF:",self.getAverageFitness())
        for x in range(generations):
            parents = self.selectionScheme(2*offsprings, parentScheme)
            for y in range(offsprings):
                self.population.append(Individual.crossover(parents[2*y], parents[2*y+1], mutation))
            self.population = self.selectionScheme(len(self.population)-offsprings, survivorScheme)
            print("Generation No.:",x+1,"\t\tBSF:",self.getBestFitness(),"\t\t\tASF:",self.getAverageFitness())


a=EA(30)
# a.population[0].fitness = 10.25
# a.population[1].fitness = 35.56
# a.population[2].fitness = 58.16
# a.population[3].fitness = 197.3
# a.population[4].fitness = 138.1
# a.population[5].fitness = 164.66
# a.population[6].fitness = 26.52
# a.population[7].fitness = 138.57
# a.population[8].fitness = 205.55
# a.population[9].fitness = 167.21
# a.selectionScheme(1,2)
a.train(4, 4, 0.5, 10, 100)