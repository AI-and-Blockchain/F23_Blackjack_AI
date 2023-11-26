
//global vars
//colors
const backgroundcolor =  'rgb(217, 222, 200)';
const backgroundimage =  "./assets/blackjack_table.jpg";
const greycolor = "rgb(77, 79, 102)";
const redcolor = "rgb(178,51,81)";
const greencolor = "rgb(136,178,51)";
const lightgreen = "rgb(108, 120, 106)";
const yellowcolor = "rgb(217, 197, 141)"

const pageAccessedByReload = (
  (window.performance.navigation && window.performance.navigation.type === 1) ||
    window.performance
      .getEntriesByType('navigation')
      .map((nav) => nav.type)
      .includes('reload')
);
const pageAccessedByButtons = (
  (window.performance.navigation && window.performance.navigation.type === 1) ||
    window.performance
      .getEntriesByType('navigation')
      .map((nav) => nav.type)
      .includes('back_forward')
);

//canvas
const canvas = document.querySelector('.myCanvas');
const width = canvas.width = window.innerWidth;
const height = canvas.height = window.innerHeight;
const ctx = canvas.getContext('2d');
ctx.background = backgroundimage;




//card vars
var cardsize = [80, 120];
var cardSuits = ["spades", "hearts", "clubs", "diamonds"];
var numSuits = 4;
var cardValues = ["", "ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"];
var numValues = 13;
var decklocation = [62.5/100, 31.2/100];
var userlocation = [47/100, 77/100];  
var cardoffset = [50, 10];
var card_backside = "./assets/Cards/backside.png";

var id = 0;
var bet_amount = 0;
var numDealerCards = 0;
var numPlayerCards = 0;
var cardList = [];
var hit_active = false;
var stand_active = false;
var bet_active = true;
var deal_active = false;
var exit_active = false;
var player_name;
var player_address;
var playerObjects = []

var changeBalanceCode = ""


//class
class Card{
  constructor(x, y, id, suit, value, angle) {
    this.x = x;
    this.y = y;
    this.id = id;
    this.sideup = -1; //1=front -1=back
    this.fliplocked = 0;
    this.suit =suit;
    this.value=value;
    this.angle = angle;
    this.card_count = 0;

  }
}

class Player{
  constructor(x, y,  name, address, angle, main_player) {
    this.x = x;
    this.y = y;
    this.name = name;
    this.address = address;
    this.angle = angle;
    this.main_player = main_player;
  }
}

window.onload = function() {
  if (pageAccessedByReload) {
    location.href = "Login.html";
  } else if (pageAccessedByButtons) {
    location.href = "Login.html";
  } else {
    init_game();
  }
  fetch('/byteCode', {
    method: 'POST',
    body: JSON.stringify({func: "changeBalance(address,uint256,bool)"}),
    headers: {
        'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
      changeBalanceCode = data.func;
  })
  checkBalance();
}

//init game: call funcitons


function init_game(){
  fetch("/playerData", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
      }
    }).then(response => response.json())
    .then(data => {
      if (data.username === "") {
        location.href = "Login.html";
      }
      player_name = data.username;
      player_address = data.address;
  init_players();
  init_dealer_deck();
  new_game();
  document.addEventListener("click", flipcard);
  })
}

function init_players(){
    main_player = new Player(userlocation[0], userlocation[1], player_name, player_address, 0, 1);
    console.log(main_player.main_player);
    console.log(main_player.name);
    ai_player = new Player(userlocation[0]+0.17, userlocation[1]-0.06, "Mr.JokerPoker", 0, -5, 0);
    playerObjects.push(main_player, ai_player);
}

function deal(){
  if(deal_active){
    fetch("/deal", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      }
    }).then(response => response.json())
    .then(data => {
      deal_all_cards(data.players, data.dealer);
      deal_active = false;
      bet_active = false;
      hit_active = true;
      stand_active = true;
    })
  }
}

function paintcard(card){
  var cardimg = new Image(); 
  var cardSuit = card.suit
  var cardValue = card.value
  cardimg.src = `./assets/Cards/${cardValue}_of_${cardSuit}.png`;
  if(card.sideup ===-1){
    cardimg.src = card_backside;
  }
  cardimg.onload = function (e)
  {
    ctx.save();
    ctx.translate(card.x, card.y);
    ctx.rotate(Math.PI/card.angle);
    ctx.drawImage(cardimg, (cardoffset[0]*card.card_count), (cardoffset[1]*card.card_count), cardsize[0], cardsize[1]);
    ctx.restore();
  }

}

