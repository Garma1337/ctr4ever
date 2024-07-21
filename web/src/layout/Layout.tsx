import {AppBar, Box, Button, Container, IconButton, Menu, MenuItem, Toolbar} from "@mui/material"
import {Outlet, useNavigate} from "react-router-dom";
import {AppRoutes} from "../routes.tsx";
import useStore from "../store.ts";
import Brightness4Icon from '@mui/icons-material/Brightness4';
import {AccountCircle} from "@mui/icons-material";
import React from "react";
import TimerOutlinedIcon from '@mui/icons-material/TimerOutlined';

const Layout = () => {
    const navigate = useNavigate();
    const setJwt = useStore(state => state.setJwt);
    const currentUser = useStore(state => state.currentUser);
    const setCurrentUser = useStore(state => state.setCurrentUser);
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

    const handleAccountMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleAccountMenuClose = () => {
        setAnchorEl(null);
    };

    const logoutPlayer = () => {
        localStorage.removeItem('jwt');
        setJwt('');
        setCurrentUser(null);
        navigate(AppRoutes.IndexPage);
    }

    const toggleTheme = () => {
        const newTheme = localStorage.getItem('theme') === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
        window.location.reload();
    }

    return (
        <Box sx={{flexGrow: 1}}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton
                        size="large"
                        edge="start"
                        color="inherit"
                        aria-label="menu"
                        sx={{mr: 2}}
                    >
                        <TimerOutlinedIcon />
                    </IconButton>
                    <Box sx={{flexGrow: 1}}>
                        <Button
                            color="inherit"
                            onClick={() => navigate(AppRoutes.IndexPage)}
                        >
                            Home
                        </Button>
                    </Box>
                    {!currentUser && (
                        <>
                            <Button color="inherit" onClick={() => navigate(AppRoutes.LoginPage)}>Login</Button>
                            <Button color="inherit" onClick={() => navigate(AppRoutes.RegisterPage)}>Register</Button>
                        </>
                    )}
                    {currentUser && (
                        <div>
                            <Button onClick={handleAccountMenu} color="inherit">
                                <AccountCircle sx={{ marginRight: 1 }}/>
                                {currentUser.name}
                            </Button>
                            <Menu
                                id="menu-appbar"
                                anchorEl={anchorEl}
                                anchorOrigin={{
                                    vertical: 'top',
                                    horizontal: 'right',
                                }}
                                keepMounted
                                transformOrigin={{
                                    vertical: 'top',
                                    horizontal: 'right',
                                }}
                                open={Boolean(anchorEl)}
                                onClose={handleAccountMenuClose}
                            >
                                <MenuItem onClick={() => navigate(AppRoutes.PlayerPage + '?name=' + currentUser.name)}>Profile</MenuItem>
                                <MenuItem onClick={() => logoutPlayer()}>Logout</MenuItem>
                            </Menu>
                        </div>
                    )}
                    <IconButton
                        size="large"
                        edge="end"
                        color="inherit"
                        aria-label="toggle theme"
                        onClick={toggleTheme}
                    >
                        <Brightness4Icon/>
                    </IconButton>
                </Toolbar>
            </AppBar>
            <Container sx={{my: 2}}>
                <Outlet/>
            </Container>
        </Box>
    )
}

export default Layout;
