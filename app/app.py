from flask import Flask, render_template, request, session, redirect, url_for
from models.models import ProjectContent, AgendaContent, CommentContent, User
from models.database import db_session
from datetime import datetime
from app import key
from hashlib import sha256

app = Flask(__name__)
app.secret_key = key.SECRET_KEY

# これがないと複数のテーブルに対する処理ができない??
@app.teardown_request
def remove_session(ex=None):
    db_session.remove()

@app.route("/")
@app.route("/project")
def project():
    # プロジェクト選択画面に入ったらsession内の選択しているプロジェクトの情報を初期化
    session["project_id"] = None

    all_project = ProjectContent.query.all()
    return render_template("project.html", all_project=all_project)

@app.route("/add_project", methods=["post"])
def add_project():
    project = request.form["project"]
    content = ProjectContent(project, datetime.now())
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("project"))

@app.route("/open_project", methods=["post"])
def open_project():
    project_id = request.form.get("open", None)
    # seeeionに開いたprojectの情報を保存
    session["project_id"] = project_id
    return redirect(url_for("agenda", project_id=project_id))

@app.route("/delete_project", methods=["post"])
def delete_project():
    content = ProjectContent.query.filter_by(id=request.form.get("delete", None)).first()
    db_session.delete(content)
    db_session.commit()
    return redirect(url_for("project"))

@app.route("/update_project", methods=["post"])
def update_project():
    content = ProjectContent.query.filter_by(id=request.form["update"]).first()
    content.project = request.form["update_project"]
    db_session.commit()
    return redirect(url_for("project"))


@app.route("/agenda")
def agenda():
    project_id = request.args.get("project_id")
    project_name = ProjectContent.query.filter_by(id=project_id).first().project
    all_agenda = AgendaContent.query.filter_by(project_id=project_id)
    return render_template("agenda.html", project_name=project_name, all_agenda=all_agenda)


@app.route("/add_agenda", methods=["post"])
def add_agenda():
    project_id = int(session["project_id"]) 
    agenda = request.form["agenda"]
    content = AgendaContent(project_id, agenda, False ,datetime.now())
    db_session.add(content)
    db_session.commit()

    return redirect(url_for("agenda", project_id=project_id))

@app.route("/delete_agenda", methods=["post"])
def delete_agenda():
    project_id = int(session["project_id"]) 
    content = AgendaContent.query.filter_by(id=request.form.get("delete", None)).first()
    db_session.delete(content)
    db_session.commit()
    return redirect(url_for("agenda", project_id=project_id))

@app.route("/update_agenda", methods=["post"])
def update_agenda():
    project_id = int(session["project_id"]) 
    content = AgendaContent.query.filter_by(id=request.form["update"]).first()
    content.agenda = request.form["update_agenda"]
    db_session.commit()
    return redirect(url_for("agenda", project_id=project_id))

@app.route("/done_agenda", methods=["post"])
def done_agenda():
    project_id = int(session["project_id"]) 
    content = AgendaContent.query.filter_by(id=request.form["done"]).first()
    content.done = not content.done
    db_session.commit()
    return redirect(url_for("agenda", project_id=project_id))

@app.route("/open_agenda", methods=["post"])
def open_agenda():
    agenda_id = request.form.get("open", None)
    # seeeionに開いたprojectの情報を保存
    session["agenda_id"] = agenda_id
    return redirect(url_for("comment", agenda_id=agenda_id))

@app.route("/comment")
def comment():
    agenda_id = request.args.get("agenda_id")
    agenda_name = AgendaContent.query.filter_by(id=agenda_id).first().agenda
    all_comment = CommentContent.query.filter_by(agenda_id=agenda_id, project_id = session["project_id"])
    # for a in all_comment:
    #     print(a.comment)
    # all_comment = CommentContent.query.filter_by(agenda_id=agenda_id)
    return render_template("comment.html", agenda_name=agenda_name, all_comment=all_comment)

@app.route("/add_comment", methods=["post"])
def add_comment():
    project_id = int(session["project_id"]) 
    agenda_id = int(session["agenda_id"]) 
    comment = request.form["comment"]
    content = CommentContent(project_id, agenda_id, comment,datetime.now())
    db_session.add(content)
    db_session.commit()

    return redirect(url_for("comment", agenda_id=agenda_id))

@app.route("/delete_comment", methods=["post"])
def delete_comment():
    project_id = int(session["project_id"]) 
    agenda_id = int(session["agenda_id"]) 
    content = CommentContent.query.filter_by(id=request.form.get("delete", None)).first()
    db_session.delete(content)
    db_session.commit()
    return redirect(url_for("comment", agenda_id=agenda_id))

@app.route("/update_comment", methods=["post"])
def update_comment():
    project_id = int(session["project_id"]) 
    agenda_id = int(session["agenda_id"]) 
    content = CommentContent.query.filter_by(id=request.form["update"]).first()
    content.comment = request.form["update_comment"]
    db_session.commit()
    return redirect(url_for("comment", agenda_id=agenda_id))

@app.route("/back_agenda", methods=["post"])
def back_agenda():
    session.pop("project_id", None)
    return redirect(url_for("project"))

@app.route("/back_comment", methods=["post"])
def back_comment():
    session.pop("agenda_id", None)
    return redirect(url_for("agenda", project_id=session["project_id"]))
if __name__ == "__main__":
    app.run(debug=True)




# @app.route("/select_project", methods=["post"])
# def select_project():
#     if request.form.get("open", None) != None:
#         project_id = request.form.get("open", None)
#         project_name = ProjectContent.query.filter_by(id=project_id).first()
#         all_agenda = AgendaContent.query.filter_by(project_id=project_id)
#         session["project_id"] = project_id
#         return render_template("agenda.html", project_name=project_name, all_agenda=all_agenda)
#     elif request.form.get("delete", None) != None:
#         content = ProjectContent.query.filter_by(id=request.form.get("delete", None)).first()
#         db_session.delete(content)
#         db_session.commit()
#     elif request.form.get("update", None) != None and request.form.get("update", None) != "":
#         content = ProjectContent.query.filter_by(id=request.form["update"]).first()
#         content.project = request.form["update_project"]
#         db_session.commit()
#     return redirect(url_for("project"))