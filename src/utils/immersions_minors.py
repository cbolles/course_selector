import configparser
from bs4 import BeautifulSoup
import urllib.request
from utils.course_objects import ProgramType, Program, CourseType, CourseSequence, Course


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


def get_num_options(string):
    convert = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10
    }
    string_data = string.split()
    for data in string_data:
        if data in convert:
            return convert[data]
    return 0


def get_course_type(raw_data):
    if CourseType.prereq.value in raw_data:
        return CourseType.prereq
    elif CourseType.required.value in raw_data:
        return CourseType.required
    elif CourseType.elective.value in raw_data:
        return CourseType.elective


def is_course_type_element(table_element, index):
    return table_element[index].find('strong') is not None


def is_num_required(table_element, index):
    return table_element[index].find('em') is not None


def is_special_column(table_element, index):
    return is_course_type_element(table_element, index) or is_num_required(table_element, index)


def get_num_required(table_data, index):
    if len(table_data[index+1]) == 1:
        return get_num_options(table_data[index+1].em[0].string)
    count = 1
    while count+index < len(table_data) and not is_special_column(table_data, index):
        count += 1
    return count


def get_new_course_sequence(table_data, index):
    string_data = table_data[index].strong.string.lower()
    course_type = get_course_type(string_data)
    num_required = get_num_required(table_data, index)
    return num_required, course_type


def get_course_data(table_data, index):
    course_data = table_data[index].find_all('td')
    course_id = course_data[0].string.strip()
    course_name = course_data[1].string.strip()
    return Course(course_name, course_id)


def get_program_data(course_table):
    course_type = CourseType.prereq
    program = Program()

    index = 1

    table_data = course_table.find_all('tr')
    while index < len(table_data):
        if len(table_data[index]) == 2 and table_data[index].find('strong') is not None:
            new_sequence_data = get_new_course_sequence(table_data, index)
            program.add_new_course_sequence(new_sequence_data[0], new_sequence_data[1])
            course_type = new_sequence_data[1]
        elif len(table_data[index]) == 2 and is_num_required(table_data, index):
            num_options = get_num_options(table_data[index].em.string)
            program.add_new_course_sequence(num_options, course_type)
        elif len(table_data[index]) == 4:
            course = get_course_data(table_data, index)
            program.add_course(course, course_type)
        index += 1
    program.clean()
    return program


def get_data(config, program_name, program_type):
    url = get_url(config, program_name, program_type)

    immersion_page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(immersion_page, features='html.parser')

    notes = get_notes(soup.find_all('ul')[2])
    program = get_program_data(soup.table.tbody)
    program.notes = notes
    program.name = program_name
    program.program_type = program_type

    return program


def test():
    config = get_config('../properties/web_details.ini')
    program = get_data(config, 'environmental-studies', ProgramType.immersion)
    print(program.notes)
    print(program.prereqs)
    print(program.required)
    print(program.electives)


if __name__ == '__main__':
    test()




