from database.DB_connect import DBConnect
from model.connessione import Connessione
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

    @staticmethod
    def getAllGiocatori():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
    from players p """

        cursor.execute(query)

        for row in cursor:
            result.append(Giocatore(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct g1 as v1,g2 as v2,sum(t1) as t1,sum(t2) as t2
from (select a.PlayerID as g1 ,a.MatchID as p1, a.TeamID as s1, a.TimePlayed as t1
from actions a 
where a.Starts=1) as t1,(select a.PlayerID as g2 ,a.MatchID as p2, a.TeamID as s2, a.TimePlayed as t2 
from actions a 
where a.Starts=1) as t2
where t1.g1!=t2.g2 and t1.p1=t2.p2 and t1.s1!=t2.s2
group by g1,g2
"""

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result

