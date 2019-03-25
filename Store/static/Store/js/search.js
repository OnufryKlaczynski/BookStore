

// It could be changed on css pseudo-class focus-within 

function changeSearchFormColorOnFocus(){
    let element = document.querySelector("form#search");
    console.log(element);
    element.setAttribute("style", "background-color: rgba(0, 0, 0, 0.06);")
}

function changeSearchFormColorOnBlur(){
    let element = document.querySelector("form#search");
    console.log(element);
    element.setAttribute("style", "background-color: #fafafa;")
}

