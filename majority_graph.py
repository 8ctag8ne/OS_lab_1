import matplotlib.pyplot as plt
import numpy as np
import file_helper as fh
import two_pointers_technique as tp

def visualize_min_count_result(input_list, majority_coeff=0.9):
    """
    Створює кругову діаграму для результатів get_graph_values_for_min_count
    """
    count_values, l, r, relative_space = tp.get_graph_values_for_min_count(input_list, majority_coeff)
    
    # Створюємо мітки для сегментів діаграми
    labels = []
    if len(count_values) == 1:
        labels = [f'В інтервалі [{l}:{r}]']
    elif len(count_values) == 2:
        if l > 1:
            labels = [f'{l-1} файлів', f'{r-l+1} файлів']
        else:
            labels = [f'{r-l+1} файлів', f'{len(input_list) - r} файлів']
    else:  # len(count_values) == 3
        labels = [f'До інтервалу [1:{l-1}]', f'В інтервалі [{l}:{r}]', f'Після інтервалу [{r+1}:кінець]']
    
    # Створюємо кругову діаграму
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Обчислюємо відсотки для відображення
    percentages = [percent * 100 for percent in relative_space]
    
    # Додаємо відсотки до міток
    labels = [f'{labels[i]} ({percentages[i]:.1f}% простору)' for i in range(len(labels))]
    
    # Виділяємо основний сегмент (інтервал з мінімальною кількістю файлів)
    explode = [0] * len(count_values)
    if len(count_values) >= 2:
        explode[1] = 0.1  # Виділяємо інтервал з мінімальною кількістю файлів
    elif len(count_values) == 1:
        explode[0] = 0.1
    
    # Створюємо діаграму
    wedges, texts, autotexts = ax.pie(
        count_values, 
        explode=explode,
        labels=labels, 
        autopct='%1.1f%%',
        shadow=True, 
        startangle=90
    )
    
    # Покращуємо читабельність
    for text in texts:
        text.set_fontsize(9)
    
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_weight('bold')
    
    # Додаємо заголовок
    plt.title(f'Розподіл кількості файлів для інтервалу з мін. кількістю файлів\n'
              f'що займають принаймні {majority_coeff*100}% простору (всього {r} файлів)')
    
    plt.tight_layout()
    return fig

def visualize_min_range_result(input_list, majority_coeff=0.9):
    """
    Створює гістограму для результатів get_graph_values_for_min_range
    """
    range_values, l, r = tp.get_graph_values_for_min_range(input_list, majority_coeff)
    
    # Створюємо мітки для стовпців гістограми
    labels = []
    if len(range_values) == 1:
        labels = [f'В інтервалі [{l}:{r}]']
    elif len(range_values) == 2:
        if l > 1:
            labels = [f'До інтервалу [1:{l-1}]', f'В інтервалі [{l}:{r}]']
        else:
            labels = [f'В інтервалі [{l}:{r}]', f'Після інтервалу [{r+1}:кінець]']
    else:  # len(range_values) == 3
        labels = [f'1 : {l-1} байт', f'{l} : {r} байт', f'{r+1} : {input_list[-1]} байт']
    
    # Створюємо гістограму
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Обчислюємо відсотки для підписів
    percentages = [val * 100 for val in range_values]
    
    # Створюємо стовпці з різними кольорами
    bars = ax.bar(labels, percentages, color=['lightblue', 'orange', 'lightgreen'][:len(percentages)])
    
    # Додаємо підписи над стовпцями
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f'{height:.1f}%',
            ha='center',
            va='bottom',
            fontweight='bold'
        )
    
    # Підписи осей та заголовок
    ax.set_xlabel('Групи файлів')
    ax.set_ylabel('Відсоток від загального простору, %')
    
    # Обчислюємо загальний розмір інтервалу в байтах
    total_size = sum(input_list)
    min_range_size = total_size * range_values[1] if 1 < len(range_values) else total_size * range_values[0]
    
    ax.set_title(f'Розподіл простору для інтервалу з мін. обсягом\n'
                f'що займає {majority_coeff*100}% загального простору')
    
    plt.ylim(0, 100)  # Обмежуємо діапазон осі Y від 0 до 100%
    plt.tight_layout()
    return fig

def visualize_results(input_list, majority_coeff=0.9):
    """
    Створює обидві візуалізації та відображає їх
    """
    # Сортуємо вхідний список, як це робиться у вашому коді
    input_list.sort()
    
    # Створюємо візуалізації
    min_count_fig = visualize_min_count_result(input_list, majority_coeff)
    min_range_fig = visualize_min_range_result(input_list, majority_coeff)
    
    # Відображаємо обидві візуалізації
    plt.show()

# Приклад використання:
# input_list = fh.get_sizes("file_size_sys.csv")
# visualize_results(input_list, 0.9)

# Для зручності - зберегти візуалізації у файли:
def save_visualizations(input_list, majority_coeff=0.9, count_filename="min_count_pie.png", range_filename="min_range_hist.png"):
    input_list.sort()
    
    min_count_fig = visualize_min_count_result(input_list, majority_coeff)
    min_range_fig = visualize_min_range_result(input_list, majority_coeff)
    
    min_count_fig.savefig(count_filename, dpi=300, bbox_inches='tight')
    min_range_fig.savefig(range_filename, dpi=300, bbox_inches='tight')
    
    print(f"Діаграми збережено у файли: {count_filename} та {range_filename}")
