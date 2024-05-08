'''
    Main flask class
'''

import os
import time
import calendar
from datetime import datetime, timedelta, date
from flask import session, redirect, render_template, make_response, flash, request, url_for
import bcrypt
import jwt
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

from app.token.auth_middleware import token_already_exist, token_required
from app.forms.auth import LoginForm, RegistrationForm
from app.forms.teacher import CourseDetails
from app.model.auth import Profile, Course, Enrollments
from app.extensions.db import app,mail
from app.extensions.db import db

# sessions defined
# session['name']
# session['wrong_cred']
# session['user']
# session['user_id']

# file upload
# @app.route('/fileupload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('upload_file',
#                                     filename=filename))
#         else:
#             flash("File not allowed")
#     return render_template('pages/uploadfile.html')

# file upload complete

# Send mail
# @app.route('/sendmail', methods=['GET', 'POST'])
def send_mail(recieptant,course_name):
    '''it will send mail when student enroll in course'''
    msg = Message(
                'Course Enrolled! Start learning now.', 
                sender ='manthan0404soni@gmail.com',
                recipients = [recieptant]
    )
    msg.body = f'Hello {recieptant}, you have successfully enrolled in {course_name}. Happy learning !!!'
    mail.send(msg)
    # flash('Sent')
    return "sent"

# send mail complete
@app.route('/login', methods=['GET', 'POST'])
@token_already_exist
def log_in():
    ''' Login page'''
    if session.get("Authorization"):
        redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        ps1 = password.encode('utf-8')
        try:
            dt = Profile.query.filter_by(username=username).first()
            dt1 = dt.password.encode('utf-8')
            if dt:
                if bcrypt.checkpw(ps1, dt1):
                    token = jwt.encode(
                        {"username": dt.username,
                            'exp': datetime.now() + timedelta(minutes=30)},
                        app.config["SECRET_KEY"],
                        algorithm="HS256"
                    )
                    if dt.designation == "Teacher":
                        response = make_response(redirect('/teacher/'))
                    elif dt.designation == "Student":
                        response = make_response(redirect('/'))
                    # response.headers["Authorization"] = token
                    response.set_cookie("Authorization", token)
                    session['name'] = dt.name
                    session['wrong_cred'] = ""
                    session['user'] = dt.username
                    session['user_id'] = dt.id
                    return response
                else:
                    session['wrong_cred'] = "Please enter correct username and password"
                    return redirect('/login')
            else:
                session['wrong_cred'] = "User not registered"
                return redirect('/login')
        except Exception as ex:
            print(ex)
            session['wrong_cred'] = "User not registered"
            return redirect('login')
    wrong_cred = session.get('wrong_cred')
    return render_template('auth/login.html', form=form, wrong_cred=wrong_cred)

# Register page


@app.route('/register', methods=['GET', 'POST'])
@token_already_exist
def register_user():
    ''' Register user page'''
    if session.get("user"):
        redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        filename=""
        if form.profile_photo.data:
            file = form.profile_photo.data
            utc_time_tuple = time.gmtime()
            utc_timestamp = calendar.timegm(utc_time_tuple)
            fextension = file.filename
            fextension = fextension.split(".")
            filename = str(utc_timestamp)+ "-" + form.username.data + "." + fextension[1]
            # print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return redirect(url_for('upload_file',filename=filename))
        password = form.password.data
        password1 = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=15)
        hashed_password = bcrypt.hashpw(password1, salt)
        try:
            user = Profile(profile_photo=filename, name=form.name.data, designation=form.designation.data,contact_no=form.contact_no.data, username=form.username.data, password=hashed_password,email=form.email.data)
            db.session.add(user)
            db.session.commit()
            # session['name'] = form.name.data
            # session['user'] = form.username.data
            flash('Thanks for registering')
            return redirect('/login')
        except Exception as ex:
            print(ex)
            flash(str(ex))
            redirect('/register')
    return render_template('auth/register.html', form=form)

# Logout Function
@app.route('/logout')
def logout_fun():
    '''Logout func'''
    session.clear()
    response = make_response(redirect('/login'))
    response.delete_cookie("Authorization")
    return response

