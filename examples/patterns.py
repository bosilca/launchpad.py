#!/usr/bin/python
#
# Quick usage of "launchpad.py", LEDs and buttons.
# Works with all Launchpads: Mk1, Mk2, S/Mini and Pro.
# 
#
# ASkr 7/2013..1/2017
# www.askrprojects.net
#

import sys

try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("error loading launchpad.py")

import random
from pygame import time

# Lightshow
mode = None
initial_step = 150
matrices = [ [ [ [0, 0, 0] for i in range(8) ] for j in range(8) ] for k in range(2) ]
# create an instance
global lp

def main():
    global lp
    lp = launchpad.Launchpad()
    # check what we have here and override lp if necessary
    if lp.Check( 0, "pro" ):
        lp = launchpad.LaunchpadPro()
        if lp.Open(0,"pro"):
            print("Launchpad Pro")
            mode = "Pro"
			
    elif lp.Check( 0, "mk2" ):
        lp = launchpad.LaunchpadMk2()
        if lp.Open( 0, "mk2" ):
            print("Launchpad Mk2")
            mode = "Mk2"
			
    else:
        if lp.Open():
            print("Launchpad Mk1/S/Mini")
            mode = "Mk1"

    if mode is None:
        print("meh...")
        return


    # scroll "HELLO" from right to left
#	if mode == "Mk1":
#		lp.LedCtrlString( "HELLO ", 0, 3, -1 )
#	else:
#		lp.LedCtrlString( "HELLO ", 0, 63, 0, -1 )


	# random output
    print("---\nRandom madness. Stop by pressing Mixer.")
    if mode == "Mk1":
        print("Notice that sometimes, old Mk1 units don't recognize any button")
        print("events before you press one of the (top) automap buttons")
        print("(or power-cycle the unit...).")

    # Clear the buffer because the Launchpad remembers everything :-)
    lp.ButtonFlush()
    lp.LedAllOn(0)
    current = 0
    items = list()
    clear_matrix(matrices[current])
    step = initial_step
#    items.append(action_cross(4, 4, [25, 0, 0], time.get_ticks()+1000, 2*initial_step))
#    items.append(action_cross(2, 3, [0, 25, 0], time.get_ticks()+100, 2*initial_step))
#    items.append(action_cross(7, 0, [0, 0, 25], time.get_ticks(), 2*initial_step, 10))
#    items.append(action_cross(0, 7, [0, 0, 10], time.get_ticks(), 2*initial_step, 2))

#    items.append(action_single_cross(0, 7, [10, 10, 10], time.get_ticks(), 0, 10, 100))
#    items.append(action_single_cross(0, 7, [-10, 0, 0], 1000, 0, 10, 100))
#    items.append(action_single_cross(0, 7, [0, -10, 0], 1100, 0, 10, 100))
#    items.append(action_single_cross(0, 7, [0, 0, -10], 1200, 0, 10, 100))

#    items.append(action_cross(0, 7, [10, 10, 10], time.get_ticks(), 0, 2))
#    items.append(action_cross(4, 4, [-25, 0, 0], time.get_ticks()+10000, 4*initial_step))
#    items.append(action_cross(2, 3, [0, -25, 0], time.get_ticks()+10000, 4*initial_step))
#    items.append(action_single_cross_reverse(0, 7, [10, 10, 10], time.get_ticks(), step, 2))
    items.append(action_cross(        3, 4, [10,  0,  0], time.get_ticks() + 0 * step,          step, 20, 7*step, step))
    items.append(action_cross(        3, 4, [ 0, 10,  0], time.get_ticks() + 1 * step,          step, 20, 7*step, step))
    items.append(action_cross(        3, 4, [ 0,  0, 10], time.get_ticks() + 2 * step,          step, 20, 7*step, step))
