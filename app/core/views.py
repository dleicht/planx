# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import redirect, render_template, render_template_string, Blueprint, g
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from flask.ext.babel import Babel
from app import app, db
from app.core.models import UserProfileForm

core_blueprint = Blueprint('core', __name__, url_prefix='/')
babel = Babel(app)

# Enabling localization
@app.before_request
def before():
        if request.view_args and 'lang_code' in request.view_args:
            if request.view_args['lang_code'] not in ('es', 'en'):
                return abort(404)
            else:
                g.current_lang = request.view_args['lang_code']
                request.view_args.pop('lang_code')

@babel.localeselector
def get_locale():
    return g.get('current_lang', 'de')

# The Home page is accessible to anyone
@core_blueprint.route('')
def home_page():
    return render_template('core/home_page.html', lang_code='de')

# The FAQ page is accessible to anyone
@core_blueprint.route('faq')
def faq_page():
    return render_template('core/faq.html')


# The User page is accessible to authenticated users (users that have logged in)
@core_blueprint.route('user')
@login_required  # Limits access to authenticated users
def user_page():
    return render_template('core/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@core_blueprint.route('admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('core/admin_page.html')


@core_blueprint.route('user/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('core.home_page'))

    # Process GET or invalid POST
    return render_template('core/user_profile_page.html',
                           form=form)


# Register blueprint
app.register_blueprint(core_blueprint)
