import pygame
pygame.init()
win = pygame.display.set_mode((640,360)) # создаем окно для игры 640 на 360 пикселей под размер backround img
pygame.display.set_caption('Game for Shit') # Заголовок для игры

# просто переменные, в последующем используем их как кординаты 
x = 50 
y = 280
width = 60
height = 71
speed = 5

isJump = False
jumpCount = 10

left = False
right = False
animation = 0

lastMove = 'right'
class snaryad:
	def __init__(self,x,y,radius,color,facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = 8 * facing
	def draw(self, win):
		pygame.draw.circle(win,self.color,(self.x, self.y), self.radius)

walkRight = [pygame.image.load('right_1.png'),pygame.image.load('right_2.png'),pygame.image.load('right_3.png'),
pygame.image.load('right_4.png'),pygame.image.load('right_5.png'),pygame.image.load('right_6.png')]

walkLeft = [pygame.image.load('left_1.png'),pygame.image.load('left_2.png'),pygame.image.load('left_3.png'),
pygame.image.load('left_4.png'),pygame.image.load('left_5.png'),pygame.image.load('left_6.png')]

playerStand = pygame.image.load('idle.png')

bg = pygame.image.load('bg-red.jpg')

clock = pygame.time.Clock()

def drawWindow():
	global animation
	win.blit(bg,(0,0))

	if animation + 1 >= 30:
		animation = 0

	if left:
		win.blit(walkLeft[animation // 5], (x,y))
		animation += 1
	elif right:
		win.blit(walkRight[animation // 5], (x,y))
		animation += 1
	else:
		win.blit(playerStand,(x,y))

	for bullet in bullets:
		bullet.draw(win)
	
	pygame.display.update() # обязательное для постоянного обновления событий 

run = True
bullets = []
while run: # создаем бесконечный цикл, что бы окно игры не закрывалось 
	clock.tick(30) # 30 fps

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run == False

	for bullet in bullets:
		if bullet.x < 640 and bullet.x > 0:
			bullet.x += bullet.vel
		else:
			bullets.pop(bullets.index(bullet))

	keys = pygame.key.get_pressed() # отслеживания события нажатия какой-либо кнопки 

	if keys[pygame.K_f]:
		if lastMove == "right":
			facing = 1
		else:
			facing = -1

		if len(bullets) < 5:
			bullets.append(snaryad (round(x + width //2), round(y + height // 2), 5, (255,0,0), facing))
	if keys[pygame.K_LEFT] and x > 5:  # x > 5 значит что меньше кардинаты 5 двигаться нельзя, что бы не вылезало за границы
		x -= speed
		left = True
		right = False
		lastMove = 'left'
	elif keys[pygame.K_RIGHT] and x < 640 - width - 5:
		x += speed
		left = False
		right = True
		lastMove = 'right'
	else:
		left = False
		right = False
		animation = 0
	if keys[pygame.K_ESCAPE]: # кнопка ecs закрывает игру
		pygame.quit()
	if not(isJump):
		if keys[pygame.K_SPACE]:
			isJump = True
	else:
		if jumpCount >= -10:
			if jumpCount < 0 :
				y += (jumpCount ** 2) / 2
			else:
				y -= (jumpCount ** 2) / 2			
			jumpCount -= 1
		else:
			isJump = False
			jumpCount = 10
	
	drawWindow()
	



	