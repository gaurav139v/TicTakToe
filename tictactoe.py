import random, time, pygame, sys
# O is the computer symbol
# X is the user symbol
# _ is the blank space

symbol = ['O','X']
# coordinate of the 9 boxes [top-left corner]
coordinate = [(246,146),(350,146),(454,146),(246,250),(350,250),(454,250),(246,354),(350,354),(454,354)]
play = 0 # 0 for computer play and 1 for 2 player
win = 0 # 1 if anyone win

# colors
white = (255,255,255)
black = (0,0,0)
intro = (255,255,185)
background = (204,232,236)
#blue = (165,217,245)
blue = (131,146,197)
green = (24,135,28)

# interface
pygame.init()
window_width = 800
window__height = 600

window = pygame.display.set_mode((window_width,window__height))
pygame.display.set_caption('TicTacToe')
clock = pygame.time.Clock()

white_img = pygame.image.load(r'white.png') # white background of the black space
user_sym = pygame.image.load(r'cross.png')
com_sym = pygame.image.load(r'circle.png')
logo = pygame.image.load(r'logo.png')

# user move in the computer play
def user_chance(pos):
	''' user makes his move '''
	global remain # list that store position of the blank space
	
	# check clicked position with all the 9 position
	for i in range(0,9):
		cord = coordinate[i]
		if cord[0]< pos[0] < cord[0] + 100 and cord[1]< pos[1] < cord[1] + 100:
			# asign the user symbol if the place is blank
			if game[i] == '_':
				remain = asign(i,'X',user_sym)
				return 1
		
def asign(index,sign,img):
	'''Asign the value to the index '''
	final_List = remain[:]
	
	game[index] = sign
	window.blit(img,coordinate[index])
	pygame.display.update()
	
	# delay between the user and computer move
	if sign == 'X':
		time.sleep(1)
	
	# remove the asign position from the remain list
	for i in range(0,len(remain)):
		if remain[i] == index:
			left_Side = remain[0:i]
			right_Side = remain[i+1:]
			final_List = left_Side + right_Side	
	return final_List 

def coumputer_chance():
	''' computer make its move  '''
	global remain # blank positions 
	
	# display the message when the match draw
	if len(remain) == 0:
		message('Match Draw',400,80,50,black)
		pygame.display.update()
		return 0

	# check the first method for the computer move	
	index = firstMethod()
	if index != None:
		remain = asign(index, 'O',com_sym)
		# if the computer win then display message
		if win_flag == 0:
			message('Computer-Wins!',400,80,50,black)
			pygame.display.update()
			return 1
	else:
		# go for the second method for the computer move
		index = secondMethod()
		remain = asign(index, 'O',com_sym)	

def firstMethod():
	""" give the index of wining box or prevent the user win """
	count = 0
	
	for k in range(0,2):
		temp1 = 1 
		temp2 = 2
		loopEnd = 7
		loopDiff = 3
		global win_flag 
		win_flag = k
		
		for j in range(0,2):
			
			for i in range(0,loopEnd,loopDiff):
				count = 0
				if game[i] == symbol[k]:
					count = count + 1
				if game[i + temp1] == symbol[k]:
					count = count + 1
				if game[i + temp2] == symbol[k]:
					count = count + 1
				if count == 2:
					if game[i] == '_':
						return i 
						
					elif game[i + temp1] == '_':
						return i + temp1
						
					elif game[i + temp2] == '_':
						return i + temp2
				else:
					count = 0                                        
								
			temp1 = 3
			temp2 = 6
			loopEnd = 3
			loopDiff = 1
			count = 0
		                                
		temp1 = 0
		temp2 = 8

		for i in range(0,2):
			count = 0
			if game[i + temp1] == symbol[k]:
				count = count + 1
			
			if game[4] == symbol[k]:
				count = count + 1

			if game[i + temp2] == symbol[k]:
				count = count + 1

			if count == 2:
				if game[i + temp1] == '_':
					return i + temp1 
					
				elif game[4] == '_':
					return 4
					
				elif game[i + temp2] == '_':
					return i + temp2
				else:
					temp1 = 1
					temp2 = 5	
			else:
				temp1 = 1
				temp2 = 5
		
