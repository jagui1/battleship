## HEADER ################################################
## Author: Jeremy Aguillon                              ##
## Title: Battleship                                    ##
## Created: June 2015                                   ##
## Description: Battleship game that is user vs no one. ##
##########################################################

## IMPORTS #############################################
# Imports randint to generate random locations for ships
from random import randint

## CONSTANTS ##############################################################
# Max rows and columns
ROWS = 6
COLS = 10
# Number of hidden ships
NUM_SHIPS = 6
# Max guesses is half the playable board, removes a row and col for indexes
MAX_GUESSES = (ROWS-1)*(COLS-1) // 2

###########################################################################
# get_playing() asks the user if they want to play and validates the input
#
# Input: times_played - number of times played to adjust the message
# Output: Boolean True if user wants to play False otherwise
def get_playing(times_played):
    messages = ["Do you want to play Battleship? (y/n) ", "Would you like to play again? (y/n) "]
    valid = False

    while (valid == False): 
         playing = raw_input(messages[times_played]).lower()

         if playing not in ['y', 'n']:
             print "Oops that's not a valid option, please use y or n."
         elif playing == 'y':
             return True
         else:
	     print "Goodbye, have a nice day!"
             return False


##########################################################################
# random_row() takes in the board and chooses a random integer 
#              within the size of a row in the board
# Input: board - a 2D array that represents the game board of a battleship
# Output: an integer between 1 and the length of 1 row in the board
def random_row(board):
    return randint(1, len(board) - 1)


##########################################################################
# random_col() takes in the board and chooses a random integer 
#              within the size of a column in the board
# Input: board - a 2D array that represents the game board of a battleship
# Output: an integer between 1 and the length of 1 column in the board
def random_col(board):
    return randint(1, len(board[0]) - 1)


###########################################################################
# get_ships takes in the number of ships and the game board and
#           generates random positions on the board for the ships
#           that do not overlap and returns the positions
# Input: numShips - integer of ship positions to be generated
#        board - a 2D array that represents the game board of a battleship
# Output: shipPos - an array of tuples of the ship positions
def get_ships(numShips, board):
    # Array to store the tuples of locations
    shipPos = []
    
    shipRow = random_row(board)
    shipCol = random_col(board)
    
    # Adds the original tuple to the array
    shipPos.append( (shipRow, shipCol) )

    # Loops through the amount of the remaining ships
    for i in range(numShips - 1):
        # Generates random row/column pairs until there is a non used space
        while (shipRow, shipCol) in shipPos:
            shipRow = random_row(board)
            shipCol = random_col(board)
        #End while loop
        
        # Adds the new ship position
        shipPos.append( (shipRow, shipCol) )
    #End for loop

    return shipPos
    

###############################################################################
# setup() creates the board and generates ship positions
# Input: None
# Output: board - a 2D array that represents the game board of a battleship
#         shipPos - an array of tuples of the ship positions
def setup():
    board = []
    
    # Adds the first row which will create a grid so the user can see
    #    what row and column they are picking
    board.append(["0"])
    
    # Loops through the number of columns to add labels to the first row
    for col in range(COLS):
        # Appends string because the .join function expects string values
        board[0].append(str(col+1))
    #End for loop    
    
    # Adds the remaining rows in the ocean 
    for row in range(ROWS):
        # Prepends a number to signify the row that is being added for the user
        board.append([str(row+1)]+["O"] * COLS)
    #End for loop
    
    # Generates positions for the ship based on the board
    shipPos = get_ships(NUM_SHIPS, board)

    # Greeting    
    print "Let's play Battleship!"
    # Debug statement that shows the locations of ships
    #print shipPos
    
    return board, shipPos
    

###############################################################################   
# print_board() prints the game board in a way that is more presentable to the
#               viewer by removing ',' and '[' and ']' characters fromt the 2D 
#               array
# Input: board - a 2D array that represents the game board of a battleship
# Output: None
def print_board(board):
    # Cycles through each subArray in the 2D array
    for row in board:
        # Prints all values in each subArray with " " between each value
        print "  ".join(row)
    #End for loop


