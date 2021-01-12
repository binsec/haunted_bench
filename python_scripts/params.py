from datetime import date
import os

# Debug enum
DEBUG_LIGHT = "debug-light"
DEBUG = "debug"
VERBOSE = "verbose"
VERBOSE_LIGHT = "verbose-light"
NONE = "none"

_DEFAULT_TIMEOUT = 0
_SOLVER_TIMEOUT = 0
_DEFAULT_NITER = 1
_DEFAULT_SPEC_DEPTH = 200
_SPEC_DEPTH_LIST = [20, 30, 40, 50, 100, 200]

_SEC_TO_LOAD = ".got,.got.plt,.data,.plt,.data.rel.ro"
_BINSECDIR = '/tmp/binsec'
_TRACEDIR = _BINSECDIR + '/traces'
_SMTDIR = _BINSECDIR + '/smtdir'

_ARG_FORALL = "-relse -relse-fp 1 -sse-depth 0 -sse-load-ro-sections \
-sse-load-sections " + _SEC_TO_LOAD + " -fml-solver boolector \
-fml-solver-timeout " + str(_SOLVER_TIMEOUT) + " -relse-debug-level 0 \
-relse-paths 0 -x86-handle-seg gs "

_ARG_VERBOSE = _ARG_FORALL + " -relse-low-decl -relse-print-model \
-sse-address-trace-file " + _TRACEDIR + "/trace -sse-comment \
-sse-smt-dir " + _SMTDIR

_ARG_VERBOSE_LIGHT = _ARG_FORALL + " -relse-low-decl -relse-print-model \
-sse-address-trace-file " + _TRACEDIR + "/trace -sse-comment "

_ARG_DEBUG = _ARG_VERBOSE + " -relse-debug-level 10"
_ARG_DEBUG_LIGHT = _ARG_FORALL + " -relse-debug-level 10"


# PARAMETERS
class Params(object):

    def date_suffix(prefix):
        return prefix + "_" + str(date.today.isoformat()) + ".csv"

    def __init__(self, timeout=_DEFAULT_TIMEOUT, n_iter=_DEFAULT_NITER,
                 stat_file="", debug=NONE):
        self.timeout = timeout
        self.n_iter = n_iter
        if stat_file == "":
            self.stat_file = self.date_suffix("stats")
        else:
            self.stat_file = stat_file
        self.debug = debug
        self.spec_depths = [_DEFAULT_SPEC_DEPTH]

    def get_args(self):
        def mk_dirs():
            if (not os.path.isdir(_BINSECDIR)):
                os.mkdir(_BINSECDIR)
            if (not os.path.isdir(_TRACEDIR)):
                os.mkdir(_TRACEDIR)
            if (not os.path.isdir(_SMTDIR)):
                os.mkdir(_SMTDIR)

        if self.debug == VERBOSE:
            args = _ARG_VERBOSE
            mk_dirs()
        elif self.debug == VERBOSE_LIGHT:
            args = _ARG_VERBOSE_LIGHT
            mk_dirs()
        elif self.debug == DEBUG:
            args = _ARG_DEBUG
            mk_dirs()
        elif self.debug == DEBUG_LIGHT:
            args = _ARG_DEBUG_LIGHT
        else:
            args = _ARG_FORALL + " -relse-stat-file " + self.stat_file
        return args + " -relse-timeout " + str(self.timeout)

    def get_spec_depths(self):
        return self.spec_depths

    def set_spec_depth_list(self, spec_list=_SPEC_DEPTH_LIST):
        self.spec_depths = spec_list
