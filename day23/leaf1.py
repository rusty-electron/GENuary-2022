from turtle_class import turtle_parser
from functions import L_System

axiom = 'F'
rules = {
            'F': 'FF+[+F-F-F]-[-F+F+F]'
        }

if __name__ == "__main__":
    tt = turtle_parser(color = '#bfd3c1', dist = 100)
    lsys = L_System(axiom, rules)
    for _ in range(4):
        tt.parse_sentence(lsys.generate())
    tt.done()
