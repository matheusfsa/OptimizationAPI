class EvolutionaryAlgorithm(object):

    def createInitialPopulation(self):
        raise NotImplementedError("Should have implemented this")

    def evaluatePopulation(self):
        raise NotImplementedError("Should have implemented this")

    def isStoppingConditionReached(self):
        raise NotImplementedError("Should have implemented this")

    def selection(self):
        raise NotImplementedError("Should have implemented this")

    def reproduction(self):
        raise NotImplementedError("Should have implemented this")

    def replacement(self):
        raise NotImplementedError("Should have implemented this")

    def initProgress(self):
        raise NotImplementedError("Should have implemented this")

    def updateProgress(self):
        raise NotImplementedError("Should have implemented this")

    def execute(self):
        population = self.createInitialPopulation()
        fitness = self.evaluatePopulation(population)
        self.initProgress()
        while not self.isStoppingConditionReached():
            mating_population = self.selection(population, fitness);
            offspring_population = self.reproduction(mating_population);
            offspring_population, fitness_offspring = self.evaluatePopulation(offspring_population);
            population = self.replacement(population, fitness, offspring_population, fitness_offspring);
            self.updateProgress()