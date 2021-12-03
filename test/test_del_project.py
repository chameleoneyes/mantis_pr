import random


def test_delete_project(app):
    old_project_list = app.soap.list_of_projects()
    if len(old_project_list) == 0:
        project = app.project.generate_project_data()
        app.project.create_project(project)
    project = random.choice(old_project_list)
    app.project.delete_project(project)
    new_project_list = app.soap.list_of_projects()
    assert len(old_project_list) - 1 == len(new_project_list)
    old_project_list.remove(project)
    assert sorted(old_project_list, key=lambda x: x.name) == sorted(new_project_list, key=lambda x: x.name)
    app.session.logout()
