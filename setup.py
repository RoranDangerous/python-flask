from setuptools import setup, find_packages

requires = [
    'psycopg2==2.8.5',
    'SQLAlchemy==1.3.16',
    'Flask==1.1.2',
    'Flask-SQLAlchemy==2.4.1',
    'Flask-Migrate==2.5.3',
    'Flask-Bcrypt==0.7.1',
    'Flask-Cors==3.0.8',
    'Flask-Script==2.0.6',
    'Flask-Security==3.0.0',
    'Flask-RESTful==0.3.8',
    'Flask-JWT-Extended==3.24.1',
    'PyJWT==1.7.1',
    'coverage==5.0.4',
    'kubernetes==11.0.0',
    'pusher==3.0.0',
    'email-validator==1.1.1'
]

setup(
    name='MintZone',
    version='0.0',
    description='TBD',
    author='Roman Iefimov',
    author_email='romaniefofficial@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)