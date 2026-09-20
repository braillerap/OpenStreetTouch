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
        <div className="flex flex-col items-center min-h-full">
          
          <a href="https://myhumankit.org/" target="_blank" rel="noreferrer">
            <img className='mx-auto w-1/2 my-2' src="./MHK.png"  alt="MyHumanKit logo"  />
          </a>
          
          <h1>OpenStreetTouch</h1>
          <h2>Version:{`${process.env.REACT_APP_VERSION}`}</h2>

          
          <a href="https://www.nlnet.nl" target="_blank" rel="noreferrer">
            <img className='mx-auto w-1/3 my-2' src="./logo-sh.svg" alt="NLnet foundation logo"  />
          </a>
          
          <a href="https://www.braillerap.org" target="_blank" rel="noreferrer">
            <img className='mx-auto w-full my-2' src="./braillerap_logo.svg"  alt="BrailleRAP logo"  />
          </a>
          

          <p className='mx-auto my-2  text-center'>{this.context.GetLocaleString("home.openstreetmap")} 
            <a href="https://www.openstreetmap.org/copyright" className='underline mx-2' target="_blank" rel="noreferrer">OpenStreetMap</a>
          </p>
        </div>
      </>

    );
  }
};

export default Home;