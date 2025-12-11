let deckId = "";
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

    let response = await fetch(`https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1`);
    let data = await response.json();
    deckId = data.deck_id;

    let drawResponse = await fetch(`https://deckofcardsapi.com/api/deck/${deckId}/draw/?count=4`);
    let drawData = await drawResponse.json();

    dealerCards.push(drawData.cards[0]);
    dealerCards.push(drawData.cards[1]);
    playerCards.push(drawData.cards[2]);
    playerCards.push(drawData.cards[3]);

    updateUI();
    checkForBlackJack();
}

async function hit(){
    if (!gameActive) return;

    let response = await fetch(`https://deckofcardsapi.com/api/deck/${deckId}/draw/?count=4`)
    let data = await response.json();

    playerCards.push(data.cards[0]);
    updateUI();

    let score = calculateScore(playerCards);
    if(score>21){
        endGame("You Busted lol");
    }
}

async function stand(){
    if (!gameActive) return;

    let dealerScore = calculateScore(dealerCards);
    let playerScore = calculateScore(playerCards);
    while(dealerScore < 17){
        let response = await fetch(`https://deckofcardsapi.com/api/deck/${deckId}/draw/?count=1`);
        let data = await response.json();
        dealerCards.push(data.cards[0]);
        dealerScore = calculateScore(dealerCards);
        displayCard(data.card[0], 'dealer-hand');
    }

    updateDealerScoreUI();

    if(dealerScore > 21) {
        endGame("Dealer Busted, you win");
    } else if (playerScore > dealerScore){
        endGame("You beat the Dealer!");
    } else if (playerScore < dealerScore){
        endGame("Dealer Wins");
    } else {
        endGame("Tie, refunded");
    }
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