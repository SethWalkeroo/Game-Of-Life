from itertools import cycle
from time import sleep
from colored import fg, bg, attr
from os import system


message = 'WELCOME TO THE GAME!'
msg_color = 'white'
msg_bg_color = 16
ptrn_color = 'white'
ptrn = ['\\', '|', '/', '-']
speed = .1
thickness = 3


def title_card(message=message, msg_color=msg_color, msg_bg_color=msg_bg_color, ptrn_color=ptrn_color, ptrn=ptrn, speed=speed, thickness=thickness):

	# reset variable for the reset attribute in the colored module
	reset = attr('reset')
	# function that defines the details of how the pattern is printed to the screen for the title_card function

	def pattern(total_frames, width, ptrn, speed):
		frames = cycle(ptrn)
		for _ in range(total_frames):
			sleep(speed)
			print('|' + next(frames) * width + '|')

	try:
		message_color = fg(msg_color)
	except KeyError:
		print()
		print(fg('magenta') + f'ERROR: Your message color "{msg_color}" is not available. Try another.' + reset)
		print()
		message_color = fg('white')
	try:
		pattern_color = fg(ptrn_color)
	except KeyError:
		print()
		print(fg('magenta') + f'ERROR: Your pattern color "{ptrn_color}" is not available. Try another.' + reset)
		print()
		pattern_color = fg('white')
	try:
		background_color = bg(msg_bg_color)
	except KeyError:
		print()
		print(fg('magenta') + f'ERROR: Your message background color "{msg_bg_color}" is not available. Try another.' + reset)
		print()
		background_color = bg('black')

	# variables for colored
	colored_message = message_color + message + reset

	# color and length stuff
	ptrn_width = len(message)

	# booleans that contain the value for if there are multiple messages and if the user wants them ordered.
	multiple_messages = False
	ordered = False

	# Checking the first two characters of the message to see if the user wants the message ordered.
	if message[:2] == 'ol':
		ordered = True

	if ',' in message:
		multiple_messages = True

	if multiple_messages:
		msg_lst = message.split(',')
		if msg_lst[0] == 'ol':
			msg_lst.pop(0)
		ptrn_width = len(sorted(msg_lst, key=len)[-1]) + 5

	# code that generates the message. Enter at your own risk.
	print(pattern_color + ' ' + '-' * ptrn_width)
	pattern(thickness, ptrn_width, ptrn, speed)
	print('|' + '-' * ptrn_width + '|')
	if multiple_messages:
		for count, msg in enumerate(msg_lst, 1):
			if count < 10:
				spacing_ordered = ptrn_width - len(msg) - 3
			else:
				spacing_ordered = ptrn_width - len(msg) - 4
			spacing_unordered = ptrn_width - len(msg)
			if ordered:
				# This is the worst thing I have ever made. God have mercy on my soul...
				print('|' + message_color + '{}: {}'.format(background_color + str(count),
					background_color + msg + ' ' * spacing_ordered + reset + pattern_color + '|'))
			else:
				print('|' + message_color + '{}'.format(background_color + msg + ' ' * spacing_unordered + reset + pattern_color + '|'))
		print(reset, end='')
	else:
		print('|' + background_color + colored_message + pattern_color + '|')
	print(pattern_color + '|' + '-' * ptrn_width + '|')
	pattern(thickness, ptrn_width, ptrn, speed)
	print(' ' + '-' * ptrn_width)
	print(reset)


def loading_animation(message='', time=3, width=1):
    frames = cycle(['|', '/', '-', '\\'])
    if time == 'infinite':
        while True:
            print(message, next(frames))
            sleep(.1)
            system('clear')
    else:
        for _ in range(time * 10):
            print(message, next(frames) * width)
            sleep(.1)
            system('clear')


# def animate_text(txt, rate, tts=False):
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     rate = engine.getProperty('rate')
#     engine.setProperty('rate', rate)
#     engine.setProperty('voice', voices[14].id)
#     text = txt.split()
#     for word in text:
#         print(word, end=' ')
#         sleep(rate)


# run tests to make sure welcome.py actually works
if __name__ == '__main__':
	title_card('joe,mama,k,om,archepelago,t')
	title_card()
	#loading_animation("searching for love...", time=10)
