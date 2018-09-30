from enum import Enum


class CourseType(Enum):
    prereq = 'prerequisite'
    required = 'required'
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

    def __init__(self, num_required):
        self.courses = []
        self.num_required = num_required

    def __str__(self):
        return 'Number Required: ' + str(self.num_required) + ' ' + str(self.courses)

    def __repr__(self):
        return self.__str__()


class Program:
    __slots__ = ['name', 'program_type', 'prereqs', 'required', 'electives', 'notes']

    def __init__(self):
        self.prereqs = []
        self.required = []
        self.electives = []

    def add_new_course_sequence(self, num_required, course_type):
        if course_type == CourseType.prereq:
            self.prereqs.append(CourseSequence(num_required))
        elif course_type == CourseType.required:
            self.required.append(CourseSequence(num_required))
        elif course_type == CourseType.elective:
            self.electives.append(CourseSequence(num_required))

    def add_course(self, course, course_type):
        if course_type == CourseType.prereq:
            self.prereqs[-1].courses.append(course)
        elif course_type == CourseType.elective:
            self.electives[-1].courses.append(course)

    def clean(self):
        for i in range(0, len(self.prereqs)):
            if i < len(self.prereqs) and len(self.prereqs[i].courses) == 0:
                self.prereqs.pop(i)
        for j in range(0, len(self.required)):
            if j < len(self.required) and len(self.required[j].courses) == 0:
                self.required.pop(j)
        for k in range(0, len(self.electives)):
            print(k)
            if k < len(self.electives) and len(self.electives[k].courses) == 0:
                self.electives.pop(k)

