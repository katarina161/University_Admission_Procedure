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


class Department:
    def __init__(self, name, places=0):
        self.name = name
        self.places = places
        self.students = []

    def enroll_students(self, students):
        self.students.extend(students)
        self.students.sort(reverse=True)
        self.places -= len(students)

    def __str__(self):
        dep_str = self.name + "\n"
        dep_str += "\n".join([str(a) for a in self.students])
        return dep_str + "\n"


class University:
    def __init__(self):
        self.departments = {"Biotech": Department("Biotech"),
                            "Chemistry": Department("Chemistry"),
                            "Engineering": Department("Engineering"),
                            "Mathematics": Department("Mathematics"),
                            "Physics": Department("Physics")}
        self.applicants = []

    def set_empty_places(self, places):
        for dep in self.departments.values():
            dep.places = places

    def get_applicants_per_department(self, start=0):
        applicants_per_department = {key: [] for key in self.departments}
        for applicant in self.applicants:
            applicants_per_department[applicant.choices[start]].append(applicant)

        for key, val in applicants_per_department.items():
            val.sort(reverse=True)

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

    def __str__(self):
        u_str = "University:\n"
        u_str += '\n'.join([str(a) for a in self.applicants])
        return u_str


class Applicant:

    def __init__(self, first_name, last_name, gpa, choices):
        self.first_name = first_name
        self.last_name = last_name
        self.gpa = gpa
        self.choices = choices

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.gpa}"

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
    university.applicants = get_applicants("applicant_list.txt")
    # print(university)
    # print()
    # for key, val in university.get_applicants_per_department().items():
    #     print(key, *val, sep="\n")
    #     print()
    university.enroll_applicants()
    for department in university.departments.values():
        print(department)


if __name__ == "__main__":
    main()
