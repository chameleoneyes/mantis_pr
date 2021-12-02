import time


def test_add_project(app):
    old_project_list = app.project.get_project_from_hp()
    project = app.project.generate_project_data()
    app.project.create_project(project)
    time.sleep(5)
#    assert len(old_project_list) + 1 == len(new_project_list)
    app.project.improve_project_object(project)
    old_project_list.append(project)
    new_project_list = app.project.get_project_from_hp()
    assert sorted(old_project_list, key=lambda x: x.name) == sorted(new_project_list, key=lambda x: x.name)
    app.session.logout()

