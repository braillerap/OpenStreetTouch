import { useContext, useState} from 'react'
import AppContext from "../components/AppContext";



const Metro = () => {
    const { setImagePreview } = useContext(AppContext);
    const [cityName, setCityName] = useState('')
    const [cityImage, setCityImage] = useState('')
    
    const goOsm = () => {
        window.pywebview.api.getCityImage (cityName).then ((imgdata) => {
            console.log (imgdata);
            //setCityImage(imgdata);
            setImagePreview(imgdata);
        }
        )
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
        <button onClick={goOsm()}>Go !</button>
        {renderImage() }
    </div>
  );
}

export default Metro;