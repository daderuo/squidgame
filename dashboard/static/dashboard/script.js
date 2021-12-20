



document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#home').addEventListener('click', () => load_view('home'));
    document.querySelector('#ranking').addEventListener('click', () => load_view('ranking'));
  
    // By default, load home
    load_view('home');
  
  });


  function load_view(view){
    game_view = document.querySelector('#game-view');
    game_list = document.querySelector('#game-list');
    ranking_view = document.querySelector('#ranking-view');
    var table = document.getElementById("gamer-list");


    if (view === 'home'){
        game_view.style.display = 'block';
        ranking_view.style.display = 'none';
        game_list.innerHTML = "";
        load_game_list();
    }
    else if (view === 'ranking'){
        game_view.style.display = 'none';
        ranking_view.style.display = 'block';
        table.innerHTML = "";
        load_gamer_list();
    }
}

function load_game_list(){
    fetch(`/games`)
    .then(response => response.json())
    .then(gs => {
        gs.forEach(function(g){
            game = document.createElement('div');
            game.addEventListener('click', function(){ 
                fetch(`/find_game?game=${g.id}`)
                .then(response => response.json())
                .then(game => {
                    console.log(game.match);  
                    console.log(game.id);  

                    if(game.match){
                        location.href = 'http://127.0.0.1:8000/game' + g.id + '?m_id='+ game.id;
                    }
                    else{
                        fetch(`/find_opp?game=${g.id}`)
                        .then(response => response.json())
                        .then(opp => {
                            console.log(opp.user);  
                            console.log(opp.op);
                            if (!opp.op){
                                location.href = 'http://127.0.0.1:8000/waiting?game='+g.id;
                            }
                            else{
                                fetch(`/match_create?opp=${opp.user}&game=${g.id}`)
                                .then(response => response.json())
                                .then(match => {
                                    location.href = 'http://127.0.0.1:8000/game' + g.id + '?m_id='+ match.match_id;
                                });
                            }
                        });
                    }
                });

                
                //location.href = 'http://127.0.0.1:8000/game' + g.id + '/';
            })
            game.className = 'game';
            game.style.backgroundImage = "url('http://127.0.0.1:8000/media/" + g.photo + "')";
            title = document.createElement('h3');
            title.className = 'game-title';
            title.innerHTML = g.name;
            title.style.backgroundColor = "rgba(255, 255, 255, 0.788)";
            game.append(title);
            document.querySelector('#game-list').append(game);
        });   
    });
}


function load_gamer_list(){
    
    fetch(`/gamer`)
    .then(response => response.json())
    .then(gs => {
        let i = 0;
        gs.forEach(function(g){            
            var table = document.getElementById("gamer-list");

            var row = table.insertRow(i);
            
            var cell1 = row.insertCell(0);
            cell1.className = "gamer-name";
            var cell2 = row.insertCell(1);
            cell2.className = "gamer-total";
            var cell3 = row.insertCell(2);
            cell3.className = "gamer-win";

            cell1.innerHTML = g.user;
            cell2.innerHTML = g.total_games;
            cell3.innerHTML = g.win_games;
            i++;
        });   
    });
}