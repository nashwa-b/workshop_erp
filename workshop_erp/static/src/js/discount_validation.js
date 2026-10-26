/** @odoo-module **/
import {PosOrderline} from "@point_of_sale/app/models/pos_order_line";
import { ask } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

// import { useService } from "@web/core/utils/hooks";
// import { PosCategory } from "@point_of_sale/static/tests/unit/data/product_category.data";
// import {PosCategory} from "@point_of_sale/app/models/pos_category";
// import { models } from "@web/../tests/web_test_helpers";
import {useService} from "@web/core/utils/hooks";


import {patch} from "@web/core/utils/patch";
// import {usePos} from "@point_of_sale/app/hooks/pos_hook";
// import {parseFloat} from "@web/views/fields/parsers";
import {WarningDialog} from "@web/core/errors/error_dialogs";
// import {useService} from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";
// import { PosCategory } from "./pos_category.data";
// import { models } from "@web/../tests/web_test_helpers";
// import { PosCategory } from "@point_of_sale/../pos_category.data";

//
// patch(PosOrderline.prototype, {
//     setup() {
//         super.setup(...arguments);
//         // Do not use useService here
//     },
//
//     myMethodToOpenAlert() {
//         // Access the dialog service via the environment object
//         const dialogService = this.env.services.dialog;
//
//         dialogService.add(AlertDialog, {
//             title: "Alert",
//             body: "Your message here",
//         });
//     }
// });
//

patch(PosOrderline.prototype, {

    setup() {
        super.setup();
        // this.notification = useService("notification");
        // this.notification = useService("notification");
    },

    async setDiscount(discount) {

        // const dialogService = this.env.services.dialog;

        // const category = this.product_id?.categ_id;


        // const max_discount = Number(category?.max_discount??0);
        // const max_discount = category?.max_discount??0;
        // const max_discount = category.max_discount;

        // const category = this.pos.models['pos.category'].get(categoryId);

        // const categoryId = 5;
        // const category = this.pos.models['pos.category'].get();
        // console.log(category.max_discount);


        // const parsed_discount =
        //     typeof max_discount === "number"
        //         ? max_discount
        //         : isNaN(parseFloat(max_discount))
        //         ? 0
        //         : parseFloat("" + max_discount);
        // console.log(parsed_discount)

        // console.log("lkj", max_discount)
        //     super.setup(...arguments);
        //     set_discount(discount){
        // const parsed_discount =
        //     typeof discount === "number"
        //         ? discount
        //         : isNaN(parseFloat(discount))
        //             ? 0
        //             : parseFloat("" + discount);

        // var disc = Math.min(Math.max(parsed_discount || 0, 0), 100);
        // var disc = Math.min(Math.max(parsed_discount || 0, 0), 100);
        // const disc = Math.min(Math.max(parsed_discount || 0, 0), 100);
        // console.log(discount)
        // console.log(this.product_id.name)
        // // console.log(this.product_id.name)
        // console.log(this.product_id.categ_id.name)
        // console.log(this.product_id.spare_type)
        // console.log("max_discount",this.product_id.categ_id.max_discount)
        // console.log("max_discount",this.product_id.categ_id.hour_after)
        // console.log("max_discount",this.product_id.categ_id.color)
        // console.log(this.config)
        // console.log(this.config.category_wise_discount)
        // console.log(this.config.max_discount)
        // console.log(this.pos.config)


        // console.log(this.categ_id.discount)

        // var maxDiscount = this.product.maxDiscount;
        //
        // console.log(this.pos.config)
        // if (this.pos.config) {

        const m_discount = this.product_id.pos_categ_ids[0].max_discount;
        console.log("p", m_discount)
        const product = this.product_id.name

        if (this.config.category_wise_discount && discount > m_discount){

            // const notification = this.pos.env.services.notification;

            // this.notification.add(_t("Quantity limit warning! Review your stock."), {
            //     title: _t("Warning"),
            //     type: "warning",
            //     sticky: false,
            // });

            // return {
            //         title: _t("Positive quantity not allowed"),
            //         body: _t(
            //             "Only a negative quantity is allowed for this refund line. Click on +/- to modify the quantity to be refunded."
            //         ),
            //     };





            console.log("The maximum allowed discount for", product, " is ", m_discount)

            // notification.add(
            // _t("Save your work and refresh to get the latest updates and avoid potential issues."),
            // {
            //     title: _t("The page is out of date"),
            //     type: "warning",
            //     sticky: true,
            //     buttons: [
            //         {
            //             name: _t("Refresh"),
            //             primary: true,
            //             onClick: () => browser.location.reload(),
            //         },
            //     ],
            // });


            // return {
            //     title: _t("Ticket error"),
            //     body: _t("You cannot change quantity for a line linked with an event registration"),
            // };

        //     console.log("yyy")
        //     this.discount = 0;
        //     this.DiscountStr = "0";
        // return super.setDiscount(...arguments)
        } else {
            this.discount = discount;
            this.DiscountStr = "" + discount;
            console.log("pp")
        }
        // return
    },
    // return super.setup(...arguments);
});


