import configparser
from bs4 import BeautifulSoup
import urllib.request
from utils.course_objects import ProgramType, CourseType, Course


def get_config(config_file: str) -> dict:
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def get_program_data(config, program_name, program_type):
    if program_type == ProgramType.immersion:
        url = config['immersions']['immersion_site'] + program_name
    elif program_type == ProgramType.minor:
        url = config['minor']['minor_site'] + program_name
    else:
        url = config['major']['major_site'] + program_name

    immersion_page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(immersion_page, features='html.parser')
    course_body = soup.table.tbody

    prereq_courses = []
    elective_courses = []
    course_type = CourseType.prereq
    for raw_course in course_body.find_all('tr'):
        course_details = raw_course.find_all('td')
        if len(course_details) > 1:
            course_id = course_details[0].string
            course_name = course_details[1].string
            if course_type == CourseType.prereq:
                prereq_courses.append(Course(course_name, course_id))
            elif course_type == CourseType.elective:
                elective_courses.append(Course(course_name, course_id))
        elif len(course_details) > 0 and CourseType.elective.value in course_details[0].string.lower():
            print(course_details)
            course_type = CourseType.elective

    print(prereq_courses)
    print(elective_courses)

    # print(raw_course_details.prettify())


def test():
    config = get_config('../properties/web_details.ini')
    get_program_data(config, 'mathematics', ProgramType.immersion)


if __name__ == '__main__':
    test()




