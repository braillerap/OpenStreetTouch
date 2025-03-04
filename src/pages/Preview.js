import { useContext, useState} from 'react'
import AppContext from "../components/AppContext";

const Preview = () => {
    const { ImagePreview } = useContext(AppContext);
    const { TransportGuide } = useContext(AppContext);
    const {GetLocaleString} = useContext(AppContext);
    const [cityName, setCityName] = useState('')
    const [cityImage, setCityImage] = useState('')
    
    const saveImage = () => {
      let dialogtitle = GetLocaleString("file.saveas"); //"Enregistrer sous...";
      let filter = [
          GetLocaleString("file.svgfile"), //"Fichier svg",
          GetLocaleString("file.all") //"Tous"
      ]

      window.pywebview.api.saveas_svgfile(ImagePreview, dialogtitle, filter);
    }
    const renderImage = () => {
        if (ImagePreview !== '') {
          return (
            <>
            <div>
              <img src={`data:image/svg+xml;utf8,${encodeURIComponent(ImagePreview)}`} />
            </div>
              {/*<button onClick={saveImage}>{GetLocaleString("preview.savesvg")}</button>*/}
            </>
          )
            /*
            console.log ("preview rendering image");
            const srcpat = "data:image/png;base64," + ImagePreview;
            return <img src={srcpat} alt="city image" width={"50%"} height={"50%"}/>
            */
        }
        return (<></>);
    }
    const renderGuide = () => {
        if (TransportGuide !== '') {
          return (
            <pre className='transportguide'>
            {TransportGuide}
            </pre>

          )
        }
    }
  return (
    <div>
      
        {renderImage() }
        {renderGuide()}
    </div>
  );
}

export default Preview;