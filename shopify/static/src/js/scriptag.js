function showDiscount(code) {
    var tag = document.getElementsByClassName("product__text")[1];
    if (tag) {
        tag.innerHTML += `<div><h2 id="discount-script" class="title h2"> Bạn có 1 mã giảm giá: ${code} </h2></div>`;
    }

}

let data;

function makeDiscount(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

const userAction = async () => {

    const response = await fetch(location.origin + '/cart.js');
    const myJson = await response.json();
    myJson.shop_url = location.hostname
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "https://odoo.website/shopify/cart/list");
    xmlhttp.send(JSON.stringify(myJson));
    xmlhttp.onload = () => {
        console.log(ShopifyAnalytics.meta)
        data = JSON.parse(xmlhttp.response);
        discount_name = data.price_discount.combo.name;
        discount_price = data.price_discount.total_price_discount;

        var dE = document.getElementsByClassName("cart__footer")[0];
        console.log(discount_price)
        if (dE) {
            var dV = `<div class="js-contents">
                        <div class="totals">
                            <h2 class="totals__subtotal"><b>Bạn có 1 ưu đãi ${discount_name}</b> </h2>
                        </div>
                    </div>
                    <div class="js-contents">
                        <div class="totals">
                        <h2 class="totals__subtotal">Khi áp dụng</h2>
                            <p class="totals__subtotal-value">${discount_price.toLocaleString('vi-VN')} VND</p>
                            <button id="apply_dicount" class="cart__checkout-button button"> Apply</button>
                        </div>
                    </div>`
            dE.innerHTML += dV;
        }

    };
}

function findButton() {
    let btn_apply = document.getElementById("apply_dicount")
    if (btn_apply) {
        btn_apply.addEventListener('click', () => {
            data.shop_url = location.hostname
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", "https://odoo.website/shopify/combo/apply");
            xmlhttp.send(JSON.stringify(data))
            btn_apply.remove()
        })
        return
    } else {
        setTimeout(() => {
            findButton()
        }, 1000)
    }
}

function main() {
    const location = window.location
    const pageCurent = location.origin + location.pathname;
    const pageShow = location.origin + "/cart"
    if (pageCurent === pageShow) {
        userAction();
        findButton()
    }
    userAction2()
}

const userAction2 = async () => {

    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "https://odoo.website/shopify/combo/list");
    xhttp.send();
    xhttp.onload = function () {
        const combos = JSON.parse(xhttp.response)
        let tag = document.getElementsByClassName("product__text")[2];
        if (ShopifyAnalytics.meta.product.id) {
            console.log(ShopifyAnalytics.meta.product.id)
            console.log(combos)
            showDiscount(makeDiscount(10))
            for (let combo of combos) {
                if (combo.product_condition.product_id == ShopifyAnalytics.meta.product.id) {
                    if (combo.position == 'above') {
                        tag = document.getElementsByClassName("product__text")[1];
                    } else {
                        tag = document.getElementsByClassName("product__text")[2];

                    }
                    if (combo.is_percent) {
                        tag.innerHTML += `<div class="js-contents">
                    </div>
                    <div display: flex>
                    <div class="js-contents">
                        <div class="totals">
                        <h2 class="totals__subtotal">Combo: ${combo.name}</h2>
                            <p class="totals__subtotal-value"> ban duoc giam ${combo.value} % cho san pham</p>
                        </div>
                    </div>
                        <div> ${combo.product_condition.name}</div>
                        </div>`
                    } else {
                        tag.innerHTML += `<div class="js-contents">
                    </div>
                    <div display: flex>
                    <div class="js-contents">
                        <div class="totals">
                        <h2 class="totals__subtotal">Combo: ${combo.name}</h2>
                            <p class="totals__subtotal-value"> ban duoc giam ${combo.value} VND cho san pham</p>
                        </div>
                    </div>
                        <div> ${combo.product_condition.name}</div>
                        </div>`
                    }
                    if (combo.color == 'xanh') {
                        tag.innerHTML += ` <button class="btn" style="background: rgb(16, 89, 126) !important;\
                         color: #ffffff !important; " type="submit">ADD COMBO</button>   `
                    }
                    else if (combo.color == 'do') {
                        tag.innerHTML += ` <button class="btn" style="background: rgb(164, 11, 11) !important;
                        color: #ffffff !important; " type="submit">ADD COMBO</button>   `
                    }
                    else if (combo.color == 'vang') {
                        tag.innerHTML += ` <button class="btn" style="background: rgba(255,215,0) !important;
                        color: #ffffff !important; " type="submit">ADD COMBO</button>   `
                    }

                    // if (combo.color == "xanh") {
                    //     tag.innerHTML += <button class="btn btn-xanh" type="submit">ADD COMBO</button>
                    //
                    // } else {
                    //     tag.innerHTML += <button class="btn btn-do" type="submit">ADD COMBO</button>
                    // }
                }


            }
        }
    }

}
main();