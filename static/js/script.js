function epilepi(){
    let boxes = document.querySelectorAll(".bestillinger_boxbox")
    setInterval(function test() {
        for (let i = 0; i < boxes.length; i++) {
            console.log("in for loop");
            boxes[i].style.backgroundColor = getRandomColor()
            document.body.style.backgroundColor = getRandomColor()
            document.addEventListener("keydown", function(event) {
                if (event.key === "g") {
                    throw new Error("Epilepi gone sad");
                }
            });
        }
        
    }, 5);
    
}

document.addEventListener("keydown", function(event) {
    if (event.key === "f") {
        epilepi();
    }
});
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

document.addEventListener('DOMContentLoaded', function() {epilepi();});

function tilbakemelding_knapp() {
    console.log("called tilbakemelding_knapp")
    document.querySelector('.tilbakemelding').style.visibility = 'visible'; 
} 

function admin_passord() {
   document.querySelector('.admin_passord').classList.toggle("hide")
} 

function nullstill() {
    document.querySelector('.tilbakemelding').style.visibility = 'hidden'; 
}


let sideVerdi = document.querySelector('.hidden');
const velgSide =  document.querySelectorAll('.velg_side');

velgSide.forEach(function(element) {
    element.addEventListener('click', function(e) {
        for (side of velgSide) {
            side.style.backgroundColor = '';
        }
        sideVerdi.value = e.target.id;
        document.forms["side_form"].submit();
        e.target.style.backgroundColor = 'lightblue';
    });
});

let admin = document.querySelector('#admin');
console.log(admin);
admin.addEventListener("click", function(){
    admin_passord()
});