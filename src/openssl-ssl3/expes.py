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
ssl3_cbc_digest_record = B.Executable(
    "ssl3_cbc_digest_record",
    high_syms="md_out,header,data,data_plus_mac_size,mac_secret",
    memory_file="ssl3_cbc_digest_record.mem")
executables = [ssl3_cbc_digest_record]

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
