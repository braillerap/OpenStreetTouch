import { useContext, useState, useRef, useEffect} from 'react'
import AppContext from "../components/AppContext";
import { MapContainer , TileLayer, Circle,  useMapEvents} from 'react-leaflet';
import "leaflet/dist/leaflet.css";

const redOptions = { color: 'red' }
const greenOptions = { color: 'green' }

const CityMap = () => {
    const {GetLocaleString} = useContext(AppContext);
    const { ImagePreview, setImagePreview } = useContext(AppContext);
    const { TransportGuide, setTransportGuide } = useContext(AppContext);
    const mapref = useRef (null);
    const [position, setPosition] = useState([51.505, -0.09]);
    const [radius, setRadius] = useState(200);
    const [building, setBuilding] = useState (true);
    const [footpath, setFootpath] = useState (false);
    const [polygon, setPolygon] = useState (false);
    const [request, setRequest] = useState (false);
    const [editLatitude, setEditLatitude] = useState (51);
    const [editLongitude, setEditLongitude] = useState (0);
    const [mapClicked, setMapClicked] = useState (false);
    const [pngavailable, setPngAvailable] = useState(false);
    const [includeWater, setIncludeWater] = useState(false);
    const [cliping, setCliping] = useState(false);

    useEffect(() => {
            window.pywebview.api.get_cairosvg_available().then ((enable) => {
                setPngAvailable(enable);
            });

            setImagePreview ('');
            setTransportGuide('');
          }, []);
    
    
    const setLatitude = (elat) => {
        setEditLatitude(elat);

        let lat = parseFloat(elat);
        if (lat)
        {
            if (lat > -90 && lat < 90)
            {
                if (position)
                {
                    if (position.lng)
                    {
                        setPosition([lat, editLongitude]);
                        mapref.setView([lat, editLongitude], mapref.getZoom())
                    }
                    else
                    {
                        setPosition([lat, editLongitude]);
                        mapref.setView([lat,editLongitude], mapref.getZoom())
                    }
                        
                }
                else
                {
                    setPosition([lat, editLongitude]);
                    mapref.setView([lat, editLongitude], mapref.getZoom())
                }
            }
        }
        
    }

    const setLongitude = (elon) => {
        setEditLongitude(elon);
        let lon = parseFloat(elon);
        if (lon)
        {
            if (lon > -180 && lon < 180)
            {
                if (position)
                {
                    if (position.lat){
                        console.log ("position.lat exist");
                        setPosition([editLatitude, lon]);
                        mapref.setView([position.lat, lon], mapref.getZoom())
                    }
                    else
                    {
                        console.log ("position.lat not exist");
                        console.log (position);
                        setPosition([editLatitude, lon]);
                        mapref.setView([editLatitude, lon], mapref.getZoom());
                    }
                }
                else
                {
                    console.log ("position  not exist");
                    setPosition([editLatitude, lon]);
                    mapref.setView([editLatitude, lon], mapref.getZoom())

                }
            }
        }
    }
    
    const LocationFinder= () => {
        
        const map = useMapEvents({
            click(e) {
                console.log(e.latlng);
                // save position value
                setPosition(e.latlng);
                
                // center map on click position
                map.setView(e.latlng, map.getZoom())
                setMapClicked (true);
                // report value in edit
                console.log ("typeof (e.latlng")
                console.log (typeof (e.latlng));
                
                setEditLatitude(e.latlng.lat);
                setEditLongitude(e.latlng.lng);
            },
        });
        return null;
    };

        const renderPosition = () => {
            
            if (position)
                return (
                    <h2>{position.lat} {position.lng}</h2>
                );    
            
            
        }
        /*
        const MapPosition = () => {
            if (position)
                return [position.lat, position.lng];
            console.log("MapPosition default");
            return [51.505, -0.09];
        }
            */
        const goRender = () =>
        {
            if (position)
            {
                console.log (position);
                console.log (editLatitude);
                console.log (editLongitude);
                setRequest(true);
                let lat = editLatitude;
                let lon = editLongitude;
                if (position.lat && position.lng)
                {
                    lat = position.lat;
                    lon = position.lng;
                }
                window.pywebview.api.ReadStreetMapData(lat, lon, radius, building, footpath, polygon, includeWater, cliping).then ((svg) => {
                   
                    setImagePreview (svg);
                    setRequest(false);
                    
                });
            }
    
        }
        const renderMapRadius = () => {
            if (position)
            {
                return (
                <Circle center={position} pathOptions={redOptions} radius={radius}>
        
                </Circle>
                );
            }
            else
            {
                return (<></>)
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
        const renderPNGcommand = () => {
            if (pngavailable)
                return (<button onClick={goDownloadPNG}>{GetLocaleString("transport.downloadpng")}</button>);
            return (<></>);
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
        const renderResultAction = () => {
            if (ImagePreview == '')
                return (<></>);
            return (
                <div className='TransportResultAction'>
                    <fieldset>
                        <legend>{GetLocaleString("transport.titleresult")}</legend>
                        <button onClick={goDownloadSVG}>{GetLocaleString("transport.downloadsvg")}</button>
                        {renderPNGcommand()}
                        
                    </fieldset>
                </div>
            );
        }
        const renderAction = () => {
            if (position  )
            {
                return (
                    <fieldset >
    
                    <legend>{GetLocaleString("citymap.sectionplan")}</legend>
                        <div className='TransportAction'>
                            <label>
                                <input type='checkbox' checked={building}
                                onChange={(e) => setBuilding(e.target.checked)} />
                                {GetLocaleString("citymap.building")}
                            </label>
                            <label>
                                <input type='checkbox' checked={footpath} 
                                onChange={(e) => setFootpath(e.target.checked)} />
                                {GetLocaleString("citymap.footpathonly")}
                            </label>
                            <label>
                                <input type='checkbox' checked={polygon} 
                                onChange={(e) => setPolygon(e.target.checked)} />
                                {GetLocaleString("citymap.streetpolygon")}
                                </label>
                                
                                
                            <label>
                                <input type='checkbox' checked={includeWater} 
                                onChange={(e) => setIncludeWater(e.target.checked)} />
                                {GetLocaleString("citymap.water")}
                                </label>
                            <label>
                                <input type='checkbox' checked={cliping} 
                                onChange={(e) => setCliping(e.target.checked)} />
                                {GetLocaleString("citymap.cliping")}
                                </label>
                            <button disabled={request} onClick={goRender}>
                                {GetLocaleString("citymap.rendermap")}
                            </button>
                        </div>
                    </fieldset>
                    );
            }    
        }
    return (
        <>
            <div className='CityMapParam'>
            <h1>{GetLocaleString("citymap.maptitle")}   </h1>
                {renderPosition()}
                <label>{GetLocaleString("citymap.latitude")}
                <input type="number" value={editLatitude} step="0.0001" min="-90" max="90" 
                onChange={(e) => setLatitude(e.target.value)} />
                </label>
                <label>{GetLocaleString("citymap.longitude")}
                <input type="number" value={editLongitude} step="0.0001" min="-180" max="180"
                onChange={(e) => setLongitude(e.target.value)} />
                </label>
                <label>{GetLocaleString("citymap.radius")}
                <input type="number" value={radius} onChange={(e) => setRadius(e.target.value)} min={40} max={1500}/>
                </label>
                
                <h2>Click on the map to get the position</h2>
            </div>
            <MapContainer center={position} zoom={2} scrollWheelZoom={true}
                ref={mapref}
                style={{ width: '99%', position: 'relative', zIndex: '9', height: '40vh' }}
                attributionControl={false}

                >

                <TileLayer
                    attribution='&copy; "https://www.openstreetmap.org/copyright" OpenStreetMap contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                 <LocationFinder />
                 {renderMapRadius()}
                 
            </MapContainer>
            {renderAction()}
            {renderResultAction ()}
        </>
    );
}

export default CityMap;