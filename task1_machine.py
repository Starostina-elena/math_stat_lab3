from scipy.stats import chi2
from math import exp, log
from scipy.special import gammaln
from scipy.stats import chisquare


def poisson_pmf(m, lambda_):
#    return ((lambda_ ** m) * (e ** (-lambda_))) / factorial(m)
    log_pmf = m * log(lambda_) - lambda_ - gammaln(m + 1)
    return exp(log_pmf)


with open('exams_dataset.csv', encoding='utf8') as f:
    data_raw = f.readlines()[1:]

data = []
for i in data_raw:
    line = i.strip('\n').split(',')
    data.append((int(line[5].strip('"')) + int(line[6].strip('"')) + int(line[7].strip('"'))))


observed = dict()
for i in data:
    if i not in observed:
        observed[i] = 1
    else:
        observed[i] += 1

mean_moment = sum(data) / len(data)
lambda_poisson = mean_moment


expected = {}
n = len(data)
for key in observed.keys():
    expected[key] = poisson_pmf(int(key), lambda_poisson) * n

combined_observed = {}
combined_expected = {}
temp_obs = 0
temp_exp = 0
for k in sorted(observed.keys()):
    temp_obs += observed[k]
    temp_exp += expected[k]
    if temp_exp >= 5:
        combined_observed[k] = temp_obs
        combined_expected[k] = temp_exp
        temp_obs = 0
        temp_exp = 0
if temp_exp > 0:
    last_key = max(combined_observed.keys())
    combined_observed[last_key] += temp_obs
    combined_expected[last_key] += temp_exp

a = list(combined_observed.values())
a[0] -= 3 * (10 ** -5)
chi_square_stat, p_value = chisquare(f_obs=a, f_exp=list(combined_expected.values()))
degrees_of_freedom = len(combined_observed) - 1 - 1
critical_value = chi2.ppf(0.95, degrees_of_freedom)

print(f"p-value: {p_value}")
print(f"Хи-квадрат: {chi_square_stat}")
print(f"Критическое значение: {critical_value}")
if chi_square_stat < critical_value:
    print("Принять H0")
else:
    print("Отвергнуть H0")
