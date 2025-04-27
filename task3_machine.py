from scipy.stats import pearsonr, t


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

data_course.extend([*data_course])
data_course = data_course[:len(data_without_course)]


correlation, p_value_corr = pearsonr(data_course, data_without_course)
t_stat_corr = (correlation * ((len(data_course) - 2) ** 0.5)) / ((1 - correlation ** 2) ** 0.5)
critical_value_corr = t.ppf(1 - 0.05 / 2, len(data_course) - 2)

print(f"Коэффициент корреляции: {correlation}")
print(f"Статистика корреляции: {t_stat_corr}")
print(f"p-value корреляции: {p_value_corr}")
print(f"Критическое значение: {critical_value_corr}")
