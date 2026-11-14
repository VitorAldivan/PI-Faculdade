# Nova DPS Informática - Service Management & Business Intelligence System (v2.0)
> Integrative Project I - FATEC Ipiranga · Applied Computing & Database Technology

A modern, high-performance desktop application for computer maintenance management, parts traceability, and executive decision-making. Developed 100% in **Python (PySide6 with Windows 11 Fluent Design)** and backed by a **Relational Database** with strict ACID integrity.

---

## 🎯 Academic Abstract
> **Abstract:** This project presents an integrated software and business intelligence solution designed for *Nova DPS Informática*, a computer technical assistance company specialized in motherboard microelectronics and hardware repair. The system addresses critical operational bottlenecks, including queue wait times, untracked replacement components, and delayed financial reconciliation. Built upon a 3-tier architecture using Python (PySide6), SQLAlchemy, and a relational database engine (PostgreSQL/SQLite), the application provides complete CRUD modules, automated PDF executive reports, and an analytical dashboard with window functions and star-schema exports for Power BI. Automated testing with pytest ensures referential integrity and software quality.

---

## 🚀 Key Features
- **Modern Windows 11 Fluent Interface:** Built with PySide6 and QFluentWidgets, featuring responsive animations, dark/light theme support, and card-based metrics.
- **Embedded Executive Dashboard:** Real-time KPI cards (active tickets, revenue, average ticket, customer count), column charts (monthly billing), and donut charts (top repair services).
- **Service Queue Management:** Intelligent queue sorting service tickets by operational wait time to minimize turnaround time (TAT).
- **Comprehensive CRUD Operations:** Centralized management of Customers (with full geolocation and address data), Service Orders, Technical Diagnostics, Parts Inventory, and Payments.
- **Star Schema Power BI Integration:** One-click script exporting `dim_customer`, `dim_order`, `fact_service`, `fact_payment`, and `fact_part` with ready-to-use DAX measures.
- **Automated PDF Reporting:** Instant generation of executive reports with ReportLab.

---

## 🛠️ Tech Stack
- **Language:** Python 3.11+ / 3.13
- **GUI Framework:** PySide6 (Qt for Python) & PySide6-Fluent-Widgets
- **Database & ORM:** PostgreSQL / SQLite with SQLAlchemy 2.0
- **Data Analysis & BI:** Pandas, ReportLab, and Microsoft Power BI Desktop
- **Testing & Quality Assurance:** pytest, Faker (pt_BR)

---

## ⚡ Quick Start

1. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Initialize and populate database (100+ synthetic records):**
   ```powershell
   python scripts/popular_banco.py
   ```

3. **Launch desktop application:**
   ```powershell
   python main.py
   ```

4. **Run automated test suite:**
   ```powershell
   pytest
   ```
