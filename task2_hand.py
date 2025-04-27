from scipy.stats import t, f


with open('exams_dataset.csv', encoding='utf8') as file:
    data_raw = file.readlines()[1:]

data_math = []
data_reading = []
for i in data_raw:
    line = i.strip('\n').split(',')
    data_math.append((int(line[5].strip('"'))))
    data_reading.append((int(line[6].strip('"'))))

math_mean = sum(data_math) / len(data_math)
reading_mean = sum(data_reading) / len(data_reading)

math_var = sum((x - math_mean) ** 2 for x in data_math) / len(data_math)
reading_var = sum((x - reading_mean) ** 2 for x in data_reading) / len(data_reading)

f_stat = max(math_var, reading_var) / min(math_var, reading_var)
t_stat = abs(math_mean - reading_mean) / ((math_var / len(data_math) + reading_var / len(data_reading)) ** 0.5)

t_critical = t.ppf(1 - 0.05 / 2, len(data_math) + len(data_reading) - 2)
f_critical = f.ppf(1 - 0.05, len(data_math), len(data_reading))

p_value_t = 2 * (1 - t.cdf(abs(t_stat), len(data_math) + len(data_reading) - 2))
p_value_f = 1 - f.cdf(f_stat, len(data_math) - 1, len(data_reading) - 1)


print(f"Математика: мат ожидание {math_mean}, дисперсия {math_var}")
print(f"Чтение: мат ожидание {reading_mean}, дисперсия {reading_var}")

print(f"Статистика: f {f_stat}, t {t_stat}")
print(f"Критические значения: {f_critical}, {t_critical}")

print(f"p-value: f {p_value_f}, t {p_value_t}")
