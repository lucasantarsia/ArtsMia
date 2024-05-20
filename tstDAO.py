from database.DAO import DAO
from model.model import Model

model = Model()

res = DAO.getAllObjects()

conn = DAO.getAllConnessioni(model._idMap)

print(len(res))

print(len(conn))
