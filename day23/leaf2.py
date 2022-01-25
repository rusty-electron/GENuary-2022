from turtle_class import turtle_parser
from functions import L_System

axiom = 'X'
rules = {
            'X': 'F[-X][X]F[-X]+FX',
            'F': 'FF'
        }

# axiom = 'X'
# rules = {
#             'X': 'F+[[X]-X]-F[-FX]+X',
#             'F': 'FF'
#         }

import turtle

WIDTH = 700
HEIGHT = 700
screen = turtle.Screen()
screen.setup(HEIGHT, WIDTH)
screen.bgcolor("#5C415D")

if __name__ == "__main__":
    tt = turtle_parser(color = '#ff0035', dist = 100)
    lsys = L_System(axiom, rules)
    for _ in range(6):
        tt.parse_sentence(lsys.generate())
    tt.done()
