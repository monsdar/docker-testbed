
import bs4
import gitlab
import re
import requests
import time

stagePrefix = "stage"
projectPrefix = "project"
numStages = 1
numProjectsPerStage = 1

URL = 'http://gitlab'
LOGINURL = URL + '/users/sign_in'

def main():
    gl = getLoggedInGitlabSession()
    
    settings = gl.settings.get()
    settings.auto_devops_enabled = False
    settings.save()
    
    #####################
    #Create a number of groups, one for each stage
    stages = {}
    for index in range(numStages):
        name = stagePrefix + str(index)
        try:
            newGroup = gl.groups.create({'name': name, 'path': name})
            stages[newGroup] = []
            
            for index in range(numProjectsPerStage):
                name = projectPrefix + '_' + newGroup.path + '_' + str(index)
                try:
                    newProject = gl.projects.create({'name': name, 'namespace_id': newGroup.id})
                    stages[newGroup].append(newProject)
                except Exception as ex:
                    print(ex)
        except Exception as ex:
            print(ex)
    print('Created ' + str(len(stages)) + ' stages with a total of ' + str(len(stages.values())) + ' projects...')
    
    #####################
    #Push our files into the projects
    print('Pushing files...')
    for stage in stages:
        print("Pushing files for projects in " + str(stage.name))
        for project in stages[stage]:
            data = {
            'branch': 'master',
            'commit_message': 'Initial commit...',
            'actions': [
                {
                    'action': 'create',
                    'file_path': 'Readme.md',
                    'content': openFileAndApplyReplacements('project_template/hellolib/Readme.md', project)
                },
                {
                    'action': 'create',
                    'file_path': 'CMakeLists.txt',
                    'content': openFileAndApplyReplacements('project_template/hellolib/CMakeLists.txt', project)
                },
                {
                    'action': 'create',
                    'file_path': 'conanfile.py',
                    'content': openFileAndApplyReplacements('project_template/hellolib/conanfile.py', project)
                },
                {
                    'action': 'create',
                    'file_path': 'hello.cpp',
                    'content': openFileAndApplyReplacements('project_template/hellolib/hello.cpp', project)
                },
                {
                    'action': 'create',
                    'file_path': 'hellolib_' + project.name + '/hello.h',
                    'content': openFileAndApplyReplacements('project_template/hellolib/hello.h', project)
                },
                {
                    'action': 'create',
                    'file_path': '.gitlab-ci.yml',
                    'content': openFileAndApplyReplacements('project_template/hellolib/.gitlab-ci.yml', project)
                }
            ]}
            commit = project.commits.create(data)
            time.sleep(0.5) #sleep a bit to not run into rate limits for the Gitlab API
    print('...done')

def openFileAndApplyReplacements(file, project):
    content = open(file).read()
    newContent = content.replace('%%NAME%%', project.name)
    return newContent

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