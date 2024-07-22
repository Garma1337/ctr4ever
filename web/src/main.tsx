import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './App.css'
import {HashRouter} from 'react-router-dom'
import {createTheme, CssBaseline, ThemeProvider} from '@mui/material'

const theme = localStorage.getItem('theme') == 'light' ? 'light' : 'dark';

const darkTheme = createTheme({
    palette: {
        mode: theme,
    },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <HashRouter>
            <ThemeProvider theme={darkTheme}>
                <CssBaseline/>
                <App/>
            </ThemeProvider>
        </HashRouter>
    </React.StrictMode>,
)
