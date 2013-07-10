import sys
from . import parse, glp, problem

_, hfile, cfile = sys.argv

prob = problem.HousingProblem()
lp = glp.LinearProblem()

houses = parse.parse_houses(prob, open(hfile))
parse.parse_customers(prob, open(cfile), houses, 0, 5)

prob.add_to_problem(lp)
st = lp.solve()
if st:
    raise ValueError('Solution Failed. Code {}'.format(st))

print('Achieved objective', lp.get_solution_obj())

for (customer, house), pref in sorted(lp.get_solution_vars().items()):
    if pref > 0.5:
        sys.stderr.write('{} {}\n'.format(customer.decode('utf-8'),
                                          house.decode('utf-8')))
