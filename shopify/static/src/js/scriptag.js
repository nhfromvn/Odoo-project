showDiscount = (code) => {
    var tag = document.getElementsByClassName("product__text")[1];
    if (tag) {
        tag.innerHTML += `<div><h2 id="discount-script" class="title h2"> Bạn có 1 mã giảm giá: ${code} </h2></div>`;
    }

}

let data;
var item_quantities = document.getElementsByClassName("cart-item__quantity")

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
        data = JSON.parse(xmlhttp.response);
        discount_price = data.best_discount.price_discount;
        combo_name = data.best_discount.combo_name
        console.log(myJson.total_price / 100)
        total_price = myJson.total_price / 100 - discount_price
        var dE = document.getElementsByClassName("cart__footer")[0];

        if (dE) {
            var dV = `<div class="js-contents">
                        <div class="totals">
                            <h2><b>Bạn có 1 ưu đãi ${combo_name}</b> </h2>
                        </div>
                    </div>
                    <div class="js-contents">
                        <div class="combo">
                        <h2 class="combo_description">Khi áp dụng duoc giam</h2>
                            <p class="combo_price">${discount_price} VND con ${total_price} VND</p>                            
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
            xmlhttp.onload = (res) => {
                console.log(res)
            }
            btn_apply.remove()
        })
        return
    } else {
        setTimeout(() => {
            findButton()
        }, 1000)
    }
}

function findAddButton(combos) {
    let btns = document.getElementsByClassName('btn_add')
    if (btns) {
        console.log(btns)
        for (let btn_add of btns) {
            console.log(btn_add)
            for (let combo of combos) {
                if (combo.id == btn_add.getAttribute('combo_id')) {
                    btn_add.addEventListener('click', () => {
                        let items = []
                        for (let product of combo.product_lines) {
                            console.log(combo.product_lines)
                            items.push({
                                'id': product.variant_id,
                                'quantity': product.quantity
                            })
                        }
                        let formData = {
                            'items': items
                        };
                        fetch(window.Shopify.routes.root + 'cart/add.js', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(formData)
                        })
                            .then(response => {
                                window.location.replace(window.Shopify.routes.root + 'cart');
                                return response.json();
                            })
                            .catch((error) => {
                                console.error('Error:', error);
                            })
                    })

                }

            }
        }
    } else {
        setTimeout(() => {
            findAddButton()
        }, 1000)
    }
    return
}


function main() {
    const location = window.location
    const pageCurent = location.origin + location.pathname;
    const pageShow = location.origin + "/cart"
    if (pageCurent === pageShow) {
        userAction();
        findButton();
    }
    userAction2()

}

const userAction2 = async () => {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "https://odoo.website/shopify/combo/list");
    xhttp.send(Shopify.shop);
    xhttp.onload = function () {
        var combos = JSON.parse(xhttp.response)
        let tag = document.getElementsByClassName("product__text")[2];
        if (ShopifyAnalytics.meta.product.id) {
            showDiscount(makeDiscount(10))
            for (let combo of combos) {
                let items = []
                for (let product_line of combo.product_lines) {
                    items.push({
                        'id': product_line.variant_id,
                        'quantity': product_line.quantity
                    })
                }
                var formData = {
                    'items': items
                }
                let check = 0
                for (let product_line of combo.product_lines) {
                    if (product_line.product.product_id == ShopifyAnalytics.meta.product.id) {
                        check = 1
                        break
                    } else {
                        check = 0
                    }
                }
                if (check) {
                    if (combo.position == 'above') {
                        tag = document.getElementsByClassName("product__text")[1];
                    } else {
                        tag = document.getElementsByClassName("product__text")[2];

                    }
                    if (combo.type_apply) {
                        if (combo.is_percent) {
                            tag.innerHTML += `<div class="js-contents">
                                            </div>
                                            <div display: flex>
                                            <div class="js-contents">
                                            <div class="totals">
                                            <h2 class="totals__subtotal">Combo: ${combo.name}</h2>
                                            </div>`
                            for (let product_line of combo.product_lines) {
                                tag.innerHTML += `</div>
                                            <div>ban duoc giam ${product_line.discount_value} % cho san pham ${product_line.product.name} ${product_line.variant_name} x ${product_line.quantity}</div>
                                            </div>`
                            }

                        } else {
                            tag.innerHTML += `<div class="js-contents">
                                            </div>
                                            <div display: flex>
                                            <div class="js-contents">
                                            <div class="totals">
                                            <h2 class="totals__subtotal">Combo: ${combo.name}</h2>                         
                                            </div>`
                            for (let product_line of combo.product_lines) {
                                tag.innerHTML += `</div>
                                                        <div>ban duoc giam ${product_line.discount_value} vnd cho san pham ${product_line.product.name} ${product_line.variant_name} x ${product_line.quantity}</div>
                                                        </div>`
                            }
                        }

                    } else {
                        if (combo.is_percent) {
                            tag.innerHTML += `<div class="js-contents">
                                            </div>
                                            <div display: flex>
                                            <div class="js-contents">
                                            <div class="totals">
                                            <h2 class="totals__subtotal">Combo: ${combo.name}</h2>
                                                <p class="totals__subtotal-value"> ban duoc giam ${combo.value} % cho combo</p>
                                            </div>`
                            for (let product_line of combo.product_lines) {
                                tag.innerHTML += `</div>
                                                    <div> ${product_line.product.name} ${product_line.variant_name} x ${product_line.quantity}</div>
                                                    </div>`
                            }

                        } else {
                            tag.innerHTML += `<div class="js-contents">
                                            </div>
                                            <div display: flex>
                                            <div class="js-contents">
                                            <div class="totals">
                                            <h2 class="totals__subtotal">Combo: ${combo.name}</h2>
                                                <p class="totals__subtotal-value"> ban duoc giam ${combo.value} vnd cho combo</p>
                                            </div>`
                            for (let product_line of combo.product_lines) {
                                tag.innerHTML += `</div>
                                                <div> ${product_line.product.name} ${product_line.variant_name} x ${product_line.quantity}</div>
                                                </div>`
                            }
                        }
                    }
                    if (combo.color) {
                        tag.innerHTML += ` <button  id="add_combo" combo_id =${combo.id} class="btn btn_add" style="background: ${combo.color} !important;\
                         color: #ffffff !important; " type="submit">ADD COMBO</button> `
                    }
                }

            }
            findAddButton(combos)
        }
    }
}
main();