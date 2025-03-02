import { useContext, useState, useEffect} from 'react'
import AppContext from "../components/AppContext";



const transport_type2 = [
    "subway",
    "funicular",
    "bus",
    "tram",
    "train",
    "light_rail",
    "monorail",
    "ferry"
];

const Transport = () => {
    const {GetLocaleString} = useContext(AppContext);
    const { setImagePreview } = useContext(AppContext);
    const { setTransportGuide } = useContext(AppContext);
    const [cityName, setCityName] = useState('');
    const [cityImage, setCityImage] = useState('');
    const [drawStation, setDrawStation] = useState(true);
    const [transportLines, setTransportLines] = useState([]);
    const [iso639codeList, setIso639CodeList] = useState([]);
    const [iso639code, setIso639Code] = useState();
    const [realCityName, setRealCityName] = useState('');
    const [transportType, setTransportType] = useState('subway');
    const [transportStrategyList, setTransportStrategyList] = useState([]);
    const [transportStrategy, setTransportStrategy] = useState(0);
    const [drawPolygon, setDrawPolygon] = useState(false);

    const [osmPending, setOsmPending] = useState(false);

    useEffect(() => {
        window.pywebview.api.GetISO639_country_code().then ((isolist) => {
           setIso639CodeList(isolist);
        });
        setIso639Code ('fr');
        let list = [
            GetLocaleString("transport.strategyways"),
            GetLocaleString("transport.strategywayscorreted"),
            GetLocaleString("transport.strategystation")
        ];
        setTransportStrategyList(list);
      }, []);
      
    

    const renderIso639 = () => {
        
        return (
            <label>{GetLocaleString("transport.iso639")}
            <select value={iso639code} onChange={(event) => {setIso639Code(event.target.value)}} >
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
            <label>{GetLocaleString("transport.type")}
            <select value={transportType} onChange={(event) => {setTransportType(event.target.value)}} >
            {
                transport_type2.map((trans) => {
                        return (
                            <option>{trans}</option>
                    )
                })
            }
            </select>
            </label>
        )
    }
    const goRender = () => {
        console.log ("call GetTransportData" + transportLines);
        window.pywebview.api.GetTransportData(transportLines, drawStation, transportStrategy, drawPolygon).then ((datastr) => {
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

        // read OSM data for city and transport type
        // iso639code is used to specified the language name of the city for OSM
        window.pywebview.api.ReadTransportData(cityName, transportType, iso639code).then ((size) => {
            
            window.pywebview.api.GetTransportLines().then ((datadic) => {
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
  return (
    <div>
        <h1>Extraction Transport</h1>

        <label>City name:
            <input type="text" 
                name="city" 
                value={cityName} 
                onChange={(e)=>{setCityName(e.target.value);}}
                />
        </label>

        {renderIso639()}
        {renderTransportType()}
        <button onClick={goOsm} disabled={osmPending}>{GetLocaleString("transport.search")}</button>
        {/*renderImage() */}

        <div className='CheckedList'>
            
            {renderTransportLines ()}
            
        </div>

        {renderTransportAction ()}
    </div>
  );
}

export default Transport;