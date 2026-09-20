import React from 'react';
import AppContext from "../components/AppContext";

class Home extends React.Component {
  static contextType = AppContext;
  
  constructor(props) {
    super(props);
    this.state = {
      falsestateforwarning: false
    };
  }

  componentDidMount() {
    console.log ("home.js");
    if (this.props.params) {
      console.log("setting up params")
      this.context.setParams(this.props.params);
    }
    
  }

  render() {
    return (
      <>
        <div className="flex flex-col items-center">
          
          <a href="https://myhumankit.org/" target="_blank" rel="noreferrer">
            <img src="./MHK.png" width='25%' alt="MyHumanKit logo"  />
          </a>
          
          <h1>OpenStreetTouch</h1>
          <h2>Version:{`${process.env.REACT_APP_VERSION}`}</h2>

          
          <a href="https://www.nlnet.nl" target="_blank" rel="noreferrer">
            <img src="./logo-sh.svg" width='25%' alt="NLnet fundation logo"  />
          </a>
          
          <a href="https://www.braillerap.org" target="_blank" rel="noreferrer">
            <img src="./braillerap_logo.svg" width='25%' alt="BrailleRAP logo"  />
          </a>
          

          <p>{this.context.GetLocaleString("home.openstreetmap")} 
            <a href="https://www.openstreetmap.org/copyright" className='underline mx-2' target="_blank" rel="noreferrer">OpenStreetMap</a>
          </p>
        </div>
      </>

    );
  }
};

export default Home;