function init_dealer_deck(){
  ctx.beginPath();
  var x=decklocation[0]*width;
  var y=decklocation[1]*height;
  const card = new Card(x, y, 0, null, null);
  paintcard(card);
}

function deal_all_cards(cards, dealerCards){
  for (let i = 0; i < 2; i++) {
    var count = 0;
    for(let p of playerObjects){
      ctx.beginPath();
      var x=p.x*width;
      var y=p.y*height;
      var cardSuit = cardSuits[Math.ceil(Math.random()*100)%numSuits];
      var cardValue = cardValues[cards[count][0][i]];
      const card = new Card(x, y, id, cardSuit, cardValue, p.angle);
      card.card_count = p.card_count;
      id+=1;
      cardList.push(card);
      p.card_count +=1;
      console.log(p.main_player);
      if(p.main_player === 1){
        numPlayerCards+=1;
      }
      card.fliplocked = 0;
      card.sideup = 1;
      // setTimeout(function(){paintcard(card)}, 200 * (count + (i*2) + 1));
      paintcard(card);
      count++;
    }
    ctx.beginPath();
    var x=decklocation[0]*width-(cardoffset[0]*numDealerCards)-200;
    var y=decklocation[1]*height-(cardoffset[1]*numDealerCards);
    var cardSuit = cardSuits[Math.ceil(Math.random()*100)%numSuits];
    var cardValue = cardValues[dealerCards[i]];
    var card = new Card(x, y, id, cardSuit, cardValue);
    if(numDealerCards === 0){
      card.fliplocked = 1;
      card.sideup = 1; 
    }else{
      card.fliplocked = 1;
      card.sideup = -1;
    }
    id+=1;
    numDealerCards+=1;
    cardList.push(card);
    // setTimeout(function(){paintcard(card)}, 250 * (playerObjects.length - count + (i*2) + 1));
    paintcard(card);
  }
}

function deal_user_card(p, c){
  ctx.beginPath();
  var x=p.x*width;
  var y=p.y*height;
  var cardSuit = cardSuits[Math.ceil(Math.random()*100)%numSuits];
  var cardValue = cardValues[c];
  const card = new Card(x, y, id, cardSuit, cardValue, p.angle);
  card.card_count = p.card_count;
  id+=1;
  cardList.push(card);
  p.card_count +=1;
  console.log(p.main_player);
  if(p.main_player === 1){
    numPlayerCards+=1;
  }
  card.fliplocked = 0;
  card.sideup = 1;
  paintcard(card);
}

function deal_dealer_card(c){
  ctx.beginPath();
  var x=decklocation[0]*width-(cardoffset[0]*numDealerCards)-200;
  var y=decklocation[1]*height- (cardoffset[1]*numDealerCards);
  var cardSuit = cardSuits[Math.ceil(Math.random()*100)%numSuits];
  var cardValue = cardValues[c];
  var card = new Card(x, y, id, cardSuit, cardValue);
  if(numDealerCards === 0){
    card.fliplocked = 1;
    card.sideup = -1; 
  }else{
    card.sideup = 1;
  }
  id+=1;
  numDealerCards+=1;
  cardList.push(card);
  paintcard(card);
}

function flipcard(event) {
  var mousex = event.clientX; 
  var mousey = event.clientY;
  for (let card of cardList) {
    x = card.x + cardoffset[0]*card.card_count;
    y = card.y + cardoffset[0]*card.card_count;
    if((x+cardsize[0] > mousex) && (x-cardsize[0] < mousex) && (y+cardsize[1] > mousey) && (y-cardsize[1] < mousey)){
      if(card.fliplocked === 0){
        card.sideup *= -1;
        paintcard(card);
      }else{
        paintcard(card);
      }
      break;
    }
  } 
}

function hit() {
  if(hit_active){
    fetch("/hit", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      }
    }).then(response => response.json())
    .then(data => {
      deal_user_card(playerObjects[0], data.card);
      if (!data.status) {
        stand();
      }
    })
  }

}

