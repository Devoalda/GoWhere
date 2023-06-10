# GoWhere
This is a simple python flask application to help you decide where to go leisure.

The dataset used is from [Wikipedia](https://en.wikipedia.org/wiki/List_of_shopping_malls_in_Singapore).
A sample dataset is provided in `SG_Shopping_Malls.py` module.

## Installation
1. Clone the repository
2. Install the requirements
3. Run the application
4. Enjoy!

```bash
# Clone and cd into the repository
# Install the requirements
pip install -r requirements.txt
# Run the application
python app.py
```

# Usage

## Flask Web Application
Open the browser and go to http://localhost:5000.
Main page will provide a random region and a few shopping malls in that region for you to pick.

To choose a specific region, go to http://localhost:5000/region where region can be:
- Central
- East
- North
- North East
- North West
- West
- South

Example: http://localhost:5000/Central

## SG_Shopping_Malls Module
This is the module that provides the random region and shopping malls. 
It can be used as a standalone module or as a command line tool.

```bash
usage: SG_Shopping_Malls.py [-h] [-a] [-p] [-H] [-r RANDOM] [-t]

Get a random mall in Singapore, this uses data from Wikipedia

options:
  -h, --help            show this help message and exit
  -a, --all             Show all the malls in Singapore
  -p, --pretty          Pretty print the dataset: SG_Shopping_Malls -p -a
  -H, --human           Human readable printing: SG_Shopping_Malls -H -r 3
  -r RANDOM, --random RANDOM
                        RANDOM = Number of malls to get: SG_Shopping_Malls -r 3
  -t, --test            Test the Shopping_Mall class

```

# Docker Image
A docker image is provided in the repository.
To run the docker image, run the following command:
```bash
docker image build -t go_where .
docker run -d -p 5000:5000 --name go_where go_where:latest
```

# License
[MIT](https://choosealicense.com/licenses/mit/)