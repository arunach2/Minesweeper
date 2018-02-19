import random
import pymysql as sql
import time



class Square:
    '''
    This is the constructor. The instance variable counter will keep track of the number of bombs adjacent to the square.
    The instance variable bomb will keep track of whether the square contains a bomb or not. The instance variable open indicates
    whether the box has been opened or not. The flag variable is a user option, so they can mark squares they believe to be bombs
    '''

    def __init__(self, counter, bomb, open, flag):
        self.counter=counter
        self.bomb = bomb
        self.open = open
        self.flag = flag








def initialize_array(num_bombs):
    '''
    This function does two things. It determines the counter values for each square. It also randomly allocates the bombs
    accross the minesweeper board
    '''

    
    # Generating an array of unique random values so that the mines can be allocated randomly to cells
    a = []
    for i in range(0, num_bombs):
        mine_location = random.randint(0, (max_rows * max_rows)-1)
        while mine_location in a:
            mine_location = random.randint(0, (max_rows * max_rows)-1)
        a.append(mine_location)

    # assigning bombs to the appropriate index within the matrix
    for i in range(0, len(a)):
        row = int(a[i] / max_rows)
        column = a[i] % max_rows
        M[row][column].bomb = "B"

    # finding the cells that do not have mines so we can update the instance counter variable for them
    for i in range(0, max_rows):
        for j in range(0, max_rows):
            if M[i][j].bomb != "B":

                # basically checking a 3x3 grid area around each of these cells
                for s in [i-1, i, i+1]:
                    for k in [j-1, j, j+1]:

                        # Conditions to make sure it does sure does not check element out of range of array
                        if ((0 <= s < max_rows) and (0 <= k < max_rows) and M[s][k].bomb == "B"):
                            M[i][j].counter = M[i][j].counter + 1
    
    # printing out a map of all the instance counter variables. This is to check if we properly updated the counter variables.
    for i in range(0, max_rows):
        for j in range(0, max_rows):
            if j == 0:
                print("\n")
            print(M[i][j].counter, end = ' ')
    print("\n")

    # prints out a map of where all the mines are located. This is to check if we properly updated the bomb variables.
    for i in range(0, max_rows):
        for j in range(0, max_rows):
            if j == 0:
                print("\n")
            print(M[i][j].bomb, end = ' ')

    print("\n")


def open_square(row,column):
    '''
    This function is enacted when the user wants to open a cell. It recursively goes through every cell from the intial
    point and stop running in one direction, once we reach a cell that holds a non-zero counter variable.
    '''

    global num_open_square
    global lost_flag

    # Checks if user put a logical numeric value and if the box is closed
    if(0 <= row < max_rows and 0 <= column < max_rows and M[row][column].open == "X"):

        # We first open up the cell the user specified, we also update the the number of opened squares by one
        M[row][column].open = "O"
        num_open_square = num_open_square + 1

        # If the user selected a bomb, the function ends and user loses
        if M[row][column].bomb == "B":
            lost_flag = 1
        # If the user selects a spaces that has a counter variable of 0, then we recursively check in all four directions
        # The recursion ends when we hit a counter variable that is a non-zero value
        elif M[row][column].counter == 0:
            open_square(row - 1, column)
            open_square(row + 1, column)
            open_square(row, column - 1)
            open_square(row, column + 1)
    
    


#Type in user information
def intro_screen():
    '''
    This function requests the user for their personal information to see if they have an account. If they have an account,
    the function will let the user know and there will be no change to PLAYER_TBL. If the name is not recognized, then function
    will request email and insert this data into PLAYER_TBL
    '''
    global name
    

    # Connect to the local database
    db = sql.connect("localhost", "root", "Hog123er", "minesweeper")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Ask user for name
    name = input("Type in your name: ")

    # Identifying if the name the user typed in is already in the database
    query = "SELECT * FROM PLAYER_TBL WHERE PLAYER_NAME LIKE ('%s')" % name
    cursor.execute(query)
    result1 = cursor.fetchall()
    # The condition checks if nothing is returned, then the user has a unique name
    # Because user is unique, we will be requesting for the email addresss

    if (len(result1) == 0):
        email = input("Type in your email: ")

        # Inserting new unique name and email to table
        query2 = "INSERT INTO PLAYER_TBL (PLAYER_NAME, PLAYER_EMAIL) VALUES ('%s', '%s')" % (name, email)
        cursor.execute(query2)
        db.commit()

    # If our initial query statement did return a record back, that means the user typed in an existing name
    else:
        print("You are in our records!")


    # query = "INSERT INTO PLAYER_TBL (PLAYER_EMAIL, PLAYER_NAME) VALUES ('Raajesh@hotmail.com', 'Raajesh Arunachalam')"
    query3 = "SELECT * FROM PLAYER_TBL"

    
    cursor.execute(query3)

    # disconnect from server
    db.close()

    # Test code below to make sure PLAYER_TBL is accurate
    result = cursor.fetchall()

    for r in result:
        print(r)

