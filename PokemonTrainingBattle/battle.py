import pytest

from helpers.go_to_pvpoke import PvPokePage
from helpers.generate_pokemon_list import pick_random_five_pokemon


class TestBattle:

    @pytest.fixture()
    def go_to_webpage(self, page) -> PvPokePage:
        pokemon_page = PvPokePage(page)
        p = pokemon_page.go_to_site()
        picked_pokemon = pick_random_five_pokemon()
        return picked_pokemon

    def test_battle(self, go_to_webpage):

        print("1")
