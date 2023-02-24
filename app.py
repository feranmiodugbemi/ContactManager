from flask import Flask, render_template, request, flash, redirect
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

client = FaunaClient(
  secret=os.getenv('FAUNASECRET')
)


@app.route("/", methods=["POST", "GET"])
def hello():
    #Creating a new contact
    if request.method == "POST":
        name = request.form.get('name')
        occupation = request.form.get('occupation', default='')
        address = request.form.get('address', default='')
        contact = request.form.get('contact')
        email = request.form.get('email', default='')
        client.query(
            q.create(
                q.ref('collections/Users'),
                {
                    'data':{
                        'id': q.new_id(),
                        'name':name,
                        'occupation':occupation,
                        'address' : address,
                        'contact': contact,
                        'email': email
                    }
                }
            )
        )
        return redirect('/')
    else:
        #Getting all the contacts
        result = client.query(
            q.map_(
                q.lambda_("x", q.get(q.var("x"))),
                q.paginate(q.documents(q.collection("Users")))
            )
        )
        data = [doc["data"] for doc in result["data"]]
        return render_template('index.html', data=data)

@app.route('/delete/<int:id>')
def delete(id):
    id = id + 1024
    contact = q.ref(q.collection("Users"), id)
    client.query(q.delete(contact))
    return redirect('/')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
