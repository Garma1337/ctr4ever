#!/bin/bash

echo "Installing master data ..."

flask --app ctr4ever installer categories --filename "install/categories.json"
flask --app ctr4ever installer characters --filename "install/characters.json"
flask --app ctr4ever installer countries --filename "install/countries.json"
flask --app ctr4ever installer engine_styles --filename "install/engine_styles.json"
flask --app ctr4ever installer game_versions --filename "install/game_versions.json"
flask --app ctr4ever installer platforms --filename "install/platforms.json"
flask --app ctr4ever installer rulesets --filename "install/rulesets.json"
flask --app ctr4ever installer tracks --filename "install/tracks.json"

echo "Successfully installed master data."
