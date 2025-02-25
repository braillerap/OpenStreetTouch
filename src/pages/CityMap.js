import { useContext, useState, useEffect} from 'react'
import AppContext from "../components/AppContext";
import { MapContainer , TileLayer, Circle,  useMapEvents} from 'react-leaflet';
import "leaflet/dist/leaflet.css";

const redOptions = { color: 'red' }
const greenOptions = { color: 'green' }

const CityMap = () => {
    const {GetLocaleString} = useContext(AppContext);
    const { setImagePreview } = useContext(AppContext);
    const [position, setPosition] = useState(null);
    const [radius, setRadius] = useState(200);
    
    const handleClick = (e) => {
        setPosition(e.latlng);
        console.log(e.latlng);
    }
    const LocationFinder= () => {
        const map = useMapEvents({
            click(e) {
                console.log(e.latlng);
                setPosition(e.latlng);
                map.setView(e.latlng, map.getZoom())
            },
        });
        return null;
    };

        const renderPosition = () => {
            
            if (position)
                return (
                    <h2>{position.lat} {position.lng}</h2>
                );    
            
            return (<h2>Click on the map to get the position</h2>);
        }
        const MapPosition = () => {
            if (position)
                return [position.lat, position.lng];
            console.log("MapPosition default");
            return [51.505, -0.09];
        }
        const goRender = () =>
        {
            if (position)
            {
                window.pywebview.api.ReadStreetMapData(position.lat, position.lng, radius).then ((svg) => {
                   
                    setImagePreview (svg);
        
                    
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
        const renderAction = () => {
            if (position  )
            {
                return (
                    <fieldset >
    
                    <legend>{GetLocaleString("citymap.sectionplan")}</legend>
                        <div className='TransportAction'>
                        
                            <button onClick={goRender}>
                                {GetLocaleString("citymap.rendermap")}
                            </button>
                        </div>
                    </fieldset>
                    );
            }    
        }
    return (
        <>
            <h1>City Map    </h1>
            {renderPosition()}
            <label>radius
            <input type="number" value={radius} onChange={(e) => setRadius(e.target.value)} />
            </label>
            <MapContainer center={MapPosition()} zoom={1} scrollWheelZoom={true}
            
            style={{ width: '99%', position: 'relative', zIndex: '9', height: '50vh' }}
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
        </>
    );
}

export default CityMap;