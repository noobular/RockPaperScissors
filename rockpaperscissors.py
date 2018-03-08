############################
#  Author: James Byrnes    #
#  Last Update: 3/8/18     #
############################

#  CHANGELOG ####
# 3/8/18 : Added Button Support
# 



#Imports
#==============================
import random,time,csv,os,operator
from gpiozero import Button

#Variables
#==============================
global again,userwins,pcwins,successfulBool,legalAnswer,useranswer,winCount,fieldnames,scorefile,plyname,plylname,getInput
again = True
userwins = 0
pcwins = 0
successfulBool = False
legalAnswer = False
useranswer = None
winCount = 1

fieldnames = ['score','fn','ln']
scorefile = "scores"

#Buttons
#==============
R = Button(12)
P = Button(17)
S = Button(26)

#Functions
#==============================

#File Checking/Reading/Writing

def createcsv():
    # Creates file then closes it, so it exists in the program for later use.
    
    if not os.path.exists("scorefiles"):
        os.makedirs("scorefiles")

    with open("scorefiles/"+scorefile+".csv", 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames)  # Create a writer for the file
        writer.writeheader()

def userExists():
    count = 0
    global fieldnames,plyname,plylname,scorefile
    fieldnames = ['score','fn','ln']
    theWholeFile = []    # this will hold the entire csv file with changes
    if os.path.isfile("scorefiles/"+scorefile+".csv") == True:
        with open("scorefiles/"+scorefile+'.csv', 'r') as csv_file:   #File being opened
            csv_reader = csv.DictReader(csv_file)                     #File being read as csv_reader(where the contents are)

            for line in csv_reader:                                   # Loop through the lines
                #print(line['fn'],line['ln'],line['score'])
                if line['fn'] == plyname.lower() and line['ln'] == plylname.lower():                          # Does CSV First Name == Player's First name?
                    line['score'] = int(line['score']) + 1 #PROBLEM PORTION
                    count = count + 1
                theWholeFile.append(line)   # add every line to theWholeFile
            csv_file.close()     # done reading the csv file, so close it

            if count == 0:                                            # if the count == 0 (player doesn't exist), add the player to the csv.
                with open("scorefiles/" + scorefile + '.csv', 'a') as newFile:  # Open CSV
                    newFileWriter = csv.writer(newFile)  # Create a writer for the file
                    newFileWriter.writerow([1, plyname.lower(), plylname.lower()])  # Write to the csv
                    #print("Wrote player name to save data.")
                    newFile.close()
            else:  # re-write the entire file (with changes)
                with open("scorefiles/" + scorefile + '.csv', 'w') as newFile:  # Open CSV
                    newFileWriter = csv.DictWriter(newFile, fieldnames)  # Create a writer for the file
                    newFileWriter.writeheader()
                    for line in theWholeFile:
                        newFileWriter.writerow(line)
                    newFile.close()
    else:
        #File path doesn't exist so it creates the new file
        createcsv()


def printScores():
    scorelist = []
    if os.path.isfile("scorefiles/"+scorefile+".csv") == True:
        with open("scorefiles/"+scorefile+'.csv', 'r') as csv_file:   #File being opened
            csv_reader = csv.DictReader(csv_file)
            scorelist = sorted(csv_reader, key=lambda row: int(row['score']), reverse=True)
            #scorelist = sorted(csv_reader, key=operator.itemgetter('score'), reverse=True) #reverse to show them from highest to lowest (verse the reverse low>high)
            del scorelist[10:]
            
            print("|==========================|")
            print("|       LEADERBOARD        |")
            print("|==========================|")
            print("| SCORE |       NAME       |")
            for line in scorelist:
                #print("| ",line['score'],"|",line['fn'],line['ln'])
                print('|   {:4}| '.format(line['score']) + '{:17}|'.format(line['fn'].title()+" "+line['ln'].title()))
            print("|==========================|")
    else:
        createcsv()

                
# Timing to act as if you're palming your hands together
def HandTime():
    print("Rock...")
    time.sleep(1)
    print("Paper...")
    time.sleep(1)
    print("Scissors...")
    time.sleep(1)
    print("Hammer!!")
    time.sleep(1.5)

#Do you want to play again function
def playAgain():
    global userwins
    global pcwins
    global plyname
    if pcwins > winCount-1 or userwins > winCount-1:
        if pcwins > winCount-1: ##PC Wins
            print("The computer has beaten you in the game of Rock Paper Scissors.(and hammers)")
            print("Computer Wins:",pcwins)
            print(plyname.title(), "Wins:",userwins)
            userwins = 0
            pcwins = 0
            printScores()
            
        else: ##User wins
            userExists()
            print("You've beaten the computer in game of Rock Paper Scissors.(and hammers)")
            print(plyname.title(), "Wins:",userwins)
            print("Computer Wins:",pcwins)
            print("   ")
            userwins = 0
            pcwins = 0
            printScores()
            
        while True:
            answer = input("Do you want to play again " + plyname.title() + "? Y/N").lower().replace(" ", "")
            print("   ")
            if answer == "y":
                Play()
            else:
                if answer == "n":
                    print("Thanks for playing!")
                    print("   ")
                    time.sleep(3)
                    exit()
                    again = False
                    break
                if answer != "n":
                    print("Please type your answer again...")
                    print("   ")
