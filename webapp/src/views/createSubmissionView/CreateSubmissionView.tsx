import { Alert, Box, Button, MenuItem, Stack, TextField, Typography } from "@mui/material";
import {useEffect, useState } from "react";
import Ctr4EverClient from "../../services/ctr4EverClient";
import useStore from "../../store";

const CreateSubmissionView = () => {
    const apiEndpoint = useStore(state => state.apiEndpoint);
    const jwt = useStore(state => state.jwt);
    const currentUser = useStore(state => state.currentUser);
    const tracks = useStore(state => state.tracks);
    const categories = useStore(state => state.categories);
    const characters = useStore(state => state.characters);
    const gameVersions = useStore(state => state.gameVersions);
    const rulesets = useStore(state => state.rulesets);
    const platforms = useStore(state => state.platforms);
    const [ctr4EverClient, setCtr4EverClient] = useState<Ctr4EverClient | null>(null);

    const [trackId, setTrackId] = useState<Number | null>(null);
    const [categoryId, setCategoryId] = useState<Number | null>(null);
    const [characterId, setCharacterId] = useState<Number | null>(null);
    const [gameVersionId, setGameVersionId] = useState<Number | null>(null);
    const [rulesetId, setRulesetId] = useState<Number | null>(null);
    const [platformId, setPlatformId] = useState<Number | null>(null);
    const [time, setTime] = useState<string | null>(null);
    const [video, setVideo] = useState<string | null>(null);
    const [comment, setComment] = useState<string | null>(null);

    const [submitSuccess, setSubmitSuccess] = useState<boolean>(false);
    const [submitError, setSubmitError] = useState<string>('');

    useEffect(() => {
        if (apiEndpoint) {
            setCtr4EverClient(new Ctr4EverClient(apiEndpoint, jwt));
        }
    }, [apiEndpoint, jwt]);

    const createSubmission = async (
        playerId: Number,
        trackId: Number,
        categoryId: Number,
        characterId: Number,
        gameVersionId: Number,
        rulesetId: Number,
        platformId: Number,
        time: string,
        video: string,
        comment: string
    ) => {
        if (!ctr4EverClient) {
            return;
        }

        const response = await ctr4EverClient.createSubmission(
            playerId,
            trackId,
            categoryId,
            characterId,
            gameVersionId,
            rulesetId,
            platformId,
            time,
            video,
            comment
        );

        if (response.success) {
            setSubmitSuccess(true);
            setSubmitError('');
        } else {
            setSubmitSuccess(false);
            setSubmitError(response.error);
        }
    }

    return (
        <>
            <Typography variant="h4">Submit Time</Typography>

            <Box my={2}>
                {submitError && (
                    <Alert severity="error">Failed to submit time: {submitError}</Alert>
                )}

                {submitSuccess && (
                    <Alert severity="success">Your time was submitted successfully!</Alert>
                )}
            </Box>

            <Stack component="form" spacing={2} width={"30ch"}>
                <TextField
                    select
                    label="Track"
                    variant="outlined"
                    name="track_id"
                    value={trackId || ''}
                    onChange={(e) => setTrackId(Number(e.target.value))}
                >
                    {tracks.map((option) => (
                        <MenuItem key={option.id} value={option.id}>
                            {option.name}
                        </MenuItem>
                    ))}
                </TextField>
                <TextField
                    select
                    label="Category"
                    variant="outlined"
                    name="category_id"
                    value={categoryId || ''}
                    onChange={(e) => setCategoryId(Number(e.target.value))}
                >
                    {categories.map((option) => (
                        <MenuItem key={option.id} value={option.id}>
                            {option.name}
                        </MenuItem>
                    ))}
                </TextField>
                <TextField
                    select
                    label="Character"
                    variant="outlined"
                    name="character_id"
                    value={characterId || ''}
                    onChange={(e) => setCharacterId(Number(e.target.value))}
                >
                    {characters.map((option) => (
                        <MenuItem key={option.id} value={option.id}>
                            {option.name}
                        </MenuItem>
                    ))}
                </TextField>
                <TextField
                    select
                    label="Game Version"
                    variant="outlined"
                    name="game_version_id"
                    value={gameVersionId || ''}
                    onChange={(e) => setGameVersionId(Number(e.target.value))}
                >
                    {gameVersions.map((option) => (
                        <MenuItem key={option.id} value={option.id}>
                            {option.name}
                        </MenuItem>
                    ))}
                </TextField>
                <TextField
                    select
                    label="Ruleset"
                    variant="outlined"
                    name="ruleset_id"
                    value={rulesetId || ''}
                    onChange={(e) => setRulesetId(Number(e.target.value))}
                >
                    {rulesets.map((option) => (
                        <MenuItem key={option.id} value={option.id}>
                            {option.name}
                        </MenuItem>
                    ))}
                </TextField>
                <TextField
                    select
                    label="Platform"
                    variant="outlined"
                    name="platform_id"
                    value={platformId || ''}
                    onChange={(e) => setPlatformId(Number(e.target.value))}
                >
                    {platforms.map((option) => (
                        <MenuItem key={option.id} value={option.id}>
                            {option.name}
                        </MenuItem>
                    ))}
                </TextField>
                <TextField
                    label="Time"
                    variant="outlined"
                    name="time"
                    value={time || ''}
                    onChange={(e) => setTime(e.target.value)}
                />
                <TextField
                    label="Video"
                    variant="outlined"
                    name="video"
                    value={video || ''}
                    onChange={(e) => setVideo(e.target.value)}
                />
                <TextField
                    multiline
                    rows={5}
                    label="Comment (optional)"
                    variant="outlined"
                    name="comment"
                    value={comment || ''}
                    onChange={(e) => setComment(e.target.value)}
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={() => createSubmission(Number(currentUser.id), Number(trackId), Number(categoryId), Number(characterId), Number(gameVersionId), Number(rulesetId), Number(platformId), String(time), String(video), String(comment))}
                >
                    Submit Time
                </Button>
            </Stack>
        </>
    );
}

export default CreateSubmissionView;