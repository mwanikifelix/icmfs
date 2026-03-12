// src/components/data/project.site.activity.js

export const projectSiteActivity = [
  {
    project_id: "MSA-AH-001",
    reports: [
      {
        report_id: "RPT-MSA-001",
        report_type: "Daily",
        submitted_by: {
          name: "Eng. Hassan Ali",
          role: "Site Engineer"
        },
        report_date: "2026-01-28",
        status_update: "Foundation works ongoing. Block C slab completed.",
        progress_percentage: 68,
        workforce: {
          skilled: 45,
          unskilled: 120,
          supervisors: 6,
          total: 171
        },
        expenses: {
          currency: "KES",
          items: [
            { item: "Cement", amount: 320000 },
            { item: "Steel Reinforcement", amount: 780000 },
            { item: "Labour", amount: 450000 }
          ],
          total: 1550000
        },
        media: {
          photos: [
            {
              file_id: "IMG-MSA-001",
              url: "/uploads/MSA-AH-001/photos/slab_block_c.jpg",
              caption: "Block C slab reinforcement",
              uploaded_at: "2026-01-28 10:24"
            }
          ],
          videos: [
            {
              file_id: "VID-MSA-001",
              url: "/uploads/MSA-AH-001/videos/site_walkthrough.mp4",
              duration_seconds: 95
            }
          ]
        },
        issues: [
          "Delayed cement delivery",
          "Heavy rains slowing excavation"
        ]
      }
    ]
  }
];

/* Helpers */
export const getProjectActivityById = (projectId) =>
  projectSiteActivity.find(a => a.project_id === projectId);

export const getLatestReport = (projectId) => {
  const activity = getProjectActivityById(projectId);
  return activity?.reports?.at(-1) || null;
};
