/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";

patch(PosOrderline.prototype, {
    getProduct() {
        return {
            ...super.getProduct(),
            spare_type: this.spare_type,
        };
    },
});

// How To Patch an Existing OWL Component in Odoo 19


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