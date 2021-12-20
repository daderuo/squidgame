const queryString = window.location.search;
console.log(queryString);

const urlParams = new URLSearchParams(queryString);

const m_id = urlParams.get('m_id')
console.log(m_id);

var opp1 = "";
var opp2 = ""
//Turn = 0 => opp1 guess and opp2 ball select
var turn = 0;
var opp1_ball_n = 0;
var opp2_ball_n = 0;
var opp1_ball_select = 0;
var opp2_ball_select = 0;
var opp1_guess = false;
var opp2_guess = false;
var active = true;
var game = "";
var winner = "";
var user = "";

const match_init = async () => {
    const response = await fetch(`/game1/load_match?id=${m_id}`);
    const json = await response.json();
    user = json.user;
    match = json.match
   
    console.log(match);
    console.log(user);
    
    opp1 = match.opp1;
    opp2 = match.opp2;
    turn = match.turn;
    opp1_ball_n = match.opp1_ball;
    opp2_ball_n = match.opp2_ball;
    opp1_ball_select = match.opp1_ball_sel;
    opp2_ball_select = match.opp2_ball_sel;
    opp1_guess = match.opp1_ball_guess;
    opp2_guess = match.opp2_ball_guess;
    active = match.active;
    game = match.game;
    winner = match.winner;
    user = user

    if(!active){
        turn = 2
    }
    
    PageUpdate();

    fade('container',true);
}

const value_update = async () => {
    const response = await fetch(`/game1/load_match?id=${m_id}`);
    const json = await response.json();
    user = json.user;
    match = json.match
    
    opp1 = match.opp1;
    opp2 = match.opp2;
    turn = match.turn;
    opp1_ball_n = match.opp1_ball;
    opp2_ball_n = match.opp2_ball;
    opp1_ball_select = match.opp1_ball_sel;
    opp2_ball_select = match.opp2_ball_sel;
    opp1_guess = match.opp1_ball_guess;
    opp2_guess = match.opp2_ball_guess;
    active = match.active;
    game = match.game;
    winner = match.winner;
    user = user

    if (user == 1){
        document.querySelector('#opp1-ball').style.color = 'red';
    }
    else{
        document.querySelector('#opp2-ball').style.color = 'red';
    }
    
    PageUpdate();
}

var guess = false;
var opp1_ball_text = "";
var opp2_ball_text = "";
var even_button = "";
var odd_button = "";
var ball_select_bar = "";
var ball_select_button = "";
var game_container = "";
var loop = '';

// The following function are copying from 
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener('DOMContentLoaded', function(){
    game_container = document.querySelector('#game-container');

    opp1_ball_text = document.querySelector("#opp1-ball");
    opp2_ball_text = document.querySelector("#opp2-ball");

    ball_select_bar = document.querySelector('#opp2-ball-select');
    
    ball_select_button = document.querySelector('#select');
    ball_select_button.addEventListener('click', function() {
        let csrftoken = getCookie('csrftoken');
        if (turn === 0){
            opp2_ball_select = parseInt(ball_select_bar.value);        
            fetch('/game1/update_match/'+m_id , {
                method: 'PUT',
                body: JSON.stringify({
                    b2_sel: opp2_ball_select
                }),
                headers: { "X-CSRFToken": csrftoken },
              }) 
        }
        else{
            opp1_ball_select = parseInt(ball_select_bar.value);        
            fetch('/game1/update_match/'+m_id , {
                method: 'PUT',
                body: JSON.stringify({
                    b1_sel: opp1_ball_select
                }),
                headers: { "X-CSRFToken": csrftoken },
              })   
        }        
    });

    even_button = document.querySelector("#even");
    even_button.addEventListener('click', function(){
        update_match(false);
        setTimeout(function(){turn_change()},300);
        //turn_change();           
    });
    odd_button = document.querySelector("#odd");
    odd_button.addEventListener('click', function(){
        update_match(true);
        setTimeout(function(){turn_change()},300);
        //turn_change();
    });

    match_init();

    loop = setInterval(function(){
        value_update();
        console.log('.');
    },2000);
});

function turn_change(){
    fetch(`/game1/turn_change/`+m_id)
    .then(response => response.json())
    .then(done => {
        console.log(done);
    });
}

function update_match(g){
    let csrftoken = getCookie('csrftoken');

    //g = false;
                
    fetch('/game1/update_match/'+m_id , {
        method: 'PUT',
        body: JSON.stringify({
            b1_guess: g,
            b2_guess: g
        }),
        headers: { "X-CSRFToken": csrftoken },
    });    
}

