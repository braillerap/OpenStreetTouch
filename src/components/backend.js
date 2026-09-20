/**
 * \file            backend.js
 * \brief           Abstract access to local ressource like files or serial port
 */

/*
 * GNU GENERAL PUBLIC LICENSE
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without restriction,
 * including without limitation the rights to use, copy, modify, merge,
 * publish, distribute, sublicense, and/or sell copies of the Software,
 * and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS LICENSED UNDER
 *                  GNU GENERAL PUBLIC LICENSE
 *                   Version 3, 29 June 2007
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
 * AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 *
 * This file is part of OpenStreetTouch software.
 *
 * SPDX-FileCopyrightText: 2025-2026 Stephane GODIN <stephane@braillerap.org>
 * 
 * SPDX-License-Identifier: GPL-3.0 
 */

const status = {
            message:"",
            status: 0
        };
class BackendWebLocal {
    constructor() {
        this.backendready = false;
        this.service = "";

    }
    isbackendready() {
        return this.backendready;
    }

    setbackendready(status) {
        this.backendready = status;
    }
    setService (service)
    {
        this.service = service;
    }
    getService ()
    {
        return (this.service);
    }
    async get_parameters() {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", "/openstreet/local/get_parameters", false); // false for synchronous request
        xmlHttp.send(null);
        console.log("parameters", xmlHttp.responseText);
        return xmlHttp.responseText;

        
    }

    async set_parameters (appparam) {
        let param = {"service":this.service, "options":appparam};
        const request = new Request("/local/gcode_set_parameters", {
            method: "POST",
            body: JSON.stringify(param),
            headers: {
                "Content-Type": "application/json;charset=UTF-8",
                }
        });
        let response = await fetch (request);

        return
    }
    async get_runtime_options() {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", "/openstreet/local/get_runtime_options", false); // false for synchronous request
        xmlHttp.send(null);
        console.log("parameters", xmlHttp.responseText);
        return xmlHttp.responseText;

    }

    async gcode_get_serial() {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", "/local/gcode_get_serial", false); // false for synchronous request
        xmlHttp.send(null);
        console.log("gcode_get_serial", xmlHttp.responseText);
        return xmlHttp.responseText;
    }

    AsyncPrintGcode(gcode, comport) {

        let param = {"gcode":gcode, "port":comport};
        const request = new Request("/local/gcode_print", {
            method: "POST",
            body: JSON.stringify(param),
            headers: {
                "Content-Type": "application/json;charset=UTF-8",
                }
        });

        return fetch (request).then((response)=> (response.json()));

    }

    CancelPrint() {
        var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
        xmlhttp.open("POST", "/local/gcode_cancelprint", true);
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        return xmlhttp.send(JSON.stringify({ "cancel": true }));
    }

    async confirm_dialog(title, message) {
        let ret = window.confirm(message);
        console.log("return from backend confirm_dialog: ", ret)
        if (ret)
            return true;
        else
            return false;
    }


    async quit ()
    {
        console.log("request for exit");
        window.location.assign('/');
    }

    GetISO639_country_code () {
        const request = new Request("/local/ISO639_country_code", {
            method: "GET"}
            );
        return fetch(request).then((response)=> (response.json()));
    }
    get_cairosvg_available () {
       const request = new Request("/local/cairosvg", {
            method: "GET"}
            );
        return fetch(request).then((response)=> {
            let ret = response.json();
            console.log (ret);
            return ret;
        });
    }

    ReadTransportData(cityName, transportType, iso639_city_code, placeid)
    {

    }

    GetTransportLines ()
    {

    }
    GetTransportData (linelist, drawstation, linestrategy, polygon)
    {

    }
    GetTransportDataSvg (linelist, drawstation, linestrategy, polygon)
    {

    }
    async ReadStreetMapData(lat, lon, radius, building, footpath, polygon, includeWater, cliping)
    {
        let param = {'latitude':lat, 'longitude':lon, 'radius':radius, 
            'building':building, 'footpath':footpath, 'polygon':polygon,
            'includeWater': includeWater, 'clipping':cliping};
        let pjs = JSON.stringify(param);
        const request = new Request("/local/readstreetmapdata", {
            method: "POST",
            body: pjs,
            headers: {
                "Content-Type": "application/json;charset=UTF-8",
                }
            });
        return fetch(request).then((response)=> {
            let res = response.text();
            console.log (res);
            return res;
        });
    }
    
    
}
class BackendPyWebview {

