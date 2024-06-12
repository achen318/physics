from vpython import *

# ------------------------- Fields -------------------------

# constants that are to be defined 
q = 1.6e-10 # charge / current is defaulted to this (proxy variable that makes it easier for sliders to work) 
k = 9e9 # 1/ 4pi epsilon naught 
u = 4e-7 * pi # permittivity constant 
e = 1e-9 # makes this easier 


#this array contains all of the object's *CURVES*, not necessarily the object itself 
shapeArr = [] 

#this array contains the final curve 
pathArr = [] 

#this array contains all of the vector objects
vecArr = [] 

#for the extrusions only! 
extArr = []

class Electric:
    # Initialize an electric field object given a shape
    def __init__(self, shape):
        self.shape = shape  # Loop or Surface object

    # Get the E-field vector at a point (x, y) from the shape
    def get_dE_vec(self, areas, x, y, q):
        dE = vec(0, 0, 0)

        # For an (x, y), accumulate the field vector dE
        # by summing the field vectors from each unit point
        for dA in areas:
            # Get the vector pointing from dA to (x, y)
            r = vec(x - dA[0], y - dA[1], 0)

            # Add to dE vector with Coulomb's Law
            dE += k * q / r.mag**2 * r.hat

        return dE

    # Draw the E-field for every unit point in the scene
    def draw(self, q):
        # Get a list of [x, y] unit points in the shape
        # Loop: path, Surface: area
        areas = self.shape.get_areas()

        # For each unit point in the scene (x, y)
        # (Jason brute forced the dimensions of the scene to be -10 to 10 in both x and y)
        for x in range(-10, 10):
            for y in range(-10, 10):
                # The vector's tail is at (x, y), with direction/magnitude from dE
                tail = vec(x, y, 0)
                dE = self.get_dE_vec(areas, x, y, q)

                # Normalize the magnitude with arctan to obtain opacity in [0, 1)
                op = 2 * atan(dE.mag) / pi

                # Draw the normalized vector with differing opacity at (x, y)
                arr = arrow(pos=tail, axis=dE.hat, shaftwidth=0.1, opacity=op)
                vecArr.append(arr) 

class Magnetic:
    # Initialize a magnetic field object given a shape
    def __init__(self, shape):
        self.shape = shape  # Loop or Surface object

    # Get the B-field vector at a point (x, y) from the shape
    def get_dB_vec(self, loop, x, y, q):
        dB = vec(0, 0, 0)

        # For an (x, y), accumulate the field vector dB
        # by summing the field vectors from each unit length element
        for i in range(len(loop) - 1):
            # Get the vector pointing from dA to (x, y)
            r = vec(x - loop[i].x, y - loop[i].y, 0)

            # Get an infinitesimal length element
            dL = loop[i + 1] - loop[i]
            
            radialDist = mag(r) 
            
            if (radialDist < 0.25): 
                radialDist = 0.25 

            # Add to dB vector with Biot-Savart's Law
        
            prod = cross(dL, r.hat) 
            
        
            dB += prod/  (radialDist ** 2 )

        return dB / (4 * pi) * q * u 

    # Draw the B-field for every unit point in the scene
    def draw(self, q):
        # Get a list of [x, y] unit points in the shape
        # Loop: path, Surface: area 
        # Area is a misnomer here (refers to the closed shape that the loop forms) 
        loop = self.shape.get_areas()

        # Convert that list to a list of 3D vectors
        loop = [vec(x, y, 0) for x, y in loop]

        # For each unit point in the scene (x, y)
        # (Jason brute forced the dimensions of the scene to be -10 to 10 in both x and y)
        for x in range(-10, 10, 0.5):
            for y in range(-10, 10, 0.5):
                # The vector's tail is at (x, y), with direction/magnitude from dB
                tail = vec(x, y, 0)
                dB = self.get_dB_vec(loop, x, y, q)


                # Draw the vectors with a scaling factor of 3e16 so you can actually notice the difference 
                if dB.z > 0: 
                    arr = arrow(pos=tail, axis=dB * 3e16, shaftwidth=0.3, color=color.orange)
                
                else: 
                    arr = arrow(pos=tail, axis=dB * 3e16, shaftwidth=0.3, color=color.red)
    
                vecArr.append(arr) 

# ------------------------- Shapes -------------------------


class Loop:
    # Initialize a loop object given a color
    def __init__(self, shape_color):
        self.path = []  # stores 3D vector objects
        self.shape_color = shape_color

    # Draw the loop by interpolating the points the mouse hovers over
    def draw(self):
        self.obj = curve(pos=self.path, color=self.shape_color)

    # Close the figure, then draw the loop
    def up(self):
        # Add the initial point as a terminal point
        self.path.append(self.path[0])
        self.draw()

    # Get a list of simple closed path points [x, y]
    def get_areas(self):
        areas = []  # stores 2D [x, y] lists

        for p in self.path:
            pos = [p.x, p.y]

            # Add unique points and initial point only
            if pos not in areas or pos == areas[0]:
                areas.append(pos)

        return areas


