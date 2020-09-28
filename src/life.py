from os import system
from time import sleep
from colored import fg, bg, attr
from welcome import title_card, loading_animation
from itertools import cycle
import random
import json


#hard coded patterns and list of patterns below
blinker = [(0, 0), (1, 0), (-1, 0)]

toad = [(0, 0), (0, 1), (0, 2),
		(1, -1), (1, 0), (1, 1)]

glider = [(0, 2),
		(1, 2),
		(2, 2), (2, 1), (1, 0)]

acorn = [(1, 2),
		(2, 4),
		(3, 1), (3, 2), (3, 4), (3, 5), (3, 6)]

light_spaceship = [(0, 3), (0, 4),
				(1, 1), (1, 2), (1, 4), (1, 5),
				(2, 1), (2, 2), (2, 3), (2, 4),
				(3, 2), (3, 3)]

middle_spaceship = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
					(1, 0), (1, 5),
					(2, 0),
					(3, 1), (3, 5),
					(4, 3)]

large_spaceship = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
				(1, 0), (1, 6),
				(2, 0),
				(3, 1), (3, 6),
				(4, 3), (4, 4)]

gosper_glider_gun = [(1, 25),
					(2, 23), (2, 25),
					(3, 13), (3, 14), (3, 21), (3, 22), (3, 35), (3, 36),
					(4, 12), (4, 16), (4, 21), (4, 22), (4, 35), (4, 36),
					(5, 1), (5, 2), (5, 11), (5, 17), (5, 21), (5, 22),
					(6, 1), (6, 2), (6, 11), (6, 15), (6, 17), (6, 18), (6, 23), (6, 25),
					(7, 11), (7, 17), (7, 25),
					(8, 12), (8, 16),
					(9, 13), (9, 14)]

ptrns = [blinker, toad, glider, acorn, light_spaceship,
		middle_spaceship, large_spaceship, gosper_glider_gun]


ptrns_str = ['random mode', 'create custom pattern',
			 'delete custom pattern', 'blinker',
			 'toad', 'glider', 'acorn',
			 'light spaceship', 'middle_spaceship',
			 'large spaceship', 'gosper glider gun']


verified = ['random mode', 'create custom pattern',
			 'delete custom pattern', 'blinker',
			 'toad', 'glider', 'acorn',
			 'light spaceship', 'middle_spaceship',
			 'large spaceship', 'gosper glider gun']


#variables for color and pattern symbols.
#grid size is a default value for whatever reason.
#The colors and test_symbols use the cycle function from the itertools module.
#This is so that the user can undo a pattern from their design
#if they change their mind while setting up the board because
#each design is unique and can be undone as a certain color.
reset = attr('reset')
pattern_symbol = fg('green') + '◼' + reset
board_pattern = fg(16) + '◻' + reset
colors = cycle([i for i in range(9, 231)])
test_symbols = cycle([fg(next(colors)) + '◼' + reset for i in range(231)])
space = 10
spacing = ' ' * space
grid_size_x = 50
grid_size_y = 50

#adjacent check does what you would think it to do.
#this function checks all the adjacent cells around each cell
#and determines whether or not there are a certain amount of adjacent living cells. 
def adjacent_check(grid, gx, gy, x, y, wrap=True):
	adjacent_living = 0
	positions = [(x, y-1), (x, y+1), (x-1, y), (x+1, y), (x-1, y+1),
				(x-1, y-1), (x+1, y-1), (x+1, y+1)]
	for x, y in positions:
		if wrap:
			max_x = gx - 1
			max_y = gy - 1
			if x > max_x:
				x = 0
			elif x < 0:
				x = max_x
			if y > max_y:
				y = 0
			elif y < 0:
				y = max_y
			if grid[x][y] == pattern_symbol:
				adjacent_living += 1
		else:
			if x == -1 or y == -1:
				pass
			else:
				try:
					if grid[x][y] == pattern_symbol:
						adjacent_living += 1
				except IndexError:
					pass

	return adjacent_living

#this function creates and places the starting patterns for the game of life.
#this is the function that places down the patterns passed in and adjusts them
#based on the user's x and y coordinates.
def starting_cells(grid, cell_list, ptrn_symbol, init_x=0, init_y=0):
	for x, y in cell_list:
		adjusted_x = x + init_x
		adjusted_y = y + init_y
		if adjusted_x >= 0 and adjusted_y >= 0:
			if grid[adjusted_x][adjusted_y] == pattern_symbol:
				break
			else:
				grid[adjusted_x][adjusted_y] = ptrn_symbol
		else:
			break

