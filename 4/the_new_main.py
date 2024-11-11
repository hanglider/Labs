import tkinter as tk
from tkinter import ttk
import random

# Определение целевой функции
def objective_function(x, y):
    return x**2 + 3 * y**2 + 2 * x * y

# Функция для одноточечного кроссинговера
def crossover(parent1, parent2):
    if random.random() < 0.5:
        return (parent1[0], parent2[1]) 
    else:
        return (parent2[0], parent1[1])

# Функция для мутации
def mutate(individual, mutation_rate):
    x, y = individual
    x += mutation_rate * random.uniform(-1, 1)
    y += mutation_rate * random.uniform(-1, 1)
    return x, y

# Генетический алгоритм
def run_generation(steps, only_mutation, mutation_rate):
    global population, generation_count, best_value
    
    for _ in range(steps):
        # Вычисление значений функции для популяции
        fitness_scores = [objective_function(x, y) for x, y in population]
        
        # Обновляем лучшее значение только если текущее лучше предыдущего
        current_best_value = min(fitness_scores)
        if current_best_value < best_value:
            best_value = current_best_value
            best_value_label.config(text=f"Лучшее значение: {round(best_value, 4)}")

        # Сортировка популяции по значению функции (от наименьшего к наибольшему)
        population = [population[i] for i in sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k])]
        
        # Обновляем таблицу и график
        update_table(population)
        draw_population(population_canvas, population)
        
        # Отбор: выбираем 50% лучших
        selected = population[:len(population) // 2]
        
        # Кроссинговер: создаем новое поколение
        children = []
        while len(children) < len(population):
            parent1, parent2 = random.sample(selected, 2)
            child = crossover(parent1, parent2)
            children.append(child)
        
        # Если режим "только мутация", выполняем мутацию без кроссинговера
        if only_mutation:
            population = [mutate(ind, mutation_rate) for ind in population]
        else:
            # В режиме "мутация + кроссинговер" выполняем мутацию для потомков
            population = [mutate(ind, mutation_rate) for ind in children]
        
        # Обновление поколения
        generation_count += 1
        generation_label.config(text=f"Поколение: {generation_count}")

# Функция обновления таблицы
def update_table(population):
    # Очищаем таблицу
    for item in table.get_children():
        table.delete(item)
    
    # Заполняем таблицу данными текущего поколения
    for i, (x, y) in enumerate(population):
        table.insert("", "end", values=(i+1, round(x, 4), round(y, 4), round(objective_function(x, y), 4)))

# Функция для рисования популяции на Canvas
def draw_population(canvas, population):
    canvas.delete("all")
    canvas.create_line(200, 0, 200, 400, fill="gray")  # ось Y
    canvas.create_line(0, 200, 400, 200, fill="gray")  # ось X
    
    scale = 19

    for x, y in population:
        canvas_x = 200 + x * scale  # Масштабирование для визуализации
        canvas_y = 200 - y * scale  # Инвертируем для правильного отображения осей
        canvas.create_oval(canvas_x-3, canvas_y-3, canvas_x+3, canvas_y+3, fill="blue")

# Запуск алгоритма на определенное количество поколений
def run_step():
    try:
        steps = int(generations_entry.get())
        mutation_rate = float(mutation_rate_entry.get())  # Получаем значение mutation_rate из поля ввода
        only_mutation = mode_var.get() == "Только мутация"
        run_generation(steps, only_mutation, mutation_rate)
    except ValueError:
        pass  # Игнорируем ошибку, если введено не число

# Инициализация начальных параметров
population_size = 300
mutation_rate = 0.01
population = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(population_size)]
generation_count = 1
best_value = float('inf')

# Создание интерфейса
root = tk.Tk()
root.title("Генетический алгоритм с таблицей и графиком")

# Параметры
frame_params = tk.Frame(root)
frame_params.grid(row=0, column=0, padx=10, pady=5, sticky="w")

generation_label = tk.Label(frame_params, text=f"Поколение: {generation_count}")
generation_label.grid(row=0, column=0, padx=5, pady=5)

run_button = tk.Button(frame_params, text="Запустить", command=run_step)
run_button.grid(row=0, column=4, padx=5, pady=5)

# Поле для ввода количества поколений за запуск
tk.Label(frame_params, text="Поколений за запуск:").grid(row=0, column=1, padx=5, pady=5)
generations_entry = tk.Entry(frame_params, width=5)
generations_entry.insert(0, "1")
generations_entry.grid(row=0, column=2, padx=5, pady=5)

# Поле для ввода значения mutation_rate
tk.Label(frame_params, text="Коэффициент мутации:").grid(row=1, column=1, padx=5, pady=5)
mutation_rate_entry = tk.Entry(frame_params, width=5)
mutation_rate_entry.insert(0, str(mutation_rate))
mutation_rate_entry.grid(row=1, column=2, padx=5, pady=5)

# Метка для отображения лучшего значения
best_value_label = tk.Label(root, text=f"Лучшее значение: {best_value}")
best_value_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

# Переключатель для выбора режима
mode_var = tk.StringVar(value="Мутация + кроссинговер")
tk.Radiobutton(frame_params, text="Мутация + кроссинговер", variable=mode_var, value="Мутация + кроссинговер").grid(row=0, column=5, padx=5, pady=5)
tk.Radiobutton(frame_params, text="Только мутация", variable=mode_var, value="Только мутация").grid(row=0, column=6, padx=5, pady=5)

# Таблица для отображения хромосом
table_frame = tk.Frame(root)
table_frame.grid(row=1, column=0, padx=10, pady=10)

table = ttk.Treeview(table_frame, columns=("Хромосома", "x", "y", "Значение функции"), show="headings")
table.heading("Хромосома", text="Хромосома")
table.heading("x", text="x")
table.heading("y", text="y")
table.heading("Значение функции", text="Значение функции")
table.grid(row=0, column=0, sticky="nsew")

# Полотно для отображения графика
population_canvas = tk.Canvas(root, width=400, height=400, bg="white")
population_canvas.grid(row=1, column=1, padx=10, pady=10)

# Первоначальное заполнение таблицы и графика
update_table(population)
draw_population(population_canvas, population)

root.mainloop()
