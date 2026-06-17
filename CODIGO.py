from tkinter import *
from tkinter import ttk, messagebox
import os

inventario = {}
archivo = "inventario.txt"

def cargar():
    try:
        f = open(archivo, "r")
        for linea in f:
            partes = linea.strip().split("|")
            if len(partes) == 4:
                inventario[partes[0]] = { "nombre": partes[1], "cantidad": int(partes[2]), "precio": float(partes[3]) }
        f.close()
    except:
        pass

def guardar():
    try:
        f = open(archivo, "w")
        for codigo in inventario:
            d = inventario[codigo]
            f.write(codigo + "|" + d["nombre"] + "|" + str(d["cantidad"]) + "|" + str(d["precio"]) + "\n")
        f.close()
    except:
        pass

def actualizar_tabla(filtro=""):
    for item in tabla.get_children():
        tabla.delete(item)
    for codigo in inventario:
        d = inventario[codigo]
        if filtro == "" or filtro.lower() in codigo.lower() or filtro.lower() in d["nombre"].lower():
            total = d["cantidad"] * d["precio"]
            tag = ""
            if d["cantidad"] <= 5:
                tag = "critico"
            tabla.insert("", END, values=(codigo, d["nombre"], d["cantidad"], "Bs " + str(d["precio"]), "Bs " + str(total)), tags=(tag,))
    actualizar_resumen()

def actualizar_resumen():
    total_prod = len(inventario)
    total_unds = 0
    valor_total = 0
    criticos = 0
    for codigo in inventario:
        d = inventario[codigo]
        total_unds = total_unds + d["cantidad"]
        valor_total = valor_total + (d["cantidad"] * d["precio"])
        if d["cantidad"] <= 5:
            criticos = criticos + 1
    label_res.config(text="productos: " + str(total_prod) + " | unidades: " + str(total_unds) + " | valor total: Bs " + str(valor_total))
    if criticos > 0:
        label_crit.config(text="ALERTA: " + str(criticos) + " producto(s) con stock critico", fg="red")
    else:
        label_crit.config(text="sin productos criticos", fg="green")

def agregar():
    codigo = entry_codigo.get().upper()
    nombre = entry_nombre.get()
    cant = entry_cantidad.get()
    precio = entry_precio.get()
    if codigo == "" or nombre == "":
        messagebox.showwarning("error", "codigo y nombre obligatorios")
        return
    try:
        cant_int = int(cant)
        if cant_int <= 0:
            messagebox.showwarning("error", "cantidad debe ser mayor a 0")
            return
    except:
        messagebox.showerror("error", "cantidad debe ser numero entero")
        return
    try:
        precio_float = float(precio)
        if precio_float <= 0:
            messagebox.showwarning("error", "precio debe ser mayor a 0")
            return
    except:
        messagebox.showerror("error", "precio debe ser numero")
        return
    if codigo in inventario:
        inventario[codigo]["cantidad"] = inventario[codigo]["cantidad"] + cant_int
        messagebox.showinfo("ok", "stock actualizado")
    else:
        inventario[codigo] = { "nombre": nombre, "cantidad": cant_int, "precio": precio_float }
        messagebox.showinfo("ok", "producto agregado")
    limpiar()
    actualizar_tabla(entry_buscar.get())
    guardar()

def vender():
    codigo = entry_codigo.get().upper()
    if codigo == "":
        messagebox.showwarning("error", "ingresa codigo")
        return
    if codigo not in inventario:
        messagebox.showerror("error", "codigo no existe")
        return
    cant = entry_cantidad.get()
    if cant == "":
        messagebox.showwarning("error", "ingresa cantidad")
        return
    try:
        cant_int = int(cant)
        if cant_int <= 0:
            messagebox.showwarning("error", "cantidad debe ser mayor a 0")
            return
    except:
        messagebox.showerror("error", "cantidad debe ser numero")
        return
    if cant_int > inventario[codigo]["cantidad"]:
        messagebox.showerror("error", "solo hay " + str(inventario[codigo]["cantidad"]) + " unidades")
        return
    inventario[codigo]["cantidad"] = inventario[codigo]["cantidad"] - cant_int
    messagebox.showinfo("venta", "venta realizada")
    if inventario[codigo]["cantidad"] <= 5:
        messagebox.showwarning("STOCK CRITICO", inventario[codigo]["nombre"] + " solo tiene " + str(inventario[codigo]["cantidad"]) + " unidades")
    limpiar()
    actualizar_tabla(entry_buscar.get())
    guardar()

def eliminar():
    codigo = entry_codigo.get().upper()
    if codigo == "":
        messagebox.showwarning("error", "ingresa codigo")
        return
    if codigo not in inventario:
        messagebox.showerror("error", "codigo no existe")
        return
    if messagebox.askyesno("confirmar", "eliminar " + inventario[codigo]["nombre"] + "?"):
        del inventario[codigo]
        messagebox.showinfo("ok", "eliminado")
        limpiar()
        actualizar_tabla(entry_buscar.get())
        guardar()

