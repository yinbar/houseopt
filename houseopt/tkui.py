from . import glp, problem, parse
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.filedialog as filedialog
    import tkinter.messagebox as messagebox
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
import traceback

# houses = {
#    63:['A 2', 'B 2', 'C 2', 'D 1', 'E 2'],
#    77:['A 3', 'B 2', 'C 2', 'D 2', 'E 2'],
#    85:['A 11', 'B 10', 'C 10', 'D 23', 'E 11'],
#    }
# sizes = [63,77,85]

filetypes = [('Text Documents', '*.txt'), ('All Files', '*.*')]

min_pref = 0
max_pref = 5

house_types = ('A', 'B', 'C', 'D', 'E')

def dump_solution(f, sol):
    for (customer, house), val in sorted(sol.items()):
        if val > 0.5:
            f.write('{} {}\n'.format(customer.decode('utf-8'),
                                     house.decode('utf-8')))

def commandof(b):
    def __wrap__(x):
        b.configure(command=x)
        return x
    return __wrap__

def pack(app, **keywds):
    app.pack(**keywds)
    return app

def main():
    root = tk.Tk()

    root.title('Housing Optimizer')
    app = ttk.Frame(root)
    app.style = ttk.Style()
    app.style.theme_use('default')

    app.pack(fill=tk.BOTH, expand=1)
    savetext = 'Save {:2d} ({:03d})'
    solution = {}

    manageframe = ttk.Frame(app)
    manageframe.pack(side=tk.TOP)

    load_houses = ttk.Button(manageframe, text='Load Houses')
    load_houses.pack(side=tk.LEFT)

    load = ttk.Button(manageframe, text='Load Problem', state=tk.DISABLED)
    load.pack(side=tk.LEFT)

    problems = []

    @commandof(load_houses)
    def do_load_houses():
        fn = filedialog.askopenfilename(filetypes=filetypes)
        if not fn:
            return

        for b in buttons:
            b.configure(state=tk.DISABLED)
        solution.clear()

        try:
            problems[:] = parse.read_lines_file(open(fn), house_types)
        except IOError:
            messagebox.showerror('Error',
                                 'Failed to open houses file')
            return
        except ValueError as e:
            messagebox.showerror('Error',
                                    traceback.format_exc())
            return

        if len(problems) != len(buttons):
            messagebox.showerror('Error',
                                    'Expected {} housing problems, got {}'.
                                    format(len(problems), len(buttons)))
            del problems[:]

        for b,(s,_) in zip(buttons,problems):
            bind_save(b, s)

        load.configure(state=tk.NORMAL)

    @commandof(load)
    def do_load():
        fn = filedialog.askopenfilename(filetypes=filetypes)
        if not fn:
            return

        for b in buttons:
            b.configure(state=tk.DISABLED)

        for b,(k,line) in zip(buttons, problems):
            prob = problem.HousingProblem()

            for name, count in line:
                prob.add_house(name, count)

            try:
                parse.parse_customers(prob, open(fn), house_types, min_pref,
                                      max_pref)
            except IOError:
                messagebox.showerror('Error',
                                        'Failed to open customers file')
                return
            except ValueError as e:
                messagebox.showerror('Error',
                                        traceback.format_exc())
                return

            lp = glp.LinearProblem()
            prob.add_to_problem(lp)
            err = lp.solve()

            if err:
                messagebox.showerror('Error',
                                        "Couldn't solve linear problem.\n\
Error Code: " + str(err))
                return

            obj = lp.get_solution_obj()
            solution[k] = lp.get_solution_vars()
            b.configure(state=tk.NORMAL, text=savetext.format(k,int(obj)))

    def bind_save(butt, k):             
        butt.configure(text=savetext.format(k, 0))
        
        @commandof(butt)
        def do_save():
            fn = filedialog.asksaveasfilename(filetypes=filetypes)
            if not fn:
                return

            try:
                f = open(fn, 'w')
                dump_solution(f, solution[k])
                f.close()
            except IOError:
                messagebox.showerror('Error',
                                        'Failed to save solution')
                return

        return butt

    buttons = [pack(ttk.Button(app, text=savetext.format(0,0),
                               state=tk.DISABLED), side=tk.LEFT)
               for k in range(3)]

    root.mainloop()

if __name__ == '__main__':
    main()
