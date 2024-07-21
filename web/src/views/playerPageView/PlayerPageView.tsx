import {Alert, Avatar, Box, List, ListItem, ListItemAvatar, ListItemText, Typography} from "@mui/material";
import {useEffect, useState} from "react";
import useStore from "../../store.ts";
import Ctr4EverClient from "../../services/ctr4EverClient.ts";
import {useSearchParams} from "react-router-dom";
import PersonIcon from '@mui/icons-material/Person';
import PublicIcon from '@mui/icons-material/Public';
import AccessTimeIcon from '@mui/icons-material/AccessTime';

const PlayerPageView = () => {
    const apiEndpoint = useStore(state => state.apiEndpoint);
    const jwt = useStore(state => state.jwt);
    const [searchParams] = useSearchParams();
    const [ctr4everClient, setCtr4everClient] = useState<Ctr4EverClient | null>(null);
    const [player, setPlayer] = useState<any>(null);

    useEffect(() => {
        setCtr4everClient(new Ctr4EverClient(apiEndpoint, jwt));
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

    function formatDate(time: string) {
        const date = new Date(time);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
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

                    {player.submissions.length > 0 && (
                        <></>
                    )}
                    {player.submissions.length <= 0 && (
                        <Alert severity="warning">This player has not submitted any times yet.</Alert>
                    )}
                </>
            )}
            {!player && <Alert severity="error">No player named {searchParams.get('name')} exists.</Alert>}
        </>
    );
}

export default PlayerPageView;