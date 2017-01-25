from robobrowser import RoboBrowser
import git, os, shutil
import getpass
browser = RoboBrowser(history=True)
browser.open('https://www.overleaf.com/users/sign_in')
form = browser.get_form(action='/users/sign_in')
form['user[email]'].value = raw_input('Enter email: ')
form['user[password]'].value = getpass.getpass('Password: ')
browser.submit_form(form)

def clone_repo(doc_json, filter_by=None):
    """ Clone all repos

    docs_json: dict
        Dictionary as returned by overleaf for active documents

    filter_by: dict
        Dictionary for filtering repos on some key:value criteria

    See example below.
    """
    doc_id  = doc_json['id']
    doc_title = doc_json['title']
    dir_name =  doc_title.replace(' ', '_') + '__' + doc_id
    if filter_by:
        for key, value in filter_by.iteritems():
            if key in doc_json and doc_json[key] == value:
                pass
            else:
                print 'Skipping {}'.format(doc_title)
                return
    remote_url = 'https://git.overleaf.com/{}'.format(doc_id)
    if doc_json['protected']:
        print 'Skipping private repo: {}'.format(remote_url)
    print 'Cloning: {}'.format(remote_url)
    if os.path.isdir(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)
    repo = git.Repo.init(dir_name)
    origin = repo.create_remote('origin',remote_url)
    origin.fetch()
    origin.pull(origin.refs[0].remote_head)



browser.open('https://www.overleaf.com/api/v0/current_user/docs/')
all_docs_json = browser.response.json()['docs']

tag = raw_input('Enter tag: ')
root_location = raw_input('Enter root location:')

for doc_json in all_docs_json:
    os.chdir(root_location)
    clone_repo(doc_json, filter_by= {'tags': [tag]})
