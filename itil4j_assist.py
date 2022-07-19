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

RELATIONSHIPS = ["REPORTS_TO", "FILLS", "SERVES"]


def is_valid_process(process) -> bool:
    return process in PROCESSES


def is_valid_source(source) -> bool:
    return source in SOURCES


def is_valid_relationship(relationship) -> bool:
    return relationship in RELATIONSHIPS


def print_valid_processes() -> None:
    for process in PROCESSES:
        print(f"{process} - {PROCESSES[process]}")


def print_valid_sources() -> None:
    for source in SOURCES:
        print(f"{source} - {SOURCES[source]}")


def print_valid_relationships() -> None:
    for relationship in RELATIONSHIPS:
        print(relationship)


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
            dependencies = session.write_transaction(self._get_dependencies_for_process, process)
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

    print("\n---- ITIL4J Assist ----")

    while True:
        print("\n")
        print("[1] Create new relationship")
        print("[2] Print dependency graph")
        print("[3] Print process dependencies")
        print("[4] Print valid processes")
        print("[5] Print valid sources")
        print("[6] Print valid relationships")
        print("[0] Exit")

        choice = input("[?] Enter your choice: ")

        print("\n")

        match choice:
            case "1":
                start_node = input("[?] Enter start node: ")
                end_node = input("[?] Enter end node: ")
                relationship_type = input("[?] Enter relationship type: ")
                properties = input("[?] Enter items property (optional): ")
                if properties == "":
                    properties = None
                elif not properties == "":
                    properties = "{items: '" + properties + "'}"

                if is_valid_process(start_node) and is_valid_process(end_node) and is_valid_relationship(relationship_type):
                    itil4j.new_relationship(start_node, end_node, relationship_type, properties)
                else:
                    print("[!] Invalid process or relationship type")
                break
            case "2":
                itil4j.print_dependency_graph()
                break
            case "3":
                process = input("[?] Enter process: ")
                if is_valid_process(process):
                    itil4j.print_process_dependencies(process)
                else:
                    print("[!] Invalid process")
                break
            case "4":
                print_valid_processes()
            case "5":
                print_valid_sources()
            case "6":
                print_valid_relationships()
            case "0":
                break
            case _:
                print("[!] Invalid choice")

    itil4j.close()
    exit(0)


if __name__ == "__main__":
    main()
