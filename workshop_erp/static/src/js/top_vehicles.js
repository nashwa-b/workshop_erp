/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
// import { sortBy } from "@web/core/utils/arrays";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
export function _chunk(array, size){
    const res = [];
    for (let i = 0; i<array.length; i+=size){
        res.push(array.slice(i,i*size))}
    return res;
    }

publicWidget.registry.get_top_vehicles = publicWidget.Widget.extend({
   selector : '.vehicle_section',
   async willStart() {
       const result = await rpc('/get_top_vehicles', {});

       // willStart: async function () { const data = await jsonrpc('/top_selling_products', {})
           const vehicles = result
           Object.assign(this,
               {vehicles}) },
    start: function ()
    {
        const {vehicles} = this
        const chunks = _chunk(vehicles, 4)
         if(result){
           this.$target.empty().html(renderToElement('workshop_erp.vehicle_data', {result: result,chunks:chunks}))
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