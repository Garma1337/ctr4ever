import {create, StateCreator } from 'zustand';
import { devtools } from 'zustand/middleware';

export type Store<T extends object> = StateCreator<T, [['zustand/devtools', never]], [], T>;

export type AppState = {
    apiEndpoint: string;
    setApiEndpoint: (apiEndpoint: string) => void;
    countries: any[];
    setCountries: (countries: any[]) => void;
    characters: any[];
    setCharacters: (characters: any[]) => void;
    tracks: any[];
    setTracks: (tracks: any[]) => void;
    categories: any[];
    setCategories: (categories: any[]) => void;
    engine_styles: any[];
    setEngineStyles: (engine_styles: any[]) => void;
    game_versions: any[];
    setGameVersions: (game_versions: any[]) => void;
    platforms: any[];
    setPlatforms: (platforms: any[]) => void;
    rulesets: any[];
}

const createStore: Store<AppState> = (set) => ({
    apiEndpoint: 'http://localhost:5000/api',
    setApiEndpoint: (apiEndpoint: string) => set(() => ({ apiEndpoint }), false, 'setApiEndpoint'),
    countries: [],
    setCountries: (countries: any[]) => set(() => ({ countries }), false, 'setCountries'),
    characters: [],
    setCharacters: (characters: any[]) => set(() => ({ characters }), false, 'setCharacters'),
    tracks: [],
    setTracks: (tracks: any[]) => set(() => ({ tracks }), false, 'setTracks'),
    categories: [],
    setCategories: (categories: any[]) => set(() => ({ categories }), false, 'setCategories'),
    engine_styles: [],
    setEngineStyles: (engine_styles: any[]) => set(() => ({ engine_styles }), false, 'setEngineStyles'),
    game_versions: [],
    setGameVersions: (game_versions: any[]) => set(() => ({ game_versions }), false, 'setGameVersions'),
    platforms: [],
    setPlatforms: (platforms: any[]) => set(() => ({ platforms }), false, 'setPlatforms'),
    rulesets: [],
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
