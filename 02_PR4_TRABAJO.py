#Victor Eduardo Aleman Padilla

# Importa los módulos necesarios
import heapq  # Módulo para implementar colas con prioridad
import tkinter as tk  # Módulo para crear interfaces gráficas
from tkinter import messagebox, scrolledtext  # Clases para mostrar mensajes y crear un widget de texto desplazable

# Función para ejecutar el algoritmo de Prim
def prim(almacen, inicio, paso_a_paso, puntos_seleccionados):
    # Obtener el número de filas y columnas de la matriz almacen
    filas = len(almacen)
    columnas = len(almacen[0])
    
    # Inicializar una matriz para rastrear los nodos en el árbol de expansión mínima
    en_arbol = [[False] * columnas for _ in range(filas)]
    # Marcar el nodo inicial como parte del árbol de expansión mínima
    en_arbol[inicio[0]][inicio[1]] = True
    
    # Inicializar una cola de prioridad para almacenar las aristas candidatas
    pq = []
    # Matriz para rastrear los nodos previos en el árbol
    anteriores = [[None] * columnas for _ in range(filas)]
    
    # Direcciones posibles: derecha, abajo, izquierda, arriba, diagonales
    direcciones = [
        (0, 1), (1, 0), (0, -1), (-1, 0),  # Derecha, Abajo, Izquierda, Arriba
        (1, 1), (-1, 1), (1, -1), (-1, -1)  # Diagonales
    ]
    
    # Añadir los nodos adyacentes al nodo inicial a la cola de prioridad
    for dx, dy in direcciones:
        nx, ny = inicio[0] + dx, inicio[1] + dy
        if 0 <= nx < filas and 0 <= ny < columnas:
            heapq.heappush(pq, (almacen[nx][ny], (nx, ny)))
            anteriores[nx][ny] = inicio
    
    # Variable para almacenar la mejor rama
    mejor_rama = []
    # Peso inicial de la mejor rama
    mejor_peso = float('inf')
    
    # Bucle principal del algoritmo de Prim
    while pq:
        peso, (x, y) = heapq.heappop(pq)
        
        # Si el nodo ya está en el árbol, continuar
        if en_arbol[x][y]:
            continue
        
        # Marcar el nodo como parte del árbol de expansión mínima
        en_arbol[x][y] = True
        
        # Mostrar el paso actual en el widget de texto
        paso_a_paso.insert(tk.END, f"Agrega la arista ({anteriores[x][y]}, ({x}, {y})) con peso {peso}\n")
        paso_a_paso.see(tk.END)
        
        # Considerar los nodos adyacentes al nodo actual
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas and not en_arbol[nx][ny]:
                heapq.heappush(pq, (almacen[nx][ny], (nx, ny)))
                anteriores[nx][ny] = (x, y)
                
                # Actualizar la mejor rama si se encuentra una arista más liviana
                if almacen[nx][ny] < mejor_peso:
                    mejor_rama = [(x, y), (nx, ny)]
                    mejor_peso = almacen[nx][ny]
                    
                    # Detener el algoritmo si se alcanza alguno de los puntos seleccionados
                    if (nx, ny) in puntos_seleccionados:
                        return mejor_rama
    
    # Construir la lista de nodos en el árbol de expansión mínima
    arbol_expansion = []
    for i in range(filas):
        for j in range(columnas):
            if en_arbol[i][j]:
                arbol_expansion.append((i, j))
    
    # Devolver el árbol de expansión mínima y la mejor rama encontrada
    return arbol_expansion, mejor_rama  

