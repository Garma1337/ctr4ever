import {Button, Stack, TextField, Typography } from "@mui/material";
import useStore from "../../store.ts";
import Ctr4Ever from "../../services/ctr4ever.ts";
import { useState } from "react";

const LoginView = () => {
    const apiEndpoint = useStore(state => state.apiEndpoint);
    const ctr4ever = new Ctr4Ever(apiEndpoint);
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');

    async function loginPlayer(username: string, password: string) {
        const response = await ctr4ever.loginPlayer(username, password);

        if (response.success) {
            console.log(`Successfully logged in as ${username}`);
        } else {
            console.log(`Failed to login as ${username}: ${response.error}`);
        }
    }

    return (
        <Stack component="form" spacing={2} width={"25ch"}>
            <Typography variant="h3">Login</Typography>
            <TextField
                label="Username"
                variant="outlined"
                onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
                label="Password"
                variant="outlined"
                type="password"
                onChange={(e) => setPassword(e.target.value)}
            />
            <Button
                variant="contained"
                color="primary"
                type="submit"
                onClick={() => loginPlayer(username, password)}
            >
                Login
            </Button>
            <Button variant="text" color="primary">Reset Password</Button>
        </Stack>
    );
}

export default LoginView;