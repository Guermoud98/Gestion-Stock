from Connexion import Database


class Admin:
    def __init__(self, username="", password="",fullname="", email="", tel="", id_admin=None):
        """
        Initialise un objet admin avec les attributs passés en paramètres.
        id_admin est optionnel, car il est généré automatiquement dans la base de données.
        """
        self.id_admin = id_admin
        self.username = username
        self.password = password
        self.email = email
        self.tel = tel
        self.fullname = fullname

class AdminDAO:
    def __init__(self,admin=Admin()):
        """
        Initialise un objet adminDAO avec une référence à la base de données.
        """
        self.db = Database()
        self.admin=admin #creation d'une instance de la classe Admin()

    def ajouter_admin(self,username):
      
        #Ajoute un admin dans la base de données.
        check_query = "SELECT * FROM admin WHERE username=%s"
        value=(username,)
        existing_user = self.db.execute_query_with_fetchone(check_query,value)
        if existing_user:
            return False  # usernom already exists, return False
        else:
            query = "INSERT INTO admin (username, password ,fullname, email, Tel) VALUES (%s, %s, %s, %s,%s)"
            values = ( self.admin.username, self.admin.password,  self.admin.fullname, self.admin.email, self.admin.tel)
            return self.db.execute_insert_query(query,values) 
    def authentifier_admin(self,username,password):# en meme temps c'est une methode  d'affichage des infos de l'admin
        query="SELECT * FROM admin WHERE username=%s AND password=%s"
        value=(username,password)
        admin_data=self.db.execute_query_with_fetchone(query,value)#retourne l'admin connecté et le stocké dans un objet admin 
        if admin_data is None:
            return None
        else:
            return admin_data
    def modifier_admin_by_id(self,username,password,fullname,email,tel,id):
        check_query="SELECT username FROM admin WHERE username=%s AND id_admin!=%s"
        val=(username,id)
        exist=self.db.execute_query_with_fetchone(check_query,val)
        if exist is not None:
            return False
        else:
            query="UPDATE admin SET username=%s, password=%s,fullname=%s,email=%s,Tel=%s WHERE id_admin=%s"
            value=(username,password,fullname,email,tel,id)
            result=self.db.execute_update_query(query,value)
            return result
    def supprimer_admin_by_id(self,id):
        query="DELETE FROM admin WHERE id_admin=%s"
        value=(id,)
        result=self.db.execute_delete_query(query,value)
        return result
    def get_id_admin_by_username(self,username):# à supprimer
        query = "SELECT id_admin FROM admin WHERE username=%s"
        value = (username,)
        result = self.db.execute_query_with_fetchone(query, value)
        return int(result[0])
    def get_info_by_id_admin(self,id_admin):# àsupprimer
        query="SELECT * FROM admin WHERE id_admin=%s"
        value=(id_admin,)
        admin_data=self.db.execute_query_with_fetchone(query,value)#retourne l'admin connecté et le stocké dans un objet admin 
       # Création d'un objet Admin à partir des données de l'administrateur authentifié
        return admin_data
        
        
#///////////////////////produit///////////////////////////////////////////////////////////////////////////////////////////
class Produit:
    def __init__(self, nom_produit="", description="", prix_unitaire="", quantite_stock="", seuil_alerte="", date_entree="", date_sortie="", image_produit="", id_admin=None, id_produit=None):
        """
        Initialise un objet Produit avec les attributs passés en paramètres.
        id_admin et id_produit sont optionnels, car ils sont générés automatiquement dans la base de données.
        """
        self.id_produit = id_produit
        self.nom_produit = nom_produit
        self.description = description
        self.prix_unitaire = prix_unitaire
        self.quantite_stock = quantite_stock
        self.seuil_alerte = seuil_alerte
        self.date_entree = date_entree
        self.date_sortie = date_sortie
        self.image_produit = image_produit
        self.id_admin = id_admin


class ProduitDAO:
    def __init__(self,new_produit=Produit()):
        self.db = Database()
        self.produit=new_produit
        self.admin_dao = AdminDAO()

    def ajouter_produit(self):
        query = "INSERT INTO produit(nom_produit, description, prix_unitaire, quantite_stock, seuil_alerte, date_entree, date_sortie, image_produit, id_admin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (self.produit.nom_produit, self.produit.description, self.produit.prix_unitaire,self.produit.quantite_stock, self.produit.seuil_alerte, self.produit.date_entree, self.produit.date_sortie, self.produit.image_produit, self.produit.id_admin)
        return   self.db.execute_insert_query(query, values)

    def modifier_produit(self, produit):
        query = "UPDATE produit SET nom_produit=%s, description=%s, prix_unitaire=%s, quantite_stock=%s, seuil_alerte=%s, date_entree=%s, date_sortie=%s,image_produit=%s WHERE id_produit=%s"
        values = (produit[1], produit[2], produit[3], produit[4], produit[5], produit[6], produit[7],produit[8],produit[0])
        result=self.db.execute_update_query(query,values)
        return result

    def recuperer_produit_par_id(self, id_produit):
        query = "SELECT * FROM produit WHERE id_produit = %s"
        values = (id_produit,)
        result = self.db.execute(query, values)
        produit = None
        if result:
            row = result[0]
            admin = self.admin_dao.recuperer_admin_par_id(row["id_admin"])
            produit = Produit(row["nom_produit"], row["description"], row["prix_unitaire"], row["quantite_stock"], row["seuil_alerte"], row["date_entree"], row["date_sortie"], row["image_produit"], admin, row["id_produit"])
        return produit

    def recuperer_tous_les_produits(self,id):
        query = "SELECT * FROM produit WHERE  id_admin=%s"
        value=(id,)
        results = self.db.execute_query_with_fetchall(query,value)
        return results
    
    def Supprimer_Produit_By_Id_Produit(self,id):
        search_query="SELECT * FROM produit WHERE id_produit=%s"
        val=(id,)
        exist=self.db.execute_query_with_fetchall(search_query,val)
        if exist:
            query="DELETE FROM produit WHERE id_produit=%s"
            value=(id,)
            result=self.db.execute_delete_query(query,value)
            return result 
        
    def Supprimer_Produit_By_Id_Admin(self,id):
        search_query="SELECT * FROM produit WHERE id_admin=%s"
        val=(id,)
        exist=self.db.execute_query_with_fetchall(search_query,val)
        if exist:
            query="DELETE FROM produit WHERE id_admin=%s"
            value=(id,)
            result=self.db.execute_delete_query(query,value)
            return result 
        
    def recherche_produit_par_nom(self,nom):
        search_query="SELECT * FROM produit WHERE nom_produit=%s"
        value=(nom,)
        result=self.db.execute_query_with_fetchone(search_query,value)
        return result
    
    def recherche_produit_par_prix(self,prix):
        search_query="SELECT * FROM produit WHERE prix_unitaire >=%s"
        value=(prix,)
        result=self.db.execute_query_with_fetchall(search_query,value)
        return result 
            