# Clase para el simulador de Prim con interfaz gráfica
class PrimSimulator(tk.Tk):
    def __init__(self, almacen):
        super().__init__()  # Inicializar la clase base de tkinter
        self.title("Simulador de Prim")  # Título de la ventana
        self.almacen = almacen  # Matriz de adyacencia del grafo
        self.matriz_labels = []  # Lista para almacenar las etiquetas de la matriz
        self.paso_a_paso = None  # Widget de texto para mostrar los pasos
        self.punto_inicio = None  # Punto de inicio del algoritmo
        self.puntos_seleccionados = []  # Lista de puntos seleccionados
        self.mejor_rama = None  # Mejor rama encontrada
        
        # Inicializar la interfaz gráfica
        self.inicializar_gui()
    
    def inicializar_gui(self):
        # Widget de texto desplazable para mostrar los pasos del algoritmo
        self.paso_a_paso = scrolledtext.ScrolledText(self, width=40, height=20, wrap=tk.WORD)
        self.paso_a_paso.grid(row=1, column=7, rowspan=7, padx=10, pady=10)
        
        # Crear etiquetas para mostrar los índices de las columnas
        for j in range(len(self.almacen[0])):
            label = tk.Label(self, text=f"Col {j}", borderwidth=1, relief="solid", width=5, height=2)
            label.grid(row=0, column=j+1)
        
        # Crear etiquetas para mostrar los índices de las filas y los valores de la matriz
        for i in range(len(self.almacen)):
            fila_labels = []
            label = tk.Label(self, text=f"Fila {i}", borderwidth=1, relief="solid", width=5, height=2)
            label.grid(row=i+1, column=0)
            for j in range(len(self.almacen[0])):
                label = tk.Label(self, text=str(self.almacen[i][j]), borderwidth=1, relief="solid", width=5, height=2)
                label.grid(row=i+1, column=j+1)
                # Establecer un evento de clic para seleccionar el punto de inicio
                label.bind("<Button-1>", lambda e, x=i, y=j: self.establecer_punto_inicio(x, y))
                fila_labels.append(label)
            self.matriz_labels.append(fila_labels)
        
        # Botón para iniciar la búsqueda del árbol de expansión mínima
        self.boton_buscar_arbol = tk.Button(self, text="Buscar Árbol", command=self.buscar_arbol)
        self.boton_buscar_arbol.grid(row=7, column=0, columnspan=5)
        
        # Botón para reiniciar las selecciones
        self.boton_reiniciar = tk.Button(self, text="Reiniciar Selecciones", command=self.reiniciar_selecciones)
        self.boton_reiniciar.grid(row=8, column=0, columnspan=5)
    
    # Método para establecer el punto de inicio del algoritmo de Prim
    def establecer_punto_inicio(self, x, y):
        self.punto_inicio = (x, y)
        messagebox.showinfo("Punto de Inicio Establecido", f"El punto de inicio se ha establecido en ({x}, {y})")
        self.puntos_seleccionados.append((x, y))
        self.matriz_labels[x][y].config(bg="yellow")  # Cambiar el color de fondo de la etiqueta
    
    # Método para iniciar la búsqueda del árbol de expansión mínima
    def buscar_arbol(self):
        if self.punto_inicio is None:
            messagebox.showwarning("Advertencia", "Debe establecer un punto de inicio primero")
            return
        
        # Limpiar el widget de texto antes de iniciar la búsqueda
        self.paso_a_paso.delete('1.0', tk.END)
        
        # Llamar a la función prim para obtener el árbol de expansión mínima y la mejor rama
        arbol_expansion, mejor_rama = prim(self.almacen, self.punto_inicio, self.paso_a_paso, self.puntos_seleccionados)
        
        # Mostrar el árbol de expansión mínima y la mejor rama en la interfaz gráfica
        self.mostrar_arbol(arbol_expansion)
        self.mostrar_mejor_rama(mejor_rama)
    
    # Método para mostrar el árbol de expansión mínima en la interfaz gráfica
    def mostrar_arbol(self, arbol):
        for i in range(len(self.almacen)):
            for j in range(len(self.almacen[0])):
                self.matriz_labels[i][j].config(bg="white")
        
        # Cambiar el color de fondo de las etiquetas que pertenecen al árbol de expansión mínima
        for (x, y) in arbol:
            self.matriz_labels[x][y].config(bg="lightgreen")
        
        # Cambiar el color de fondo del punto de inicio seleccionado
        if self.punto_inicio:
            self.matriz_labels[self.punto_inicio[0]][self.punto_inicio[1]].config(bg="yellow")
        
        # Cambiar el color de fondo de los puntos seleccionados
        for (x, y) in self.puntos_seleccionados:
            self.matriz_labels[x][y].config(bg="yellow")
    
    # Método para mostrar la mejor rama encontrada en la interfaz gráfica
    def mostrar_mejor_rama(self, rama):
        if rama:
            self.mejor_rama = rama
            # Obtener los extremos de la mejor rama
            (x1, y1), (x2, y2) = rama
            # Cambiar el color de fondo de los extremos de la mejor rama a rojo
            self.matriz_labels[x1][y1].config(bg="red")
            self.matriz_labels[x2][y2].config(bg="red")
            
            # Mostrar la rama más directa hacia el punto seleccionado
            for (x, y) in self.puntos_seleccionados:
                if (x, y) == (x1, y1):
                    break
                # Cambiar el color de fondo de los nodos en la ruta hacia el punto seleccionado a naranja
                self.matriz_labels[x][y].config(bg="orange")
                x1, y1 = x, y
    
    # Método para reiniciar las selecciones y limpiar la interfaz gráfica
    def reiniciar_selecciones(self):
        self.punto_inicio = None
        self.puntos_seleccionados = []
        self.paso_a_paso.delete('1.0', tk.END)
        self.mejor_rama = None
        
        # Restaurar el color de fondo de todas las etiquetas
        for i in range(len(self.almacen)):
            for j in range(len(self.almacen[0])):
                self.matriz_labels[i][j].config(bg="white")
    
if __name__ == "__main__":
    # Matriz de adyacencia para el ejemplo
    almacen = [
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [4, 5, 6, 7, 8],
        [5, 6, 7, 8, 9],
        [6, 7, 8, 9, 10]
    ]
    
    # Crear una instancia del simulador Prim con la matriz de adyacencia
    app = PrimSimulator(almacen)
    # Iniciar la aplicación tkinter
    app.mainloop()

