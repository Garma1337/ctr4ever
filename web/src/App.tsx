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
import Ctr4EverClient from "./services/ctr4EverClient.ts";
import useStore from "./store.ts";
import {useEffect} from 'react';
import PlayerPageView from "./views/playerPageView/PlayerPageView.tsx";

const App = () => {
    const apiEndpoint = useStore(state => state.apiEndpoint);
    const setApiEndpoint = useStore(state => state.setApiEndpoint);
    const jwt = useStore(state => state.jwt);
    const setJwt = useStore(state => state.setJwt);
    const setCurrentUser = useStore(state => state.setCurrentUser);
    const setCountries = useStore(state => state.setCountries);

    useEffect(() => {
        setJwt(localStorage.getItem('jwt') || '');
    }, [setJwt]);

    useEffect(() => {
        setApiEndpoint('http://127.0.0.1:5000/api');
    }, [setApiEndpoint]);

    useEffect(() => {
        if (!apiEndpoint) {
            return;
        }

        const ctr4ever = new Ctr4EverClient(apiEndpoint, jwt)
        ctr4ever.getSession().then(currentUser => setCurrentUser(currentUser));
        ctr4ever.findCountries().then(countries => setCountries(countries));
    }, [jwt, apiEndpoint, setCountries, setCurrentUser]);

    return (
        <Routes>
            <Route path={AppRoutes.IndexPage} element={<Layout/>}>
                <Route index element={<IndexView/>}/>
                <Route path={AppRoutes.LoginPage} element={<LoginView/>}/>
                <Route path={AppRoutes.RegisterPage} element={<RegisterView/>}/>
                <Route path={AppRoutes.PlayerPage} element={<PlayerPageView/>}/>
            </Route>
        </Routes>
    )
}

export default App;
