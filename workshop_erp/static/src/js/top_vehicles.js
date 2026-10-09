/** @odoo-module */
import {renderToElement} from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";

export function chunk(array, size) {
    const res = [];
    for (let i = 0; i < array.length; i += size) {
        res.push(array.slice(i, i + size));
        console.log("res", res);
    }
    return res;
}

publicWidget.registry.get_top_vehicles = publicWidget.Widget.extend({
    selector: '.vehicle_section',
    async willStart() {
        const result = await rpc('/get_top_vehicles', {});
        Object.assign(this,
            {vehicles: result});
    },
    start: function () {
        const vehicles = this.vehicles.vehicles;
        const date = this.vehicles.date

        console.log("vehicles", vehicles)
        // const ne = chunk([1, 2, 3, 4, 5], 2);
        // console.log('new',ne)
        const chunks = chunk(vehicles, 4)
        console.log("chunks", chunks)

        chunks[0].is_active = true;
        if(vehicles){
            this.$target.empty().html(renderToElement('workshop_erp.vehicle_data', {chunks: chunks,date:date}))
        }
    },
});


// /** @odoo-module */
// import { renderToElement } from "@web/core/utils/render";
// import publicWidget from "@web/legacy/js/public/public_widget";
// import { rpc } from "@web/core/network/rpc";
// publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
//    selector : '.categories_section',
//    async willStart() {
//        const result = await rpc('/get_top_vehicles', {});
//        console.log(result)
//        if(result){
//            this.$target.empty().html(renderToElement('workshop_erp.category_data', {result: result}))
//        }
//    },
// });


// selector: '.dynamic_snippet_blog',
//
// willStart: async function() {
//
// var self = this;
//
// await rpc.query({
//
// route: '/latest_elearning_courses',
//
// }).then((data) => {
//
// this.data = data;
//
// });
//
// },
//
// start: function() {
//
// var chunks = _.chunk(this.data, 4)
//
// chunks[0].is_active = true
//
// this.$el.find('#courosel').html(
//
// qweb.render('elearning_course_snippet.elearning_snippet_carousel', {
//
// chunks
//
// })
//
// )
//
// },
// });
// PublicWidget.registry.dynamic_snippet_blog = Dynamic;
// return Dynamic;
// });