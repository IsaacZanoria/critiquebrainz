from flask import Blueprint, request, redirect, render_template, url_for, session, flash
from flask_login import login_user, logout_user, login_required
from flask_babel import gettext
from critiquebrainz.frontend.login import login_forbidden, provider

login_bp = Blueprint('login', __name__)


@login_bp.route('/')
@login_forbidden
def index():
    return render_template('login/login.html')


@login_bp.route('/musicbrainz')
@login_forbidden
def musicbrainz():
    session['next'] = request.args.get('next')
    force_prompt = 'force' if request.args.get('force') else 'auto'
    return redirect(provider.get_authentication_uri(force_prompt))


@login_bp.route('/musicbrainz/post')
@login_forbidden
def musicbrainz_post():
    """Callback endpoint."""
    if provider.validate_post_login():
        user = provider.get_user()
        if not user.mb_refresh_token:
            # Making sure that we have refresh token for this user
            return redirect(url_for('.musicbrainz', force=True))
        login_user(user)
        next = session.get('next')
        if next:
            return redirect(next)
    else:
        flash(gettext("Login failed."), 'error')
    return redirect(url_for('frontend.index'))


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('frontend.index'))
