import datetime
from django.db import models
from django.utils import timezone
from channels.db import database_sync_to_async

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


    @staticmethod
    async def get_questions():

        def query():
            return Question.objects.filter(pub_date__lte=timezone.now())

        return await database_sync_to_async(query)()

    @staticmethod
    async def get_ordered_questions():

        def query():
            return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

        return await database_sync_to_async(query)()


    @staticmethod
    async def get_question(pk:int):

        def query():
            return Question.objects.filter(pk=pk)


        return await database_sync_to_async(query)()


    async def inc_vote(self, choice: int):
        selected_choice = await database_sync_to_async(self.choice_set.get)(pk=choice)
        selected_choice.votes += 1
        await database_sync_to_async(selected_choice.save)()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.choice_text)
