import { useContext, useState, useEffect} from 'react'
import AppContext from "../components/AppContext";
import { MapContainer } from 'react-leaflet';

const CityMap = () => {
    const {GetLocaleString} = useContext(AppContext);
    const { setImagePreview } = useContext(AppContext);


    return (
        <>
            <h1>City Map    </h1>
            
        </>
    );
}

export default CityMap;