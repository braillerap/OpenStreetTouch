import { useContext } from 'react';
import { Outlet, Link} from "react-router-dom";
import Preview from './pages/Preview'
import AppContext from "./components/AppContext";

import Toolbar from "./pages/Toolbar";




const Layout = () => {
    const {GetLocaleString, GetLocaleDir} = useContext(AppContext);
    
    
   

    return (
        <div className='AppContainer'>
            <div className="App" dir={GetLocaleDir()}>
                <div className='AppHeader'>
                    <div className="pure-menu pure-menu-horizontal menu_font" role={'presentation'} >
                        <nav>
                            <ul className="pure-menu-list">
                                <li className="pure-menu-item">
                                    <Link to="/" className="pure-menu-link">{GetLocaleString("menu.home")} </Link>
                                </li>

                                <li className="pure-menu-item">
                                    <Link to="/metro" className="pure-menu-link">{GetLocaleString("menu.metro")} </Link>
                                </li>
                                <li className="pure-menu-item">
                                    <Link to="/parameter" className="pure-menu-link">{GetLocaleString("menu.param")}</Link>
                                </li>
                                
                            </ul>
                            {/*<button className="pure-menu-heading" onClick={() => {ForceResize()}}>FR</button>*/}

                        </nav>

                    </div>
                    <Toolbar />
                </div>
                
                <div className="App-Work">
                    <Preview/>
                </div>    
                <div className="App-function">
                    <Outlet />
                </div>
                
                
            </div>
        </div>
    )
};

export default Layout;

