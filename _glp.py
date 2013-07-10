import ctypes, os
from .util import throw

if os.name == 'posix':
    GLP = ctypes.CDLL('libglpk.so')
else:
    GLP = ctypes.CDLL('glpk.dll')


glp_prob_p = ctypes.POINTER(type('glp_prob', (ctypes.Structure,), {}))

GLP_MIN = 1
GLP_MAX = 2

GLP_FR = 1
GLP_LO = 2
GLP_UP = 3
GLP_DB = 4
GLP_FX = 5

GLP_CV = 1
GLP_IV = 2
GLP_BV = 3

# Problem
create_prob = GLP.glp_create_prob
create_prob.restype = glp_prob_p
create_prob.argtypes = []

delete_prob = GLP.glp_delete_prob
delete_prob.restype = None
delete_prob.argtypes = [glp_prob_p]

simplex = GLP.glp_simplex
simplex.restype = ctypes.c_int
simplex.argtypes = [glp_prob_p, ctypes.c_void_p]

intopt = GLP.glp_intopt
intopt.restype = ctypes.c_int
intopt.argtypes = [glp_prob_p, ctypes.c_void_p]

# Objective
set_obj_dir = GLP.glp_set_obj_dir
set_obj_dir.restype = None
set_obj_dir.argtypes = [glp_prob_p, ctypes.c_int]

set_obj_coef = GLP.glp_set_obj_coef
set_obj_coef.restype = None
set_obj_coef.argtypes = [glp_prob_p, ctypes.c_int, ctypes.c_double]

mip_obj_val = GLP.glp_mip_obj_val
mip_obj_val.restype = ctypes.c_double
mip_obj_val.argtypes = [glp_prob_p]

# Rows
add_rows = GLP.glp_add_rows
add_rows.restype = ctypes.c_int
add_rows.argtypes = [glp_prob_p, ctypes.c_int]

set_row_name = GLP.glp_set_row_name
set_row_name.restype = None
set_row_name.argtypes = [glp_prob_p, ctypes.c_int, ctypes.c_char_p]

set_row_bnds = GLP.glp_set_row_bnds
set_row_bnds.restype = None
set_row_bnds.argtypes = [glp_prob_p, ctypes.c_int,
                         ctypes.c_int, ctypes.c_double, ctypes.c_double]

_set_mat_row = GLP.glp_set_mat_row
_set_mat_row.restype = None
_set_mat_row.argtypes = [glp_prob_p, ctypes.c_int, ctypes.c_int,
                         ctypes.POINTER(ctypes.c_int),
                         ctypes.POINTER(ctypes.c_double)]

set_mat_row = lambda lp, row, ind, val: _set_mat_row(
    lp,
    ctypes.c_int(row),
    ctypes.c_int(len(ind)),
    (ctypes.c_int * (len(ind)+1))(0, *ind),
    (ctypes.c_double * (len(val)+1))(0, *val)) if len(ind) == len(
        val) else throw(ValueError)

# Columns
add_cols = GLP.glp_add_cols
add_cols.restype = ctypes.c_int
add_cols.argtypes = [glp_prob_p, ctypes.c_int]

set_col_name = GLP.glp_set_col_name
set_col_name.restype = None
set_col_name.argtypes = [glp_prob_p, ctypes.c_int, ctypes.c_char_p]

set_col_bnds = GLP.glp_set_col_bnds
set_col_bnds.restype = None
set_col_bnds.argtypes = [glp_prob_p, ctypes.c_int,
                         ctypes.c_int, ctypes.c_double, ctypes.c_double]

set_col_kind = GLP.glp_set_col_kind
set_col_kind.restype = None
set_col_kind.argtypes = [glp_prob_p, ctypes.c_int, ctypes.c_int]

mip_col_val = GLP.glp_mip_col_val
mip_col_val.restype = ctypes.c_double
mip_col_val.argtypes = [glp_prob_p, ctypes.c_int]

__all__ = ['create_prob', 'delete_prob', 'simplex', 'intopt',

           'set_obj_dir', 'set_obj_coef', 'mip_obj_val',

           'add_rows', 'set_row_name', 'set_row_bnds', 'set_mat_row',

           'add_cols', 'set_col_name', 'set_col_bnds', 'set_col_kind',
           'mip_col_val',

           'GLP_MIN', 'GLP_MAX',
           'GLP_FR', 'GLP_LO', 'GLP_UP', 'GLP_DB', 'GLP_FX',
           'GLP_CV', 'GLP_IV', 'GLP_BV',
           ]
