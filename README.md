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

waiting.html: Is just a "waiting room" showed every time a user doesnt find an opponent imidiatly for the choosen game. The code is very simple, every 2 seconds this page perform a fetch request in order to understand if an opponent is available. If it is, server create a new match and redirect to game page.

### Game1:
This is the first real multiplayer game implemented in this web application. EVEN or ODD
