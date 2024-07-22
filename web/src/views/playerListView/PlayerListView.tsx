import {useEffect, useState} from "react";
import Ctr4EverClient from "../../services/ctr4EverClient";
import useStore from "../../store";
import {
    Alert,
    Box,
    Button,
    FormControl,
    MenuItem,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography
} from "@mui/material";
import formatDate from "../../utils/formatDate.ts";
import {Link, useNavigate } from "react-router-dom";
import {AppRoutes} from "../../routes.tsx";

const PlayerListView = () => {
    const navigate = useNavigate();

    const apiEndpoint = useStore(state => state.apiEndpoint);
    const jwt = useStore(state => state.jwt);
    const countries = useStore(state => state.countries);

    const [ctr4EverClient, setCtr4EverClient] = useState<Ctr4EverClient | null>(null);

    const [players, setPlayers] = useState<any[]>([]);
    const [countryId, setCountryId] = useState<string | null>(null);

    useEffect(() => {
        if (apiEndpoint) {
            setCtr4EverClient(new Ctr4EverClient(apiEndpoint, jwt));
        }
    }, [apiEndpoint, jwt, setCtr4EverClient]);

    useEffect(() => {
        if (ctr4EverClient) {
            ctr4EverClient.findPlayers(countryId).then(setPlayers);
        }
    }, [ctr4EverClient, setPlayers, countryId]);

    const resetForm = () => {
        setCountryId(null);
    }

    return (
        <>
            <Typography variant="h4">Player List</Typography>

            <Box my={2}>
                <FormControl sx={{minWidth: 180, marginRight: 2, marginBottom: 2}}>
                    <TextField
                        select
                        label="Category"
                        variant="outlined"
                        name="category_id"
                        value={countryId}
                        onChange={(e) => setCountryId(e.target.value)}
                    >
                        {countries.map((option) => (
                            <MenuItem key={option.id} value={option.id}>
                                {option.name}
                            </MenuItem>
                        ))}
                    </TextField>
                </FormControl>

                <Button
                    onClick={() => resetForm()}
                    variant="contained"
                    color="primary"
                    size="large"
                    sx={{padding: 1.75}}
                >
                    Reset
                </Button>
            </Box>

            {players.length <= 0 && (
                <Alert severity="warning">No players match your filter criteria.</Alert>
            )}

            {players.length > 0 && (
                <TableContainer component={Paper}>
                    <Table sx={{minWidth: 650}} aria-label="PBs">
                        <TableHead>
                            <TableRow>
                                <TableCell>#</TableCell>
                                <TableCell align="right">Name</TableCell>
                                <TableCell align="right">Country</TableCell>
                                <TableCell align="right">Registered</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {players.map((row) => (
                                <TableRow
                                    key={row.id}
                                    sx={{'&:last-child td, &:last-child th': {border: 0}}}
                                >
                                    <TableCell component="th" scope="row">
                                        {row.id}
                                    </TableCell>
                                    <TableCell align="right">
                                        <Typography onClick={() => navigate(`${AppRoutes.PlayerPage}?name=${row.name}`)}>
                                            <Link to="#">{row.name}</Link>
                                        </Typography>
                                    </TableCell>
                                    <TableCell align="right">{row.country.name}</TableCell>
                                    <TableCell align="right">{formatDate(row.created)}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}
        </>
    );
}

export default PlayerListView;