##    items.append(action_cross_reverse(3, 4, [10,  0,  0], time.get_ticks() + 7*step, step, 20, 7*step, step))
#    items.append(action_cross_reverse(3, 4, [ 0, 10,  0], time.get_ticks() + 8*step, step, 20, 7*step, step))
#    items.append(action_cross_reverse(3, 4, [ 0,  0, 10], time.get_ticks() + 9*step, step, 20, 7*step, step))
    next_update = time.get_ticks()
    while 1:
        updates = 0
        but = lp.ButtonStateXY()
        if but != []:
            print( " button: ", but[0], but[1], but[2], "down" if but[2] == 127 else "up" )
            buttonX = but[0]
            buttonY = but[1]
            # If we exit on Mixer "down" a spurious "up" will be read the next time
            if 7 == buttonX and 0 == buttonY and 0 == but[2]: # Exit on Mixer up
                break
            if 0 == buttonY or 8 == buttonX:
                # We have a configuration button
                if 8 == buttonX:
                    step = initial_step * buttonY
                    print( "step set to ", step)
                if 0 == buttonX and 0 == buttonY and 0 == but[2]:
                    clear_matrix(matrices[current])
                    lp.LedAllOn(0)
                if 1 == buttonX and 0 == buttonY and 0 == but[2]:
                    clear_matrix(matrices[current])
                continue
            # When "down" create an action and move forward
            if 0 != but[2]:
                items.append(action_cross(but[0], but[1]-1, [20, 20, 20], time.get_ticks(), step, 1, 100, 2*step))
                updates += 1
                next_update = 0 # force an update

        # Noting is ready to be updated. Keep going
        if next_update > time.get_ticks():
            continue
        next_update = 10000000
        for item in items[:]:
            (update, when) = item.step(time.get_ticks(), matrices[current])
            if update < 0:
                print "release item {0}".format(item)
                # https://docs.python.org/2/reference/compound_stmts.html#for
                items.remove(item)
            else:
                updates += update
                print "item {0} -> ({1}, {2})".format(item, update, when)
                if next_update > when:
                     next_update = when

        if updates != 0:
            print "Need updates {0}".format(updates)
            print_matrix(matrices[current])
            current = update_matrix(current)
        time.wait(initial_step)

    # now crash it :-)
    print("\nNow let's crash PyGame...")
    print("Don't worry, that's just a bug in PyGame's MIDI implementation.")

    lp.Reset() # turn all LEDs off
    lp.Close() # close the Launchpad (will quit with an error due to a PyGame bug)

def clear_matrix(matrix):
    for x, row in enumerate(matrix):
        print row
        for y in range(1, len(row)):
            row[y] = [0, 0, 0]

def print_matrix(matrix):
    for row in matrix:
        for item in row:
            print "{0:02x}{1:02x}{2:02x} ".format(item[0], item[1], item[2]),
        print ""

def update_matrix(current):
    global lp
    save = 1
    for x, row in enumerate(matrices[current]):
        for y, val in enumerate(row):
            if row[y] != matrices[save][x][y]:
                if mode == "Mk1":
                    lp.LedCtrlXY(x, y+1, row[y], row[y])  # Each color between 0-3
                else:
                    lp.LedCtrlXY(x, y+1, row[y][0], row[y][1], row[y][2])  # Each color between 0-63
                matrices[save][x][y] = row[y]
    return 0

class action(object):
    def __init__(self, x, y, color, timestamp, timestep = 0, loops = 1, skip = -1):
        self.x = x
        self.y = y
        self.color = color
        self.timestamp = timestamp
        self.timestep = timestep
        self.loops = loops
        self.skip = skip
        self.trigger = timestamp
        self.name = "unnamed"

    def get_name(self):
        if "unnamed" == self.name:
            return "{0}".format(self)
        return self.name

    def step(self, timestamp, matrix):
        if self.loops <= 0:
            print "action {0} done (loops {1} <= 0)".format(self.get_name(), self.loops)
            return (-1, -1)
        if ((self.timestamp + self.timestep) > timestamp):
            print "action {0} not yet ready for update ({1} + {2}) >= {3}".format(self.get_name(), self.timestamp, self.timestep, timestamp)
            return (0, self.timestamp + self.timestep)
        return (1, timestamp)  # Might have something to do

    def __update__(self, x, y, distance, color, matrix):
        #print "Update object{0}: ({1}, {2}) distance {3} color {4}".format(self, x, y, distance, color)
        if 0 == distance:
            matrix[x][y] = [a+b for a,b in zip(matrix[x][y], color)]
            print "Update ({0}, {1}) -> {2} [{3}]".format(x, y, matrix[x][y], self.get_name())
            return 1
        action = 0
        if (x - distance) >= 0 and (x - distance) <= 7:
            matrix[x - distance][y] = [a+b for a,b in zip(matrix[x - distance][y], color)]
            action += 1
            print "Update ({0}, {1}) -> {2} [{3}]".format(x - distance, y, matrix[x - distance][y], self.get_name())
        if (x + distance) >= 0 and (x + distance) <= 7:
            matrix[x + distance][y] = [a+b for a,b in zip(matrix[x + distance][y], color)]
            action += 1
            print "Update ({0}, {1}) -> {2} [{3}]".format(x + distance, y, matrix[x + distance][y], self.get_name())
        if (y - distance) >= 0 and (y - distance) <= 7:
            matrix[x][y - distance] = [a+b for a,b in zip(matrix[x][y - distance], color)]
            action += 1
            print "Update ({0}, {1}) -> {2} [{3}]".format(x, y - distance, matrix[x][y - distance], self.get_name())
        if (y + distance) >= 0 and (y + distance) <= 7:
            matrix[x][y + distance] = [a+b for a,b in zip(matrix[x][y + distance], color)]
            action += 1
            print "Update ({0}, {1}) -> {2} [{3}]".format(x, y + distance, matrix[x][y + distance], self.get_name())
        return action

