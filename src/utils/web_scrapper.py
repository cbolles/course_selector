import configparser
from bs4 import BeautifulSoup
import urllib.request
from utils.course_objects import ProgramType, Program, CourseType, Course


def get_config(config_file: str) -> dict:
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def get_url(config, program_name, program_type):
    if program_type == ProgramType.immersion:
        return config['immersions']['immersion_site'] + program_name
    elif program_type == ProgramType.minor:
        return config['minor']['minor_site'] + program_name
    return config['major']['major_site'] + program_name


def get_notes(note_element):
    notes = ''
    for note in note_element.find_all('li'):
        notes += ''.join(note.findAll(text=True)).strip() + '\n'
    return notes.strip()


def get_courses(course_table):
    prereq_courses = []
    elective_courses = []
    course_type = CourseType.prereq

    for raw_course in course_table.find_all('tr'):
        course_details = raw_course.find_all('td')
        if len(course_details) > 1:
            course_id = course_details[0].string.strip()
            course_name = course_details[1].string.strip()
            if course_type == CourseType.prereq:
                prereq_courses.append(Course(course_name, course_id))
            elif course_type == CourseType.elective:
                elective_courses.append(Course(course_name, course_id))
        elif len(course_details) > 0 and CourseType.elective.value in course_details[0].string.lower():
            course_type = CourseType.elective

    return prereq_courses, elective_courses


def get_program_data(config, program_name, program_type):
    url = get_url(config, program_name, program_type)

    immersion_page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(immersion_page, features='html.parser')

    notes = get_notes(soup.find_all('ul')[2])
    courses = get_courses(soup.table.tbody)

    return Program(program_name, program_type, notes, courses[0], courses[1])


def test():
    config = get_config('../properties/web_details.ini')
    program = get_program_data(config, 'mathematics', ProgramType.immersion)
    print(program.notes)
    print(program.prereqs)
    print(program.electives)


if __name__ == '__main__':
    test()




