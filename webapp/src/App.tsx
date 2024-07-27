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
import {useEffect, useState} from 'react';
import PlayerPageView from "./views/playerPageView/PlayerPageView.tsx";
import PlayerListView from "./views/playerListView/PlayerListView.tsx";
import CreateSubmissionView from "./views/createSubmissionView/CreateSubmissionView.tsx";

const App = () => {
    const apiEndpoint = useStore(state => state.apiEndpoint);
    const setApiEndpoint = useStore(state => state.setApiEndpoint);
    const jwt = useStore(state => state.jwt);
    const setJwt = useStore(state => state.setJwt);
    const setCurrentUser = useStore(state => state.setCurrentUser);
    const setCategories = useStore(state => state.setCategories);
    const setCountries = useStore(state => state.setCountries);
    const setCharacters = useStore(state => state.setCharacters);
    const setEngineStyles = useStore(state => state.setEngineStyles);
    const setGameVersions = useStore(state => state.setGameVersions);
    const setPlatforms = useStore(state => state.setPlatforms);
    const setRulesets = useStore(state => state.setRulesets);
    const setTracks = useStore(state => state.setTracks);
    const [ctr4EverClient, setCtr4EverClient] = useState<Ctr4EverClient | null>(null);

    useEffect(() => {
        setJwt(localStorage.getItem('jwt') || '');
    }, [setJwt]);

    useEffect(() => {
        setApiEndpoint('http://127.0.0.1:5000/api');
    }, [setApiEndpoint]);

    useEffect(() => {
        if (apiEndpoint) {
            setCtr4EverClient(new Ctr4EverClient(apiEndpoint, jwt));
        }
    }, [apiEndpoint, jwt]);

    useEffect(() => {
        if (ctr4EverClient) {
            ctr4EverClient.getSession().then(setCurrentUser);
        }
    }, [ctr4EverClient, setCurrentUser]);

    useEffect(() => {
        if (ctr4EverClient) {
            ctr4EverClient.findCategories().then(setCategories);
        }
    }, [ctr4EverClient, setCategories]);

    useEffect(() => {
        if (ctr4EverClient) {
            ctr4EverClient.findCharacters().then(setCharacters);
        }
    }, [ctr4EverClient, setCharacters]);

    useEffect(() => {
        if (ctr4EverClient) {
            ctr4EverClient.findCountries().then(setCountries);
        }
    }, [ctr4EverClient, setCountries]);

    useEffect(() => {
        if (ctr4EverClient) {
            ctr4EverClient.findEngineStyles().then(setEngineStyles);
        }
    }, [ctr4EverClient, setEngineStyles]);

    useEffect(() => {
        if (ctr4EverClient) {
            ctr4EverClient.findGameVersions().then(setGameVersions);
        }
    }, [ctr4EverClient, setGameVersions]);

    useEffect(() => {
        if (ctr4EverClient) {
            ctr4EverClient.findPlatforms().then(setPlatforms);
        }
    }, [ctr4EverClient, setPlatforms]);

    useEffect(() => {
        if (ctr4EverClient) {
            ctr4EverClient.findRulesets().then(setRulesets);
        }
    }, [ctr4EverClient, setRulesets]);

    useEffect(() => {
        if (ctr4EverClient) {
            ctr4EverClient.findTracks().then(setTracks);
        }
    }, [ctr4EverClient, setTracks]);

    return (
        <Routes>
            <Route path={AppRoutes.IndexPage} element={<Layout/>}>
                <Route index element={<IndexView/>}/>
                <Route path={AppRoutes.LoginPage} element={<LoginView/>}/>
                <Route path={AppRoutes.RegisterPage} element={<RegisterView/>}/>
                <Route path={AppRoutes.PlayerPage} element={<PlayerPageView/>}/>
                <Route path={AppRoutes.PlayerListPage} element={<PlayerListView />}/>
                <Route path={AppRoutes.CreateSubmissionPage} element={<CreateSubmissionView />}/>
            </Route>
        </Routes>
    )
}

export default App;
