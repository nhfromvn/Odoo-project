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
        accountId: null,
        contactId: null,
        listContacts: [],
        listConnection: [],
        listAccounts: [],
        isSelected: "",
        orders: []
    }, methods: {

        selectCompany(company) {
            bubled.isSelected = company;
            axios.get("/xero/list-contact", {
                params: {
                    tenant_id: bubled.isSelected
                }
            }).then((res) => {
                if (res.data.status == "success") {
                    bubled.listContacts = res.data.result.Contacts
                }
            })
            axios.get("/xero/list-account", {
                params: {
                    tenant_id: bubled.isSelected
                }
            }).then((res) => {
                if (res.data.status == "success") {
                    bubled.listAccounts = res.data.result.Accounts
                    console.log(bubled.listAccounts)
                }
            })
        }
    }
})
var xero = new Vue({
    el: '#xero-orders',
    delimiters: ['[[', ']]'],
    data: {
        orders: [],
        historySync: [],
        history: {},
        timePicker: {
            startTime: null,
            endTime: null,
        },
        totalSync: 0
    }, methods: {
        selectCompany(company) {
            bubled.isSelected = company;
        },
        syncAll() {
            if (bubled.accountId && bubled.contactId && xero.timePicker.startTime && xero.timePicker.endTime) {
                axios.get('/xero/sync-all-orders', {
                    params: {
                        tenant_id: bubled.isSelected,
                        contact_id: bubled.contactId,
                        account_id: bubled.accountId,
                        start_time: xero.timePicker.startTime,
                        end_time: xero.timePicker.endTime
                    }
                }).then(function (res) {
                    if (res.data.status == "synced") {
                        alert("nothing to synced")
                    } else {
                        alert("success")
                    }
                })
                    .catch(function (error) {
                        console.log(error);
                    })
                    .then(function () {
                        // luôn luôn được thực thi
                    });
            } else {
                alert("chua chon day du thong tin")
            }
        },
        synOrder(id) {
            if (bubled.accountId && bubled.contactId && xero.timePicker.startTime && xero.timePicker.endTime) {
                console.log(id)
                axios.get('/shopify/sync/order', {
                    params: {
                        tenant_id: bubled.isSelected,
                        order_id: id,
                        contact_id: bubled.contactId,
                        account_id: bubled.accountId,
                        start_time: xero.timePicker.startTime,
                        end_time: xero.timePicker.endTime
                    }
                })
                    .then(function (res) {
                        console.log(res);
                        if (res.data.status == "order error") {
                            alert("can't sync this order to payment be cause of status is not 'paid'")
                        } else if (res.data.status == "payments error") {
                            alert("can't sync this order to payment \n" +
                                res.data.result.Message)
                        } else if (res.data.status == "line error") {
                            alert("this order has no item")
                        } else if (res.data.status == "synced") {
                            alert("this order is already synced")
                        } else {
                            alert("success")
                        }
                    })
                    .catch(function (error) {
                        console.log(error);
                    })
                    .then(function () {
                        // luôn luôn được thực thi
                    });
            } else {
                alert("chua chon day du thong tin")
            }
        }
    }
})
