# System Capacity & Care Load Analytics for Unaccompanied Children

## Live Dashboard

🔗 https://system-capacity-care-load-analytics-for-unaccompanied-children.streamlit.app/

---

## Project Overview

The **Unaccompanied Alien Children (UAC) Program** is a federally mandated care pipeline in which children apprehended by border authorities are transferred to the Department of Health and Human Services (HHS) for medical screening, sheltering, and reunification.

This project develops an **operational healthcare analytics framework** to monitor system capacity, intake pressure, and sustainability of care delivery over time.

Rather than simple visualization, the system models the program as a **dynamic service pipeline** consisting of:

* Intake into CBP custody
* Transfer into HHS shelters
* Discharge to sponsors
* Capacity stabilization

The dashboard provides decision-support visibility into overcrowding risk, backlog formation, and operational strain periods.

---

## Objectives

### Primary

* Quantify total children under care across the system
* Analyze inflow vs outflow balance
* Identify capacity stress windows

### Secondary

* Support staffing and shelter planning
* Improve situational awareness
* Enable policy-level evaluation

---

## Dataset

Daily operational records (2023–2025):

| Column      | Description                        |
| ----------- | ---------------------------------- |
| Date        | Reporting date                     |
| apprehended | Children entering CBP custody      |
| cbp_custody | Children held at border facilities |
| transferred | Moved into HHS care                |
| hhs_care    | Children in shelters               |
| discharged  | Released to sponsors               |

---

## Analytical Methodology

### 1. Time-Series Structuring

* Converted to continuous daily timeline
* Missing reporting days reconstructed
* State variables forward-filled
* Flow variables zero-filled

### 2. Data Validation

* Transfer ≤ CBP custody constraint
* Discharge ≤ HHS care constraint
* Reporting anomaly detection

### 3. Derived Capacity Metrics

| Metric           | Meaning                        |
| ---------------- | ------------------------------ |
| Total Load       | Government care responsibility |
| Net Intake       | System pressure indicator      |
| Growth Rate      | Expansion stress               |
| Backlog Streak   | Sustained overload             |
| Volatility Index | Operational instability        |
| Discharge Ratio  | System efficiency              |

### 4. Stress Detection

The system is considered under strain when:

* Net intake pressure is positive
* Load volatility is high
* Backlog persists over time

---

## Dashboard Features

### Core Modules

* System Load Overview
* CBP vs HHS Capacity Comparison
* Intake Pressure & Backlog Trends
* KPI Monitoring Panel

### Interactive Controls

* Date range filter
* Daily / Weekly / Monthly aggregation
* Metric selector

---

## Technology Stack

* Python
* Pandas
* Plotly
* Streamlit
* Time-Series Analysis

---

## Key Insights Generated

The dashboard helps stakeholders identify:

* Overcrowding periods
* Recovery phases
* Care throughput efficiency
* Sustainability of operations

---

## How to Run Locally

```bash
git clone https://github.com/<your-username>/uac-care-analytics.git
cd uac-care-analytics

pip install -r requirements.txt
streamlit run app.py
```

---

## Project Structure

```
uac-care-analytics/
│── app.py
│── analysis.py
│── processed.csv
│── requirements.txt
│── data/uac_cleaned.csv
```

---

## Author

**Parikshith**
Business Analyst | Data Analytics & Decision Systems

This project was developed as part of a healthcare operations analytics study focused on capacity monitoring, system stability, and policy-level decision support using time-series data and interactive visualization tools.


