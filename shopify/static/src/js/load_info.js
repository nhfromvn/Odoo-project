document.addEventListener("DOMContentLoaded", () => {
    function refreshData() {
        axios.post('/xero/check-connect', {
            params: {}
        })
            .then(function (response) {
                data = response.data.result.status
                info.status_xero = data
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    refreshData();
    var info = new Vue({
        el: '#index-info',
        delimiters: ['[[', ']]'],
        data: {
            status_xero: null,
            product: null
        }
    });

    axios.get("/shopify/sync/product").then((res) => {
        if (res.data.error){
            alert("Can not load product please connect app again!")
        }
    })

});




