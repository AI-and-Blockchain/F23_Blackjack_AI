
//global vars
//colors
const backgroundcolor =  'rgb(217, 222, 200)';
const backgroundimage =  "assets\ClassicBackground.png";
const greycolor = "rgb(77, 79, 102)";
const redcolor = "rgb(178,51,81)";
const greencolor = "rgb(136,178,51)";
const lightgreen = "rgb(108, 120, 106)";
const yellowcolor = "rgb(217, 197, 141)"

//canvas
const canvas = document.querySelector('.myCanvas');
const width = canvas.width = window.innerWidth;
const height = canvas.height = window.innerHeight;
const ctx = canvas.getContext('2d');
ctx.background = backgroundimage;




//card vars
var cardsize = [80, 120];
cardList = [];
cardCount = 0;
cardSuits = ["spades", "hearts", "clubs", "diamonds"];
numSuits = 4;
cardValues = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"];
numValues = 13;
decklocation = [900, 250]
userlocation = [810, 610]
card_backside = "/assets/Cards/backside.png"


//class
class Card{
  constructor(x, y, id, suit, value) {
    this.x = x;
    this.y = y;
    this.id;
    this.sideup = -1; //1=front -1=back
    this.suit =suit;
    this.value=value;

  }
}



//call funcitons
draw_user_card();
draw_dealer_card();
draw_deck();
document.addEventListener("click", flipcard);


function paintcard(card){
  var cardimg = new Image(); 
  var cardSuit = card.suit
  var cardValue = card.value
  cardimg.src = `/assets/Cards/${cardValue}_of_${cardSuit}.png`;
  if(card.sideup==-1){
    cardimg.src = card_backside;
  }
  cardimg.onload = function (e)
  {
      ctx.drawImage(cardimg, card.x, card.y, cardsize[0], cardsize[1]);
  }

}

function draw_user_card(){
  ctx.beginPath();
  var id = 0;
  var x=userlocation[0];
  var y=userlocation[1];
  var cardSuit = cardSuits[Math.ceil(Math.random()*100)%numSuits];
  var cardValue = cardValues[Math.ceil(Math.random()*100)%numValues];
  const card = new Card(x, y, id, cardSuit, cardValue);
  id+=1;
  cardList.push(card);
  cardCount +=1;
  paintcard(card);
}

function draw_deck(){
  ctx.beginPath();
  var id = 0;
  var x=decklocation[0];
  var y=decklocation[1];
  const card = new Card(x, y, id, );
  id+=1;
  cardCount +=1;
  paintcard(card);
}

function draw_dealer_card(){
  ctx.beginPath();
  var id = 0;
  var x=decklocation[0]+100;
  var y=decklocation[1];
  var cardSuit = cardSuits[Math.ceil(Math.random()*100)%numSuits];
  var cardValue = cardValues[Math.ceil(Math.random()*100)%numValues];
  const card = new Card(x, y, id, cardSuit, cardValue);
  id+=1;
  cardCount +=1;
  ctx.rect(x, y, cardsize[0], cardsize[1]);
  ctx.stroke();
  var cardimg = new Image(); 
  cardimg.src = `/assets/Cards/backside.png`;
  cardimg.onload = function (e)
  {
      ctx.drawImage(cardimg, x, y, cardsize[0], cardsize[1]);
  }
}

function flipcard(event) {
  var mousex = event.clientX; 
  var mousey = event.clientY;
  for (let item of cardList) {
    if((item.x+cardsize[0] > mousex) && (item.x-cardsize[0] < mousex) && (item.y+cardsize[1] > mousey) && (item.y-cardsize[1] < mousey)){
      item.sideup *= -1;
      console.log("clicked");
      paintcard(item);
      break;
    }
  } 
}

function hit() {
  console.log("hit")

}


function stand() {
  console.log("stand")
  
}

function bet (){
  console.log("bet")
}
