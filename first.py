import time
import matplotlib.pyplot as plt

def test_for_n(n):
    dct = dict()

    time_start = time.time()

    for i in range(n):
        dct[n] = n

    time_end = time.time()

    print(f"Время добавления {n} элементов в словарь: {time_end - time_start}")

    return time_end - time_start


n_values = (1000, 10_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000)
times = []

for n_value in n_values:
    times.append(test_for_n(n_value))

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(n_values, times, color='royalblue', linestyle='-', marker='o', linewidth=2, label='Время работы')

ax.set_xscale('log')

ax.set_xticks(n_values)
ax.set_xticklabels([f'{n:,}'.replace(',', '_') for n in n_values])

ax.set_title('Зависимость времени выполнения от N', fontsize=14, fontweight='bold')
ax.set_xlabel('Размер входных данных (N)', fontsize=12)
ax.set_ylabel('Время выполнения (секунды)', fontsize=12)
ax.grid(True, which="both", linestyle=':', alpha=0.5)
ax.legend()

plt.tight_layout()
plt.show()