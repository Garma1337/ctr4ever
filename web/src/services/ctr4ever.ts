import axios, { AxiosInstance } from "axios";

export default class Ctr4Ever {
    protected client: AxiosInstance;

    public constructor(apiEndpoint: string) {
        this.client = axios.create({
            baseURL: apiEndpoint,
            timeout: 5000,
            validateStatus: (status) => status >= 200 && status < 300
        });
    }

    public async findCountries(): Promise<any> {
        try {
            const response = await this.client.get('/countries');
            return response.data['countries'];
        } catch (e) {
            console.log(`Failed to fetch country list: ${e}`);
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