#Play function/loop
def Play() :
    global again,userwins,pcwins,successfulBool,legalAnswer,useranswer,winCount,getInput

    while True :
        pcinput = random.randint(1,4)
        if again == True:
            print(plyname.title(),'Please choose "Rock", "Paper", "Scissors", (or "Hammer" If there was a fourth button...)')
            print("   ")
           # useranswer = str(input()).lower()   ### ORIGINAL Method of getting rock paper or scissors
           
            getInput = False
            while getInput == False:
                if R.is_pressed:
                    useranswer = "rock"
                    getInput = True
                elif P.is_pressed:
                    useranswer = "paper"
                    getInput = True
                elif S.is_pressed:
                    useranswer = "scissors"
                    getInput = True
                else:
                   time.sleep(.025)

            if useranswer == "rock" or useranswer == "paper" or useranswer == "scissors" or useranswer=="hammer":
                if useranswer == "rock" or useranswer=="paper" or useranswer=="scissors" or useranswer=="hammer":
                    successfulBool = True
                    
                    if useranswer == "hammer":
                        HandTime()
                        print("You've chosen",useranswer)
                        print("   ")
                        useranswer = 4
                        if pcinput == 1:
                            print("you win, the computer has also chosen rock")
                            userwins += 1
                        if pcinput == 2:
                            print("You lose, the computer has chosen paper")
                            pcwins += 1
                        if pcinput == 3:
                            print("You win, the computer has chosen scissors")
                            userwins += 1
                        if pcinput == 4:
                            print("You draw, the computer has chosen hammer")
                            
                    if useranswer == "rock":
                        HandTime()
                        print("You've chosen",useranswer)
                        print("   ")
                        useranswer = 1
                        if pcinput == 1:
                            print("You Draw, the computer has also chosen rock")
                        if pcinput == 2:
                            print("You lose, the computer has chosen paper")
                            pcwins += 1
                        if pcinput == 3:
                            print("You win, the computer has chosen scissors")
                            userwins += 1
                        if pcinput == 4:
                            print("You lose, the computer has chosen hammer")
                            pcwins += 1
                            
                    if useranswer == "paper":
                        HandTime()
                        print("You've chosen",useranswer)
                        print("   ")
                        useranswer = 2
                        if pcinput == 1:
                            print("You win, the computer has chosen rock")
                            userwins += 1
                        if pcinput == 2:
                            print("You Draw, the computer has also chosen paper")
                        if pcinput == 3:
                            print("You lose, the computer has chosen scissors")
                            pcwins += 1
                        if pcinput == 4:
                            print("You win, the computer has chosen hammer")
                            userwins += 1
                            
                    if useranswer == "scissors":
                        HandTime()
                        print("You've chosen",useranswer)
                        print("   ")
                        useranswer = 3
                        if pcinput == 1:
                            print("You lose, the computer has chosen rock")
                            pcwins += 1
                        if pcinput == 2:
                            print("You win, the computer has chosen paper")
                            userwins += 1
                        if pcinput == 3:
                            print("You Draw, the computer has also chosen scissors")
                        if pcinput == 4:
                            print("You lose, the computer has chosen hammer")
                            pcwins += 1
                            
                print(plyname.title(),":",userwins)
                print("Computer:",pcwins)
                print("   ")
                pcinput = random.randint(1,3)
                playAgain()
        else :
            print('Try Again',plyname.title())               

print("Welcome to the game, The game of Rocks, papers.. and cyanide... Wait wrong game, I meant scissors. (and hammers..)")
time.sleep(1)
print("The rules are as follows, rock beats scissors, scissors beats paper, paper beats rock, Hammer beats rock and scissors.. loses against paper, and draws against itself.")
time.sleep(1)
print("What is your name stranger?")

inputname = input("Enter your first and last name: ").title().split()
canescape = False
while canescape == False:
    if len(inputname) == 2:
        global plyname,plylname
        plyname = inputname[0].lower()
        plylname = inputname[1].lower()
        canescape = True
    else:
        inputname = input("Enter your first and last name: ").title().split()
        
topfile = input("Please enter a file name for a top 10 file, (Don't add an extension)")
if topfile == "":
    scorefile = "scores"
else:
    scorefile = topfile.split(".", 1)[0]

#Start of program
printScores()   
Play()