    constructor() {
        this.backendready = false;
        this.service = "";

    }

    isbackendready() {
        return this.backendready;
    }

    setbackendready(status) {
        // clear pywebview shared storage
        window.pywebview.state = {};

        console.log ("set backendready ", status);
        this.backendready = status;
    }
    setService (service)
    {
        this.service = service;
    }
    getService ()
    {
        return (this.service);
    }

    async get_parameters() {
        return await window.pywebview.api.get_parameters();
    }
    async get_runtime_options() {
        return await window.pywebview.api.get_runtime_options();
    }

    async confirm_dialog(title, message) {
        let ret = await window.pywebview.api.confirm_dialog(title, message);
        console.log("return from pywebview confirm_dialog: ", ret)
        if (ret)
            return true;
        else
            return false;
    }

    async import_file(dialogtitle, filter, types) {
        let ret = await window.pywebview.api.import_file(dialogtitle, filter, types);

        return ret;
    }

    async save_file(data, dialogtitle, filter, types) {
        let ret = await window.pywebview.api.save_file(data, dialogtitle, filter, types);

        return ret;
    }

    async saveas_file(data, dialogtitle, filter, types) {
        let ret = await window.pywebview.api.saveas_file(data, dialogtitle, filter, types);

        return ret;
    }

    async load_file(dialogtitle, filter, types) {
        let ret = await window.pywebview.api.load_file(dialogtitle, filter, types);

        return ret;
    }

    async quit() {
        window.pywebview.api.quit();
    }

    async read_file(filename) {
        let ret = await window.pywebview.api.read_file(filename);
        return ret;
    }

    async download_file(gcode, dialogtitle, filter, types) {
        let ret = await window.pywebview.api.download_file(gcode, dialogtitle, filter, types);

        return ret;
    }
    async gcode_get_serial() {
        let ret = await window.pywebview.api.gcode_get_serial();

        return ret;
    }

    async set_parameters(options) {
        await window.pywebview.api.set_parameters(options);
    }

    AsyncPrintGcode(gcode, comport) {
        return window.pywebview.api.PrintGcode(gcode, comport);
    }
    CancelPrint() {
        window.pywebview.api.CancelPrint();
    }
    GetISO639_country_code () {
        return window.pywebview.api.GetISO639_country_code();
    }
    get_cairosvg_available () {
        return window.pywebview.api.get_cairosvg_available ();
    }

    ReadTransportData(cityName, transportType, iso639_city_code, placeid)
    {
        return window.pywebview.api.ReadTransportData(cityName, transportType, iso639_city_code, placeid);
    } 
    GetTransportLines ()
    {
        return window.pywebview.api.GetTransportLines ();
    }
    GetTransportData (linelist, drawstation, linestrategy, polygon)
    {
        return window.pywebview.api.GetTransportData (linelist, drawstation, linestrategy, polygon);
    }
    
    GetTransportDataSvg (linelist, drawstation, linestrategy, polygon)
    {
        return window.pywebview.api.GetTransportDataSvg (linelist, drawstation, linestrategy, polygon);
    }

    ReadStreetMapData(lat, lon, radius, building, footpath, polygon, includeWater, cliping)
    {
        return window.pywebview.api.ReadStreetMapData(lat, lon, radius, building, footpath, polygon, includeWater, cliping);
    }
};

class Backend {
    constructor() {
        this.backendready = false;
        
        if (process.env.REACT_APP_LOCALWEB === true || process.env.REACT_APP_LOCALWEB === "true")
            this.backend = new BackendWebLocal();
        else if (process.env.REACT_APP_PYWEBVIEW === true || process.env.REACT_APP_PYWEBVIEW === "true")
            this.backend = new BackendPyWebview();
        else
        {
            console.log ("Error: no backend configuration");
            throw new TypeError("Error: no backend configuration");

        }
    }

    isbackendready() {
        return this.backendready;
    }

