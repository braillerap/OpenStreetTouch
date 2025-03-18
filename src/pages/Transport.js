import { useContext, useState, useEffect} from 'react'
import AppContext from "../components/AppContext";


const Transport = () => {
    const {GetLocaleString, Params, SetOption} = useContext(AppContext);
    const { ImagePreview, setImagePreview } = useContext(AppContext);
    const { TransportGuide, setTransportGuide } = useContext(AppContext);
    const [cityName, setCityName] = useState('');
    const [drawStation, setDrawStation] = useState(true);
    const [transportLines, setTransportLines] = useState([]);
    const [iso639codeList, setIso639CodeList] = useState([]);
    
    const [realCityName, setRealCityName] = useState('');
    const [transportType, setTransportType] = useState('subway');
    const [transportStrategyList, setTransportStrategyList] = useState([]);
    const [transportStrategy, setTransportStrategy] = useState(0);
    const [drawPolygon, setDrawPolygon] = useState(false);
    const [placeid, setPlaceid] = useState(0);
    const [pngavailable, setPngAvailable] = useState(false);
    const [osmPending, setOsmPending] = useState(false);

    useEffect(() => {
        window.pywebview.api.GetISO639_country_code().then ((isolist) => {
           setIso639CodeList(isolist);
        });
        window.pywebview.api.get_cairosvg_available().then ((enable) => {
            
            setPngAvailable(enable);
         });

        
        let list = [
            GetLocaleString("transport.strategyways"),
            GetLocaleString("transport.strategywayscorreted"),
            GetLocaleString("transport.strategystation")
        ];
        setTransportStrategyList(list);
        setImagePreview ('');
        setTransportGuide('');
      }, []);
      
    const place_id = [
        GetLocaleString("transport.city"),
        GetLocaleString("transport.wikidata")
    ];
    const transport_type_dic = {
        "subway":GetLocaleString("transport.type.subway"),
        "funicular":GetLocaleString("transport.type.funicular"),
        "bus":GetLocaleString("transport.type.bus"),
        "tram":GetLocaleString("transport.type.tram"),
        "train":GetLocaleString("transport.type.train"),
        "light_rail":GetLocaleString("transport.type.light_rail"),
        "monorail":GetLocaleString("transport.type.monorail"),
        "ferry":GetLocaleString("transport.type.ferry"),
    
    }
    const setOsmIso639Code = (code) => {
        
        let option = {
            ...Params
            
          };
        option["osmiso639"] = code;
        SetOption(option);
        console.log ("context set option");
    }
    const renderIso639 = () => {
        
        return (
            <label>{GetLocaleString("transport.iso639")}:
            <select value={Params["osmiso639"]} onChange={(event) => {setOsmIso639Code(event.target.value)}} >
            {
                iso639codeList.map((code) => {
                    return (
                    <option value={code}>{code}</option>
                    );
                })
            }
            </select>
            </label>
        );
    }
    const renderTransportType =  () => {
        return (
            <label>{GetLocaleString("transport.type")}:
            <select value={transportType} onChange={(event) => {setTransportType(event.target.value)}} >
            {
                
                Object.entries(transport_type_dic).map ((key) => {
                    
                    return (
                            <option value={key[0]}>{key[1]}</option>
                        );
                    }
                )   
            }
            </select>
            </label>
        )
    }
    const goRender = () => {
        console.log ("call GetTransportData" + transportLines);
        let jslines = '';
        try
        {
            jslines = JSON.stringify(transportLines);
            console.log ("json encoded");
        }
        catch (e)
        {
            console.log (e);
            console.log ("jslines error")
            //console.log (transportLines);
        }
        window.pywebview.api.GetTransportData(jslines, drawStation, transportStrategy, drawPolygon).then ((datastr) => {
            console.log (datastr);
            let data = JSON.parse(datastr);
            console.log (data);
            setImagePreview (data.svg);
            console.log (data.stations);
            setTransportGuide (data.stations);
        });
    }

    const goOsm = () => {
        
        setImagePreview('');
        setTransportGuide ('');
        setTransportLines([]);
        setOsmPending(true);
        console.log (transportType);
        // read OSM data for city and transport type
        // iso639code is used to specified the language name of the city for OSM
        window.pywebview.api.ReadTransportData(cityName, transportType, Params["osmiso639"], placeid).then ((size) => {
            
            window.pywebview.api.GetTransportLines().then ((jsondata) => {
                let datadic = JSON.parse(jsondata);
                setRealCityName (datadic.city);

                // update result for suitable checkbox display
                let sline = [];
                if ("lines" in datadic)
                {
                    for (let line in datadic.lines) 
                    {
                        console.log ("line " +line);
                        {
                            sline.push ({id:line, name:datadic.lines[line], select:false});
                        }
                    }
                }  
                setTransportLines(sline);
                setOsmPending(false);
            });
        });
    }
    const onSelectLine = (e) => {
        
        let lines = transportLines;
        lines[e.target.id].select = e.target.checked;
        setTransportLines(lines);
    }

    const onSelectStations = (e) => {
        console.log(e.target.checked);
        setDrawStation(e.target.checked);
    }
        
    const renderTransportLines = () => {
        if (osmPending)
            return (<>{GetLocaleString("transport.osmpending")}</>);

        if (transportLines.length === 0  )
            return (<>{GetLocaleString("transport.nodata")}</>);
        
        return (
                <>
                <p>{GetLocaleString("transport.osmcityname")} : {realCityName}</p>
                {transportLines.map((line) => {
                        return (
                            <label>
                                <input type="checkbox" 
                                    id={line.id} 
                                    name={line.name} 
                                    onChange={onSelectLine}/>
                                {line.name} 
                            </label>
                        )
                    })}
                </>
            
            
        );
    }
    

    const renderTransportAction = () => {
        if (transportLines.length > 0  )
        {
            return (
                <fieldset >

                <legend>{GetLocaleString("transport.sectionplan")}</legend>
                    <div className='TransportAction'>
                    <label>
                        <input 
                            type='checkbox' 
                            id='stations' 
                            name='stations' 
                            checked={drawStation} 
                            onChange={onSelectStations} />
                        {GetLocaleString("transport.renderstation")}

                    </label>
                    <label>
                        <input 
                            type='checkbox' 
                            id='polygons' 
                            name='polygons' 
                            checked={drawPolygon} 
                            onChange={(e)=>{setDrawPolygon(e.target.checked)}} />
                        {GetLocaleString("transport.polygon")}

                    </label>
                    <label>{GetLocaleString("transport.renderstrategy")}
                    <select value={transportStrategy} onChange={(event) => {setTransportStrategy(event.target.value)}} >
                    {
                        transportStrategyList.map((trans, index) => {
                                return (
                                    <option value={index}>{trans}</option>
                            )
                        })
                    }
                    </select>
                    </label>
                    
                    <button onClick={goRender}>
                        {GetLocaleString("transport.renderimg")}
                    </button>
                    </div>
                </fieldset>
                );
        }    
    }
    const goDownloadPNG = () => {
        if (pngavailable)
        {
            let dialogtitle = GetLocaleString("file.saveas"); //"Enregistrer sous...";
            let filter = [
                GetLocaleString("file.pngfile"), //"Fichier svg",
                GetLocaleString("file.all") //"Tous"
            ]

            window.pywebview.api.saveas_svg_aspngfile(ImagePreview, dialogtitle, filter);
            
        }
    }
    const goDownloadSVG = () => {
        let dialogtitle = GetLocaleString("file.saveas"); //"Enregistrer sous...";
        let filter = [
            GetLocaleString("file.svgfile"), //"Fichier svg",
            GetLocaleString("file.all") //"Tous"
        ]

        window.pywebview.api.saveas_svgfile(ImagePreview, dialogtitle, filter);
    }
    const goDownloadTXT = () => {
        let dialogtitle = GetLocaleString("file.saveas"); //"Enregistrer sous...";
        let filter = [
            GetLocaleString("file.txtfile"), //"Fichier txt",
            GetLocaleString("file.all") //"Tous"
        ]

        window.pywebview.api.saveas_file(TransportGuide, dialogtitle, filter);
    }
    const renderPNGcommand = () => {
        if (pngavailable)
            return (<button disabled={osmPending} onClick={goDownloadPNG}>{GetLocaleString("transport.downloadpng")}</button>);
        return (<></>);
    }
    const renderResultAction = () => {
        if (ImagePreview == '')
            return (<></>);
        return (
            <div className='TransportResultAction'>
                <fieldset>
                    <legend>{GetLocaleString("transport.titleresult")}</legend>
                    <button disabled={osmPending} onClick={goDownloadSVG}>{GetLocaleString("transport.downloadsvg")}</button>
                    {renderPNGcommand()}
                    <button disabled={osmPending} onClick={goDownloadTXT}>{GetLocaleString("transport.downloadtxt")}</button>
                </fieldset>
            </div>
        );
    }
  return (
    <div>
        <div className='TransportParam'>
            <h1>{GetLocaleString("transport.title")}</h1>

            <label>{GetLocaleString("transport.place_id")} :
                    <select value={placeid} onChange={(event) => {setPlaceid(event.target.value)}} >
                    {
                        place_id.map((id, index) => {
                                return (
                                    <option value={index}>{id}</option>
                            )
                        })
                    }
                </select>
                <input type="text" 
                    aria-description={place_id[placeid]}
                    name="city" 
                    value={cityName} 
                    onChange={(e)=>{setCityName(e.target.value);}}
                    />
            </label>
        </div>    
        <div className='TransportParam'>
            {renderIso639()}
            {renderTransportType()}
            </div>
            <div className='TransportParam'>    
            <button onClick={goOsm} disabled={osmPending}>{GetLocaleString("transport.search")}</button>
                    </div>
        

        <div className='CheckedList'>
            
            {renderTransportLines ()}
            
        </div>

        {renderTransportAction ()}
        {renderResultAction ()}
    </div>
  );
}

export default Transport;