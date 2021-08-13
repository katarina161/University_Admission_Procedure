import os
from sys import stderr


def get_applicants(fpath):
    applicants = []

    try:
        with open(fpath, 'r') as fobj:
            for line in [l.strip() for l in fobj]:
                name, last_name, gpa, choices = line.split(maxsplit=3)
                applicants.append(Applicant(name, last_name, float(gpa), choices.split()))
    except FileNotFoundError:
        stderr.write(f"Error! File {fpath} does not exist. Cannot proceed.\n")
    except OSError as err:
        stderr.write(f"An error occurred while reading from file {fpath}:\n{err}\n")
    else:
        return applicants


def get_applicant_with_scores(fpath):
    applicants = []
    exams = ["physics", "chemistry", "math", "computer_science"]

    try:
        with open(fpath, 'r') as fobj:
            for line in [l.strip() for l in fobj]:
                applicant_data = line.split()
                name = applicant_data[0]
                last_name = applicant_data[1]
                scores = dict(zip(exams, [float(score) for score in applicant_data[2:6]]))
                choices = applicant_data[6:]
                applicants.append(Applicant(name, last_name, scores=scores, choices=choices))
    except FileNotFoundError:
        stderr.write(f"Error! File {fpath} does not exist. Cannot proceed.\n")
    except OSError as err:
        stderr.write(f"An error occurred while reading from file {fpath}:\n{err}\n")
    else:
        return applicants


def write_to_file(department):
    fpath = f"{department.name.lower()}.txt"
    try:
        with open(fpath, "w") as fobj:
            for s in department.students:
                fobj.write(f"{s.first_name} {s.last_name} {s.mean_score}\n")
    except os.error as err:
        stderr.write(f"An error occurred while trying to write to file {fpath}:\n{err}\n")


class Department:
    def __init__(self, name, places=0, exam=None):
        self.name = name
        self.places = places
        self.students = []
        self.exam = exam

    def enroll_students(self, students):
        self.students.extend(students)
        self.students.sort(key=lambda x: (-x.mean_score, (x.first_name + x.last_name)))
        self.places -= len(students)

    def __str__(self):
        dep_str = self.name + "\n"
        dep_str += "\n".join([f"{a.first_name} {a.last_name} {a.mean_score}" for a in self.students])
        return dep_str + "\n"


class University:
    departments = {"Biotech": Department("Biotech", exam=["chemistry", "physics"]),
                   "Chemistry": Department("Chemistry", exam=["chemistry"]),
                   "Engineering": Department("Engineering", exam=["computer_science", "math"]),
                   "Mathematics": Department("Mathematics", exam=["math"]),
                   "Physics": Department("Physics", exam=["physics", "math"])}

    def __init__(self):
        self.applicants = []

    def set_empty_places(self, places):
        for dep in self.departments.values():
            dep.places = places

    def get_applicants_per_department(self, start=0):
        applicants_per_department = {key: [] for key in self.departments}
        for applicant in self.applicants:
            department = self.departments[applicant.choices[start]]
            scores = [applicant.scores[exam] for exam in department.exam]
            applicant.mean_score = round(sum(scores) / len(scores), 1)

            applicants_per_department[department.name].append(applicant)

        for key, val in applicants_per_department.items():
            val.sort(key=lambda x: (-x.mean_score, (x.first_name + x.last_name)))

        return dict(sorted(applicants_per_department.items()))

    def remove_applicants(self, applicants):
        for a in applicants:
            self.applicants.remove(a)

    def enroll_applicants(self):
        i = 0
        while i <= 2:
            for key, val in self.get_applicants_per_department(start=i).items():
                department = self.departments[key]
                students = val[:department.places]
                department.enroll_students(students)
                self.remove_applicants(students)
            i += 1

    def save_data(self):
        for department in self.departments.values():
            write_to_file(department)

    def __str__(self):
        u_str = "University:\n"
        u_str += '\n'.join([str(a) for a in self.applicants])
        return u_str


class Applicant:

    def __init__(self, first_name, last_name, gpa=None, choices=None, scores: dict = None):
        self.first_name = first_name
        self.last_name = last_name
        self.gpa = gpa
        self.choices = choices
        self.scores = scores
        self.mean_score = None

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.scores} {self.choices}"

    def __eq__(self, other):
        return self.first_name == other.first_name and\
               self.last_name == other.last_name and\
               self.gpa == other.gpa

    def __lt__(self, other):
        return self.gpa < other.gpa or\
               (self.gpa == other.gpa and
                (self.first_name + self.last_name) > (other.first_name + other.last_name))


def main():
    empty_places = int(input())
    university = University()
    university.set_empty_places(empty_places)
    university.applicants = get_applicant_with_scores("applicant_list_scores.txt")
    # university.applicants = get_applicants("applicant_list.txt")
    # print(university)
    # print()
    # for key, val in university.get_applicants_per_department().items():
    #     print(key, *val, sep="\n")
    #     print()
    university.enroll_applicants()
    # for department in university.departments.values():
    #     print(department)
    university.save_data()


if __name__ == "__main__":
    main()
