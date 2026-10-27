/** @odoo-module **/
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {

    setDiscount(discount) {
        const m_discount = this.product_id.pos_categ_ids[0].max_discount;
        console.log("p", m_discount)

        if (this.config.category_wise_discount && discount > m_discount){
            window.alert("The maximum allowed discount for", this.product_id.name ,"is", m_discount)
            this.discount = 0;
        }

        else {
            this.discount = discount;
        }
                return super.setDiscount(...arguments);

    },
});

