# devops learning

## Description 

A simple devops project base on TODO list application in order to learn and improve skills about devops.
The main idea is to create a simple application (TODO list) and deploy it using devops best practice and increase scalability.

| stage name | Stage description | difficulty | 
| ---------  | ----------------- | ---------- |
| [1.api](./1.api/1.api.md) | Create simple rest api | easy |
| [2.test_case](./2.test_case/2.test_case.md) | Adding test case framework (pytest) to run test | easy |
| [3.ci](./3.ci/3.ci.md) | Adding ci to automate testing, linting, packaging, ... | easy |
| [4.python_docstring](./4.python_docstring/4.python_docstring.md) | Adding docstring documentation and html pdoc page... | easy |


## temp idea

- env variable configuration
- logging
- fastapi/flask file hierarchy best practice

- secure it using JSON TOKEN
- secure it using OAuth 2.0
- adding a csv export feature
- separate application into multiple microservice


- optimize python code following best practices (docstrings)
- add a script to remove all comment in code
- add a script to condense code (remove all uneeded carriage return) and compare code size optimization
- dockerize application :
    - Add health‑check endpoint
    - clear python code script (remove comment, optimize code size)
- deploy application using docker-compose
- deploy application using kubernetes

- dependencies :
    - https://pip.pypa.io/en/stable/topics/secure-installs/
    - using poetry instead of requirements.txt to manage dependencies and project configuration (pyproject.toml)

- ci :
    - Enforce with pydocstyle, flake8-docstrings, or ruff in CI.
    - Static analysis (ruff, mypy, pytest) in CI
    - keep pip cache (~/.cache/pip) to speed up install
    - add code/package/image versioning