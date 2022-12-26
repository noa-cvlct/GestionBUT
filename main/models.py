import math
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Establishment(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    def getDepartments(self):
        # Retourne les départements appartenant à l'établissement
        return Department.objects.filter(establishment=self)

    def getProfessors(self):
        professors = []                                 # Liste de retour
        for department in self.getDepartments():        # Loop les départements de l'établissement
            for professor in department.getProfessors():    # Loop les professeurs associés
                if professor not in professors:                 # Check pour l'insertion unique de prof
                    professors.append(professor)                    # Insert le prof dans la liste
        return professors

    def createITDepartment(self):
        department = Department(name="Informatique", establishment=self)
        department.save()
        str_ues = {
            1: [
                "Développer des applications informatiques simples",
                "Partir des exigences et aller jusqu'à une application complète",
                "Adapter des applications sur un ensemble de supports (embarqué, web, mobile, IoT…)"
            ],
            2: [
                "Appréhender et construire des algorithmes",
                "Sélectionner les algorithmes adéquats pour répondre à un problème donné",
                "Analyser et optimiser des applications"
            ],
            3: [
                "Installer et configurer un poste de travail",
                "Déployer des services dans une architecture réseau",
                "Faire évoluer et maintenir un système informatique communicant en conditions opérationnelles"
            ],
            4: [
                "Concevoir et mettre en place une base de données à partir d'un cahier des charges client",
                "Optimiser une base de données, interagir avec une application et mettre en œuvre la sécurité",
                "Administrer une base de données, concevoir et réaliser des systèmes d'informations décisionnels"
            ],
            5: [
                "Identifier les besoins métiers des clients et des utilisateurs",
                "Appliquer une démarche de suivi de projet en fonction des besoins métiers des clients et des utilisateurs",
                "Participer à la conception et à la mise en oeuvre d'un projet système d'information"
            ],
            6: [
                "Identifier ses aptitudes pour travailler dans une équipe",
                "Situer son rôle et ses missions au sein d'une équipe informatique",
                "Manager une équipe informatique"
            ]
        }
        # UE1.2 => (1=semestre, 2=competence)
        # ues[competence]
        # ues[x][0] = 1, 2 ; [1] = 3, 4 ; [2] = 5, 6
        ues = {}
        for number, names in str_ues.items():
            ues[number] = []
            for name in names:
                ue = UE(department=department, number=number, description=name)
                ue.save()
                ues[number].append(ue)

        semesters = []
        for i in range(6):
            semester = Semester(department=department, number=i+1)
            semester.save()
            semesters.append(semester)

        str_resources = {
            semesters[0]: {
                1: (
                    "Initiation au développement",
                    [ues[1][0], ues[2][0]]
                ),
                2: (
                    "Développement d'interfaces web",
                    [ues[1][0], ues[5][0], ues[6][0]]
                ),
                3: (
                    "Introduction à l'architecture des ordinateurs",
                    [ues[2][0], ues[3][0]]
                ),
                4: (
                    "Introduction aux systèmes d'exploitation et à leur fonctionnement",
                    [ues[3][0]]
                ),
                5: (
                    "Introduction aux bases de données et SQL",
                    [ues[4][0]]
                ),
                6: (
                    "Mathématiques discrètes",
                    [ues[2][0], ues[4][0]]
                ),
                7: (
                    "Outils mathématiques fondamentaux",
                    [ues[2][0]]
                ),
                8: (
                    "Introduction à la gestion des organisations",
                    [ues[5][0], ues[6][0]]
                ),
                9: (
                    "Introduction à l'économie durable et numérique",
                    [ues[4][0], ues[6][0]]
                ),
                10: (
                    "Anglais",
                    [ues[1][0], ues[3][0], ues[6][0]]
                ),
                11: (
                    "Base de la communication",
                    [ues[3][0], ues[5][0], ues[6][0]]
                ),
                12: (
                    "Projet professionnel et personnel",
                    [ues[6][0]]
                )
            },
            semesters[1]: {
                1: (
                    "Développement orienté objets",
                    [ues[1][0], ues[2][0]]
                ),
                2: (
                    "Développement d'applications avec IHM",
                    [ues[1][0], ues[5][0], ues[6][0]]
                ),
                3: (
                    "Qualité de développement",
                    [ues[1][0], ues[5][0]]
                ),
                4: (
                    "Communication et fonctionnement bas niveau",
                    [ues[2][0], ues[3][0]]
                ),
                5: (
                    "Introduction aux services réseaux",
                    [ues[3][0]]
                ),
                6: (
                    "Exploitation d'une base de données",
                    [ues[4][0]]
                ),
                7: (
                    "Graphes",
                    [ues[2][0], ues[5][0]]
                ),
                8: (
                    "Outils numériques pour les statistiques descriptives",
                    [ues[4][0]]
                ),
                9: (
                    "Méthodes numériques",
                    [ues[2][0]]
                ),
                10: (
                    "Introduction à la gestion des systèmes d'information",
                    [ues[4][0], ues[5][0]]
                ),
                11: (
                    "Introduction au droit",
                    [ues[6][0]]
                ),
                12: (
                    "Anglais",
                    [ues[3][0], ues[4][0], ues[5][0], ues[6][0]]
                ),
                13: (
                    "Communication technique",
                    [ues[1][0], ues[3][0], ues[5][0], ues[6][0]]
                ),
                14: (
                    "Projet professionnel et personnel",
                    [ues[6][0]]
                )
            }
        }
        # R1.2 => (1=semestre, 2=number)
        # str_resources = { semester: { number: ("name", [ues]), ... }, ... }
        for semester, r in str_resources.items():
            for resource, content in r.items():
                resource = Resource(number=resource, name=content[0], semester=semester)
                resource.save()
                for ue in content[1]:
                    resource.ues.add(ue)

class Department(models.Model):
    name = models.CharField(max_length=80)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, default=None, blank=False, null=True)

    def __str__(self):
        return self.name

    def getUEs(self):
        # Retourne les UEs appartenant au département
        return UE.objects.filter(department=self).order_by("number")

    def getSemesters(self):
        # Retourne les semestres appartenant au département
        return Semester.objects.filter(department=self).order_by("number")

    def getGroups(self):
        # Retourne les groupes appartenant au département
        return Group.objects.filter(department=self).order_by("name")

    def getStudents(self):
        # Retourne les étudiants appartenant au département
        return Student.objects.filter(department=self)

    def getProfessors(self):
        # Retourne les professeurs appartenant au département
        professors = []                         # Liste de retour
        for semester in self.getSemesters():    # Loop les semestres du département
            for resource in semester.getResources():    # Loop les ressources associés
                for professor in resource.professors.all(): # Loop les professeurs associés
                    if professor not in professors:             # Check pour l'insertion unique de prof
                        professors.append(professor)                # Insert le prof dans la liste
        return professors

    def getUsefulLinks(self):
        # Retourne les liens utiles appartenant au département
        return UsefulLink.objects.filter(department=self).order_by("name")

