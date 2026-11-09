/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";

class MySystrayIcon extends Component {
   setup() {
   this.dialogService = useService("dialog");
   }
   onClick() {
   this.dialogService.add(Dialog, {
       title: "My Systray Dialog",
       });
   }
}
MySystrayIcon.template = "systray_icon";
export const systrayItem = {
   Component: MySystrayIcon,
};
registry.category("systray").add(
   "MySystrayIcon",
   systrayItem,
   { sequence: 10 }
);