#These are the rules for cell death and cell life.
#This function works with the adjacent_check function
#to determine whether or not each cell in the current generation
#should live or die. 
def life_rules(grid, gx, gy, wrap=True):
	dead_cells = []
	birthed_cells = []
	for x_pos in range(gx):
		for y_pos in range(gy):
			if grid[x_pos][y_pos] == pattern_symbol:
				if adjacent_check(grid, gx, gy, x_pos, y_pos, wrap) >= 4:
					dead_cells.append((x_pos, y_pos))
				elif adjacent_check(grid, gx, gy, x_pos, y_pos, wrap) < 2:
					dead_cells.append((x_pos, y_pos))
			elif grid[x_pos][y_pos] == board_pattern:
				if adjacent_check(grid, gx, gy, x_pos, y_pos,wrap) == 3:
					birthed_cells.append((x_pos, y_pos))

	for x, y in dead_cells:
		grid[x][y] = board_pattern
	for x, y in birthed_cells:
		grid[x][y] = pattern_symbol

#wipes a grid depending on what you pass for an argument and a certain symbol from said grid.
#the nuke option wipes the pattern_symbol from the board no matter what is passed.
def map_wipe(grid, gx, gy, symbol=pattern_symbol, nuke=False):
	for x in range(gx):
		for y in range(gy):
			if grid[x][y] == symbol:
				grid[x][y] = board_pattern
	if nuke:
		for x in range(gx):
			for y in range(gy):
				if grid[x][y] == pattern_symbol:
					grid[x][y] = board_pattern

#this function selects random positions on the board for cells.
#The amount of random cells is the gridx length (gx) times the
#gridy length (gy). 
def random_mode(grid, gx, gy):
	for _ in range(gx * gy):
		rand_x = random.randint(0, gx - 1)
		rand_y = random.randint(0, gy - 1)
		grid[rand_x][rand_y] = pattern_symbol


def rotate_ptrn(grid, pattern, quadrant):

	def x_reflect():
		return [(pair[0], pair[1] * -1) for pair in pattern]

	def y_reflect():
		return [(pair[0] * -1, pair[1]) for pair in pattern]

	if quadrant == 1:
		rotated_ptrn = x_reflect()
		return rotated_ptrn
	elif quadrant == 2:
		rotated_ptrn = y_reflect()
		return rotated_ptrn
	elif quadrant == 3:
		rotated_ptrn = x_reflect()
		return rotated_ptrn
	elif quadrant == 4:
		rotated_ptrn = y_reflect()
		return rotated_ptrn
	else:
		print('wtf, how?')


