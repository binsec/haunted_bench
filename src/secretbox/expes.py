#!/usr/bin/python3
import sys
sys.path.insert(1, '../../python_scripts/')
import params as P
import benchs as B
import libxp as E

TIMEOUT = 3600 * 6              # 6 hours timeout
N_ITER = 1
STAT_FILE = "results.csv"
DEBUG = P.NONE
# DEBUG = P.VERBOSE
# DEBUG = P.VERBOSE_LIGHT
# DEBUG = P.DEBUG
# DEBUG = P.DEBUG_LIGHT

# Use cases
secretbox = B.Executable("secretbox", high_syms="m,k",
                         memory_file="secretbox.mem")
executables = [secretbox]

if __name__ == '__main__':

    benchs = B.BenchsFromExecutables(executables)
    params = P.Params(timeout=TIMEOUT, n_iter=N_ITER,
                      stat_file=STAT_FILE, debug=DEBUG)

    # Run expes for CT
    E.xp_runner(benchs, params)

    # Experiments for Spectre_PHT Dynamic
    E.xp_runner(benchs, params, pht=E.PHT_EXPLICIT, dyn_pht=E.DYN_PHT_FULL)
    E.xp_runner(benchs, params, pht=E.PHT_HAUNTED, dyn_pht=E.DYN_PHT_FULL)

    # Experiments for Spectre-STL
    E.xp_runner(benchs, params, stl=E.STL_EXPLICIT)
    E.xp_runner(benchs, params, stl=E.STL_HAUNTED)
