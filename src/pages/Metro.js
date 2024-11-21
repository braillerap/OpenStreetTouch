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

    const goOsm = () => {
        
        setImagePreview('');
        
        window.pywebview.api.ReadTransportData(cityName, "subway", iso639code).then ((size) => {
            console.log (size);
            window.pywebview.api.GetTransportLines().then ((datadic) => {
                setRealCityName (datadic.city);

                console.log (datadic.lines);
                console.log (datadic.lines.line_name);
                let sline = [];
                if ("line_name" in datadic.lines)
                {
                    for (let line in datadic.lines.line_name) 
                    {
                        {
                            sline.push ({id:line, name:datadic.lines.line_name[line], select:false});
                        }
                    }
                }   
                setTransportLines(sline);
                window.pywebview.api.GetTransportSVG().then ((svg) => {
                    setImagePreview (svg);
                });
            });

            
        });

       

        /*
        window.pywebview.api.getCityImage(cityName).then((imgdata) => {
            if (imgdata) {
                console.log(imgdata);
                //setCityImage(imgdata);
                setImagePreview(imgdata);
            }
            else
                console.log("imgdata == null");
        }
        )
        */
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
            return (<></>);
        
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
  return (
    <div>
        <h1>Extraction OSM</h1>

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
            <p>{realCityName}</p>
            {renderTransportLines ()}
        </div>

    </div>
  );
}

export default Metro;