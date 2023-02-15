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
}

function findProductWithName(name) {
    for (let product of cart.products) {
        if (name == product.name) {
            return product
        }
    }
}

axios.get("/shopify/combo/report").then((res) => {
    let data = res.data.report

    data.forEach((rec) => {
        cart.label.push(rec.combo_name)
        cart.data.push(rec.total_apply)
    })
})

function chart() {


    const ctx = document.getElementById('myChart').getContext('2d');
    ctx.canvas.width = 300;
    ctx.canvas.height = 300;
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: cart.label,
            datasets: [{

                label: 'Combo',
                data: cart.data,
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
                borderWidth: 5
            }]
        },
        options: {
            scales: {

                y: {
                    beginAtZero: true
                }
            }
        }

    });
}

refreshData();
axios.get("/shopify/sync/product").then((res) => {
    cart.products = res.data.products
})


var cart = new Vue({
    el: '#cart-bubble',
    delimiters: ['[[', ']]'],
    data: {
        style: null,
        combo: [],
        data: [],
        label: [],
        value: {
            id: null,
            name: null,
            product_name: null,
            is_percent: null,
            type_apply: null,
            quantity_condition: null,
            product_lines: [],
            discount_value : null
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
                product_condition: null,
                is_percent: null,
                type_apply: null,
                quantity_condition: null,
                product_lines: [],
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
            line_product = {
                product: findProductWithName(cart.value.product_name),
                quantity: cart.value.quantity_condition,
                discount_value: cart.value.discount_value
            }
            console.log(line_product)
            console.log(cart.value.product_lines)
            let check = 0
            for (let line of cart.value.product_lines) {
                console.log(line)
                if (line.product.product_id==line_product.product.product_id) {
                    check = 1
                    line.quantity = line_product.quantity
                    line.discount_value = line_product.discount_value
                    break
                } else {
                    check = 0
                }
            }
            if (!check) {
                cart.value.product_lines.push(line_product)
                console.log(cart.value)
            }
            else{

            }
            // location.reload();
        },
        test: function () {


        }
    }

})

document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        chart();
    }, 100)


})
