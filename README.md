# SignalPost Company Verification Agent

SignalPost is a multi-source company verification agent that collects,
checks, compares, and reports company information using public sources.

## Project Objective

The goal of SignalPost is to verify company information using:

1. Official company registry data
2. A second public source
3. Cross-source evidence matching
4. Official company status analysis

The system is designed as a rule-based verification workflow.

---

## Features

### 1. Company Lookup

The agent accepts a Norwegian organisation number and searches the
saved company dataset.

If the company is not available locally, SignalPost performs a live
lookup using the Brønnøysundregistrene API.

### 2. Company Profile

The system collects information such as:

- Company name
- Organisation number
- Organisation type
- Registration date
- Foundation date
- Industry code
- Industry description
- Employee count
- Website
- Email
- Phone
- Address
- Municipality
- Country

### 3. Second Public Source

SignalPost uses Wikidata as a second public evidence source.

The second source can provide information such as:

- Company number
- Company name
- Description
- Website
- Country
- Industry
- Wikidata entity

### 4. Evidence Matching

Information from the primary and secondary sources is normalized
and compared.

The system identifies:

- MATCH
- MISMATCH
- NOT_AVAILABLE

It also calculates:

- Evidence coverage
- Available-field match rate
- Matched fields
- Mismatched fields
- Unavailable fields

### 5. Official Status Analysis

SignalPost checks official registry status information including:

- Bankruptcy
- Liquidation

The rule-based status analyzer reports:

- LOW
- MEDIUM
- HIGH

These labels describe the registry-status conditions detected by the
program and are not financial predictions.

---

## Architecture

```text
                         SIGNALPOST
                              |
                              v
                     Company Number Input
                              |
                              v
                  +------------------------+
                  | Primary Company Lookup |
                  +-----------+------------+
                              |
                    +---------+---------+
                    |                   |
                    v                   v
             Local CSV Dataset     Brreg API
                    |                   |
                    +---------+---------+
                              |
                              v
                     Company Profile
                              |
                 +------------+------------+
                 |                         |
                 v                         v
        Second Public Source       Official Status
             Wikidata                 Analysis
                 |                         |
                 +------------+------------+
                              |
                              v
                    Evidence Matching
                              |
                              v
                    Final Verification
                         Report