    setbackendready(status) {
        console.log("set backend status");
        this.backendready = status;
    }
    setService (service)
    {
        this.backend.setService(service);
    }
    getService ()
    {
        return (this.backend.getService());
    }
    async confirm_dialog(title, message) {
        if (this.backendready) {
            let ret = await this.backend.confirm_dialog(title, message);
            console.log("return from backend confirm_dialog: ", ret)
            return ret;

        }
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }
    async import_file(dialogtitle, filter, types) {
        if (this.backendready) {
            let ret = await this.backend.import_file(dialogtitle, filter, types);

            return ret;
        }
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }

    async save_file(data, dialogtitle, filter, types) {
        if (this.backendready) {
            let ret = await this.backend.save_file(data, dialogtitle, filter, types);

            return ret;
        }
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }
    async saveas_file(data, dialogtitle, filter, types) {
        if (this.backendready) {
            let ret = await this.backend.saveas_file(data, dialogtitle, filter, types);

            return ret;
        }
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }

    async load_file(dialogtitle, filter, types) {
        if (this.backendready) {
            let ret = await this.backend.load_file(dialogtitle, filter, types);

            return ret;
        }
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }

    async read_file(filename) {
        if (this.backendready) {
            let ret = await this.backend.read_file(filename);

            return ret;
        }
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }
    async quit() {
        if (this.backendready)
            this.backend.quit();
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }

    async download_file(gcode, dialogtitle, filter, types) {
        if (this.backendready) {
            let ret = await this.backend.download_file(gcode, dialogtitle, filter, types);
            return ret;
        }
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }
    async gcode_get_serial() {
        if (this.backendready) {
            console.log("backend calling gcode_get_serial");
            let ret = await this.backend.gcode_get_serial();

            return ret;

        }
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
        return [];
    }

    async set_parameters(options) {
        console.log ("backend set parameters ", options);
        if (this.backend) {
            console.log ("calling instantiate backend to set parameters ", options)
            await this.backend.set_parameters(options);
        }
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }
    AsyncPrintGcode(gcode, comport) {
        
        if (this.backendready) {
            
            return this.backend.AsyncPrintGcode(gcode, comport);
        }
        // return a promise as the function should be async
        let pr = new Promise ((resolve, reject)=> {
            // build a status similar to AsyncPrintGcode return
            let ret = status;
            ret.message = "backend not ready";
            ret.status = 1;

            resolve ( ret);
        });
        
        return pr;
    }
    AsyncCancelPrint() {
        if (this.backendready) {
            this.backend.CancelPrint();
        }
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }

    async get_parameters() {
        if (this.backendready)
            return await this.backend.get_parameters();
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }
    async get_runtime_options() {
        if (this.backendready)
            return await this.backend.get_runtime_options();
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }

    GetISO639_country_code() {
        if (this.backendready)
            return this.backend.GetISO639_country_code();
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }

    get_cairosvg_available() {
        if (this.backendready)
        {
            return this.backend.get_cairosvg_available();
        }
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }
    ReadTransportData(cityName, transportType, iso639_city_code, placeid)
    {
        if (this.backendready)
            return this.backend.ReadTransportData(cityName, transportType, iso639_city_code, placeid);
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }
    GetTransportLines ()
    {
        if (this.backendready)
            return this.backend.GetTransportLines();
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }

    GetTransportData (linelist, drawstation, linestrategy, polygon)
    {
         if (this.backendready)
            return this.backend.GetTransportData (linelist, drawstation, linestrategy, polygon);
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }

    GetTransportDataSvg (linelist, drawstation, linestrategy, polygon)
    {
        if (this.backendready)
            return this.backend.GetTransportDataSvg (linelist, drawstation, linestrategy, polygon);
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }
    }

    ReadStreetMapData(lat, lon, radius, building, footpath, polygon, includeWater, cliping)
    {
     if (this.backendready)
            return this.backend.ReadStreetMapData(lat, lon, radius, building, footpath, polygon, includeWater, cliping);
        else
        {
            console.log ("ERROR: backend not ready");
            throw new TypeError("ERROR: backend not ready");
        }   
    }
}

export default Backend;
