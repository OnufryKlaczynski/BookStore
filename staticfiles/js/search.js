function changeSearchFormColorOnFocus(){
    let element = document.querySelector("form#search");
    element.setAttribute("style", "background-color: rgba(0, 0, 0, 0.06);")
}

function changeSearchFormColorOnBlur(){
    let element = document.querySelector("form#search");
    element.setAttribute("style", "background-color: #fafafa;")
}

