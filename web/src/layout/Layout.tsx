import {AppBar, Box, Container, Grid, Toolbar, Typography} from "@mui/material"
import {Outlet, useNavigate} from "react-router-dom";
import {AppRoutes} from "../routes.tsx";
import {StyledMainContainer} from "./Layout.styles.ts";


const Layout = () => {
    const navigate = useNavigate();

    return (
        <StyledMainContainer>
            <AppBar position="sticky">
                <Toolbar>
                    <Container>
                        <Grid container spacing={1}>
                            <Grid item xs={0}>
                                <Typography onClick={() => navigate(AppRoutes.IndexPage)}>Home</Typography>
                            </Grid>
                            <Grid item xs={0}>
                                <Typography onClick={() => navigate(AppRoutes.LoginPage)}>Login</Typography>
                            </Grid>
                            <Grid item xs={0}>
                                <Typography onClick={() => navigate(AppRoutes.RegisterPage)}>Register</Typography>
                            </Grid>
                        </Grid>
                    </Container>
                </Toolbar>
            </AppBar>
            <Container>
                <Box my={2}>
                    <Outlet />
                </Box>
            </Container>
        </StyledMainContainer>
    )
}

export default Layout;
