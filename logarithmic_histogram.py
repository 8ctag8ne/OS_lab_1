import file_helper as fh
from matplotlib import pyplot as plt
import numpy as np

# Отримання розмірів файлів
size_list = fh.get_sizes("file_size_sys.csv")
size_list.sort()

# Загальний розмір файлів
total_size = sum(size_list)
# print(total_size, size_list[0], size_list[-1])

# Визначення вагового коефіцієнта як відсотка від загального обсягу
weights = np.array(size_list) / total_size  

# Побудова гістограми
plt.figure(figsize=(15, 8))
plt.xscale('log')
plt.yscale('log')  # Важливо, щоб частки від загального обсягу теж відображались логарифмічно

# Використання логарифмічних бінів для рівномірнішого відображення
bins = np.logspace(np.log10(max(min(size_list), 1)), np.log10(max(size_list)), num=100)

plt.hist(size_list, bins=bins, weights=weights, edgecolor='black')

plt.xlabel("Розмір файлів (байти)")
plt.ylabel("Частка від загального обсягу файлів")
plt.title("Розподіл розміру файлів у відсотковому співвідношенні")

plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.savefig('logarithmic_histogram.png', dpi=200)
plt.show()