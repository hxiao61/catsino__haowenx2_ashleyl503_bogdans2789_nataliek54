let deckID = "";
let dealerCards = [];
let playerCards = [];
let gameActive = false;

async function startGame(){
    document.getElementById('message').innerText = "";
    document.getElementById('dealer-hand').innerHTML = "";
    document.getElementById('player-hand').innerHTML = "";
    document.getElementById('dealer-score').innerText = "?";
    document.getElementById('player-score').innerText = "0";

    document.getElementById('hit-btn').disabled = false;
    document.getElementById('stand-btn').disabled = false;
    document.getElementById('start-btn').disabled = true;

    dealerCards = [];
    playerCards = [];
    gameActive = true;

    let response = await fetch('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1');
    let data = await response.json();
    deckId = data.deck_id;

    let drawResponse = await fetch('https://deckofcardsapi.com/api/deck/${deckId}/draw/?count=4');
    let drawData = await drawResponse.json();

    dealerCards.push(drawData.cards[0]);
    dealerCards.push(drawData.cards[1]);
    playerCards.push(drawData.cards[2]);
    playerCards.push(drawData.cards[3]);

    updateUI();
    checkForBlackJack();
}

async function hit(){

}

async function stand(){

}

function calculateScore(cards){

}

function updateUI(){

}

function displayCard(card, elementID){

}

function updateDealerScoreUI(){

}

function checkForBlackjack() {

}

function endGame(msg) {
    
}