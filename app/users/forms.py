from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    PasswordField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Regexp
)


class ContactForm(FlaskForm):
    name = StringField(
        'Ім\'я',
        validators=[
            DataRequired(message='Це поле є обов\'язковим'),
            Length(min=4, max=10, message='Ім\'я має бути від 4 до 10 символів')
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Це поле є обов\'язковим'),
            Email(message='Невірний формат email')
        ]
    )

    phone = StringField(
        'Телефон',
        validators=[
            DataRequired(message='Це поле є обов\'язковим'),
            Regexp(
                r'^380\d{9}$',
                message='Формат телефону: 380XXXXXXXXX (12 цифр)'
            )
        ]
    )

    subject = SelectField(
        'Тема',
        choices=[
            ('', 'Оберіть тему'),
            ('general', 'Загальне питання'),
            ('support', 'Технічна підтримка'),
            ('feedback', 'Відгук'),
            ('cooperation', 'Співпраця'),
            ('other', 'Інше')
        ],
        validators=[
            DataRequired(message='Оберіть тему повідомлення')
        ]
    )

    message = TextAreaField(
        'Повідомлення',
        validators=[
            DataRequired(message='Це поле є обов\'язковим'),
            Length(
                max=500,
                message='Повідомлення не може бути довшим за 500 символів'
            )
        ]
    )

    submit = SubmitField('Відправити')


class LoginForm(FlaskForm):
    username = StringField(
        'Ім\'я користувача',
        validators=[
            DataRequired(message='Це поле є обов\'язковим')
        ]
    )

    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message='Це поле є обов\'язковим'),
            Length(
                min=4,
                max=10,
                message='Пароль має бути від 4 до 10 символів'
            )
        ]
    )

    remember = BooleanField('Запам\'ятати мене')

    submit = SubmitField('Увійти')
