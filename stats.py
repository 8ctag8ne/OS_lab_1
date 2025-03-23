import numpy as np
from collections import Counter
import math
import matplotlib.pyplot as plt
from scipy import stats

def get_file_statistics(input_list):
    """
    Обчислює різні статистичні показники для розмірів файлів.
    
    Args:
        input_list (list): Список розмірів файлів у байтах
        
    Returns:
        dict: Словник зі статистичними показниками
    """
    if not input_list or len(input_list) == 0:
        return {"error": "Список розмірів файлів порожній"}
    
    # Конвертуємо у numpy масив для ефективніших обчислень
    sizes = np.array(input_list)
    total_size = np.sum(sizes)
    
    # Базові статистичні показники
    stats_dict = {
        # Абсолютні розміри
        "total_size": total_size,
        "min_size": np.min(sizes),
        "max_size": np.max(sizes),
        "mean_size": np.mean(sizes),
        "median_size": np.median(sizes),
        
        # Відносні розміри
        "min_relative_size": np.min(sizes) / total_size if total_size > 0 else 0,
        "max_relative_size": np.max(sizes) / total_size if total_size > 0 else 0,
        
        # Загальна кількість
        "file_count": len(sizes)
    }
    
    # Знаходимо моду (найбільш поширений розмір)
    counter = Counter(sizes)
    mode_value, mode_count = counter.most_common(1)[0] if counter else (None, 0)
    stats_dict["mode_size"] = mode_value
    stats_dict["mode_frequency"] = mode_count
    stats_dict["mode_percentage"] = (mode_count / len(sizes)) * 100 if len(sizes) > 0 else 0
    
    # Додаткові статистичні показники
    
    # Стандартне відхилення і дисперсія
    stats_dict["std_dev"] = np.std(sizes)
    stats_dict["variance"] = np.var(sizes)
    
    # Квартилі розподілу
    stats_dict["q1_size"] = np.percentile(sizes, 25)  # Перший квартиль (25%)
    stats_dict["q3_size"] = np.percentile(sizes, 75)  # Третій квартиль (75%)
    
    # Міжквартильний діапазон (IQR)
    stats_dict["iqr"] = stats_dict["q3_size"] - stats_dict["q1_size"]
    
    # Коефіцієнт варіації (CV)
    stats_dict["cv"] = (stats_dict["std_dev"] / stats_dict["mean_size"]) * 100 if stats_dict["mean_size"] > 0 else 0
    
    # Коефіцієнт асиметрії (skewness)
    stats_dict["skewness"] = stats.skew(sizes) if len(sizes) > 2 else 0
    
    # Коефіцієнт ексцесу (kurtosis)
    stats_dict["kurtosis"] = stats.kurtosis(sizes) if len(sizes) > 3 else 0
    
    # Глобальний коефіцієнт нерівномірності файлових розмірів (аналог коефіцієнта Джині)
    # Цей коефіцієнт показує, наскільки нерівномірно розподілений дисковий простір
    # 0 означає рівномірний розподіл, 1 - максимальна нерівномірність
    sorted_sizes = np.sort(sizes)
    cum_sizes = np.cumsum(sorted_sizes)
    cum_proportions = cum_sizes / total_size if total_size > 0 else np.zeros_like(cum_sizes)
    
    # Обчислення площі під кривою Лоренца (використовуємо метод трапецій)
    lorenz_area = np.trapz(cum_proportions, dx=1/len(sizes))
    
    # Коефіцієнт Джині: 2 * (0.5 - площа під кривою Лоренца)
    stats_dict["gini_coefficient"] = 2 * (0.5 - lorenz_area)
    
    # Паретівський аналіз: який відсоток файлів займає 80% загального простору
    pareto_threshold_index = np.searchsorted(cum_proportions, 0.8)
    stats_dict["pareto_threshold"] = pareto_threshold_index / len(sizes) if len(sizes) > 0 else 0
    
    # Додаємо відсоток файлів, розмір яких менший за середній
    stats_dict["percent_below_mean"] = np.mean(sizes < stats_dict["mean_size"]) * 100
    
    # Додаємо відсоток файлів, розмір яких менший за медіану
    stats_dict["percent_below_median"] = 50.0  # За визначенням медіани
    
    # Додаємо геометричне середнє (корисно для даних з великим розкидом)
    # Використовуємо логарифмічне перетворення для стабільності обчислень
    if np.all(sizes > 0):  # Геометричне середнє визначене лише для додатних чисел
        stats_dict["geometric_mean"] = np.exp(np.mean(np.log(sizes)))
    else:
        stats_dict["geometric_mean"] = None
    
    # Відношення мін/макс (степінь варіативності розмірів)
    stats_dict["min_max_ratio"] = stats_dict["min_size"] / stats_dict["max_size"] if stats_dict["max_size"] > 0 else 0
    
    # Точки аномалій (використання правила 1.5*IQR)
    lower_bound = stats_dict["q1_size"] - 1.5 * stats_dict["iqr"]
    upper_bound = stats_dict["q3_size"] + 1.5 * stats_dict["iqr"]
    
    outliers = sizes[(sizes < lower_bound) | (sizes > upper_bound)]
    stats_dict["outlier_count"] = len(outliers)
    stats_dict["outlier_percentage"] = (len(outliers) / len(sizes)) * 100 if len(sizes) > 0 else 0
    
    # Частотний аналіз: розподіл файлів за розмірами у логарифмічних інтервалах
    # Це дає уявлення про кластеризацію файлів за розмірами
    if np.all(sizes > 0):
        log_sizes = np.log10(sizes)
        min_log = np.floor(np.min(log_sizes))
        max_log = np.ceil(np.max(log_sizes))
        
        # Створюємо логарифмічні інтервали
        log_bins = np.arange(min_log, max_log + 1)
        size_ranges = 10 ** log_bins
        
        # Підраховуємо кількість файлів у кожному інтервалі
        bin_indices = np.digitize(sizes, size_ranges)
        size_distribution = dict(Counter(bin_indices))
        
        # Перетворюємо на зручний формат для інтерпретації
        formatted_distribution = {}
        for idx, count in size_distribution.items():
            if idx > 0 and idx <= len(size_ranges):
                lower = size_ranges[idx-1]
                upper = size_ranges[idx] if idx < len(size_ranges) else float('inf')
                key = f"{lower:.0f}-{upper:.0f}" if upper != float('inf') else f"{lower:.0f}+"
                formatted_distribution[key] = count
                
        stats_dict["size_distribution"] = formatted_distribution
    
    return stats_dict

