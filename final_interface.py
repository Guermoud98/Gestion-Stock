import customtkinter
from tkinter import *
from datetime import date
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.ttk import Button
from tkinter import filedialog
from PIL import Image, ImageTk
#appel aux classes produit et admin
from Les_Classes import Admin,AdminDAO
from Les_Classes import Produit,ProduitDAO
import math 
class MainApp(tk.Frame):
    def __init__(self,master=None):
        #En résumé, le paramètre master est utilisé pour spécifier le widget parent de la fenêtre principale de l'application et permet à la fenêtre principale d'être placée à l'intérieur d'un autre widget.
        super().__init__(master)
        self.master=master
        
        self.master.title("Application Gestion Stock")
        self.master.geometry("500x500+100+50")
        self.admin_instance=AdminDAO()
        self.connected_admin=None # pour specifier l'admin connecté
        
        self.current_width = 0
        self.current_height = 0
        self.image_path=None  # Chemin vers l'image du produit dans la base de données
        # Lier la taille de self à self.master
        self.grid(sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
       
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        
    def creer_Login_Page(self):
        
        self.login_page_container = tk.Frame(self, borderwidth=5, relief="flat")
        self.login_page_container.grid(row=0, column=0, sticky="nsew")   # configurer les entry et label
        self.background_image = Image.open("photo.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.login_page_container, image=self.background_photo)
        self.background_label.place(relwidth=1,relheight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
            
        self.background_label.bind('<Configure>', self._resize_image)
        style = ttk.Style()

        style.configure('TEntry', padding=5, relief='flat',font=('Courier New', 15,'bold'))
        style.configure('TLabel', padding=5, relief='flat', background="white",font=('Courier New', 15,'bold'))  
        # configurer le style des buttons
        style.configure("TButton", padding=6, relief="flat", font=("Courier New", 12,'bold'))
        style.map("TButton",
                foreground=[('pressed', 'white'), ('active', 'white')],
                background=[('pressed', '#007bff'), ('active', '#0069d9')])

        self.form_login=tk.Frame(self.login_page_container, borderwidth=5, relief="flat", background="white")
        self.form_login.place(relx=0.5,rely=0.5,anchor="center")
        tk.Label(self.form_login, text="Login", background="#d4cae8",font=("Courier New", 25,'italic','bold')).grid(row=0, column=0, columnspan=2,sticky='news')
       
        # Create the username label and entry widget
        self.username_label = ttk.Label(self.form_login, text="Username:", style='TLabel')
        self.username_entry = ttk.Entry(self.form_login, style='TEntry', width='40')
        self.username_label.grid(row=1, column=0, padx=10, pady=10,sticky='news')
        self.username_entry.grid(row=1, column=1, padx=10, pady=10,sticky='news')

        # Create the password label and entry widget
        self.password_label = ttk.Label(self.form_login, text="Password:", style='TLabel')
        self.password_entry = ttk.Entry(self.form_login, style='TEntry', width='40', show='*')
        self.password_label.grid(row=2, column=0, padx=10, pady=10,sticky='news')
        self.password_entry.grid(row=2, column=1, padx=10, pady=10,sticky='news')
        username=self.username_entry.get()

        # Create the login button
        self.login_button = ttk.Button(self.form_login, text="Login", style="TButton", width='20', command=lambda:[self.check_login(),self.clear_widgets(),self.creer_Page_Acceuil()])
        self.login_button.grid(row=3, column=1, padx=10, pady=10,sticky='ew')
        self.signup_button = ttk.Button(self.form_login, text="Sign Up", style="TButton", width='20', command=lambda:[self.clear_widgets(),self.creer_SignUp_Page()])
        self.signup_button.grid(row=4, column=1, padx=10, pady=10,sticky='ew')


       

    def get_admin_logged_in(self):#pour mémoriser l'admin connecte right now
        return self.connected_admin
        
       
    def check_login(self):#retourne id de l'admin connecté
        username = self.username_entry.get()
        password = self.password_entry.get()
         # Call the authenticate method from the AdminDAO class
        ad = self.admin_instance.authentifier_admin(username,password) # user donc contient l'objet de type admin qui a l username et  password indique
        # Check if the user is valid
        self.connected_admin=ad
        if self.connected_admin:
            print("Login successful!")
            messagebox.showinfo("info","Login successful!")
            return self.connected_admin
            #print(AdminDAO(admin=user).get_id_admin_by_username(user.username))
             #print(user)
        
                #self.clear_widgets()
                #self.creer_Affichage_Admin_Page()
                #self.creer_Ajout_Porduit_Page() # si l'admin se connecte la page des produits va se créer
        
        else:
            print("Invalid username or password.")
            messagebox.showerror("Erreur d'authentification", "Invalid username or password.") 
            return False

    def clear_widgets(self):
        if self.connected_admin:
            
            for widget in self.winfo_children():
                widget.grid_forget()
                widget.place_forget()
   
    def creer_Ajout_Produit_Page(self):
        
        self.clear_widgets()
       # conteneur grand
        self.container=tk.Frame(self,bg="white")
        self.container.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")
                        
        # Création des deux sous-conteneurs égaux
        left_container = tk.Frame(self, bg="white")
        left_container.grid(row=0, column=0, sticky="nsew")
        right_container = tk.Frame(self, bg="white")
        right_container.grid(row=0, column=1, sticky="nsew")

        # Configuration de la grille de disposition pour diviser le grand conteneur en deux colonnes égales
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

         # Configuration de la grille de disposition pour diviser chaque sous-conteneur en une seule ligne et colonne
        left_container.rowconfigure(0, weight=1)
        left_container.columnconfigure(0, weight=1)
        right_container.rowconfigure(0, weight=1)
        right_container.columnconfigure(0, weight=1)
        tk.Label(left_container, text="Ajout des produits ",background='white',font=("Courier New", 25,'italic','bold')).grid(row=0, column=0, columnspan=2,sticky='news')

        # Create the nom_produit label and entry widget
        self.nom_produit_label = ttk.Label(left_container, text="Nom du produit:", font=("Courier New", 12))
        self.nom_produit_entry = ttk.Entry(left_container, style='TEntry', width='40')
        self.nom_produit_label.grid(row=1, column=0, padx=10, pady=10)
        self.nom_produit_entry.grid(row=1, column=1, padx=10, pady=10)
        # Create the description label and entry widget
        self.description_label = ttk.Label(left_container, text="Descritpion:", font=("Courier New", 12))
        self.description_entry = ttk.Entry(left_container, style='TEntry', width='40')
        self.description_label.grid(row=2, column=0, padx=10, pady=10)
        self.description_entry.grid(row=2, column=1, padx=10, pady=10)
        #Create the prix label and entry widget
        self.prix_entry = ttk.Entry(left_container, style='TEntry', width='40')
        self.prix_label = ttk.Label(left_container, text="Prix Unitaire:", font=("Courier New", 12))
        self.prix_label.grid(row=3, column=0, padx=10, pady=10)
        self.prix_entry.grid(row=3, column=1, padx=10, pady=10)
        # Create the quantite label and entry widget
        self.quantite_label = ttk.Label(left_container, text="Quantité en Stock:", font=("Courier New", 12))
        self.quantite_entry = ttk.Entry(left_container, style='TEntry', width='40')
        self.quantite_label.grid(row=4, column=0, padx=10, pady=10)
        self.quantite_entry.grid(row=4, column=1, padx=10, pady=10)
        # Create the seuil alerte label and entry widget
        self.seuil_alerte_label = ttk.Label(left_container, text="Seuil d'alerte:", font=("Courier New", 12))
        self.seuil_alerte_entry = ttk.Entry(left_container, style='TEntry', width='40')
        self.seuil_alerte_label.grid(row=6, column=0, padx=10, pady=10)
        self.seuil_alerte_entry.grid(row=6, column=1, padx=10, pady=10)
        # Create the seuil date_entree label and entry widget
        self.date_entree_label = ttk.Label(left_container, text="Date entrée:", font=("Courier New", 12))
        self.date_entree_entry = ttk.Entry(left_container, style='TEntry', width='40')
        self.date_entree_label.grid(row=7, column=0, padx=10, pady=10)
        self.date_entree_entry.grid(row=7, column=1, padx=10, pady=10)
        self.date_entree_entry.insert(0, "YYYY-MM-DD")
        self.date_entree_entry.bind("<FocusIn>", lambda event: self.date_entree_entry.delete(0, "end"))
    
        # Create the seuil date_sortie label and entry widget
        self.date_sortie_label = ttk.Label(left_container, text="Date Sortie:", font=("Courier New", 12))
        self.date_sortie_entry = ttk.Entry(left_container, style='TEntry', width='40')
        self.date_sortie_label.grid(row=8, column=0, padx=10, pady=10)
        self.date_sortie_entry.grid(row=8, column=1, padx=10, pady=10)
        self.date_sortie_entry.insert(0, "YYYY-MM-DD")
        self.date_sortie_entry.bind("<FocusIn>", lambda event: self.date_sortie_entry.delete(0, "end"))
      
       # configurer le style des buttons------
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#d9d2e9", foreground="black", font=("Courier New", 12))
     
        self.ajout_button=ttk.Button(left_container, text="Ajouter Produit",style="TButton",width='20', command=self.Ajout_Produit)
        self.ajout_button.grid(row=9,column=1,columnspan=2,padx=10,pady=10)
        self.retourner_button=ttk.Button(left_container, text="Retourner", style="TButton",width='20',command=self.creer_Liste_Produit_Page)
        self.retourner_button.grid(row=10,column=1,columnspan=2,padx=10,pady=10)


        self.select_button = ttk.Button(right_container, text="Select File",style="TButton",width="20", command=lambda:[self.choose_file(right_container)])
        self.select_button.grid(row=1,column=1,columnspan=2,padx=10,pady=10)
        
        # Ajout de l'image du produit
        image = Image.open(self.image_path)
        image = image.resize((200, 200), Image.ANTIALIAS)  # Redimensionnement de l'image
        self.photo = ImageTk.PhotoImage(image)
        self.label_image = tk.Label(right_container, image=self.photo)
        self.label_image.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
       
       
        
        
        
   
    def choose_file(self,right_container):# responsable à l'affichage des images choisi à partir du button select file
        file_path = filedialog.askopenfilename()
        if file_path:
           # self.image_entry.delete(0, tk.END)
            #self.image_entry.insert(0, file_path)
            self.image_path=file_path
            image = Image.open(self.image_path)
            image = image.resize((200, 200), Image.ANTIALIAS)  # Redimensionnement de l'image
            self.photo = ImageTk.PhotoImage(image)
            self.label_image = tk.Label(right_container, image=self.photo)
            self.label_image.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
   
    def Ajout_Produit(self):
        # Get the values from the entry widgets
        name = self.nom_produit_entry .get()
        description = self.description_entry.get()
        price = self.prix_entry.get()
        quantity = self.quantite_entry.get()
        alert_quantity = self.seuil_alerte_entry.get()
        last_entry = self.date_entree_entry.get()
        last_exit = self.date_sortie_entry.get()
      
        if self.connected_admin[0]:
          product = ProduitDAO(new_produit=Produit(name, description, price, quantity, alert_quantity, last_entry, last_exit, self.image_path, id_admin=self.connected_admin[0]))
        # Add the product to the database
          if product.ajouter_produit():
            messagebox.showinfo("Success", "Product added successfully")
          else:
            messagebox.showerror("Error", "Failed to add product")
        else:
           messagebox.showerror("Error", "Failed to authenticate admin")
       
   
    def creer_Affichage_Admin_Page(self):# creation de la page qui affiche tous les infos de l'admin
        # Créer la barre de navigation
        self.main_container=tk.Frame(self,bg='white')
        self.main_container.place(x=0,y=0,relwidth=1,relheight=1)
        
        self.navbar_frame = tk.Frame(self.main_container, bg="#d4cae8", height=50)
        self.navbar_frame.place(x=0,y=0,relwidth=1)
        # Ajouter des boutons à la barre de navigation
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Navbar.TButton", padding=10, relief="flat", background="#d4cae8", foreground="white", font=("Arial", 14, "bold"))
        
        self.mes_produits_button = ttk.Button(self.navbar_frame, text="Mes Produits", style="Navbar.TButton",command=lambda:[self.clear_widgets(),self.creer_Liste_Produit_Page()])
        self.mes_produits_button.grid(row=0, column=0, padx=20, pady=5)

        self.mon_profil_button = ttk.Button(self.navbar_frame, text="Mon Profil", style="Navbar.TButton",command=lambda:[self.clear_widgets(),self.creer_Affichage_Admin_Page()])
        self.mon_profil_button.grid(row=0, column=1, padx=20, pady=5)

        self.deconnexion_button = ttk.Button(self.navbar_frame, text="Deconnexion", style="Navbar.TButton",command=lambda:[self.clear_widgets(),self.creer_Login_Page()])
        self.deconnexion_button.grid(row=0, column=2, padx=20, pady=5)
        self.grid_columnconfigure(0, weight=1)
       
        #styler les entry
        style = ttk.Style()
        style.configure('TEntry', padding=5, relief='flat', background='#d4cae8', foreground='#212529', font=('Courier New', 12))
        #conteneur des informations de l'admin 
        self.container=tk.Frame(self.main_container,bg='white')
        self.container.place(relx=0.5,rely=0.5,anchor='center')
       
        # Ajouter des classes Bootstrap à votre conteneur
        self.container.configure(highlightbackground="#ccc", highlightthickness=1)
        self.container.configure(borderwidth=1)
        self.container.configure(padx=10, pady=10)
        self.container.configure(relief="ridge")
        self.container.configure(width=400)
        
        # Create the username label and entry widget
        tk.Label(self.container, text="Vos Informations Personnelles", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2)

        
        
        self.username_label = ttk.Label(self.container, text="Username:", font=("Courier New", 12))
        self.username_entry = ttk.Entry(self.container, style='TEntry', width='40')
        self.username_label.grid(row=1, column=0, padx=10, pady=10)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)
        # Create the password label and entry widget
        self.password_label = ttk.Label(self.container, text="Password:", font=("Courier New", 12))
        self.password_entry = ttk.Entry(self.container, style='TEntry', width='40')
        self.password_label.grid(row=2, column=0, padx=10, pady=10)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)
        #Create the fullname label and entry widget
        self.fullname_label = ttk.Label(self.container, text="Fullname:", font=("Courier New", 12))
        self.fullname_entry = ttk.Entry(self.container, style='TEntry', width='40')
        self.fullname_label.grid(row=3, column=0, padx=10, pady=10)
        self.fullname_entry.grid(row=3, column=1, padx=10, pady=10)
        # Create the email label and entry widget
        self.email_label = ttk.Label(self.container, text="Email:", font=("Courier New", 12))
        self.email_entry = ttk.Entry(self.container, style='TEntry', width='40')
        self.email_label.grid(row=4, column=0, padx=10, pady=10)
        self.email_entry.grid(row=4, column=1, padx=10, pady=10)
        # Create the tel label and entry widget
        self.tel_label = ttk.Label(self.container, text="Telephone:", font=("Courier New", 12))
        self.tel_entry = ttk.Entry(self.container, style='TEntry', width='40')
        self.tel_label.grid(row=5, column=0, padx=10, pady=10)
        self.tel_entry.grid(row=5, column=1, padx=10, pady=10)
     
        # configurer le style des buttons------
        style.configure("TButton", padding=6, relief="flat", background="#d9d2e9", foreground="black", font=("Courier New", 12))
        # Create the login button
        self.modify_button = ttk.Button(self.container, text="Modifier", style="TButton", width='20',command=self.Modifier_Admin)
        self.modify_button.grid(row=7, column=1, padx=10, pady=10)
    
        self.delete_button = ttk.Button(self.container, text="Supprimer Votre compte ", style="TButton", width='20',command=self.Supprimer_Admin)
        self.delete_button.grid(row=7, column=2, padx=10, pady=10)
        
        print(self.connected_admin)
        # Affiche les informations dans les widgets correspondants
        self.username_entry.insert(0,self.connected_admin[1])
        self.password_entry.insert(0,self.connected_admin[2])
        self.fullname_entry.insert(0,self.connected_admin[3])
        self.email_entry.insert(0,self.connected_admin[4])
        self.tel_entry.insert(0,self.connected_admin[5])
   
    def Modifier_Admin(self):
        fullname=self.fullname_entry.get()
        password=self.password_entry.get()
        email=self.email_entry.get()
        tel=self.tel_entry.get()
        username=self.username_entry.get()
        self.connected_admin=self.get_admin_logged_in()
        print("avant")
        print(self.connected_admin)
        if self.connected_admin:
             ad = self.admin_instance.modifier_admin_by_id(username,password,fullname,email,tel,self.connected_admin[0]) # user donc contient l'objet de type admin qui a l username et  password indique
             if ad:
                print("modification done ")
                self.connected_admin=self.admin_instance.authentifier_admin(username,password)
                print("apres")
                print(self.connected_admin)
             else:
                 print("username exist ")
        else:
           print(" unconnected admin echec to modify")
           return False 
   
    def Supprimer_Admin(self):
        if messagebox.askokcancel("Confirmation", "Voulez-vous vraiment supprimer cet admin , les  produits que  vous avez crée vont supprimer aussi ?"):
            produits_deleted = ProduitDAO().Supprimer_Produit_By_Id_Admin(self.connected_admin[0])
            print("connected admin\n",self.connected_admin)
            if produits_deleted:
                print("l'admin a des produits , ils sont supprimés")
                deleted = self.admin_instance.supprimer_admin_by_id(self.connected_admin[0])
            
                if deleted:
                    self.clear_widgets()
                    self.creer_Login_Page()
                    print("deleted",self.connected_admin)
                else:
                    print("echec de suppression de l'admin ")
            else:
                print("l'admin n'a jamais crée  des produits")
                deleted = self.admin_instance.supprimer_admin_by_id(self.connected_admin[0])
                if deleted:
                    self.clear_widgets()
                    self.creer_Login_Page()
                    print("deleted",self.connected_admin)
                else:
                    print("echec de suppression de l'admin ")
                

        else:
            print("Suppression annulée par l'administrateur")
   
    def creer_SignUp_Page(self):
        
            self.clear_widgets()
            # Créer le conteneur
            self.sign_up_page_container = tk.Frame(self, borderwidth=5, relief="flat")
            self.sign_up_page_container.grid(row=0, column=0, sticky="nsew")        # configurer les entry et label
            style = ttk.Style()
            # Créer l'image de fond
            self.background_image = Image.open("photo.png")
            self.background_photo = ImageTk.PhotoImage(self.background_image)
            self.background_label = tk.Label(self.sign_up_page_container, image=self.background_photo)
            self.background_label.place(relwidth=1,relheight=1)
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            
            self.background_label.bind('<Configure>', self._resize_image)

            style.configure('TEntry', padding=5, relief='flat', font=('Courier New', 15,'bold'))
            style.configure('TLabel', padding=5, relief='flat', font=('Courier New', 15,'bold'))  
            # configurer le style des buttons
            style.configure("TButton", padding=6, relief="flat", font=("Courier New", 12,'bold'))
            style.map("TButton",
                    foreground=[('pressed', 'white'), ('active', 'white')],
                    background=[('pressed', '#007bff'), ('active', '#0069d9')])

            self.form_signup=tk.Frame(self.sign_up_page_container, borderwidth=5, relief="flat", background="white")
            self.form_signup.place(relx=0.5,rely=0.5,anchor="center")
            tk.Label(self.form_signup, text="Sign Up", background="#d4cae8",font=("Courier New", 25,'italic','bold')).grid(row=0, column=0, columnspan=2,sticky='news')
                
           
            # Ajouter des widgets pour saisir les informations de l'utilisateur
            style = ttk.Style()
            style.configure('TEntry', padding=5, relief='flat', background='#f8f9fa', foreground='#212529')
            self.fullname_label = ttk.Label(self.form_signup, text="Fullname:", font=("Courier New", 12))
            self.fullname_entry = ttk.Entry(self.form_signup, style='TEntry', width='40')
            self.email_label = ttk.Label(self.form_signup, text="Email:", font=("Courier New", 12))
            self.email_entry = ttk.Entry(self.form_signup, style='TEntry', width='40')
            self.tel_label = ttk.Label(self.form_signup, text="Tel:", font=("Courier New", 12))
            self.tel_entry = ttk.Entry(self.form_signup, style='TEntry', width='40')
            self.username_label = ttk.Label(self.form_signup, text="Username: ", font=("Courier New", 12))
            self.username_entry = ttk.Entry(self.form_signup, style='TEntry', width='40')
            self.password_label = ttk.Label(self.form_signup, text="Password : ", font=("Courier New", 12))
            self.password_entry = ttk.Entry(self.form_signup, style='TEntry', width='40', show='*')
            # style buttons------
            style = ttk.Style()
            style.configure("TButton", padding=6, relief="flat", background="#d9d2e9", foreground="black", font=("Courier New", 12))
            self.create_user_button = ttk.Button(self.form_signup, text="Create account", style="TButton", width='20', command=lambda:[self.create_user(),self.clear_widgets(),self.vider_login_container(),self.creer_Login_Page()])
            # Afficher les widgets en utilisant Grid
            self.fullname_label.grid(row=1, column=0, padx=5, pady=5)
            self.fullname_entry.grid(row=1, column=1, padx=5, pady=5)
            self.email_label.grid(row=2, column=0, padx=5, pady=5)
            self.email_entry.grid(row=2, column=1, padx=5, pady=5)
            self.tel_label.grid(row=3, column=0, padx=5, pady=5)
            self.tel_entry.grid(row=3, column=1, padx=5, pady=5)
            self.username_label.grid(row=4, column=0, padx=5, pady=5)
            self.username_entry.grid(row=4, column=1, padx=5, pady=5)
            self.password_label.grid(row=5, column=0, padx=5, pady=5)
            self.password_entry.grid(row=5, column=1, padx=5, pady=5)
            self.create_user_button.grid(row=6, column=1, padx=5, pady=5)
           
            
   
           

           
   
            for widget in self.login_page_container.winfo_children():
                        widget.grid_forget()
                        widget.place_forget()
            
            


     
    def create_user(self):
        # Récupérer les informations saisies
        fullname=self.fullname_entry.get()
        email=self.email_entry.get()
        tel=self.tel_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
        else:
            # Créer une instance de la classe User
            new_user=AdminDAO(admin=Admin(username,password,fullname,email,tel))
            # Ajouter l'utilisateur à la base de données ou à une liste d'utilisateurs
            if new_user.ajouter_admin(username):#ici j'ai passé username comme arg pour chercher si username déjà existe 
                print("User added successfully!")
                messagebox.showinfo("info","User added successfully!")
                self.clear_widgets()
                self.creer_Login_Page()

            else:
                 print("username already exist")
                 messagebox.showerror("Erreur", "username already exist") 
                 

        
        # Effacer les champs de saisie
        self.fullname_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.tel_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    
    def creer_Page_Acceuil(self):
        if self.connected_admin:
            # Créer le container principal
            self.clear_widgets()
            self.container = tk.Frame(self)
            self.container.grid(row=0, column=0, sticky="nsew")
            self.container.grid_rowconfigure(1, weight=1)
            self.container.grid_columnconfigure(0, weight=1)
            
            # Créer la barre de navigation
            self.navbar_frame = tk.Frame(self.container, bg="#d4cae8", height=50)
            self.navbar_frame.grid(row=0, column=0, columnspan=2, sticky="news")
            self.navbar_frame.grid_rowconfigure(0, weight=1)  # configuration de la ligne pour prendre de la place
            self.navbar_frame.grid_columnconfigure((0, 1, 2), weight=1)  # configuration des colonnes pour prendre de la place
            
            # Ajouter des boutons à la barre de navigation
            self.style = ttk.Style()
            self.style.theme_use('clam')
            self.style.configure("Navbar.TButton", padding=10, relief="flat", background="#d4cae8", foreground="white", font=("Arial", 14, "bold"))

            self.mes_produits_button = ttk.Button(self.navbar_frame, text="Mes Produits", style="Navbar.TButton",command=lambda:[self.clear_widgets(),self.creer_Liste_Produit_Page()])
            self.mes_produits_button.grid(row=0, column=0, padx=20, pady=5)

            self.mon_profil_button = ttk.Button(self.navbar_frame, text="Mon Profil", style="Navbar.TButton",command=lambda:[self.clear_widgets(),self.creer_Affichage_Admin_Page()])
            self.mon_profil_button.grid(row=0, column=1, padx=20, pady=5)

            self.deconnexion_button = ttk.Button(self.navbar_frame, text="Deconnexion", style="Navbar.TButton",command=lambda:[self.clear_widgets(),self.creer_Login_Page()])
            self.deconnexion_button.grid(row=0, column=2, padx=20, pady=5)
        
            # Créer l'image de fond
            self.background_image = Image.open("photo.png")
            self.background_photo = ImageTk.PhotoImage(self.background_image)
            self.background_label = tk.Label(self.container, image=self.background_photo)
            self.background_label.grid(row=1, column=0, columnspan=2, sticky="nsew")
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            
            self.background_label.bind('<Configure>', self._resize_image)



    def _resize_image(self, event):
        if abs(event.width - self.current_width) > 10 or abs(event.height - self.current_height) > 10:
            self.current_width = event.width
            self.current_height = event.height
            new_width = event.width
            new_height = event.height
            self.image = self.background_image.resize((new_width, new_height))
            self.background_photo = ImageTk.PhotoImage(self.image)
            self.background_label.configure(image=self.background_photo)


   
    def creer_Liste_Produit_Page(self):
            self.clear_widgets()
    
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            self.navbar_frame = tk.Frame(self, bg='#6a4ab4', width=1000)
            self.navbar_frame.place(x=0, y=0, relheight=1)
            
            # Créer le cadre pour la barre de recherche
            search_frame = tk.Frame(self.navbar_frame, bg='#6a4ab4', width=400, height=40)
            search_frame.place(x=0, y=0, relwidth=1)
            # Ajouter un texte au-dessus de la barre de recherche
            text_label = tk.Label(search_frame, text="Recherche de produits", bg="#6a4ab4", fg="#FFFFFF", font=("Arial", 12, "bold"))
            text_label.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
            # Ajouter la zone de texte pour la recherche
            self.search_var = tk.StringVar()
            search_entry = ttk.Entry(search_frame, width=20, textvariable=self.search_var, font=("Arial", 12))
            search_entry.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

            # Ajouter le bouton de recherche
            search_button = ttk.Button(search_frame, text="Rechercher", command=self.affiche_produit_par_nom)
            search_button.grid(row=3, column=0, padx=5, pady=5)


            # Ajouter le texte en bas de la barre de recherche
            text_label = tk.Label(search_frame, text="Sélectionnez un prix:", bg="#6a4ab4", fg="#FFFFFF", font=("Arial", 12,'bold'))
            text_label.grid(row=4, column=0, padx=5, pady=5)

            # Ajouter le scale en bas de la barre de recherche
            self.scale_var = tk.DoubleVar()
            self.scale_var.set(0) # valeur initiale
            style = ttk.Style()
            style.configure('Horizontal.TScale', background='white', troughcolor='white', sliderlength=20, sliderthickness=15, sliderrelief='flat', foreground='#007BFF')
            scale = ttk.Scale(search_frame, from_=0, to=500, variable=self.scale_var, orient="horizontal", length=200, command=lambda var=self.scale_var: self.affiche_produit_par_prix(var), style='Horizontal.TScale')
            scale.grid(row=5, column=0, padx=5, pady=5)
             
            value_label = tk.Label(search_frame, textvariable=self.scale_var)
            value_label.grid(row=6, column=0, padx=5, pady=5)


            

            # Styliser la barre de recherche
            self.style.configure("Search.TEntry", padding=5, relief="flat", background="#FFFFFF", foreground="#495057", font=("Arial", 12))
            search_entry.config(style="Search.TEntry")
            self.style.configure("Search.TButton", padding=5, relief="flat", background="gray", foreground="#FFFFFF", font=("Arial", 12,'bold'))
            search_button.config(style="Search.TButton")
            # ajouter bouton ajout produit 
            self.style = ttk.Style()
            self.style.theme_use('clam')
            self.style.configure("Navbar.TButton", padding=10, relief="ridge", background="#6a4ab4", foreground="white", font=("Arial", 15, "bold"))
            Ajout_button = ttk.Button(search_frame, text="Ajouter un produit ",style="Navbar.TButton",command=self.creer_Ajout_Produit_Page)
            Ajout_button.grid(row=7, column=0, padx=5, pady=5,sticky="s")
            home_page_button = ttk.Button(search_frame, text="Page  Acceuil ",style="Navbar.TButton",command=self.creer_Page_Acceuil)
            home_page_button.grid(row=0, column=0, padx=5, pady=5,sticky="s")
            
            
            #canvas pour nous permet de utiliser scrollbar
            self.canvas = tk.Canvas(self, bg='white')
            self.canvas.place(x=200, y=0, relwidth=1, relheight=1)
            #self.canvas.config(width=self.winfo_width(),height=self.winfo_height())
            
            
            #creation de scrollbar
            self.scrollbar=ttk.Scrollbar(self,orient=VERTICAL,command=self.canvas.yview)
            self.scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")         
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            #scroll the whole box of canvas
            self.canvas.bind('<Configure>',lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            # second frame c'est le conteneur des produits 
            self.secondframe=tk.Frame(self.canvas)
            self.canvas.create_window((0,0),window=self.secondframe,anchor="nw")
            self.secondframe.place(x=0, y=0, relwidth=1, relheight=1)
            produits=ProduitDAO().recuperer_tous_les_produits(self.connected_admin[0])
            self.images = []
                                
            cadre_style = {'bg': 'white', 'bd': 1, 'relief': 'solid', 'highlightthickness': 0, 'padx': 5, 'pady': 5, 'width':350, 'borderwidth': 1}

            for i, produit in enumerate(produits):
                    
                    self.secondframe.columnconfigure((0,1,2), uniform=1)
                    self.secondframe.rowconfigure((1,2,3), uniform=1)

                    self.produit_frame = tk.Frame(self.secondframe, height=250,**cadre_style)
                    self.produit_frame.grid(row=(i//4)+1, column=i%4, padx=5, pady=5, sticky="nwse")
                    # Ajout de l'image du produit
                    image_path = produit[8] # Chemin vers l'image du produit dans la base de données
                    image = Image.open(image_path)
                    image = image.resize((200, 200), Image.ANTIALIAS)  # Redimensionnement de l'image
                    self.photo = ImageTk.PhotoImage(image)
                    self.images.append(self.photo)  # Ajout de la photo dans une liste pour éviter qu'elle ne soit supprimée
                    self.label_image = tk.Label(self.produit_frame, image=self.photo, bg='white', anchor='center', padx=0, pady=0)
                    self.label_image.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
                    # Ajout du nom du produit
                    self.label_nom = tk.Label(self.produit_frame, text=produit[1], font=('Helvetica', 16))
                    self.label_nom.grid(row=1, column=0, padx=10, pady=5, sticky='w')

                    # Ajout du prix du produit
                    self.label_prix = tk.Label(self.produit_frame, text=produit[2], font=('Helvetica', 14))
                    self.label_prix.grid(row=1, column=1, padx=10, pady=5, sticky='e')

                    # Ajout d'autres informations du produit
                    self.label_info = tk.Label(self.produit_frame, text=produit[3], font=('Helvetica', 12))
                    self.label_info.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
                    # Ajout du bouton de modification
                    #self.modifier_produit = functools.partial(self.modifier_Produit_Page, produit[0])
                    self.bouton_modifier = tk.Button(self.produit_frame, text='Modifier',bg='#6a4ab4',fg='white',command=lambda:[self.clear_widgets(),print(produit),self.modifier_produit_page(prod=produit)])
                    self.bouton_modifier.grid(row=3, column=0, padx=10, pady=10)

                    # Ajout du bouton de suppression
                    #self.supprimer_produit = functools.partial(self.supprimer_Produit_Page, produit[0])
                    self.bouton_supprimer = tk.Button(self.produit_frame, text='Supprimer',bg='#6a4ab4',fg='white', command=lambda id_prod=produit[0]: self.supprimer_Produit_Page(id_prod))
                    self.bouton_supprimer.grid(row=3, column=1, padx=10, pady=10)  
                    # Configurer la disposition des lignes et des colonnes du conteneur des produits
                    for i in range(4):
                        
                        self.columnconfigure(i, weight=1)
                        self.rowconfigure(i//4+1, weight=1)
            
        
                
      
    
    def affiche_produit_par_prix(self,var):
        
        print("prix",var)
        produits=ProduitDAO().recherche_produit_par_prix(var)
        print("produits :",produits)
        self.images = []
                            
        cadre_style = {'bg': 'white', 'bd': 1, 'relief': 'solid', 'highlightthickness': 0, 'padx': 5, 'pady': 5, 'width':350, 'borderwidth': 1}
        
        for widget in self.secondframe.winfo_children():
                widget.grid_forget()
                widget.place_forget()
       
        if len(produits)>1:
            
            for i, produit in enumerate(produits):
                    
                    self.secondframe.columnconfigure((0,1,2), uniform=1)
                    self.secondframe.rowconfigure((1,2,3), uniform=1)

                    self.produit_frame = tk.Frame(self.secondframe, height=250,**cadre_style)
                    self.produit_frame.grid(row=(i//4)+1, column=i%4, padx=5, pady=5, sticky="nwse")
                    # Ajout de l'image du produit
                    image_path = produit[8] # Chemin vers l'image du produit dans la base de données
                    image = Image.open(image_path)
                    image = image.resize((200, 200), Image.ANTIALIAS)  # Redimensionnement de l'image
                    self.photo = ImageTk.PhotoImage(image)
                    self.images.append(self.photo)  # Ajout de la photo dans une liste pour éviter qu'elle ne soit supprimée
                    self.label_image = tk.Label(self.produit_frame, image=self.photo, bg='white', anchor='center', padx=0, pady=0)
                    self.label_image.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
                    # Ajout du nom du produit
                    self.label_nom = tk.Label(self.produit_frame, text=produit[1], font=('Helvetica', 16))
                    self.label_nom.grid(row=1, column=0, padx=10, pady=5, sticky='w')

                    # Ajout du prix du produit
                    self.label_prix = tk.Label(self.produit_frame, text=produit[2], font=('Helvetica', 14))
                    self.label_prix.grid(row=1, column=1, padx=10, pady=5, sticky='e')

                    # Ajout d'autres informations du produit
                    self.label_info = tk.Label(self.produit_frame, text=produit[3], font=('Helvetica', 12))
                    self.label_info.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
                    # Ajout du bouton de modification
                    #self.modifier_produit = functools.partial(self.modifier_Produit_Page, produit[0])
                    self.bouton_modifier = tk.Button(self.produit_frame, text='Modifier',bg='#6a4ab4',fg='white',command=lambda:[self.clear_widgets(),print(produit),self.modifier_produit_page(produit)])
                    self.bouton_modifier.grid(row=3, column=0, padx=10, pady=10)

                    # Ajout du bouton de suppression
                    #self.supprimer_produit = functools.partial(self.supprimer_Produit_Page, produit[0])
                    self.bouton_supprimer = tk.Button(self.produit_frame, text='Supprimer',bg='#6a4ab4',fg='white', command=lambda id_prod=produit[0]: self.supprimer_Produit_Page(id_prod))
                    self.bouton_supprimer.grid(row=3, column=1, padx=10, pady=10)  
                    # Configurer la disposition des lignes et des colonnes du conteneur des produits
                    for i in range(4):
                        
                        self.columnconfigure(i, weight=1)
                        self.rowconfigure(i//+1, weight=1)
        
        elif len(produits)==1:
          
                self.secondframe.columnconfigure((0,1,2), uniform=1)
                self.secondframe.rowconfigure((1,2,3), uniform=1)
                self.produit_frame = tk.Frame(self.secondframe, height=250,**cadre_style)
                self.produit_frame.grid(row=1, column=0, sticky="nsew")
                # Si un seul produit est trouvé, afficher ses informations dans le cadre principal
                self.produit_frame.columnconfigure((0, 1), weight=1) 
                self.produit_frame.rowconfigure((0, 1, 2, 3), weight=1)
                # Ajout de l'image du produit
                image_path = produits[0][8] # Chemin vers l'image du produit dans la base de données
                image = Image.open(image_path)
                image = image.resize((200, 200), Image.ANTIALIAS)  # Redimensionnement de l'image
                self.photo = ImageTk.PhotoImage(image)
                #self.images.append(self.photo)  # Ajout de la photo dans une liste pour éviter qu'elle ne soit supprimée
                self.label_image = tk.Label(self.produit_frame, image=self.photo, bg='white', anchor='center', padx=0, pady=0)
                self.label_image.grid(row=0, column=0, padx=10, pady=10,sticky='ew')

                # Ajout du nom du produit
                self.label_nom = tk.Label(self.produit_frame, text=produits[0][1], font=('Helvetica', 18))
                self.label_nom.grid(row=1, column=0, padx=10, pady=5, sticky='w')

                # Ajout du prix du produit
                self.label_prix = tk.Label(self.produit_frame, text=produits[0][2], font=('Helvetica', 16))
                self.label_prix.grid(row=1, column=1, padx=10, pady=5, sticky='e')

                # Ajout d'autres informations du produit
                self.label_info = tk.Label(self.produit_frame, text=produits[0][3], font=('Helvetica', 14))
                self.label_info.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
                # Ajout du bouton de modification
                self.bouton_modifier = tk.Button(self.produit_frame, text='Modifier', bg='#ADD8E6', fg='white', command=lambda:[self.clear_widgets(), self.modifier_produit_page(produits[0])])
                self.bouton_modifier.grid(row=3, column=0, padx=10, pady=10)

                # Ajout du bouton de suppression
                self.bouton_supprimer = tk.Button(self.produit_frame, text='Supprimer', bg='#ADD8E6', fg='white', command=lambda id_prod=produits[0][0]: self.supprimer_Produit_Page(id_prod))
                self.bouton_supprimer.grid(row=3, column=1, padx=10, pady=10)
                       
                self.columnconfigure(0, weight=1)
                self.rowconfigure(0, weight=1)
            
     
    
    def affiche_produit_par_nom(self):
        
        cadre_style = {'bg': 'white', 'bd': 1, 'relief': 'solid', 'highlightthickness': 0, 'padx': 5, 'pady': 5, 'width':350, 'borderwidth': 1}

        if len(self.search_var.get())==0:
            for widget in self.secondframe.winfo_children():
                widget.grid_forget()
                widget.place_forget()
              
            #au debut si la barre de recherche est vide il affiche tout
            produits=ProduitDAO().recuperer_tous_les_produits(self.connected_admin[0])
            self.images = []
                            
           
            for i, produit in enumerate(produits):
                
                self.secondframe.columnconfigure((0,1,2), uniform=1)
                self.secondframe.rowconfigure((1,2,3), uniform=1)

                self.produit_frame = tk.Frame(self.secondframe, height=250,**cadre_style)
                self.produit_frame.grid(row=(i//5)+1, column=i%5, padx=5, pady=5, sticky="nwse")
                # Ajout de l'image du produit
                image_path = produit[8] # Chemin vers l'image du produit dans la base de données
                image = Image.open(image_path)
                image = image.resize((200, 200), Image.ANTIALIAS)  # Redimensionnement de l'image
                self.photo = ImageTk.PhotoImage(image)
                self.images.append(self.photo)  # Ajout de la photo dans une liste pour éviter qu'elle ne soit supprimée
                self.label_image = tk.Label(self.produit_frame, image=self.photo, bg='white', anchor='center', padx=0, pady=0)
                self.label_image.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
                self.produit_frame.columnconfigure(0, weight=1)
                self.produit_frame.rowconfigure(0, weight=1)
                # Ajout du nom du produit
                self.label_nom = tk.Label(self.produit_frame, text=produit[1], font=('Helvetica', 16))
                self.label_nom.grid(row=1, column=0, padx=10, pady=5, sticky='w')

                # Ajout du prix du produit
                self.label_prix = tk.Label(self.produit_frame, text=produit[2], font=('Helvetica', 14))
                self.label_prix.grid(row=1, column=1, padx=10, pady=5, sticky='e')

                # Ajout d'autres informations du produit
                self.label_info = tk.Label(self.produit_frame, text=produit[3], font=('Helvetica', 12))
                self.label_info.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
                # Ajout du bouton de modification
                #self.modifier_produit = functools.partial(self.modifier_Produit_Page, produit[0])
                self.bouton_modifier = tk.Button(self.produit_frame, text='Modifier',bg='#ADD8E6',fg='white',command=lambda:[self.clear_widgets(),print(produit),self.modifier_produit_page(produit)])
                self.bouton_modifier.grid(row=3, column=0, padx=10, pady=10)

                # Ajout du bouton de suppression
                #self.supprimer_produit = functools.partial(self.supprimer_Produit_Page, produit[0])
                self.bouton_supprimer = tk.Button(self.produit_frame, text='Supprimer',bg='#ADD8E6',fg='white', command=lambda id_prod=produit[0]: self.supprimer_Produit_Page(id_prod))
                self.bouton_supprimer.grid(row=3, column=1, padx=10, pady=10)
                            
                            
                            
                # Configurer la disposition des lignes et des colonnes du conteneur des produits
                for i in range(5):
                    
                    self.columnconfigure(i, weight=1)
                    self.rowconfigure(i//5+1, weight=1)
        else:
             
               
            produit=ProduitDAO().recherche_produit_par_nom(self.search_var.get())
            print(produit)  
            for widget in self.secondframe.winfo_children():
                widget.grid_forget()
                widget.place_forget()
              
           
            self.secondframe.columnconfigure((0,1,2), uniform=1)
            self.secondframe.rowconfigure((1,2,3), uniform=1)
            self.produit_frame = tk.Frame(self.secondframe, height=250,**cadre_style)
            self.produit_frame.grid(row=1, column=0, sticky="nsew")            # Si un seul produit est trouvé, afficher ses informations dans le cadre principal
      
            # Ajout de l'image du produit
            image_path = produit[8] # Chemin vers l'image du produit dans la base de données
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.ANTIALIAS)  # Redimensionnement de l'image
            self.photo = ImageTk.PhotoImage(image)
            #self.images.append(self.photo)  # Ajout de la photo dans une liste pour éviter qu'elle ne soit supprimée
            self.label_image = tk.Label(self.produit_frame, image=self.photo, bg='white', anchor='center', padx=0, pady=0)
            self.label_image.grid(row=0, column=0, padx=10, pady=10,sticky='nsew')
            self.produit_frame.columnconfigure(0, weight=1)
            self.produit_frame.rowconfigure(0, weight=1)

            # Ajout du nom du produit
            self.label_nom = tk.Label(self.produit_frame, text=produit[1], font=('Helvetica', 18))
            self.label_nom.grid(row=1, column=0, padx=10, pady=5, sticky='w')

            # Ajout du prix du produit
            self.label_prix = tk.Label(self.produit_frame, text=produit[2], font=('Helvetica', 16))
            self.label_prix.grid(row=1, column=1, padx=10, pady=5, sticky='e')

            # Ajout d'autres informations du produit
            self.label_info = tk.Label(self.produit_frame, text=produit[3], font=('Helvetica', 14))
            self.label_info.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
            # Ajout du bouton de modification
            self.bouton_modifier = tk.Button(self.produit_frame, text='Modifier', bg='#ADD8E6', fg='white', command=lambda:[self.clear_widgets(), print(produit), self.modifier_produit_page(produit)])
            self.bouton_modifier.grid(row=3, column=0, padx=10, pady=10)

            # Ajout du bouton de suppression
            self.bouton_supprimer = tk.Button(self.produit_frame, text='Supprimer', bg='#ADD8E6', fg='white', command=lambda id_prod=produit[0]: self.supprimer_Produit_Page(id_prod))
            self.bouton_supprimer.grid(row=3, column=1, padx=10, pady=10)
            print("coontrr",self.search_var.get())        
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
        
           
   
    def supprimer_Produit_Page(self,id_prod):
                result=ProduitDAO().Supprimer_Produit_By_Id_Produit(id_prod)
                if result:
                    print("supprimeé")
                    self.clear_widgets()
                    #affichage à nouveau des produits restant 
                    self.creer_Liste_Produit_Page()
                else:
                    print("echec de suppression")
   
    def modifier_produit_page(self,prod): 
            self.clear_widgets()
            style = ttk.Style()
            # conteneur grand
            self.container=tk.Frame(self,bg="white")
            self.container.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")
            #sous conteneurs ------
            
            # Création des deux sous-conteneurs égaux
            left_container = tk.Frame(self.container, bg="white")
            left_container.grid(row=0, column=0, sticky="nsew")
            right_container = tk.Frame(self.container, bg="white")
            right_container.grid(row=0, column=1, sticky="nsew")

            # Configuration de la grille de disposition pour diviser le grand conteneur en deux colonnes égales
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)
            
            tk.Label(left_container, text="Modifier produit ",background='white',font=("Courier New", 25,'italic','bold')).grid(row=0, column=0, columnspan=2,sticky='news')


            # Configuration de la grille de disposition pour diviser chaque sous-conteneur en une seule ligne et colonne
            left_container.rowconfigure(0, weight=1)
            left_container.columnconfigure(0, weight=1)
            right_container.rowconfigure(0, weight=1)
            right_container.columnconfigure(0, weight=1)
            
            
            # Create the nom_produit label and entry widget
            
            
            self.nom_produit_label = ttk.Label(left_container, text="Nom du produit:", font=("Courier New", 12))
            self.nom_produit_entry = ttk.Entry(left_container, style='TEntry', width='40')
            self.nom_produit_label.grid(row=1, column=0, padx=10, pady=10)
            self.nom_produit_entry.grid(row=1, column=1, padx=10, pady=10)
            # Create the description label and entry widget
            self.description_label = ttk.Label(left_container, text="Descritpion:", font=("Courier New", 12))
            self.description_entry = ttk.Entry(left_container, style='TEntry', width='40')
            self.description_label.grid(row=2, column=0, padx=10, pady=10)
            self.description_entry.grid(row=2, column=1, padx=10, pady=10)
            #Create the prix label and entry widget
            self.prix_entry = ttk.Entry(left_container, style='TEntry', width='40')
            self.prix_label = ttk.Label(left_container, text="Prix Unitaire:", font=("Courier New", 12))
            self.prix_label.grid(row=3, column=0, padx=10, pady=10)
            self.prix_entry.grid(row=3, column=1, padx=10, pady=10)
            # Create the quantite label and entry widget
            self.quantite_label = ttk.Label(left_container, text="Quantité en Stock:", font=("Courier New", 12))
            self.quantite_entry = ttk.Entry(left_container, style='TEntry', width='40')
            self.quantite_label.grid(row=4, column=0, padx=10, pady=10)
            self.quantite_entry.grid(row=4, column=1, padx=10, pady=10)
            # Create the seuil alerte label and entry widget
            self.seuil_alerte_label = ttk.Label(left_container, text="Seuil d'alerte:", font=("Courier New", 12))
            self.seuil_alerte_entry = ttk.Entry(left_container, style='TEntry', width='40')
            self.seuil_alerte_label.grid(row=6, column=0, padx=10, pady=10)
            self.seuil_alerte_entry.grid(row=6, column=1, padx=10, pady=10)
            # Create the seuil date_entree label and entry widget
            self.date_entree_label = ttk.Label(left_container, text="Date entrée:", font=("Courier New", 12))
            self.date_entree_entry = ttk.Entry(left_container, style='TEntry', width='40')
            self.date_entree_label.grid(row=7, column=0, padx=10, pady=10)
            self.date_entree_entry.grid(row=7, column=1, padx=10, pady=10)
            # Create the seuil date_sortie label and entry widget
            self.date_sortie_label = ttk.Label(left_container, text="Date Sortie:", font=("Courier New", 12))
            self.date_sortie_entry = ttk.Entry(left_container, style='TEntry', width='40')
            self.date_sortie_label.grid(row=8, column=0, padx=10, pady=10)
            self.date_sortie_entry.grid(row=8, column=1, padx=10, pady=10)
        
        
            # configurer le style des buttons------
            style.configure("TButton", padding=6, relief="flat", background="#d9d2e9", foreground="black", font=("Courier New", 12))
            # Create the login button
            self.modify_button = ttk.Button(left_container, text="Modifier", style="TButton", width='20',command=lambda:[self.confirm_modification_produit(prod)])
            self.modify_button.grid(row=9, column=1, padx=10, pady=10)
            self.modify_button = ttk.Button(left_container, text="Retourner", style="TButton", width='20',command=self.creer_Liste_Produit_Page)
            self.modify_button.grid(row=9, column=2, padx=10, pady=10)
    
            #print(self.connected_admin)
            # Affiche les informations dans les widgets correspondants
            self.nom_produit_entry.insert(0,prod[1])
            self.description_entry.insert(0,prod[2])
            self.prix_entry.insert(0,prod[3])
            self.quantite_entry.insert(0,prod[4])
            self.seuil_alerte_entry.insert(0,prod[5])
            self.date_entree_entry.insert(0,prod[6])
            self.date_sortie_entry.insert(0,prod[7])
            # Ajout de l'image du produit
            self.image_path = prod[8] # Chemin vers l'image du produit dans la base de données
            image = Image.open(self.image_path)
            image = image.resize((200, 200), Image.ANTIALIAS)  # Redimensionnement de l'image
            self.photo = ImageTk.PhotoImage(image)
            self.label_image = tk.Label(right_container, image=self.photo)
            self.label_image.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
            self.select_button = tk.Button(right_container, text="Select File", command=lambda:[self.choose_file(right_container)])
            self.select_button.grid(row=1,column=1,columnspan=2,padx=10,pady=10)
       
    def confirm_modification_produit(self,prod):
            # cette fonction fait appel à la fonction modifier produit de la classe ProduitDao 
            # prod est un tuple il faut qu'on transforme le en list pour qu'on  puisse changer son contenu 
            list_prod=list(prod)
            list_prod[1]=self.nom_produit_entry.get()
            list_prod[2]=self.description_entry.get()
            list_prod[3]=self.prix_entry.get()
            list_prod[4]=self.quantite_entry.get()
            list_prod[5]=self.seuil_alerte_entry.get()
            list_prod[6]=self.date_entree_entry.get()
            list_prod[7]=self.date_sortie_entry.get()
            list_prod[8]=self.image_path
            
            prod=tuple(list_prod)
            result=ProduitDAO().modifier_produit(prod)
            if result :
                messagebox.showinfo("Success", "Produit est modifié")
                print("produit modifié ")
            else:
                messagebox.showerror("Error", "echec de modifier ce produit")
                print("echec de modification")

        

                


            
        
root=tk.Tk()
app=MainApp(root)
app.creer_Login_Page()
root.mainloop()