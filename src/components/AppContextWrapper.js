import React, { useState } from 'react';
import AppContext from './AppContext';
import AppOption from './AppOption.js';
import LocaleString from './localestring.js';

let params = AppOption;
let pywebviewready = false;
let locale = "fr";
let localedata = new LocaleString();

const AppContextWrapper = (props) => {
    const [Params, setParams] = useState(params);
    const [PyWebViewReady, setPyWebViewReady] = useState(pywebviewready);
    const [Locale, setLocale] = useState(locale);
    const [ImagePreview, setImagePreview] = useState('');

    function getLocaleData ()
    {
        console.log ("localedata in context:" + localedata);

        return (localedata);
    }
    function setAppLocale (localecode)
    {
        console.log ("setAppLocale:" + localecode);
        localedata.setLocaleCode(localecode);
        setLocale(localedata.getLocaleCode());
    }
   
    function setOption(opt) {
        setParams(opt);
        if (window.pywebview)
            window.pywebview.api.gcode_set_parameters(opt);

    }
   
    function getLocaleString (id)
    {
        return localedata.getLocaleString(id);

    }
    function getLocaleDir()
    {
        return localedata.getLocaleDir();
    }
    
     
    
    return (
        <AppContext.Provider value={{
            SetOption: setOption,
            GetLocaleData: getLocaleData,
            SetAppLocale: setAppLocale,
            GetLocaleString: getLocaleString,
            GetLocaleDir: getLocaleDir,
            
            Params, setParams,
            PyWebViewReady, setPyWebViewReady,
            Locale, setLocale,
            ImagePreview, setImagePreview
        }} >
            {props.children}
        </AppContext.Provider>
    );
}

export default AppContextWrapper;