def limpiar():
    entry_codigo.delete(0, END)
    entry_nombre.delete(0, END)
    entry_cantidad.delete(0, END)
    entry_precio.delete(0, END)
    entry_codigo.focus()

def seleccionar(event):
    sel = tabla.selection()
    if len(sel) > 0:
        valores = tabla.item(sel[0])["values"]
        entry_codigo.delete(0, END)
        entry_codigo.insert(0, valores[0])
        entry_nombre.delete(0, END)
        entry_nombre.insert(0, valores[1])

def buscar_click():
    actualizar_tabla(entry_buscar.get())

def mostrar_todo():
    entry_buscar.delete(0, END)
    actualizar_tabla("")

cargar()

root = Tk()
root.title("Inventario Gaming Center")
root.geometry("850x500")
root.resizable(False, False)

frame_top = Frame(root, padx=10, pady=5)
frame_top.pack(fill=X)

Label(frame_top, text="BUSCAR:", font=("Arial", 9, "bold")).pack(side=LEFT, padx=(0, 5))
entry_buscar = Entry(frame_top, width=30, font=("Arial", 9))
entry_buscar.pack(side=LEFT, padx=(0, 5))
entry_buscar.bind("<KeyRelease>", lambda e: actualizar_tabla(entry_buscar.get()))
Button(frame_top, text="buscar", command=buscar_click, width=8).pack(side=LEFT, padx=(0, 5))
Button(frame_top, text="mostrar todo", command=mostrar_todo, width=10).pack(side=LEFT)

frame_izq = Frame(root, padx=10, pady=5)
frame_izq.pack(side=LEFT, fill=Y)

Label(frame_izq, text="DATOS", font=("Arial", 11, "bold")).pack(pady=(0, 10))

Label(frame_izq, text="codigo:", font=("Arial", 9)).pack(anchor=W)
entry_codigo = Entry(frame_izq, width=25, font=("Arial", 9))
entry_codigo.pack(pady=(0, 5))

Label(frame_izq, text="nombre:", font=("Arial", 9)).pack(anchor=W)
entry_nombre = Entry(frame_izq, width=25, font=("Arial", 9))
entry_nombre.pack(pady=(0, 5))

Label(frame_izq, text="cantidad:", font=("Arial", 9)).pack(anchor=W)
entry_cantidad = Entry(frame_izq, width=25, font=("Arial", 9))
entry_cantidad.pack(pady=(0, 5))

Label(frame_izq, text="precio (Bs):", font=("Arial", 9)).pack(anchor=W)
entry_precio = Entry(frame_izq, width=25, font=("Arial", 9))
entry_precio.pack(pady=(0, 10))

Button(frame_izq, text="AGREGAR", bg="#90EE90", command=agregar, width=22).pack(pady=2)
Button(frame_izq, text="VENDER", bg="#FFB6C1", command=vender, width=22).pack(pady=2)
Button(frame_izq, text="ELIMINAR", bg="#FF9999", command=eliminar, width=22).pack(pady=2)
Button(frame_izq, text="LIMPIAR", command=limpiar, width=22).pack(pady=2)

frame_der = Frame(root, padx=10, pady=5)
frame_der.pack(side=RIGHT, fill=BOTH, expand=True)

Label(frame_der, text="INVENTARIO", font=("Arial", 12, "bold")).pack()

scroll = Scrollbar(frame_der)
scroll.pack(side=RIGHT, fill=Y)

tabla = ttk.Treeview(frame_der, columns=("Codigo", "Nombre", "Stock", "Precio", "Total"), show="headings", yscrollcommand=scroll.set, height=18)
scroll.config(command=tabla.yview)

tabla.heading("Codigo", text="Codigo")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Stock", text="Stock")
tabla.heading("Precio", text="Precio")
tabla.heading("Total", text="Total Bs")

tabla.column("Codigo", width=70, anchor=CENTER)
tabla.column("Nombre", width=180)
tabla.column("Stock", width=60, anchor=CENTER)
tabla.column("Precio", width=80, anchor=CENTER)
tabla.column("Total", width=90, anchor=CENTER)

tabla.tag_configure("critico", foreground="red")

tabla.pack(fill=BOTH, expand=True, pady=5)
tabla.bind("<ButtonRelease-1>", seleccionar)

frame_info = Frame(frame_der)
frame_info.pack(fill=X)

label_res = Label(frame_info, text="productos: 0 | unidades: 0 | valor total: Bs 0", font=("Arial", 9))
label_res.pack(anchor=W)

label_crit = Label(frame_info, text="", font=("Arial", 9, "bold"))
label_crit.pack(anchor=W)

actualizar_tabla("")
entry_codigo.focus()

root.mainloop()