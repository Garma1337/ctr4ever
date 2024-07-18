import {Route, Routes} from 'react-router-dom'
import {AppRoutes} from "./routes.tsx";
import Layout from "./layout/Layout.tsx";
import IndexView from "./views/indexView/IndexView.tsx";
import LoginView from "./views/loginView/LoginView.tsx";
import RegisterView from "./views/registerView/RegisterView.tsx";

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import Ctr4Ever from "./services/ctr4ever.ts";
import useStore from "./store.ts";
import { useEffect } from 'react';

const App = () => {
    const ctr4ever = new Ctr4Ever('http://127.0.0.1:5000/api');
    const setCountries = useStore(state => state.setCountries);
    const setApiEndpoint = useStore(state => state.setApiEndpoint);

    useEffect(() => {
        setApiEndpoint('http://127.0.0.1:5000/api');
    }, [setApiEndpoint]);

    useEffect(() => {
        ctr4ever.findCountries().then(countries => setCountries(countries));
    }, [ctr4ever, setCountries]);

    return (
        <Routes>
            <Route path={AppRoutes.IndexPage} element={<Layout/>}>
                <Route index element={<IndexView/>}/>
                <Route path={AppRoutes.LoginPage} element={<LoginView/>}/>
                <Route path={AppRoutes.RegisterPage} element={<RegisterView/>}/>
            </Route>
        </Routes>
    )
}

export default App;
