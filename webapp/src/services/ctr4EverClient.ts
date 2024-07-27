import axios, {AxiosInstance} from "axios";

export default class Ctr4EverClient {
    protected client: AxiosInstance;

    public constructor(apiEndpoint: string, jwt: string) {
        this.client = axios.create({
            baseURL: apiEndpoint,
            timeout: 5000,
            validateStatus: (status) => status >= 200 && status < 300
        });

        if (jwt) {
            this.client.defaults.headers.common['Authorization'] = `Bearer ${jwt}`;
        }
    }

    public async findCategories(name: string | null = null): Promise<any> {
        try {
            const response = await this.client.get('/categories', {params: {name}});
            return response.data['categories'];
        } catch (e) {
            console.log(`Failed to fetch category list: ${e}`);
            return [];
        }
    }

    public async findCharacters(name: string | null = null): Promise<any> {
        try {
            const response = await this.client.get('/characters', {params: {name}});
            return response.data['characters'];
        } catch (e) {
            console.log(`Failed to fetch character list: ${e}`);
            return [];
        }
    }

    public async findCountries(countryName: string | null = null): Promise<any> {
        try {
            const response = await this.client.get('/countries', {params: {countryName}});
            return response.data['countries'];
        } catch (e) {
            console.log(`Failed to fetch country list: ${e}`);
            return [];
        }
    }

    public async findEngineStyles(name: string | null = null): Promise<any> {
        try {
            const response = await this.client.get('/engineStyles', {params: {name}});
            return response.data['engine_styles'];
        } catch (e) {
            console.log(`Failed to fetch engine style list: ${e}`);
            return [];
        }
    }

    public async findGameVersions(name: string | null = null): Promise<any> {
        try {
            const response = await this.client.get('/gameVersions', {params: {name}});
            return response.data['game_versions'];
        } catch (e) {
            console.log(`Failed to fetch game version list: ${e}`);
            return [];
        }
    }

    public async findPlatforms(name: string | null = null): Promise<any> {
        try {
            const response = await this.client.get('/platforms', {params: {name}});
            return response.data['platforms'];
        } catch (e) {
            console.log(`Failed to fetch platform list: ${e}`);
            return [];
        }
    }

    public async findPlayers(
        countryId: Number | null = null,
        name: string | null = null,
        email: string | null = null,
        active: boolean | null = null,
    ): Promise<any> {
        try {
            const response = await this.client.get('/players', {params: {country_id: countryId, name, email, active}});
            return response.data['players'];
        } catch (e) {
            console.log(`Failed to fetch player list: ${e}`);
            return [];
        }
    }

    public async findRulesets(name: string | null = null): Promise<any> {
        try {
            const response = await this.client.get('/rulesets', {params: {name}});
            return response.data['rulesets'];
        } catch (e) {
            console.log(`Failed to fetch ruleset list: ${e}`);
            return [];
        }
    }

    public async findTracks(name: string | null = null): Promise<any> {
        try {
            const response = await this.client.get('/tracks', {params: {name}});
            return response.data['tracks'];
        } catch (e) {
            console.log(`Failed to fetch track list: ${e}`);
            return [];
        }
    }

    public async loginPlayer(username: string, password: string): Promise<any> {
        try {
            const response = await this.client.post('/loginPlayer', {username, password});
            return response.data;
        } catch (e) {
            console.log(`Failed to login player ${username}: ${e}`);

            return {
                success: false,
                error: e
            };
        }
    }

    public async getSession(): Promise<any> {
        try {
            const response = await this.client.get('/session');
            return response.data['current_user'];
        } catch (e) {
            console.log(`Failed to get session: ${e}`);
            return {'current_user': {}};
        }
    }

    public async registerPlayer(country_id: Number, email: string, password: string, username: string): Promise<any> {
        try {
            const response = await this.client.post('/registerPlayer', {country_id, email, password, username});
            return response.data;
        } catch (e) {
            console.log(`Failed to register player ${username}: ${e}`);

            return {
                success: false,
                error: e
            };
        }
    }

    public async createSubmission(
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
    ): Promise<any> {
        try {
            const response = await this.client.post('/createSubmission', {
                player_id: playerId,
                track_id: trackId,
                category_id: categoryId,
                character_id: characterId,
                game_version_id: gameVersionId,
                ruleset_id: rulesetId,
                platform_id: platformId,
                time,
                video,
                comment
            });

            return response.data;
        } catch (e) {
            console.log(`Failed to create submission: ${e}`);

            return {
                success: false,
                error: e
            };
        }
    }
}