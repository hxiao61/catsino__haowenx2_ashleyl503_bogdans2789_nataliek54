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
    checkForBlackjack();
}

async function hit(){
    if (!gameActive) return;

    let response = await fetch(`https://deckofcardsapi.com/api/deck/${deckId}/draw/?count=1`)
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

    updateDealerScoreUI();

    let dealerScore = calculateScore(dealerCards);
    let playerScore = calculateScore(playerCards);

    while(dealerScore < 17){
        let response = await fetch(`https://deckofcardsapi.com/api/deck/${deckId}/draw/?count=1`);
        let data = await response.json();
        dealerCards.push(data.cards[0]);
        dealerScore = calculateScore(dealerCards);

        updateDealerScoreUI();
    }


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
    let score = 0;
    let aces = 0;

    for(let i = 0; i < cards.length; i++){
        let card = cards[i];

        if(card.value == "ACE") {
            score += 11;
            aces++;
        } else if (card.value == "KING" || card.value == "QUEEN" || card.value == "JACK"){
            score += 10;
        } else {
            score += parseInt(card.value);
        }
    }

    while (score > 21 && aces > 0){
        score -= 10;
        aces -= 1;
    }

    return score;
}

function updateUI(){
    document.getElementById('dealer-hand').innerHTML = "";
    document.getElementById('player-hand').innerHTML = "";

    for(let i = 0; i < dealerCards.length; i++){
        let img = document.createElement('img');
        img.className = 'card-img';

        if (gameActive && i == 0){
            img.src = "https://www.deckofcardsapi.com/static/img/back.png";
        } else {
            img.src = dealerCards[i].image;
        }
        document.getElementById('dealer-hand').appendChild(img);
    }

    for (let card of playerCards) {
        displayCard(card, 'player-hand');
    }
    document.getElementById('player-score').innerText = calculateScore(playerCards);
}

function displayCard(card, elementID){
    let img = document.createElement('img');
    img.src = card.image;
    img.className = 'card-img';
    document.getElementById(elementID).appendChild(img);
}

function updateDealerScoreUI(){
    document.getElementById('dealer-score').innerText = calculateScore(dealerCards);
    let dealerDiv = document.getElementById('dealer-hand');
    dealerDiv.innerHTML = "";
    for (let card of dealerCards) {
        let img = document.createElement('img');
        img.src = card.image;
        img.className = 'card-img';
        dealerDiv.appendChild(img);
    }
}

function checkForBlackjack() {
    let pScore = calculateScore(playerCards);
    if (pScore == 21){
        endGame("Blackjack! You win!");
    }
}

function endGame(msg) {
    gameActive = false;
    document.getElementById('message').innerText = msg;
    document.getElementById('hit-btn').disabled = true;
    document.getElementById('stand-btn').disabled = true;
    document.getElementById('start-btn').disabled = false;
    updateDealerScoreUI();
}