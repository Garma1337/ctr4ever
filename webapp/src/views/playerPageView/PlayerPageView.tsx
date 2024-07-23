import {
    Alert,
    Avatar,
    Box,
    Button,
    FormControl,
    List,
    ListItem,
    ListItemAvatar,
    ListItemText,
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
import {useEffect, useState} from "react";
import useStore from "../../store.ts";
import Ctr4EverClient from "../../services/ctr4EverClient.ts";
import {useSearchParams} from "react-router-dom";
import PersonIcon from '@mui/icons-material/Person';
import PublicIcon from '@mui/icons-material/Public';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import formatDate from "../../utils/formatDate.ts";

const PlayerPageView = () => {
    const apiEndpoint = useStore(state => state.apiEndpoint);
    const jwt = useStore(state => state.jwt);
    const categories = useStore(state => state.categories);
    const platforms = useStore(state => state.platforms);
    const gameVersions = useStore(state => state.gameVersions);
    const ruleSets = useStore(state => state.rulesets);
    const tracks = useStore(state => state.tracks);

    const [searchParams] = useSearchParams();
    const [ctr4everClient, setCtr4everClient] = useState<Ctr4EverClient | null>(null);
    const [player, setPlayer] = useState<any>(null);

    const [categoryId, setCategoryId] = useState<string>('');
    const [platformId, setPlatformId] = useState<string>('');
    const [gameVersionId, setGameVersionId] = useState<string>('');
    const [ruleSetId, setRuleSetId] = useState<string>('');

    useEffect(() => {
        if (apiEndpoint) {
            setCtr4everClient(new Ctr4EverClient(apiEndpoint, jwt));
        }
    }, [apiEndpoint, jwt]);

    useEffect(() => {
        if (!ctr4everClient) {
            return;
        }

        const username = searchParams.get('name');
        ctr4everClient.findPlayers(null, username).then((players) => {
            if (players.length <= 0) {
                return;
            }

            setPlayer(players[0]);
        });
    }, [ctr4everClient, searchParams, setPlayer]);

    function resetForm() {
        setCategoryId('');
        setPlatformId('');
        setGameVersionId('');
        setRuleSetId('');
    }

    return (
        <>
            {player && (
                <>
                    <Typography variant="h4">Player Profile</Typography>

                    <Box my={2}>
                        <Alert severity="info">
                            You will find all the information about the player here. You can click on one of the times
                            listed to access the corresponding chart. You can also access the different rankings by
                            clicking one of the 'Totals' categories ...
                        </Alert>
                    </Box>

                    <List sx={{width: '100%', maxWidth: 360, bgcolor: 'background.paper'}}>
                        <ListItem>
                            <ListItemAvatar>
                                <Avatar>
                                    <PersonIcon/>
                                </Avatar>
                            </ListItemAvatar>
                            <ListItemText primary="Name" secondary={player.name}/>
                        </ListItem>
                        <ListItem>
                            <ListItemAvatar>
                                <Avatar>
                                    <PublicIcon/>
                                </Avatar>
                            </ListItemAvatar>
                            <ListItemText primary="Country" secondary={player.country.name}/>
                        </ListItem>
                        <ListItem>
                            <ListItemAvatar>
                                <Avatar>
                                    <AccessTimeIcon/>
                                </Avatar>
                            </ListItemAvatar>
                            <ListItemText primary="Registered since" secondary={formatDate(player.created)}/>
                        </ListItem>
                    </List>

                    <Typography variant="h5">Submissions</Typography>

                    <Box my={2}>
                        <FormControl sx={{minWidth: 180, marginRight: 2, marginBottom: 2}}>
                            <TextField
                                select
                                label="Category"
                                variant="outlined"
                                name="category_id"
                                value={categoryId}
                                onChange={(e) => setCategoryId(e.target.value)}
                            >
                                {categories.map((option) => (
                                    <MenuItem key={option.id} value={option.id}>
                                        {option.name}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </FormControl>

                        <FormControl sx={{minWidth: 180, marginRight: 2, marginBottom: 2}}>
                            <TextField
                                select
                                label="Platform"
                                variant="outlined"
                                name="platform_id"
                                value={platformId}
                                onChange={(e) => setPlatformId(e.target.value)}
                            >
                                {platforms.map((option) => (
                                    <MenuItem key={option.id} value={option.id}>
                                        {option.name}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </FormControl>

                        <FormControl sx={{minWidth: 180, marginRight: 2, marginBottom: 2}}>
                            <TextField
                                select
                                label="Game Version"
                                variant="outlined"
                                name="game_version_id"
                                value={gameVersionId}
                                onChange={(e) => setGameVersionId(e.target.value)}
                            >
                                {gameVersions.map((option) => (
                                    <MenuItem key={option.id} value={option.id}>
                                        {option.name}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </FormControl>

                        <FormControl sx={{minWidth: 180, marginRight: 2, marginBottom: 2}}>
                            <TextField
                                select
                                label="Ruleset"
                                variant="outlined"
                                name="ruleset_id"
                                value={ruleSetId}
                                onChange={(e) => setRuleSetId(e.target.value)}
                            >
                                {ruleSets.map((option) => (
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

                    <TableContainer component={Paper}>
                        <Table sx={{minWidth: 650}} aria-label="PBs">
                            <TableHead>
                                <TableRow>
                                    <TableCell>Track</TableCell>
                                    <TableCell align="right">Character</TableCell>
                                    <TableCell align="right">Game Version</TableCell>
                                    <TableCell align="right">Rank</TableCell>
                                    <TableCell align="right">SR:PR</TableCell>
                                    <TableCell align="right">Standard</TableCell>
                                    <TableCell align="right">Points</TableCell>
                                    <TableCell align="right">Date</TableCell>
                                    <TableCell align="right">Video</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {tracks.map((row) => (
                                    <TableRow
                                        key={row.id}
                                        sx={{'&:last-child td, &:last-child th': {border: 0}}}
                                    >
                                        <TableCell component="th" scope="row">
                                            {row.name}
                                        </TableCell>
                                        <TableCell align="right">-</TableCell>
                                        <TableCell align="right">-</TableCell>
                                        <TableCell align="right">-</TableCell>
                                        <TableCell align="right">-</TableCell>
                                        <TableCell align="right">-</TableCell>
                                        <TableCell align="right">-</TableCell>
                                        <TableCell align="right">-</TableCell>
                                        <TableCell align="right">-</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </>
            )}
            {!player && <Alert severity="error">No player named {searchParams.get('name')} exists.</Alert>}
        </>
    );
}

export default PlayerPageView;