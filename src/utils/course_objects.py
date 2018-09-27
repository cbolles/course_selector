class ProgramType(enum.Enum):
    immersion = 'immersion'
    minor = 'minor'
    major = 'major'


class Course:
    __slots__ = ['name', 'course_id']

    def __init__(self, name, course_id):
        self.name = name
        self.course_id = course_id


class Program:
    __slots__ = ['name', 'program_type', 'prereqs', 'electives', 'notes']

    def __init__(self, name, program_type):
        self.name = name
        self.program_type = program_type
        self.prereqs = []
        self.electives = []


