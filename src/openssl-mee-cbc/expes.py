#!/usr/bin/python3
import sys
sys.path.insert(1, '../../python_scripts/')
import params as P
import benchs as B
import libxp as E

TIMEOUT = 3600 * 6  # 6 hours timeout
N_ITER = 1
STAT_FILE = "stats/results.csv"
DEBUG = P.NONE
# DEBUG = P.VERBOSE
# # DEBUG = P.DEBUG

# Use cases
mee_cbc = B.Executable("mee-cbc",
                       high_syms="out,enc_sk,mac_sk",
                       memory_file="mee-cbc.mem")
executables = [mee_cbc]

if __name__ == '__main__':

    benchs = B.BenchsFromExecutables(executables)
    params = P.Params(timeout=TIMEOUT, n_iter=N_ITER,
                      stat_file=STAT_FILE, debug=DEBUG)

    # Run expes for CT
    E.xp_runner(benchs, params)

    # Experiments for Spectre-PHT
    E.xp_runner(benchs, params, pht=E.PHT_EXPLICIT)
    E.xp_runner(benchs, params, pht=E.PHT_HAUNTED)

    # Experiments for Spectre-STL
    E.xp_runner(benchs, params, stl=E.STL_EXPLICIT)
    E.xp_runner(benchs, params, stl=E.STL_HAUNTED)
