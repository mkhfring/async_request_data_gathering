# Async request data gathering

There are times it is needed to define some tasks in a run forever async loop
and the cumulative result of all these tasks is needed. We had such a problem
to implement bale bots here in SADAD. In these situations the loop.run_until_complete()
is not practical because the loop can not be stopped. 
Here I suggest a way to accomplish   such task by gathering the data in a bound method of an object.
Take a look at test_async_request to understand the problem. Of course here the
loop is stoped in the sake of the test. However, in real-world situations the
loop can not be stoped. To implement the situation here, a flask HTTP mockup
server is used and finally the result of all the requests to this server is written to an
excel file. 
## Getting Started

# Enviroment setup
First install requirments and create a virtual environment for the project
using codes below:
```
sudo apt-get install python3-pip python3-dev
sudo pip3.6 install virtualenvwrapper
echo "export VIRTUALENVWRAPPER_PYTHON=`which python3.6`" >> ~/.bashrc
echo "alias v.activate=\"source $(which virtualenvwrapper.sh)\"" >> ~/.bashrc
source ~/.bashrc
v.activate
mkvirtualenv --python=$(which python3.6) --no-site-packages async_request
```

Clone the project with the following link:
```
git clone git@github.com:mkhfring/async_request_data_gathering.git

```
Then in the virtual env created in the previous step run commands below:

```
pip install -e .
pip install -r requirements.txt
```

### Prerequisites

requirements for the project are listed in requirements.txt

