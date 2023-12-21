from vpython import *
#Web VPython 3.2


# ---------- Constants ----------
G = 6.67e-11
dt = 50000
zero = vector(0, 0, 0)


# ---------- Methods ----------
def create_body(name, mass, radius, distance, inclination, eccentricity, texture):
    theta = random() * pi / 4

    return sphere(
        name=name,
        mass=mass,
        radius=radius * 50,
        angle=theta,
        pos=distance * vector(cos(theta), sin(theta), sin(radians(inclination))),
        vel=zero,
        acc=zero,
        texture=texture,
        make_trail=distance > 0,
        interval=1
    )


def create_planet(name, mass, diameter, distance, inclination, eccentricity, texture, star):
    planet = create_body(name, mass, diameter / 0.0002, distance, inclination, eccentricity, texture)
    text = label(pos=planet.pos, text=planet.name, height=10)

    v = sqrt(G * star.mass / distance)
    theta = planet.angle

    planet.vel = v * vector(-sin(theta), cos(theta), 0)

    return planet, text


def gravity(star, satellite):
    rad = satellite.pos - star.pos
    force = -(G * satellite.mass * star.mass / (rad.mag * rad.mag)) * rad.hat
    return force


def update(star, planet):
    body, text = planet

    body.acc = gravity(star, body) / body.mass
    body.vel += body.acc * dt
    body.pos += body.vel * dt

    text.pos = body.pos


# ---------- Setup ----------
scene = canvas(width=720, height=720)


def update_dt():
    global dt
    dt = slide.value
    wt.text = f"dt = {slide.value}"


slide = slider(min=0, max=100000, step=100, value=50000, bind=update_dt)
wt = wtext(text=f"dt = {slide.value}")

sun = create_body("Sun"    , 1.9891e30, 6.957e8, 0       , 0  , 0    , "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Solarsystemscope_texture_8k_sun.jpg/800px-Solarsystemscope_texture_8k_sun.jpg")
planets = [
    create_planet("Mercury", 0.330e24 , 4879   , 57.9e9  , 7.0, 0.206, "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Solarsystemscope_texture_8k_mercury.jpg/800px-Solarsystemscope_texture_8k_mercury.jpg"            , sun),
    create_planet("Venus"  , 4.84e24  , 12104  , 108.2e9 , 3.4, 0.007, "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Solarsystemscope_texture_8k_venus_surface.jpg/800px-Solarsystemscope_texture_8k_venus_surface.jpg", sun),
    create_planet("Earth"  , 5.97e24  , 12756  , 149.6e9 , 0.0, 0.017, "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Solarsystemscope_texture_8k_earth_daymap.jpg/800px-Solarsystemscope_texture_8k_earth_daymap.jpg"  , sun),
    create_planet("Mars"   , 0.642e24 , 6792   , 228.0e9 , 1.8, 0.094, "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Solarsystemscope_texture_8k_mars.jpg/800px-Solarsystemscope_texture_8k_mars.jpg"                  , sun),
    create_planet("Jupiter", 1898e24  , 142984 , 778.5e9 , 1.3, 0.049, "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Solarsystemscope_texture_8k_jupiter.jpg/800px-Solarsystemscope_texture_8k_jupiter.jpg"            , sun),
    create_planet("Saturn" , 568e24   , 120536 , 1432.0e9, 2.5, 0.052, "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Solarsystemscope_texture_8k_saturn.jpg/800px-Solarsystemscope_texture_8k_saturn.jpg"              , sun),
    create_planet("Uranus" , 86.8e24  , 51118  , 2867.0e9, 0.8, 0.047, "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Solarsystemscope_texture_2k_uranus.jpg/800px-Solarsystemscope_texture_2k_uranus.jpg"              , sun),
    create_planet("Neptune", 102e24   , 49528  , 4515.0e9, 1.8, 0.010, "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Solarsystemscope_texture_2k_neptune.jpg/800px-Solarsystemscope_texture_2k_neptune.jpg"            , sun)
]

# ---------- Main Loop ----------
t = 0

while True:
    rate(1000)

    for planet in planets:
        update(sun, planet)

    t += dt
