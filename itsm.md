# ITSM in Cipher

## Common Queries

### Get all dependencies of one Process

```cypher
MATCH (p:Process {name: "<Process Name>"}) OPTIONAL MATCH (p)-[r]-(f) RETURN p, r, f;
```

### Get all Processes of one lifecycle phase

```cypher
MATCH (p:Process:Phase) RETURN p;
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

## Create Nodes (ITIL Processes)

```cypher
CREATE (scm:Process:Design {name: "Service Catalogue Management", abb: "SCM"});
CREATE (slm:Process:Design {name: "Service Level Management", abb: "SLM", role: "Service Level Manager"});
CREATE (spm:Process:Strategy {name: "Service Portfolio Management", abb: "SPM"});
CREATE (stratm:Process:Strategy {name: "Strategy Management", abb: "STM"});
CREATE (sm:Process:Design {name: "Supplier Management", abb: "SUM"});
CREATE (chm:Process:Transition {name: "Change Managment", abb: "CHM" role: "Change Manager"});
CREATE (capm:Process:Design {name: "Capacity Management", abb: "CPM"});
CREATE (ssip:Process:Improvement {name: "7-Step Improvement Process", abb: "SSIP"});
CREATE (tps:Process:Transition {name: "Transition Planning & Support", abb: "TPS"});
CREATE (svt:Process:Transition {name: "Service Validation & Testing", abb: "SVT"});
CREATE (ce:Process:Transition {name: "Change Evalutation", abb: "CHE"});
CREATE (sacm:Process:Transition {name: "Service Asset & Configuration Management", abb: "SACM"});
CREATE (rf:Process:Operations {name: "Request Fulfillment", abb: "RF"});
CREATE (rdm:Process:Transition {name: "Release & Deployment Management", abb: "RDM", role: "Release Manager"});
CREATE (pm:Process:Operations {name: "Problem Management", abb: "PM", role: "Problem Manager"});
CREATE (km:Process:Transition {name: "Knowledge Management", abb: "KM"});
CREATE (itscm:Process:Design {name: "IT-Service Continuity Management", abb: "ITSCM"});
CREATE (ism:Process:Design {name: "Information Security Management", abb: "ISM"});
CREATE (im:Process:Operations {name: "Incident Management", abb: "IM"});
CREATE (fm:Process:Strategy {name: "Financial Management", abb: "FM", role: "Financial Manager"});
CREATE (em:Process:Operations {name: "Event Management", abb: "EM"});
CREATE (dm:Process:Strategy {name: "Demand Management", abb: "DM"});
CREATE (brm:Process:Strategy {name: "Business Relationship Management", role: "BIZ Manager"});
CREATE (avm:Process:Design {name: "Availability Management", abb: "AVM"});
CREATE (acm:Process:Operations {name: "Access Management", abb: "ACM"});
CREATE (dc:Process:Design {name: "Design Coordination", abb: "DC"});
```

## Create Nodes (ITIL Sources)

```cypher
CREATE (dml:Source {name: "Definitive Media Library"});
CREATE (cmdb:Source {name: "Configuration Management Database"});
CREATE (cms:Source {name: "Configuration Management System"});
CREATE (kedb:Source {name: "Known Error Database"});
CREATE (skms:Source {name: "Service Knowledge Management System"});
CREATE (sc:Source {name: "Service Catalogue"});
```

## Create Relations

```cypher
MATCH (s1:Source), (s2:Source) WHERE s1.name = "Service Knowledge Management System" AND s2.name = "Configuration Management System" CREATE (s1)-[:HAS_COMPONENT]->(s2) RETURN s1, s2;
MATCH (s1:Source), (s2:Source) WHERE s1.name = "Service Knowledge Management System" AND s2.name = "Known Error Database" CREATE (s1)-[:HAS_COMPONENT]->(s2) RETURN s1, s2;
MATCH (s1:Source), (s2:Source) WHERE s1.name = "Service Knowledge Management System" AND s2.name = "Service Catalogue" CREATE (s1)-[:HAS_COMPONENT]->(s2) RETURN s1, s2;
MATCH (s1:Source), (s2:Source) WHERE s1.name = "Configuration Management System" AND s2.name = "Configuration Management Database" CREATE (s1)-[:HAS_COMPONENT]->(s2) RETURN s1, s2; 
MATCH (s1:Source), (s2:Source) WHERE s1.name = "Configuration Management System" AND s2.name = "Definitive Media Library" CREATE (s1)-[:HAS_COMPONENT]->(s2) RETURN s1, s2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Incident Management" AND p2.name = "Service Level Management" CREATE (p1)-[:REPORTS_TO {items: "Incident Count"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Incident Management" AND p2.name = "Service Level Management" CREATE (p2)-[:REPORTS_TO {items: "SLA"}]->(p1) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Incident Management" AND p2.name = "Service Catalogue Management" CREATE (p2)-[:REPORTS_TO {items: "Service Catalogue"}]->(p1) RETURN p1, p2;
MATCH (p:Process), (s:Source) WHERE p.name = "Problem Management" AND s.name = "Known Error Database" CREATE (p)-[:FILLS]->(s) RETURN p, s;
MATCH (p:Process), (s:Source) WHERE p.name = "Incident Management" AND s.name = "Known Error Database" CREATE (s)-[:SERVES]->(p) RETURN p, s;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Event Management" AND p2.name = "Service Asset & Configuration Management" CREATE (p1)-[:REPORTS_TO {items: "Service Status"}]->(p2) RETURN p1, p2;
MATCH (p:Process), (s:Source) WHERE p.name = "Service Asset & Configuration Management" AND s.name = "Configuration Management System" CREATE (p)-[:FILLS]->(s) RETURN p, s;
MATCH (p:Process), (s:Source) WHERE p.name = "Incident Management" AND s.name ="Configuration Management System" CREATE (s)-[:SERVES]->(p) RETURN p, s;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Incident Management" AND p2.name = "Change Management" CREATE (p2)-[:REPORTS_TO {items: "Changelog"}]->(p1) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Incident Management" AND p2.name = "Change Management" CREATE (p1)-[:REPORTS_TO {items: "RfC"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Access Management" AND p2.name = "Change Management" CREATE (p1)-[:REPORTS_TO {items: "RfC"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Availability Management" AND p2.name = "Service Level Management" CREATE (p2)-[:REPORTS_TO {items: "SLA"}]->(p1) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Availability Management" AND p2.name = "Service Level Management" CREATE (p1)-[:REPORTS_TO {items: "Availability, MTRS, MTBSI, MTBF"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Business Relationship Management" AND p2.name = "Service Portfolio Management" CREATE (p2)-[:REPORTS_TO {items: "Service Portfolio"}]->(p1) RETURN p1, p2;
MATCH (p:Process), (s:Source) WHERE p.name = "Service Catalogue Management" AND s.name = "Service Catalogue" CREATE (p)-[:FILLS]->(s) RETURN p, s;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Service Catalogue Management" AND p2.name = "Service Portfolio Management" CREATE (p2)-[:REPORTS_TO {items: "Service Portfolio"}]->(p1) RETURN p1, p2;
MATCH (p:Process), (s:Source) WHERE p.name = "Service Catalogue Management" AND s.name = "Configuration Management System" CREATE (p)-[:FILLS]->(s) RETURN p, s;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Capacity Management" AND p2.name = "Incident Management" CREATE (p2)-[:REPORTS_TO {items: "Incidents"}]->(p1) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Capacity Management" AND p2.name = "Service Level Management" CREATE (p2)-[:REPORTS_TO {items: "SLA"}]->(p1) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Capacity Management" AND p2.name = "Change Management" CREATE (p1)-[:REPORTS_TO {items: "RfC"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Information Security Management" AND p2.name = "Access Management" CREATE (p1)-[:REPORTS_TO {items: "Technical Measures"}]->(p2) RETURN p1, p2;
MATCH (p:Process), (s:Source) WHERE p.name = "Information Security Management" AND s.name = "Configuration Management System" CREATE (p)-[:FILLS]->(s) RETURN p,s;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Change Management" AND p2.name = "Change Evaluation" CREATE (p2)-[:REPORTS_TO {items: "Change successful?"}]->(p1) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "7-Step Improvement Process" AND p2.name = "Change Evaluation" CREATE (p2)-[:REPORTS_TO {items: "future Service development"}]->(p1) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Change Management" AND p2.name = "Change Evaluation" CREATE (p1)-[:REPORTS_TO {items: "Change for evaluation"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Release & Deployment Management" AND p2.name = "Service Validation & Testing" CREATE (p1)-[:REPORTS_TO {items: "Tests"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Release & Deployment Management" AND p2.name = "Service Validation & Testing" CREATE (p2)-[:REPORTS_TO {items: "Test Report"}]->(p1) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Change Management" AND p2.name = "Problem Management" CREATE (p2)-[:REPORTS_TO {items: "RfC"}]->(p1) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Release & Deployment Management" AND p2.name = "Change Management" CREATE (p2)-[:REPORTS_TO {items: "Change acceptance and order"}]->(p1) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Service Asset & Configuration Management" AND p2.name = "Release & Deployment Management" CREATE (p2)-[:REPORTS_TO {items: "Changes"}]->(p1) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Service Asset & Configuration Management" AND p2.name = "Release & Deployment Management" CREATE (p1)-[:REPORTS_TO {items: "Changes"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Service Asset & Configuration Management" AND p2.name = "Change Management" CREATE (p1)-[:REPORTS_TO {items: "Impact Analysis"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "IT-Service Continuity Management" AND p2.name = "Change Management" CREATE (p1)-[:REPORTS_TO {items: "RfC"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Transition Planning & Support" AND p2.name = "Release & Deployment Management" CREATE (p1)-[:REPORTS_TO {items: "Transition strategy"}]->(p2) RETURN p1, p2;
MATCH (p:Process), (s:Source) WHERE p.name = "Knowledge Management" AND s.name = "Service Knowledge Management System" CREATE (p)-[:FILLS]->(s) RETURN p, s;
MATCH (p:Process), (s:Source) WHERE p.name = "Event Management" AND s.name = "Configuration Management System" CREATE (p)-[:FILLS]->(s) RETURN p, s;
MATCH (p:Process), (s:Source) WHERE p.name = "Event Management" AND s.name = "Known Error Database" CREATE (p)-[:FILLS]->(s) RETURN p, s;
MATCH (p:Process), (s:Source) WHERE p.name = "Request Fulfillment" AND s.name = "Configuration Management System" CREATE (p)-[:FILLS]->(s) RETURN p, s;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Problem Management" AND p2.name = "Incident Management" CREATE (p2)-[:REPORTS_TO {items: "Problems"}]->(p1) RETURN p1, p2;
MATCH (p:Process), (s:Source) WHERE p.name = "Problem Management" AND s.name = "Configuration Management Database" CREATE (p)-[:FILLS]->(s) RETURN p, s;
MATCH (p:Process), (s:Source) WHERE p.name = "Access Management" AND s.name = "Configuration Management System" CREATE (p)-[:FILLS]->(s) RETURN p, s;
MATCH (p:Process), (s:Source) WHERE p.name = "Access Management" AND s.name = "Configuration Management System" CREATE (s)-[:SERVES]->(p) RETURN p, s;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Strategy Management" AND p2.name = "7-Step Improvement Process" CREATE (p1)-[:REPORTS_TO {items: "Business Strategy"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Design Coordination" AND p2.name = "Change Management" CREATE (p1)-[:REPORTS_TO {items: "RfC"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Demand Management" AND p2.name = "Capacity Management" CREATE (p1)-[:REPORTS_TO {items: "Updated capacity"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Financial Management" AND p2.name = "Service Portfolio Management" CREATE (p1)-[:REPORTS_TO {items: "Budget"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Financial Management" AND p2.name = "Capacity Management" CREATE (p1)-[:REPORTS_TO {items: "Budget"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "IT-Service Continuity Management" AND p2.name = "Release & Deployment Management" CREATE (p1)-[:REPORTS_TO {items: "Continuity Plan"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Demand Management" AND p2.name = "Service Level Management" CREATE (p1)-[:REPORTS_TO {items: "Demand"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Availability Management" AND p2.name = "Service Catalogue Management" CREATE (p1)-[:REPORTS_TO {items: "Service Catalogue"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Information Security Management" AND p2.name = "Request Fulfillment" CREATE (p1)-[:REPORTS_TO {items: "Security Policy"}]->(p2) RETURN p1, p2;
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Availability Management" AND p2.name = "Incident Management" CREATE (p1)-[:REPORTS_TO {items: "Support"}]->(p2) RETURN p1, p2
MATCH (p1:Process), (p2:Process) WHERE p1.name = "IT-Service Continuity Management" AND p2.name = "Change Management" CREATE (p1)-[:REPORTS_TO {items: "RfC"}]->(p2) RETURN p1, p2
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Capacity Management" AND p2.name = "Change Management" CREATE (p1)-[:REPORTS_TO {items: "RfC"}]->(p2) RETURN p1, p2
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Supplier Management" AND p2.name = "Service Level Management" CREATE (p1)-[:REPORTS_TO {items: "Suppliers"}]->(p2) RETURN p1, p2
MATCH (p1:Process), (p2:Process) WHERE p1.name = "Service Catalogue Management" AND p2.name = "Request Fulfillment" CREATE (p1)-[:REPORTS_TO {items: "Service Catalogue"}]->(p2) RETURN p1, p2
```
