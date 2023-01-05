$ (function (){
   $($('tr#order_total_taxes td.text-right')[0]).text('Discount')
})
$.ajax({
        url: "/shop/cart/update_json",
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            jsonrpc: "2.0",
        params: {product_id: product_id},
        })
    }).then(response => {
            console.log(response.result);
            var data = response.result
            render_bundle_cart(data)
        }
    ).catch((error) => {
        console.log(error);
    });
function render_bundle_cart(data){
console.log('abc')
}
