function addToObserved(event){
    const elementClicked = event.target;
    const bookId = elementClicked.getAttribute('data-book-id');
      

    const url = `${window.location.origin}/accounts/observed-books/${bookId}/`;

    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        }

    }).then(response => console.log(response.json()));

}