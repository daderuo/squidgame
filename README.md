# DadeGame
## This website is inspired to the Netflix tv show Squidgame. Yes, this is a platform for multiplayer game (obvieosly if you lose, you will not die).
## Distinctiveness and Complexity: 
This web application is a multiplayer games platform, not ad ecommerce or a social web site. This web application utilize Django in the back-end, javascript on the front-end and it is mobile-responsive.

## Web application main files:
As it is possible to see inside the main folder we can find two application:

### Dashboard:
This application manage users,games and match.

#### template/dashboard/
login.html, register.html: Basically used for create new users and login existings. In both cases, using a Django model form User(abstractuser) we add new user to a database or check if existing and log it into the web app.

layout.html: This file contain element always showed on the top of user-interface. Contains the main button for navigate trought different views. Home button show the user the game list. Ranking Show the list of all users ordered by winned games.

index.html: Using buttons described above this page change dinamically witout reload, just show/hide elements. This functionality is possible using API and fetch request using javascript to Django views. Ranking view doesnt allow interaction, just shows data. In gameview every game showed in the list, when clicked, generate some fetch request in order to understand:
- if current user have a match already running
   - yes: go directly to the match
   - no: next fetch request
- if there is an opponent already waiting for this game
   - yes: go directly to the game
   - no: create a waiting list item and redirect to waiting.hmtl

waiting.html: Is just a "waiting room" showed every time a user doesnt find an opponent imidiatly for the choosen game. The js code is very simple, every 2 seconds this page perform a fetch request in order to understand if an opponent is available. If it is, server create a new match and redirect to game page.

### static/dashboard

script.js contain three simple views: load view manage wich view/function call based on the request.
Load game list create a grid element for every game. Every item has an eventListener 'click'that provide funcions described above.
Load gamer list basically create a table, in the first position we have the user with more win match and at the and the user with less win games.

styles.css contain some media queries in order to provide mobile-responsive design.

### Game1:
This is the first real multiplayer game implemented in this web application. EVEN or ODD

### templates/game

This folder contain only one html page. This game has a single page user interfase design.

### static/game

styles.css contain some media queries in order to provide mobile-responsive design.

BallGame_mp.js, with views.py are the real core of the application.

When a new match starts also a new match item is added to the database by dashboard application.
BallGame.js every two seconds request updated data to the database.

When match start opp1 (opponent1) have to select how many balls bet on this turn, opp2 (opponent2) have to guess if the opp1 ball number is even or odd. if opp2 guess right: opp2 gain as much ball as opp1 bet and opp1 lose the same amount of balls.
EXAMPLE: opp1 srtart with 10 balls, same opp2:
if opp1 bet 5 balls, Opp2 guess odd. Now opp 1 has 5 balls and opp2 has 15 balls;
if opp1 bet 5 balls, Opp2 guess even. Now opp 1 has 15 balls and opp2 has 5 balls;

First opponent that reach 0 balls lose the match.

This javascript provide functions for update the user interface when turns change and when both users are allowed to play the next step of the game. At the same time trought some fetch request to views.py update the match database in order to store the last turn data.
If browser crash or connection is lost during match the user can easily resume the game at the same point.

The game has basicly 4 views:
1. select view: in this view user has to select how many ballswant to bet during this turn
2. guess view: in this view user has to guess even or odd just clicking the related button (obviously these two views will never showed at the same time)
3. wait view: a user can not guess even or odd until other opponent bet some balls,and a user cannot change the number of balls he bet, basically in this view user have no command to use, have just to wait the opponent to play.
4. final view: whan the metch is at the end a text will inform the user if he win or he lose and two button appear (Play again and home page)


Basicly every page, every function, every views has @login required because a user that is not logged in can't play to games.

### media/photo

This folder contain game related images, in order to store images inside this folder and inside the game related database i've used the Pillow python extension ( as it is possible to see inside requirement.txt)

## A Docker enviroment is already set-up so for run this application you just need to provide "docker-compose up" command
