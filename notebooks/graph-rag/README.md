# Graph-RAG with LangChain and Neo4j


## Docker container

```bash
docker run \
    -p 7474:7474 -p 7687:7687 \
    -v $PWD/data:/data -v $PWD/plugins:/plugins \
    --name neo4j-apoc \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4JLABS_PLUGINS=\[\"apoc\"\] \
    -e NEO4J_dbms_security_procedures_unrestricted=apoc.\\\* \
    --rm neo4j
```

#### References

- [Original Post](https://github.com/sunnysavita10/Generative-AI-Indepth-Basic-to-Advance/blob/main/RAG%20with%20Knowledge%20Graph%20Neo4j/RAG_With_Knowledge_graph(Neo4j).ipynb)