###############################################################################
# get_user_int() takes in a prompt to the user and keeps getting input from the
#                user until a valid integer is given
# Input: prompt - a string that will be displayed to the user before input
def get_user_int(prompt):
    # Flag for debugging input
    invalid = True
    
    # Loops to get input from the user until a valid integer is given
    while invalid:
        try:
            # Attempts to get value from user
            userInt = int(raw_input(prompt))
            # Does not end loop until successfully converts integer
            invalid = False
            
        except:
            # If there is an error, reprompts user with new message
            prompt = "Invalid input! Enter an integer: "
        #End try/except
    #End while loop
            
    return userInt
    

##############################################################################
# game_over() takes in the final information from the game and prints out
#             an ending screen for the user that shows all locations of the 
#             ships and their guesses.
# Input: shipsLeft - integer representing how many ships the user has not sunk
#        board - a 2D array that represents the game board of a battleship
#        shipPos - an array of tuples of the ship positions 
# Output: None
def game_over(shipsLeft, board, shipPos):
    # Losing message
    print "You have run out of guesses"
    print "You sank" ,NUM_SHIPS - shipsLeft, "of" ,NUM_SHIPS

    # Loops through each tuple in the ship locations
    for position in shipPos:
        # Stores values - The tuple is structured as a row and a column
        shipRow = position[0]
        shipCol = position[1]
        
        # Checks if the tuple has not been sunk
        if board[shipRow][shipCol] != '*':
            # Changes the signal to signify that it has not been guessed
            board[shipRow][shipCol] = '!'
    #End for loop

    # Prints key of the symbols, the updated board and a game over message
    print "X = missed, * = sunk, ! = not guessed"
    print_board(board)
    print "Game Over"


###############################################################################
# play_game() takes in the board and positions of the ships and plays the game 
#             by getting input from the user, checking their guess and marking
#             it on the board. The game is over when the user runs out of 
#             guesses or if they sink all of the ships.
# Input: board - a 2D array that represents the game board of a battleship
#        shipPos - an array of tuples of the ship positions  
# Output: None 
def play_game(board, shipPos):
    playing = True
    # Counter for the turn of the user
    turn = 1
    # Number of ships the user has not sunk starting at the amount of ships
    shipsLeft = NUM_SHIPS
    
    while playing:
        print "Turn:",(turn), "of", MAX_GUESSES
        turn += 1
        print_board(board)
        
        guessRow = get_user_int("Guess Row: ")
        guessCol = get_user_int("Guess Col: ")
        
        # Debugging input to end program so I don't have to go through whole game
        #if guessRow == -1:
            #break
        
        # Checks if the user entered a row or column outside of the game board
        invalidRow = guessRow <= 0 or guessRow > ROWS
        invalidCol = guessCol <= 0 or guessCol > COLS
        
        if invalidRow or invalidCol:
            # Prints message that the user guessed outside of the board
            print "Oops, that's not even in the ocean.\n"

        else:
            # Checks if the current is a ship location that has not been guessed
            if (guessRow, guessCol) in shipPos and board[guessRow][guessCol] == "O":
                # Prints message that the user sunk a ship
                print "Congratulations! You sunk one of my battleships!"
                # Decrements amount of ships left
                shipsLeft -= 1
                # Displays how many ships are unguessed
                print "Remaining ship(s): " + str(shipsLeft) + "\n"
                # Updates board to signify sunk ship
                board[guessRow][guessCol] = "*"
    
                # Checks if the user has sunk all ships
                if shipsLeft == 0:
                    # Displays game winning message with updated board
                    print "You sank" ,NUM_SHIPS - shipsLeft, "of" ,NUM_SHIPS
                    print_board(board)
                    print "You win!"
                    # Sets flag to false to end the game loop
                    playing = False

            # If the guess is not a ship location
            else:
                # Checks if the space has been guessed already
                if(board[guessRow][guessCol] != "O"):
                    print "You guessed that one already.\n"
                    
                # If the guess has not been guessed and is not a ship
                else:
                    print "You missed my battleship!\n"
                    # Updates board to show miss
                    board[guessRow][guessCol] = "X"
        # Checks if the user has used all of their turns
        if turn > MAX_GUESSES:
            # Calls game over function to display losing message
            game_over(shipsLeft, board, shipPos)
            # Sets flag to false to end the game loop
            playing = False
    #End while loop
    
###############################################
# Main function
def main():
  playing = get_playing(0)

  while playing:
    # Sets up the board and ship positions
    board, positions = setup()
    # Executes game loop until the game is over
    play_game(board, positions)

    playing = get_playing(1)

# Call to main
main()
