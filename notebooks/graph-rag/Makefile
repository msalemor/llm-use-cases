default:
	@echo "Please specify a target to build"

clean:
	sudo rm -rf ./neo4j

docker-run:
	docker run --rm \
    -p 7474:7474 -p 7687:7687 \
    -v .neo4j/data:/data -v ./neo4j/plugins:/plugins \
    --name neo4j-apoc \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4JLABS_PLUGINS=\[\"apoc\"\] \
    -e NEO4J_dbms_security_procedures_unrestricted=apoc.\\\* \
    neo4j