class action_line(action):
    def __init__(self, xs, ys, xe, ye, color, timestamp, timestep, loops = 1, skip = -1):
        action.__init__(self, xs, ys, color, timestamp, timestep, loops, skip)
        self.xe = xe
        self.ye = ye
        if (xe != xs) and (ye != ys):
            if abs(xs - xe) != abs(ys - ye):
                ye = ys
        self.xstep = 0 if xe == xs else (xe - xs) / abs(xe - xs)
        self.ystep = 0 if ye == ys else (ye - ys) / abs(ye - ys)
        self.distance = 0
        self.next_trigger = timestamp

    def __update__(self, color):
        x = self.xs + self.distance * self.xstep
        y = self.ys + self.distance * self.ystep
        if ((self.xstep < 0) and (x < xe)) or \
           ((self.xstep > 0) and (x > xe)) or \
           ((self.ystep < 0) and (y < ye)) or \
           ((self.ystep > 0) and (y > ye)):
            return 0
        matrix[x][y] = [a+b for a,b in zip(matrix[x][y], color)]
        return 1

    def step(self, timestamp, matrix):
        while True:
            (val, when) = super(action_line, self).step(timestamp, matrix)
            if val <= 0:
                return (actions + val, when)
            last_action = self.__update__(self.color)
            if 0 == last_action:
                if 0 < self.loops:
                    self.loops -= 1
                    self.next_trigger = timestamp + self.skip
                    break
                else:
                    self.next_trigger = timestamp + self.timestep

class action_single_cross(action):
    '''
    Basic class for lighting a cross across the pad. The cross is centered at the
    (x,y) position, and progresses every 'step' toward the exterior, starting from
    timestamp. Once all the points of the cross exit the visible surface, the
    entire operation is started again after 'skip' units of time. The operation
    is repeated 'loops' number of times.
    '''
    def __init__(self, x, y, color, timestamp, timestep, loops = 1, skip = -1):
        '''
        :param x:
        :param y:
        :param color:
        :param timestamp:
        :param timestep:
        :param loops:
        :param skip:
        '''
        action.__init__(self, x, y, color, timestamp, timestep, loops)
        if -1 == skip:
            maxval = max(max(x, y), 7 - min(x, y))
            skip = maxval * timestep
        self.skip = skip
        print "Create action_single_cross object pos ({0}, {1}) color {2} timestamp {3} timestep {4} loops {5} skip {6}".format(self.x, self.y, self.color, self.timestamp, self.timestep, self.loops, self.skip)
        self.distance = 0

    def step(self, timestamp, matrix):
        actions = 0
        last_action = 0
        while True:
            (val, when) = super(action_single_cross, self).step(timestamp, matrix)
            if val <= 0:
                return (actions + val, when)

            last_action = self.__update__(self.x, self.y, self.distance, self.color, matrix)
            self.distance = self.distance + 1
            self.timestamp = timestamp
            actions += last_action
            if (0 != self.timestep) or (last_action <= 0):
                break

        # reboot the object
        if 0 == last_action:
            self.distance = 0
            self.loops -= 1
            self.timestamp += self.skip
            # We only need to keep the when
            (ignore, when) = super(action_single_cross, self).step(timestamp, matrix)

        return (actions, when)

