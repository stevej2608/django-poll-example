import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self) -> str:
        return str(self.question_text)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # https://books.agiliq.com/projects/django-admin-cookbook/en/latest/sorting_calculated_fields.html#how-to-enable-sorting-on-calculated-fields

    was_published_recently.admin_order_field = 'pub_date' # type: ignore
    was_published_recently.boolean = True # type: ignore
    was_published_recently.short_description = 'Published recently?'# type: ignore


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.choice_text)
