from app.models.project import Project
from app.models.activity import Activity
from app.algorithms.pert import PertAlgorithm

project = Project(name="Proyecto Actual")


def get_project():
    PertAlgorithm.calculate(project)
    return project


def add_activity(activity: Activity):
    project.activities.append(activity)
    PertAlgorithm.calculate(project)


def remove_activity(activity_name: str):
    project.activities = [
        activity
        for activity in project.activities
        if activity.name != activity_name
    ]
    PertAlgorithm.calculate(project)