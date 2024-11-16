import tkinter as tk
from tkinter import ttk
import random

# Определение целевой функции
def target_function(x, y):
    return x**2 + 3*y**2 + 2*x*y

class Particle:
    def __init__(self, x, y):
        self.position = [x, y]
        self.initial_position = self.position[:]  # Сохранение начальной позиции
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.initial_velocity = self.velocity[:]  # Сохранение начальной скорости
        self.best_position = self.position[:]
        self.best_value = target_function(x, y)

    def reset(self):
        # Восстанавливаем начальные значения позиции и скорости
        self.position = self.initial_position[:]
        self.velocity = self.initial_velocity[:]
        self.best_position = self.position[:]
        self.best_value = target_function(*self.position)

    def update_best(self):
        current_value = target_function(self.position[0], self.position[1])
        if current_value < self.best_value:
            self.best_value = current_value
            self.best_position = self.position[:]

class PSO:
    def __init__(self, num_particles, w, c1, c2, iterations, adaptive_speed=False):
        self.particles = [Particle(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(num_particles)]
        self.global_best_position = min(self.particles, key=lambda p: p.best_value).best_position[:]
        self.global_best_value = target_function(self.global_best_position[0], self.global_best_position[1])
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.iterations = iterations
        self.adaptive_speed = adaptive_speed
        self.iteration_count = 0

    def reset_particles(self):
        # Восстанавливаем начальные положения и скорости для всех частиц
        for particle in self.particles:
            particle.reset()
        # Обновляем глобальное лучшее значение
        self.global_best_position = min(self.particles, key=lambda p: p.best_value).best_position[:]
        self.global_best_value = target_function(*self.global_best_position)

    def update_particles(self):
        for particle in self.particles:
            for i in range(2):
                cognitive_component = self.c1 * random.random() * (particle.best_position[i] - particle.position[i])
                social_component = self.c2 * random.random() * (self.global_best_position[i] - particle.position[i])
                particle.velocity[i] = self.w * particle.velocity[i] + cognitive_component + social_component
                particle.position[i] += particle.velocity[i]

            particle.update_best()
            if particle.best_value < self.global_best_value:
                self.global_best_value = particle.best_value
                self.global_best_position = particle.best_position[:]

        if self.adaptive_speed:
            self.w = max(0.1, self.w * 0.95)

    def run(self):
        for _ in range(self.iterations):
            self.update_particles()
        return self.global_best_position, self.global_best_value

class PSOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PSO Optimization with Adaptive Speed")
        
        self.num_particles = 300
        self.w = 0.3
        self.c1 = 2
        self.c2 = 5
        self.adaptive_speed = tk.BooleanVar()
        self.iterations = tk.IntVar(value=1)

        self.create_interface()

    def create_interface(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=10)
        
        ttk.Label(self.root, text="Параметры:").grid(row=0, column=1, sticky="w")
        
        ttk.Label(self.root, text="Коэфф. скорости (w):").grid(row=1, column=1, sticky="w")
        self.w_entry = ttk.Entry(self.root)
        self.w_entry.insert(0, "0.3")
        self.w_entry.grid(row=1, column=2)
        
        ttk.Label(self.root, text="Коэфф. личного лучшего (c1):").grid(row=2, column=1, sticky="w")
        self.c1_entry = ttk.Entry(self.root)
        self.c1_entry.insert(0, "2")
        self.c1_entry.grid(row=2, column=2)
        
        ttk.Label(self.root, text="Коэфф. глобального лучшего (c2):").grid(row=3, column=1, sticky="w")
        self.c2_entry = ttk.Entry(self.root)
        self.c2_entry.insert(0, "5")
        self.c2_entry.grid(row=3, column=2)
        
        ttk.Label(self.root, text="Количество итераций:").grid(row=4, column=1, sticky="w")
        self.iterations_entry = ttk.Entry(self.root)
        self.iterations_entry.insert(0, "1")
        self.iterations_entry.grid(row=4, column=2)
        
        self.adaptive_speed_check = tk.Checkbutton(self.root, text="Адаптивное снижение скорости (AS)", variable=self.adaptive_speed)
        self.adaptive_speed_check.grid(row=5, column=1, columnspan=2, sticky="w")
        
        self.generate_button = ttk.Button(self.root, text="Генерация частиц", command=self.generate_particles)
        self.generate_button.grid(row=6, column=1, columnspan=2)
        
        self.calculate_button = ttk.Button(self.root, text="Расчет решения", command=self.calculate_solution)
        self.calculate_button.grid(row=7, column=1, columnspan=2)
        
        self.result_label = ttk.Label(self.root, text="Лучшее значение:")
        self.result_label.grid(row=8, column=1, columnspan=2)
        
    def generate_particles(self):
        self.w = float(self.w_entry.get())
        self.c1 = float(self.c1_entry.get())
        self.c2 = float(self.c2_entry.get())
        self.iterations = int(self.iterations_entry.get())
        self.pso = PSO(num_particles=self.num_particles, w=self.w, c1=self.c1, c2=self.c2, iterations=self.iterations, adaptive_speed=self.adaptive_speed.get())
        self.plot_particles()

    def calculate_solution(self):
        # Сбрасываем положения частиц перед новым расчётом
        self.pso.reset_particles()
        self.iterations = int(self.iterations_entry.get())
        self.pso.iterations = self.iterations
        best_position, best_value = self.pso.run()
        
        if best_position:
            self.result_label.config(text=f"Лучшее значение: x={best_position[0]:.2f}, y={best_position[1]:.2f}, f(x,y)={best_value:.2f}")
            self.plot_particles()

    def plot_particles(self):
        self.canvas.delete("all")
        self.canvas.create_line(50, 200, 350, 200, fill="black")
        self.canvas.create_line(200, 50, 200, 350, fill="black")
        for particle in self.pso.particles:
            x, y = particle.position
            x_canvas = 200 + x * 3  
            y_canvas = 200 - y * 3
            self.canvas.create_oval(x_canvas-2, y_canvas-2, x_canvas+2, y_canvas+2, fill="blue")

root = tk.Tk()
app = PSOApp(root)
root.mainloop()
