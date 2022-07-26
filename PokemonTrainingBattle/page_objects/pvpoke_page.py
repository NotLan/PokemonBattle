from time import sleep

import logging

from plugins.playwright import AbstractPage
from pyotp import random


class PvPokePage(AbstractPage):
    add_pokemon_button = 'text=+ Add Pokemon >> nth=0'
    add_selected_pokemon_button = '.save-poke'
    search_text_field = 'text=Random Swap Select a Pokemon AbomasnowAbomasnow (Mega)Abomasnow ' \
                        '(Shadow)AbraAbra >> [placeholder="Search name"]'
    opponent_search_text_field = '[placeholder="Search name"] >> nth=1'
    pick_pokemon_dropdown = 'text=Random Swap Select a Pokemon AbomasnowAbomasnow (Mega)Abomasnow ' \
                            '(Shadow)AbraAbra >> select >> nth=0'
    pokemon_selection_dropdown = 'text=Random Swap Select a Pokemon AbomasnowAbomasnow ' \
                                 '(Mega)Abomasnow (Shadow)AbraAbra >> select >> nth=0'
    battle_button = 'button:has-text("Battle")'
    pick_opponent_dropdown = 'div:nth-child(2) > .poke-select'
    league_dropdown = '.league-cup-select'
    difficulty_dropdown = '.difficulty-select'
    auto_tap_button = 'text=Autotap >> nth=0'
    no_shields = '.option >> nth=0'
    no_oppenent_shield = 'div:nth-child(2) > .poke-stats > .options > .shield-section > .form-group > div >> nth=0'
    random_button = 'text=Random >> nth=1'
    faint = '.item.faint'
    outcome_section = '//div[contains(@class, "summary section white")]'

    url = 'https://pvpoke.com/battle/'

    def go_to_site(self):
        self.navigate()
        return PvPokePage

    def click_opponent_random(self):
        self.page.click(self.random_button)

    def click_no_opponent_shield(self):
        self.page.click(self.no_oppenent_shield)

    def click_no_shields(self):
        self.page.click(self.no_shields)

    def click_auto_tap(self):
        self.page.click(self.auto_tap_button)

    def select_league(self):
        self.page.type(self.league_dropdown, "GO Battle League (Great)", delay=5)

    def click_battle(self):
        self.page.click(self.battle_button)

    def click_add_selected_pokemon(self):
        self.page.click(self.add_selected_pokemon_button)

    def click_add_a_pokemon(self):
        self.page.click(self.add_pokemon_button)

    def select_users_pokemon(self, pokemon_list):
        self.page.type(self.search_text_field, f"{pokemon_list[0]}", delay=5)

    def select_opponents_pokemon(self, pokemon_list):
        self.page.type(self.opponent_search_text_field, f"{pokemon_list[1]}", delay=5)

    def select_difficulty(self):
        difficulty_list = [
            "Novice",
            "Rival",
            "Elite",
            "Champion"
        ]
        self.page.type(self.difficulty_dropdown, random.choice(difficulty_list), delay=5)

    def pull_stats(self):
        while self.page.text_content(self.outcome_section) is None:
            sleep(1)

        pokemon_names = \
        self.page.query_selector_all('//table[contains(@class, "stats-table")]')[3].query_selector_all("//tr")[
            0].text_content().split()[0:2]
        pokemon_battle_ratings = \
            self.page.query_selector_all('//table[contains(@class, "stats-table")]')[3].query_selector_all("//tr")[
                1].inner_text().split()[2:4]
        pokemon_total_damage = \
            self.page.query_selector_all('//table[contains(@class, "stats-table")]')[3].query_selector_all("//tr")[
                2].inner_text().split()[2:4]
        pokemon_fast_move_damage = \
            self.page.query_selector_all('//table[contains(@class, "stats-table")]')[3].query_selector_all("//tr")[
                3].inner_text().split('\t')[1:3]
        pokemon_charged_move_damage = \
            self.page.query_selector_all('//table[contains(@class, "stats-table")]')[3].query_selector_all("//tr")[
                4].inner_text().split('\t')[1:3]
        pokemon_turns_to_first_charged_move = \
            self.page.query_selector_all('//table[contains(@class, "stats-table")]')[3].query_selector_all("//tr")[
                6].inner_text().split('\t')[1:3]
        pokemon_energy_gained = \
            self.page.query_selector_all('//table[contains(@class, "stats-table")]')[3].query_selector_all("//tr")[
                7].inner_text().split()[2:4]
        pokemon_energy_used = \
            self.page.query_selector_all('//table[contains(@class, "stats-table")]')[3].query_selector_all("//tr")[
                8].inner_text().split()[2:4]
        pokemon_energy_remaining = \
            self.page.query_selector_all('//table[contains(@class, "stats-table")]')[3].query_selector_all("//tr")[
                9].inner_text().split()[2:4]
        pokemon_stats = {}

        number_of_pokemon = 0
        while number_of_pokemon != 2:
            pokemon_stats[pokemon_names[number_of_pokemon]] = {
                "Battle Rating": pokemon_battle_ratings[number_of_pokemon],
                "Total Damage": pokemon_total_damage[number_of_pokemon],
                "Fast Move Damage": pokemon_fast_move_damage[number_of_pokemon],
                "Charged Move Damage": pokemon_charged_move_damage[number_of_pokemon],
                "Turns to first charged move": pokemon_turns_to_first_charged_move[number_of_pokemon],
                "Energy Gained": pokemon_energy_gained[number_of_pokemon],
                "Energy Used": pokemon_energy_used[number_of_pokemon],
                "Energy Remaining": pokemon_energy_remaining[number_of_pokemon]
            }
            number_of_pokemon += 1

        return pokemon_stats

    def who_won(self, picked_pokemon):
        outcome = self.page.text_content(self.outcome_section)
        logger = logging.getLogger(__name__)

        if "wins" in outcome:
            logger.info(f"\n {picked_pokemon[0]} won!")
            logger.info(f"\n {picked_pokemon[1]} lost :( ")
            return picked_pokemon[0], picked_pokemon[1]
        else:
            logger.info(f"\n {picked_pokemon[1]} won!")
            logger.info(f"\n {picked_pokemon[0]} lost :(")
            return picked_pokemon[1], picked_pokemon[0]

    def update_winner_and_loser(self, statistics, winner, loser):
        if statistics[f"{winner}"].get("Wins") is None:
            statistics[f"{winner}"]["Wins"] = 1
        else:
            statistics.get(f"{winner}")["Wins"] += 1

        if statistics[f"{loser}"].get("Losses") is None:
            statistics[f"{loser}"]["Losses"] = -1
        else:
            statistics.get(f"{loser}")["Losses"] -= 1

