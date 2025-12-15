let cards = [];
let deckId = "";
let bet = 0;

async function Setup()
{
  let idResponse = await fetch("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1");
  let idData = await idResponse.json();
  deckId = idData.deck_id;

  let drawResponse = await fetch(`https://deckofcardsapi.com/api/deck/${deckId}/draw/?count=5`);
  let drawData = await drawResponse.json();

  cards.push(drawData.cards[0]);
  cards.push(drawData.cards[1]);
  cards.push(drawData.cards[2]);
  cards.push(drawData.cards[3]);
  cards.push(drawData.cards[4]);

  document.getElementById('cds').appendChild(document.createTextNode(cards[0].code));
  document.getElementById('cds').appendChild(document.createTextNode(cards[1].code));
  document.getElementById('cds').appendChild(document.createTextNode(cards[2].code));
  document.getElementById('cds').appendChild(document.createTextNode(cards[3].code));
  document.getElementById('cds').appendChild(document.createTextNode(cards[4].code));

}

function SetBet()
{
  bet = document.getElementById('betIN').value;
  document.getElementById('betOUT').innerText = bet;
}
