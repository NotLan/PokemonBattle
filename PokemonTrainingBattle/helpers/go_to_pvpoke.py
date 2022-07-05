from ottermation.plugins.playwright import AbstractPage


class PvPokePage(AbstractPage):

    url = 'https://pvpoke.com/train/'

    def go_to_site(self):
        """

        :return:
        """
        return self.page.goto(self.url, wait_until="networkidle")
