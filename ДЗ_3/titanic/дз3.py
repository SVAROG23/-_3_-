import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# 1. ЗАГРУЗКА ДАННЫХ
def load_data(file_name):
    """
    Функция для чтения CSV-файла.
    Возвращает DataFrame (таблицу с данными) или None, если произошла ошибка.
    """
    print("--- ПУНКТ 1. ЗАГРУЗКА ДАННЫХ ---")
    try:
        # Получаем абсолютный путь к папке, в которой лежит наш скрипт.
        # Это нужно, чтобы программа не путалась, откуда она запущена.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Соединяем путь к папке и имя файла, получая полный путь
        file_path = os.path.join(script_dir, file_name)
        
        # Проверяем, существует ли файл по этому пути (обработка ошибки, чтобы программа не упала)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл '{file_name}' не найден в папке: {script_dir}")
        
        # Если файл на месте — читаем его с помощью Pandas
        df = pd.read_csv(file_path)
        print(f"Успех! Данные загружены из файла: {file_name}")
        
        # Выводим размер таблицы (сколько строк и столбцов)
        print("Размер датасета (строки, столбцы):", df.shape)
        
        # Выводим первые 3 строки, чтобы визуально проверить, что данные корректные
        print("\nПервые 3 строки данных:")
        print(df.head(3))
        return df
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
        return None

# 2. ФИЛЬТРАЦИЯ
def filter_data(df):
    """
    Функция для фильтрации данных.
    Оставляем только пассажиров, которые выжили (в колонке Survived стоит 1).
    """
    print("\n--- ПУНКТ 2. ФИЛЬТРАЦИЯ ---")
    print("Фильтруем пассажиров: оставляем только тех, кто выжил (Survived == 1).")
    
    # Создаем логическую маску: True, если пассажир выжил, и False, если нет.
    # Затем применяем эту маску к таблице, чтобы оставить только строки с True.
    filtered_df = df[df['Survived'] == 1]
    
    # Показываем, сколько строк было и сколько осталось
    print(f"Строк ДО фильтрации: {len(df)}")
    print(f"Строк ПОСЛЕ фильтрации (выжившие): {len(filtered_df)}")
    return filtered_df

# 3. РАСЧЕТ СРЕДНЕГО ЗНАЧЕНИЯ
def calculate_mean(df):
    """
    Функция для расчета среднего значения.
    Считаем средний возраст пассажиров по колонке Age.
    """
    print("\n--- ПУНКТ 3. РАСЧЕТ СРЕДНЕГО ЗНАЧЕНИЯ ---")
    
    # Берем колонку Age и применяем метод .mean()
    # Метод автоматически игнорирует пустые значения (NaN), если они есть
    mean_age = df['Age'].mean()
    print(f"Средний возраст пассажира в датасете: {mean_age:.0f} лет")
    
    # Возвращаем имя колонки, чтобы передать его в функцию построения графика
    return 'Age'

# 4. ВИЗУАЛИЗАЦИЯ (ГРАФИК)
def plot_graph(df, col_name):
    """
    Функция для построения графика (гистограммы) распределения возраста.
    """
    print("\n--- ПУНКТ 4. ВИЗУАЛИЗАЦИЯ ---")
    print(f"Строим гистограмму распределения для колонки: {col_name}")
    
    # Задаем размер окна для графика (ширина 8, высота 5)
    plt.figure(figsize=(8, 5))
    
    # Строим гистограмму:
    # df[col_name].dropna() — берем колонку и убираем пустые значения, чтобы не было ошибки
    # bins=20 — разбиваем данные на 20 столбиков
    plt.hist(df[col_name].dropna(), bins=20, color='skyblue', edgecolor='black')
    
    # Подписываем график, чтобы было понятно, что на нем изображено
    plt.title('Распределение возраста пассажиров (Титаник)')
    plt.xlabel('Возраст (лет)')
    plt.ylabel('Количество человек')
    
    # Добавляем сетку по оси Y (для красоты и удобства чтения)
    plt.grid(axis='y', alpha=0.75)
    
    # Отображаем окно с графиком
    plt.show()

# 5. ОПЦИОНАЛЬНО: ИНТЕРАКТИВНЫЙ ДАШБОРД
def run_dashboard():
    """
    Функция для запуска интерактивного веб-дашборда (Streamlit).
    Позволяет загрузить файл через браузер и посмотреть графики.
    """
    try:
        import streamlit as st
        
        # Заголовок страницы
        st.title("📊 Дашборд: Анализ пассажиров Титаника")
        st.write("Загрузите файл `train.csv`, чтобы увидеть данные и интерактивный график.")
        
        # Кнопка для загрузки файла
        uploaded_file = st.file_uploader("Выберите CSV файл", type=["csv"])
        
        if uploaded_file is not None:
            # Если файл загружен, читаем его
            df = pd.read_csv(uploaded_file)
            
            st.subheader("Предпросмотр данных")
            st.dataframe(df.head())
            
            # Ищем все числовые колонки, чтобы предложить пользователю выбор
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            
            # Выпадающий список для выбора колонки
            selected_col = st.selectbox("Выберите колонку для графика:", numeric_cols)
            
            st.subheader(f"График: {selected_col}")
            # Встроенная функция Streamlit для построения столбчатой диаграммы
            st.bar_chart(df[selected_col].value_counts().head(10))
            
            # Выводим среднее значение для выбранной колонки
            st.write(f"Среднее значение для выбранной колонки: **{df[selected_col].mean():.2f}**")
    except ImportError:
        print("Ошибка: библиотека Streamlit не установлена.")

# ГЛАВНЫЙ БЛОК ЗАПУСКА

if __name__ == "__main__":
    # Проверяем: если скрипт запущен через Streamlit, вызываем функцию дашборда
    if "streamlit" in sys.modules:
        run_dashboard()
    else:
        # Обычный запуск через Python в VS Code
        FILE_NAME = 'train.csv' 
        
        # Вызываем функции по очереди
        df = load_data(FILE_NAME)
        if df is not None:
            filtered = filter_data(df)
            column_for_plot = calculate_mean(df)
            plot_graph(df, column_for_plot)
            
            # Выводим подсказку, как запустить дашборд
            print("\n" + "="*50)
            print("ОПЦИОНАЛЬНОЕ ЗАДАНИЕ:")
            print("Чтобы открыть интерактивный дашборд, введите в терминале:")
            print(f"streamlit run {os.path.basename(__file__)}")
            print("="*50)