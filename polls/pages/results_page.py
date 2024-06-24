from django.urls import reverse
from reactpy import component, html
from reactpy_router import use_params, link

from ..models import Question, Choice

from .common import use_query, LoadingException
from .page_404 import Page_404


@component
def results():

    @component
    def ChoiceVote(choice: Choice):

        def pluralize(count):
            return "s" if count != 1 else ""

        return html.li({'class_name': 'list-group-item'},
            f"{choice.choice_text}",
            html.span({'class_name': 'badge badge-primary float-right'}, f"{choice.votes} vote{pluralize(choice.votes)}")
        )

    try:

        params = use_params()
        qs = use_query(Question.get_questions)
        pk = int(params['pk'])
        question = qs.data[pk - 1]


        return html.div(
            html.h1({'class_name': 'mb-5 text-center'}, f"{question.question_text}"),
            html.ul({'class_name': 'results list-group mb-5'},

                [ChoiceVote(choice) for choice in question.choice_set.all()],

            ),

            html.div({'class_name':'btn-group'},
                link("Back To Polls", to=reverse('polls:index'), class_name='btn btn-secondary  mx-1'),
                link("Vote again?", to=reverse("polls:detail", kwargs={'pk': pk}), class_name='btn btn-primary'),
            ),

        )
    except LoadingException as ex:
        return html.h2(str(ex))
    except Exception as error:
        return Page_404(str(error))
