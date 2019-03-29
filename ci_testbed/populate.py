
import bs4
import gitlab
import os
import re
import requests
import sys
import time

URL = 'http://gitlab'
LOGINURL = URL + '/users/sign_in'

def main():
    gl = getLoggedInGitlabSession()
    
    settings = gl.settings.get()
    settings.auto_devops_enabled = False
    settings.save()
    
    #upload the template projects etc
    bsGroup = createGroup(gl, "BuildSystem")
    createProject(gl, bsGroup, "ci-templates")
    createProject(gl, bsGroup, "conan-config_release")
    createProject(gl, bsGroup, "conan-config_prerelease")
    
    #upload the components
    compGroup = createGroup(gl, "demo")
    createProject(gl, compGroup, "hellolib")
    createProject(gl, compGroup, "foobarlib")
    createProject(gl, compGroup, "leetlib")
    createProject(gl, compGroup, "concatlib")
    
    #upload the metas
    metaGroup = createGroup(gl, "MetaBuilds")
    createProject(gl, metaGroup, "demo-meta")
    
    #upload the app
    appGroup = createGroup(gl, "Applications")
    createProject(gl, appGroup, "generateApp")
    
    #upload the projects
    projGroup = createGroup(gl, "projects")
    createProject(gl, projGroup, "SampleProject")
    
    print('...done')

def createGroup(gl, name):
    return gl.groups.create({'name': name, 'path': name})

def createProject(gl, group, name):
    project = gl.projects.create({'name': name, 'namespace_id': group.id})
    data = {
        'branch': 'master',
        'commit_message': 'Automatic commit...',
        'actions': []
    }
    
    #add the files from the template to our data dict
    projDir = os.path.join('project_template', name)
    for root, subdirs, files in os.walk(projDir):
        for file in files:
            filePath = os.path.join(root, file).replace(projDir, '')[1:].replace('\\', '/')
            data['actions'].append({
                'action': 'create',
                'file_path': filePath,
                'content': open(os.path.join(projDir, filePath)).read()
            })
    
    commit = project.commits.create(data)
    return project

def getLoggedInGitlabSession():
    session = requests.Session()
    sign_in_page = session.get(LOGINURL).content.decode('utf-8')
    for l in sign_in_page.split('\n'):
        m = re.search('name="authenticity_token" value="([^"]+)"', l)
        if m:
            break
    token = m.group(1)

    data = {'user[login]': 'root',
            'user[password]': 'qwer1234',
            'authenticity_token': token}
    r = session.post(LOGINURL, data=data)
    
    page_tokens = session.get('/'.join((URL, 'profile/personal_access_tokens')))
    private_token = None
    if page_tokens.ok:
        root = bs4.BeautifulSoup(page_tokens.text, "html5lib")
        token = root.find_all("form", id='new_personal_access_token')[0].find_all('input', attrs={'name': 'authenticity_token'})[0]['value']

        body = {
        "personal_access_token[name]": 'mytoken',
        "personal_access_token[scopes][]": 'api',
        'authenticity_token': token
        }

        response = session.post('/'.join((URL, 'profile/personal_access_tokens')), data=body)

        if response.ok:
            private_token_page = bs4.BeautifulSoup(response.text, "html5lib")
            private_token = private_token_page.find_all('input', id='created-personal-access-token')[0]['value']

    session.headers.update({'Private-Token': private_token})
    print('Private Token: ' + private_token)

    return gitlab.Gitlab(URL, api_version=4, session=session)
    

if __name__ == "__main__":
    main()