#main function that holds the main game loop.
#this is kind of rediculous and unorganized but
#I really just wanted to hack this together and make it work.
#Hopefully I don't make a habit out of this and get better at making
#readable and organized code. I guess the main issue is that this is a console app
#and it's hard to make a console app look pretty with all these strings for UI.
def life_main(managed=True):

	quadrant_tracker = 1

	if managed:
		custom_path = 'data/user-cells.json'
	else:
		custom_path = '../data/user-cells.json'

	system('clear')
	title_card('WELCOME TO THE GAME OF LIFE!', thickness=2)
	print()
	print()
	print('Enter the lengths for the x and y axis of the display grid...')
	print()
	print(fg('yellow') + 'WARNING: ' + reset + 'A size >= 38x38 is recommended for all patterns to fit' + reset)
	print()
	print()

	while True:
		try:
			grid_size_x = int(input('How large do you want the x axis to be?: '))
			print()
		except ValueError:
			loading_animation('ERROR: Please enter an integer value...', time=1)
			continue
		try:
			grid_size_y = int(input('How large do yo uwant the y axis to be?: '))
			break
		except ValueError:
			loading_animation('ERROR: Please enter an integer value...', time=1)

	gx = grid_size_x
	gy = grid_size_y

	grid = [[board_pattern for i in range(grid_size_x)]for i in range(grid_size_y)]
	custom_grid = grid.copy()

	#displays the grid with or without coordinates.
	#the coordinates are displayed during the game creation stages
	#and the coordinates are not displayed while the game runs. 
	def map_display(grid, coordinates=True):
		if coordinates:
			print('     ' + spacing + '0' + (' ' * (grid_size_x * 2 - 3)) + str(grid_size_x - 1))
			print('     ' + spacing + ''.join(['-' for i in range(grid_size_x * 2)]))
			for count, line in enumerate(grid):
				if count < 10:
					print(spacing + '{}  | {}'.format(count, ' '.join(line) + '|'))
				else:
					print(spacing + '{} | {}'.format(count, ' '.join(line) + '|'))
			print('     ' + spacing + ''.join(['-' for i in range(grid_size_x * 2)]))
		else:
			for line in grid:
				print(spacing + ' '.join(line))

	while True:
		
		stop_the_friggin_program = False
		system('clear')
		pattern_choice = None
		print()
		map_wipe(grid, gx, gy, nuke=True)
		display_grid = grid.copy()

		#function for saving custom patterns
		#you enter the name you want to save it as
		#then the function iterates trhough ever space on the board
		#and adds the spaces with a pattern to the custom_cell_coards list
		#that pattern is then dumped into the user-cells.json file
		#with the save name you chose.
		def save_pattern():
			print()
			save_name = input('What would you like to name this cell?: ')
			custom_cell_coords = []
			for x in range(gx):
				for y in range(gy):
					if custom_grid[x][y] == pattern_symbol:
						custom_cell_coords.insert(0, [x, y])

			with open(custom_path, 'r') as custom_cells:
				data = json.load(custom_cells)
			with open(custom_path, 'w') as custom_cells:
				data['custom_cells'][save_name] = custom_cell_coords
				json.dump(data, custom_cells)
			map_wipe(custom_grid, gx, gy)

		loading_animation(time=1)
		while pattern_choice != 'f':

			#this part of the code loads in all of the custom patterns
			#from user-cells.json. 
			with open(custom_path, 'r') as custom:
				custom_data = json.load(custom)
				custom_patterns = {cell_name:pattern for cell_name, pattern in custom_data['custom_cells'].items()}
			
			for ptrn_name in custom_patterns:
				if ptrn_name not in ptrns_str:
					ptrns.append(custom_patterns[ptrn_name])
					ptrns_str.append(ptrn_name)

			#creating a list of patterns with a str(value) pair for the user to select
			#the message is for the title_card function which is from the welcome.py file. 
			patterns = {str(count):ptrn for count, ptrn in enumerate(ptrns, 1)}
			message = 'ol,{}'.format(','.join(ptrns_str))
			title_card(message)
			pattern_choice = input('Which pattern would you like to add to the grid?: ')
			print()
			#'2' is the key for the create custom cell choice
			#a user can create their own design once cell at a time
			#inside of a seperate display grid
			if pattern_choice == '2':
				while True:
					system('clear')
					map_display(custom_grid)
					print()
					print('Type "clear" to reset the grid, "exit" to exit, or "save" to save your cell design.')
					print()
					cx = input('Enter x coordinate: ')
					if cx == 'clear':
						map_wipe(custom_grid, gx, gy)
						continue
					elif cx == 'exit':
						system('clear')
						break
					elif cx == 'save':
						save_pattern()
						print()
						another_custom = input('Would you like to create another custom cell? [y/n]: ')
						if another_custom == 'n':
							system('clear')
							break
						else:
							system('clear')
							continue
					else:
						try:
							cx = int(cx)
						except ValueError:
							loading_animation('make sure to enter an integer value for coordinates...', time=1)
							continue
					try:
						cy = int(input('Enter y coordinate: '))
					except ValueError:
						loading_animation('make sure to enter an integer value for coordinates...', time=1)
						continue
					custom_grid[cx][cy] = pattern_symbol
			#'3' is the delete custom pattern choice
			#The user will enter the name of said pattern
			#and the following code overwrites that pattern in the json file
			#as well as the pattern string list. 
			elif pattern_choice == '3':
				while True:
					print()
					cell_name = input('Enter the name of the pattern you are deleting or type "exit" to exit: ')
					if cell_name in ptrns_str and cell_name not in verified:
						with open(custom_path, 'r') as custom:
							data = json.load(custom)
						with open(custom_path, 'w') as custom:
							del data['custom_cells'][cell_name]
							json.dump(data, custom)
						index = ptrns_str.index(cell_name)
						ptrns.pop(index - 3)
						ptrns_str.remove(cell_name)
						system('clear')
						break
					elif cell_name == 'exit':
						system('clear')
						break
					else:
						print()
						print('That cell/pattern name is either non-custom or doesn\'t exist')

			#clearly uses the random_mode function
			#which places random cells on the grid
			elif pattern_choice == '1':
				random_mode(grid, gx, gy)
				break
			
			#stops the current loop and sets
			#stop_the_friggin_program to True
			#this was a stupid work around/solution
			#but I really just wanted to make this work.
			elif pattern_choice == 'exit':
				pattern_choice = 'f'
				stop_the_friggin_program = True
				break
			
			#if you choose one of the hard coded patterns
			#or one of the patterns you already created
			#you will be brought to a grid where you will decide
			#the general location you want it to exist based on
			#the first position in the pattern.
			elif str(int(pattern_choice) - 3) in patterns:
				while True:
					try:
						symbol = next(test_symbols)
						system('clear')
						map_display(grid)
						print()
						print(spacing + 'Enter starting position for pattern')
						print()
						try:
							init_x = int(input(spacing + 'Enter x coordinate: '))
						except ValueError:
							loading_animation('ERROR: make sure to enter integer value', time=1)
							continue
						print()
						try:
							init_y = int(input(spacing + 'Enter y coordinate: '))
						except ValueError:
							loading_animation('ERROR: make sure to enter integer value', time=1)
							continue
						pattern = patterns[str(int(pattern_choice) - 3)]
						starting_cells(display_grid, pattern, symbol, init_x, init_y)
						system('clear')
						map_display(display_grid)
						print()
						rotate = input(spacing + 'Reflect your cells? [y/n]: ')
						if rotate == 'y':
							system('clear')
							while True:
								pattern = rotate_ptrn(display_grid, pattern, quadrant_tracker)
								map_wipe(display_grid, gx, gy, symbol)
								starting_cells(display_grid, pattern, symbol, init_x, init_y)
								quadrant_tracker += 1
								if quadrant_tracker == 5:
									quadrant_tracker = 1
								map_display(display_grid)
								print()
								more_rotation = input(spacing + 'Reflect again? [y/n]: ')
								if more_rotation == 'n':
									print()
									break
								else:
									system('clear')

						confirmation = input(spacing + 'Are you sure about this placement? [y/n]: ')
						if confirmation == 'y':
							starting_cells(grid, pattern, pattern_symbol, init_x, init_y)
							print()
							another = input(spacing + f'would you like to add another pattern {pattern_choice}? (y/n): ')
							print()
							if another == 'y':
								pass
							else:
								print(spacing + ' - Type "f" to see your masterpiece')
								print(spacing + ' - Type "w" to wipe the entire grid')
								print(spacing + ' - Or hit enter to enter another pattern')
								print()
								pattern_choice = input(spacing + 'enter response: ')
								if pattern_choice == 'w':
									map_wipe(display_grid, gx, gy, symbol, nuke=True)
									loading_animation('wiping entire board', time=1)
								system('clear')
								break
						else:
							map_wipe(display_grid, gx, gy, symbol)

					except IndexError:
						loading_animation('** ERROR: Those coordinates either don\'t exist or do not fit the selected patern **', time=3)
						map_wipe(display_grid, gx, gy, symbol)
			else:
				loading_animation('Sorry that pattern is not in the patterns list. Try again.', time=2)

		#loop to decide how long you want the life game to run
		#it also asks if you want the cells to be able to wrap
		#around the edges of the grid. 
		while True:
			if stop_the_friggin_program:
				break
			try:
				loading_animation(time=1)
				print()
				print()
				length = int(input(spacing + 'How long do you want the simulation to run? (seconds): '))
				print()
				wrap_choice = input(spacing + 'Do you want the cells to wrap past the borders? (y/n): ')
				if wrap_choice == 'y':
					wrap = True
				else:
					wrap = False
				break
			except ValueError:
				print('Please only enter integer values...')
		
		if not stop_the_friggin_program:
			system('clear')
			for i in range(length * 20):
				map_display(grid, coordinates=False)
				life_rules(grid, gx, gy, wrap=wrap)
				sleep(.05)
				system('clear')

			loading_animation(spacing + 'ending simulation...', time=1)
			print()
			print()
			repeat = input(spacing + 'Would you like to create another game of life? (y/n): ')
			if repeat == 'y':
				pattern_choice = 'again!'
				continue
			else:
				break
		
		break

	system('clear')
	title_card('THANKS FOR TRYING THE GAME OF LIFE!')
	sleep(1)
	loading_animation('Now back to the real thing!', time=1)

def pattern_test():
	pattern_choice = '7'
	pattern = patterns[pattern_choice]
	starting_cells(grid, pattern)
	map_display(grid)

if __name__ == '__main__':
	system('clear')
	mode = 'main'
	if mode == 'main':
		life_main(managed=False)
	else:
		pattern_test()