def print_file_statistics(stats_dict, format_bytes=True):
    """
    Форматує та виводить статистичні показники у читабельному вигляді.
    
    Args:
        stats_dict (dict): Словник зі статистичними показниками
        format_bytes (bool): Чи форматувати байти у читабельний вигляд
    """
    if "error" in stats_dict:
        print(f"Помилка: {stats_dict['error']}")
        return
    
    def format_size(size):
        """Форматує розмір у читабельний вигляд"""
        if not format_bytes or size is None:
            return size
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        formatted_size = size
        
        while formatted_size >= 1024 and unit_index < len(units) - 1:
            formatted_size /= 1024
            unit_index += 1
            
        return f"{formatted_size:.2f} {units[unit_index]}"
    
    print("\n=== СТАТИСТИКА РОЗМІРІВ ФАЙЛІВ ===\n")
    
    print("--- ОСНОВНІ ПОКАЗНИКИ ---")
    print(f"Загальна кількість файлів: {stats_dict['file_count']:,}")
    print(f"Загальний розмір всіх файлів: {format_size(stats_dict['total_size'])}")
    
    print("\n--- АБСОЛЮТНІ РОЗМІРИ ---")
    print(f"Мінімальний розмір файлу: {format_size(stats_dict['min_size'])}")
    print(f"Максимальний розмір файлу: {format_size(stats_dict['max_size'])}")
    print(f"Середній розмір файлу: {format_size(stats_dict['mean_size'])}")
    print(f"Медіанний розмір файлу: {format_size(stats_dict['median_size'])}")
    print(f"Найпоширеніший розмір файлу (мода): {format_size(stats_dict['mode_size'])} "
          f"(зустрічається {stats_dict['mode_frequency']} разів, "
          f"{stats_dict['mode_percentage']:.2f}% від загальної кількості)")
    
    print("\n--- ВІДНОСНІ РОЗМІРИ ---")
    print(f"Мінімальний відносний розмір: {stats_dict['min_relative_size']*100:.8f}% від загального")
    print(f"Максимальний відносний розмір: {stats_dict['max_relative_size']*100:.2f}% від загального")
    
    print("\n--- МІРИ РОЗСІЮВАННЯ ---")
    print(f"Стандартне відхилення: {format_size(stats_dict['std_dev'])}")
    print(f"Дисперсія: {format_size(stats_dict['variance'])}")
    print(f"Міжквартильний діапазон (IQR): {format_size(stats_dict['iqr'])}")
    print(f"Коефіцієнт варіації (CV): {stats_dict['cv']:.2f}%")
    
    print("\n--- КВАРТИЛІ ---")
    print(f"Перший квартиль (Q1, 25%): {format_size(stats_dict['q1_size'])}")
    print(f"Медіана (Q2, 50%): {format_size(stats_dict['median_size'])}")
    print(f"Третій квартиль (Q3, 75%): {format_size(stats_dict['q3_size'])}")
    
    print("\n--- ФОРМА РОЗПОДІЛУ ---")
    print(f"Коефіцієнт асиметрії: {stats_dict['skewness']:.2f}")
    if stats_dict['skewness'] > 0:
        print("  (Позитивна асиметрія: багато маленьких файлів і декілька дуже великих)")
    elif stats_dict['skewness'] < 0:
        print("  (Негативна асиметрія: багато великих файлів і декілька дуже маленьких)")
    else:
        print("  (Симетричний розподіл)")
        
    print(f"Коефіцієнт ексцесу: {stats_dict['kurtosis']:.2f}")
    if stats_dict['kurtosis'] > 0:
        print("  (Висока гостровершинність: значення сконцентровані навколо середнього)")
    elif stats_dict['kurtosis'] < 0:
        print("  (Низька гостровершинність: значення розподілені більш рівномірно)")
    else:
        print("  (Нормальний розподіл)")
    
    print("\n--- АНАЛІЗ НЕРІВНОМІРНОСТІ ---")
    print(f"Коефіцієнт Джині: {stats_dict['gini_coefficient']:.4f}")
    if stats_dict['gini_coefficient'] < 0.3:
        print("  (Низька нерівномірність розмірів)")
    elif stats_dict['gini_coefficient'] < 0.6:
        print("  (Помірна нерівномірність розмірів)")
    else:
        print("  (Висока нерівномірність розмірів)")
        
    print(f"Аналіз Парето: {stats_dict['pareto_threshold']*100:.2f}% найбільших файлів займають 80% загального простору")
    
    print("\n--- ДОДАТКОВА ІНФОРМАЦІЯ ---")
    print(f"Відсоток файлів, менших за середній розмір: {stats_dict['percent_below_mean']:.2f}%")
    
    if stats_dict['geometric_mean'] is not None:
        print(f"Геометричне середнє: {format_size(stats_dict['geometric_mean'])}")
    
    print(f"Співвідношення мін/макс: {stats_dict['min_max_ratio']:.8f}")
    
    print(f"Кількість викидів (аномальних розмірів): {stats_dict['outlier_count']} "
          f"({stats_dict['outlier_percentage']:.2f}% від загальної кількості)")
    
    if "size_distribution" in stats_dict:
        print("\n--- РОЗПОДІЛ ФАЙЛІВ ЗА РОЗМІРАМИ ---")
        for size_range, count in sorted(stats_dict["size_distribution"].items()):
            print(f"{size_range}: {count} файлів ({count/stats_dict['file_count']*100:.2f}%)")
    
    print("\n" + "="*35)

