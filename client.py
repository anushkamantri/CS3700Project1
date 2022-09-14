#!/usr/bin/env python3

import socket
import json
import sys
import argparse
import ssl


# if the letter is present in the secret word and is in the correct position, 
# remove all words in the word_list with the letter not in that position (mark = 2)
def remove_words_with_letter_not_in_position(word_list, letter, position):
	for word in word_list:
		if (word[position] != letter):
			word_list.remove(word)

	return word_list

# if the letter is present in the secret word but is not in the correct position, 
# remove all words in the word_list with the letter in that position (mark = 1)
def remove_words_with_letter_in_position(word_list, letter, position):
	for word in word_list:
		if (word[position] == letter):
			word_list.remove(word)

	return word_list


# filters out words based on the marks of the most recent guess
def filter_word_list(word_list, last_guess):
	guess_word = last_guess.get("word")
	marks_array = last_guess.get("marks")

	word_list.remove(guess_word)

	for i in range(len(marks_array)):
		if (marks_array[i] == 1):
			word_list = remove_words_with_letter_in_position(word_list, guess_word[i], i)

		elif (marks_array[i] == 2):
			word_list = remove_words_with_letter_not_in_position(word_list, guess_word[i], i)

	return word_list


# creates a guess for the server
def create_guess(word_list, game_id):
	guess_dict = { 
		"type": "guess", 
		"id": game_id, 
		"word": word_list[0]
		} 	

	guess = (json.dumps(guess_dict)) + "\n"
	return guess


# receives messages from the server and determines the course of action 
# depending on the type of the message
def server_receiver(s, word_list):
	while True:
		received_data = s.recv(1024).decode()
		while not received_data.endswith('\n'):
			received_data += s.recv(1024).decode()

		message_dict = json.loads(received_data)
		message_type = message_dict.get("type")
		game_id = message_dict.get("id")

		if (message_type == "bye"):
			secret_flag = message_dict.get("flag")
			print(secret_flag)
			s.close()
			break

		elif (message_type == "error"):
			print(message_dict.get("message"))
			s.close()
			sys.exit(1) 
			break

		elif (message_type == "start"):
			guess = create_guess(word_list, game_id)
			s.sendall(guess.encode())

		else:
			word_list = filter_word_list(word_list, (message_dict.get("guesses"))[-1]) # filters out words and reassigns word_list to the filtered list
			guess = create_guess(word_list, game_id)

			s.sendall(guess.encode())


# main function
def main():
	# parsing the command line
	argument_parser = argparse.ArgumentParser(usage = './client <-p port> <-s> [hostname] [Northeastern-username]')
	argument_parser.add_argument('-p', type = int, required = False, help = 'The TCP port that the server is listening on', dest = 'port')
	argument_parser.add_argument('-s', action = 'store_true', required = False,
		help = 'TLS encrypted socket connection', dest = 'tls')
	argument_parser.add_argument('hostname', type = str,
		help = 'The name of the server (either a DNS name or an IP address in dotted notation)')
	argument_parser.add_argument('northeastern_username', type = str, metavar='Northeastern-username', help = 'Your Northeastern username')
	arguments = argument_parser.parse_args()


# if a port is not provided, choose one based on whether the socket is tls encrypted
	if (arguments.port is None):
		if (arguments.tls):
			port = 27994
		else:
			port = 27993

	else:
		port = arguments.port


	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		if arguments.tls:
			context = ssl.create_default_context()
			s = context.wrap_socket(s, server_hostname=arguments.hostname)

		s.connect((arguments.hostname, port))

		hello_message_dict = { 
			"type": "hello", 
			"northeastern_username": arguments.northeastern_username
		} 	


		# the list of words to guess from
		with open('project1-words.txt') as file:
			word_list = file.read().split('\n')


		# initial message to the server 
		hello_message = (json.dumps(hello_message_dict)) + "\n"
		s.sendall(hello_message.encode())
		server_receiver(s, word_list)


if __name__ == '__main__':
  main()