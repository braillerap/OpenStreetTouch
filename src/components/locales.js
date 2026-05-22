import French from '../locales/fr.json';
import English from '../locales/en.json';
import Netherland from '../locales/nl.json';
import SimpleChinese from '../locales/zh_Hans.json';

const locales = {
    "en":       {lang:"en", dir:'ltr', desc:'en - English',data:English},
    "fr":       {lang:"fr", dir:'ltr', desc:'fr - Français',data:French},
    "nl":       {lang:"nl", dir:'ltr', desc:'nl - Dutch',data:Netherland},
    "zh-hans":  {lang:"zh-hans", dir:'ltr', desc:'zh-hans - 简体中文',   reverse:false, data:SimpleChinese}
}; 

export default locales;