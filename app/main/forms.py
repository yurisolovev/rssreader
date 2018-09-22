from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, HiddenField, StringField
from wtforms.validators import DataRequired, URL
from app.models import RSSChanel, Theme


class RSSChanelAddForm(FlaskForm):
    chanel = SelectField('Добавить канал', coerce=int)
    type = HiddenField('Hidden', default='add')
    submit = SubmitField('Добавить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chanel.choices = [(chanel.id, chanel.chanelname)
                                for chanel in RSSChanel.query.order_by(RSSChanel.chanelname).all()]


class RSSChanelRemForm(FlaskForm):
    chanel = SelectField('Отписаться от канала', coerce=int)
    type = HiddenField('Hidden', default='rem')
    submit = SubmitField('Отписаться')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chanel.choices = [(chanel.chanel.id, chanel.chanel.chanelname)
                                for chanel in user.chanels.filter_by(follower_id=user.id).all()]


class RSSChanelAdminForm(FlaskForm):
    reference = StringField('Адрес RSS канала', validators=[DataRequired(), URL(message='Некорректный URL')],
                            render_kw={"placeholder": "http://"})
    chanelname = StringField('Название канала', validators=[DataRequired()],
                             render_kw={"placeholder": "Название канала..."})
    type = HiddenField('Hidden', default='admin')
    submit = SubmitField('Сохранить')


class ThemeChangeForm(FlaskForm):
    theme = SelectField('Выбрать тему', coerce=int)
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme.choices = [(theme.id, theme.themename)
                                for theme in Theme.query.all()]
