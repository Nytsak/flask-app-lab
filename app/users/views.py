from flask import (
    request,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    make_response
)

from . import users_bp

VALID_USERS = {
    'admin': 'admin123',
    'user': 'password',
    'oleg': 'nytsak2024'
}


@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("users/hi.html", name=name, age=age)


@users_bp.route("/admin")
def admin():
    to_url = url_for(
        "users_bp.greetings",
        name="administrator",
        age=45,
        _external=True
    )
    print(to_url)
    return redirect(to_url)


@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in VALID_USERS and VALID_USERS[username] == password:
            session['username'] = username
            flash('Ви успішно увійшли в систему!', 'success')
            return redirect(url_for('users_bp.profile'))
        else:
            flash('Невірне ім\'я користувача або пароль!', 'danger')
            return redirect(url_for('users_bp.login'))

    return render_template("users/login.html")


@users_bp.route("/profile")
def profile():
    if 'username' not in session:
        flash(
            'Будь ласка, увійдіть в систему для доступу до профілю!',
            'warning'
        )
        return redirect(url_for('users_bp.login'))

    username = session['username']
    cookies = {key: value for key, value in request.cookies.items()
               if key not in ['session']}

    color_scheme = request.cookies.get('color_scheme', 'light')

    return render_template(
        "users/profile.html",
        username=username,
        cookies=cookies,
        color_scheme=color_scheme
    )


@users_bp.route("/logout")
def logout():
    session.pop('username', None)
    flash('Ви успішно вийшли з системи!', 'info')
    return redirect(url_for('users_bp.login'))


@users_bp.route("/add_cookie", methods=['POST'])
def add_cookie():
    if 'username' not in session:
        flash('Будь ласка, увійдіть в систему!', 'warning')
        return redirect(url_for('users_bp.login'))

    key = request.form.get('cookie_key')
    value = request.form.get('cookie_value')
    max_age = request.form.get('cookie_max_age', type=int)

    if key and value:
        response = make_response(redirect(url_for('users_bp.profile')))
        if max_age:
            response.set_cookie(key, value, max_age=max_age)
        else:
            response.set_cookie(key, value)
        flash(f'Кукі "{key}" успішно додано!', 'success')
        return response
    else:
        flash('Заповніть всі поля!', 'danger')
        return redirect(url_for('users_bp.profile'))


@users_bp.route("/delete_cookie", methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        flash('Будь ласка, увійдіть в систему!', 'warning')
        return redirect(url_for('users_bp.login'))

    key = request.form.get('cookie_key')

    if key:
        response = make_response(redirect(url_for('users_bp.profile')))
        response.delete_cookie(key)
        flash(f'Кукі "{key}" успішно видалено!', 'success')
        return response
    else:
        flash('Вкажіть ключ кукі для видалення!', 'danger')
        return redirect(url_for('users_bp.profile'))


@users_bp.route("/delete_all_cookies", methods=['POST'])
def delete_all_cookies():
    if 'username' not in session:
        flash('Будь ласка, увійдіть в систему!', 'warning')
        return redirect(url_for('users_bp.login'))

    response = make_response(redirect(url_for('users_bp.profile')))

    for key in request.cookies.keys():
        if key not in ['session']:
            response.delete_cookie(key)

    flash('Всі кукі успішно видалено!', 'success')
    return response


@users_bp.route("/set_color/<scheme>")
def set_color(scheme):
    if scheme not in ['light', 'dark']:
        scheme = 'light'

    response = make_response(redirect(url_for('users_bp.profile')))
    response.set_cookie('color_scheme', scheme, max_age=60 * 60 * 24 * 365)
    flash(f'Кольорову схему змінено на "{scheme}"!', 'info')
    return response
