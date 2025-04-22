



document.getElementById('lag-boks').addEventListener('click', function () {
    const boxContainer = document.getElementById('boks-holder');
    // const checkboxes = document.querySelectorAll('.input-halvdel input[type="checkbox"]');

    const farge = document.querySelector('.input-halvdel input[type="color"]').value;

    const tekstStørrelse = document.querySelector('.input-halvdel select');
    const valgtTekstStørrelse = tekstStørrelse.options[tekstStørrelse.selectedIndex].value;

    const tekstInput = document.querySelector('.input-halvdel input[type="text"].tekst').value;
    const bredde = document.querySelector('.input-halvdel input[type="text"].boks-bredde').value;
    const høyde = document.querySelector('.input-halvdel input[type="text"].boks-høyde').value;
    const avrunding = document.querySelector('.input-halvdel input[type="text"].border-radius').value;
    const tekstFarge = document.querySelector('.input-halvdel input[type="color"].tekst-farge').value;
    const margin = document.querySelector('.input-halvdel input[type="checkbox"].margin');
    const mysteriKnapp = document.querySelector('.input-halvdel input[type="checkbox"].mysteri-knapp');
    let boksAntall = document.querySelector('.input-halvdel input[type="number"].boks-antall').value;

    if (!boksAntall) {
        boksAntall = 1;
    }
    for (let i = 0; i < boksAntall; i++){
        const box = document.createElement('div');
        box.classList.add("placeholder");
        if (bredde) {
            box.style.width = bredde;
        } else {
            box.style.width = '100px';
        }
        if (høyde) {
            box.style.height = høyde;
        } else {
            box.style.height = '100px';
        }
        box.style.border = '1px solid black';

        box.style.backgroundColor = farge;
        box.style.borderRadius = avrunding;

        if (margin.checked) {
            box.style.margin = '10px';
        } else {
            box.style.margin = '0';
        }
        
        tekst = document.createElement(valgtTekstStørrelse);
        tekst.textContent = tekstInput;
        box.style.color = tekstFarge;
        box.appendChild(tekst);

        if (mysteriKnapp.checked) {
            let epilepiKnapp = document.createElement('button');
            epilepiKnapp.classList.add('epileppiknapp');
            epilepiKnapp.textContent = 'knapp???';
            box.appendChild(epilepiKnapp);
            
        }
        
        boxContainer.appendChild(box);
    
        if(mysteriKnapp.checked) {
            box.querySelector('.epileppiknapp').addEventListener('click', function() {
                epilepi2(box);
            });
        }

        
        
        function bevegBoks(boks){
            
            if (!boks.classList.contains("draggable")) {

                let boxX = box.getBoundingClientRect().x
                let boxY = box.getBoundingClientRect().y
                box.style.left = `${boxX}px`;
                box.style.top = `${boxY}px`;

                boks.classList.add("draggable");
            }

            // const boxList = [];
            // boxList.push(document.getElementsByClassName("placeholder"));
            
            // for (let i = 0; i < boxList[0].length; i++) {        
            //     if (!boxList[0][i].classList.contains("draggable")) {
            //         boxList[0][i].classList.add("draggable");
            //     }
            // }
        }

        
        
        box.addEventListener("mousedown", function() {
            bevegBoks(box);
            
            box.addEventListener("keydown", function(event) {
                console.log(event);
                console.log("test");
                if (event.key === "f") {
                    epilepi2(box);
                }
            });
        });
        box.addEventListener('mousedown', function (e) {
            let offsetX = e.clientX - box.offsetLeft;
            let offsetY = e.clientY - box.offsetTop;

            function mouseMoveHandler(e) {
                box.style.left = `${e.clientX - offsetX}px`;
                box.style.top = `${e.clientY - offsetY}px`;
            }

            function mouseUpHandler() {
                document.removeEventListener('mousemove', mouseMoveHandler);
                document.removeEventListener('mouseup', mouseUpHandler);
            }

            document.addEventListener('mousemove', mouseMoveHandler);
            document.addEventListener('mouseup', mouseUpHandler);
            
            
        });
    }
});


function epilepi2(boks){
    setInterval(function () {
        boks.style.backgroundColor = getRandomColor2()
    },100);
}

function getRandomColor2() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}