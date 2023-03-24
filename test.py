from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from dotenv import load_dotenv
import os

load_dotenv()






def delete(name):
    client = FaunaClient(
        secret=os.getenv('FAUNASECRET')
    )
    result = client.query(
        q.select(['ref'], q.get(q.match(q.index("users_by_id"), name)))
    )
    client.query(q.delete(result))
    return result


print(delete("Feranmi Odugbemi"))
