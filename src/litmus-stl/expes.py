#!/usr/bin/python3
import sys
sys.path.insert(1, '../../python_scripts/')
import params as P
import benchs as B
import libxp as E

TIMEOUT = 3600
N_ITER = 1
STAT_FILE = "stats/results.csv"
DEBUG = P.NONE
# DEBUG = P.VERBOSE
# DEBUG = P.DEBUG

# Use cases
executable = "spectrev4"
entrypoints = ["case_1", "case_2", "case_3", "case_4", "case_5",
               "case_6", "case_7", "case_8", "case_9",
               "case_9_bis", "case_10", "case_11", "case_12",
               "case_13"]
high_syms = "secretarray"

if __name__ == '__main__':

    benchs = B.BenchsMultiEp(executable, entrypoints, high_syms=high_syms)
    params = P.Params(timeout=TIMEOUT, n_iter=N_ITER,
                      stat_file=STAT_FILE, debug=DEBUG)

    # # Run expes for CT
    E.xp_runner(benchs, params)

    # # Experiments for Spectre-STL
    E.xp_runner(benchs, params, stl=E.STL_EXPLICIT)
    E.xp_runner(benchs, params, stl=E.STL_HAUNTED)
