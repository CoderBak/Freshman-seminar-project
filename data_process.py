class Lecture:
    def __init__(self, dictionary):
        self.name = dictionary['name']
        self.length = dictionary['length']
        self.start_time = date_to_absolute_time(dictionary['time'])
        self.end_time = self.start_time + self.length
        self.allowed_cnt = dictionary['allowed_cnt']

    def check_if_available(self, student):
        for valid_time in student.timetable:
            valid_start_time = date_to_absolute_time(valid_time[:2])
            valid_end_time = valid_start_time + valid_time[2]
            if valid_start_time <= self.start_time and self.end_time <= valid_end_time:
                return True
        return False


class Student:
    def __init__(self, dictionary):
        self.name = dictionary['name']
        self.id = dictionary['id']
        self.timetable = dictionary['timetable']
        self.prefer_lecture = []
        self.allowed_lecture = []
        for lecture in dictionary['lecture']:
            self.prefer_lecture.append(lecture_find_system[lecture])

    def clear_invalid_lecture(self):
        for lecture in self.prefer_lecture:
            if lecture.check_if_available(self):
                self.allowed_lecture.append(lecture)


def date_to_absolute_time(lst_of_date):
    weekday = week[lst_of_date[0]]
    time = lst_of_date[1]
    return (weekday - 1) * 24 * 2 + time


week = {'Mon': 1, 'Tues': 2, 'Wed': 3, 'Thur': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}

all_lecture = []

all_student = []

lecture_find_system = {}


def data_process():
    total_allowed_people = 0
    total_student = 0

    file = open('output.txt', "w")

    for lines in open('lecture.txt'):
        current_lecture_dict = eval('dict(' + lines[:len(lines)-1] + ')')
        current_lecture = Lecture(current_lecture_dict)
        all_lecture.append(current_lecture)
        lecture_find_system[current_lecture.name] = current_lecture

    for lines in open('student.txt'):
        current_student_dict = eval('dict(' + lines[:len(lines)-1] + ')')
        current_student = Student(current_student_dict)
        all_student.append(current_student)

    for student in all_student:
        student.clear_invalid_lecture()
        total_student += 1

    for lecture in all_lecture:
        total_allowed_people += lecture.allowed_cnt

    file.write('{0} {1}\n'.format(total_student, total_allowed_people))

    total_student = 0
    total_allowed_people = 0
    total_edge = 0

    for student in all_student:
        for lecture in student.allowed_lecture:
            for i in range(lecture.allowed_cnt):
                file.write('{0} {1}\n'.format(total_student + 1, total_allowed_people + i + 1))
                total_edge += 1
            total_allowed_people += lecture.allowed_cnt
        total_student += 1

    file.close()

data_process()