def secondMethod():
	''' give the index of the best possible box '''
	sym = ['X','O']
	priority = [0,0,0,0,0,0,0,0,0]

	if len(remain) == 6:
		index = specialCase()
		if index != None:
			return index
	
	for k in range(0,2):
		temp1 = 1
		temp2 = 2
		loopEnd = 7
		loopDiff = 3

		for j in range(0,2):
			for i in range(0,loopEnd,loopDiff):
				if game[i] != sym[k]:
					if game[i + temp1] != sym[k]:
						if game[i + temp2] != [k]:
							priority[i] = priority[i] + 1
							priority[i + temp1] = priority[i + temp1] + 1
							priority[i + temp2] = priority[i + temp2] + 1
					
			temp1 = 3
			temp2 = 6
			loopEnd = 3
			loopDiff = 1					

		temp1 = 0
		temp2 = 8

		for i in range(0,2):
			if game[i + temp1] != sym[k]:
				if game[4] != sym[k]:
					if game[i + temp2] != sym[k]:
						priority[i + temp1] = priority[i + temp1] + 1
						priority[4] = priority[4] + 1
						priority[i + temp2] = priority[i + temp2] + 1
						
			temp1 = 1
			temp2 = 5			 

	blanks_priority = []
	length = len(remain)
	local_remain = remain[:]

	for i in range(0,length):
		blanks_priority.append(priority[remain[i]])
			
	#sort
	for i in range(1,length+1):
		for j in range(0,length-i):
			if blanks_priority[j] < blanks_priority[j+1]:
				blanks_priority[j],blanks_priority[j+1] = blanks_priority[j+1],blanks_priority[j]
				local_remain[j],local_remain[j+1] = local_remain[j+1],local_remain[j]
				
	i = 0
	while blanks_priority[i] == blanks_priority[i+1]:
		i = i + 1
		if i == len(blanks_priority)-1:
			break

	local_remain = local_remain[:i+1]
	
	final_index = random.randint(0,i)
	return local_remain[final_index]		

def specialCase():
	''' special case for second chance of computer '''
	temp_list = []
	count = 0
	loopEnd = 7
	loopDiff = 6
	temp1 = 1
	temp2 = 2
	for j in range(0,2):
		for i in range(0,loopEnd,loopDiff):
			if game[i] == '_' and game[i+temp1] == 'X' and game[i+temp2] == '_':
				count = count + 1
		loopEnd = 3
		loopDiff = 2
		temp1 = 3
		temp2 = 6	

	if count != 0 and count != 1 and count != 2:
		return None
	
	flag = 0
	if count == 2:
		if game[1] == 'X' and game[4] == 'O' and game[7] == 'X':
			flag = flag + 1
		if game[3] == 'X' and game[4] == 'O' and game[5] == 'X':
			flag = flag + 1	
		
		if flag == 0:
			loopEnd = 7
			loopDiff = 6
			temp1 = 1
			temp2 = 2
			for j in range(0,2):
				for i in range(0,loopEnd,loopDiff):
					if game[i] == '_' and game[i+temp1] == 'X' and game[i+temp2] == '_':
						temp_list.append(i)
						temp_list.append(i+temp2)
				loopEnd = 3
				loopDiff = 2
				temp1 = 3
				temp2 = 6
		
		    
			for i in range(0,3):
				if temp_list[i] == temp_list[i+1]:
					del(temp_list[i])
					break	
				
			i = len(temp_list)-1
			final_index = random.randint(0,i)
			return 	temp_list[final_index]

	if count == 1:
		loopEnd = 7
		loopDiff = 6
		temp1 = 1
		temp2 = 2
		for j in range(0,2):
			for i in range(0,loopEnd,loopDiff):
				if game[i] == '_' and game[i+temp1] == 'X' and game[i+temp2] == '_':
					temp_list.append(i)
					temp_list.append(i+temp2)
				if game[i] == '_' and game[i+temp1] == '_' and game[i+temp2] == '_':
					temp_list.append(i+temp1)	
			loopEnd = 3
			loopDiff = 2
			temp1 = 3
			temp2 = 6
				
		i = len(temp_list)-1
		final_index = random.randint(0,i)
		return temp_list[final_index]

	if count == 0:
		flag = 0	
		if game[0] == 'X' and game[4] == 'O' and game[8] == 'X':
			flag =  1
			
		elif game[2] == 'X' and game[4] == 'O' and game[6] == 'X':
			flag = 1
		
		if flag == 1:
			temp_list = [1,3,5,7]
			i = len(temp_list)-1
			final_index = random.randint(0,i)
			return temp_list[final_index]			

def fun(text, ftext,color):
	textSurface = ftext.render(text, True, color)
	return textSurface, textSurface.get_rect()

def message(text,x,y, text_size,color):
	''' display the user text '''
	ftext = pygame.font.Font('freesansbold.ttf', text_size)
	textSur, textRect = fun(text, ftext,color)
	textRect.center = (x,y)
	window.blit(textSur,textRect)

