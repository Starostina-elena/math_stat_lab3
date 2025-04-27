from scipy.stats import t


with open('exams_dataset.csv', encoding='utf8') as file:
    data_raw = file.readlines()[1:]

data_course = []
data_without_course = []
for i in data_raw:
    line = i.strip('\n').split(',')
    ex_res = int(line[5].strip('"')) + int(line[6].strip('"')) + int(line[7].strip('"'))
    if line[4] == '"none"':
        data_without_course.append(ex_res)
    else:
        data_course.append(ex_res)

mean_course = sum(data_course) / len(data_course)
mean_without_course = sum(data_without_course) / len(data_without_course)

numerator = sum((x - mean_course) * (y - mean_without_course) for x, y in zip(data_course, data_without_course))
denominator_x = sum((x - mean_course) ** 2 for x in data_course)
denominator_y = sum((y - mean_without_course) ** 2 for y in data_without_course)

correlation = numerator / (denominator_x ** 0.5 * denominator_y ** 0.5)

t_stat_corr = (correlation * ((len(data_course) - 2) ** 0.5)) / ((1 - correlation ** 2) ** 0.5)
p_value_corr = 2 * t.sf(abs(t_stat_corr), len(data_course) - 2)
critical_value_corr = t.ppf(1 - 0.05 / 2, len(data_course) - 2)

print(f"Коэффициент корреляции: {correlation}")
print(f"Статистика корреляции: {t_stat_corr}")
print(f"p-value корреляции: {p_value_corr}")
print(f"Критическое значение: {critical_value_corr}")