class Surface:
    # Initialize a surface object given a color
    def __init__(self, shape_color):
        self.path = []  # stores 3D vector objects
        self.shape_color = shape_color

    # Draw the boundary by interpolating the points the mouse hovers over
    def draw(self):
        self.obj = curve(pos=self.path, color=self.shape_color)

    # Close the figure, then draw the boundary
    def up(self):
        # Add the initial point as a terminal point
        self.path.append(self.path[0])
        self.draw()

        # Add simple closed path points [x, y] to areas
        shape = []  # stores 2D [x, y] lists
        for p in self.path:
            pos = [-p.x, p.y]  # no clue why x is negative but it works!

            # Add unique points and initial point only
            if pos not in shape or pos == shape[0]:
                shape.append(pos)

        # Extrude the boundary to a closed surface from z=0 to z=1
        self.ext = extrusion(
            shape=shape, path=[vec(0, 0, 0), vec(0, 0, 1)], color=self.shape_color
        )

    # Get a list of unit points [x, y] that are within the boundary
    # (Credits to Tracey for suggesting this algorithm!)
    def get_areas(self):
        areas = []  # stores 2D [x, y] lists

        # Compile a list of integer x values at each integer y level
        y_to_xs = {}
        for p in self.path:
            x = round(p.x)
            y = round(p.y)

            if y in y_to_xs:
                y_to_xs[y].append(x)
            else:
                y_to_xs[y] = [x]

        # For each integer y level, sort the integer x values
        for y, xs in y_to_xs.items():
            y_to_xs[y] = sorted(xs)

        # For each integer y level, check if each integer x value is within the boundary
        for y, xs in y_to_xs.items():
            add = False

            for x in range(xs[0], xs[-1]):
                # If we encounter a boundary, toggle in/out
                if x in xs:
                    add = not add

                # If we are "inside" the boundary, add the unit point to areas
                else:
                    if add:
                        areas.append([x, y])

        return areas

# ------------------------- Main -------------------------


scene = canvas(width=500, height=500) # init canvas 
scene.camera.pos = vector(0, 0, 1)
scene.center = vector(0, 0, 0)  # the object is centered at (0, 0, 0) for convienence
scene.userspin = False  # restrict it to be practically 2D
scene.userzoom = False  # stop the user from zooming too far in/out
scene.autoscale = False


#helper function for clear 
def clearHelper (): 
    
    # this is to clear everything from the vector field 
    for x in vecArr: 
        x.visible = False
        del x 
    
    #clear the vectors from system memory  
    vecArr.clear() 
    
    # reset shape to none 
    shape = None 
    
    


#clear everything by removing them from the graphics processing thingy-ma-bob 
#then, delete it 
def clear(b): 
    clearHelper() 
    
    # this is to clear the extrusion 
    for x in shapeArr: 
        x.visible = False 
        del x 
        
    # clear every jordan curve from graphics processing    
    for x in pathArr: 
        x.visible = False
        del x 
    
    #delete everything from reply 
    pathArr.clear()
    shapeArr.clear()
    
    # clear extrusion (if there is) from graphics processing 
    for x in extArr: 
        x.visible = False
        del x 
    #remove from memory 
    extArr.clear() 
    
#dummy method to just do nothing :-) 
def do_nothing(ev):
    pass

# this allows you to not fill the surface up 
def surface_loop_toggle(ev):
    # If B-field is selected, disable surface and enable loop
    surface_toggle.disabled = b_toggle.checked
    loop_toggle.checked = b_toggle.checked
    clear() #clears everything else 

#--------Define all the buttons that we have----- 
loop_toggle = radio(
    name="shape",
    text="Loop",
    pos=scene.title_anchor,
    bind=do_nothing,
    checked=True,
)
surface_toggle = radio(
    name="shape", text="Surface     ", pos=scene.title_anchor, bind=do_nothing
)
e_toggle = radio(
    name="field",
    text="E-field (red)",
    pos=scene.title_anchor,
    bind=surface_loop_toggle,
    checked=True,
)
b_toggle = radio(
    name="field",
    text="B-field (blue)     ",
    pos=scene.title_anchor,
    bind=surface_loop_toggle,
)


#this is a button to restart (cannot be radio) 
button(text="Restart", 
       pos=scene.title_anchor, 
       bind = clear )
       

#function to alter Charge/current (       
def alterChargeOrCurrent(s): 
    q = s.value * 1e-10 
    wt.text = '{:1.2f}'.format(s.value) # f-string! to display the values 
    clearHelper() 
  
    if e_toggle.checked:
        Electric(shape).draw(q) #alter the vector field based on the charge 
    else:
        Magnetic(shape).draw(q)

#slider to update the value of charge/current 
currSlider = slider(bind=alterChargeOrCurrent, vertical=False, min= -5.1, max=5.1,step=0.1, value = 1.0, length= 500 ,width=10 )

wt = wtext(text='{:1.2f}'.format(currSlider.value))  #dynamic text! 

shape = None

while True:
    ev = scene.waitfor("mousedown mousemove mouseup")

    # clear everything before we start the drawing 
    if ev.event == "mousedown":
        scene.mouse.click = True
        clear()

        # Red E-field, Blue B-field
        shape_color = color.red if e_toggle.checked else color.blue

        # Loop or Surface
        shape = Loop(shape_color) if loop_toggle.checked else Surface(shape_color)
    elif ev.event == "mousemove":
        if scene.mouse and scene.mouse.click:
            shape.path.append(scene.mouse.pos)
            shape.draw()
            #append to the shape array so we can delete it later 
            shapeArr.append(shape.obj)
    else:
        scene.mouse.click = False

        if shape:
            try:
                shape.up()
            except Exception: #this is to attempt to fix any bugs that may occur (if the shape isn't a proper jordan curve) 
                clear()
                continue
            
            #append the shape to the array so we can delete it later 
            shapeArr.append(shape.obj)
            
            #append the outline to the array so we can delete it later 
            for x in shape.path: 
                pathArr.append(x) 
                
            #append the extrusion to the drawings array 
            if surface_toggle.checked: 
                extArr.append(shape.ext)
            
            #draw everything! 
            if e_toggle.checked:
                Electric(shape).draw(q)
            else:
                Magnetic(shape).draw(q)

