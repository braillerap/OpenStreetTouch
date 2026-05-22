import { useContext } from 'react';
import { Outlet, Link} from "react-router-dom";
import Preview from './pages/Preview'
import AppContext from "./components/AppContext";

//import Toolbar from "./pages/Toolbar";




const Layout = () => {
    const {GetLocaleString, GetLocaleDir, Params} = useContext(AppContext);
    
    const exitrequest = (e) => {
        
        e.preventDefault();
        window.pywebview.api.confirm_dialog("OpenStreetTouch", GetLocaleString("app.confirquit")).then ((ret) => {
            if (ret === true)
                window.pywebview.api.quit();
        });
        

    }
    
    const getAccessKeyMenuCallback = (menukey, accessKey, cb) => {
        
        if (Params.accesskey === true)
            return (<Link onClick={cb} className="pure-menu-link"
                accessKey={GetLocaleString(accessKey)}> 
                    {GetLocaleString(menukey)}
            </Link>
            );

        return (<Link onClick={cb} className="pure-menu-link" 
            >
                {GetLocaleString(menukey)} 
        </Link>);
        
    }
    const getAccessKeyMenu = (url, menukey, accessKey) => {
        
        if (Params.accesskey === true)
            return (<Link to={url} className="pure-menu-link"
                accessKey={GetLocaleString(accessKey)}> 
                    {GetLocaleString(menukey)}
            </Link>
            );

        return (<Link to={url} className="pure-menu-link" 
            >
                {GetLocaleString(menukey)} 
        </Link>);
        
    }

    return (
        <div className='AppContainer'>
            <div className="App" dir={GetLocaleDir()}>
                <div className='AppHeader'>
                    <div className="pure-menu pure-menu-horizontal menu_font" role={'presentation'} >
                        <nav aria-live={"polite"}>
                            {/*accessKey={GetLocaleString("menu.home.shortcut")}*/ }
                            <ul className="pure-menu-list">
                                <li className="pure-menu-item">
                                    
                                    {getAccessKeyMenu("/", "menu.home", "menu.home.shortcut")}
                                </li>

                                <li className="pure-menu-item">
                                   
                                    {getAccessKeyMenu("/transport", "menu.transport", "menu.transport.shortcut")}
                                </li>
                                <li className="pure-menu-item">
                                   
                                    {getAccessKeyMenu("/cmap", "menu.citymap", "menu.citymap.shortcut")}
                                </li>
                                <li className="pure-menu-item">
                                    
                                    {getAccessKeyMenu("/parameter", "menu.param", "menu.param.shortcut")}
                                </li>
                                <li className="pure-menu-item">
                                    {/*<Link onClick={exitrequest} className="pure-menu-link"
                                        accessKey={GetLocaleString("menu.exit.shortcut")}>
                                    
                                        {GetLocaleString("menu.exit")} </Link>*/}
                                    {getAccessKeyMenuCallback("menu.exit", "menu.exit.shortcut", exitrequest)}
                                </li>
                            </ul>
                            {/*<button className="pure-menu-heading" onClick={() => {ForceResize()}}>FR</button>*/}

                        </nav>

                    </div>
                    {/*<Toolbar />*/}
                </div>
                
                <div aria-live={"polite"} aria-atomic={false} role={"log"} aria-relevant={"all"} className="App-function">
                    <Outlet />
                </div>    
                <div className="App-Work">
                    <Preview/>
                    
                </div>
                
                
            </div>
        </div>
    )
};

export default Layout;

