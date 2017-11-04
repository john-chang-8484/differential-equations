#!/usr/bin/env python

import sys, random, math, pygame, time, stringtofunc
from pygame.locals import *

#constants
window = [900, 400]
tau = 6.28318530717958
tstep = 0.0005
history_size = 804
speedup = 16
compress_history = True


def randcolour():
    # produce a random colour (list of length 3)
    # can't be too close to white
    return [random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)]

def maximum(l):
    ans = 0.0
    for i in l:
        if abs(i) > ans:
            ans = abs(i)
    return ans

class variable:
    colour = [0, 0, 0]
    val = 0.0
    history = [0.0] * history_size
    func = (lambda allvars : 0.0)
    scale = 1
    next = 0
    def __init__(self, aval, afunc):
        self.history = [0.0] * 804
        self.colour = randcolour()
        self.val = aval
        self.history.append(self.val)
        self.scale = 1
        self.next = 0
        self.func = afunc # use lambda expression
        m = max(self.history[1 - history_size:])
        self.scale = pow(2, int(math.ceil(math.log(1.00000001 + abs(m), 2) - math.log(200.0, 2))))
    def step(self):
        # update history, increment by a time step, rescale if necessary
        self.history.append(self.val)
        self.val += tstep * self.next
        m = maximum(self.history[1 - history_size:])
        self.scale = pow(2, int(math.ceil(math.log(1.00000001 + abs(m), 2) - math.log(200.0, 2))))
    def calc(self, allvars):
        # set next to expression given for dy/dt
        self.next = (self.func(allvars))
        


#----The Best Function: Main----
def main():
    pygame.init()
    try:
        lemming_icon = pygame.image.load("lightbulb.png")
        pygame.display.set_icon(pygame.transform.scale(lemming_icon, (32, 32)))
    except pygame.error:
        pass
    pygame.display.set_caption("Differential Equations")
    screen = pygame.display.set_mode(window)
    font_one = pygame.font.SysFont("Courier New", 20, "b")

    t = 0.0
    
    # all variables is a dictionary of variables, with each var's key being it's name
    all_variables = {}
    
    infile = open(sys.argv[1], "r")
    equations = infile.readlines()
    infile.close()
    
    for i in equations:
        print i
    
    i = 0
    while i < len(equations):
        if equations[i][0] == "#":
            equations.pop(i)
        else:
            equations[i] = equations[i].replace("\n", "").split(":")
            vname = equations[i][0].replace(" ", "")
            all_variables[vname] = variable(float(equations[i][1]), stringtofunc.tofunction(equations[i][2]))
            i += 1
    
    # main loop:
    inloop = True
    while inloop:
        for i in range(0, speedup):
            t += tstep
            for j in all_variables:
                all_variables[j].calc(all_variables)
            for j in all_variables:
                all_variables[j].step()
            if compress_history and i > 0:
                for j in all_variables:
                    all_variables[j].history.pop()

        #Draw all the stuff:
        screen.fill([255, 255, 255])
        for i in all_variables:
            for j in range(-700, -1):
                pygame.draw.line(screen, all_variables[i].colour, [701 + j, 200 - (all_variables[i].history[j]/all_variables[i].scale)], [700 + j, 200 - (all_variables[i].history[j - 1]/all_variables[i].scale)])
            screen.blit(font_one.render(i + ": " + str(all_variables[i].val), 1, all_variables[i].colour), [701, 200 - (all_variables[i].val/all_variables[i].scale)])
        pygame.draw.line(screen, [0, 0, 0], [0, 200], [899, 200])
        pygame.draw.line(screen, [0, 0, 0], [700, 0], [700, 399])
        screen.blit(font_one.render(str(t), 1, [0, 0, 0]), [20, 20])

        #General Pygame Management.------------------------
        for event in pygame.event.get():#See if program is over.
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):#End Program?
                inloop = False
                break


        pygame.display.update()#Update Screen
        pygame.display.flip()

        time.sleep(0.005)

        for event in pygame.event.get():#See if program is over a second time.
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):#End Program?
                inloop = False
                break
        #--------------------------------------------------
main()#Run the program.
