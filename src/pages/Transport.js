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
            <select value={iso639code} onChange={(event) => {setIso639Code(event.target.value)}} >
            {
                iso639codeList.map((code) => {
                    return (
                    <option value={code}>{code}</option>
                    );
                })
            }
            </select>
        );
    }
    const renderTransportType =  () => {
        return (
            <label>
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
        console.log ("call GetTransportDataSvg" + transportLines);
        window.pywebview.api.GetTransportDataSvg(transportLines, drawStation, transportStrategy).then ((svg) => {
            setImagePreview (svg);
        });
    }

    const goOsm = () => {
        
        setImagePreview('');
        setTransportLines([]);
        console.log ("tansport type", transportType);
        window.pywebview.api.ReadTransportData(cityName, transportType, iso639code).then ((size) => {
            console.log (size);
            window.pywebview.api.GetTransportLines().then ((datadic) => {
                setRealCityName (datadic.city);

                console.log (datadic.lines);
                
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
                console.log (sline) ;
                setTransportLines(sline);
                
                /*
                window.pywebview.api.GetTransportDataSvg(sline).then ((svg) => {
                    setImagePreview (svg);
                });
                */
            });

            
        });

       

       
    }
    const onSelectLine = (e) => {
        console.log(e.target.id);
        console.log(e.target.name);
        console.log(e.target.checked);

        let lines = transportLines;
        lines[e.target.id].select = e.target.checked;
        setTransportLines(lines);
    }

    const onSelectStations = (e) => {
        console.log(e.target.checked);
        setDrawStation(e.target.checked);
    }
    const onSelectFill = (e) => {
        console.log(e.target.value);
    }
    
    const renderTransportLines = () => {
        if (transportLines.length === 0  )
            return (<>empty</>);
        
        return (
            
               
                transportLines.map((line) => {
                        return (
                            <label>
                                <input type="checkbox" 
                                    id={line.id} 
                                    name={line.name} 
                                    onChange={onSelectLine}/>
                                {line.name} 
                            </label>
                        )
                    })
                
            
            
        );
    }
    const renderImage = () => {
        if (cityImage !== '') {
            const srcpat = "data:image/png;base64," + cityImage;
            return <img src={srcpat} alt="city image" />
        }
        return (<></>);
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
                    <label>Stratégie
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
                    <label>
                        <input type='checkbox' id='fill' name='fill' onChange={onSelectFill} />
                        {GetLocaleString("transport.renderfill")}
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
        <button onClick={goOsm}>Go !</button>
        {/*renderImage() */}

        <div className='CheckedList'>
            <p>OSM city name : {realCityName}</p>
            {renderTransportLines ()}
            
        </div>

        {renderTransportAction ()}
    </div>
  );
}

export default Transport;