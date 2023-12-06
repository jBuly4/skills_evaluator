import csv
import json
import logging
import os
from typing import Generator

import openai
import tiktoken

from datetime import datetime
from statistics import mean

from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

# To see how many tokens are used by an API call, check the usage field in the API response (e.g., response['usage'][
# 'total_tokens']).


def truncate_text_for_max_tokens(text, max_tokens=3995):
    """Truncate length of incoming text"""
    encoding = tiktoken.get_encoding('cl100k_base')
    tokens = encoding.encode(text)
    num_tokens = len(tokens)

    if num_tokens > max_tokens:
        tokens_trunk = tokens[:max_tokens]
        return encoding.decode(tokens_trunk)

    return text


def get_skill_from_description(description: str):
    """Call api of ChatGPT, prepare it for the role you want, thn send promt and get response"""
    client = openai.OpenAI(
            api_key=os.getenv('OPEN_AI_API'),
    )
    prompt = (f'Evaluate which skills are required in the following job description. Extract 10 skills from the '
              f'following job description and return them in a json dict: '
              f'{{"skills": ["skill_1", "skill_2", ..., "skill_n"]}}. '
              f'Skills must be one or two words but also skills should be understandable what they mean. Here is '
              f'the description: {description}')
    model = 'gpt-3.5-turbo'
    messages = [
        {
            'role': 'system',
            'content': 'You are experienced datascientist, skilled in extracting precise skill from different data'
        },
        {
            'role': 'user',
            'content': prompt
        }
    ]
    response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
    )

    return response.choices[0].message.content


def get_annual_salary(salary: float) -> float:
    """Compute annual salary from hour payment"""
    return salary * 8 * 22 * 12


def clean_job_raw_data(path_to_file, aggregator_name) -> str:
    """
    Main function for raw data preparing. The main purposue is to get raw line with correct length and skills
    description cleaned from HTML tags and truncated to the length for gpt-3.5-turbo model.
    :param path_to_file: source file
    :param aggregator_name: aggregator name
    :return: path to prepared raw data
    """
    with open(path_to_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        path_to_raw_data = f'./cleaned_data/{aggregator_name}_cleaned_salary-{datetime.now()}.csv'
        with open(path_to_raw_data, 'w', newline='') as cleaned_csv:
            writer = csv.writer(cleaned_csv, delimiter=',')
            for row in reader:
                if len(row) != 0 and row[-3] != 'noSalaryInfoAtAll':
                    if row[-1] == 'salaryText':
                        row[-3] = 'salary'
                        writer.writerow([row[0], row[5], row[7], row[-3]])
                    elif 'an hour' in row[-1]:
                        salary_max = float(row[-3])
                        salary_min = float(row[-2])
                        row[-3] = mean([get_annual_salary(salary_min), get_annual_salary(salary_max)])
                        clean_text = BeautifulSoup(row[7], 'lxml').text.replace('\n', '').replace('\r', '')
                        text = truncate_text_for_max_tokens(clean_text)
                        writer.writerow([row[0], row[5], text, row[-3]])
                    else:
                        salary_max = float(row[-3])
                        salary_min = float(row[-2])
                        row[-3] = mean([salary_min, salary_max])
                        clean_text = BeautifulSoup(row[7], 'lxml').text.replace('\n', '').replace('\r', '')
                        text = truncate_text_for_max_tokens(clean_text)
                        writer.writerow([row[0], row[5], text, row[-3]])
    return path_to_raw_data


def get_skills(path_to_file, start_row=1) -> Generator[tuple]:
    """
    Generate rows with skills from ChatGPT
    :param path_to_file: source file with data
    :param start_row: start row
    :return: tuple which consists of cleaned data with skills
    """
    with open(path_to_file, 'r') as csv_file:
        reader = csv.reader(csv_file)

        # skip rows before start row
        for _ in range(start_row - 1):
            next(reader)

        for row in reader:
            if row[0] == 'keyword':
                yield row[0], row[1], 'skills', row[-1]
            else:
                skills_raw = get_skill_from_description(row[-2])
                try:
                    skills_json = json.loads(get_skill_from_description(row[-2]))
                    skills = ', '.join(skills_json['skills'])
                    logging.info(f'Skills list: {skills}')
                    yield row[0], row[1], skills, row[-1]
                except Exception as e:
                    logging.error(f'No skills list: {skills_raw}, error: {e}')
                    yield row[0], row[1], 0, row[-1]


def create_clean_file(path_to_source_file, aggregator_name, start_row=0) -> None:
    """
    Create file with cleaned data and skills, which are generated by ChatGPT
    :param path_to_source_file: file with raw data after parsing jobsite
    :param aggregator_name: aggregator name
    :param start_row: if something went wrong you can start from other row to avoid repetions in requests
    """
    file_path = f'./cleaned_data/skill_sets/{aggregator_name}_skill_set.csv'
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        if not start_row:
            for row in get_skills(path_to_source_file):
                writer.writerow([row[0], row[1], row[2], row[3]])
        else:
            for row in get_skills(path_to_source_file, start_row):
                writer.writerow([row[0], row[1], row[2], row[3]])


if __name__ == '__main__':
    logging.basicConfig(
            format='[%(asctime)s] %(levelname).1s %(message)s',
            level=logging.INFO, datefmt='%Y.%m.%d %H:%M:%S'
    )
    path = '../../indeed_project/data/indeed_2023-11-28T21-27-52+00-00.csv'
    source_file = clean_job_raw_data(path, 'indeed')
    create_clean_file(source_file, 'indeed')
