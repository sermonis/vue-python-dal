from django.db import models


class Milfaculty(models.Model):
    milfaculty = models.CharField(primary_key=True, max_length=10)

    def __str__(self):
        return str(self.milfaculty)

    class Meta:
        verbose_name = 'Military Faculty'
        verbose_name_plural = 'Military Faculties'


class Milgroup(models.Model):
    milgroup = models.DecimalField(primary_key=True,
                                   max_digits=4,
                                   decimal_places=0)
    milfaculty = models.ForeignKey(Milfaculty, models.DO_NOTHING)
    weekday = models.DecimalField(max_digits=1, decimal_places=0)

    def __str__(self):
        return f'{str(self.milgroup)}, {str(self.milfaculty)}'

    class Meta:
        verbose_name = 'Military Group'
        verbose_name_plural = 'Military Groups'
