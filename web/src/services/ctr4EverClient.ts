import axios, { AxiosInstance } from "axios";

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

    public async findCountries(countryName: string | null = null): Promise<any> {
        try {
            const response = await this.client.get('/countries', {params: {countryName}});
            return response.data['countries'];
        } catch (e) {
            console.log(`Failed to fetch country list: ${e}`);
            return [];
        }
    }

    public async findPlayers(
        country_id: Number | null = null,
        name: string | null = null,
        email: string | null = null,
        active: boolean | null = null,
    ): Promise<any> {
        try {
            const response = await this.client.get('/players', {params: {country_id, name, email, active}});
            return response.data['players'];
        } catch (e) {
            console.log(`Failed to fetch player list: ${e}`);
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
}