function refreshData() {
    axios.get("/shopify/combo/list").then((res) => {
        var vals = []
        res.data.forEach((e) => {
            vals.push({
                id: e.id,
                name: e.name,
                product_condition: e.product_condition,
                value: e.value,
                is_percent: e.is_percent,
                type_apply: e.type_apply,
                quantity_condition: e.quantity_condition,
                product_lines: e.product_lines,
            })
        })
        cart.combo = vals
    })
    axios.get("/shopify/combo/report").then((res) => {
        let data = res.data.report
        data.forEach((rec) => {
            cart.label.push(rec.combo_name)
            cart.total_apply.push(rec.total_apply)
            cart.total_sale.push(rec.total_sale)
            console.log(data)
        })
    })
}

<<<<<<< HEAD
refreshData()

=======
>>>>>>> origin/bt_thuc_hanh_shopify
function findProductWithId(id) {
    for (let product of cart.products) {
        if (id == product.product_id) {
            return product
        }
    }
}

function findVariantWithId(id, product) {
    console.log(product)
    for (let variant of product.variants) {
        if (id == variant.variant_id) {
            return variant
            break
        }
    }
}


function chart() {
    const ctx = document.getElementById('myChart').getContext('2d');
    ctx.canvas.width = 300;
    ctx.canvas.height = 300;
    const myChart = new Chart(ctx, {
<<<<<<< HEAD
=======

>>>>>>> origin/bt_thuc_hanh_shopify
        data: {
            labels: cart.label,
            datasets: [{
                type: 'bar',
                label: 'Total Apply',
                data: cart.total_apply,
                borderWidth: 5
            },
                {
                    type: 'bar',
                    yAxisID: 'y1',
                    label: 'Total Sale',
                    data: cart.total_sale,
                    borderWidth: 5
                }
            ],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
        },
        options: {
            scales: {

                y: {
                    title: {
                        display: true,
                        text: 'Total Apply',
                    },

                    beginAtZero: true
                },
                y1: {
<<<<<<< HEAD
                    title: {
=======
                     title: {
>>>>>>> origin/bt_thuc_hanh_shopify
                        display: true,
                        text: 'Total Sale',
                    },
                    beginAtZero: true,
                    display: true,
                    position: 'right',
                }
            }
        }

    });
}

<<<<<<< HEAD
//
axios.get("/shopify/sync/product").then((res) => {
    cart.products = res.data.products
    console.log(res.data.products)
})
//
//
=======
refreshData();
axios.get("/shopify/sync/product").then((res) => {
    cart.products = res.data.products
})


>>>>>>> origin/bt_thuc_hanh_shopify
var cart = new Vue({
    el: '#cart-bubble',
    delimiters: ['[[', ']]'],
    data: {
        style: null,
        combo: [],
        total_apply: [],
        total_sale: [],
        label: [],
        value: {
            id: null,
            name: null,
            product_id: null,
            product: null,
            is_percent: null,
            type_apply: null,
            quantity_condition: null,
            product_lines: [],
            discount_value: null,
            product_variant: null
        },
        products: null,
        select_id: 0
    },
    methods: {
        onSelect(id) {

            cart.select_id = id
            cart.combo.forEach((e) => {
                if (e.id == id) {
                    cart.select = e.id
                    cart.value.id = e.id
                    cart.value.name = e.name
                    cart.value.value = e.value
                    cart.value.is_percent = e.is_percent
                    cart.value.type_apply = e.type_apply
                    cart.value.product_condition = e.product_condition.product_id
                    cart.value.quantity_condition = e.quantity_condition
                    cart.value.product_lines = e.product_lines


                }
            })
        },
        onSave() {
            if (cart.value.name) {
                axios.post('/shopify/combo/update', {
                        value: cart.value
                    }
                ).then((res) => {
                    if (res.data.result.status) {
                        location.reload();
                    }
                })
            } else {
                alert("Name is required")
            }

        },
        onCreate() {
            cart.value = {
                id: null,
                name: null,
                product_id: null,
                product: null,
                is_percent: null,
                type_apply: null,
                quantity_condition: null,
                product_lines: [],
                discount_value: null,
                product_variant: null
            }
        },
        onCheck(value) {
            if (value == 'percent') {
                cart.value.is_percent = true;
            } else if (value == 'amount') {
                cart.value.is_percent = false;
            } else if (value == 'only_product') {
                cart.value.type_apply = true
            } else {
                cart.value.type_apply = false

            }
        },
        onDelete() {
            if (cart.value.id) {
                axios.post('/shopify/combo/unlink', {
                        id: cart.value.id
                    }
                ).then((res) => {
                    if (res.data.result.status) {
                        location.reload();
                    }
                })
            } else {
                alert("ID is required")
            }
        },
        onAdd() {
            if (!cart.value.product_variant) {
                alert("chua chon variant")
            }
            let variant = findVariantWithId(cart.value.product_variant, cart.value.product)
            cart.value.product.variant_id = variant.variant_id
            line_product = {
                product: cart.value.product,
                quantity: cart.value.quantity_condition,
                discount_value: cart.value.discount_value,
                variant_id: variant.variant_id,
                variant_name: variant.variant_name
            }
            let check = 0
            for (let line of cart.value.product_lines) {
                if (line.variant_id == line_product.variant_id) {
                    check = 1
                    line.quantity = line_product.quantity
                    line.discount_value = line_product.discount_value
                    // line.variant_id = line_product.variant_id
                    // line.variant_name = line_product.variant_name
                    break
                } else {
                    check = 0
                }
            }
            if (!check) {
                cart.value.product_lines.push(line_product)

            } else {
            }
            console.log(line_product)
            console.log(cart.value.product_lines)
        },
        selectProduct: function () {
            console.log('haha')
            cart.value.product = findProductWithId(cart.value.product_id)
            if (cart.value.product.variants.length == 1) {
                cart.value.product_variant = cart.value.product.variant_id
            }

        }
    }

})
<<<<<<< HEAD
=======

>>>>>>> origin/bt_thuc_hanh_shopify
document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        chart();
    }, 100)


})
