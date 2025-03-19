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
        
        webviewready: false,
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
    //alert("webview loaded");
    //this.setState({ webviewready: true });
    //window.pywebview.state = {};
    this.setState({ webviewready: true });
    let option = await window.pywebview.api.gcode_get_parameters();
    console.log ("pywebview ready :");
    console.log (option);
    let params = JSON.parse(option);
    this.setState({params:params});

    console.log ("set data in context");
    this.context.setParams (params);
    this.context.SetAppLocale (params.lang);

    console.log ("Set pywebview state");
    this.context.setPyWebViewReady(true);
    
    
    console.log ("webviewloaded end");
  }

  async componentDidMount() {
    //this.LouisInit();
    console.log ("Registering event");
    window.addEventListener('pywebviewready', this.webviewloaded);
    //this.webviewloaded();
    //window.addEventListener('resize', this.handleResize)
    console.log ("componentDidMount");
  }

  render() {
    
    if ( !this.state.webviewready) {
      return (<h1>Loading</h1>);
    }
    return (
      
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<Home  params={this.context.Params} />} />
              <Route path="/parameter" element={<Parameter params={this.context.Params} />} />
              <Route path="/transport"  element={<Transport  />}/>
              <Route path="/cmap"  element={<CityMap  params={this.context.Params} />} />
              
              <Route path="*" element={<Home />} />
            </Route>
          </Routes>
        </BrowserRouter>
      
    );
  }
}

export default App;
