pip install virtualenv
virtualenv virtual_env
source virtual_env/bin/activate
pip install git+ssh://git@github.com/rileymat/web_plugins.git
sudo apt-get install libffi-dev
pip install bcrypt
pip install pystache
setup_app.py --no-generate-basic-site --no-create-git-repo --app-name=familybank

