import pytest

from page_objects.pvpoke_page import *
from helpers.generate_pokemon_list import *
from page_objects.battle_page import BattlePage


class TestBattle:

    @pytest.fixture()
    def training_battle_page(self, page) -> PvPokePage:
        pokemon_page = PvPokePage(page)
        pokemon_page.go_to_site()
        return pokemon_page

    def test_battle(self, training_battle_page):
        picked_pokemon = pick_random_five_pokemon()
        training_battle_page.select_pokemon(pokemon_list=picked_pokemon)
        training_battle_page.select_league()
        training_battle_page.select_difficulty()
        training_battle_page.click_auto_tap()
        battle_page = training_battle_page.click_battle()
        battle_page.is_battle_still_occurring()
        assert battle_page.did_we_win()
