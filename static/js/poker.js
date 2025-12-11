let cards = [];
let deckId = "";

async function Setup()
{
  let idResponse = await fetch("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1");
  let idData = await idResponse.json();
  deckId = idData.deck_id;

  let cardResponse = await fetch("https://deckofcardsapi.com/api/deck/${deck_id}/draw/?count=5")
  let cardData = await cardResponse.json();

  cards.push(cardData.cards[0]);
  cards.push(cardData.cards[1]);
  cards.push(cardData.cards[2]);
  cards.push(cardData.cards[3]);
  cards.push(cardData.cards[4]);

  document.getElementById('cds').appendChild(cards[0]);
  document.getElementById('cds').appendChild(cards[1]);
  document.getElementById('cds').appendChild(cards[2]);
  document.getElementById('cds').appendChild(cards[3]);
  document.getElementById('cds').appendChild(cards[4]);

  document.getElementById('test').innerText = 'works';
}
