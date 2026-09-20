import React from 'react';

import AppContext from "../components/AppContext";


class Parameters extends React.Component {
  static contextType = AppContext;

  constructor(props) {
    super(props);
    this.state = {
      localedata: [],
      themedata: []
    }

    this.handleChangeGeneral = this.handleChangeGeneral.bind(this);
    this.handleChangeNumeric = this.handleChangeNumeric.bind(this);
    this.handleChangeLanguage = this.handleChangeLanguage.bind(this);
    this.handleChangeTheme = this.handleChangeTheme.bind(this);
    this.setFocusPolicy = this.setFocusPolicy.bind(this);

    
  }

  async componentDidMount() {

    console.log("componentdidmount parameter");


    let localedata = this.context.GetLocaleData().getLocaleList();
    //console.log ("localedata=" + localedata + " " + this.context.Locale);
    this.setState({ localedata: localedata });

    let data = [
      {theme:"normal",  desc: this.context.GetLocaleString("param.theme-normal") },
      {theme:"thdark",  desc:this.context.GetLocaleString("param.theme-wb") },
      {theme:"thlight", desc:this.context.GetLocaleString("param.theme-bw")}
    ];

    this.setState ({themedata: data})

  }

  /*!
     *\brief Theme select calback. Apply theme and save parameters
     *
     */
  async handleChangeTheme(evt) {
    let param = {
      ...this.context.Params,
      theme: evt.target.value
    };
    this.context.SetOption(param);

    // display the new theme immediately
    this.context.setAppTheme(evt.target.value);
  }

  /*!
     *\brief Locale select calback. Apply locale and save parameters
     *
     */
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

  setFocusPolicy(value) {
    let option = {
      ...this.context.Params,
    }
    option.focuspolicy = value;
    this.context.SetOption(option);
  }

  render() {


    return (
      <main >

        <h1>{this.context.GetLocaleString("param.formtitle")}</h1>






        <div className='flex flex-col'>

          <fieldset className='flex flex-col my-2'>
            <legend>{this.context.GetLocaleString("param.general.section")}</legend>
            <p>
              {this.context.GetLocaleString("param.locale")}&nbsp;
              <b>{this.context.Params.lang}</b>
            </p>

            <label htmlFor='langid' aria-label="param.language_aria" >
              {this.context.GetLocaleString("param.locale")}
              <select id="langid"
                value={this.context.Locale}
                onChange={this.handleChangeLanguage}
                className='select'
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
              

                <label htmlFor='themeid' aria-label={this.context.GetLocaleString("param.theme_aria")} >
                  {this.context.GetLocaleString("param.themeselect")}
                  
                  <select id="themeid"
                    value={this.context.AppTheme}
                    onChange={this.handleChangeTheme}
                    className='select'
                  >
                    {this.state.themedata.map((item, index) => {
                      if (this.context.Theme === item.theme)
                        return (<option aria-selected={true} key={item.theme} value={item.theme}>{item.desc}</option>);
                      else
                        return (<option aria-selected={false} key={item.theme} value={item.theme}>{item.desc}</option>);
                      })
                    }

                    
                  </select>
                </label>

              </fieldset>

              <fieldset className='flex flex-col'>
                <legend>{this.context.GetLocaleString("param.accesibility.section")}</legend>
                <div className='flex flex-row gap-2'>
                  <input type='checkbox' checked={this.context.Params.focuspolicy} 
                    onChange={(e) => this.setFocusPolicy(e.target.checked)} />
                <label>
                  {this.context.GetLocaleString("param.focuspolicy")}
                </label>
                </div>
                <div className='flex flex-row gap-2'>
                  <input type='checkbox' checked={this.context.Params.accesskey}
                    onChange={(e) => this.handleChangeGeneral("accesskey", e.target.checked)} />
                <label>
                  {this.context.GetLocaleString("param.accesskeypolicy")}
                </label>
                </div>
              </fieldset>

            </div>


          </main >
          );
  }
};

          export default Parameters;