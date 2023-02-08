function showDiscount(code) {
    const element = document.getElementsByClassName("product__info-wrapper")[0].children[0].children[1]
    if(element){
        element.innerHTML += `<div><h2 id="discount-script" class="title h2"> Bạn có 1 mã giảm giá: ${code} </h2></div>`;
    }
}


function makeDiscount(length) {
    let result = '';
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

    showDiscount(makeDiscount(10));