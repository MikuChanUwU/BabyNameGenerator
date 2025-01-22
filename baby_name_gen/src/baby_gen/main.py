#!/usr/bin/env python
import sys
import warnings

from crew import BabyNameGen

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():

    # request user input for detail about baby names
    baby_details = input("Enter all the details of your baby! Gender, birth date and other personal preferences. Be as specific as you want!: ")

    """
    Run the crew.
    """
    inputs = {
        'topic': 'Baby Names',
        'topic_details': baby_details,
        'date': '2025-01-22'
    }
    BabyNameGen().crew().kickoff(inputs=inputs)

run()
