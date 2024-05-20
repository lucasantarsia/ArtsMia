from database.DB_connect import DBConnect
from model.artObject import ArtObject
from model.connessioni import Connessione


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllObjects():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from objects o"""
        cursor.execute(query, ())

        for row in cursor:
            result.append(ArtObject(**row))  # -> senza scrivere per ogni attributo
            #result.append(ArtObject(object_id=row["object_id"], ... ))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(v1: ArtObject, v2: ArtObject):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(*)
                from exhibition_objects eo1, exhibition_objects eo2
                where eo1.exhibition_id = eo2.exhibition_id 
                and eo1.object_id < eo2.object_id 
                and eo1.object_id = %s
                and eo2.object_id = %s"""
        cursor.execute(query, (v1.object_id, v2.object_id))

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnessioni(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select eo1.object_id as o1, eo2.object_id as o2, count(*) as peso
                from exhibition_objects eo1, exhibition_objects eo2
                where eo1.exhibition_id = eo2.exhibition_id 
                and eo1.object_id < eo2.object_id 
                group by eo1.object_id, eo2.object_id 
                order by peso desc"""
        cursor.execute(query, ())

        for row in cursor:
            result.append(Connessione(idMap[row["o1"]], idMap[row["o2"]], row["peso"]))
        cursor.close()
        conn.close()
        return result
