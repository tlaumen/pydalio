# PYDALIO

This package is inspired by the book of Ray Dalio, Principles.
The idea is to pose a number of principle questions to make more informed, rational decisions. These can be saved and the endgoal is to be able to abstract a personal working algorithm from it.

How to get started using the package:
0. Create a virtual environment: https://realpython.com/python-virtual-environments-a-primer/#create-it
1. pip install pydalio
2. Define your principles:
    a. create a .yaml file
    b. define principle questions as shown in example_principles.yaml
    c. define possible options as shown in example_principles.yaml
    d. Set yaml path to .env file as shown in example_config.env
3. Set database path in .env file as shown in example_config.env. Please note the name of the db (sqlite) is currently fixed at dalio.db
4. Optional: if sqlite is not installed, please install it. For more information: https://www.gurusoftware.com/the-complete-guide-to-downloading-installing-sqlite/
5. Setup environment by running the following python script:
    from pydalio.db import create_db
    from pydalio.db import initiliaze_tables

    create_db()
    initiliaze_tables()
6. Activate your virtual environment: https://realpython.com/python-virtual-environments-a-primer/#activate-it
7. Run the command "pydalio --help" to see all commands you can run.
8. Enjoy your journey of improved decision making!

Development track:
    [x] create cli application basis
    [ ] create orchestrating logic to run continuously
    [x] create sqllite db interface
    [x] create generalised principle questions interface
    [ ] create simple algorithm interface based on database.First guesstimate is decision tree algorithm or logistic regression.
    [ ] make a bash script to install/run globally?

If you would like to contribute, fork the package: https://github.com/tlaumen/pydalio and make a PR.
For further questions, e-mail to tom_laumen@hotmail.com
