import React, { useState } from 'react';
import AppContext from './AppContext';
import AppOption from './AppOption.js';
import LocaleString from './localestring.js';
import Backend from './backend.js';

let params = AppOption;

let locale = "fr";
let localedata = new LocaleString();
let backend = new Backend();

const AppContextWrapper = (props) => {
    const [Params, setParams] = useState(params);
    const [Locale, setLocale] = useState(locale);
    const [ImagePreview, setImagePreview] = useState('');
    const [TransportGuide, setTransportGuide] = useState('');
    
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
        if (backend)
            backend.set_parameters(opt);

    }
   
    function getLocaleString (id)
    {
        return localedata.getLocaleString(id);

    }
    function getLocaleDir()
    {
        return localedata.getLocaleDir();
    }
    
    function getBackend() {
        return backend;
    }
    
    return (
        <AppContext.Provider value={{
            SetOption: setOption,
            GetLocaleData: getLocaleData,
            SetAppLocale: setAppLocale,
            GetLocaleString: getLocaleString,
            GetLocaleDir: getLocaleDir,
            GetBackend: getBackend,
            Params, setParams,
            Locale, setLocale,
            ImagePreview, setImagePreview,
            TransportGuide, setTransportGuide
        }} >
            {props.children}
        </AppContext.Provider>
    );
}

export default AppContextWrapper;
