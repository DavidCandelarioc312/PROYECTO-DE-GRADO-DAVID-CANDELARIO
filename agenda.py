import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage  # Para cargar la imagen 
#dar la parte grafica del programa
import sqlite3
#Tener una base de datos simple dentro de python

#Programacio orientada a obejtos que se basa en clases y funciones

#Esta clase es la parte logica del programa 
class BaseDatosContactos:
    #Y estas funciones nos permite eliminar, agregar, buscar, mostrar e intercambiar datos 
    def __init__(self, db_name="agenda.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contactos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                correo TEXT
            )
        ''')
        self.conn.commit()

    def agregar_contacto(self, nombre, telefono, correo):
        self.cursor.execute("INSERT INTO contactos (nombre, telefono, correo) VALUES (?, ?, ?)", 
                            (nombre, telefono, correo))
        self.conn.commit()

    def eliminar_contacto(self, nombre):
        self.cursor.execute("DELETE FROM contactos WHERE nombre = ?", (nombre,))
        self.conn.commit()

    def buscar_contacto(self, nombre):
        self.cursor.execute("SELECT * FROM contactos WHERE nombre LIKE ?", ('%' + nombre + '%',))
        return self.cursor.fetchall()

    def obtener_todos(self):
        self.cursor.execute("SELECT * FROM contactos")
        return self.cursor.fetchall()

#esta clase es la parte grafica del programa lo que nos permite interactuar con la parte logica
class AgendaApp:
    def __init__(self, root):
        self.db = BaseDatosContactos()
        self.root = root
        self.root.title("Agenda de Contactos")

        self.logo = PhotoImage(file=r"C:\Users\JOSUE\Documents\Vscode\PROYECTO FINAL DAVID CANDELARIO\sello.png")
        tk.Label(root, image=self.logo).grid(row=0, column=2, rowspan=3, padx=10, pady=10)

        tk.Label(root, text="Nombre").grid(row=0, column=0)
        tk.Label(root, text="Teléfono").grid(row=1, column=0)
        tk.Label(root, text="Correo").grid(row=2, column=0)

        self.nombre = tk.Entry(root)
        self.telefono = tk.Entry(root)
        self.correo = tk.Entry(root)

        self.nombre.grid(row=0, column=1)
        self.telefono.grid(row=1, column=1)
        self.correo.grid(row=2, column=1)

        tk.Button(root, text="Agregar", command=self.agregar).grid(row=3, column=0, pady=5)
        tk.Button(root, text="Eliminar", command=self.eliminar).grid(row=3, column=1)
        tk.Button(root, text="Buscar", command=self.buscar).grid(row=4, column=0)
        tk.Button(root, text="Mostrar Todos", command=self.mostrar_todos).grid(row=4, column=1)

        self.text_area = tk.Text(root, width=50, height=15)
        self.text_area.grid(row=5, column=0, columnspan=3, pady=10)

    def agregar(self):
        nombre = self.nombre.get()
        telefono = self.telefono.get()
        correo = self.correo.get()
        if nombre and telefono:
            self.db.agregar_contacto(nombre, telefono, correo)
            messagebox.showinfo("Éxito", "Contacto agregado")
            self.limpiar()
            self.mostrar_todos()
        else:
            messagebox.showwarning("Advertencia", "Nombre y teléfono son obligatorios")

    def eliminar(self):
        nombre = self.nombre.get()
        if nombre:
            self.db.eliminar_contacto(nombre)
            messagebox.showinfo("Éxito", "Contacto eliminado")
            self.limpiar()
            self.mostrar_todos()
        else:
            messagebox.showwarning("Advertencia", "Escribe el nombre para eliminar")

    def buscar(self):
        nombre = self.nombre.get()
        if nombre:
            resultados = self.db.buscar_contacto(nombre)
            self.text_area.delete("1.0", tk.END)
            for r in resultados:
                self.text_area.insert(tk.END, f"ID: {r[0]}, Nombre: {r[1]}, Tel: {r[2]}, Email: {r[3]}\n")
        else:
            messagebox.showwarning("Advertencia", "Escribe un nombre para buscar")

    def mostrar_todos(self):
        contactos = self.db.obtener_todos()
        self.text_area.delete("1.0", tk.END)
        for c in contactos:
            self.text_area.insert(tk.END, f"ID: {c[0]}, Nombre: {c[1]}, Tel: {c[2]}, Email: {c[3]}\n")

    def limpiar(self):
        self.nombre.delete(0, tk.END)
        self.telefono.delete(0, tk.END)
        self.correo.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
