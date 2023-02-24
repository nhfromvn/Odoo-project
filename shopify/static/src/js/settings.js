document.addEventListener("DOMContentLoaded", () => {
    function refreshData() {
        axios.get('/shopify/register_script-tags').then(
            function (res) {
                if (res.data.status == 'success') {
                    script_tags.registered = 1
                } else if (res.data.status == 'registered') {
                    script_tags.registered = 1
                }
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    refreshData();
    var script_tags = new Vue({
        el: '#script_tags-button',
        delimiters: ['[[', ']]'],
        data: {
            registered: null,
        },
    });
});


