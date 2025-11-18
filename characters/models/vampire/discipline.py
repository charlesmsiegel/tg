from characters.models.core.statistic import Statistic


class Discipline(Statistic):
    """
    Represents a Vampire Discipline (supernatural power).
    Examples: Celerity, Fortitude, Potence, Dominate, etc.
    """

    type = "discipline"

    class Meta:
        verbose_name = "Discipline"
        verbose_name_plural = "Disciplines"
