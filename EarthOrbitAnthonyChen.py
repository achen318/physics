from vpython import *
#Web VPython 3.2

scene = canvas(width=800, height=800)

g1 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Energy"), align='left', scroll=True, xmin=0, xmax=7200000)
kDots=gdots(color=color.red, graph=g1)
uDots=gdots(color=color.green, graph=g1)
totDots=gdots(color=color.purple, graph=g1)

G = 6.67e-11

sun = sphere(pos = vector(0, 0, 0), radius = 12e9, texture = "https://i.imgur.com/XdRTvzj.jpeg", shininess = 0, make_trail = True);
earth = sphere(pos = vector(1.5e11, 0, 0), radius = 6.37e9, texture=textures.earth, make_trail = True, interval=10, retain=50);

# Please note that I made the radii of the earth and the Sun much too large, just so they're more visible. 
# All other quantities are realistic.

sun.mass = 1.9891e30
earth.mass = 5.97e24

circ_vel = sqrt(G*sun.mass/earth.pos.x)

sun.velocity = vector(0,0,0)
earth.velocity = vector(0, 2e4, 0) # elliptical
#earth.velocity = vector(0,circ_vel,0) # circular

sun.acc = vector(0,0,0)
earth.acc = vector(0,0,0)

# The last 6 lines added attributes to the definitions of the earth and the sun. I COULD have added those attributes
# in the original call to sphere(), but I had limited space in the line.

def gravity(star, satellite):
    rad = (satellite.pos - star.pos)
    force = -(G*satellite.mass*star.mass/(rad.mag*rad.mag))*rad.hat
    return force

def kinetic(object):
    return object.mass * (object.velocity.mag)**2 / 2

def potential(obj1, obj2):
    return -G * obj1.mass * obj2.mass / (obj1.pos - obj2.pos).mag

t=0; dt=3600
    
while((earth.pos-sun.pos).mag>(earth.radius+sun.radius)):
    rate(1000)

    earth.acc = gravity(sun,earth)/earth.mass
    sun.acc = gravity(earth,sun)/sun.mass

    earth.velocity = earth.velocity + earth.acc*dt
    sun.velocity = sun.velocity + sun.acc*dt

    earth.pos = earth.pos + earth.velocity*dt
    sun.pos = sun.pos + sun.velocity*dt
    
    if t % 36000 == 0:
        k = kinetic(earth) + kinetic(sun)
        u = potential(earth, sun)

        kDots.plot(t, k)
        uDots.plot(t, u)
        totDots.plot(t, k + u)

    t = t+dt
