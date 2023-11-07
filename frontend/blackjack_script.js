

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
// ctx.fillStyle = backgroundcolor;
// ctx.fillRect(0,0,width,height);
ctx.background = backgroundimage;
//grid
var gridx = 850;
var gridy = 550;


var nodeCount = 0;
var squaresize = 20;
const nodeList = [];
var startnode;
var endnode;

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
    this.sideup = 1; //1=front -1=back
    this.suit =suit;
    this.value=value;

  }
}


//class
class Node{
  constructor(x, y, id) {
    this.x = x;
    this.y = y;
    this.id;
    this.color = backgroundcolor;
    this.start = false;
    this.end = false;
    this.distance = -1;
    this.distfromend = -1;
  }
}

//call funcitons
draw_user_card();
draw_dealer_card();
draw_deck();
flip_card();
// creategrid();
// randomStartEndNode();
document.addEventListener("click", flipcard);

function draw_user_card(){
  ctx.beginPath();
  var id = 0;
  var x=userlocation[0];
  var y=userlocation[1];
  const card = new Card(x, y, id);
  id+=1;
  cardList.push(card);
  cardCount +=1;
  ctx.rect(x, y, cardsize[0], cardsize[1]);
  ctx.stroke();
  var cardimg = new Image(); 
  var cardSuit = cardSuits[Math.ceil(Math.random()*100)%numSuits];
  console.log(cardSuit)
  var cardValue = cardValues[Math.ceil(Math.random()*100)%numValues];
  cardimg.src = `/assets/Cards/${cardValue}_of_${cardSuit}.png`;
  cardimg.onload = function (e)
  {
      ctx.drawImage(cardimg, x, y, cardsize[0], cardsize[1]);
  }
}

function draw_deck(){
  ctx.beginPath();
  var id = 0;
  var x=decklocation[0];
  var y=decklocation[1];
  const card = new Card(x, y, id);
  id+=1;
  cardCount +=1;
  ctx.rect(x, y, cardsize[0], cardsize[1]);
  ctx.stroke();
  var cardimg = new Image(); 
  cardimg.src = card_backside;
  cardimg.onload = function (e)
  {
      ctx.drawImage(cardimg, x, y, cardsize[0], cardsize[1]);
  }
}

