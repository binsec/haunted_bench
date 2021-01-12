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
# DEBUG = P.DEBUG_LIGHT

# Use cases
high_syms = "secret"
donna_O0 = B.Executable("donna_O0", high_syms=high_syms,
                        memory_file="donna_O0.mem")
donna_O1 = B.Executable("donna_O1", high_syms=high_syms,
                        memory_file="donna_O1.mem")
donna_O2 = B.Executable("donna_O2", high_syms=high_syms,
                        memory_file="donna_O2.mem")
donna_O3 = B.Executable("donna_O3", high_syms=high_syms,
                        memory_file="donna_O3.mem")
donna_Of = B.Executable("donna_Of", high_syms=high_syms,
                        memory_file="donna_Of.mem")

executables = [donna_O0, donna_O1, donna_O2, donna_O3, donna_Of]


if __name__ == '__main__':

    benchs = B.BenchsFromExecutables(executables)
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
