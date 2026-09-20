/**
 * \file            app.js
 * \brief           Main entry 
 */

/*
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

import './App.css';

import React, { Component } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from './Layout';
import Home from './pages/Home';
import Transport from './pages/Transport';
import Parameter from './pages/Parameter';
import CityMap from './pages/CityMap';

import AppOption from "./components/AppOption";
import AppContext from "./components/AppContext";

class App extends Component {
  static contextType = AppContext;
  constructor(props) {
    super(props);
    this.state = (
      {
        backendready: false,
        params:AppOption
      }
    );

    this.componentDidMount = this.componentDidMount.bind(this);
    this.webviewloaded = this.webviewloaded.bind(this);
    this.handleResize = this.handleResize.bind(this);
  }

  
  

  handleResize ()
  {
    
  }
  
  async webviewloaded() {
    let backend = this.context.GetBackend ();

    // backend is ready
    backend.setbackendready (true);
    
    // define the backend service name
    backend.setService (process.env.REACT_APP_NAME);


    this.setState({ backendready: true });
    let option = await backend.get_parameters();
    console.log ("backend ready :");
    console.log (option);
    let params = JSON.parse(option);
    this.setState({params:params});

    console.log ("set data in context");
    this.context.setParams (params);
    this.context.SetAppLocale (params.lang);
    
    console.log ("webviewloaded end");
  }

  async componentDidMount() {
    if (process.env.REACT_APP_LOCALWEB === true || process.env.REACT_APP_LOCALWEB === "true")
        this.webviewloaded ();
    else if (process.env.REACT_APP_PYWEBVIEW === true || process.env.REACT_APP_PYWEBVIEW === "true")
      window.addEventListener('pywebviewready', this.webviewloaded);
    console.log ("componentDidMount");
  }

  render() {
    
    if ( !this.state.backendready) {
      return (<h1>Loading</h1>);
    }
    return (
      
        <BrowserRouter>
          <Routes>
            <Route path={process.env.PUBLIC_URL + "/"} element={<Layout />}>
              <Route index element={<Home  params={this.context.Params} />} />
              <Route path={process.env.PUBLIC_URL + "/parameter"} element={<Parameter params={this.context.Params} />} />
              <Route path={process.env.PUBLIC_URL +"/transport"}  element={<Transport  />}/>
              <Route path={process.env.PUBLIC_URL +"/cmap"}  element={<CityMap  params={this.context.Params} />} />
              
              <Route path="*" element={<Home />} />
            </Route>
          </Routes>
        </BrowserRouter>
      
    );
  }
}

export default App;
