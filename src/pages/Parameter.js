import React from 'react';

import AppContext from "../components/AppContext";


class Parameters extends React.Component {
  static contextType = AppContext;

  constructor(props) {
    super(props);
    this.state = {
      localedata: [],
    }
    
    this.handleChangeGeneral = this.handleChangeGeneral.bind(this);
    this.handleChangeNumeric = this.handleChangeNumeric.bind(this);
    this.handleChangeLanguage = this.handleChangeLanguage.bind(this);
    this.setFocusPolicy = this.setFocusPolicy.bind(this);

  }

  async componentDidMount() {
    
    console.log ("componentdidmount parameter");
    
    
    let localedata = this.context.GetLocaleData().getLocaleList();
    //console.log ("localedata=" + localedata + " " + this.context.Locale);
    this.setState({ localedata: localedata });

    
    
  }
  
  handleChangeLanguage(event) {

    let option = {
      ...this.context.Params,
      lang: event.target.value
    };
    this.context.SetOption(option);
    this.context.SetAppLocale(event.target.value);
  }
  
  handleChangeNumeric(key, value) {
    let option = {
      ...this.context.Params
    };

    option[key] = parseFloat(value);
    this.context.SetOption(option);

  }
  handleChangeGeneral(key, value) {

    let option = {
      ...this.context.Params
    };
    option[key] = value;

    this.context.SetOption(option);
  }
  
  setFocusPolicy (value) {
      let option = {
        ...this.context.Params,
      }
      option.focuspolicy = value;
      this.context.SetOption(option);
  }

  render() {

    
    return (
      <div >

        <h2>{this.context.GetLocaleString("param.formtitle")}</h2>

        <div className="pure-form pure-form-aligned">
          

          
          
          <div className='ParamGroup'>
            <section aria-label={this.context.GetLocaleString("param.general.section")}>
            <fieldset className='ParamGroup'>
              <legend>Application</legend>
              <p>
              {this.context.GetLocaleString("param.locale")}&nbsp;
                <b>{this.context.Params.lang}</b>
              </p>
              <label htmlFor='langid' aria-label="param.language_aria" >
                {this.context.GetLocaleString("param.locale")}
             


              <select id="langid"
                value={this.context.Locale}
                onChange={this.handleChangeLanguage}
                className='select_param'
              >
                {this.state.localedata.map((item, index) => {
                  if (this.context.Locale === item.lang)
                    return (<option aria-selected={true} key={item.lang} value={item.lang}>{item.desc}</option>);
                  else
                    return (<option aria-selected={false} key={item.lang} value={item.lang}>{item.desc}</option>);
                })
                }

               

              </select>
              </label>
              <label>
                    <input type='checkbox' checked={this.context.Params.focuspolicy}
                    onChange={(e) => this.setFocusPolicy(e.target.checked)} />
                    {this.context.GetLocaleString("param.focuspolicy")}
              </label>
            </fieldset>
            </section>
          </div>
        </div >

      </div >
    );
  }
};

export default Parameters;