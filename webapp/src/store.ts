import {create, StateCreator } from 'zustand';
import { devtools } from 'zustand/middleware';

export type Store<T extends object> = StateCreator<T, [['zustand/devtools', never]], [], T>;

export type AppState = {
    apiEndpoint: string;
    setApiEndpoint: (apiEndpoint: string) => void;
    jwt: string;
    setJwt: (jwt: string) => void;
    currentUser: any;
    setCurrentUser: (currentUser: any) => void;
    countries: any[];
    setCountries: (countries: any[]) => void;
    characters: any[];
    setCharacters: (characters: any[]) => void;
    tracks: any[];
    setTracks: (tracks: any[]) => void;
    categories: any[];
    setCategories: (categories: any[]) => void;
    engineStyles: any[];
    setEngineStyles: (engine_styles: any[]) => void;
    gameVersions: any[];
    setGameVersions: (game_versions: any[]) => void;
    platforms: any[];
    setPlatforms: (platforms: any[]) => void;
    rulesets: any[];
    setRulesets: (rulesets: any[]) => void;
}

const createStore: Store<AppState> = (set) => ({
    apiEndpoint: 'http://localhost:5000/api',
    setApiEndpoint: (apiEndpoint: string) => set(() => ({ apiEndpoint }), false, 'setApiEndpoint'),
    jwt: '',
    setJwt: (jwt: string) => set(() => ({ jwt }), false, 'setJwt'),
    currentUser: null,
    setCurrentUser: (currentUser: any) => set(() => ({ currentUser }), false, 'setCurrentUser'),
    countries: [],
    setCountries: (countries: any[]) => set(() => ({ countries }), false, 'setCountries'),
    characters: [],
    setCharacters: (characters: any[]) => set(() => ({ characters }), false, 'setCharacters'),
    tracks: [],
    setTracks: (tracks: any[]) => set(() => ({ tracks }), false, 'setTracks'),
    categories: [],
    setCategories: (categories: any[]) => set(() => ({ categories }), false, 'setCategories'),
    engineStyles: [],
    setEngineStyles: (engineStyles: any[]) => set(() => ({ engineStyles }), false, 'setEngineStyles'),
    gameVersions: [],
    setGameVersions: (gameVersions: any[]) => set(() => ({ gameVersions }), false, 'setGameVersions'),
    platforms: [],
    setPlatforms: (platforms: any[]) => set(() => ({ platforms }), false, 'setPlatforms'),
    rulesets: [],
    setRulesets: (rulesets: any[]) => set(() => ({ rulesets }), false, 'setRulesets'),
});

const useStore = create<AppState>()(
  devtools(
    (...storeApi) => ({
      ...createStore(...storeApi),
    }),
    { name: 'sharedStore' },
  ),
);

export default useStore;
