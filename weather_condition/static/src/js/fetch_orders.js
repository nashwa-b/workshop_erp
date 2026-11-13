/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
import { useService } from "@web/core/utils/hooks";

export class LocationButtonWidget extends Component {
    static template = "weather_condition.LocationButtonWidget";
    static props = { ...standardWidgetProps };


    setup() {
        // this.notification = useService("notification");
        this.location = ""
    }

    async onClick() {
        // const recordId = this.props.record.resId;
        // this.notification.add(`Clicked widget on record ID: ${recordId}`, {
        //     type: "info",
        // });

         if (navigator.geolocation) {
             navigator.geolocation.getCurrentPosition(
                 (position) => {
                     const lat = position.coords.latitude;
                     const lng = position.coords.longitude;
                     this.location ={
                         latitude: lat,
                         longitude: lng,
                     }
                 },
                 //
                 // (error) => {
                 //     console.error("Error getting location: ", error.message);
                 // },
                  await this.props.record.update({
            latitude: this.location.latitude,
            longitude: this.location.longitude,
        })
             )
         }
    }
}

registry.category("view_widgets").add("fetch_button", {
    component: LocationButtonWidget,
});
