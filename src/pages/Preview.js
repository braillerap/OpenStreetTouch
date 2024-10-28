import { useContext, useState} from 'react'
import AppContext from "../components/AppContext";

const Preview = () => {
    const { ImagePreview } = useContext(AppContext);
    const [cityName, setCityName] = useState('')
    const [cityImage, setCityImage] = useState('')
    
   
    const renderImage = () => {
        if (ImagePreview !== '') {
          return (
            <div>
              <img src={`data:image/svg+xml;utf8,${encodeURIComponent(ImagePreview)}`} />
            </div>
        )

            console.log ("preview rendering image");
            const srcpat = "data:image/png;base64," + ImagePreview;
            return <img src={srcpat} alt="city image" width={"50%"} height={"50%"}/>
        }
        return (<></>);
    }
  return (
    <div>
      
        {renderImage() }
    </div>
  );
}

export default Preview;