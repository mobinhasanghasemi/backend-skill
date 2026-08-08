# Service-Oriented Architecture (SOA)

## Identity
- **Type**: pattern (classic)
- **Status**: active — legacy/mixed; see microservices for modern form

## Purpose
Organize into interoperable services via standardized contracts (often XML/SOAP historically), enterprise-wide integration.

## Core Concept
Coarse-grained services that expose contracts (WSDL/XML, message formats), connect via enterprise bus (ESB), services are cross-organization.

## Activation Conditions
- legacy enterprise ecosystems with existing ESB/SOAP contracts
- integration with mainframes/legacy systems needed
- have a regulator requiring documented contracts

## Do Not Activate
- new greenfield (microservices/modular monolith are superior forms)

## Advantages / Disadvantages
+ contract discipline, mature tooling
− ESB central bottleneck, XML overhead

## Failure Modes
- ESB single point
- contract friction (frequent version cycles blocked)
- sync calls galore

## Security, Performance, Reliability
- Security: contract-level authN; moving/migrating to mTLS for service identity
- Perf: XML serialization cost; batch
- Reliability: message queues core

## Evolution
→ microservices (modern tooling) or stay if intact; else strangler-fig them out

## Evidence
- SOA literature: patterns; VERIFIED mature practice