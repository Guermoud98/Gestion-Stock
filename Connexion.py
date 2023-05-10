import mysql.connector

class Database:
    def __init__(self, host="localhost", user="root", password="2018", database="GESTIONSTOCK"):
        """
        Initialise un objet Database avec les informations de connexion passées en paramètres.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        """
        Établit une connexion avec la base de données et renvoie un objet de connexion.
        """
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def execute_query_with_fetchall(self, query, values=None):
        """
        Exécute une requête SQL et renvoie les résultats sous forme de tuple.
        Si des paramètres sont nécessaires, ils peuvent être passés en paramètre values
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as error:
            print(f"Erreur lors de l'exécution de la requête: {error}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def execute_query_with_fetchone(self, query, values=None):
        """
        Exécute une requête SQL et renvoie la première ligne de résultat sous forme de tuple.
        Si des paramètres sont nécessaires, ils peuvent être passés en paramètre values
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result
           # if result is  not None: # existe   username par exemple 
               # return True
            #else: 
             # return False
        except mysql.connector.Error as error:
            print(f"Erreur lors de l'exécution de la requête: {error}")
            
        finally:
            if conn:
                cursor.close()
                conn.close()

    def execute_insert_query(self, query, values=None):
        """
        Exécute une requête SQL d'insertion et renvoie le dernier ID inséré.
        Si des paramètres sont nécessaires, ils peuvent être passés en paramètre values
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as error:
            print(f"Erreur lors de l'exécution de la requête: {error}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def execute_update_query(self, query, values=None):
        """
        Exécute une requête SQL de mise à jour et renvoie le nombre de lignes modifiées.
        Si des paramètres sont nécessaires, ils peuvent être passés en paramètre values
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
        except mysql.connector.Error as error:
            print(f"Erreur lors de l'exécution de la requête: {error}")
        finally:
            if conn:
                cursor.close
    def execute_delete_query(self, query, values=None):
        """
        Exécute une requête SQL de suppression et renvoie le nombre de lignes supprimées.
        Si des paramètres sont nécessaires, ils peuvent être passés en paramètre values.
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
        except mysql.connector.Error as error:
            print(f"Erreur lors de l'exécution de la requête: {error}")
        finally:
            if conn:
                cursor.close()
