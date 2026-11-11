/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component, useState, onWillStart} from "@odoo/owl";
// import {Dialog} from "@web/core/dialog/dialog";
import {useService} from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

// import { useDropdownState } from "@web/core/dropdown/dropdown_hooks";
// import { DropdownGroup } from "@web/core/dropdown/dropdown_group";


export class WeatherCondition extends Component {

    static template = "weather_condition.WeatherCondition";
    static components = {Dropdown, DropdownItem};
    static props = [];


    setup() {
        super.setup();
        this.orm = useService("orm");
        this.weather = ""
        this.state = useState({
            formatted_date:"",
            date: "",
            location: "",
            weather_api_key: "",
            data:"",
            icon:""
        });

        // getWeather(ev) {

        onWillStart(async () => {
            const settings = await this.orm.call("ir.config_parameter", 'get_weather_parameter', []);

            this.state.date = settings.date
            this.state.formatted_date = settings.formatted_date
            this.state.location = settings.location
            this.state.weather_api_key = settings.weather_api_key
            console.log(settings)
            console.log(settings.date)
            console.log('k',settings.location)
        });
    }



    async getWeather() {
        // console.log('l',this.state.date)


        // console.log(this.state.weather_api_key)
        // console.log(this.state.location)
        // const loc = this.state.location
        // const wet = this.state.weather_api_key
        // console.log('loc',loc)
        // console.log('wet',wet)


        const url = `https://api.openweathermap.org/data/2.5/weather?q=${this.state.location}&units=metric&appid=${this.state.weather_api_key}`
        const response = await fetch(url)
        this.state.data = await response.json();
        const datas = this.state.data
        console.log("kjh",this.state.data)

        // const icons = await fetch("https://openweathermap.org/payload/api/media/file/10d@2x.png")
        // this.state.icon = await icons.json();
        // console.log("kjkjhgf",this.state.icon)
        this.state.icon = 'https://openweathermap.org/payload/api/media/file/{this.state.data.weather?.[0]?.icon}@2x.png'



         this.state.iconUrl =  `http://openweathermap.org/img/w/${this.state.data.weather?.[0]?.icon}.png`

         this.weather = {
            'formatted_date':this.state.formatted_date ,
             'date': this.state.date,
             'location': this.state.location,
             'api_key': this.state.weather_api_key,
            // 'date': this.state.date,
            // 'location':this.state.location,
            // 'api_key':this.state.weather_api_key,
             'description': this.state.data.weather?.[0]?.description,
             'main': this.state.data.weather?.[0]?.main,
             'icon': this.state.iconUrl,

             'temp': this.state.data.main?.temp,
        }

        console.log('wetheicon',this.weather.icon)
        console.log(url)
        console.log('ll',this.state.data)
        console.log('ll',this.state.data)


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






