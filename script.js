
document.getElementById("game_name_submit_button").onclick = function(){

    let user_request = document.getElementById("game_name_input").value ;
    let text = "";
    let i = 1;
    fetch(`https://desicheapsahrk.onrender.com/search?user_request=${user_request}`)
    .then(response => response.json())
    .then(data => { data.forEach(element => {
        text += `${i}. ${element["name"]} \n`;
        i++;
                    });

    let game_list_header = document.createElement("h3");

    game_list_header.textContent = text;

    game_list_header.style.whiteSpace = "pre-line";

    document.body.appendChild(game_list_header);

    let game_choice = document.createElement("input");

    let br1 = document.createElement("br");

    let br2 = document.createElement("br");

    game_choice.type = "text";

    game_choice.id = "game_choice_input";

    game_choice.placeholder = "Enter num of game";

    document.body.appendChild(game_choice);

    document.body.appendChild(br1);

    document.body.appendChild(br2);

    let number_submit = document.createElement("button");

    number_submit.id = "number_submit_button";

    number_submit.textContent = "submit";

    number_submit.onclick = function(){
    let game_number = Number(document.getElementById("game_choice_input").value);
    fetch(`https://desicheapsahrk.onrender.com/game?game_id=${game_number}`)
    .then(response => response.json())
    .then(data => {console.log(data)
    fetch("https://desicheapsahrk.onrender.com/SteamURL")
    .then(response => response.json())
    .then(data => {console.log(data)
    let a1 = document.createElement("a");
    a1.textContent = "SteamLink";
    a1.href = data[0];
    a1.id = "Steam_Link";
    a1.target = "_blank";
    let br3 = document.createElement("br");
    let br4 = document.createElement("br");
    document.body.appendChild(br3);
    document.body.appendChild(br4);
    document.body.appendChild(a1);
    fetch("https://desicheapsahrk.onrender.com/EpicURL")
    .then(response => response.json())
    .then(data => {console.log(data)
    let a2 = document.createElement("a");
    a2.textContent = "EpicLink";
    a2.href = data[0];
    a2.id = "Epic_Link";
    a2.target = "_blank";
    let br5 = document.createElement("br");
    let br6 = document.createElement("br");
    document.body.appendChild(br5);
    document.body.appendChild(br6);
    document.body.appendChild(a2);
    fetch("https://desicheapsahrk.onrender.com/steam")
    .then(response => response.json())
    .then(data => {console.log(data)
    let p1 = document.createElement("p");
    p1.textContent = data[0];
    let br7 = document.createElement("br");
    document.body.appendChild(br7);
    document.body.appendChild(p1);
    fetch("https://desicheapsahrk.onrender.com/epic")
    .then(response => response.json())
    .then(data => {console.log(data)
    let p2 = document.createElement("p");
    p2.textContent = data[0];
    document.body.appendChild(p2);
    fetch("https://desicheapsahrk.onrender.com/finalResult")
    .then(response => response.json())
    .then(data => {
        console.log(data);
        let p3 = document.createElement("p");
        p3.textContent = data;
        document.body.appendChild(p3);
    })
    .catch(error => console.log(error))
    })
    .catch(error => console.log(error))
    })
    .catch(error => console.log(error))
    })
    .catch(error => console.log(error))
    })
    .catch(error => console.log(error))
    })
    .catch(error => console.log(error));
    }
    document.body.appendChild(number_submit);
})
    .catch(error => console.log(error));

}



