from django.urls import reverse

from core.utils import get_short_gameline_name


class HumanUrlBlock:
    @staticmethod
    def get_gameline_for_url(gameline):
        g = get_short_gameline_name(gameline)
        if g:
            g += ":"
        return g

    def get_full_update_url(self):
        return reverse(
            f"characters:{self.get_gameline_for_url(self.gameline)}update:{self.type}_full",
            kwargs={"pk": self.pk},
        )

    def get_update_url(self):
        return reverse(
            f"characters:{self.get_gameline_for_url(self.gameline)}update:{self.type}",
            kwargs={"pk": self.pk},
        )

    @classmethod
    def get_full_creation_url(cls):
        return reverse(f"characters:{cls.get_gameline_for_url(cls.gameline)}create:{cls.type}_full")

    @classmethod
    def get_creation_url(cls):
        return reverse(f"characters:{cls.get_gameline_for_url(cls.gameline)}create:{cls.type}")
