import datetime

from django.db import models

from lms.models.student import Student
from lms.models.teacher import Teacher


class EncouragementType(models.Model):
    encouragement_type = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.encouragement_type)

    class Meta:
        verbose_name = 'Encouragement Type'
        verbose_name_plural = 'Encouragement Types'


class Encouragement(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING)
    reason = models.CharField(max_length=200)
    encouragement_type = models.ForeignKey(EncouragementType, models.DO_NOTHING)
    date = models.DateField(default=datetime.date.today)
    teacher = models.ForeignKey(Teacher, models.DO_NOTHING)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.student)}, ' \
               f'TeacherID = {str(self.teacher)}\n' \
               f'Type = {str(self.encouragement_type)}\n' \
               f'Date = {str(self.date)}'

    class Meta:
        verbose_name = 'Encouragement Journal'
        verbose_name_plural = 'Encouragement Journal'
