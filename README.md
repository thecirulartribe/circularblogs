# Circularblog

## Steps to run web app on local

### Step 1: Install a Pycharm community edition


### Step 2: Open a new folder/project


### Step 3: Open terminal in Pycharm


### Step 4: Type the following in the terminal

#### Clone the repository
```
git clone https://github.com/thecirculartribe/circularblog.git
```

#### Enter the root directory
```
cd .\circularblog\
```

#### Check if you are on the root
```
git pull origin main
git status
```

#### If you are on the main branch then create a new branch
>Add any custom branch name place of `<branch-name>`
```
git checkout -b <branch-name>
git status
```
#### Install all dependencies
```
pip install -r requirements.txt
```

#### Start django application
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
### You web app should be running on the local host
