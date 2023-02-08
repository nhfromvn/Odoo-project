document.addEventListener("DOMContentLoaded", () => {
    axios.get("/xero/list-connections").then((res) => {
        var listConnect = [];
        if (res.data.status == "success") {
            res.data.result.forEach(function (e) {
                listConnect.push({name: e.tenantName, tenantId: e.tenantId});
            });
            bubled.listConnection = listConnect;

        }
    })

    axios.get("/shopify/order/list").then((res) => {
        var listConnect = [];
        if (res.data.status == "success") {
            xero.orders = res.data.orders
        }
    })
})

var bubled = new Vue({
    el: '#xero-connection',
    delimiters: ['[[', ']]'],
    data: {
        listConnection: [],
        isSelected: "",
        orders: []
    }, methods: {
        selectCompany(company) {
            bubled.isSelected = company;
        }
    }
})
var xero = new Vue({
    el: '#xero-orders',
    delimiters: ['[[', ']]'],
    data: {
        orders: []
    }, methods: {
        selectCompany(company) {
            bubled.isSelected = company;
        },
        synOrder(id) {
            console.log(id)
            axios.get('/shopify/sync/order', {
                params: {
                    tenant_id: bubled.isSelected,
                    order_id: id
                }
            })
                .then(function () {
                    console.log('hihi');
                })
                .catch(function (error) {
                    console.log(error);
                })
                .then(function () {
                    // luôn luôn được thực thi
                });


        }
    }
})
