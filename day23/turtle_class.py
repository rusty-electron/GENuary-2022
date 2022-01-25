import turtle

from functions import L_System

axiom = 'F'
rules = {
            'F': 'FF+[+F-F-F]-[-F+F+F]'
        }

WIDTH = 700
HEIGHT = 700
screen = turtle.Screen()
screen.setup(HEIGHT, WIDTH)
screen.bgcolor("#4B6858")

class turtle_parser:
    def __init__(self, initial_loc = None, color = None, dist = 5, angle = 25):
        self.speed = 5
        self.angle = angle

        self.t = turtle.Turtle()
        self.t.ht()
        self.t.penup()
        self.t.setheading(90)

        if initial_loc == None:
            self.initial_loc = (0, - HEIGHT//2)
        self.t.setpos(self.initial_loc)
        self.stack = []
        self.t.pendown()

        if color != None:
            self.t.color(color)
        self.dist = dist

    def parse_sentence(self, sent):
        self.t.setheading(90)
        self.speed += 5
        self.t.speed(self.speed)

        self.t.penup()
        self.t.setpos(self.initial_loc)
        self.t.pendown()

        for ch in sent:
            if ch == 'F':
                self.t.fd(self.dist)
            elif ch == '+':
                self.t.rt(self.angle)
            elif ch == '-':
                self.t.lt(self.angle)
            elif ch == '[':
                status = (self.t.heading(), self.t.pos())
                self.stack.append(status)
            elif ch == ']':
                if len(self.stack) == 0:
                    print("[ERROR] No saved location exists, skipping!")
                    continue
                else:
                    self.t.penup()
                    status = self.stack.pop()
                    self.t.setheading(status[0])
                    self.t.setpos(status[1])
                    self.t.pendown()
        self.dist *= .5

    def done(self):
        print("[INFO] Drawing done!")
        turtle.done()

if __name__ == "__main__":
    tt = turtle_parser(color = '#bfd3c1', dist = 100)
    lsys = L_System(axiom, rules)
    for _ in range(4):
        tt.parse_sentence(lsys.generate())
    turtle.done()
