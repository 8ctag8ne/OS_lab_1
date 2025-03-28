import file_helper as fh
from matplotlib import pyplot as plt
from two_pointers_for_quantity import get_interval_with_min_borders as get_min
import numpy as np

# Отримання розмірів файлів
size_list = fh.get_sizes(fh.STATS_FILENAME)
size_list.sort()

# Знаходження інтервалу
interval_start, interval_end = get_min(size_list)

# Побудова гістограми
plt.figure(figsize=(15, 8))
plt.xscale('log')
plt.yscale('log')

# Використання логарифмічних бінів для рівномірнішого відображення
bins = np.logspace(np.log10(max(min(size_list), 1)), np.log10(max(size_list)), num=100)

# Створення масивів для розділення кольорів
sizes_before = size_list[:interval_start]
sizes_interval = size_list[interval_start:interval_end+1]
sizes_after = size_list[interval_end+1:]

# Побудова гістограм різними кольорами
plt.hist(sizes_before, bins=bins, edgecolor='black', color='lightblue', alpha=0.7, label='До основного інтервалу')
plt.hist(sizes_interval, bins=bins, edgecolor='black', color='red', alpha=0.7, label='Основний інтервал')
plt.hist(sizes_after, bins=bins, edgecolor='black', color='lightgreen', alpha=0.7, label='Після основного інтервалу')

plt.xlabel("Розмір файлів (байти)")
plt.ylabel("Кількість файлів")
plt.title("Розподіл кількості файлів залежно від розміру")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()

# Додаткова інформація про інтервал
print(f"Основний інтервал: від {size_list[interval_start]} до {size_list[interval_end]} байт")
print(f"Кількість файлів в інтервалі: {interval_end - interval_start + 1}")
print(f"Відсоток файлів в інтервалі: {(interval_end - interval_start + 1) / len(size_list) * 100:.2f}%")

plt.savefig('logarithmic_histogram_with_interval.png', dpi=200)
plt.show()