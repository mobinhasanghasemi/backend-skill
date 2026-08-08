# SYSTEM DESIGN — ROOT NEURON

## Identity
- ID: architecture.system-design
- Type: process
- Domain: architecture

## Purpose
Routers for the design-process skills: how to take a vague request and produce a demanding design.

## Child Neurons
- requirements.md — gathering + acceptance
- capacity-planning.md — rough math
- design-review.md — the review checklist

## Activation Conditions
- "design a system for X"
- product brief → architecture
- interviewing-style problems should ALSO run this discipline (requirements first!)

## The discipline (order)
1. requirements (clarify; functional + non-functional)
2. constraints (scale, cost, compliance, team)
3. capacity math (rough)
4. architecture selection (Genome, patterns)
5. data model + API sketch
6. failure mode review (failure-propagation)
7. security check
8. validation & next steps

## Do Not Activate
- already-scoped feature/immediate implementation (route to domain instead)

## Mandatory questions
- What should NOT the system do? (defines scope)
- What's the worst thing that could legitimately happen? (fail)
- Who runs it? (ops)
- What's the deadline vs desired quality (timebox)

## Evidence
- Software architecture practice (SUPPORTED)