class UsefulLink(models.Model):
    name = models.CharField(max_length=30)
    file_path = models.CharField(max_length=50)
    link = models.CharField(max_length=70)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None, blank=False, null=True)

    def __str__(self):
        return self.name

# class BUT(models.Model):
#     type = models.CharField(max_length=50)
#     departments = models.ManyToManyField(Department)

#     def __str__(self):
#         return self.type

# class Course(models.Model):
#     BUTs = models.ManyToManyField(BUT)
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

class UE(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None, blank=False, null=True)
    number = models.IntegerField(default=None, blank=False, null=True)
    description = models.CharField(max_length=500, default="")

    def __str__(self):
        return "UE" + str(self.number) + " - " + self.description

    def getResources(self):
        # Retourne les ressources appartenant à l'UE
        return Resource.objects.filter(ues=self).order_by("number")

    def getNote(self, student):
        # Retourne la note de l'UE d'un étudiant donné
        nb, sum = 0, 0                                  # Nombre de note, Somme des notes
        for resource in self.getResources():            # Loop les ressources de l'UE
            for evaluation in resource.getEvaluations():    # Loop les évaluations associés
                note = evaluation.getNote(student)              # Prend la note de l'étudiant de l'évaluation
                if note != None:                                # Si la note existe
                    sum += note                                     # Ajoute la note à la somme
                    nb += 1                                         # Incrémente le nombre de note
        return round(sum / nb, 2) if nb > 0 else None   # Si le nombre de note > 0, retourne une moyenne, sinon None

    def getRanking(self, student):
    	# Retourne le classement de l'UE d'un étudiant donné
        notes = {}										# notes = { student: note, ... }
        students = student.department.getStudents()		# Prend tout les étudiants du départment de l'étudiant
        for s in students:								# Loop les étudiants
            note = self.getNote(s)							# Prend la note de l'UE associé
            if note != None:								# Si la note existe
                notes[s] = note									# Rempli le dictionnaire notes
        if len(notes) > 0:								# S'il y a des notes
															# Tri le dictionnaire en fonction des notes
            notes = dict(sorted(notes.items(), key=lambda notes:notes[1], reverse=True))
            index = list(notes.keys()).index(student)		# Prend la place de l'étudiant
            return str(index + 1) + "/" + str(len(notes))	# Retourne le classement (i.e. "1/4")
        return None										# Sinon renvoie None

