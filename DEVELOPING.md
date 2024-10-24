# Build flags

```bash
build-container-kaniko-flags=--build-arg "APP_LIST=duckduckgo googlesearch docbuilder wikipedia health"
--build-arg "APP_LIST=duckduckgo googlesearch docbuilder health wikipedia instructlab_yaml_builder datagenerator test test_llm mermaid time jokes summarizer webex_summarizer"
--build-arg "APP_LIST=all"
```

TODO: make the route loader to also respect APP_LIST


## Converting Pydantic v1 to v2

bump-pydantic - see https://docs.pydantic.dev/latest/migration/#install-pydantic-v2
