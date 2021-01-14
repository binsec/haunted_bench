#!/usr/bin/python3
import sys
sys.path.insert(1, '../../python_scripts/')
import params as P
import benchs as B
import libxp as E
import import_csv as I
import pandas as pd
import os

TIMEOUT = 3600
N_ITER = 1
STAT_FILE = "results"
STAT_DIR = "stats/"
STAT_PATH = STAT_DIR + STAT_FILE + ".csv"
DEBUG = P.NONE
# DEBUG = P.DEBUG

# Use cases
executablev1 = "spectrev1"
entrypointsv1 = ["case_1", "case_2", "case_3", "case_4", "case_5",
                 "case_6", "case_7", "case_8", "case_9", "case_10",
                 "case_11gcc", "case_11ker", "case_11sub", "case_12",
                 "case_13", "case_14"]
executablev4 = "spectrev4"
entrypointsv4 = ["case_1", "case_2", "case_3", "case_4", "case_5",
                 "case_6", "case_7", "case_8", "case_9",
                 "case_9_bis", "case_10", "case_11", "case_12",
                 "case_13"]
high_syms = "secretarray"

if __name__ == '__main__':

    benchsv1 = B.BenchsMultiEp(executablev1, entrypointsv1, high_syms=high_syms, memory_file="spectrev1.mem")
    paramsv1 = P.Params(timeout=TIMEOUT, n_iter=N_ITER,
                        stat_file=STAT_PATH, debug=DEBUG)
    benchsv4 = B.BenchsMultiEp(executablev4, entrypointsv4, high_syms=high_syms, memory_file="spectrev4.mem")
    paramsv4 = P.Params(timeout=TIMEOUT, n_iter=N_ITER,
                        stat_file=STAT_PATH, debug=DEBUG)

    try:
        os.remove(STAT_PATH)
    except OSError:
        print(STAT_PATH)
        pass

    # Run expes for CT
    E.xp_runner(benchsv1, paramsv1)
    E.xp_runner(benchsv4, paramsv4)

    # Experiments for Spectre-PHT
    E.xp_runner(benchsv1, paramsv1, pht=E.PHT_HAUNTED, dyn_pht=E.DYN_PHT_FULL)

    # # Experiments for Spectre-STL
    E.xp_runner(benchsv4, paramsv4, stl=E.STL_HAUNTED)

    # Printing results
    print("\n\nSummary of results:\n")
    df = I.get_df_from_files(STAT_DIR, [STAT_FILE])
    df = df.groupby(['pht_status', 'stl_status']).sum()
    df = df[(df.T != 0).any()]
    df['label'] = "None"
    df.loc[('NoPHT', 'NoSTL'), ['label']] = "0-CT"
    df.loc[('Haunted', 'NoSTL'), ['label']] = "1-PHT"
    df.loc[('NoPHT', 'HauntedIteSTL'), ['label']] = "2-STL"
    I.pp_df(df.reset_index().sort_values(by='label'), I.PROJ_MIN)
