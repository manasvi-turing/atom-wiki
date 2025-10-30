---
tags: [testing, tables, datatables]
---

# Testing DataTables

This document tests the DataTables functionality with various table sizes.

## Small Table (Should NOT get DataTables)

Tables with less than 3 rows should remain simple tables:

| Name | Role | Status |
|------|------|--------|
| Alice | Admin | Active |
| Bob | User | Active |

## Medium Table (SHOULD get DataTables)

This table has enough rows to benefit from search, sort, and pagination:

| ID | Name | Email | Department | Role | Salary | Location | Status |
|----|------|-------|------------|------|--------|----------|--------|
| 1 | Alice Johnson | alice@example.com | Engineering | Senior Developer | $120,000 | New York | Active |
| 2 | Bob Smith | bob@example.com | Marketing | Manager | $95,000 | San Francisco | Active |
| 3 | Charlie Brown | charlie@example.com | Sales | Representative | $65,000 | Chicago | Active |
| 4 | Diana Prince | diana@example.com | Engineering | Lead Developer | $140,000 | Austin | Active |
| 5 | Edward Norton | edward@example.com | HR | Specialist | $70,000 | Boston | Active |
| 6 | Fiona Apple | fiona@example.com | Finance | Analyst | $80,000 | Seattle | Active |
| 7 | George Miller | george@example.com | Engineering | Junior Developer | $75,000 | Portland | Active |
| 8 | Hannah Montana | hannah@example.com | Marketing | Coordinator | $60,000 | Denver | Active |
| 9 | Ian Fleming | ian@example.com | Sales | Manager | $100,000 | Miami | Active |
| 10 | Julia Roberts | julia@example.com | Engineering | Senior Developer | $125,000 | Los Angeles | Active |

## Large Table (SHOULD get DataTables with pagination)

This table has many rows and really benefits from DataTables features:

| ID | Product | Category | Price | Stock | Supplier | Rating | Last Updated |
|----|---------|----------|-------|-------|----------|--------|--------------|
| 1 | Laptop Pro 15 | Electronics | $1,299 | 45 | TechCorp | 4.5 | 2024-01-15 |
| 2 | Wireless Mouse | Accessories | $29 | 230 | PeripheralCo | 4.2 | 2024-01-14 |
| 3 | USB-C Hub | Accessories | $49 | 120 | ConnectTech | 4.7 | 2024-01-13 |
| 4 | Monitor 27" 4K | Electronics | $599 | 67 | DisplayPlus | 4.6 | 2024-01-12 |
| 5 | Mechanical Keyboard | Accessories | $129 | 89 | KeyMaster | 4.8 | 2024-01-11 |
| 6 | Webcam HD | Electronics | $79 | 156 | VisionTech | 4.3 | 2024-01-10 |
| 7 | Desk Lamp LED | Furniture | $39 | 203 | LightCo | 4.4 | 2024-01-09 |
| 8 | Office Chair | Furniture | $299 | 34 | ComfortSeats | 4.7 | 2024-01-08 |
| 9 | Standing Desk | Furniture | $499 | 28 | ErgoPro | 4.9 | 2024-01-07 |
| 10 | Noise Cancelling Headphones | Electronics | $249 | 112 | AudioMax | 4.6 | 2024-01-06 |
| 11 | External SSD 1TB | Storage | $119 | 178 | DataDrive | 4.5 | 2024-01-05 |
| 12 | Tablet 10" | Electronics | $399 | 92 | TabletPro | 4.4 | 2024-01-04 |
| 13 | Wireless Charger | Accessories | $35 | 267 | ChargeTech | 4.1 | 2024-01-03 |
| 14 | Phone Case | Accessories | $19 | 445 | ProtectCo | 4.0 | 2024-01-02 |
| 15 | Screen Protector | Accessories | $12 | 523 | ShieldTech | 3.9 | 2024-01-01 |
| 16 | Cable Organizer | Accessories | $15 | 334 | OrganizePro | 4.3 | 2023-12-31 |
| 17 | Laptop Stand | Accessories | $45 | 156 | StandCo | 4.5 | 2023-12-30 |
| 18 | Bluetooth Speaker | Electronics | $89 | 198 | SoundWave | 4.4 | 2023-12-29 |
| 19 | Smart Watch | Electronics | $279 | 87 | WearTech | 4.2 | 2023-12-28 |
| 20 | Fitness Tracker | Electronics | $129 | 143 | FitGear | 4.3 | 2023-12-27 |
| 21 | Power Bank 20000mAh | Accessories | $49 | 267 | PowerPlus | 4.6 | 2023-12-26 |
| 22 | HDMI Cable 6ft | Accessories | $14 | 412 | CableCo | 4.1 | 2023-12-25 |
| 23 | Graphics Tablet | Electronics | $199 | 54 | ArtTech | 4.7 | 2023-12-24 |
| 24 | Microphone USB | Electronics | $79 | 98 | AudioPro | 4.5 | 2023-12-23 |
| 25 | Router WiFi 6 | Electronics | $149 | 76 | NetGear | 4.4 | 2023-12-22 |

## Test Features

With DataTables enabled, you should be able to:

1. **Search** - Type in the search box to filter rows
2. **Sort** - Click column headers to sort ascending/descending
3. **Paginate** - Navigate through pages if table has many rows
4. **Page size** - Choose how many rows to display (5, 10, 25, 50, 100)

## Simple 2-Row Table (Should NOT get DataTables)

| Feature | Status |
|---------|--------|
| Search | ✅ Enabled |

This tiny table should remain simple.

