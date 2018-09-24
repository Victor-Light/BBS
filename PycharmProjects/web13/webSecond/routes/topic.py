from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *

from models.topic import Topic
from models.board import Board
from routes.index import current_user


main = Blueprint('topic', __name__)


import uuid
csrf_tokens = dict()

@main.route("/")
def index():
    # board_id = 2
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    token = str(uuid.uuid4())
    u = current_user()
    bs = Board.all()
    if u == None:
        return render_template("topic/index2.html", ms=ms, bs=bs)
    csrf_tokens['token'] = u.id
    return render_template("topic/index.html", ms=ms, token=token, bs=bs, user = u)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    board_id = m.board_id
    b = Board.find_by(id=board_id)
    return render_template("topic/detail.html", topic=m, board=b)


@main.route("/add", methods=["POST"])
def add():

    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    print(u)
   # return redirect(url_for('.detail', id=m.id))
    return redirect(url_for('.index'))

@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    # 判断 token 是否是我们给的
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        if u is not None:
            print('删除 topic 用户是', u, id)
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)


@main.route("/new")
def new():
    u = current_user()
    if u is None:
        # 转到 topic.index 页面
        # return redirect(url_for('topic.index'))
        return redirect(url_for("index.loginpage"))
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)
