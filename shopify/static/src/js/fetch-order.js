document.addEventListener("DOMContentLoaded", () => {
    var bubbled = new Vue({
        el: '#date-picker',
        delimiters: ['[[', ']]'],
        data: {
            historyFetch: [],
            history: {},
            timePicker: {
                startTime: null,
                endTime: null,
            },
            totalFetch: 0
        }, methods: {
            fetchOrders(start, end) {
                var date = new Date()
                var param = {}
                if (start) {
                    param['start'] = Date.parse(start)
                }
                if (end) {
                    param['end'] = Date.parse(end)
                }
                axios.get("/shopify/api/fetch-order", {
                    params: param
                }).then(function (response) {
                    if (response.data.orders) {
                        const totalProduct = response.data.orders.length
                        bubbled.totalFetch = totalProduct;
                        let time = date.toLocaleDateString() + " " + date.toLocaleTimeString()
                        var a = bubbled.history = {quantity: totalProduct, time: time}
                        bubbled.historyFetch.push(a)
                    }

                })
                    .catch(function (error) {
                        console.log(error);
                    });
            }, clearHistory() {
                bubbled.historyFetch = []
            }

        }

    });
});
