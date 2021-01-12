#!/usr/bin/python3
import subprocess
import os
import params as P
import benchs as B
from pathlib import Path

# EXE="cgexec -g memory:binsec binsec "
EXE = "binsec "

PHT_NONE = "none"
PHT_EXPLICIT = "explicit-smart"
PHT_HAUNTED = "haunted"

STL_NONE = "none"
STL_EXPLICIT = "explicit"
STL_HAUNTED = "haunted-ite"

DYN_PHT_NONE = "none"
DYN_PHT_HYB0 = "hybrid0"
DYN_PHT_HYB20 = "hybrid20"
DYN_PHT_FULL = "full"


# Get the command from params
def get_cmd(executable, params, spec_depth, pht, dyn_pht, stl):
    exec_file = executable.get_exec_file()
    entrypoint = executable.get_entrypoint()
    high_syms = executable.get_high_syms()
    memory_file = str(executable.get_memory_file())
    prefix = Path(exec_file).stem + "_" + entrypoint
    args = params.get_args()
    cmd = EXE + str(exec_file) + " " + args + " -entrypoint " + entrypoint + \
        (" -relse-high-sym " + high_syms if high_syms != "" else "") + \
        (" -sse-memory " + memory_file if memory_file != "" else "") + \
        " -relse-stat-prefix " + prefix + " -relse-spectre-pht " + \
        pht + " -relse-spectre-dyn-pht " + dyn_pht + \
        " -relse-speculative-window " + str(spec_depth) + \
        " -relse-spectre-stl " + stl
    print(cmd)
    return cmd


def run(executable, params, spec_depth, pht, dyn_pht, stl):
    print("\n----------\nAnalyzing " + str(executable.get_exec_file())
          + " at " + executable.get_entrypoint() + " with pht=" + pht
          + ", dyn_pht=" + dyn_pht + ", stl=" + stl)
    cmd = get_cmd(executable, params, spec_depth, pht, dyn_pht, stl)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0 and result.returncode != 7 and \
       result.returncode != 8:
        raise ValueError('Unknown return code from Binsec !')
    subprocess.run("killall boolector", shell=True)


# Run all the experiments
def xp_runner(bench, params, pht=PHT_NONE, dyn_pht=DYN_PHT_NONE, stl=STL_NONE):
    for i in range(params.n_iter):
        for spec_depth in params.get_spec_depths():
            for executable in bench.get_executables():
                run(executable, params, spec_depth, pht, dyn_pht, stl)
