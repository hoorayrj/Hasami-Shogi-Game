# HASAMI SHOGI GAME
#### Video Demo:  https://youtu.be/d7dlSJmcP5w
#### Description:

##### Introduction
This is a Hasami Shogi Game also known as Intercepting Chess. There are many variants of game, but follows variant 1 from
https://en.wikipedia.org/wiki/Hasami_shogi. The game was coded in python and runs as a script in the terminal. I hope to get this game into a web app, so can be played more visually. The game is played by 2 players, one person can be Black pieces (represented by the B) and the other player can be Red pieces (represented by the R). The purpose of the game is to capture as many of the opponents pieces. When a player only has one piece remaining, that player is the loser and the opponent is the winner. 

The starting Board will look like this:

![Starting Board](https://user-images.githubusercontent.com/46697316/145130874-585838e2-6966-4c6a-a80c-499fe2d5048b.png)

R represents the R pieces and B represents the Black Pieces. Columns are numbered 1 to 9 and rows are lettered ‘a’ to ‘I’.

##### Rules of the Game
###### Moving Pieces
Pieces can only be moved horizontally or vertically. Diagonal moves are not allowed. Pieces can be moved as many places (as a rook in chess) but is limited if there is a piece in the way. Jumping is not allowed. To make a move follow the prompts on the screen. The prompts specify who’s turn it is.

![Prompts](https://user-images.githubusercontent.com/46697316/145130950-d75a7423-7a48-463d-b492-3484cb293b0e.png)

Type in the location of the piece that you want to move. For example, if I want to move a Black Piece on ‘i1’ then I type in i1. Then the prompt asks where you would like to place this piece. So if I want to move this piece to c1, then I type in c1. The move will look like this. The piece has moved from the blue circle i1 to the green circle c1. 

![Move Example](https://user-images.githubusercontent.com/46697316/145130985-e27c6ce4-5ffd-4923-8747-1c1f18c13b90.png)

###### Capturing Pieces
This game follows the custodian capture rule. Where if a piece or pieces are surrounded by the opponent on the same axis, then those pieces are captured. Here is an example of a capture. The red circle shows the cells where the pieces were captured. 

<img width="354" alt="Screen Shot 2021-12-07 at 8 19 34 PM" src="https://user-images.githubusercontent.com/46697316/145131384-7f3d2094-7760-4624-8393-398f96a4855d.png">

Captures can also be done on multiple axis at the same time. So you have pieces surrounded by the opponent on both the column and rows, the pieces can be all captured by the opponent with the correct move. 
Corner captures follow the rule too. If a piece is at a corner, and that piece is surrounded on 2 axises, row and a column. Then that piece is captured.

##### Winning the Game
To win the game, a player must either capture all but one of the opponents pieces or capture all the pieces. 

##### Code
The game is written in python only, using only 1 file titled, hasamishogigame.py. There is one Class for this entire game that stores the board information, player information and methods for rules for game play.

All the data members are private. The board is initilized with the pieces and the board information is stored in a list of lists.
There are several methods for this game. When a player makes a move, it takes the start and ending cells inputted by the player. These cells are then checked to determine if the move is valid. In order to check the correct cells, a search method is created to find the correct cell. The type of search used is binary search. 

To determine if pieces can move multiple places, another method is used to check if there are any pieces, or if the cells are 'null'. Again, to search all these cells, the search method is called.

For capturing, a method is created to determine if the correct sequence is met. If the sequence is met, then the capture is true, and the pieces are collected. To check the sequence a recursive method was created. The recursive method has several checks to determine if the pattern of pieces satisfies the sequence. 

##### Next Steps
The next steps of this game would be to add it as a web application game. Using this python script as the backend, would like to incorporate front-end, using HTML, CSS and Javscript. The end goal would be to have the end users simply drag their pieces to the desired cells instead of the user entering their desired move. 
