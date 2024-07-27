import {Alert, Box, Button, Stack, TextField, Typography} from "@mui/material";
import useStore from "../../store.ts";
import {useEffect, useState} from "react";
import Ctr4EverClient from "../../services/ctr4EverClient.ts";
import {useNavigate} from "react-router-dom";
import {AppRoutes} from "../../routes.tsx";

const LoginView = () => {
    const navigate = useNavigate();
    const apiEndpoint = useStore(state => state.apiEndpoint);
    const jwt = useStore(state => state.jwt);
    const setJwt = useStore(state => state.setJwt);
    const currentUser = useStore(state => state.currentUser);
    const [loginError, setLoginError] = useState<string | null>(null);
    const [ctr4EverClient, setCtr4EverClient] = useState<Ctr4EverClient | null>(null);
    const [username, setUsername] = useState<string | null>(null);
    const [password, setPassword] = useState<string | null>(null);

    useEffect(() => {
        setCtr4EverClient(new Ctr4EverClient(apiEndpoint, jwt));
    }, [setCtr4EverClient, apiEndpoint, jwt]);

    useEffect(() => {
        if (currentUser) {
            navigate(AppRoutes.IndexPage);
        }
    }, [navigate, currentUser, AppRoutes]);

    async function loginPlayer(username: string, password: string) {
        if (!ctr4EverClient) {
            return;
        }

        const response = await ctr4EverClient.loginPlayer(username, password);

        if (response.success) {
            localStorage.setItem('jwt', response.access_token);
            setJwt(response.access_token);
            navigate(AppRoutes.IndexPage);
        } else {
            setLoginError(response.error);
        }
    }

    return (
        <>
            <Typography variant="h3">Login</Typography>

            <Box my={2}>
                {loginError && <Alert severity="error">Failed to log in: {loginError}</Alert>}
            </Box>

            <Stack component="form" spacing={2} width={"25ch"}>
                <TextField
                    label="Username"
                    variant="outlined"
                    value={username || ''}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                    label="Password"
                    variant="outlined"
                    type="password"
                    value={password || ''}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <Button
                    variant="contained"
                    color="primary"
                    type="submit"
                    onClick={() => loginPlayer(String(username), String(password))}
                >
                    Login
                </Button>
                <Button variant="text" color="primary">Reset Password</Button>
            </Stack>
        </>
    );
}

export default LoginView;