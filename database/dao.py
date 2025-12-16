from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.connessione import Connessione

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """

    @staticmethod
    def read_rifugi():
        # leggo tutti i rifugi presenti
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("CONNESSIONE NON RIUSCITA")

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM rifugio"
        cursor.execute(query)

        for row in cursor:
            rifugio = Rifugio(row["id"], row["nome"], row["localita"])
            result.append(rifugio)

        cnx.close()
        cursor.close()
        return result

    @staticmethod
    def read_connessioni(anno):
        # leggo le connessioni in base all'anno selezionato
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("CONNESSIONE NON RIUSCITA")

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM connessione WHERE anno<=%s"
        cursor.execute(query, (anno,))

        for row in cursor:
            connessione = Connessione(row["id_rifugio1"], row["id_rifugio2"], row["distanza"],row["difficolta"],row["anno"])
            result.append(connessione)

        cnx.close()
        cursor.close()
        return result