function draw_dealer_card(){
  ctx.beginPath();
  var id = 0;
  var x=decklocation[0]+100;
  var y=decklocation[1];
  const card = new Card(x, y, id);
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

function creategrid(){
  ctx.beginPath();
  var id = 0;
  for(var x=400; x<=gridx ;x+=squaresize+10){
    for(var y=100; y<=gridy;y+=squaresize+10){
      const n = new Node(x, y, id);
      id+=1;
      nodeList.push(n);
      nodeCount +=1;
      ctx.rect(x, y, squaresize, squaresize);
      ctx.stroke();
    }
  }
}


function colorMousePos(event) {
    var mousex = event.clientX; 
    var mousey = event.clientY;
    for (let item of nodeList) {
      if((item.x+squaresize > mousex) && (item.x-squaresize < mousex) && (item.y+squaresize > mousey) && (item.y-squaresize < mousey)){
        if(item.color === greycolor){
          item.color = backgroundcolor;
        }else if(item.color === backgroundcolor){
          item.color = greycolor;
        }
        colorNode(item);
        break;
      }
    } 
}


function flipcard(event) {
  var mousex = event.clientX; 
  var mousey = event.clientY;
  for (let item of cardList) {
    if((item.x+squaresize > mousex) && (item.x-squaresize < mousex) && (item.y+squaresize > mousey) && (item.y-squaresize < mousey)){
      item.sideup *= -1;
      drawcard(item);
      break;
    }
  } 
}


function randomStartEndNode(){
  var index = Math.floor(Math.random() * nodeCount);
  startnode = nodeList[index]  
  startnode.color = greencolor;
  startnode.start = true;
  colorNode(startnode);
  endnode = startnode;  
  while(endnode.start==true){
    index = Math.floor(Math.random() * nodeCount);
    endnode = nodeList[index]  
  }
  endnode.color = redcolor;
  endnode.end = true;
  colorNode(endnode);
}

function colorNode(n){
  ctx.fillStyle = n.color;
  ctx.fillRect(n.x, n.y, squaresize, squaresize);
  ctx.stroke();
}

function colorCard(n){
  ctx.fillStyle = n.color;
  ctx.fillRect(n.x, n.y, cardsize[0], cardsize[1]);
  ctx.stroke();
}

function hit() {
  for (let n of nodeList) {
    if(n.start===false && n.end===false){
      n.color = backgroundcolor;
      colorNode(n);
    }
  }
}


function stand() {
  for (let n of nodeList) {
    if(n.color!==greycolor){
      n.color = backgroundcolor;
    }
    n.start = false;
    n.end = false;
    colorNode(n);
  }
  randomStartEndNode();
}

function bet (){
  var pathlist = BFS();
  var i = 1;
  for (let p of pathlist) {
      //cause a delay
      setTimeout(function(){
        colorNode(p);
      }, 50*i);
      i+=1;
  }
  setTimeout(function(){
    tracePath(pathlist);
  }, 50*i);
}

function startAstarPath (){
  var pathlist = Astar();
  var i = 1;
  for (let p of pathlist) {
      //cause a delay
      setTimeout(function(){
        colorNode(p);
      }, 50*i);
      i+=1;
  }
  setTimeout(function(){
    tracePath(pathlist);
  }, 50*i);
}

//same as BFS but adds distance from node to end node
function Astar(){
  const graphlist = [...nodeList]
  var pathlist = [];
  const queuelist = [];
  var dist = 0;
  var n = startnode;
  n.distance = dist;
  n.distfromend = 0;
  queuelist.push(startnode);
  while(queuelist.length > 0){
    //sort queue by closest distances
    queuelist.sort((a, b) => (a.distfromend > b.distfromend) ? 1 : -1);
    n = queuelist[0];
    queuelist.shift();
    //add edges to queue 
    var distance = squaresize + 10;
    const edgecoords = [[n.x+distance, n.y], [n.x-distance, n.y],  //right left
      [n.x, n.y+distance], [n.x, n.y-distance]] //up down
    for(let e of edgecoords){
      for (let i=0;i!=graphlist.length;i++) {
        var m = graphlist[i];
        if(m.color != lightgreen){
          if(m.x === e[0] && m.y ===e[1]){
            if(m.end===true){
              m.distance = dist+=1;
              return pathlist;
            }
            if(m.color !== greycolor){
              m.color = lightgreen;
              if(m.start===false){
                queuelist.push(m);
                pathlist.push(m);
                m.distance = dist+=1;
                distFromEnd = ((n.x - endnode.x)**2 + (n.y-endnode.y)**2) ** 0.5
                console.log(distFromEnd);
                m.distfromend = distFromEnd;
              }
            }
          }
        }
      }
    }
  }
  return pathlist;
}



function BFS(){
  const graphlist = [...nodeList]
  var pathlist = [];
  const queuelist = [];
  var dist = 0;
  var n = startnode;
  n.distance = dist;
  queuelist.push(startnode);
  while(queuelist.length > 0){
    n = queuelist[0]
    queuelist.shift();
    //add edges to queue 
    var distance = squaresize + 10;
    const edgecoords = [[n.x+distance, n.y], [n.x-distance, n.y],  //right left
      [n.x, n.y+distance], [n.x, n.y-distance]] //up down
    for(let e of edgecoords){
      for (let i=0;i!=graphlist.length;i++) {
        var m = graphlist[i];
        if(m.color != lightgreen){
          if(m.x === e[0] && m.y ===e[1]){
            if(m.end===true){
              m.distance = dist+=1;
              return pathlist;
            }
            if(m.color !== greycolor){
              m.color = lightgreen;
              if(m.start===false){
                queuelist.push(m);
                pathlist.push(m);
                m.distance = dist+=1;
              }
            }
          }
        }
      }
    }
  }
  return pathlist;
}


//highlights shortest path in yellow
function tracePath(pathlist){
  var shortestpathnodes = []
  pathlist.push(startnode);
  var n = endnode;
  var mindist = n;
  var index = 0;
  var distance = 0;
  while(n !== startnode && index<=nodeCount){
    var found = false;
    distance = squaresize + 10;
    index+=1;
    const edgecoords = [[n.x+distance, n.y], [n.x-distance, n.y],  //right left
    [n.x, n.y+distance], [n.x, n.y-distance]] //up down
    for(let e of edgecoords){
      for (let i=0;i!=pathlist.length;i++) {
        var m = pathlist[i];
        if(m.x === e[0] && m.y ===e[1]){
          if(m===startnode){
            colorshortestpath(shortestpathnodes);
            return;
          }
          //update mindist node with smallest distance
          if(Math.min(m.distance, mindist.distance) < mindist.distance){
            mindist = m;
            found = true;
            break;
          }
          if(found===true){
            break;
          }
          mindist.color = yellowcolor;
          n = mindist;
          shortestpathnodes.push(n);
        }
      }
    }
  }
  colorshortestpath(shortestpathnodes);
}

function colorshortestpath(shortestpathnodes){
  var i = 1;
  for (let p of shortestpathnodes) {
      //cause a delay
      setTimeout(function(){
        colorNode(p);
      }, 20*i);
      i+=1;
  }
}


