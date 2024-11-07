import tkinter as tk
from tkinter import ttk
import random

class GeneticAlgorithmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генетический Алгоритм")

        # Параметры алгоритма
        self.population_size = 10
        self.mutation_probability = tk.DoubleVar(value=0.1)  # Вероятность мутации
        self.generation_count = tk.IntVar(value=1)  # Количество поколений за запуск
        self.population = self.initialize_population()
        self.best_solution = None

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Поле ввода для вероятности мутации
        tk.Label(self.root, text="Вероятность мутации:").pack()
        tk.Entry(self.root, textvariable=self.mutation_probability).pack()

        # Поле ввода для количества поколений
        tk.Label(self.root, text="Количество поколений за запуск:").pack()
        tk.Entry(self.root, textvariable=self.generation_count).pack()

        # Кнопка запуска
        tk.Button(self.root, text="Запуск", command=self.run_algorithm).pack()

        # Холст для графика
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Таблица для отображения хромосом
        self.table = ttk.Treeview(self.root, columns=("x", "y", "fitness"), show="headings")
        self.table.heading("x", text="x")
        self.table.heading("y", text="y")
        self.table.heading("fitness", text="fitness")
        self.table.pack()

        # Поле для отображения лучшего значения
        self.best_label = tk.Label(self.root, text="Лучшее значение: ")
        self.best_label.pack()

    def initialize_population(self):
        return [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(self.population_size)]

    def fitness(self, x, y):
        return x**2 + 3*y**2 + 2*x*y

    def selection(self):
        # Селекция: выбираем половину лучших хромосом по фитнесу
        sorted_population = sorted(self.population, key=lambda ind: self.fitness(ind[0], ind[1]))
        return sorted_population[:self.population_size // 2]

    def crossover(self, parent1, parent2):
        # Одноточечный кроссинговер
        x = (parent1[0] + parent2[0]) / 2
        y = (parent1[1] + parent2[1]) / 2
        return x, y

    def mutate(self, individual):
        # Мутация с использованием заданной вероятности
        if random.random() < self.mutation_probability.get():
            individual = (individual[0] + random.uniform(-1, 1), individual[1] + random.uniform(-1, 1))
        return individual

    def run_algorithm(self):
        generations = self.generation_count.get()
        for _ in range(generations):
            # Селекция
            selected = self.selection()

            # Кроссинговер и мутация для нового поколения
            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(selected, 2)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            self.population = new_population

            # Найти лучшее решение в поколении
            self.best_solution = min(self.population, key=lambda ind: self.fitness(ind[0], ind[1]))

        # Обновление интерфейса
        self.update_table()
        self.update_canvas()
        self.best_label.config(text=f"Лучшее значение: {self.fitness(self.best_solution[0], self.best_solution[1]):.4f}")

    def update_table(self):
        # Очистить таблицу и заполнить новыми значениями
        for row in self.table.get_children():
            self.table.delete(row)
        for x, y in self.population:
            fitness_value = self.fitness(x, y)
            self.table.insert("", "end", values=(f"{x:.2f}", f"{y:.2f}", f"{fitness_value:.2f}"))

    def update_canvas(self):
        self.canvas.delete("all")
        # Отрисовка осей
        self.canvas.create_line(200, 0, 200, 400, fill="gray")
        self.canvas.create_line(0, 200, 400, 200, fill="gray")

        # Масштаб для отображения
        scale = 10
        for x, y in self.population:
            canvas_x = 200 + x * scale
            canvas_y = 200 - y * scale
            self.canvas.create_oval(canvas_x - 3, canvas_y - 3, canvas_x + 3, canvas_y + 3, fill="blue")

# Запуск приложения
root = tk.Tk()
app = GeneticAlgorithmApp(root)
root.mainloop()