# =========================================================Student pages=============================================

# Home page
@app.route("/")
@token_required
def main():
    ''' Home page func'''
    user = session.get('name')
    # nonlocal page
    page = "home"
    if user == "":
        return redirect('/login')
    else:
        # print(Profile.query.all())
        return render_template('pages/index.html', user=user, page=page)


@app.route('/blog')
@token_required
def blog():
    ''' about us page func'''
    user = session.get('name')
    # nonlocal page
    page = "blog"
    return render_template('pages/blog.html', user=user, page=page)


@app.route('/contact')
@token_required
def contact_us():
    ''' about us page func'''
    user = session.get('name')
    # nonlocal page
    page = "contact"
    return render_template('pages/contact.html', user=user, page=page)

# offset=0
@app.route('/course',methods=['GET','POST'])
@token_required
def course():
    ''' about us page func'''
    user = session.get('name')

    page = "course"
    offset = 0

    next = request.args.get('next')
    prev = request.args.get('prev')
    word = request.args.get('word')

    if next:
        offset = offset + 4
    elif prev and offset != 0:
        offset = offset - 4

    if word:
        worddata = Course.query.msearch(word)
    else:
        worddata = ""
    totalcount = len(Course.query.all())    
    courses = Course.query.limit(4).offset(offset).all()
    
    return render_template('pages/course.html', user=user, page=page, courses=courses, word = word, worddata = worddata,offset = offset,totalcount = totalcount)


@app.route('/coursePlay', methods=['POST'])
@token_required
def course_play():
    ''' about us page func'''
    data = request.form.to_dict()
    print(data)
    user = session.get('name')
    # nonlocal page
    page = "course"
    # courses = Course.query.all()
    return render_template('pages/coursePlay.html', user=user, page=page, link=data['link'], val=data['cid'], name=data['coursename'])


@app.route('/cancelcourse', methods=['POST'])
@token_required
def cancel_course():
    '''Cancel course'''
    data = request.form.to_dict()
    sid = session.get('user_id')
    val = db.session.execute(db.select(Enrollments).filter_by(
        cid=data['cid'], sid=sid)).scalar_one()
    val.cancelled = 1
    val.cancelled_reason = data['reason']
    db.session.commit()
    return redirect('/profile')


@app.route('/enrollcourse', methods=['GET'])
@token_required
def enroll_course():
    ''' about us page func'''
    val = request.args.get('id')
    user_id = session.get('user_id')
    try:
        course_details = Course.query.filter_by(id=val).one_or_none()
        recieptant = Profile.query.filter_by(id=user_id).one_or_none()
        enrollments = Enrollments.query.filter_by(cid=course_details.id,sid=user_id).one_or_none()
        if enrollments:
            if enrollments.id != None:
                raise Exception("You are already enrolled in that course !!!")
        if date.today() > course_details.end_date:
            flash("Sorry, course is over !!! you cannot enroll now")
        # flash(cDate)
        elif date.today() < course_details.start_date:
            flash("Sorry, course is not yet started !!! you cannot enroll now")
        else:
            enrol = Enrollments(cid=val, sid=user_id, enroll_date=date.today())
            db.session.add(enrol)
            db.session.commit()
            mailsent = send_mail(recieptant.email,course_details.name)
            if mailsent:
                flash("Enrolled successfully")
            else:
                print(mailsent)
    except Exception as ex:
        flash(str(ex))
    return redirect('/course')


@app.route('/teacher')
@token_required
def teacher():
    ''' teacher page func'''
    user = session.get('name')
    # nonlocal page
    page = "teacher"
    return render_template('pages/teacher.html', user=user, page=page)


@app.route('/single')
@token_required
def single():
    '''single page func'''
    user = session.get('name')
    # nonlocal page
    page = "blog"
    return render_template('pages/single.html', user=user, page=page)

# About us page


@app.route('/about')
@token_required
def about_us():
    ''' about us page func'''
    user = session.get('name')
    # nonlocal page
    page = "about"
    return render_template('pages/about.html', user=user, page=page)

# Profile page


