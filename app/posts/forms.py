from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    DateTimeLocalField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField(
        'Заголовок',
        validators=[
            DataRequired(message='Заголовок обов\'язковий'),
            Length(
                min=1,
                max=150,
                message='Заголовок має бути від 1 до 150 символів'
            )
        ]
    )

    content = TextAreaField(
        'Контент',
        validators=[
            DataRequired(message='Контент обов\'язковий')
        ]
    )

    enabled = BooleanField('Активний пост', default=True)

    publish_date = DateTimeLocalField(
        'Дата публікації',
        format='%Y-%m-%dT%H:%M',
        default=datetime.utcnow,
        validators=[DataRequired(message='Дата публікації обов\'язкова')]
    )

    category = SelectField(
        'Категорія',
        choices=[
            ('news', 'Новини'),
            ('publication', 'Публікація'),
            ('tech', 'Технології'),
            ('other', 'Інше')
        ],
        default='other'
    )

    submit = SubmitField('Зберегти')
