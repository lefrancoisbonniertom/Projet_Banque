from tkinter import *
from tkinter import ttk, messagebox, simpledialog

class CompteBancaire:
    def __init__(self, nom, argent=0):
        self.nom = nom
        self.argent = argent
    
    def get_nom(self):
        return self.nom

    def get_argent(self):
        return self.argent

    def set_argent(self, variation):
        self.argent += variation
        if self.argent < 0:
            messagebox.showwarning("Attention", "Le compte est à découvert !")

    def depot(self, somme):
        self.set_argent(somme)

    def retrait(self, somme):
        self.set_argent(-somme)

    def __str__(self):
        return f"Le compte de {self.nom} contient {self.argent} euros."  # le f sert a faire un doc string pour servir au root de lancer l'ecriture du programme

class BanqueEnLigne:
    def __init__(self, root):
        self.root = root
        self.root.title("Banque en Ligne")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        # Base de données des comptes
        self.comptes = {}

        # Encadré du formulaire
        frame1 = Frame(self.root, bg="#007acc")
        frame1.place(x=50, y=50, width=700, height=200)

        # Titre
        Label(frame1, text="Formulaire d'inscription", font=("Arial", 18, "bold"), bg="#007acc", fg="white").place(x=200, y=10)

        # Champs du formulaire
        Label(frame1, text="Nom", bg="#007acc", fg="white", font=("Arial", 12)).place(x=50, y=60)
        self.entry_nom = Entry(frame1, font=("Arial", 12))
        self.entry_nom.place(x=200, y=60)

        Label(frame1, text="Dépôt Initial (€)", bg="#007acc", fg="white", font=("Arial", 12)).place(x=50, y=100)
        self.entry_initial_depot = Entry(frame1, font=("Arial", 12))
        self.entry_initial_depot.place(x=200, y=100)

        # Bouton de création du compte
        Button(frame1, text="Créer Compte", bg="#4caf50", fg="white", font=("Arial", 12), command=self.creer_compte).place(x=500, y=100)

        # Choix du compte
        Label(self.root, text="Sélectionner un compte :", font=("Arial", 12), bg="#f0f0f0").place(x=50, y=270)
        self.combo_comptes = ttk.Combobox(self.root, state="readonly", font=("Arial", 12))
        self.combo_comptes.place(x=250, y=270)
        self.combo_comptes.bind("<<ComboboxSelected>>", self.selectionner_compte)

        # Encadré des opérations
        frame2 = Frame(self.root, bg="white", highlightbackground="#007acc", highlightthickness=2)
        frame2.place(x=50, y=300, width=700, height=200)

        Label(frame2, text="Solde Actuel : ", font=("Arial", 14, "bold"), bg="white").place(x=50, y=20)
        self.solde_label = Label(frame2, text="0 €", font=("Arial", 14, "bold"), bg="white", fg="green")
        self.solde_label.place(x=200, y=20)

        Button(frame2, text="Déposer", bg="#4caf50", fg="white", font=("Arial", 12), command=self.deposer).place(x=50, y=80)
        Button(frame2, text="Retirer", bg="#f44336", fg="white", font=("Arial", 12), command=self.retirer).place(x=150, y=80)
        Button(frame2, text="Virement", bg="#007acc", fg="white", font=("Arial", 12), command=self.virement).place(x=250, y=80)

        # Compte sélectionné
        self.compte_actif = None

    def creer_compte(self):
        nom = self.entry_nom.get()
        # Vérifier si le champ du nom est vide
        if not nom:
            messagebox.showerror("Erreur", "Veuillez entrer un nom pour le compte.")
            return

        try:
            depot_initial = float(self.entry_initial_depot.get())
            # Vérifier si le dépôt initial est positif
            if depot_initial < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide pour le dépôt initial (doit être un nombre positif).")
            return

        # Vérification d'existence de compte
        if nom in self.comptes:
            messagebox.showerror("Erreur", "Un compte avec ce nom existe déjà.")
            return

        # Création du compte et mise à jour de la base de données
        nouveau_compte = CompteBancaire(nom, depot_initial)
        self.comptes[nom] = nouveau_compte
        self.maj_liste_comptes()
        messagebox.showinfo("Compte créé", f"Compte de {nom} créé avec succès ! Solde initial : {depot_initial} €")


    def maj_liste_comptes(self):
        # Met à jour la liste déroulante avec les comptes
        self.combo_comptes['values'] = list(self.comptes.keys())
        if not self.compte_actif:
            self.combo_comptes.set('')

    def selectionner_compte(self, event):
        nom_compte = self.combo_comptes.get()
        self.compte_actif = self.comptes.get(nom_compte)
        if self.compte_actif:
            self.solde_label.config(text=f"{self.compte_actif.get_argent()} €")

    def deposer(self):
        if not self.compte_actif:
            messagebox.showwarning("Attention", "Veuillez sélectionner un compte.")
            return
        montant = simpledialog.askfloat("Dépôt", "Montant à déposer (€) :")
        if montant is not None and montant > 0:
            self.compte_actif.depot(montant)
            self.solde_label.config(text=f"{self.compte_actif.get_argent()} €")
            messagebox.showinfo("Dépôt réussi", f"{montant} € déposés sur le compte {self.compte_actif.get_nom()}.")
        else:
            messagebox.showerror("Erreur", "Montant invalide ou négatif.")

    def retirer(self):
        if not self.compte_actif:
            messagebox.showwarning("Attention", "Veuillez sélectionner un compte.")
            return
        montant = simpledialog.askfloat("Retrait", "Montant à retirer (€) :")
        if montant is not None and montant > 0:
            if montant <= self.compte_actif.get_argent():
                self.compte_actif.retrait(montant)
                self.solde_label.config(text=f"{self.compte_actif.get_argent()} €")
                messagebox.showinfo("Retrait réussi", f"{montant} € retirés du compte {self.compte_actif.get_nom()}.")
            else:
                messagebox.showerror("Erreur", "Fonds insuffisants pour ce retrait.")
        else:
            messagebox.showerror("Erreur", "Montant invalide ou négatif.")

    def virement(self):
        if not self.compte_actif:
            messagebox.showwarning("Attention", "Veuillez sélectionner un compte.")
            return
        destinataire = simpledialog.askstring("Virement", "Nom du destinataire :")
        if not destinataire or destinataire not in self.comptes:
            messagebox.showerror("Erreur", "Compte destinataire introuvable.")
            return
        montant = simpledialog.askfloat("Virement", "Montant à virer (€) :")
        if montant is not None and montant > 0:
            if montant <= self.compte_actif.get_argent():
                # Effectuer le virement
                self.compte_actif.retrait(montant)
                self.comptes[destinataire].depot(montant)
                self.solde_label.config(text=f"{self.compte_actif.get_argent()} €")
                messagebox.showinfo("Virement réussi", f"{montant} € transférés à {destinataire}.")
            else:
                messagebox.showerror("Erreur", "Fonds insuffisants pour ce virement.")
        else:
            messagebox.showerror("Erreur", "Montant invalide ou négatif.")

root = Tk()
app = BanqueEnLigne(root)
root.mainloop()
