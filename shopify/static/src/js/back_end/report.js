odoo.define('s_discount_report', function (require) {
    "use strict";
    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');
    var core = require('web.core');
    var QWeb = core.qweb;

    var DiscountGraph = AbstractField.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        _render: function () {
            var self = this;
            var data = JSON.parse(this.value);
            this.$el.html('<canvas id="discount_graph" width="800" height="100"></canvas>');
            var interval = setInterval(function () {
                if (document.getElementById('discount_graph')) {
                    clearInterval(interval);
                    var ctx = document.getElementById('bundle_purchase_value_graph').getContext('2d');
                    var myChartLine = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: [],
                            datasets: []
                        },
                        options: {
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero: true,
                                        stepSize: 1
                                    }
                                }]
                            }
                        }
                    });

                }
            }, 500)
        }
    });


    registry.add('discount_graph', DiscountGraph);

})