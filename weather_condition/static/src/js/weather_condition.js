/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component, useState, onWillStart} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";


export class WeatherCondition extends Component {

    static template = "weather_condition.WeatherCondition";
    static components = {Dropdown, DropdownItem};
    static props = [];


    setup() {
        super.setup();
        this.orm = useService("orm");
        this.location = "";
        this.weather = ""
        this.state = useState({
            formatted_date: "",
            date: "",
            location: "",
            latitude: "",
            longitude: "",
            weather_api_key: "",
            data: "",
            icon: "",
            location_data: "",
            status: ""


        });

        // getWeather(ev) {

        onWillStart(async () => {
            const settings = await this.orm.call("ir.config_parameter", 'get_weather_parameter', []);

            this.state.date = settings.date
            this.state.formatted_date = settings.formatted_date
            this.state.latitude = settings.latitude
            this.state.longitude = settings.longitude
            this.state.location = settings.location
            this.state.weather_api_key = settings.weather_api_key
            this.state.enable_weather = settings.enable_weather
            this.state.status = settings.status
            console.log(settings)
            console.log(settings.date)
            console.log('k', settings.location)

            if (this.state.status == 'fetch_location') {
                console.log('fte')
                this.state.location = false

            }

            if (this.state.status == 'manual_location') {
                console.log('kj')
                this.state.latitude = 0
                this.state.longitude = 0
            }

            console.log('status', this.state.status)

            if (this.state.longitude && this.state.latitude) {
                console.log("poiuh")
                const url = `https://api.openweathermap.org/data/2.5/weather?lat=${this.state.latitude}&lon=${this.state.longitude}&units=metric&appid=${this.state.weather_api_key}`
                const response = await fetch(url)
                // console.log('ll',respose)
                this.state.data = await response.json();
                console.log('llllll', this.state.data)
            }

            if (this.state.location) {
                console.log("locat")
                const url = `https://api.openweathermap.org/data/2.5/weather?q=${this.state.location}&units=metric&appid=${this.state.weather_api_key}`
                const response = await fetch(url)
                // console.log('ll',respose)

                this.state.data = await response.json();
                console.log('looooooo', this.state.data)
            }


            this.state.iconUrl = `http://openweathermap.org/img/w/${this.state.data.weather?.[0]?.icon}.png`

            this.weather = {
                'formatted_date': this.state.formatted_date,
                'date': this.state.date,
                'latitude': this.state.latitude,
                'longitude': this.state.longitude,
                'api_key': this.state.weather_api_key,
                'enable_weather': this.state.enable_weather,
                'location': this.state.location,
                'description': this.state.data.weather?.[0]?.description,
                'main': this.state.data.weather?.[0]?.main,
                'icon': this.state.iconUrl,
                'cod': this.state.data.cod,
                'temp': this.state.data.main?.temp,
            }

            console.log('wetheicon', this.weather.icon)
        });
    }

     }

     console.log(WeatherCondition.template)

export const systrayItem = {
Component: WeatherCondition,
};
registry.category("systray").add(
"WeatherCondition",
systrayItem,
{sequence: 10}
);









