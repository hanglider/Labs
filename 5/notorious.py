import tkinter as tk
from tkinter import ttk
import random

# Определение целевой функции
def target_function(x, y):
    return x**2 + 3*y**2 + 2*x*y

class Particle:
    def __init__(self, x, y, max_velocity):
        self.position = [x, y]
        self.initial_position = self.position[:]
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.max_velocity = max_velocity
        self.initial_velocity = self.velocity[:]
        self.best_position = self.position[:]
        self.best_value = target_function(x, y)

    def reset(self):
        self.position = self.initial_position[:]
        self.velocity = self.initial_velocity[:]
        self.best_position = self.position[:]
        self.best_value = target_function(*self.position)

    def update_best(self):
        current_value = target_function(self.position[0], self.position[1])
        if current_value < self.best_value:
            self.best_value = current_value
            self.best_position = self.position[:]

    def update_velocity(self, global_best_position, w, c1, c2, modify=False):
        for i in range(2):
            cognitive_component = c1 * random.random() * (self.best_position[i] - self.position[i])
            social_component = c2 * random.random() * (global_best_position[i] - self.position[i])
            if modify:  # Модифицированный кроссинговер
                cross_component = random.uniform(-1, 1) * (global_best_position[i] + self.best_position[i]) / 2
                new_velocity = w * self.velocity[i] + cognitive_component + social_component + cross_component
            else:  # Обычный PSO
                new_velocity = w * self.velocity[i] + cognitive_component + social_component
            self.velocity[i] = max(-self.max_velocity, min(new_velocity, self.max_velocity))

    def move(self):
        for i in range(2):
            self.position[i] += self.velocity[i]

class PSO:
    def __init__(self, num_particles, w, c1, c2, iterations, max_velocity, adaptive_speed=False, modify=False):
        self.particles = [Particle(random.uniform(-20, 20), random.uniform(-20, 20), max_velocity) for _ in range(num_particles)]
        self.global_best_position = min(self.particles, key=lambda p: p.best_value).best_position[:]
        self.global_best_value = target_function(self.global_best_position[0], self.global_best_position[1])
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.iterations = iterations
        self.adaptive_speed = adaptive_speed
        self.modify = modify

    def reset_particles(self):
        for particle in self.particles:
            particle.reset()
        self.global_best_position = min(self.particles, key=lambda p: p.best_value).best_position[:]
        self.global_best_value = target_function(*self.global_best_position)

    def update_particles(self):
        for particle in self.particles:
            particle.update_velocity(self.global_best_position, self.w, self.c1, self.c2, self.modify)
            particle.move()
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
        self.root.title("PSO Optimization with Comparison")

        self.num_particles = 200
        self.w = 0.3
        self.c1 = 2
        self.c2 = 5
        self.adaptive_speed = tk.BooleanVar()
        self.iterations = tk.IntVar(value=10)
        self.max_velocity = 0.3

        self.create_interface()

    def create_interface(self):
        self.canvas_lite = tk.Canvas(self.root, width=300, height=300, bg="white")
        self.canvas_lite.grid(row=0, column=0, rowspan=10)

        self.canvas_pro = tk.Canvas(self.root, width=300, height=300, bg="white")
        self.canvas_pro.grid(row=0, column=1, rowspan=10)

        ttk.Label(self.root, text="Параметры:").grid(row=0, column=2, sticky="w")

        ttk.Label(self.root, text="Коэфф. скорости (w):").grid(row=1, column=2, sticky="w")
        self.w_entry = ttk.Entry(self.root)
        self.w_entry.insert(0, "0.3")
        self.w_entry.grid(row=1, column=3)

        ttk.Label(self.root, text="Коэфф. личного лучшего (c1):").grid(row=2, column=2, sticky="w")
        self.c1_entry = ttk.Entry(self.root)
        self.c1_entry.insert(0, "2")
        self.c1_entry.grid(row=2, column=3)

        ttk.Label(self.root, text="Коэфф. глобального лучшего (c2):").grid(row=3, column=2, sticky="w")
        self.c2_entry = ttk.Entry(self.root)
        self.c2_entry.insert(0, "5")
        self.c2_entry.grid(row=3, column=3)

        ttk.Label(self.root, text="Количество итераций:").grid(row=4, column=2, sticky="w")
        self.iterations_entry = ttk.Entry(self.root)
        self.iterations_entry.insert(0, "10")
        self.iterations_entry.grid(row=4, column=3)

        self.adaptive_speed_check = tk.Checkbutton(self.root, text="Адаптивное снижение скорости (AS)", variable=self.adaptive_speed)
        self.adaptive_speed_check.grid(row=5, column=2, columnspan=2, sticky="w")

        self.generate_button = ttk.Button(self.root, text="Генерация частиц", command=self.generate_particles)
        self.generate_button.grid(row=6, column=2, columnspan=2)

        self.calculate_button = ttk.Button(self.root, text="Расчет решения", command=self.calculate_solution)
        self.calculate_button.grid(row=7, column=2, columnspan=2)

        self.result_label = ttk.Label(self.root, text="Лучшее значение:")
        self.result_label.grid(row=8, column=2, columnspan=2)

    def generate_particles(self):
        self.w = float(self.w_entry.get())
        self.c1 = float(self.c1_entry.get())
        self.c2 = float(self.c2_entry.get())
        self.iterations = int(self.iterations_entry.get())

        # Создание PSO для lite и pro версий
        self.pso_lite = PSO(num_particles=self.num_particles, w=self.w, c1=self.c1, c2=self.c2,
                            iterations=self.iterations, max_velocity=self.max_velocity, adaptive_speed=self.adaptive_speed.get(), modify=False)
        self.pso_pro = PSO(num_particles=self.num_particles, w=self.w, c1=self.c1, c2=self.c2,
                           iterations=self.iterations, max_velocity=self.max_velocity, adaptive_speed=self.adaptive_speed.get(), modify=True)
        self.plot_particles()

    def calculate_solution(self):
        self.pso_lite.reset_particles()
        self.pso_pro.reset_particles()

        lite_best_position, lite_best_value = self.pso_lite.run()
        pro_best_position, pro_best_value = self.pso_pro.run()

        self.result_label.config(
            text=f"Lite: f(x,y)={lite_best_value:.2f} | Pro: f(x,y)={pro_best_value:.2f}"
        )
        self.plot_particles()

    def plot_particles(self):
        for canvas, pso in [(self.canvas_lite, self.pso_lite), (self.canvas_pro, self.pso_pro)]:
            canvas.delete("all")
            canvas.create_line(150, 0, 150, 300, fill="black")
            canvas.create_line(0, 150, 300, 150, fill="black")
            for particle in pso.particles:
                x_canvas = 150 + particle.position[0] * 5
                y_canvas = 150 - particle.position[1] * 5
                canvas.create_oval(x_canvas-2, y_canvas-2, x_canvas+2, y_canvas+2, fill="blue")

            best_x, best_y = pso.global_best_position
            x_canvas = 150 + best_x * 5
            y_canvas = 150 - best_y * 5
            canvas.create_oval(x_canvas-5, y_canvas-5, x_canvas+5, y_canvas+5, fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = PSOApp(root)
    root.mainloop()
