/** @odoo-module **/
import {PosOrderline} from "@point_of_sale/app/models/pos_order_line";
// import { PosCategory } from "@point_of_sale/static/tests/unit/data/product_category.data";
// import {PosCategory} from "@point_of_sale/app/models/pos_category";
import {patch} from "@web/core/utils/patch";
// import { usePos } from "@point_of_sale/app/hooks/pos_hook";
// import {parseFloat} from "@web/views/fields/parsers";
import {AlertDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {_t} from "@web/core/l10n/translation";
// import { PosCategory } from "./pos_category.data";
// import { models } from "@web/../tests/web_test_helpers";
// import { PosCategory } from "@point_of_sale/../pos_category.data";

patch(PosOrderline.prototype, {
    // setup() {
    //     super.setup(...arguments);
    //      console.log("POS store accessible here:", this.pos);
    //
    // },


//     /** @odoo-module **/
// import { PosOrderline } from "@point_of_sale/app/models/pos_order_line"; // Path varies slightly depending on Odoo version
// import { patch } from "@web/core/utils/patch";
//
// patch(PosOrderline.prototype, {
//     setup(vals) {
//         super.setup(...arguments); // Pass all arguments correctly
//
//         // this.pos is automatically available via the model parent initialization
//         console.log("POS store accessible here:", this.pos);
//     },
// });


    setDiscount(discount) {
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
        console.log(discount)
        console.log(this.product_id.name)
        // console.log(this.product_id.name)
        console.log(this.product_id.categ_id.name)
        console.log(this.product_id.categ_id.discount)
        console.log(this.config.category_wise_discount)
        // console.log(this.pos.config)


        // console.log(this.categ_id.discount)

        // var maxDiscount = this.product.maxDiscount;
        //
        // console.log(this.pos.config)
        // if (this.pos.config) {
        if (discount > 10) {
                this.dialog.add(AlertDialog, {
                title: _t("Configuration"),
                body: _t("An administrator needs to configure Google Synchronization before you can use it!"),
            });
            console.log("10")
            this.discount = 0;
            this.discountStr = "0";
        } else {
            this.discount = discount;
            this.DiscountStr = "" + discount;
            console.log("pp")
        }
    }
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