


export const dashboardConfig = {
  system_admin: {
    title: 'System Administrator Dashboard',
    subtitle: 'Complete system overview and management',
    stats: ['projects', 'users', 'budget', 'regions'],
    widgets: ['stats', 'projects', 'progress', 'finance', 'payments', 'safety', 'quick-actions', 'notifications']
  },

  regional_admin: {
    title: 'Regional Administrator Dashboard',
    subtitle: 'Regional projects and performance tracking',
    stats: ['regional-projects', 'sites', 'budget', 'completion'],
    widgets: ['stats', 'projects', 'progress', 'finance', 'quick-actions', 'notifications']
  },

  project_owner: {
    title: 'Project Owner Dashboard',
    subtitle: 'Investment and project oversight',
    stats: ['owned-projects', 'investment', 'roi', 'completion'],
    widgets: ['stats', 'projects', 'progress', 'finance', 'payments', 'quick-actions', 'notifications']
  },

  project_manager: {
    title: 'Project Manager Dashboard',
    subtitle: 'Project execution and team coordination',
    stats: ['active-projects', 'sites', 'team-size', 'progress'],
    widgets: ['stats', 'projects', 'progress', 'safety', 'quick-actions', 'notifications']
  },

  site_manager: {
    title: 'Site Manager Dashboard',
    subtitle: 'Daily site operations and workforce management',
    stats: ['sites', 'workforce', 'tasks-today', 'safety-score'],
    widgets: ['stats', 'projects', 'progress', 'safety', 'quick-actions', 'notifications']
  },

  civil_engineer: {
    title: 'Civil Engineer Dashboard',
    subtitle: 'Technical oversight and engineering reviews',
    stats: ['projects', 'inspections', 'drawings', 'approvals'],
    widgets: ['stats', 'projects', 'progress', 'quick-actions', 'notifications']
  },

  structural_engineer: {
    title: 'Structural Engineer Dashboard',
    subtitle: 'Structural design and analysis',
    stats: ['projects', 'designs', 'calculations', 'approvals'],
    widgets: ['stats', 'projects', 'progress', 'quick-actions', 'notifications']
  },

  architect: {
    title: 'Architect Dashboard',
    subtitle: 'Design coordination and approvals',
    stats: ['projects', 'drawings', 'revisions', 'approvals'],
    widgets: ['stats', 'projects', 'progress', 'quick-actions', 'notifications']
  },

  quantity_surveyor: {
    title: 'Quantity Surveyor Dashboard',
    subtitle: 'Cost estimation and budget tracking',
    stats: ['projects', 'estimates', 'variations', 'savings'],
    widgets: ['stats', 'projects', 'finance', 'quick-actions', 'notifications']
  },

  contractor: {
    title: 'Contractor Dashboard',
    subtitle: 'Project execution and deliverables',
    stats: ['contracts', 'deliverables', 'payment-due', 'completion'],
    widgets: ['stats', 'projects', 'progress', 'payments', 'quick-actions', 'notifications']
  },

  subcontractor: {
    title: 'Subcontractor Dashboard',
    subtitle: 'Task assignments and progress tracking',
    stats: ['tasks', 'workforce', 'payment-due', 'completion'],
    widgets: ['stats', 'projects', 'progress', 'payments', 'quick-actions', 'notifications']
  },

  consultant: {
    title: 'Consultant Dashboard',
    subtitle: 'Advisory and technical guidance',
    stats: ['projects', 'reports', 'recommendations', 'meetings'],
    widgets: ['stats', 'projects', 'progress', 'quick-actions', 'notifications']
  },

  qa_officer: {
    title: 'QA Officer Dashboard',
    subtitle: 'Quality assurance and compliance',
    stats: ['inspections', 'passed', 'failed', 'pending'],
    widgets: ['stats', 'projects', 'quick-actions', 'notifications']
  },

  safety_officer: {
    title: 'Safety Officer Dashboard',
    subtitle: 'Safety compliance and incident management',
    stats: ['sites', 'incidents', 'audits', 'compliance-score'],
    widgets: ['stats', 'projects', 'safety', 'quick-actions', 'notifications']
  },

  finance_officer: {
    title: 'Finance Officer Dashboard',
    subtitle: 'Financial management and payments',
    stats: ['budget', 'spent', 'pending-payments', 'variance'],
    widgets: ['stats', 'finance', 'payments', 'quick-actions', 'notifications']
  },

  procurement_officer: {
    title: 'Procurement Officer Dashboard',
    subtitle: 'Supplier management and purchase orders',
    stats: ['orders', 'suppliers', 'deliveries', 'pending'],
    widgets: ['stats', 'projects', 'payments', 'quick-actions', 'notifications']
  },

  auditor: {
    title: 'Auditor Dashboard',
    subtitle: 'Financial and compliance auditing',
    stats: ['audits', 'findings', 'resolved', 'pending'],
    widgets: ['stats', 'finance', 'payments', 'projects', 'quick-actions', 'notifications']
  },

  supplier: {
    title: 'Supplier Dashboard',
    subtitle: 'Orders, deliveries, and payments tracking',
    stats: ['orders', 'deliveries', 'invoices', 'payments'],
    widgets: ['stats', 'payments', 'quick-actions', 'notifications']
  },

  ai_assistant: {
    title: 'AI Assistant Dashboard',
    subtitle: 'Intelligent insights and predictions',
    stats: ['predictions', 'recommendations', 'alerts', 'accuracy'],
    widgets: ['stats', 'projects', 'finance', 'safety', 'notifications']
  },

  public_viewer: {
    title: 'Public Viewer Dashboard',
    subtitle: 'Transparency and project information',
    stats: ['total-projects', 'total-units', 'total-investment', 'regions'],
    widgets: ['stats', 'projects', 'progress', 'notifications']
  },

  default: {
    title: 'Dashboard',
    subtitle: 'Welcome to ICMFS',
    stats: ['projects', 'sites', 'budget', 'completion'],
    widgets: ['stats', 'projects', 'quick-actions', 'notifications']
  }
}