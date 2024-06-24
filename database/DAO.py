from database.DB_connect import DBConnect
from model.giocatore import Giocatore


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNodi(minGoal):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select p.*
from players p ,actions a 
where p.PlayerID =a.PlayerID 
group by p.PlayerID 
having avg(a.Goals)>%s """

        cursor.execute(query,(minGoal,))

        for row in cursor:
            result.append(Giocatore(**row))

        cursor.close()
        conn.close()
        return result
