from enum import Enum


class CourseType(Enum):
    prereq = 'prerequisite'
    elective = 'elective'


class ProgramType(Enum):
    immersion = 'immersion'
    minor = 'minor'
    major = 'major'


class Course:
    __slots__ = ['name', 'course_id']

    def __init__(self, name, course_id):
        self.name = name
        self.course_id = course_id

    def __str__(self):
        return 'Name: ' + self.name + ', ID: ' + self.course_id

    def __repr__(self):
        return self.__str__()


class CourseSequence:
    __slots__ = ['courses', 'num_required']

    def __init__(self):
        self.courses = []
        self.num_required = 0

    def __init__(self, courses, num_required):
        self.courses = courses
        self.num_required = num_required


class Program:
    __slots__ = ['name', 'program_type', 'prereqs', 'electives', 'notes']

    def __init__(self, name, program_type):
        self.name = name
        self.program_type = program_type
        self.preq = CourseSequence()
        self.electives = CourseSequence()