def check(pos):
	''' decision of the user symbol '''
	global user_sym,com_sym,play
	color = [blue,blue]
	if 370 < pos[0] < 470 and 400< pos[1] < 500:
		user_sym = pygame.image.load(r'cross.png')
		com_sym = pygame.image.load(r'circle.png')
		return 1
		
	elif  500 <pos[0]< 600 and 400 < pos[1] < 500:
		user_sym = pygame.image.load(r'circle.png')
		com_sym = pygame.image.load(r'cross.png')
		return 1

	if 325 < pos[0] < 515 and 200 < pos[1] < 270:
		play = 0
		return (green,blue)

	elif 325 < pos[0] < 515 and 300 < pos[1] < 370:
		play = 1
		return (blue,green)

	return (blue,blue)	
				
def intro_screen():
	gameExit = False
	bcolor = [blue,blue]
	name = 'Created by- Gaurav Verma'
	count = 0
	while not gameExit:
			user_sym = pygame.image.load(r'cross.png')
			com_sym = pygame.image.load(r'circle.png') 

			for event in pygame.event.get(): 
				if event.type == pygame.QUIT:
					pygame.quit()
					#quit()
					sys.exit()
				
				click = pygame.mouse.get_pressed()
				if click[0] == 1:
					pos = pygame.mouse.get_pos()
					bcolor = check(pos)
					if check(pos) == 1:
						time.sleep(0.2)
						bcolor = [blue,blue]
						start()
								
			window.fill(intro)
			window.blit(logo,(40,-20))

			if count< len(name):
					p = name[:count]
					#time.sleep(0.01)
					message(p,window_width/2,580,20,black)
					count += 1
			else:
				message('Created by- Gaurav Verma',window_width/2,580,20,black)		

			pygame.draw.rect(window, bcolor[0], [325,200,190,70])
			message('1 Player',420,235,30,white)
			pygame.draw.rect(window, bcolor[1], [325,300,190,70])
			message('2 Player',420,335,30,white)

			message("Play",230,450,60,black)
			window.blit(user_sym,(370,400))
			window.blit(com_sym,(500,400))
										
			pygame.display.update()
			clock.tick(40)

def start():
	global game,remain,win,play
	# index [0,  1,  2   3   4   5   6   7   8]
	game = ['_','_','_','_','_','_','_','_','_']
	win = 0
	
	remain = [0,1,2,3,4,5,6,7,8]   # list of the blank boxes
	window.fill(background)
	
	for i in range(0,9):
		window.blit(white_img,coordinate[i])

	pygame.display.update()	
	game_loop()

def turn(pos,player):
	global remain
	if len(remain) == 0:
		return
		
	for i in range(0,9):
		cord = coordinate[i]
		if cord[0]< pos[0] < cord[0] + 100 and cord[1]< pos[1] < cord[1] + 100:
			if game[i] == '_' and player == 0:
				remain = asign(i,'X',user_sym)
				dob_check('X')
				return 1
			elif game[i] == '_' and player == 1:
				remain = asign(i,'O',com_sym)
				dob_check('O')
				return 0

def dob_check(symbol):
	global win
	
	temp1 = 1
	temp2 = 2
	loopEnd = 7
	loopDiff = 3

	for j in range(0,2):
		for i in range(0,loopEnd,loopDiff):
			if game[i] == symbol:
				if game[i + temp1] == symbol:
					if game[i + temp2] == symbol:
						if symbol == 'X':
							message('Player 1 wins!',400,80,50,black)
						else:
							message('Player 2 wins!',400,80,50,black)
						win = 1		
			
		temp1 = 3
		temp2 = 6
		loopEnd = 3
		loopDiff = 1					

	temp1 = 0
	temp2 = 8

	for i in range(0,2):
		if game[i + temp1] == symbol:
			if game[4] == symbol:
				if game[i + temp2] == symbol:
					if symbol == 'X':
							message('Player 1 wins!',400,80,50,black)
					else:
						message('Player 2 wins!',400,80,50,black)
					win = 1	
							
		temp1 = 1
		temp2 = 5

def game_loop():
	global play,win
	gameExit = False
	valid = 0

	while not gameExit: 
				
			for event in pygame.event.get(): 
				if event.type == pygame.QUIT:
					gameExit = True
				
				click = pygame.mouse.get_pressed()
				if play == 0:
					if click[0] == 1:
						if win != 1:
							pos = pygame.mouse.get_pos()
							valid = user_chance(pos)
							if valid != None:
								win = coumputer_chance()

				if play == 1:
					if click[0] == 1:
						if win != 1:
							pos = pygame.mouse.get_pos()
							if temp == 0:
								valid = turn(pos,0)
							elif temp == 1:
								valid = turn(pos,1)
																
					if len(remain) == 0 and win != 1:
						message('Match Draw',400,80,50,black)
					if valid != None:
						temp = valid

						
			pygame.display.update()
			clock.tick(30)

intro_screen()








			

           				


				 
				                                   
		                                  
		                                
        

                            	
			
					
				      
				       
				                                     
				
				

			
				
						
		
