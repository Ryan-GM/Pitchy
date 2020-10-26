from flask import render_template,redirect,url_for,abort,request
from . import main
from flask_login import login_required,current_user
from ..models import User,Comment,Likes,Pitchy,Dislikes
from .. import db,photos
from .form import PitchyForm,UpdateProfile,CommentForm

@main.route('/')
def index():
    pitches = Pitchy.query.all()
    funny = Pitchy.query.filter_by(category = 'Funny').all()
    cheesy = Pitchy.query.filter_by(category = 'Cheesy').all()
    life = Pitchy.query.filter_by(category = 'Life').all()
    return render_template('index.html', pitch = pitches, funny = funny,life = life,cheesy = cheesy)

@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
    user_id = current_user._get_current_object().id
    posts = Pitchy.query.filter_by(user_id = user_id).all()
    if user is None:
        abort(404)
    return render_template("profile/profile.html",user = user,post = posts)

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_u()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/update.html',form =form)

@main.route('/create_new',methods = ['POST','GET'])
@login_required
def new_pitch():
    form = PitchyForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        post = form.post.data
        user_id = current_user
        new_pitch_object = Pitchy(post = post,user_id = current_user._get_current_object().id,category = category,title = title)
        new_pitch_object.save_p()
        return redirect(url_for('main.index'))
    return render_template('create_pitchy.html',form =form)

@main.route('/comment/<int:pitchy_id>',methods = ['POST','GET'])
@login_required
def comment(pitchy_id):
    form =CommentForm()
    pitchy = Pitchy.query.get(pitchy_id)
    all_comments = Comment.query.filter_by(pitchy_id = pitchy_id).id()
    if form.validate_on_submit():
        comment = form.comment.data
        pitchy_id = pitchy_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitchy_id = pitchy_id)
        new_comment.save_c()
        return redirect(url_for('.comment',pitchy_id = pitchy_id))
    return render_template('comment.html',form = form,pitch = pitchy,all_comments = all_comments) 

@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',name=name))

@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    get_pitches = Likes.get_likes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Likes(user = current_user, pitchy_id = id)
    new_vote.save()
    return redirect(url_for('main.index',id=id))

@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    pitch = Dislikes.get_dislikes(id)
    valid_string = f'{current_user.id}:{id}'
    for p in pitch:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id = id))
        else:
            continue
    new_dislikes = Dislikes(user = current_user, pitchy_id = id)
    new_dislikes.save()
    return redirect(url_for('main.index',id = id))