from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main import main
from app.models import RSSChanel
from app.rss import feed_reader, feeds_reader
from .forms import RSSChanelAddForm, RSSChanelRemForm, RSSChanelAdminForm, ThemeChangeForm
from app.themes import preview_image


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    chanels = current_user.chanels.filter_by(follower_id=current_user.id).all()
    form_add = RSSChanelAddForm()
    form_rem = RSSChanelRemForm(current_user)
    form_admin = RSSChanelAdminForm()

    if form_add.validate_on_submit() and request.form.get('type') == 'add':
        chanel = RSSChanel.query.get(form_add.chanel.data)
        if not current_user.is_following(chanel):
            current_user.follow(chanel)
            flash("Вы подписались на канал <{}>".format(chanel.chanelname))
        else:
            flash("Вы уже подписаны на канал <{}>".format(chanel.chanelname))
        return redirect(url_for('main.settings'))

    if form_rem.validate_on_submit() and request.form.get('type') == 'rem':
        chanel = RSSChanel.query.get(form_add.chanel.data)
        current_user.unfollow(chanel)
        flash("Вы отписались от канала <{}>".format(chanel.chanelname))
        return redirect(url_for('main.settings'))

    if form_admin.validate_on_submit() and request.form.get('type') == 'admin':
        if RSSChanel.query.filter_by(reference=form_admin.reference.data).first()\
                or RSSChanel.query.filter_by(chanelname=form_admin.chanelname.data).first():
            flash('Канал с таким названием или адресом уже существует.')
        else:
            chanel = RSSChanel(reference=form_admin.reference.data,
                               chanelname=form_admin.chanelname.data)
            db.session.add(chanel)
            db.session.commit()
            flash("Канал <{}> сохранен в базе данных.".format(form_admin.chanelname.data))
        return redirect(url_for('main.settings'))

    return render_template('settings.html', chanels=chanels, form_add=form_add,
                           form_rem=form_rem, form_admin=form_admin)


@main.route('/news/chanel/<chanelname>')
@login_required
def chanel(chanelname):
    chanels = current_user.chanels.filter_by(follower_id=current_user.id).all()
    page = request.args.get('page', 1, type=int)
    if chanelname != 'all':
        active_chanel = RSSChanel.query.filter_by(chanelname=chanelname).first()
        news, pagination = feed_reader(active_chanel.reference, page)
    else:
        news, pagination = feeds_reader([chanel.chanel.reference for chanel in chanels], page)
        active_chanel = None
    return render_template('news.html', chanels=chanels, active_chanel=active_chanel,
                           pagination=pagination, news=news)


@main.route('/themes', methods=['GET', 'POST'])
@login_required
def themes():
    user_theme = current_user.current_theme.themename
    form = ThemeChangeForm()
    if form.validate_on_submit():
        user = current_user._get_current_object()
        user.theme = form.theme.data
        db.session.add(user)
        db.session.commit()
        flash('Тема оформления <{}> успешно установлена.'.format(current_user.current_theme.themename))
        return redirect(url_for('main.themes'))

    return render_template('themes.html', form=form, user_theme=user_theme,
                           active_image=preview_image[0], images=preview_image[1:],
                           indicators=len(preview_image[1:]))
