import file_helper as fh
import matplotlib.pyplot as plt
import numpy as np

def categorize_file_sizes(sizes):
    """
    Категоризація розмірів файлів за стандартними Linux тегами:
    - Empty (0 bytes)
    - Tiny (< 1 KB)
    - Small (1 KB - 1 MB)
    - Medium (1 MB - 100 MB)
    - Large (100 MB - 1 GB)
    - Huge (1 GB - 10 GB)
    - Massive (> 10 GB)
    """
    categories = {
        'Empty (0 B)': 0,
        'Tiny (< 1 KB)': 0,
        'Small (1 KB - 1 MB)': 0,
        'Medium (1 MB - 100 MB)': 0,
        'Large (100 MB - 1 GB)': 0,
        'Huge (1 GB - 10 GB)': 0,
        'Massive (> 10 GB)': 0
    }
    
    for size in sizes:
        if size == 0:
            categories['Empty (0 B)'] += 1
        elif size < 1024:  # < 1 KB
            categories['Tiny (< 1 KB)'] += 1
        elif size < 1024 * 1024:  # < 1 MB
            categories['Small (1 KB - 1 MB)'] += 1
        elif size < 100 * 1024 * 1024:  # < 100 MB
            categories['Medium (1 MB - 100 MB)'] += 1
        elif size < 1024 * 1024 * 1024:  # < 1 GB
            categories['Large (100 MB - 1 GB)'] += 1
        elif size < 10 * 1024 * 1024 * 1024:  # < 10 GB
            categories['Huge (1 GB - 10 GB)'] += 1
        else:
            categories['Massive (> 10 GB)'] += 1
    
    return categories

# Отримання розмірів файлів
size_list = fh.get_sizes(fh.STATS_FILENAME)

# Категоризація
file_categories = categorize_file_sizes(size_list)

# Підготовка даних для графіку
categories = list(file_categories.keys())
counts = list(file_categories.values())

# Кольорова схема
colors = [
    '#E0E0E0',  # Empty - сірий
    '#87CEEB',  # Tiny - світло-блакитний
    '#4682B4',  # Small - синій
    '#1E90FF',  # Medium - яскраво-синій
    '#4169E1',  # Large - Royal Blue
    '#000080',  # Huge - темно-синій
    '#00008B'   # Massive - темно-темно-синій
]

# Створення графіку
plt.figure(figsize=(12, 6))

# Горизонтальна діаграма для кращої читабельності
plt.barh(categories, counts, color=colors)
plt.xlabel('Кількість файлів')
plt.title('Розподіл файлів за розміром')

# Додавання значень поруч зі стовпчиками
for i, v in enumerate(counts):
    plt.text(v, i, f' {v} ({v/sum(counts)*100:.2f}%)', va='center')

plt.tight_layout()
plt.savefig('file_size_categories.png', dpi=200)

# Виведення детальної інформації
print("Розподіл файлів за категоріями розміру:")
total_files = sum(counts)
for category, count in file_categories.items():
    percentage = count / total_files * 100
    print(f"{category}: {count} файлів ({percentage:.2f}%)")

plt.show()