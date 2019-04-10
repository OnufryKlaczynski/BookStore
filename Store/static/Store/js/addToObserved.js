function addToObserved(event){
    const elementClicked = event.target;
    const bookId = elementClicked.getAttribute('data-book-id');
    let observed = elementClicked.classList.toggle("observed")

    const url = `${window.location.origin}/accounts/observed-books/${bookId}/`;
    
    if(observed === false){
        fetch(url, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
    
        }).then(response => console.log(response.json()))
        .catch(error => console.log(error));
    
    }else{
        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
    
        }).then(response => console.log(response.json()))
        .catch(error => console.log(error));
    
    }
    
}