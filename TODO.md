# Templates

- [ ] Move JSON templates to ICA instead or to templates/ directory

# TODO @cmihai

- [ ] Add a make development target, to start uvicorn under app/development_routes

- [ ] Rename to integration_host
- [ ] Multistage build - finish
- [ ] Maybe use a PAT instead of ssh key
- [ ] Migrate to gunicorn
- [ ] Add a cli to start the server
- [ ] Add tests
- [ ] pydantic.errors.PydanticUserError: If you use `@root_validator` with pre=False (the default) you MUST specify `skip_on_failure=True`. Note that `@root_validator` is deprecated and should be replaced with `@model_validator`.
comes from from langchain.prompts import PromptTemplate in google route
- [ ] pydantic<2 migration

  File "/home/cmihai/.venv/langserve_server/lib/python3.11/site-packages/libica/libica.py", line 304, in get_model_id_by_name
    if model_name and model_name.isdigit():
                      ^^^^^^^^^^^^^^^^^^
AttributeError: 'int' object has no attribute 'isdigit'
