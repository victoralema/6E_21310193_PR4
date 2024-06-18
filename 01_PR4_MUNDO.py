#Victor Eduardo Aleman PAdilla 21310193
import tkinter as tk  # Importamos la biblioteca tkinter para la interfaz gráfica
from tkinter import messagebox  # Importamos messagebox de tkinter para mostrar mensajes emergentes

class TransportRoutePlanner:
    def __init__(self, master):
        self.master = master  # Guardamos una referencia al objeto raíz de la ventana
        self.master.title("Árbol Parcial Mínimo - Prim")  # Establecemos el título de la ventana
        
        self.canvas = tk.Canvas(self.master, width=600, height=500)  # Creamos un canvas dentro de la ventana
        self.canvas.pack()  # Empaquetamos el canvas dentro de la ventana
        
        # Definimos el grafo que representa las paradas y rutas de autobús
        self.graph = {
            'A': {'B': 10, 'C': 5, 'E': 20},
            'B': {'A': 10, 'D': 15},
            'C': {'A': 5, 'D': 20},
            'D': {'B': 15, 'C': 20, 'F': 10},
            'E': {'A': 20, 'F': 5, 'G': 15},
            'F': {'D': 10, 'E': 5, 'H': 8},
            'G': {'E': 15, 'H': 12, 'I': 7},
            'H': {'F': 8, 'G': 12, 'I': 5},
            'I': {'G': 7, 'H': 5}
        }
        
        # Diccionario para almacenar los colores de las aristas del grafo
        self.edge_colors = {
            ('A', 'B'): 'gray',
            ('A', 'C'): 'gray',
            ('A', 'E'): 'gray',
            ('B', 'A'): 'gray',
            ('B', 'D'): 'gray',
            ('C', 'A'): 'gray',
            ('C', 'D'): 'gray',
            ('D', 'B'): 'gray',
            ('D', 'C'): 'gray',
            ('D', 'F'): 'gray',
            ('E', 'A'): 'gray',
            ('E', 'F'): 'gray',
            ('E', 'G'): 'gray',
            ('F', 'D'): 'gray',
            ('F', 'E'): 'gray',
            ('F', 'H'): 'gray',
            ('G', 'E'): 'gray',
            ('G', 'H'): 'gray',
            ('G', 'I'): 'gray',
            ('H', 'F'): 'gray',
            ('H', 'G'): 'gray',
            ('H', 'I'): 'gray',
            ('I', 'G'): 'gray',
            ('I', 'H'): 'gray',
        }
        
        self.draw_graph()  # Llamamos al método para dibujar el grafo en el canvas
        
        self.start_node = tk.StringVar()  # Variable para almacenar la parada de origen seleccionada
        
        # Creación de etiqueta y menú desplegable para seleccionar origen
        tk.Label(self.master, text="Seleccione la parada de origen:").pack()  # Creamos una etiqueta en la ventana
        tk.OptionMenu(self.master, self.start_node, *list(self.graph.keys())).pack()  # Creamos un menú desplegable con las opciones de origen
        
        # Botón para calcular el Árbol Parcial Mínimo (MST)
        tk.Button(self.master, text="Calcular MST", command=self.calculate_mst).pack()  # Creamos un botón que llama a calculate_mst al hacer clic

    def draw_graph(self):
        self.canvas.delete("all")  # Borramos todo lo dibujado previamente en el canvas
        
        # Posiciones de los nodos en el canvas
        node_positions = {
            'A': (100, 100),
            'B': (200, 100),
            'C': (200, 200),
            'D': (300, 150),
            'E': (100, 200),
            'F': (300, 200),
            'G': (150, 300),
            'H': (250, 300),
            'I': (200, 400)
        }
        
        # Dibujamos los nodos como óvalos y etiquetas de texto en el canvas
        for node, pos in node_positions.items():
            self.canvas.create_oval(pos[0] - 10, pos[1] - 10, pos[0] + 10, pos[1] + 10, fill='white', outline='black')  # Creamos un óvalo para representar el nodo
            self.canvas.create_text(pos[0], pos[1], text=node)  # Creamos un texto con el nombre del nodo
        
        # Dibujamos las aristas del grafo en el canvas
        for node, neighbors in self.graph.items():
            x1, y1 = node_positions[node]  # Posición del nodo actual
            for neighbor, weight in neighbors.items():
                x2, y2 = node_positions[neighbor]  # Posición del vecino
                color = self.edge_colors.get((node, neighbor), 'gray')  # Obtenemos el color de la arista o 'gray' por defecto
                self.canvas.create_line(x1, y1, x2, y2, fill=color)  # Dibujamos la arista con el color correspondiente

    def calculate_mst(self):
        self.reset_edge_colors()  # Reiniciamos los colores de las aristas
        
        start = self.start_node.get()  # Obtenemos la parada de origen seleccionada
        mst_edges, mst_weight = self.prim_mst(start)  # Calculamos el MST desde el nodo de inicio
        
        self.highlight_mst_edges(mst_edges)  # Resaltamos las aristas del MST
        self.show_mst_route(mst_edges)  # Mostramos la ruta del MST en un mensaje

    def prim_mst(self, start):
        visited = {start}  # Conjunto de nodos visitados
        mst_edges = []  # Lista de aristas en el MST
        mst_weight = 0  # Peso total del MST
        
        while len(visited) < len(self.graph):
            min_edge = None
            min_weight = float('inf')
            
            for node in visited:
                for neighbor, weight in self.graph[node].items():
                    if neighbor not in visited and weight < min_weight:
                        min_edge = (node, neighbor)
                        min_weight = weight
            
            if min_edge:
                mst_edges.append(min_edge)
                mst_weight += min_weight
                visited.add(min_edge[1])
                # Actualizamos el color de la arista para indicar que es parte del MST
                self.edge_colors[min_edge] = 'green'
                self.edge_colors[(min_edge[1], min_edge[0])] = 'green'
        
        return mst_edges, mst_weight

    def highlight_mst_edges(self, mst_edges):
        for edge in mst_edges:
            self.edge_colors[edge] = 'green'
            self.edge_colors[(edge[1], edge[0])] = 'green'
        
        self.draw_graph()  # Redibujamos el grafo con los nuevos colores

    def show_mst_route(self, mst_edges):
        route = "Ruta del Árbol Parcial Mínimo:\n"
        for edge in mst_edges:
            route += f"{edge[0]} -> {edge[1]}\n"
        messagebox.showinfo("Ruta del Árbol Parcial Mínimo", route)  # Mostramos la ruta del MST en un mensaje emergente

    def reset_edge_colors(self):
        for edge in self.edge_colors:
            self.edge_colors[edge] = 'gray'  # Reiniciamos todos los colores de las aristas a 'gray'
        self.draw_graph()  # Redibujamos el grafo con los colores reiniciados

def main():
    root = tk.Tk()  # Creamos la ventana principal de tkinter
    app = TransportRoutePlanner(root)  # Creamos una instancia de la aplicación de planificación de rutas
    root.mainloop()  # Iniciamos el bucle principal de la interfaz gráfica

if __name__ == "__main__":
    main()  # Llamamos a la función principal para iniciar la aplicación
