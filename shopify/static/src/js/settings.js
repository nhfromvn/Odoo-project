function main() {
    console.log("klasjflsaj")
}

main()
var script_tags = new Vue({
    el: '#script_tags-button',
    delimiters: ['[[', ']]'],
    data: {
        registered: null,
    },
    methods:
        {
            register() {
                axios.get('/shopify/register_script-tags').then(
                    function (res) {
                        if (res.data.status == 'success'){
                            script_tags.registered = 1
                        }
                        else if(res.data.status == 'registered'){
                            alert("khong the dang ki lai")
                            script_tags.registered = 1
                        }
                            })
                    .catch(function (error) {
                        console.log(error);
                    });
            },
        }
});
