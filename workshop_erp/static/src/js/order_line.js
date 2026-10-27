/** @odoo-module **/
import {patch} from "@web/core/utils/patch";
import {Orderline} from "@point_of_sale/app/components/orderline/orderline";
import {AlertDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {useService} from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";

patch(Orderline.prototype, {
    setup() {
        this.dialog = useService("dialog");
        this.pos = usePos();
    },

    async _onClickRemoveEachLine() {
        this.line.delete()
   },

    get lineScreenValues() {
        const line = this.line;
        const discount = line.discount
        const max_discount = line.product_id.pos_categ_ids[0].max_discount;
        if (this.pos.config.category_wise_discount && discount > max_discount) {
            this.dialog.add(AlertDialog, {
                title: _t("Invalid Discount"),
                body: _t("Discount exceeds maximum limit.")
            });
            line.discount = 0
        } else {
            line.discount = discount;
        }
        return super.lineScreenValues;
    }
});


