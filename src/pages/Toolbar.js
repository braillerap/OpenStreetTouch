import { useContext } from 'react';

import { FaRegTrashCan } from "react-icons/fa6";
import { FaEraser } from "react-icons/fa6";

import AppContext from "../components/AppContext";


const Toolbar = () => {
  // TODO : clarify use of state or context call
    const {GetLocaleString, GetBackend} = useContext(AppContext);

    
    //
    // delete selected object
    //
    const handleDelete = () => {
      
    }

    // 
    // clear the project
    //
    const handleDeleteAll = async () => {
          }
    
    return (
    <>
        <div className="toolbar">
            
            
            
            <button className ="pure-button " onClick={handleDelete}>
            <FaEraser />
            
            
            </button>
            &nbsp;
            <button className ="pure-button " onClick={handleDeleteAll}>
            <FaRegTrashCan />
            </button>

        </div>

    </>
    );
  };
  
  export default Toolbar;