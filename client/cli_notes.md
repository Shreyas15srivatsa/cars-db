# TODO:
- Validation of input parameters. [done]
    - Add datatypes to the parameters
- DBAction enum is not being used. Do we need to keep it? [not true anymore]
- Will need to convert dates to a comparable format. Str won't work I think
- Need a way to generate SQL based on the selected functionality. So far I can only do it based on CRUD [figured out how to add new functions. Just add new DBActions]
- Clear out the TODO and the TODO_NEW tags
- Tell user to use SPACE to clear out desc
- Add a confirm dialogue to add listings.

# How to:
- Add new client functionality:
    - Update global functionality dict.
    - If operation not covered by simple CRUD, add a new type of action to DBActions class.
        - Define behaviour for that DBAction, in a function inside connection.py
        - Call the new function from cli layer.
    - check for TODO_NEW
- Add new entity: create a new class same as the table name in MySQL