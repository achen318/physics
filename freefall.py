from vpython import *
#Web VPython 3.2

k = 0.5   # drag constant
t = 0     # time
dt= 0.01  # increment in time
m = 1     # mass
A = 1     # area
g = -9.81 # gravitational acceleration
vy= 50    # velocity in the y-direction
y_init = 10
yy = y_init
ball = sphere(pos=vector(0,y_init,0), radius = 0.5, color=color.red)

g1 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Y Position"), align='left')
yyDots=gdots(color=color.green, graph=g1)

g2 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Velocity"), align='left')
vyDots=gdots(color=color.red, graph=g2)

scene.camera.pos=vector(0, 5, 10) # This tells VPython to view the scene from the position (0,5,10)


while yy>0:
    rate(1/dt)
    
    fy = m*g - k * A * vy # Net force in the y direction: Fg - Fd
    ay = fy/m # Acceleration in the y direction
    vy = vy + ay*dt # Update the velocity in the y direction
    yy = yy + vy*dt # Update the position in the y direction
    
    ball.pos = vector(0, yy, 0) # Update the ball's visual position
    
    yyDots.plot(t,yy) # Plot position vs. time
    vyDots.plot(t,vy) # Plot velocity vs. time
    
    t = t + dt # Increment the time