// setDiscount(discount) {
// const parsed_discount =
//     typeof discount === "number"
//         ? discount
//         : isNaN(parseFloat(discount))
//         ? 0
//         : parseFloat("" + discount);
//
// const disc = Math.min(Math.max(parsed_discount || 0, 0), 100);
// this.discount = disc;
// }


// import { patch } from "@web/core/utils/patch";
// import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
//
// patch(PosOrderline.prototype, {
//     _load_pos_data_fields() {
//         return [...super._load_pos_data_fields(), "spare_type"];
//     },
// });


//     _load_pos_data_fields() {
//         return [
//             ...super._load_pos_data_fields(),
//             "spare_type",
//             // "reward_id",
//             // "coupon_id",
//             // "reward_identifier_code",
//             // "points_cost",
//         ];
//     },
// });


// console.log("jjj")


// Example method showing how to read the data in JS
//     checkPartnerAge() {
//         const partner = this.get_product();
//         console.log("ll")
//         if (partner) {
//             // The field is automatically present here because of Python's _load_pos_data_fields
//             console.log("Partner's Custom Age:", partner.spare_type);
//         }
//     }
// });

//      prepareBaseLineForTaxesComputationExtraValues(customValues = {}) {
//         const extraValues = super.prepareBaseLineForTaxesComputationExtraValues(customValues);
//         extraValues.l10n_in_hsn_code = this.product_id?.l10n_in_hsn_code;
//         return extraValues;
//     },
// });


// static/src/js/custom_pos_logic.js
// import { patch } from "@web/core/utils/patch";
// import { PosStore } from "@point_of_sale/app/store/pos_store";
//
// patch(PosStore.prototype, {
//     async setup() {
//         super.setup(...arguments);
//     },
//
//     // Example method showing how to read the data in JS
//     checkPartnerAge() {
//         const partner = this.get_partner();
//         if (partner) {
//             // The field is automatically present here because of Python's _load_pos_data_fields
//             console.log("Partner's Custom Age:", partner.custom_age);
//         }
//     }
// });


//     get totalQuantity() {
//         let totalQuantity = 0;
//         this.order.lines.forEach((line) => (totalQuantity += line.qty));
//         return totalQuantity;
//     },
// });
//
//
//

//
// /** @odoo -module **/
//
// import { Order } from "@point_of_sale/app/store/models";
// import { patch } from "@web/core/utils/patch";
//
// patch(Order.prototype, {
//     export_for_printing() {
//         const result = super.export_for_printing();
//         result.qr_code = this.qr_code;  // must match field in Python
//         return result;
//     },
// });


// import { patch } from "@web/core/utils/patch";
// import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
//
// patch(Orderline.prototype, {
//     // async processData(loadedData) {
//         async setup()
//         {
//             await super.setup(...arguments);
//             console.log("print")
//
//             // console.log("Loaded Partners with Custom Fields:", loadedData['product.template']);
//
//     },

// Example function to retrieve your custom field from the active partner
// getCustomLoyaltyCode() {
// const partner = this.get_partner();
// return partner ? partner.custom_loyalty_code : '';
// }
// });

// import { patch } from "@web/core/utils/patch";
// import { PosStore } from "@point_of_sale/app/services/pos_store";
//
// patch(PosStore.prototype, {
//     async setup() {
//         await super.setup(...arguments);
//         this.data.connectWebSocket("ADYEN_LATEST_RESPONSE", () => {
//             const pendingLine = this.getPendingPaymentLine("adyen");
//
//             if (pendingLine) {
//                 pendingLine.payment_method_id.payment_terminal.handleAdyenStatusResponse();
//             }
//         });
//     },
// });
//


//
// /** @odoo -module **/
//
// import { Order } from "@point_of_sale/app/store/models";
// import { patch } from "@web/core/utils/patch";
//
// patch(Order.prototype, {
//     export_for_printing() {
//         const result = super.export_for_printing();
//         result.qr_code = this.qr_code;  // must match field in Python
//         return result;
//     },
// });