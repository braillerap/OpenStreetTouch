import { useContext, useState, useEffect} from 'react'
import AppContext from "../components/AppContext";



const Metro = () => {
    const { setImagePreview } = useContext(AppContext);
    const [cityName, setCityName] = useState('');
    const [cityImage, setCityImage] = useState('');
    const [transportLines, setTransportLines] = useState([]);
    const [iso639codeList, setIso639CodeList] = useState([]);
    const [iso639code, setIso639Code] = useState();
    const [realCityName, setRealCityName] = useState('');

    useEffect(() => {
        window.pywebview.api.GetISO639_country_code().then ((isolist) => {
            console.log (isolist);
            setIso639CodeList(isolist);
        });
        setIso639Code ('fr');
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

    const goRender = () => {
        console.log ("call GetTransportDataSvg" + transportLines);
        window.pywebview.api.GetTransportDataSvg(transportLines).then ((svg) => {
            setImagePreview (svg);
        });
    }

    const goOsm = () => {
        
        setImagePreview('');
        
        window.pywebview.api.ReadTransportData(cityName, "subway", iso639code).then ((size) => {
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
            return (<><button onClick={goRender}>Render Transport line(s)</button></>);
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
        <button onClick={goOsm}>Go !</button>
        {/*renderImage() */}

        <div className='CheckedList'>
            <p>OSM city name : {realCityName}</p>
            {renderTransportLines ()}
            {renderTransportAction ()}
        </div>

    </div>
  );
}

export default Metro;