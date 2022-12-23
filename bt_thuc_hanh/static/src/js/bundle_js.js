order_data = [{product_id: 1, amount: 10},{product_id: 2, amount :1}];


this._rpc({

        route: '/bundle-update',

        params: { order_products: order_data, note: note }

    }).then((data) => {

        window.location = '/contactus-thank-you';

    }).catch((error) => {

        console.error(error);

    });