

function dropDownMenu(){
    let active = this.classList.toggle("active");
    if(active !== false){
        document.querySelector("#search").style.display="block";
        document.querySelector("#favourites").style.display="block";
        document.querySelector("#settings").style.display="block";
        document.querySelector("#cart").style.display="block";
    }else{
        document.querySelector("#search").style.display="none";
        document.querySelector("#favourites").style.display="none";
        document.querySelector("#settings").style.display="none";
        document.querySelector("#cart").style.display="none";
    }

}



const menuElement = document.querySelector("#menu");
menuElement.onclick = dropDownMenu;
