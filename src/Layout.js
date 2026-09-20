import { useContext } from 'react';
import { Outlet, Link} from "react-router-dom";
import Preview from './pages/Preview'
import AppContext from "./components/AppContext";

const Layout = () => {
    const {GetLocaleString, GetLocaleDir, Params, GetBackend, AppTheme} = useContext(AppContext);
    
    const exitrequest = (e) => {
        
        e.preventDefault();

        GetBackend().confirm_dialog("OpenStreetTouch", GetLocaleString("app.confirquit")).then ((ret) => {
            if (ret === true)
                GetBackend().quit(); // exit appication
        });
    }
    
    const getAccessKeyMenuCallback = (menukey, accessKey, cb) => {
        
        if (Params.accesskey === true)
            return (<Link onClick={cb} className="MenuLink"
                accessKey={GetLocaleString(accessKey)}> 
                    {GetLocaleString(menukey)}
            </Link>
            );

        return (<Link onClick={cb} className="MenuLink" 
            >
                {GetLocaleString(menukey)} 
        </Link>);
        
    }
    const getAccessKeyMenu = (url, menukey, accessKey) => {
        
        if (Params.accesskey === true)
            return (<Link to={process.env.PUBLIC_URL + url} className="MenuLink"
                accessKey={GetLocaleString(accessKey)}> 
                    {GetLocaleString(menukey)}
            </Link>
            );

        return (<Link to={process.env.PUBLIC_URL + url} className="MenuLink" 
            >
                {GetLocaleString(menukey)} 
        </Link>);
        
    }

    return (
        <div className={AppTheme + ' AppContain'}>
            <div className="AppTail" dir={GetLocaleDir()}>
                <div className='AppHeaderTail'>
                    <div className="" role={'presentation'} >
                        <nav aria-live={"polite"}>
                            {/*accessKey={GetLocaleString("menu.home.shortcut")}*/ }
                            <ul className="flex flex-row justify-start gap-2">
                                <li className="relative">
                                    
                                    {getAccessKeyMenu("/", "menu.home", "menu.home.shortcut")}
                                </li>

                                <li className="relative">
                                   
                                    {getAccessKeyMenu( "/transport", "menu.transport", "menu.transport.shortcut")}
                                </li>
                                <li className="relative">
                                   
                                    {getAccessKeyMenu( "/cmap", "menu.citymap", "menu.citymap.shortcut")}
                                </li>
                                <li className="relative">
                                    
                                    { getAccessKeyMenu("/parameter", "menu.param", "menu.param.shortcut")}
                                </li>
                                <li className="relative">
                                    {getAccessKeyMenuCallback("menu.exit", "menu.exit.shortcut", exitrequest)}
                                </li>
                            </ul>
                            
                        </nav>

                    </div>
                    
                </div>
                
                <div aria-live={"polite"} aria-atomic={false} role={"log"} aria-relevant={"all"} className="App-functionTail">
                    <Outlet />
                </div>    
                <div className="App-WorkTail">
                    <Preview/>
                    
                </div>
                
                
            </div>
        </div>
    )
};

export default Layout;