@app.route('/profile')
@token_required
def user_profile():
    ''' profile page func '''
    name = session.get('name')
    user = session.get('user')
    user_id = session.get('user_id')
    # nonlocal page
    page = "profile"
    enrolledC = []
    coursedetails = []
    dt = Profile.query.filter_by(username=user).first()
    dt1 = Enrollments.query.filter_by(sid=user_id, cancelled=0).all()
    for i in dt1:
        enrolledC.append(i.cid)
    # print("data", dt)
    for i in enrolledC:
        dt1 = Course.query.filter_by(id=i).one_or_none()
        tname = Profile.query.filter_by(id=dt1.teacher_id).one_or_none()
        coursedetails.append(
            [dt1.id, dt1.name, dt1.description, str(dt1.start_date), str(dt1.end_date), dt1.link, tname.name])

    return render_template('pages/profile.html', data=dt, user=name, page=page, course=coursedetails)


@app.errorhandler(404)
def not_found(error):
    ''' Error func '''
    print(error)
    return render_template('pages/error.html')


# =========================================================Student pages=============================================


@app.route('/teacher/', methods=['GET'])
@token_required
def teacher_home():
    '''teacher home page func '''
    name = session.get('name')
    user = session.get('user')
    user_id = session.get('user_id')
    page = "home"
    return render_template('teacher/teacher_index.html', user=name, page=page)


@app.route('/teacher/course', methods=['GET'])
@token_required
def teacher_course():
    ''' teacher course page func'''
    user = session.get('name')
    user_id = session.get('user_id')
    # nonlocal page
    page = "course"
    courses = Course.query.filter_by(teacher_id=user_id).all()
    return render_template('teacher/course.html', user=user, page=page, courses=courses)


@app.route('/teacher/addcourse', methods=['GET', 'POST'])
@token_required
def teacher_add_course():
    '''teacher add course page func'''
    user = session.get('name')
    user_id = session.get('user_id')
    # nonlocal page
    page = "course"
    form = CourseDetails()
    if form.validate_on_submit():
        try:
            course = Course(id=form.id.data, name=form.name.data,
                            description=form.description.data, start_date=form.start_date.data, end_date=form.end_date.data, teacher_id=user_id, link=form.link.data)
            db.session.add(course)
            db.session.commit()
        except Exception as ex:
            print(ex)
        return redirect('/teacher/course')
    return render_template('teacher/addcourse.html', user=user, page=page, form=form)


@app.route('/teacher/coursedetails', methods=['GET', 'POST'])
@token_required
def teacher_course_details():
    ''' teacher course details page func'''
    val = request.args.get('id')
    user = session.get('name')
    page = "course"
    data = Course.query.filter_by(id=val).one_or_none()
    total = len(data.enrollment)
    for i in data.enrollment:
        print(i.profile.name)
    form = CourseDetails(id=data.id, name=data.name,
                         description=data.description, start_date=data.start_date, end_date=data.end_date, link=data.link)
    if form.validate_on_submit():
        try:
            val = db.session.execute(db.select(Course).filter_by(
                id=form.id.data)).scalar_one()
            print(val)
            val.name = form.name.data
            val.description = form.description.data
            val.start_date = form.start_date.data
            val.end_date = form.end_date.data
            val.link = form.link.data
            db.session.commit()
        except Exception as ex:
            flash(str(ex))
    return render_template('teacher/coursedetails.html', user=user, page=page, data=data, total=total, form=form)


@app.route('/teacher/deletecourse', methods=['GET', 'POST'])
@token_required
def teacher_course_delete():
    '''teacher course delete page'''
    id = request.args.get('id')
    val = db.session.execute(db.select(Course).filter_by(
        id=id)).scalar_one()
    db.session.delete(val)
    db.session.commit()
    flash("Course deleted successfully")
    return redirect('/teacher/course')


@app.route('/teacher/profile', methods=['GET'])
@token_required
def teacher_profile():
    ''' profile page func '''
    name = session.get('name')
    user = session.get('user')
    # nonlocal page
    page = "profile"
    dt = Profile.query.filter_by(username=user).first()
    return render_template('teacher/profile.html', data=dt, user=name, page=page)
