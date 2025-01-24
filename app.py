from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
db = SQLAlchemy(app)

# Data class
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"


with app.app_context():
    db.create_all()

# Home page
@app.route("/", methods=["POST", "GET"])
def aname():
    if request.method == "POST":
        current_task = request.form.get("content")
        if not current_task:
            return "Content cannot be empty!"
        
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)



# deleting an item
@app.route("/delete/<int:id>")
def remove(id:int):
    remove_task=MyTask.query.get_or_404(id)
    try:
        db.session.delete(remove_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error{e}"
    
# editing data
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id: int):
    # Fetch the task to be edited
    edit_task = MyTask.query.get_or_404(id)

    if request.method == "POST":
        # Update the task content
        edit_task.content = request.form.get("content")
        if not edit_task.content:
            return "Task content cannot be empty!"
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error: {e}"
    else:
        # Render the edit form
        return render_template("edit.html", task=edit_task)

if __name__ == "__main__":
 

    app.run(debug=True)
