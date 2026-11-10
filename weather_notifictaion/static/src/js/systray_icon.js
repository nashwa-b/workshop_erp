/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {useService} from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { useDropdownState } from "@web/core/dropdown/dropdown_hooks";
// import { DropdownGroup } from "@web/core/dropdown/dropdown_group";


export class WeatherIcon extends Component {

    static components = { Dropdown };
    static props = [];
    static template = "weather_condition";

    setup() {
        // super.setup();


        // const API_KEY = '2dff67ab3d78ed4c01d9caeee0035306'; // Get from OpenWeatherMap
        // const API_URL = 'https://api.openweathermap.org/data/2.5/weather';


        // this.dialogService = useService("dialog");
        // this.dropdown = useDropdownState();
    }

    // console.log(template)

    onClick() {

              const API_KEY = '77f5a37d961dc97040707887e68cc203'; // Get from OpenWeatherMap
              const API_URL = 'https://api.openweathermap.org/data/4.0/onecall/timeline/1day?cnt=10&lat=51.5000&lon=-0.1000&start=1778324400&appid={API_KEY}';
    //           console.log(API_KEY)
    //        try {
    //
    //            const response = fetch(`${API_URL}`);
    //             console.log(response)
    //             const data =response.json();
    //             console.log(data)
    //       }
    //       catch (error) {
    //     console.log('Error fetching weather by coordinates:', error);
    // }

    (async () => {
    // You MUST store this key securely. Place it in an
    // environment variable or in in a file outside of
    // git (e.g. your home directory).
    const apiKey = "77f5a37d961dc97040707887e68cc203";
    const url = "https://api.openweathermap.org/data/4.0"

    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + apiKey,
            // "X-Odoo-Database": "...",
        },
        // body: JSON.stringify(${objStr}),
    };
     // const responses = requests.post(f"{self.url}/json/2/purchase.order.line/search_read",
    const response = await fetch("${https://api.openweathermap.org/data/4.0/onecall/current?lat=52.2297&lon=21.0122&units=metric&lang=en&appid={77f5a37d961dc97040707887e68cc203}}", request);
    console.log("l",response)
    if (response.ok) {
        const data = await response.json();
        console.log(data)
    } else {
        // Handle errors
    }
})();

        // const response = await fetch(`${API_URL}`);
        // const data = await response.json();
    //     this.dialogService.add(Dialog, {
    //         title: "My Systray Dialog",
    //     });
    }

}


// WeatherIcon.template = "weather_notification.WeatherIcon";
// console.log(WeatherIcon.template)


// export const systrayItem = {
//     Component: WeatherIcon,
// };

// TemplateSet.registerTemplate("__portal__", portalTemplate);

export const systrayItem = {
    Component: WeatherIcon,
};
registry.category("systray").add(
    "WeatherIcon",
    systrayItem,
    {sequence: 10}
);

// async function getWeatherByCoords() {
//     try {
//         const API_KEY = '2dff67ab3d78ed4c01d9caeee0035306'; // Get from OpenWeatherMap
//         const API_URL = 'https://api.openweathermap.org/data/2.5/weather';
//
//         const response = await fetch(`${API_URL}`);
//         const data = await response.json();
//         console.log(data)
//         // displayWeather(data);
//     } catch (error) {
//         console.log('Error fetching weather by coordinates:', error);
//     }
// }