from . import _glp
from .util import shuffled

class LinearProblem:
    def __init__(self):
        self.lp = _glp.create_prob()

        self.max_row_codename = 0
        self.row_name_to_id = {}

        self.max_col_codename = 0
        self.col_name_to_id = {}
        self.col_name_to_idx = {}

    def _get_row_id(self, var):
        if var in self.row_name_to_id:
            return self.row_name_to_id[var]

        self.row_name_to_id[var] = 'c{}'.format(self.max_row_codename
                                                ).encode('ascii')
        self.max_row_codename += 1
        
        return self.row_name_to_id[var]

    def _get_col_id(self, var):
        if var in self.col_name_to_id:
            return self.col_name_to_id[var]

        self.col_name_to_id[var] = 'v{}'.format(self.max_col_codename
                                                ).encode('ascii')
        self.max_col_codename += 1
        
        return self.col_name_to_id[var]

    def add_binary_variable(self, var, obj):
        self.add_independent_variable(var, obj, 0, 1, _glp.GLP_BV)

    def _add_constraints(self, csf, cr, mini, maxi):
        if mini is None and maxi is None:
            csf(self.lp, cr, _glp.GLP_FR, 0, 0)
        elif mini is not None and maxi is None:
            csf(self.lp, cr, _glp.GLP_LO, mini, 0)
        elif mini is None and maxi is not None:
            csf(self.lp, cr, _glp.GLP_HI, 0, maxi)
        elif mini == maxi:
            csf(self.lp, cr, _glp.GLP_FX, mini, maxi)
        else:
            csf(self.lp, cr, _glp.GLP_DB, mini, maxi)

    def add_independent_variable(self, var, coef, mini, maxi, vt):
        varidx = _glp.add_cols(self.lp, 1)
        self.col_name_to_idx[var] = varidx
        varid = self._get_col_id(var)

        _glp.set_col_name(self.lp, varidx, varid)
        _glp.set_obj_coef(self.lp, varidx, coef)
        self._add_constraints(_glp.set_col_bnds, varidx, mini, maxi)
        _glp.set_col_kind(self.lp, varidx, vt)

    def add_dependent_variable(self, var, coefs, mini, maxi):
        varidx = _glp.add_rows(self.lp, 1)
        varid = self._get_row_id(var)

        _glp.set_row_name(self.lp, varidx, varid)
        self._add_constraints(_glp.set_row_bnds, varidx, mini, maxi)
        if not coefs:
            return

        _glp.set_mat_row(self.lp, varidx, *(zip(*((self.col_name_to_idx[i],j)
                                                for (i,j) in
                                                shuffled(coefs.items())))))

    def set_obj_dir(self, maximize):
        if maximize:
            _glp.set_obj_dir(self.lp, _glp.GLP_MAX)
        else:
            _glp.set_obj_dir(self.lp, _glp.GLP_MIN)
            
    def solve(self):
        st = _glp.simplex(self.lp, None)
        if st:
            return st

        st = _glp.intopt(self.lp, None)
        return st
    
    def get_solution_vars(self):
        return {name: _glp.mip_col_val(self.lp, idx) for
                (name, idx) in self.col_name_to_idx.items()}

    def get_solution_obj(self):
        return _glp.mip_obj_val(self.lp)
    
    def __del__(self):
        _glp.delete_prob(self.lp)
