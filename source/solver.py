
from problem import *
import time


class Solver:
    @staticmethod
    def solve(problem, solverCls):
        solverStartTime = time.perf_counter()
        logging.debug(f"{solverStartTime}")
        solverCls.solve(problem)
        solverFinishTime = time.perf_counter()
        logging.debug(f"{solverFinishTime}")
        logging.debug(f" {solverFinishTime - solverStartTime:0.4f} seconds")
        print(f" {solverFinishTime - solverStartTime:0.4f} seconds")
