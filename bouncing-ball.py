import simpleguitk as simplegui
import random
import math

DOMAIN_WIDTH = 600
DOMAIN_HEIGHT = 400
DOMAIN_DIAM = 400
BALL_RADIUS = 10
BOUND = 4

COLOR_LIST = ["Red", "Blue", "White", "Yellow", "Green"]
ACCELERATION = 0.5

def dot(vec1, vec2):
	return vec1[0] * vec2[0] + vec1[1] * vec2[1]
	
def distance(p, q):
	return math.sqrt( (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 )

class RectDomain:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.diag_grad = (height - 1.0 - BOUND)/(width - 1.0 - BOUND)
		
	def __str__(self):
		return "Domain size = " + str(self.width) + "X" + str(self.height)
	
	def inside(self, center, radius):
		if center[0] < BOUND + radius or center[1] < BOUND + radius or center[0] > self.width - 1 - radius or center[1] > self.height - 1 - radius:
			return False
		else:
			return True
	
	def random_pos(self, radius):
		center = [0.0, 0.0]
		center[0] = random.random() * (self.width - 2.0 * (radius + BOUND)) + radius + BOUND
		center[1] = random.random() * (self.height - 2.0 * (radius + BOUND)) + radius + BOUND
		return center
		
	def normal(self, pos):
		if pos[1] - BOUND > self.diag_grad * (pos[0] - BOUND) and pos[1] - BOUND > -self.diag_grad * (pos[0] - self.width + 1):
			return [0.0, -1.0]
		if pos[1] - BOUND > self.diag_grad * (pos[0] - BOUND) and pos[1] - BOUND < -self.diag_grad * (pos[0] - self.width + 1):
			return [1.0, 0.0]
		if pos[1] - BOUND < self.diag_grad * (pos[0] - BOUND) and pos[1] - BOUND > -self.diag_grad * (pos[0] - self.width + 1):
			return [-1.0, 0.0]
		if pos[1] - BOUND < self.diag_grad * (pos[0] - BOUND) and pos[1] - BOUND < -self.diag_grad * (pos[0] - self.width + 1):
			return [0.0, 1.0]
	
	def draw(self, canvas):
		canvas.draw_polygon([(BOUND, BOUND), (self.width - 1, BOUND), (self.width - 1, self.height - 1), (BOUND, self.height - 1)], 2, 'Gray')

class CircleDomain:
	def __init__(self, Radius, origin):
		self.Radius = Radius
		self.origin = origin
		
	def __str__(self):
		return "Circular Domain of Radius " + str(self.Radius)
		
	def inside(self, center, radius):
		if distance(center, self.origin) > self.Radius - radius:
			return False
		else:
			return True
			
	def random_pos(self, radius):
		center = [0.0, 0.0]
		radial = random.random() * (self.Radius - radius)
		arg = random.random() * math.pi
		center[0] = self.origin[0] + radial * math.cos(arg)
		center[1] = self.origin[0] + radial * math.sin(arg)
		return center
	
	def normal(self, pos):
		n1 = (self.origin[0] - pos[0]) / distance(self.origin, pos)
		n2 = (self.origin[1] - pos[1]) / distance(self.origin, pos)
		return [n1, n2]
	
	def draw(self, canvas):
		canvas.draw_circle(self.origin, self.Radius, 2, "Gray")

class Ball:
	def __init__(self, radius, color, domain):
		self.radius = radius
		self.color = color
		self.domain = domain
		
		self.pos = self.domain.random_pos(self.radius)
		self.vel = [random.random() * 2 + 3.0, random.random() * 2 + 3.0]
	
	def __str__(self):
		return "Ball of color " + self.color + " with radius " + str(self.radius) + " at position " + str(self.pos)
	
	def bounce(self):
		norm = self.domain.normal(self.pos)
		norm_length = dot(self.vel, norm)
		self.vel[0] = self.vel[0] - 2 * norm_length * norm[0]
		self.vel[1] = self.vel[1] - 2 * norm_length * norm[1]
	
	def update(self):
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]
		if not self.domain.inside(self.pos, self.radius):
			self.bounce()
	
	def draw(self, canvas):
		canvas.draw_circle(self.pos, self.radius, 1, self.color, self.color)

def draw(canvas):
	ball.update()
	field.draw(canvas)
	ball.draw(canvas)
	
def change_velocity(key):
	if key==simplegui.KEY_MAP["left"]:
		ball.vel[0] += -ACCELERATION
	if key==simplegui.KEY_MAP["right"]:
		ball.vel[0] += ACCELERATION
	if key==simplegui.KEY_MAP["down"]:
		ball.vel[1] += ACCELERATION
	if key==simplegui.KEY_MAP["up"]:
		ball.vel[1] += -ACCELERATION
	
#field = RectDomain(DOMAIN_WIDTH, DOMAIN_HEIGHT)
field = CircleDomain(DOMAIN_DIAM/2, [DOMAIN_DIAM/2.0 + 10, DOMAIN_DIAM/2.0 + 10])
ball = Ball(BALL_RADIUS, random.choice(COLOR_LIST), field)

#frame = simplegui.create_frame("Ball Physics", DOMAIN_WIDTH, DOMAIN_HEIGHT)
frame = simplegui.create_frame("Ball Physics", DOMAIN_DIAM + 20, DOMAIN_DIAM + 20)
frame.set_keydown_handler(change_velocity)
frame.set_draw_handler(draw)

frame.start()