def plot_file_size_statistics(input_list, title="Статистика розмірів файлів"):
    """
    Створює набір графіків для візуалізації статистики розмірів файлів.
    
    Args:
        input_list (list): Список розмірів файлів у байтах
        title (str): Заголовок для графіків
        
    Returns:
        matplotlib.figure.Figure: Об'єкт фігури з графіками
    """
    if not input_list or len(input_list) == 0:
        print("Список розмірів файлів порожній")
        return None
        
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=16)
    
    sizes = np.array(input_list)
    
    # 1. Гістограма розподілу розмірів (з логарифмічною шкалою для осі X)
    if np.all(sizes > 0):  # Уникаємо помилок з логарифмічною шкалою
        ax = axs[0, 0]
        # Використовуємо логарифмічну шкалу для кращого відображення
        log_sizes = np.log10(sizes)
        min_log = np.floor(np.min(log_sizes))
        max_log = np.ceil(np.max(log_sizes))
        log_bins = np.linspace(min_log, max_log, min(50, int(max_log - min_log + 1) * 5))
        bins = 10 ** log_bins
        
        hist, bin_edges = np.histogram(sizes, bins=bins)
        widths = np.diff(bin_edges)
        
        ax.bar(bin_edges[:-1], hist, width=widths, align='edge', alpha=0.7)
        ax.set_xscale('log')
        ax.set_title('Розподіл розмірів файлів (лог. шкала)')
        ax.set_xlabel('Розмір файлу (байти)')
        ax.set_ylabel('Кількість файлів')
        
        # Додаємо вертикальні лінії для середнього та медіанного значень
        ax.axvline(np.mean(sizes), color='r', linestyle='--', label=f'Середнє: {np.mean(sizes):.1f}')
        ax.axvline(np.median(sizes), color='g', linestyle='-.', label=f'Медіана: {np.median(sizes):.1f}')
        
        # Додаємо легенду
        ax.legend()
    
    # 2. Boxplot (коробка з вусами) для розмірів
    ax = axs[0, 1]
    ax.boxplot(sizes, vert=False, showfliers=False)  # Не показуємо викиди для кращої читабельності
    ax.set_title('Коробка з вусами (без викидів)')
    ax.set_xlabel('Розмір файлу (байти)')
    ax.set_xscale('log')
    ax.grid(True, alpha=0.3)
    
    # 3. Крива Лоренца (показує нерівномірність розподілу)
    ax = axs[1, 0]
    sorted_sizes = np.sort(sizes)
    cum_sizes = np.cumsum(sorted_sizes)
    cum_proportions = cum_sizes / np.sum(sizes)
    
    # Лінія ідеально рівномірного розподілу
    ax.plot([0, 1], [0, 1], 'k--', label='Рівномірний розподіл')
    
    # Фактична крива Лоренца
    ax.plot(np.linspace(0, 1, len(sizes)), cum_proportions, label='Фактичний розподіл')
    
    # Заповнюємо область між кривими
    ax.fill_between(np.linspace(0, 1, len(sizes)), np.linspace(0, 1, len(sizes)), 
                    cum_proportions, alpha=0.2)
    
    ax.set_title('Крива Лоренца (нерівномірність розмірів)')
    ax.set_xlabel('Накопичена частка файлів')
    ax.set_ylabel('Накопичена частка простору')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # 4. Топ-5 найбільших файлів (у відсотках від загального розміру)
    ax = axs[1, 1]
    
    # Сортуємо розміри за спаданням і беремо топ-5
    top_sizes = np.sort(sizes)[::-1][:min(5, len(sizes))]
    top_percentages = top_sizes / np.sum(sizes) * 100
    
    # Додаємо решту файлів як одну категорію
    if len(sizes) > 5:
        rest_percentage = 100 - np.sum(top_percentages)
        labels = [f'Файл #{i+1}: {size:.1f} байт ({pct:.2f}%)' 
                 for i, (size, pct) in enumerate(zip(top_sizes, top_percentages))]
        labels.append(f'Інші файли ({len(sizes)-5:,}): {rest_percentage:.2f}%')
        sizes_to_plot = np.append(top_percentages, rest_percentage)
    else:
        labels = [f'Файл #{i+1}: {size:.1f} байт ({pct:.2f}%)' 
                 for i, (size, pct) in enumerate(zip(top_sizes, top_percentages))]
        sizes_to_plot = top_percentages
    
    ax.pie(sizes_to_plot, labels=None, autopct='%1.1f%%', startangle=90, 
           wedgeprops={'edgecolor': 'w', 'linewidth': 1})
    ax.set_title('Топ-5 найбільших файлів (% від загального розміру)')
    
    # Додаємо легенду за межами діаграми
    ax.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    
    return fig

def analyze_file_sizes(input_list):
    """
    Комплексний аналіз розмірів файлів: обчислює статистики, 
    виводить на екран і створює візуалізації.
    
    Args:
        input_list (list): Список розмірів файлів у байтах
        
    Returns:
        tuple: (статистичний_словник, matplotlib_фігура)
    """
    # Обчислюємо статистичні показники
    stats = get_file_statistics(input_list)
    
    # Виводимо результати
    print_file_statistics(stats)
    
    # Створюємо візуалізації
    fig = plot_file_size_statistics(input_list)
    
    return stats, fig
