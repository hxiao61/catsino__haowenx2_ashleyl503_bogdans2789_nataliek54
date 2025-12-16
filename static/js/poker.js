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

  document.getElementById('cds').appendChild(document.createTextNode(cards[0].code + " "));
  document.getElementById('cds').appendChild(document.createTextNode(cards[1].code + " "));
  document.getElementById('cds').appendChild(document.createTextNode(cards[2].code + " "));
  document.getElementById('cds').appendChild(document.createTextNode(cards[3].code + " "));
  document.getElementById('cds').appendChild(document.createTextNode(cards[4].code));
  bet = document.getElementById('betOUT').value;
}

function CheckHand()
{
  let message = document.getElementById('msg');
  let hasHand = 0;
  let multiplier = 0;
  let hands= [0, 0, 0, 0, 0, 0, 0, 0, 0];
  /*
  0 = royal flush
  1 = straight flush
  2 = four of a kind
  3 = full house
  4 = flush
  5 = straight
  7 = three of a kind
  8 = two pair
  9 = one pair
  */

  cards.sort();

  for (let i = 1; i < cards.length; i++) //checking for pairs, triples and fours of a kind
  {
    if (cards[i] == cards[i-1])
    {
      hasHand = 1;
      if (cards[i] == cards[i+1] && i<cards.length-1)
      {
        hands[7]++;
        i+=2;
      }
      if (cards[i] == cards[i+2] && i<cards.length-2)
      {
        hands[2]++;
        i+=3;
      }
      else
      {
        hands[9]++;
        i++;
      }
    }
  }

  if (hands[9] == 2)
    hands[8]++;
  if (hands[9] == 1 && hands[7] == 1)
    hands[]
}
