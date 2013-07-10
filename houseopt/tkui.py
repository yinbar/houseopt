from . import glp, problem, parse
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
import tkinter.messagebox
import traceback

houses = {
    63:['A 2', 'B 2', 'C 2', 'D 1', 'E 2'],
    77:['A 3', 'B 2', 'C 2', 'D 2', 'E 2'],
    85:['A 11', 'B 10', 'C 10', 'D 23', 'E 11'],
    }

sizes = [63,77,85]
filetypes = [('Text Documents', '*.txt'), ('All Files', '*.*')]

min_pref = 0
max_pref = 5

def dump_solution(f, sol):
    for (customer, house), val in sorted(sol.items()):
        if val > 0.5:
            f.write('{} {}\n'.format(customer.decode('utf-8'),
                                     house.decode('utf-8')))

def main():
    root = tk.Tk()

    root.title('Housing Optimizer')
    app = ttk.Frame(root)
    app.style = ttk.Style()
    app.style.theme_use('default')

    app.pack(fill=tk.BOTH, expand=1)
    savetext = 'Save {:2d} ({:03d})'
    solution = {}

    def do_load():
        fn = tk.filedialog.askopenfilename(filetypes=filetypes)
        if not fn:
            return

        for k in sizes:
            buttons[k].configure(state=tk.DISABLED)

        for k in sizes:
            prob = problem.HousingProblem()
            houses_ = parse.parse_houses(prob, houses[k])
            try:
                parse.parse_customers(prob, open(fn), houses_, min_pref,
                                      max_pref)
            except IOError:
                tk.messagebox.showerror('Error',
                                        'Failed to open customers file')
                return
            except ValueError as e:
                tk.messagebox.showerror('Error',
                                        traceback.format_exc())
                return

            lp = glp.LinearProblem()
            prob.add_to_problem(lp)
            err = lp.solve()

            if err:
                tk.messagebox.showerror('Error',
                                        "Couldn't solve linear problem.\n\
Error Code: " + str(err))
                return

            obj = lp.get_solution_obj()
            solution[k] = lp.get_solution_vars()
            buttons[k].configure(state=tk.NORMAL, text=savetext.format(k,
                                                                    int(obj)))
            

    load = ttk.Button(app, text='Load Problem', command=do_load)
    load.pack(side=tk.TOP)


    def make_ksave(k):
        def do_save():
            fn = tk.filedialog.asksaveasfilename(filetypes=filetypes)
            if not fn:
                return

            try:
                f = open(fn, 'w')
                dump_solution(f, solution[k])
                f.close()
            except IOError:
                tk.messagebox.showerror('Error',
                                        'Failed to save solution')
                return
                
        
        butt = ttk.Button(app, text=savetext.format(k, 0), command=do_save,
                          state=tk.DISABLED)
        butt.pack(side=tk.LEFT)
        return butt

    buttons = {k:make_ksave(k) for k in sizes}
    
    root.mainloop()

if __name__ == '__main__':
    main()
