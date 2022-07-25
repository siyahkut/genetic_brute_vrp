from solver import *
from itertools import permutations
import threading
import queue
import math

class Brute:
    __slots__ = 'problem'
    minTotalDuration = math.inf;
    bestRouteResult = []

    @classmethod
    def solve(self, problem):

        

        self.problem = problem
        jobIndexes = problem.jobIndexes

        jobRouteIndexesPermutations = list(permutations(jobIndexes))

        threadCount = int(input(f'Threading count (default => 2):') or 2)
        q = queue.Queue()
        for i in jobRouteIndexesPermutations:
            q.put(i)

        for i in range(threadCount):
            worker = threading.Thread(target=self.runCalculation, args=(
                q,), daemon=True)
            worker.start()

        q.join()
        
        logging.debug("total_delivery_duration %s", self.minTotalDuration)
        logging.debug("routes %s", self.bestRouteResult)
        print("total_delivery_duration :", self.minTotalDuration)    
        print("routes :", self.bestRouteResult)       
        self.problem.exportSolution();
        print("output filename :", problem.outputFileName)

    @classmethod
    def runCalculation(self, que):
        while not que.empty():
            #print(".", " ", ".")
            # print("...")
            print(que.qsize())
            jobRouteIndexes = que.get()
            for assignes in self.problem.assignesPermutation:
                for assign in assignes:
                    assignResult = self.problem.calculateRepresentation(
                        list(jobRouteIndexes), assign)
                    if assignResult["total_delivery_duration"] < self.minTotalDuration:
                        self.minTotalDuration = assignResult["total_delivery_duration"]
                        self.bestRouteResult = assignResult["routes"]
                        self.problem.setFinalSolution(assignResult);

            que.task_done()
       
