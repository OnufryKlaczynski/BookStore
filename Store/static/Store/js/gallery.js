class Gallery{
    constructor(galleryElement, leftArrow, rightArrow){
        this.galleryElement = galleryElement
        this.length = galleryElement.children.length;
        this.from = 0;
        console.log(parseInt(galleryElement.offsetWidth/204))
        this.gap = parseInt(galleryElement.offsetWidth/204);
        this.leftArrow = leftArrow;
        this.rightArrow = rightArrow;
        this.leftArrow.onclick = this.moveGalleryLeft.bind(this);
        this.rightArrow.onclick = this.moveGalleryRight.bind(this);
        this.displayElements();
    }   

    displayElements(){
        let from = this.from;
        let to = from+this.gap;
        for (let i = this.length-1; i>=0 ; i--) {
            if(i>=to || i<from){
                this.galleryElement.children[i].style.display = "none";
                console.log(this.galleryElement.children[i])
                    
            }else{
                this.galleryElement.children[i].style.display = "inline-block";
            }
        }
    }

    moveGalleryLeft(){
        if(this.from == 0){
            return;
        }
        this.from -= 1;
        
        this.displayElements();
    }
    moveGalleryRight(){
        if(this.from+this.gap == this.length){
            return;
        }
        this.from += 1;
        this.displayElements();
    }
}


const leftArrow = document.querySelector(".left");
const rightArrow = document.querySelector(".right"); 

const otherBooksElement = document.querySelector(".other-books");

new Gallery(otherBooksElement, leftArrow, rightArrow);