class Semester(models.Model):
    number = models.IntegerField(default=None, blank=False, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None, blank=False, null=True)

    def __str__(self):
        return "S" + str(self.number)

    def getResources(self):
        # Retourne les ressources appartenant au semestre
        return Resource.objects.filter(semester=self).order_by("number")

    def getProfessorResources(self, professor):
        # Retourne les ressources d'un professeur donné
        resources = Resource.objects.filter(semester=self).order_by("number")
        return list(set(resources & professor.resources.all()))

    def getUEs(self):
        # Retourne les UEs appartenant au semestre
        ues = []								# Liste de retour
        for resource in self.getResources():	# Loop les ressources du semestre
            for ue in resource.ues.all():			# Loop les UEs associés
                if ue not in ues:						# Check pour l'insertion unique d'UE
                    ues.append(ue)							# Insert l'UE dans la liste
        return ues

class Resource(models.Model):
    number = models.IntegerField(default=None, blank=False, null=True)
    name = models.CharField(max_length=50)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=None, blank=False, null=True)
    ues = models.ManyToManyField(UE, related_name="resources")

    def __str__(self):
        return f"R{self.semester.number}.{self.number} {self.name}"

    def getEvaluations(self):
        # Retourne les évaluations appartenant à la ressource
        return Evaluation.objects.filter(resource=self)

    def getNote(self, student):
        # Retourne la note de la ressource d'un étudiant donné
        nb, sum = 0, 0
        for evaluation in self.getEvaluations():
            note = evaluation.getNote(student)
            if note != None:
                sum += note
                nb += 1
        return sum / nb if nb > 0 else None

    def getRanking(self, student):
        # Retourne le classement de la ressource d'un étudiant donné
        notes = {}
        for s in student.department.getStudents():
            note = self.getNote(s)
            if note != None:
                notes[s] = note
        if len(notes) > 0:
            notes = dict(sorted(notes.items(), key=lambda notes:notes[1], reverse=True))
            index = list(notes.keys()).index(student)
            return str(index + 1) + "/" + str(len(notes))
        return None

# class Year(models.Model):
#     name = models.CharField(max_length=70)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None, blank=True, null=True)
#     first_semester = models.ForeignKey(Semester, related_name="first_semester", on_delete=models.CASCADE, default=None, blank=False, null=True)
#     second_semester = models.ForeignKey(Semester, related_name="second_semester", on_delete=models.CASCADE, default=None, blank=False, null=True)

#     def __str__(self):
#         return self.name

class Group(models.Model):
    name = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None, blank=False, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, blank=True, null=True, related_name="children")

    def __str__(self):
        return self.name

    def getDepartmentTree(department):
        tree = {}
        for child in Group.objects.filter(parent=None, department=department):
            tree[child] = child.getTree()
        return tree

    def getTree(self):
        if len(self.children.all()) == 0:
            return {}
        group = {self: {}}
        for child in self.children.order_by("name"):
            group[self].update(child.getTree())
        return group

class Student(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None, blank=False, null=True)
    groups = models.ManyToManyField(Group, blank=False, related_name="students")

    def __str__(self):
        return self.id.username

    def getGrades(self):
        # Retourne les notes d'un étudiant donné
        return Grade.objects.filter(student=self)

    def getLastGrades(self, amount):
        # Retourne les {amount} dernières notes d'un étudiant donné
        return self.getGrades()[:amount]

