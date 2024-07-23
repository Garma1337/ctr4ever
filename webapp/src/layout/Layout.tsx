import {AppBar, Box, Button, Container, IconButton, Menu, MenuItem, Toolbar} from "@mui/material"
import {Outlet, useNavigate} from "react-router-dom";
import {AppRoutes} from "../routes.tsx";
import useStore from "../store.ts";
import Brightness4Icon from '@mui/icons-material/Brightness4';
import {AccountCircle} from "@mui/icons-material";
import React from "react";
import TimerOutlinedIcon from '@mui/icons-material/TimerOutlined';
import HomeIcon from '@mui/icons-material/Home';

const Layout = () => {
    const navigate = useNavigate();
    const setJwt = useStore(state => state.setJwt);
    const currentUser = useStore(state => state.currentUser);
    const setCurrentUser = useStore(state => state.setCurrentUser);
    const [accountAnchorEL, setAccountAnchorEL] = React.useState<null | HTMLElement>(null);
    const [siteAnchorEL, setSiteAnchorEL] = React.useState<null | HTMLElement>(null);

    const handleAccountMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAccountAnchorEL(event.currentTarget);
    };

    const handleAccountMenuClose = () => {
        setAccountAnchorEL(null);
    };

    const handleSiteMenu = (event: React.MouseEvent<HTMLElement>) => {
        setSiteAnchorEL(event.currentTarget);
    };

    const handleSiteMenuClose = () => {
        setSiteAnchorEL(null);
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
                <Container>
                    <Toolbar sx={{paddingLeft: 0, paddingRight: 0}}>
                        <IconButton
                            size="large"
                            edge="start"
                            color="inherit"
                            aria-label="menu"
                            sx={{mr: 2}}
                        >
                            <TimerOutlinedIcon/>
                        </IconButton>
                        <Box sx={{flexGrow: 1}}>
                            <Button onClick={handleSiteMenu} color="inherit">
                                <HomeIcon sx={{marginRight: 1}}/>
                                Site
                            </Button>
                            <Menu
                                id="menu-appbar"
                                anchorEl={siteAnchorEL}
                                anchorOrigin={{
                                    vertical: 'top',
                                    horizontal: 'right',
                                }}
                                keepMounted
                                transformOrigin={{
                                    vertical: 'top',
                                    horizontal: 'right',
                                }}
                                open={Boolean(siteAnchorEL)}
                                onClose={handleSiteMenuClose}
                            >
                                <MenuItem onClick={() => navigate(AppRoutes.IndexPage)}>Home</MenuItem>
                                <MenuItem onClick={() => window.location.href = 'https://discord.gg/B65emaw'}>
                                    Discord Server
                                </MenuItem>
                            </Menu>
                            <Button color="inherit" onClick={() => navigate(AppRoutes.PlayerListPage)}>Players</Button>
                        </Box>
                        {!currentUser && (
                            <>
                                <Button color="inherit" onClick={() => navigate(AppRoutes.LoginPage)}>Login</Button>
                                <Button color="inherit"
                                        onClick={() => navigate(AppRoutes.RegisterPage)}>Register</Button>
                            </>
                        )}
                        {currentUser && (
                            <div>
                                <Button onClick={handleAccountMenu} color="inherit">
                                    <AccountCircle sx={{marginRight: 1}}/>
                                    {currentUser.name}
                                </Button>
                                <Menu
                                    id="menu-appbar"
                                    anchorEl={accountAnchorEL}
                                    anchorOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    keepMounted
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    open={Boolean(accountAnchorEL)}
                                    onClose={handleAccountMenuClose}
                                >
                                    <MenuItem
                                        onClick={() => navigate(AppRoutes.PlayerPage + '?name=' + currentUser.name)}>Profile</MenuItem>
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
                </Container>
            </AppBar>
            <Container sx={{my: 2}}>
                <Outlet/>
            </Container>
        </Box>
    )
}

export default Layout;