function fade(e,d) {
    let id = null;
    const elem = document.getElementById(e);

    if(d){
        elem.style.display = "block";
    }  
    //let pos = 0;
    let op = 0;
    let f_op = 100;
    if(d)
    {
        op = 0;
        f_op = 100;
    }
    else{
        op = 100;
        f_op = 0;
    }
    clearInterval(id);
    id = setInterval(frame, 10);   
    
    function frame() {
        if (op == f_op) {
        clearInterval(id);
        if(!d){
            elem.style.display = "none";
        } 
        } else {
        if(d){
            op++;
        }
        else{
            op--;
        }         
        elem.style.opacity = op + "%"; 
        }
    }
  }

function PageUpdate(){  
    
    if(turn === 0){
        //aggiorno quantità di biglie
        opp1_ball_text.innerHTML = opp1 + ":" + opp1_ball_n + " ball";
        opp2_ball_text.innerHTML = opp2 + ": " + opp2_ball_n + " ball";
        if(user === 1){ 
            guess_view();            
        }
        else{
            if (opp2_ball_select === 0){
                select_view(user);
            }
            else{
                wait_view();
            }            
        }
    }
    else if(turn === 1){
        //aggiorno quantità di biglie
        opp1_ball_text.innerHTML = opp1 + ":" + opp1_ball_n + " ball";
        opp2_ball_text.innerHTML = opp2 + ": " + opp2_ball_n + " ball";
        if(user === 1){            
            select_view();
            if (opp1_ball_select === 0){
                select_view();
            }
            else{
                wait_view();
            }
        }
        else{
            guess_view();
        }
    }
    else{
        final_view();
    }
}

function wait_view(){
    ball_select_bar.style.display = "none";
    ball_select_button.style.display = "none";
    even_button.style.display = "none";
    odd_button.style.display = "none";
}

function select_view(u){
    ball_select_bar.style.display = "inline";
    if(user === 1){
        ball_select_bar.max = opp1_ball_n;
    }
    else{
        ball_select_bar.max = opp2_ball_n;
    }
    datalist = document.querySelector('#tickmarks');
    datalist.innerHTML = "";
    for (let i = 1; i <= ball_select_bar.max; i++){
        option = document.createElement('option');
        option.value = i;
        option.label = i;
        datalist.append(option);
    }
    ball_select_button.style.display = "inline";
    even_button.style.display = "none";
    odd_button.style.display = "none";
}

function guess_view(){
    ball_select_bar.style.display = "none";
    ball_select_button.style.display = "none";
    if (user === 1 && opp2_ball_select > 0){
        even_button.style.display = "inline";
        odd_button.style.display = "inline";
    }
    else if (user === 2 && opp1_ball_select > 0){
        even_button.style.display = "inline";
        odd_button.style.display = "inline";
    }
    else{
        even_button.style.display = "none";
        odd_button.style.display = "none";
    }
    
}


function final_view(){
    ball_select_bar.style.display = "none";
    ball_select_button.style.display = "none";
    even_button.style.display = "none";
    odd_button.style.display = "none";
    game_container.innerHTML = "";

    t = document.createElement('h1')

    if(user === 1){
        if(opp1 === winner){
            //you win
            t.innerHTML = 'You WIN!';
            
        }
        else{
            //you lose
            t.innerHTML = 'You lose.';
        }
    }
    else{
        if(opp2 === winner){
            //you win
            t.innerHTML = 'You WIN!';
        }
        else{
            //you lose
            t.innerHTML = 'You lose.';
        }
    }

    game_container.append(t);

    r = document.createElement('button');
    r.id = 'restart';
    r.innerHTML = "Play";
    r.addEventListener('click', function(){
        fetch(`/find_game?game=1`)
                .then(response => response.json())
                .then(game => {
                    console.log(game.match);  
                    console.log(game.id);  

                    if(game.match){
                        location.href = 'http://127.0.0.1:8000/game1?m_id='+ game.id;
                    }
                    else{
                        fetch(`/find_opp?game=1`)
                        .then(response => response.json())
                        .then(opp => {
                            console.log(opp.user);  
                            console.log(opp.op);
                            if (!opp.op){
                                location.href = 'http://127.0.0.1:8000/waiting?game=1';
                            }
                            else{
                                fetch(`/match_create?opp=${opp.user}&game=1`)
                                .then(response => response.json())
                                .then(match => {
                                    location.href = 'http://127.0.0.1:8000/game1?m_id='+ match.match_id;
                                });
                            }
                        });
                    }
                });
    });
    game_container.append(r);
    
    dashboard = document.createElement('button');
    dashboard.id = 'dashboard';
    dashboard.innerHTML = "Home";
    dashboard.addEventListener('click', function(){
        location.href = "http://127.0.0.1:8000/";
    });
    game_container.append(dashboard);

    clearInterval(loop);
}

