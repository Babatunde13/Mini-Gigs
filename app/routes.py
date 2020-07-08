'''Module for creating endpoints/view functions to the app'''

# Third party imports
from flask import (render_template, redirect, abort,
                    url_for, flash, request)
from werkzeug.security import (
    generate_password_hash, check_password_hash)
from flask_login import  (login_user, logout_user, 
                login_required, current_user)

#Local imports
from app import app, db, mail
from app.forms import (LoginForm, RegisterForm,
                ResetPasswordForm, NewPasswordForm,
                UpdateAccountForm, CreateJob)
from app.models import (User, Job,
            WorkExperience, Education,
            Interest, Skill)
from app.utils import send_mail, save_pic

@app.route('/')
def home():
    jobs=Job.query.all()
    tot_jobs=[]
    for i in range(0, len(jobs), 4):
        if i+4 >= len(jobs):
            tot_jobs.append(jobs[i:])
        else:
            tot_jobs.append(jobs[i:i+3])
    return render_template('home.html', jobs=tot_jobs)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    #checks if all form inputs are validated and the submit button is clicked
    if form.validate_on_submit():
        email = form.email.data
        user=User.query.filter_by(email=email).first()

        #checks if username exist in the db and if password matches, then logs user in and redirects to the profile page
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        flash('Invalid Username or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password=generate_password_hash(form.password.data)
        email=form.email.data
        user=User(username=username,
                password=password,
                is_recruiter=form.is_recruiter.data,
                email=email,
                fname=form.fname.data,
                lname=form.lname.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully.', 'success')
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html', title='About Page')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(500)
def not_found(e):
    return render_template('500.html'), 500

@app.route('/profile')
@login_required
def profile():
    if not current_user.is_confirmed:
        flash("You haven't confirm your account", 'warning')
    if current_user.is_recruiter:
        jobs=Job.query.filter_by(creator_id=current_user.id).all()
        tot_jobs=[]
        for i in range(0, len(jobs), 3):
            if i+3 >= len(jobs):
                tot_jobs.append(jobs[i:])
            else:
                tot_jobs.append(jobs[i:i+3])
        return render_template('recruitprofile.html', user=current_user, jobs=tot_jobs)
    else:
        return render_template('userprofile.html', user=current_user)
    
@app.route('/profile/<name>')
# @login_required
def profile_(name):
    user=User.query.filter_by(username=name).first_or_404()
    if current_user.is_authenticated and user==current_user:
        return redirect(url_for('profile'))
    if not user.is_confirmed:
        flash("You haven't confirm your account", 'warning')
    if user.is_recruiter:
        jobs=Job.query.filter_by(creator_id=user.id).all()
        return render_template('recruitprofile.html', user=user, jobs=jobs)
    else:
        return render_template('userprofile.html', user=user)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    '''View function for getting link to reset password'''

    if current_user.is_authenticated: # If user is authenticated, then user should be redirected to their profile page
        return redirect(url_for('profile'))
    form=ResetPasswordForm()

    #If form is validated and submitted
    if form.validate_on_submit(): 
        email=form.email.data
        user = User.query.filter_by(email=email).first()
        send_mail(user, 'passwordmail.html', 'Reset Password', 1800)
        flash('Instructions has been sent to your mail on how to reset your password', 'info')
        
    return render_template('reset_password.html',
                            title='Reset Password',
                            form=form)

@app.route('/resetpasswordlink/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    user=User.verify_reset_token(token)
    if user is None:
        flash('Token is invalid or has expired', 'warning')
        return redirect(url_for('reset_password'))
    form = NewPasswordForm()
    if form.validate_on_submit():
        password=generate_password_hash(form.password.data)
        user.password=password
        db.session.commit()
        flash('Password has been updated! You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', 
                            title='Reset Password',
                            form=form)


@app.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateAccountForm()
    present_interest=Interest.query.filter(Interest.users.any(username=current_user.username)).all()
    present_skill=Skill.query.filter(Skill.users.any(username=current_user.username)).all()
    if form.validate_on_submit():
        if form.resume.data:
            pic_file = save_pic(form.resume.data, 'static/resume')
            current_user.resume = pic_file
        if form.profile_picture.data:
            pic_file_ = save_pic(form.profile_picture.data, 'static/profileimages')
            current_user.profile_picture = pic_file_
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.phone_number = form.phone.data
        current_user.is_super_admin = form.is_admin.data
        current_user.is_actively_interviewing = form.is_actively_interviewing.data
        current_user.is_recruiter = form.is_recruiter.data
        current_user.facebook_link = form.facebook_link.data
        current_user.twitter_link = form.twitter_link.data
        current_user.linkedin_link = form.linkedin_link.data
        current_user.salary_expt = form.salary.data
        current_user.address = form.address.data
        skill=form.skills.data
        skills = {1:'C++', 2:'Python', 3: 'JavaScript', 
                4: 'Java', 5: 'React', 6: 'Golang', 7: 'Rust'}
        interest=form.interests.data
        interests={
            1:'Product Design', 2:'UI/UX', 3: 'Software Development', 
            4: 'Artificial Intelligence', 5: 'Data Science', 
            6: 'Game Development', 7: 'Cyber Security'}
        if skill:
            for skl in present_skill:
                db.session.delete(skl)
            for choice in skill:
                current_user.skills.append(Skill(name=skills[choice]))  
        if interest:
            for skl in present_interest:
                db.session.delete(skl)
            for choice in interest:
                current_user.interests.append(Interest(name=interests[choice]))
        db.session.commit()
        
        flash('Your account has been updated', 'success')
        return redirect(url_for('profile'))
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.fname.data = current_user.fname
    form.lname.data = current_user.lname
    form.phone.data = current_user.phone_number
    if form.phone.data == None:
        form.phone.data = '+2340000000000'
    form.address.data = current_user.address
    form.is_admin.data = current_user.is_super_admin
    form.is_actively_interviewing.data = current_user.is_actively_interviewing
    form.is_recruiter.data = current_user.is_recruiter
    form.facebook_link.data = current_user.facebook_link
    form.twitter_link.data = current_user.twitter_link
    form.interests.data=present_interest
    form.skills.data=present_skill
    form.linkedin_link.data = current_user.linkedin_link
    form.salary.data = current_user.salary_expt
    return render_template('updateprofile.html', 
                            title='Update Account',
                            form=form)
    
@app.route('/confirm')
@login_required
def confirm():
    if current_user.is_confirmed: # If user is confirmed, then user should be redirected to their profile page
        flash('Your account has been confirmed', 'info')
        return redirect(url_for('profile'))
    send_mail(current_user, 'passwordmail.html', 'Confirm Account')
    flash('A confirmation has been sent to your mail', 'info')
    return redirect(url_for('profile'))

@app.route('/confirm/account/<token>')
@login_required
def confirm_profile(token):
    user=User.verify_reset_token(token)
    user=User.verify_reset_token(token)
    if user is None:
        flash('Token is invalid or has expired', 'warning')
        return redirect(url_for('profile'))
    user.is_confirmed=True
    db.session.commit()
    flash('Account has been confirmed', 'success')
    return redirect(url_for('profile'))

@app.route('/job/new', methods=['GET', 'POST'])
@login_required
def add_job():
    if not current_user.is_recruiter:
        abort(403)
    form = CreateJob()
    if form.validate_on_submit():
        title=form.title.data
        company=form.company.data
        description=form.description.data
        exp_date=form.expiry_date.data
        job=Job(title=title, 
                company=company,
                description=description, 
                expiry_date=exp_date,
                creator_id=current_user.id)
        db.session.add(job)
        db.session.commit()
        flash('Job added successfully', 'success')
        return redirect(url_for('profile'))
    return render_template('addjob.html', 
                            form=form, 
                            title='Create Job')

@app.route('/job/<id>')
@login_required
def view_job(id):
    job=Job.query.get_or_404(id)
    user=User.query.filter_by(id=job.creator_id).first()
    return render_template('viewjob.html', 
                            job=job, 
                            title='View Job', 
                            user=user)

@app.route('/job/<id>/apply', methods=['GET', 'POST'])
@login_required
def apply(id):
    job=Job.query.get_or_404(id)
    if not current_user.resume:
        flash('You need to upload your resume before applying', 'danger')
        return redirect(url_for('update_profile'))
    job.users.append(current_user)
    db.session.commit()
    print(job.users.all())
    flash("You've successfully applied for the job", 'success')
    return redirect(url_for('profile'))
    

