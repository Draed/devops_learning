## temp idea

- adding database and SQLAlchemy as ORM
- secure it using OAuth 2.0
- add keycloak for authentication
- adding a csv export feature
- separate application into multiple microservice

- Opentelemetry integration
- adding CORS middleware

- add a script to remove all comment in code
- add a script to condense code (remove all uneeded carriage return) and compare code size optimization

- dockerize application :
    - add dockerignore file
    - add dockerfile
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