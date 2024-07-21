import {Alert, Box, Button, MenuItem, Stack, TextField, Typography} from "@mui/material";
import useStore from "../../store.ts";
import Ctr4EverClient from "../../services/ctr4EverClient.ts";
import {useEffect, useState} from "react";
import { useNavigate } from "react-router-dom";
import { AppRoutes } from "../../routes.tsx";

const RegisterView = () => {
    const navigate = useNavigate();
    const apiEndpoint = useStore(state => state.apiEndpoint);
    const jwt = useStore(state => state.jwt);
    const currentUser = useStore(state => state.currentUser);
    const countries = useStore(state => state.countries);
    const [ctr4ever, setCtr4Ever] = useState<Ctr4EverClient | null>(null);
    const [registerSuccess, setRegisterSuccess] = useState<boolean>(false);
    const [registerError, setRegisterError] = useState<string>('');
    const [registeredUsername, setRegisteredUsername] = useState<string>('');
    const [username, setUsername] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [countryId, setCountryId] = useState<string>('');

    useEffect(() => {
        setCtr4Ever(new Ctr4EverClient(apiEndpoint, jwt));
    }, [setCtr4Ever, apiEndpoint, jwt]);

    useEffect(() => {
        if (currentUser) {
            navigate(AppRoutes.IndexPage);
        }
    }, [navigate, currentUser, AppRoutes]);

    async function registerPlayer(username: string, email: string, password: string, country_id: number) {
        if (!ctr4ever) {
            return;
        }

        const response = await ctr4ever.registerPlayer(country_id, email, password, username);

        if (response.success) {
            setRegisterSuccess(true);
            setRegisterError('');
            setRegisteredUsername(username);
        } else {
            setRegisterSuccess(false);
            setRegisterError(response.error);
            setRegisteredUsername('');
        }
    }

    return (
        <>
            <Typography variant="h4">Register</Typography>

            <Box my={2}>
                {registerSuccess && <Alert severity="success">You successfully registered on ctr4ever. Welcome, {registeredUsername}!</Alert>}
                {registerError && <Alert severity="error">Error while registering your account: {registerError}</Alert>}
            </Box>

            <Stack component="form" spacing={2} width={"25ch"}>
                <TextField
                    label="Username"
                    variant="outlined"
                    name="username"
                    onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                    label="E-Mail"
                    variant="outlined"
                    name="email"
                    onChange={(e) => setEmail(e.target.value)}
                />
                <TextField
                    label="Password"
                    variant="outlined"
                    name="password"
                    type="password"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <TextField
                    select
                    label="Country"
                    variant="outlined"
                    name="country_id"
                    onChange={(e) => setCountryId(e.target.value)}
                >
                    {countries.map((option) => (
                        <MenuItem key={option.id} value={option.id}>
                            {option.name}
                        </MenuItem>
                    ))}
                </TextField>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={() => registerPlayer(username, email, password, Number(countryId))}
                >
                    Register
                </Button>
            </Stack>
        </>
    );
}

export default RegisterView;
