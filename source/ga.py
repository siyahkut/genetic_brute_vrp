from mimetypes import init
from solver import *
from itertools import permutations
import threading
from dataclasses import dataclass
from problem import *
import random
import math
import queue


@dataclass
class Chromosome:
    jobRouteIndexes: list
    assignes: list


class GA:
    __slots__ = 'problem'
    minTotalDuration = math.inf
    bestRouteResult = []
    population = []
    nextPopulation = []
    iteration = 10
    mutationRate = 0.05

    @classmethod
    def solve(self, problem):
        threadCount = int(input(f'Threading count (default => 2):') or 2)
        initPopulationCount = int(
            input(f'Initial population (default => 200):') or '200')
        self.problem = problem

        self.initialPopulation(initPopulationCount)

        for i in range(self.iteration):
            print(f'iteration:{i}')
            logging.debug(f'iteration:{i}')
            self.nextPopulation = []
            q = queue.Queue()
            with q.mutex:
                q.queue.clear()
            for i in self.population:
                q.put(i)

            for i in range(threadCount):
                worker = threading.Thread(target=self.makeSelection, args=(
                    q,), daemon=True)
                worker.start()

            q.join()

            random.shuffle(self.nextPopulation)
            self.makeCrossover()
            self.makeMutation()
            self.population = self.nextPopulation

        logging.debug("total_delivery_duration %s", self.minTotalDuration)
        logging.debug("routes %s", self.bestRouteResult)
        print("total_delivery_duration :", self.minTotalDuration)    
        print("routes :", self.bestRouteResult)       
        self.problem.exportSolution();
        print("output filename :", problem.outputFileName)
        

    @classmethod
    def initialPopulation(self, populationCount):
        #[[9], [6], [3, 4, 7, 8, 5]]
        # self.population.append(Chromosome([9,6,3,4,7,8,5],[1,1,5]))
        for i in range(populationCount):
            self.population.append(self.makeRandomChromosome())

    @classmethod
    def makeSelection(self, que):
        #print("SelectioLENnextPopulation", len(self.nextPopulation))
        #print("SelectioLENpopulation", len(self.population))
        print("Selection")
        while not que.empty():
            print(que.qsize())
            chromosome1 = que.get()
            que.task_done()
            logging.debug("chromosome1 %s", chromosome1)
            chromosome1Result = self.problem.calculateRepresentation(
                chromosome1.jobRouteIndexes, chromosome1.assignes)
            chromosome1Fit = chromosome1Result["total_delivery_duration"]
            chromosome2 = que.get()
            que.task_done()
            logging.debug("chromosome2 %s", chromosome2)
            chromosome2Result = self.problem.calculateRepresentation(
                chromosome2.jobRouteIndexes, chromosome2.assignes)
            chromosome2Fit = chromosome2Result["total_delivery_duration"]

            if chromosome1Fit < chromosome2Fit:
                betterChromosome, betterChromosomeFit, betterChromosomeResult = chromosome1, chromosome1Fit, chromosome1Result
            else:
                betterChromosome, betterChromosomeFit, betterChromosomeResult = chromosome2, chromosome2Fit, chromosome2Result
             
            

            self.nextPopulation.append(betterChromosome)
           
            if betterChromosomeFit < self.minTotalDuration:
                self.minTotalDuration = betterChromosomeFit
                self.bestRouteResult = betterChromosome
                self.problem.setFinalSolution(betterChromosomeResult)

       
        print('Done makeSelection')

    @classmethod
    def makeCrossover(self):
        print("Crossover")
        for i in range(len(self.nextPopulation)):
            parent1 = self.nextPopulation[i]
            parent2 = self.nextPopulation[i+1]
            logging.debug("parent1 %s", parent1)
            logging.debug("parent2 %s", parent2)
            child = Chromosome([], [])
            crossOverPoints = random.choices(
                range(len(self.problem.jobIndexes)), k=2)
            crossOverPoints.sort()
            crossoverPoint1 = crossOverPoints[0]
            crossoverPoint2 = crossOverPoints[1]
            logging.debug("crossoverPoint1 %s", crossoverPoint1)
            logging.debug("crossoverPoint2 %s", crossoverPoint2)
            child.assignes = parent2.assignes
            count = 0
            for i in parent1.jobRouteIndexes:
                if(count == crossoverPoint1):
                    break
                if(i not in parent1.jobRouteIndexes[crossoverPoint1:crossoverPoint2]):
                    child.jobRouteIndexes.append(i)
                    count = count+1

            child.jobRouteIndexes.extend(
                parent2.jobRouteIndexes[crossoverPoint1:crossoverPoint2])
            child.jobRouteIndexes.extend(
                [x for x in parent1.jobRouteIndexes if x not in child.jobRouteIndexes])
            my_finallist = [i for j, i in enumerate(
                child.jobRouteIndexes) if i not in child.jobRouteIndexes[:j]]
            child.jobRouteIndexes = my_finallist
            self.nextPopulation.append(child)
            logging.debug("child %s", child)

    @classmethod
    def makeMutation(self):
        selectedChromosomes = random.choices(self.nextPopulation, k=round(
            len(self.nextPopulation)*self.mutationRate))

        # for i in selectedChromosomes:
        #     if i in self.nextPopulation:
        #         self.nextPopulation.remove(i)

        for i in selectedChromosomes:
            switchIndexes = random.choices(
                range(len(self.problem.jobIndexes)), k=2)

            i.assignes = random.choice(random.choice(
                self.problem.assignesPermutation))
            i.jobRouteIndexes[switchIndexes[0]], i.jobRouteIndexes[switchIndexes[1]
                                                                   ] = i.jobRouteIndexes[switchIndexes[1]], i.jobRouteIndexes[switchIndexes[0]]
            self.nextPopulation.append(i)

    def calculateFitness():
        pass

    @classmethod
    def makeRandomChromosome(self):

        randomAssign = random.choice(
            random.choice(self.problem.assignesPermutation))
        randomJobRoutesIndexes = random.sample(
            self.problem.jobIndexes, k=len(self.problem.jobIndexes))
        chromosome = Chromosome(randomJobRoutesIndexes, randomAssign)
        return chromosome
