**Project 1: Socket Basics**
=========================== 

## **Approach**

To make the process of writing the client simpler, I broke down the assignment into smaller chunks. The first task was to establish a connection between the client and the server using the socket. After a connection had been successfully established, the first "hello" message was sent to ensure that the socket was working as expected.

Then, I approached the main loop of the game, where the client interacts with the server until the secret word is guessed correctly. To make the guessing process more efficient, the list of words was pared down as much as possible after each guess. This was done in three ways:

- The current guess word itself was removed from the list of words
- If a letter in the current guess was present in the secret word but was in an incorrect position (i.e. mark = 1), all words with the same letter in the same position are removed from the word list
- If a letter in the current guess was present in the secret word and was in the correct position (i.e. mark = 2), all words that did not have the same letter in the same position are removed from the word list

After running this program a few times to ensure that the algorithm worked as expected, I proceeded to creating a command line argument parser for the program and added support for TLS-encrypted sockets and ensured that both types of sockets produced different secret flags.


## **Challenges**
There was a learning curve involved with getting hands-on Python experience for the first time as well as learning how to program with sockets and command line prompts. 

At first, the Wordle algorithm also dealt with letters with mark=0, removing all words that contained that letter in the word list. However, this brought about the challenge of words with a repeated letter. For example, if the word 'hooly' had marks [0, 0, 2, 0, 0], the algorithm would reach the first 'o' and decide to remove all words with the letter o in them, which would create a problem since the secret word does have an 'o', just not in that position. 

To combat this challenge, I decided to take the simpler approach and only reduce the list based on the when the marks were either 1 or 2.

## **Testing**
Since this was a relatively small and primarily simple project, testing was done solely with the help of print statements and reruns of specific components of the program. For instance, the format of the JSON messages and dictionary conversions were first checked with print statements before moving on to the algorithm, and the algorithm was checked with print statements to see which words were being removed from the word list, and each guess and message received from the server was also printed. After a few reruns of getting the non-encrypted socket's secret flag, I moved onto implementing the handling of the encrypted version and command line, and ensured that the new secret flag was also printed on multiple reruns.

However, I do believe that proper testing would be vital for the current and future projects and would reduce the amount of guess-work while writing the program.