class action_single_cross_reverse(action):
    '''
    Basic class for lighting a cross across the pad. The cross is centered at the
    (x,y) position, and progresses every 'step' from the exterior, starting from
    timestamp. Once all the points of the cross reach the center position, the
    entire operation is started again after 'skip' units of time. The operation
    is repeated 'loops' number of times.
    '''
    def __init__(self, x, y, color, timestamp, timestep, loops = 1, skip = -1):
        '''
        :param x:
        :param y:
        :param color:
        :param timestamp:
        :param timestep:
        :param loops:
        :param skip:
        '''
        action.__init__(self, x, y, color, timestamp, timestep, loops)
        self.distance = max(max(x, y), 7 - min(x, y))
        if -1 == skip:
            skip = self.distance * timestep
        self.skip = skip
        print "Create action_single_cross_reverse object pos ({0}, {1}) color {2} timestamp {3} timestep {4} loops {5} skip {6}".format(self.x, self.y, self.color, self.timestamp, self.timestep, self.loops, self.skip)

    def step(self, timestamp, matrix):
        actions = 0
        last_action = 0
        while True:
            (val, when) = super(action_single_cross_reverse, self).step(timestamp, matrix)
            if val <= 0:
                return (actions + val, when)

            last_action = self.__update__(self.x, self.y, self.distance, self.color, matrix)
            self.distance = self.distance - 1
            self.timestamp = timestamp
            actions += last_action
            if (0 != self.timestep) or (last_action <= 0) or (self.distance < 0):
                break

        # reboot the object
        if (0 == last_action) or (self.distance < 0):
            self.distance = max(max(self.x, self.y), 7 - min(self.x, self.y))
            self.loops -= 1
            self.timestamp += self.skip
            # We only need to keep the when
            (ignore, when) = super(action_single_cross_reverse, self).step(timestamp, matrix)

        return (actions, when)


class action_cross(action_single_cross):
    '''
    An extension to the action_single_cross where the initial cross is followed
    after 'fadedelay' units of time by it's complementary (the result is that the
    lights are turned to their original color.
    '''
    def __init__(self, x, y, color, timestamp, timestep, loops = 1, skip = -1, fadedelay = -1):
        '''
        :param x: the x starting position of the cross
        :param y: the y starting position of the cross
        :param color: the color of the initial cross
        :param timestamp: the initial moment of the apperance of the first element of the cross
        :param timestep: the time difference between 2 successive points of the cross
        :param loops: the number of time a cross will be generated. Default to -1 to signal a single repetition
        :param skip: how many timesteps will exist between 2 loops
        :param fadedelay: the timestep after each a point will fade. A negative value prevents any fading.
        '''
        self.fadedelay = fadedelay
        if fadedelay == -1:
            maxval = max(max(x,y), 7 - min(x,y))
            self.fadedelay = maxval * timestep
        if skip == -1:
            skip = self.fadedelay
        print "Create action_cross object fadedelay {0}".format(self.fadedelay)
        action_single_cross.__init__(self, x, y, color, timestamp, timestep, loops, skip)
        self.fader = None
        if fadedelay != -1:
            self.fader = action_single_cross(x, y, [-v for v in color], timestamp + self.fadedelay,
                                             timestep, loops, self.skip)

    def step(self, timestamp, matrix):
        (val, when) = super(action_cross, self).step(timestamp, matrix)
        if None != self.fader:
            (fval, fwhen) = self.fader.step(timestamp, matrix)
        else:
            (fval, fwhen) = (val, when)
        if when == -1:
            when = fwhen
        if fwhen == -1:
            fwhen = when
        return (max(val, fval), min(when, fwhen))

class action_cross_reverse(action_single_cross_reverse):
    '''
    An extension to the action_single_cross class, where the cross instead of being
    reversed from the center is reversed from the extremities. This gives a movement
    of back-and-forth.
    '''
    def __init__(self, x, y, color, timestamp, timestep, loops = 1, skip = -1, fadedelay = -1):
        self.fadedelay = fadedelay
        if -1 == fadedelay:
            maxval = max(max(x, y), 7 - min(x, y))
            self.fadedelay = maxval * timestep
        if skip == -1:
            skip = self.fadedelay
        print "Create action_cross_reverse object fadedelay {0}".format(self.fadedelay)
        action_single_cross_reverse.__init__(self, x, y, color, timestamp, timestep, loops, skip)
        self.fader = None
        if fadedelay != -1:
            self.fader = action_single_cross_reverse(x, y, [-v for v in color], timestamp + self.fadedelay,
                                                     timestep, loops, self.skip)

    def step(self, timestamp, matrix):
        (val, when) = super(action_cross_reverse, self).step(timestamp, matrix)
        if None != self.fader:
            (fval, fwhen) = self.fader.step(timestamp, matrix)
        else:
            (fval, fwhen) = (val, when)
        if when == -1:
            when = fwhen
        if fwhen == -1:
            fwhen = when
        return (max(val, fval), min(when, fwhen))

if __name__ == '__main__':
    main()