def end_game():
    '''
    Once game is complete, game statistics are written to database GAME_TBL, such as number of squares in the board, number
    of mines in the game, time taken from start to finish, and completion percentage
    '''
    global name

    # Connect to the local database
    db = sql.connect("localhost", "root", "Hog123er", "minesweeper")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Using the name provided by the user, to obtain the player_id associated with it
    # We do this so that we can use the player_id as a foreign key for the GAME_TBL table
    query = "SELECT PLAYER_ID FROM PLAYER_TBL WHERE (PLAYER_NAME = '%s')" % (name)
    cursor.execute(query)
    result = cursor.fetchall()
    player_id = result[0][0]
    

    # Populating after game statistics into GAME_TBL after the person has completed their game, whether they won or lost
    query2 = "INSERT INTO GAME_TBL (PLAYER_ID,NUM_SQUARES,NUM_MINES,TIME,COMPLETION_PERC) VALUES (%d, %d, %d, %f, %f)" \
    % (player_id, total_square, num_bombs, end_time, num_open_square / (total_square-num_bombs) * 100)
    cursor.execute(query2)
    db.commit()

    #disconnect from the server
    db.close()



# initial parameters
name = ''
num_open_square = 0
lost_flag = 0
num_bombs = 5
M = []
max_rows = 5
max_rows = 5

# To request user for personal information
intro_screen()

# Creates a max_rows X max_rows square matrix that is fully populated with Square instances
total_square = max_rows * max_rows
for i in range(0, max_rows):
    M.append([])
    for j in range(0, max_rows):
        M[i].append(Square(0, 0, "X", 0))

# Initiates where all the mines will be and adjusts the counter variables accordingly
initialize_array(num_bombs)

# Starts the timer when the user first gets to the board
start_time = time.time()

# Conditions it so that you will keep getting prompted until either you lose, or you win
while (num_open_square < (max_rows*max_rows) - num_bombs):

    # This will print out the board. It will print out all the closed boxes and the boxes that are open with thier counter value
    for i in range(0, max_rows):
        for j in range(0, max_rows):
            if j == 0:
                print("\n")
            if M[i][j].open == "X":
                print(M[i][j].open, end=' ')
            else:
                print(M[i][j].counter, end=' ')
    
        
    print("\n")
    # request row and column information from user. We subtract one to make it more intuitive, since no counts from zero
    try:
        row = (int(input("Type in row: ")) - 1)
        column = (int(input("Type in column: ")) - 1)
        if 0 <= row < 5 and 0 <= column < 5:
            open_square(row, column)
        else:
            print("Out of bounds.")
    except ValueError:
        print("Illogical value typed in. Please try again.")

    # If lost_flag is 1, then it will reveal the cell with the bomb that you opened along with all the other cells you opened
    if lost_flag == 1:
        for i in range(0, max_rows):
            for j in range(0, max_rows):
                if j == 0:
                    print("\n")
                if M[i][j].bomb == "B" and M[i][j].open == "O":
                    print(M[i][j].bomb, end = ' ')
                elif M[i][j].open == "X":
                    print(M[i][j].open, end=' ')
                else:
                    print(M[i][j].counter, end=' ')
        # total time is calculated and printed out.
        print("\n")
        print("You lost!")
        end_time = time.time() - start_time
        print("Total game time: %.2f" % end_time)
        break

# If the user opens up all the boxes, aside from the bombs, he wins
if (num_open_square == (max_rows * max_rows) - num_bombs) and lost_flag == 0:
    print("You won!")
    end_time = time.time() - start_time
    print("Total game time: %.2f" % end_time)
# Call function that writes game statistics to database
end_game()









