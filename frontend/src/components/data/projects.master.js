// src/components/data/projects.master.js

export const counties = [
  {
    county_id: "KE-001",
    name: "Mombasa",
    region: "Coast",
    projects: [
      {
        project_id: "MSA-AH-001",
        title: "Buxton Affordable Housing – Phase I",
        sector: "Housing",
        category: "Affordable Housing",
        owner_type: "Government",
        owner_name: "Ministry of Housing",
        status: "in_progress",
        progress: 65,
        budget_kes: 6500000000,
        start_date: "2023-05-01",
        expected_end_date: "2026-02-28",
        site: {
          sub_county: "Mvita",
          ward: "Buxton"
        }
      },
      {
        project_id: "MSA-INF-002",
        title: "Likoni–Lunga Lunga Road Expansion",
        sector: "Infrastructure",
        category: "Road",
        owner_type: "Government",
        owner_name: "KeNHA",
        status: "completed",
        progress: 100,
        budget_kes: 4200000000,
        start_date: "2020-01-10",
        end_date: "2024-07-15",
        site: {
          sub_county: "Likoni"
        }
      }
    ]
  },

  {
    county_id: "KE-047",
    name: "Nairobi",
    region: "Nairobi Metropolitan",
    projects: [
      {
        project_id: "NBO-AH-001",
        title: "Pangani Affordable Housing Project",
        sector: "Housing",
        category: "Affordable Housing",
        owner_type: "Government",
        owner_name: "Nairobi County Government",
        status: "in_progress",
        progress: 72,
        budget_kes: 8200000000,
        start_date: "2022-08-01",
        expected_end_date: "2026-06-30",
        site: {
          sub_county: "Starehe",
          ward: "Pangani"
        }
      },
      {
        project_id: "NBO-HLT-004",
        title: "Mathare Level 4 Hospital Upgrade",
        sector: "Health",
        category: "Hospital",
        owner_type: "NGO",
        owner_name: "AMREF",
        status: "on_hold",
        progress: 40,
        budget_kes: 1200000000,
        start_date: "2023-03-12",
        site: {
          sub_county: "Mathare"
        }
      }
    ]
  },

  {
    county_id: "KE-022",
    name: "Kilifi",
    region: "Coast",
    projects: [
      {
        project_id: "KLF-EDU-001",
        title: "Kilifi Technical Training Institute",
        sector: "Education",
        category: "TVET",
        owner_type: "Government",
        owner_name: "Ministry of Education",
        status: "planned",
        progress: 0,
        budget_kes: 950000000,
        start_date: "2026-01-01",
        site: {
          sub_county: "Kilifi North"
        }
      }
    ]
  }
];

/* -------------------------------------------------
   Helper (optional, safe to use anywhere)
-------------------------------------------------- */
export const getAllProjects = () =>
  counties.flatMap(c =>
    c.projects.map(p => ({
      ...p,
      county: c.name,
      region: c.region
    }))
  );
