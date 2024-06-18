#Victor Eduardo Aleman Padilla

import tkinter as tk  # Importa el módulo tkinter y lo alias como tk
from tkinter import ttk, messagebox  # Importa ttk y messagebox desde tkinter
import heapq  # Importa el módulo heapq para utilizar colas de prioridad (heap)

class DijkstraGUI:
    def __init__(self, master):
        self.master = master  # Guarda la referencia a la ventana principal (root) en self.master
        self.master.title("Simulador de Árbol Parcial Mínimo de Prim")  # Establece el título de la ventana principal
        
        # Definición del grafo como un diccionario de diccionarios con pesos entre nodos
        self.graph = {
            'Trabajo': {'Casa': 1, 'Ceti': 4},
            'Casa': {'Trabajo': 1, 'Ceti': 2, 'Servicio': 5},
            'Ceti': {'Trabajo': 4, 'Casa': 2, 'Servicio': 1},
            'Servicio': {'Casa': 5, 'Ceti': 1}
        }
        
        # Creación de etiquetas y cuadros combinados (combobox) para seleccionar nodos de inicio y destino
        self.label_start = ttk.Label(master, text="Nodo de inicio:")  # Crea una etiqueta con texto
        self.label_start.grid(row=0, column=0, padx=10, pady=10)  # Coloca la etiqueta en la cuadrícula de la ventana
        
        self.start_var = tk.StringVar()  # Variable de control para el cuadro combinado de inicio
        self.start_combo = ttk.Combobox(master, textvariable=self.start_var, values=list(self.graph.keys()))
        # Crea un cuadro combinado con valores iniciales y asigna la variable de control
        self.start_combo.grid(row=0, column=1, padx=10, pady=10)  # Coloca el cuadro combinado en la cuadrícula
        
        # Define el evento de selección del cuadro de inicio para actualizar las opciones del cuadro de destino
        self.start_combo.bind('<<ComboboxSelected>>', self.update_end_options)
        
        # Creación de etiqueta y cuadro combinado para seleccionar nodo de destino
        self.label_end = ttk.Label(master, text="Nodo de destino:")
        self.label_end.grid(row=1, column=0, padx=10, pady=10)
        
        self.end_var = tk.StringVar()  # Variable de control para el cuadro combinado de destino
        self.end_combo = ttk.Combobox(master, textvariable=self.end_var, values=list(self.graph.keys()))
        # Crea un cuadro combinado con valores iniciales y asigna la variable de control
        self.end_combo.grid(row=1, column=1, padx=10, pady=10)  # Coloca el cuadro combinado en la cuadrícula
        
        # Etiqueta para mostrar el resultado del cálculo
        self.label_output = ttk.Label(master, text="Resultado:")
        self.label_output.grid(row=2, column=0, padx=10, pady=10)
        
        # Cuadro de texto para mostrar el resultado del cálculo
        self.output_text = tk.Text(master, height=6, width=30)
        self.output_text.grid(row=2, column=1, padx=10, pady=10)
        
        # Botón para iniciar el cálculo del árbol parcial mínimo usando Prim
        self.run_button = ttk.Button(master, text="Calcular Árbol Parcial Mínimo", command=self.calculate_mst)
        self.run_button.grid(row=3, columnspan=2, padx=10, pady=10)
    
    def update_end_options(self, event):
        # Método para actualizar las opciones del cuadro combinado de destino al seleccionar un inicio
        selected_start = self.start_var.get()  # Obtiene el nodo de inicio seleccionado
        valid_ends = list(self.graph[selected_start].keys())  # Obtiene los nodos válidos como destinos
        self.end_combo['values'] = valid_ends  # Actualiza los valores del cuadro combinado de destino
        self.end_var.set(valid_ends[0] if valid_ends else "")  # Establece el primer valor como selección inicial
        
    def calculate_mst(self):
        # Método para calcular y mostrar el árbol parcial mínimo entre el nodo de inicio y el nodo de destino
        start_node = self.start_var.get()  # Obtiene el nodo de inicio seleccionado
        end_node = self.end_var.get()  # Obtiene el nodo de destino seleccionado
        
        # Verifica si el nodo de inicio no está en el grafo
        if start_node not in self.graph:
            messagebox.showerror("Error", f"El nodo {start_node} no existe en el grafo.")
            return
        
        # Verifica si el nodo de destino no está en el grafo
        if end_node not in self.graph:
            messagebox.showerror("Error", f"El nodo {end_node} no existe en el grafo.")
            return
        
        # Ejecuta el algoritmo de Prim para encontrar el árbol parcial mínimo
        mst_weight, mst_edges = self.prim_mst(self.graph, start_node)
        
        # Borra el contenido anterior del cuadro de texto de salida
        self.output_text.delete(1.0, tk.END)
        
        # Muestra el resultado en el cuadro de texto de salida
        self.output_text.insert(tk.END, f"Peso total del Árbol Parcial Mínimo: {mst_weight}\n")
        self.output_text.insert(tk.END, "Aristas del Árbol Parcial Mínimo:\n")
        for edge in mst_edges:
            self.output_text.insert(tk.END, f"{edge[0]} - {edge[1]} : {self.graph[edge[0]][edge[1]]}\n")
    
    def prim_mst(self, graph, start):
        # Implementación del algoritmo de Prim para encontrar el árbol parcial mínimo
        mst_weight = 0  # Inicializa el peso total del árbol parcial mínimo
        mst_edges = []  # Inicializa la lista de aristas del árbol parcial mínimo
        visited = set()  # Conjunto para almacenar nodos visitados
        priority_queue = [(0, start, None)]  # Cola de prioridad (peso, nodo actual, nodo anterior)
        
        while priority_queue:
            weight, u, prev = heapq.heappop(priority_queue)  # Extrae el nodo con menor peso
            
            if u in visited:  # Si el nodo actual ya ha sido visitado, continua con el siguiente
                continue
            
            visited.add(u)  # Marca el nodo actual como visitado
            mst_weight += weight  # Añade el peso de la arista al peso total del árbol parcial mínimo
            
            if prev:  # Si hay un nodo anterior, añade la arista al árbol parcial mínimo
                mst_edges.append((prev, u))
            
            for v, weight in graph[u].items():  # Itera sobre los vecinos del nodo actual
                if v not in visited:  # Si el vecino no ha sido visitado
                    heapq.heappush(priority_queue, (weight, v, u))  # Agrega el vecino a la cola de prioridad
        
        return mst_weight, mst_edges  # Retorna el peso total y las aristas del árbol parcial mínimo

def main():
    root = tk.Tk()  # Crea la ventana principal
    dijkstra_gui = DijkstraGUI(root)  # Crea una instancia de la interfaz gráfica
    root.mainloop()  # Inicia el bucle principal de eventos

if __name__ == "__main__":
    main()  # Ejecuta la función main si este script es el programa principal
