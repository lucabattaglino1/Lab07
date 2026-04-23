from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getUmidita():
        cnx = DBConnect.get_connection()  # connessione
        cursor = cnx.cursor(dictionary=True)  # creo cursore

        # query scritta su DBVEAR
        query = """SELECT Localita, AVG(umidita) as media
                    FROM situazione
                    WHERE MONTH(Data) = %s
                    ORDER BY Localita"""

        cursor.execute(query)  # eseguo la query

        # ciclo su cursore per leggere i dati
        # li inserisco in una lista
        res = []
        for row in cursor:
            res.append(row)

        cursor.close()  # chiudo cursore
        cnx.close()  # restituisco connessione
        return res  # return della lista


