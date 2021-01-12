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
# DEBUG = P.DEBUG

# Use cases
executables = ["tea_encrypt_O0", "tea_encrypt_O1", "tea_encrypt_O2",
               "tea_encrypt_O3", "tea_encrypt_Of"]
executables = ["tea_encrypt_Of"]
high_syms = "key,data"

if __name__ == '__main__':

    benchs = B.BenchsMultiExec(executables, high_syms=high_syms)
    params = P.Params(timeout=TIMEOUT, n_iter=N_ITER,
                      stat_file=STAT_FILE, debug=DEBUG)

    # Run expes for CT
    E.xp_runner(benchs, params)

    # Experiments for Spectre-PHT
    E.xp_runner(benchs, params, pht=E.PHT_EXPLICIT, dyn_pht=E.DYN_PHT_FULL)
    E.xp_runner(benchs, params, pht=E.PHT_HAUNTED, dyn_pht=E.DYN_PHT_FULL)

    # Experiments for Spectre-STL
    E.xp_runner(benchs, params, stl=E.STL_EXPLICIT)
    E.xp_runner(benchs, params, stl=E.STL_HAUNTED)
