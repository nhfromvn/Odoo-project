$(function () {
    $($('tr#order_total_taxes td.text-right')[0]).text('Discount')
    let input = $('input.js_quantity')
    console.log(input)
    input[0].addEventListener("onchange", changeText)

})
// $('input.js_quantity').addEventListener("onchange", changeText);
//
function changeText() {
    $($('tr#order_total_taxes td.text-right')[0]).text('Discount')
}

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
    render_bundle_cart(data)
});

function render_bundle_cart(data) {
    $($('tr#order_total_taxes td.text-right')[0]).text('Discount')

}
