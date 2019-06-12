import os
import time

from flask import Blueprint, render_template, flash, request, redirect, \
    url_for, Response
from flask.ext.login import login_user, logout_user, login_required

from hello_up.extensions import cache
from hello_up.forms import LoginForm
from hello_up.models import User

from hello_up.utils import unsafe_execute_command

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    platform = "test"
    platform = unsafe_execute_command(["uname -s"])
    return render_template('index.html', platform=platform)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for(".home"))

    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".home"))


@main.route("/restricted")
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200

log_file_path = "/var/log/app.stdout.log"  # "/var/log/system.log"


def follow(thefile):
    thefile.seek(0, os.SEEK_END)  # End-of-file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)  # Sleep briefly
            continue
        yield line


def watch_logs(log_file_path):
    with open(log_file_path, 'r') as log_file:
        loglines = follow(log_file)
        for line in loglines:
            # print(line, end='')
            yield line


@main.route('/logs')
def logs():
    global log_file_path
    return Response(watch_logs(log_file_path))  # , mimetype='text/csv')


@main.route('/env')
def env():
    env = os.environ
    return render_template("envs.html", env=env)
