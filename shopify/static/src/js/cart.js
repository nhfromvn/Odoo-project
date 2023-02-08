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
            })
        })
        cart.combo = vals
    })
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
    console.log(cart.products)
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
            product_condition: null,
            is_percent: null,
            type_apply: null,
            quantity_condition: null
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
        }
    }

})

document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        chart();
    }, 100)


})