class Professor(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    resources = models.ManyToManyField(Resource, blank=True, related_name="professors")

    def __str__(self):
        return f"{self.id.first_name} {self.id.last_name}"

    def getResources(self, department):
        resources = []
        for resource in self.resources.all():
            if resource.semester.department == department:
                resources.append(resource)
        return resources

    def getDepartments(self):
        departments = []
        for resource in self.resources.all():
            if resource.semester.department not in departments:
                departments.append(resource.semester.department)
        return departments

    def getEtablishments(self):
        establishments = []
        for department in self.getDepartments():
            if department.establishment not in establishments:
                establishments.append(department.establishment)
        return establishments

class Administrator(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.id.username

class Competence(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Evaluation(models.Model):
    name = models.CharField(max_length=50)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, default=None, blank=False, null=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, default=None, blank=False, null=True)

    def __str__(self):
        return self.name

    def getGrades(self):
        return Grade.objects.filter(evaluation=self)

    def getGrade(self, student):
        return Grade.objects.filter(evaluation=self, student=student)

    def getNote(self, student):
        grades = self.getGrade(student)
        return grades.first().note if len(grades) == 1 else None

    def getAverage(self):
        grades = self.getGrades()	# Prend les notes de l'évaluation
        if len(grades) <= 0:		# S'il n'y a pas de note
            return None					# Retourne None
        nb, sum = len(grades), 0	# Nombre de note, Somme des notes
        for grade in grades:		# Loop les notes
            sum += grade.note			# Ajoute la note à la somme
        return round(sum / nb, 2)	# Retourne une moyenne

    def getMax(self):
        grades = self.getGrades()	# Prend les notes de l'évaluation
        if len(grades) <= 0:		# S'il n'y a pas de note
            return None					# Retourne None
        max = -math.inf				# Note maximale stockée (- infini)
        for grade in grades:		# Loop les notes
            if max < grade.note:		# Si la note stockée est plus petite que la note associée
                max = grade.note			# Affecte la note associée à la note stockée
        return max					# Retourne la note stockée

    def getMin(self):
        grades = self.getGrades()	# Prend les notes de l'évaluation
        if len(grades) <= 0:		# S'il n'y a pas de note
            return None					# Retourne None
        min = math.inf				# Note minimale stockée (+ infini)
        for grade in grades:		# Loop les notes
            if min > grade.note:		# Si la note stockée est plus grande que la note associée
                min = grade.note			# Affecte la note associée à la note stockée
        return min					# Retourne la note stockée

    def getRanking(self, student):
        notes = {}
        for s in student.department.getStudents():
            note = self.getNote(s)
            if note != None:
                notes[s] = note
        if len(notes) > 0:
            notes = dict(sorted(notes.items(), key=lambda notes:notes[1], reverse=True))
            index = list(notes.keys()).index(student)
            return str(index + 1) + "/" + str(len(notes))
        return None

class Grade(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, default=None, blank=False, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None, blank=False, null=True)
    note = models.FloatField(default=0.0, blank=False, null=False)
    coef = models.FloatField(default=1.0, blank=True, null=False)

    def __str__(self):
        return self.evaluation.name

    def calcNote(self):
        return self.note * self.coef

def load():
    empty()

    establishment = Establishment(name="IUT Claude Bernard Lyon 1 - Bourg en bresse")
    establishment.save()

    department = Department(name="Informatique", establishment=establishment)
    department.save()

    moodle = UsefulLink(name="Moodle", file_path="img/moodle.png", link="https://moodle.univ-lyon1.fr/", department=department)
    moodle.save()
    mail = UsefulLink(name="Mail", file_path="img/mail.png", link="https://mail.univ-lyon1.fr/", department=department)
    mail.save()

    ue1_1 = UE(department=department, number=1, description="Développer des applications informatiques simples")
    ue1_1.save()
    ue1_2 = UE(department=department, number=1, description="Partir des exigences et aller jusqu'à une application complète")
    ue1_2.save()
    ue1_3 = UE(department=department, number=1, description="Adapter des applications sur un ensemble de supports (embarqué, web, mobile, IoT…)")
    ue1_3.save()

    ue2_1 = UE(department=department, number=2, description="Appréhender et construire des algorithmes")
    ue2_1.save()
    ue2_2 = UE(department=department, number=2, description="Sélectionner les algorithmes adéquats pour répondre à un problème donné")
    ue2_2.save()
    ue2_3 = UE(department=department, number=2, description="Analyser et optimiser des applications")
    ue2_3.save()

    ue3_1 = UE(department=department, number=3, description="Installer et configurer un poste de travail")
    ue3_1.save()
    ue3_2 = UE(department=department, number=3, description="Déployer des services dans une architecture réseau")
    ue3_2.save()
    ue3_3 = UE(department=department, number=3, description="Faire évoluer et maintenir un système informatique communicant en conditions opérationnelles")
    ue3_3.save()

    ue4_1 = UE(department=department, number=4, description="Concevoir et mettre en place une base de données à partir d'un cahier des charges client")
    ue4_1.save()
    ue4_2 = UE(department=department, number=4, description="Optimiser une base de données, interagir avec une application et mettre en œuvre la sécurité")
    ue4_2.save()
    ue4_3 = UE(department=department, number=4, description="Administrer une base de données, concevoir et réaliser des systèmes d'informations décisionnels")
    ue4_3.save()

    ue5_1 = UE(department=department, number=5, description="Identifier les besoins métiers des clients et des utilisateurs")
    ue5_1.save()
    ue5_2 = UE(department=department, number=5, description="Appliquer une démarche de suivi de projet en fonction des besoins métiers des clients et des utilisateurs")
    ue5_2.save()
    ue5_3 = UE(department=department, number=5, description="Participer à la conception et à la mise en oeuvre d'un projet système d'information")
    ue5_3.save()

    ue6_1 = UE(department=department, number=6, description="Identifier ses aptitudes pour travailler dans une équipe")
    ue6_1.save()
    ue6_2 = UE(department=department, number=6, description="Situer son rôle et ses missions au sein d'une équipe informatique")
    ue6_2.save()
    ue6_3 = UE(department=department, number=6, description="Manager une équipe informatique")
    ue6_3.save()

    semester1 = Semester(number=1, department=department)
    semester1.save()
    semester2 = Semester(number=2, department=department)
    semester2.save()

    semester3 = Semester(number=3, department=department)
    semester3.save()
    semester4 = Semester(number=4, department=department)
    semester4.save()

    semester5 = Semester(number=5, department=department)
    semester5.save()
    semester6 = Semester(number=6, department=department)
    semester6.save()

    resource1 = Resource(number="1", name="Initiation au dev.", semester=semester1)
    resource1.save()
    resource1.ues.add(ue1_1, ue3_1)

    resource2 = Resource(number="2", name="Développement d'interfaces web", semester=semester1)
    resource2.save()
    resource2.ues.add(ue1_1, ue5_1, ue6_1)

    groupS1 = Group(name="S1", department=department, parent=None)
    groupS1.save()
    groupS1G1 = Group(name="S1G1", department=department, parent=groupS1)
    groupS1G1.save()
    groupS1G1_1 = Group(name="S1G1.1", department=department, parent=groupS1G1)
    groupS1G1_1.save()
    groupS1G1_2 = Group(name="S1G1.2", department=department, parent=groupS1G1)
    groupS1G1_2.save()

    groupS2 = Group(name="S2", department=department, parent=None)
    groupS2.save()
    groupS2G1 = Group(name="S2G1", department=department, parent=groupS2)
    groupS2G1.save()
    groupS2G1_1 = Group(name="S2G1.1", department=department, parent=groupS2G1)
    groupS2G1_1.save()
    groupS2G1_2 = Group(name="S2G1.2", department=department, parent=groupS2G1)
    groupS2G1_2.save()

    noa = Student(id=User.objects.all().filter(username="noa_cavalcante").first(), department=department)
    noa.save()
    noa.groups.add(groupS1, groupS1G1, groupS1G1_1)

    lilian = Student(id=User.objects.all().filter(username="lilian_ouraha").first(), department=department)
    lilian.save()
    lilian.groups.add(groupS1, groupS1G1, groupS1G1_1)

    corto = Student(id=User.objects.all().filter(username="corto_bouviolle").first(), department=department)
    corto.save()
    corto.groups.add(groupS1, groupS1G1, groupS1G1_2)

    peytavie = Professor(id=User.objects.all().filter(username="adrien_peytavie").first())
    peytavie.save()
    peytavie.resources.add(resource1, resource2)

    administrator = Administrator(id=User.objects.all().filter(username="administrateur").first())
    administrator.save()

    evaluation = Evaluation(name="TP 1", professor=peytavie, resource=resource1)
    evaluation.save()

    grade = Grade(evaluation=evaluation, student=noa, note=20.0)
    grade.save()
    grade = Grade(evaluation=evaluation, student=corto, note=4.0)
    grade.save()
    grade = Grade(evaluation=evaluation, student=lilian, note=1.5)
    grade.save()

    evaluation = Evaluation(name="TP 2", professor=peytavie, resource=resource1)
    evaluation.save()

    grade = Grade(evaluation=evaluation, student=noa, note=16.0)
    grade.save()
    grade = Grade(evaluation=evaluation, student=corto, note=10.0)
    grade.save()
    grade = Grade(evaluation=evaluation, student=lilian, note=11.5)
    grade.save()

def empty():
    Professor.objects.all().delete()
    Student.objects.all().delete()
    Group.objects.all().delete()
    # Year.objects.all().delete()
    Semester.objects.all().delete()
    UE.objects.all().delete()
    Department.objects.all().delete()
    Establishment.objects.all().delete()