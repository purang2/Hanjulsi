from django import forms 
from pybo.models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question #사용할 모델 
        fields = ['subject', 'content'] # QuestionForm에서 사용할 Question 모델의 속성 


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }
    