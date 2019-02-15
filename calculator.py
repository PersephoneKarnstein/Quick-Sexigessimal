''' tk_calculator_tiny2.py
A updated tiny calculator using the Tkinter GUI toolkit
you can type in functions contained in module math
for instance type in  tan(pi/180)  then click  =
tested with Python27 and Python33  by  vegaseat  13nov2013
'''
# avoid integer division by Python2
from __future__ import division
from math import *
import numpy as np
from functools import partial
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
class MyApp(tk.Tk):
    def __init__(self):
        # the root will be self
        tk.Tk.__init__(self)
        self.title("Tiny TK Calculator")
        # use width x height + x_offset + y_offset (no spaces!)
        #self.geometry("300x150+150+50")
        # or set x, y position only
        self.geometry("+150+50")
        self.memory = 0
        self.create_widgets()
    def create_widgets(self):
        # this also shows the calculator's button layout
        btn_list = [
        '7',  '8',  '9',  'x',  'C',
        '4',  '5',  '6',  '/',  'Mem',
        '1',  '2',  '3',  '-',  'M+',
        '0',  '.',  '=',  '+',  'neg' ]
        rel = 'ridge'
        # create all buttons with a loop
        r = 2
        c = 0
        for b in btn_list:
            # partial takes care of function and argument
            cmd = partial(self.calculate, b)
            tk.Button(self, text=b, width=5, relief=rel,
                command=cmd).grid(row=r, column=c)
            c += 1
            if c > 4:
                c = 0
                r += 1
        # use an Entry widget for an editable display
        self.entry = tk.Entry(self, width=33, bg="grey")
        self.entry.grid(row=0, column=0, columnspan=5)
        self.sexentry = tk.Entry(self, width=33, bg="grey")
        self.sexentry.grid(row=1, column=0, columnspan=5)

    def desex(sex):
        import numpy as np
        if sex[0] == '-':
            sex = sex[1:]
            negative = True
        else: negative = False

        if ";" in sex:
            sex = sex.split(";")
            decimal = True
        else: decimal = False

        if decimal == True:
            if len(sex) > 2: raise Exception("There should be at most one semicolon in a sexigessimal number.")
            else:
                integer_sex = sex[0].split(",")
                decimal_sex = sex[1].split(",")
        else:
            integer_sex = sex.split(",")

        for digit in np.arange(len(integer_sex)): 
            if integer_sex[digit] != '': integer_sex[digit] = int(integer_sex[digit])
            else: integer_sex[digit] = int(0)

        if decimal == True: 
            for digit in np.arange(len(decimal_sex)): 
                if decimal_sex[digit] != '': decimal_sex[digit] = int(decimal_sex[digit])
                else: decimal_sex[digit] = int(0)
        else: pass

        n, answer = 0, 0
        for element in integer_sex[::-1]:
            answer += element*(60**n)
            n += 1

        n = 1
        if decimal == True:
            for element in decimal_sex:
                answer += element*(60**(-n))
                n += 1
        else: pass

        if negative == True: answer *= (-1)
        else: pass

        return answer

    def sex(x):
        import numpy as np
        if x == int(x): integer = True
        else: integer = False
        
        if 18446744073709551615 > x > 0:
            max_order = int(np.log(x)/np.log(60.))
            negative = False
        elif 0 > x > -18446744073709551615:
            x = np.abs(x)
            max_order = int(np.log(x)/np.log(60.))
            negative = True
        elif x == 0: 
            return str(x) #due to problems with logs this is the easiest way
            raise Exception("Seriously?")
        else:
            raise Exception("Currently cannot calculate numbers greater than 2^64 - 1 but props for trying")
        
        digits = list()
        
        if x >= 1:
            orders_to_check = np.arange(max_order+1)[::-1]
            if integer == True: pass
            else: orders_to_check = np.append(orders_to_check, (-1)*np.arange(8)[1:] )
            
            for n in orders_to_check:
                digits.append(int(float(x)/(60**n)))
                x = round(((float(x)/(60**n))-int(float(x)/(60**n)))*(60**n),8) #the 'round' deals with floating point errors
            
            if negative == False:
                if integer == True: sex = str(digits[:max_order+1])[1:-1]
                else: sex = str(digits[:max_order+1])[1:-1]+"; "+str(digits[max_order+1:])[1:-1]
            else:
                if integer == True: sex = "-"+str(digits[:max_order+1])[1:-1]
                else: sex = "-"+str(digits[:max_order+1])[1:-1]+"; "+str(digits[max_order+1:])[1:-1]
        
        else:
            orders_to_check = (-1)*np.arange(8)[1:]
            for n in orders_to_check:
                digits.append(int(float(x)/(60**n)))
                x = ((float(x)/(60**n))-int(float(x)/(60**n)))*(60**n)
            
            if negative == False: sex = "0; "+str(digits)[1:-1]
            else: sex = "-0; "+str(digits)[1:-1]
        
        return sex

    def calculate(self, key):
        if key == '=':
            # guard against the bad guys abusing eval()
            if '_' in self.entry.get():
                self.entry.insert(tk.END, " not accepted!")
            # here comes the calculation part
            try:
                result = eval(self.entry.get())
                self.entry.insert("= " + str(result))
                self.sexentry.insert("= " + str(sex(result)))
            except:
                self.entry.insert("Error!")
                self.sexentry.insert("Error!")
        elif key == 'C':
            self.entry.delete(0, tk.END)  # clear entry
        elif key == '->M':
            self.memory = self.entry.get()
            # extract the result
            if '=' in self.memory:
                ix = self.memory.find('=')
                self.memory = self.memory[ix+2:]
            self.title('M=' + self.memory)
        elif key == 'M->':
            if self.memory:
               self.entry.insert(tk.END, self.memory)
        elif key == 'neg':
            if '=' in self.entry.get():
                self.entry.delete(0, tk.END)
            try:
                if self.entry.get()[0] == '-':
                    self.entry.delete(0)
                else:
                    self.entry.insert(0, '-')
            except IndexError:
                pass
        else:
            # previous calculation has been done, clear entry
            if '=' in self.entry.get():
                self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, key)
app = MyApp()
app.mainloop()
