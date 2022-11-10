# ITIL4J

This is a personal project risen from the need to quickly get dependencies of certain ITIL processes.

## Install/Setup

* Install Neo4J (e.g. via Docker)

```bash
docker run -d --name itil4j --env NEO4J_AUTH=none -p 7474:7474 -p 7687:7687 neo4j
```

* Go to the web interface (or connect otherwise, as you prefer) and connect with no parameters
* Drag'n'drop init.cypher file to the web interface or copy the code and paste it to the query execution field (starting with neo4j$)
* If you like, drag'n'drop the viewer.grass file (feel free to adapt it to your needs) into the neo4j web interface for improved UI
* Explore!

## How to Use

### Get all dependencies of one Process/Source

```cypher
MATCH (p:[Process|Source] {[name: "<Process Name>"|abb: "<Abb>"]}) OPTIONAL MATCH (p)-[r]-(f) RETURN p, r, f;
```

Example: 

```cypher
MATCH (p:Process {name: "Incident Management"}) OPTIONAL MATCH (p)-[r]-(f) RETURN p, r, f;
MATCH (p:Source {abb: "CMS"}) OPTIONAL MATCH (p)-[r]-(f) RETURN p, r, f;
```

### Get all Processes of one lifecycle phase

```cypher
MATCH (p:Process:[Phase]) RETURN p;
```

Phases are:

* Strategy
* Design
* Transition
* Operations
* Improvement

### Get complete dependenciy graph

```cypher
MATCH (p:Process), (s:Source) RETURN p, s;
```
