from celery import shared_task


@shared_task(bind=True)
def validate_question_task(self, question_id):
    from .models import Question

    question = Question.objects.get(id=question_id)
    if question.choices.count() != 4:
        question.delete()
        return 'The question is deleted because it has less than 4 choices.'
    
    correct_choice = question.choices.filter(choice_text=question.correct_chocie)

    if not correct_choice:
        question.delete()
        return 'The question is deleted because the correct choice is not in the choices.'
    
    if correct_choice.count() > 1:
        question.delete()
        return 'The question is deleted because the correct choice is duplicated in the choices.'
    
    return 'The question is valid.'
