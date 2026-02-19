# Ted's Operations Dashboard 📊

A Python-based operations analytics tool built to automate performance reporting across multiple salon branches — replacing manual Excel workflows with automated data pipelines and visual dashboards.

---

## 🎯 Why I Built This

In my current role managing IT operations across 22 branches, performance data was scattered across spreadsheets and reviewed manually. This project automates that process: feeding in daily appointment and revenue data, it generates branch-level insights, peak-hour analysis, and service breakdowns — instantly.

**Real problem → real solution.** No toy data, no tutorial clone.

---

## 📸 Dashboard Output

![Dashboard Preview](reports/dashboard_example.png)

---

## 🔧 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| pandas | Data loading, transformation, aggregation |
| matplotlib | Chart generation and dashboard layout |
| CSV | Input format (easily swappable for Excel/DB) |

---

## 📂 Project Structure

```
teds-ops-dashboard/
├── dashboard.py          # Main script — run this
├── requirements.txt      # Dependencies
├── data/
│   └── sample_data.csv   # Anonymized sample dataset
└── reports/              # Auto-generated output (charts + CSVs)
```

---

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/teds-ops-dashboard.git
cd teds-ops-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
python dashboard.py
```

Output: a PNG dashboard + 3 CSV reports saved to `/reports/`

---

## 📊 What It Analyses

- **Branch Revenue Comparison** — which locations drive the most income
- **Peak Hour Heatmap** — when is demand highest across the day
- **Service Type Breakdown** — haircut vs colour vs treatment revenue split
- **Daily Trend** — revenue trajectory over time
- **KPI Summary Table** — key numbers at a glance

---

## 💡 What I Learned / What Broke

- pandas `groupby` + `agg` is powerful but needs careful column naming — lost 30 mins to a silent overwrite bug
- matplotlib `GridSpec` for multi-panel dashboards was new to me — iterated 3 times to get the layout right
- anonymizing real data while keeping it realistic required generating proportional fake values

---

## 🔮 Next Steps (Planned)

- [ ] AWS S3 integration — upload reports automatically after generation
- [ ] AWS Lambda scheduler — run daily at 08:00 via CloudWatch Events
- [ ] Slack/email notification when report is ready
- [ ] Add Terraform IaC for provisioning the AWS infrastructure

---

## 📝 Data Note

All data in `/data/sample_data.csv` is anonymized and synthetic. Branch names and figures do not represent real business data.

---

*Built by Osman Ural | AWS DevOps learner | London, UK*
