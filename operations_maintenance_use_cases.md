# Using Nimble, Jev, or JevK5 for Operations and Maintenance Use Cases

## Simple summary

Use **Nimble**, **Jev**, or **JevK5** as fast text classifiers for operations and maintenance. They should not make final plant decisions. They should read short plant text — work orders, shift logs, alarm comments, incident notes — and convert it into structured labels.

Example input:

```text
P-101A seal leak observed, standby pump started.
```

Example output:

```text
equipment = pump
failure_mode = seal
containment = true
urgency = immediate
needs_review = true
```

This structured data is useful for dashboards, bad-actor analysis, routing, prioritization, and human review.

---

## 1. Maintenance work order classification

Use case: clean up CMMS/free-text work orders.

### Input

```text
P-204 bearing temperature high, vibration increasing, inspection requested.
```

### Classifiers

| Question | Type | Example labels |
|---|---|---|
| Failure mode | choice | seal, bearing, cavitation, instrument, other |
| Work type | choice | corrective, preventive, inspection, emergency |
| Urgency | score | routine, soon, immediate |
| Safety concern | noul | true, false |
| Needs review | noul | true, false |

### Value

- Better failure coding
- Easier bad-actor reports
- Cleaner reliability data
- Less manual review by engineers and planners

---

## 2. Shift log and operator handover triage

Use case: scan many operator comments and highlight important ones.

### Input

```text
C-301 dP rising since night shift. Overhead product trending off-spec.
```

### Example output

```text
equipment_type = distillation_column
issue_type = flooding_or_instability
urgency = immediate
production_impact = high
needs_engineer_review = true
```

### Value

- Important issues do not get buried in shift notes
- Better handover summaries
- Cleaner daily production meeting issue list

---

## 3. Incident and near-miss pre-screening

Use case: route reports to the right reviewer.

### Classifiers

| Question | Type |
|---|---|
| Is this a safety event? | noul |
| Is there loss of containment? | noul |
| Is environmental impact mentioned? | noul |
| Event type | choice: leak, spill, injury, equipment damage, alarm, other |
| Severity potential | score: low, moderate, high |

### Important caution

This should **not replace HSE review**. It should only flag, sort, and route reports.

---

## 4. Equipment-specific troubleshooting assistant

Use equipment type to select the right questions.

### Pump questions

- Seal failure?
- Bearing issue?
- Cavitation?
- Suction restriction?
- Standby pump started?
- Immediate action needed?

### Heat exchanger questions

- Fouling?
- Tube leak?
- Cross-contamination?
- High pressure drop?
- Poor heat transfer?

### Distillation column questions

- Flooding?
- Weeping?
- Foaming?
- Off-spec product?
- Unstable level?
- High dP?

This is close to what the current `nimble_plant` workbook already does.

---

## 5. MOC screening

Use Nimble, Jev, or JevK5 to flag changes that may need human MOC review.

### Input

```text
Temporary bypass installed around ESD valve for startup troubleshooting.
```

### Classifiers

| Question | Type |
|---|---|
| Mentions temporary bypass? | noul |
| Affects safety system? | noul |
| Affects operating envelope? | noul |
| Needs MOC review? | noul |
| Risk potential | score: low, moderate, high |

### Important caution

The model can flag possible MOC items, but it should never approve or reject MOCs by itself.

---

## 6. Document routing / RAG router

Use Nimble, Jev, or JevK5 before a bigger AI system.

Example user question:

```text
Why is the compressor recycle valve hunting?
```

Classifier output:

```text
document_set = compressor_controls
data_source = historian
expert_area = process_control
priority = medium
```

Then another AI/RAG system can search the correct documents or data source.

---

## 7. Planner and scheduler support

Classify maintenance notifications before planning.

### Useful labels

- Discipline: mechanical, electrical, instrument, operations
- Outage required: yes/no
- Spare parts likely needed: yes/no
- Equipment criticality: low, medium, high
- Job clarity: clear, unclear

### Value

- Faster work order triage
- Better routing to the right discipline
- Improved planning quality
- Easier backlog cleanup

---

## Deployment approach

### Step 1 — Start with one use case

Do not classify everything at first.

A good first use case:

```text
maintenance work order failure coding
```

Reason: it is high value and easier to validate against historical work orders.

---

### Step 2 — Define fixed questions

Example for pumps:

```text
failure_mode:
  seal
  bearing
  cavitation
  instrument
  other

urgency:
  routine
  soon
  immediate

loss_of_containment:
  true / false
```

---

### Step 3 — Run on historical records

Take 100–300 old work orders where humans already know the correct labels.

Compare:

```text
model answer vs known correct answer
```

Measure:

- Accuracy
- Confidence when correct
- Confidence when wrong
- Which labels are confused

---

### Step 4 — Set review thresholds

Example rules:

```text
confidence > 0.85      -> accept label after validation
confidence 0.60–0.85   -> optional review
confidence < 0.60      -> human review
safety-related true     -> always human review
```

Thresholds should be based on actual site test data, not guessed.

---

### Step 5 — Integrate with tools

Possible outputs:

- Excel workbook
- CSV file
- CMMS upload
- Power BI dashboard
- Daily review report
- Bad-actor reliability report

---

## Nimble vs Jev recommendation

| Situation | Recommended engine |
|---|---|
| Sensitive plant/client data must stay local | Nimble |
| Cloud API is acceptable and speed is important | Jev |
| Need independent comparison | Run both |
| Safety/event triage | Run both plus human review |
| High-volume batch classification | Jev may be faster |
| Offline/local plant network | Nimble |

---

## Best practical use

Use the tools like this:

```text
Nimble/Jev = classification layer
Engineer = decision maker
CMMS/Excel/Power BI = system of record
```

They are best at:

- Sorting
- Tagging
- Flagging
- Routing
- Prioritizing review

They are not for:

- Approving MOCs
- Replacing HAZOP
- Deciding whether equipment is safe
- Making live operating decisions

---

## Suggested next improvement for the current workbook

The current workbook has a possible ambiguity around containment.

Instead of one broad question:

```text
containment: Does the statement describe process fluid leaking out of the equipment to the surroundings?
```

Consider splitting into two clearer questions:

```text
external_containment_loss:
Does the statement describe process fluid leaking outside the equipment to atmosphere, ground, drain, or surrounding area?

internal_cross_leak:
Does the statement describe leakage between process sides, utility sides, shell side, or tube side?
```

This would help distinguish external leaks from heat-exchanger tube leaks or internal cross-contamination.
