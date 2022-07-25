import json
from utils import *
from itertools import permutations
import os
class Problem:
    __slots__ = 'details'
    jobIndexes = []
    vehicles = []
    matrix = []
    assignesPermutation = []
    finalSolution={}
    inputFileName = ""
    outputFileName = ""
    def __init__(self, jsonInputFile):
        self.setInputFileName(jsonInputFile);
        f = open(jsonInputFile, "r")
        jsonstr = f.read()
        self.details = json.loads(jsonstr)
        for x in self.details['vehicles']:
            self.vehicles.append(x)

        for x in self.details['jobs']:
            self.jobIndexes.append(x['location_index'])

        for x in self.details['matrix']:
            self.matrix.append(x)

        potantialAssignes = self.findNumbersAddUpToGivenNumber(
            len(self.jobIndexes), len(self.vehicles))
        self.assignesPermutation.clear()
        for x in potantialAssignes:
            logging.debug("potantialAssignes")
            logging.debug(x)
            self.assignesPermutation.append(list(permutations(x)))

        logging.debug("potantialAssignes permutations")
        logging.debug(self.assignesPermutation)

        f.close()

    @classmethod
    def calculateRepresentation(self, route, assign):
        vehicleIndex = 0
        representResult = {}
        routeList = []
        routeObject = {}
        routeIndex = 0
        totalDuration = 0
        logging.debug("route %s", route)
        logging.debug("assign %s", assign)
        logging.debug("vehicles %s", self.vehicles)

        for assignCount in assign:
            logging.debug("assignCount %s", assignCount)
            logging.debug("0 %s", self.vehicles[vehicleIndex]['start_index'])
            logging.debug("1 %s", route[routeIndex:routeIndex+assignCount])
            logging.debug("vehicleIndex %s", vehicleIndex)
            logging.debug("routeIndex %s", vehicleIndex)
            logging.debug(
                "self.vehicles[vehicleIndex]['id'] %s", self.vehicles[vehicleIndex]['id'])
            routeDuration = self.calculateRoute(
                self.vehicles[vehicleIndex]['start_index'], route[routeIndex:routeIndex+assignCount])
            routeList.append(route[routeIndex:routeIndex+assignCount])

            routeObject[f"{self.vehicles[vehicleIndex]['id']}"] = {}
            routeObject[f"{self.vehicles[vehicleIndex]['id']}"]['jobs'] = route[routeIndex:routeIndex+assignCount]
            routeObject[f"{self.vehicles[vehicleIndex]['id']}"]['delivery_duration'] = routeDuration
            totalDuration += routeDuration
            routeIndex += assignCount
            vehicleIndex = vehicleIndex+1
            logging.debug(totalDuration)

        representResult["total_delivery_duration"] = totalDuration        
        representResult["routes"] = routeObject
        return representResult

    @classmethod
    def calculateRoute(self, start_position, route):
        routeDuration = 0

        if route != [] and route != ():
            routeDuration = self.matrix[start_position][route[0]]
            for i in range(len(route)-1):
                routeDuration += self.matrix[route[i]][route[i + 1]]
        return routeDuration

    # Finds the exact count of numbers which sum up to given number
    @classmethod
    def findNumbersAddUpToGivenNumber(self, givenNumber, countOfNumbers):
        combinationsArray = [0] * givenNumber
        finalResult = []

        self.findNumbersAddUpToGivenNumberBaseRecursive(
            combinationsArray, 0, givenNumber, givenNumber, finalResult, countOfNumbers)

        logging.debug("finalResult %s",finalResult)
        return finalResult
    
    @classmethod
    # Function solution base
    # Find all combinations that add upto given number
    # https://www.geeksforgeeks.org/find-all-combinations-that-adds-upto-given-number-2/
    def findNumbersAddUpToGivenNumberBaseRecursive(self, combinationsArray, index, num, reducedNum, result, countOfNumbers):
        logging.debug("0, reducedNum %s,combinationsArray %s, index %s,",reducedNum,combinationsArray,index)
        
        if (reducedNum < 0):
            logging.debug("return")
            return

        logging.debug("combinationsArray %s, index %s, num %s, reducedNum %s, result %s, countOfNumbers %s",combinationsArray, index, num, reducedNum, result, countOfNumbers);

        if (reducedNum == 0):
            localResult = []
            for i in range(countOfNumbers):
                if i < index:
                    logging.debug("i %s, combinationsArray[i] %s",i,combinationsArray[i])
                    localResult.append(combinationsArray[i])
                else:
                    localResult.append(0)

            if (countOfNumbers >= index):
                result.append(localResult)

            return

        prev = 1 if(index == 0) else combinationsArray[index - 1]
        logging.debug("prev %s, combinationsArray %s,reducedNum %s",prev,combinationsArray,reducedNum)
        for k in range(prev, num + 1):
            combinationsArray[index] = k
            logging.debug("k %s, combinationsArray[index] %s",k,combinationsArray[index])
            self.findNumbersAddUpToGivenNumberBaseRecursive(combinationsArray, index + 1, num,
                                                            reducedNum - k, result, countOfNumbers)
    
    @classmethod
    def exportSolution(self):
        outputFileName = f'output_for_{os.path.splitext(self.inputFileName)[0]}.json'
        self.setOutputFileName(outputFileName)
        with open(outputFileName, "w") as outputFile:
            outputFile.write(json.dumps(self.finalSolution));
    
    @classmethod
    def setFinalSolution(self,input):
        self.finalSolution = input;
    
    @classmethod
    def setInputFileName(self,input):
        self.inputFileName = input;
        
    @classmethod
    def setOutputFileName(self,input):
        self.outputFileName = input;
    
