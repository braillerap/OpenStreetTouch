import { useContext} from 'react'
import AppContext from "../components/AppContext";

const Preview = () => {
    const { ImagePreview } = useContext(AppContext);
    const { TransportGuide } = useContext(AppContext);
    
    
    
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