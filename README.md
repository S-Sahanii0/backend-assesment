# Flights back-end recruitment test

[Task](docs/task.md)

## Getting Started
- Requirements

- Tests

- Coverage 
    `coverage run manage.py test`
    `coverage html`
    `open htmlcov/index.html`


## Architecture 
- Diagrams
    `pip install graphviz pyparsing`
    `python manage.py graph_models -a -o ../images/entity_diagram.png`

## Workflow
- Tasks

## Improvements
- ID ambiguity
- secrets
- add ci
- indexes
- logger
- prod vs dev

## Assumptions
1. The given url is the source of data and the schema that it's sending will be maintained.
2. Authentication is not required for the API.
3. All airlines will have a different agent entity.


