document.addEventListener("DOMContentLoaded", () => {
    function refreshData() {
        axios.post('/shopify/webhook/list', {
            params: {}
        })
            .then(function (response) {
                data = response.data.result['webhooks']
                data.forEach((e) => {
                    bubble.topics.forEach((el) => {
                        if (e.topic === el.topic) {
                            el.id = e.id;
                            el.status = false
                        }
                    })
                });
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    refreshData();
    var bubble = new Vue({
        el: '#index-bubble',
        delimiters: ['[[', ']]'],
        data: {
            shopify: {
                topic: ''
            },
            name: 'hello world',
            topics: [{
                topic: 'orders/create',
                status: true,
                id: ""
            }, {
                topic: 'orders/updated',
                status: true,
                id: ""
            }, {
                topic: 'products/create',
                status: true,
                id: ""
            }, {
                topic: 'products/update',
                status: true,
                id: ""
            }]
        }, methods: {
            registerWebhook(topic) {
                console.log(topic)
                axios.post('/shopify/register-webhook', {

                    params: {
                        'topic': topic
                    }
                }).then(function (response) {
                    bubble.topics.filter((e) => {
                        if (e.topic === response.data.result.status.webhook.topic) {
                            e.status = false;
                        }
                    })
                })
                    .catch(function (error) {
                        console.log(error);
                    });
            },
            deleteWebhook(id) {
                axios.get('/shopify/webhook/delete', {

                    params: {
                        "id_webhook": id
                    }
                })
                    .then(function (response) {
                        bubble.topics.filter((e) => {
                            if (e.id === id) {
                                e.status = true;
                            }
                        })
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            }
        }
    })


});




