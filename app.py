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
    return render_template('index.html')






if __name__ == "__main__":
    app.run(port=5000, debug=True)
