import csv

from statistics import mean


def get_annual_salary(salary: float) -> float:
    return salary * 8 * 22 * 12


def clean_salary_data(path_to_file, aggregator_name) -> None:
    with open(path_to_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        with open(f'./cleaned_data/{aggregator_name}_cleaned_salary.csv', 'w', newline='') as cleaned_csv:
            writer = csv.writer(cleaned_csv, delimiter=',')
            for row in reader:
                if len(row) != 0 and row[-3] != 'noSalaryInfoAtAll':
                    if row[-1] == 'salaryText':
                        row[-3] = 'salary'
                        writer.writerow(row[:-2])
                    elif 'an hour' in row[-1]:
                        salary_max = float(row[-3])
                        salary_min = float(row[-2])
                        row[-3] = mean([get_annual_salary(salary_min), get_annual_salary(salary_max)])
                        writer.writerow(row[:-2])
                    else:
                        salary_max = float(row[-3])
                        salary_min = float(row[-2])
                        row[-3] = mean([salary_min, salary_max])
                        writer.writerow(row[:-2])
