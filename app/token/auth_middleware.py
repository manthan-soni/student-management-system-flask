'''
Authorization middleware for authenticate if user is already logged in or authorized user or not.
'''

from functools import wraps
import jwt
from flask import request, redirect, session, flash
from app.model.auth import Profile
from app.extensions.db import app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = ""
        token = request.cookies.get('Authorization')
        print(token)
        if not token:
            return redirect('/login')
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            with app.app_context():
                current_user = Profile.query.filter_by(
                    username=data['username']).first()

        except Exception as ex:
            print(ex)

        # if current_user != "":
        return f(*args, **kwargs)
        # else:
        #     flash("Session expire login again")
        #     return redirect('/login')

    return decorated


def token_already_exist(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('Authorization')
        if not token:
            return f(*args, **kwargs)
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            if data:
                return redirect('/')
        except Exception as ex:
            print(ex)
            return f(*args, **kwargs)

        return f(*args, **kwargs)

    return decorated
