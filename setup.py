from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:

    requirements_list:List[str] = []

    try :
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found. Please ensure it exists in the same directory as setup.py.")

    return requirements_list

print(get_requirements())

setup(
    name='AI_Trip_Planner',
    version='0.1.0',
    packages=find_packages(),
    author='Arun Kundil',
    author_email='arunkkd21@gmail.com',
    install_requires=get_requirements()
)

