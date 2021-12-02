import time


def test_untitled_test_case(app):
    app.session.login("administrator", "root")
    assert app.session.is_logged_in_as("administrator")
    old_project_list = app.project.get_project_from_hp()
    project = app.project.generate_project_data()
    app.project.create_project(project)
    time.sleep(5)
#    assert len(old_project_list) + 1 == len(new_project_list)
    if project.status == '10':
        project.status = 'development'
    elif project.status == '30':
        project.status = 'release'
    elif project.status == '50':
        project.status = 'stable'
    elif project.status == '70':
        project.status = 'obsolete'
    else:
        pass
    if project.view_state == '10':
        project.view_state = 'public'
    elif project.view_state == '50':
        project.view_state = 'private'
    else:
        pass
    old_project_list.append(project)
    new_project_list = app.project.get_project_from_hp()
    assert sorted(old_project_list, key=lambda x: x.name) == sorted(new_project_list, key=lambda x: x.name)
    app.session.logout()

