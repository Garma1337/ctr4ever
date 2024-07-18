import {Button, Stack, TextField, Typography } from "@mui/material";

const LoginView = () => {
    return (
        <Stack component="form" spacing={2} width={"25ch"}>
            <Typography variant="h3">Login</Typography>
            <TextField label="Username" variant="outlined"/>
            <TextField label="Password" variant="outlined" type="password"/>
            <Button variant="contained" color="primary">Login</Button>
            <Button variant="text" color="primary">Reset Password</Button>
        </Stack>
    );
}

export default LoginView;