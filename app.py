from flask import Flask, render_template, request, flash
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
        client.query(
            q.create(
                q.ref('collections/Users'),
                {
                    'data':{
                        'id': q.new_id(),
                        'name':"Feranmi",
                        'occupation':'CEO',
                        'address' : "Block 200, Alaka",
                        'contact': "+234 816 043 5459",
                        'email': 'feranmi@email.com'
                    }
                }
            )
        )
    else:
        return render_template('index.html')






if __name__ == "__main__":
    app.run(port=5000, debug=True)
