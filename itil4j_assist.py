#!/usr/bin/env python3
from neo4j import GraphDatabase

NEO4J_URL: str = "bolt://localhost:7687"

PROCESSES: dict = {"SSIP": "7-Step Improvement Process",
                   "ACM": "Access Management",
                   "AVM": "Availability Management",
                   "BRM": "Business Relationship Management",
                   "CPM": "Capacity Management",
                   "CHM": "Change Management",
                   "DM": "Demand Management",
                   "DC": "Design Coordination",
                   "EM": "Event Management",
                   "FM": "Financial Management",
                   "IM": "Incident Management",
                   "ISM": "Information Security Management",
                   "ITSCM": "IT-Service Continuity Management",
                   "KM": "Knowledge Management",
                   "PM": "Problem Management",
                   "RDM": "Release & Deployment Management",
                   "RF": "Request Fulfillment",
                   "SACM": "Service Asset & Configuration Management",
                   "SCM": "Service Catalogue Management",
                   "SLM": "Service Level Management",
                   "SPM": "Service Portfolio Management",
                   "SVT": "Service Validation & Testing",
                   "STM": "Strategy Management",
                   "SUM": "Supplier Management",
                   "TPS": "Transition Planning & Support"}

SOURCES: dict = {"CMDB": "Configuration Management Database",
                 "CMS": "Configuration Management System",
                 "DML": "Definitive Media Library",
                 "KEDB": "Known Error Database",
                 "SC": "Service Catalogue",
                 "SKMS": "Service Knowledge Management System"}


def is_valid_process(process) -> bool:
    return process in PROCESSES


def is_valid_source(source) -> bool:
    return source in SOURCES


def print_valid_processes() -> None:
    print(PROCESSES)


def print_valid_sources() -> None:
    print(SOURCES)


class Neo4jAssist:

    def __init__(self, uri=NEO4J_URL):
        self.driver = GraphDatabase.driver(uri)

    def close(self):
        self.driver.close()

    def new_relationship(self, start_node, end_node, relationship_type, properties=None):
        with self.driver.session() as session:
            if properties is None:
                properties = {}
            relationship = session.write_transaction(self._create_relationship, start_node, end_node, relationship_type,
                                                     properties)
            print(relationship)

    def print_dependency_graph(self):
        with self.driver.session() as session:
            graph = session.write_transaction(self._get_dependency_graph)
            print(graph)

    def print_process_dependencies(self, process):
        with self.driver.session() as session:
            dependencies = session.write_transaction(self._get_process_dependencies, process)
            print(dependencies)

    @staticmethod
    def _create_relationship(tx, start_node, end_node, relationship_type, properties=None):
        result = tx.run(
            "MATCH (a), (b) WHERE a.abb = '$start_node' AND b.abb = '$end_node' CREATE (a)-[r:$relationship_type $properties]->(b) RETURN a, b",
            start_node=start_node, end_node=end_node, relationship_type=relationship_type, properties=properties)
        return result

    @staticmethod
    def _get_dependency_graph(tx):
        result = tx.run("MATCH (p:Process), (s:Source) RETURN p, s")
        return result

    @staticmethod
    def _get_dependencies_for_process(tx, process):
        result = tx.run("MATCH (p:Process {name: '$process'}) OPTIONAL MATCH (p)-[r]-(f) RETURN p, r, f",
                        process=process)
        return result


def main():
    itil4j = Neo4jAssist()

    # Do things

    itil4j.close()


if __name__ == "__main__":
    main()