function stand() {
  if(stand_active){
    fetch("/stand", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      }
    }).then(_ => {
      fetch("/AI", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
      }).then(response => response.json())
      .then(data => {
        for (let i = 0; i < data.cards.length; i++) {
          for (let c of data.cards[i]) {
            deal_user_card(playerObjects[i+1], c);
          }
        }
        fetch("/dealer", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          }
        }).then(response => response.json())
        .then(data => {
          for (let c of data.cards) {
            deal_dealer_card(c);
          }
          var j=0;
          for (let item of cardList) {
            item.sideup = 1;
            item.fliplocked = 1;
            setTimeout(function(){paintcard(item)}, 200*j);
            j+=1
          }
          //reorder cards
          setTimeout(function(){
          for (let item of cardList) {
            paintcard(item);
          }}, 300*numPlayerCards);
          fetch("/results", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
          }).then(response => response.json())
          .then(async data => {
            for (let i = 0; i < data.data.length; i++) {
              document.getElementById(i == 0 ? "playerStatus" : i == 1 ? "AI1Status" : "AI2Status").innerHTML = data.data[i][0];
            }
            await changeBal(data.data[0][1]);
            stand_active = false;
            hit_active = false;
            bet_amount = 0;
          })
        })
      })
    })
  }
}

function new_game(){
  for(let p of playerObjects){
    p.card_count = 0;
  }
  numPlayerCards = 0;
  bet_amount = 0;
  numDealerCards = 0;
  cardList = [];
  hit_active = false;
  stand_active = false;
  bet_active = true;
  deal_active = false;
  exit_active = true;
  repaint_canvas();
}

function repaint_canvas(){
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  init_dealer_deck();
  paint_playername();

}

function paint_playername(){
  for(let p of playerObjects){
    ctx.save();
    ctx.translate( (p.x+0.03) * width, (p.y+0.22) * height);
    ctx.rotate( Math.PI / p.angle );
    ctx.font = "bold 20px Arial";
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.fillText(`${p.name}`, p.angle*-20, p.angle*-2);
    ctx.restore();
  }
}

function bet_helper(a){
  if(bet_active){
    if(bet_amount===0){
      new_game();
    }
    repaint_canvas();
    deal_active = true;
    ctx.fillStyle = "gold";
    ctx.font = "20px Comic Sans";
    bet_amount = a;
    ctx.fillText(`+${bet_amount} WEI...`, 77/100*width, 37.5/100*height);
  }
}

function plus(){
  if (Number(document.getElementById("balanceLabel").innerHTML) >= bet_amount + 10) {
    bet_helper(bet_amount + 10);
  }
}
function minus(){
  if(bet_amount > 10){
    bet_helper(bet_amount - 10);
  }
}

function bet(){
  if (bet_amount == 0) {
    return;
  }
  var jsonData = {"address":   player_address, "bet": bet_amount, message: ""};
  console.log(jsonData);
  fetch("/setBet", {
      method: "POST",
      body: JSON.stringify(jsonData),
      headers: {
          "Content-Type": "application/json"
      }
  }).then(response => response.json())
  .then(data => {
    // alert(data.bet)
    if (data.message == "invalid") {
      alert("Invalid bet, please do not bet higher than your wallet balance")
      deal_active = false;
    } else {
        bet_active = false;
        exit_active = false;
        deal_active = true;
    }
  })
  .then(json => {
    console.log(json);
  })
  .catch(error => {
      console.error('Error:', error);
  });

}

function exit() {
  if (exit_active) {
    location.href = "Login.html";
  }
}


async function changeBal(modifier) {
  await getAccount();

  var amount = hex64(bet_amount * Math.abs(modifier));
  console.log(amount);  
  var increase = hex64(modifier == -1 ? "0": "1");

  fetch('/owner', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
      var owner = pad64(data.address);

      ethereum
      .request({
          method: 'eth_sendTransaction',
          params: [
          {
              from: account, // The user's active address.
              to: contract,
              data: changeBalanceCode + owner + amount + increase,
              gasLimit: '0x5028', // Customizable by the user during MetaMask confirmation.
              maxPriorityFeePerGas: '0x3b9aca00', // Customizable by the user during MetaMask confirmation.
              maxFeePerGas: '0x2540be400', // Customizable by the user during MetaMask confirmation.
          },
          ],
      })
      .then((txHash) => {
              console.log(txHash);
              fetch('/trackTransaction', {
                  method: 'POST',
                  body: JSON.stringify({address: txHash}),
                  headers: {
                      'Content-Type': 'application/json'
                  }
              })
              .then(async _ => {
                await checkBalance();
                if (Number(document.getElementById("balanceLabel").innerHTML) < 10) {
                  setTimeout(function(){alert("You do not have enough money to continue betting, please exit and deposit more.")}, 10);
                  hit_active = false;
                  stand_active = false;
                  bet_active = false;
                  deal_active = false;
                  exit_active = true;
                } else {
                  bet_active = true;
                  exit_active = true;
                }
              })
      })
      .catch((_) => changeBal(modifier));
      })
}