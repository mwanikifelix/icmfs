<template>
  <div class="risk-assessments">
    <!-- Header -->
    <div class="page-header">
      <div>
        <span class="page-tag">SAFETY MODULE · AI RISK ENGINE</span>
        <h1>Risk Assessments</h1>
        <p class="page-sub">AI-powered risk prediction and proactive mitigation tracking for all construction sites</p>
      </div>
      <div class="header-actions">
        <button class="btn-secondary" @click="runAIPrediction">
          <span class="ai-icon">🤖</span> Run AI Prediction
        </button>
        <button class="btn-primary" @click="showForm = true">+ Log Risk</button>
      </div>
    </div>

    <!-- AI Prediction Banner -->
    <div class="ai-banner" v-if="aiRunning">
      <div class="ai-pulse"></div>
      <span class="ai-text">AI Risk Engine analyzing site data, EVM metrics, and historical incidents...</span>
      <div class="ai-progress">
        <div class="ai-fill" :style="{ width: aiProgress + '%' }"></div>
      </div>
    </div>

    <!-- Risk Matrix Overview -->
    <div class="matrix-section">
      <div class="matrix-header">
        <h2>Risk Matrix</h2>
        <span class="matrix-sub">Likelihood × Impact Assessment</span>
      </div>
      <div class="matrix-grid-wrap">
        <div class="matrix-y-label">
          <span>IMPACT</span>
        </div>
        <div class="matrix-content">
          <div class="matrix-grid">
            <div v-for="cell in matrixCells" :key="`${cell.row}-${cell.col}`"
              class="matrix-cell" :class="cell.level"
              :title="`Likelihood: ${cell.col}, Impact: ${cell.row}`">
              <div class="cell-dots">
                <div v-for="risk in getRisksInCell(cell.row, cell.col)" :key="risk.id"
                  class="risk-dot" :title="risk.title">
                </div>
              </div>
              <span class="cell-label">{{ cell.label }}</span>
            </div>
          </div>
          <div class="matrix-x-labels">
            <span v-for="l in ['Very Low', 'Low', 'Medium', 'High', 'Very High']" :key="l">{{ l }}</span>
          </div>
          <div class="matrix-x-title">LIKELIHOOD</div>
        </div>
      </div>
    </div>

    <!-- Risk Stats -->
    <div class="risk-stats">
      <div class="risk-stat" v-for="s in riskStats" :key="s.label" :class="s.cls">
        <div class="rs-val">{{ s.val }}</div>
        <div class="rs-label">{{ s.label }}</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <select v-model="filterLevel" class="filter-select">
        <option value="">All Levels</option>
        <option value="critical">Critical</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>
      <select v-model="filterSite" class="filter-select">
        <option value="">All Sites</option>
        <option v-for="s in siteOptions" :key="s" :value="s">{{ s }}</option>
      </select>
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Status</option>
        <option value="open">Open</option>
        <option value="mitigating">Mitigating</option>
        <option value="mitigated">Mitigated</option>
        <option value="accepted">Accepted</option>
      </select>
      <div class="sort-control">
        <label class="mono">Sort by:</label>
        <select v-model="sortBy" class="filter-select">
          <option value="score">Risk Score</option>
          <option value="date">Date Added</option>
          <option value="site">Site</option>
        </select>
      </div>
    </div>

    <!-- Risk Cards -->
    <div class="risk-list">
      <div class="risk-card" v-for="risk in filteredRisks" :key="risk.id" @click="viewRisk(risk)">
        <div class="risk-level-bar" :class="risk.level"></div>
        <div class="risk-body">
          <div class="risk-top">
            <div class="risk-id-title">
              <span class="risk-ref mono">{{ risk.ref }}</span>
              <span class="risk-title">{{ risk.title }}</span>
            </div>
            <div class="risk-badges">
              <span class="level-badge" :class="risk.level">{{ risk.level }}</span>
              <span class="status-badge" :class="risk.status">{{ risk.status }}</span>
              <span class="ai-badge" v-if="risk.aiPredicted">🤖 AI</span>
            </div>
          </div>
          <p class="risk-desc">{{ risk.description }}</p>
          <div class="risk-meta">
            <span>📍 {{ risk.site }}</span>
            <span>👤 {{ risk.owner }}</span>
            <span>📅 {{ risk.dateAdded }}</span>
            <span>🏷 {{ risk.category }}</span>
          </div>
          <div class="risk-scores">
            <div class="score-item">
              <span class="score-lbl mono">Likelihood</span>
              <div class="score-dots">
                <div v-for="n in 5" :key="n" class="score-dot" :class="n <= risk.likelihood ? risk.level : 'empty'"></div>
              </div>
              <span class="score-num">{{ risk.likelihood }}/5</span>
            </div>
            <div class="score-item">
              <span class="score-lbl mono">Impact</span>
              <div class="score-dots">
                <div v-for="n in 5" :key="n" class="score-dot" :class="n <= risk.impact ? risk.level : 'empty'"></div>
              </div>
              <span class="score-num">{{ risk.impact }}/5</span>
            </div>
            <div class="risk-score-total" :class="risk.level">
              <span class="total-label">Score</span>
              <span class="total-val">{{ risk.likelihood * risk.impact }}</span>
            </div>
          </div>
          <div class="mitigation-preview" v-if="risk.mitigation">
            <span class="mit-label mono">Mitigation:</span>
            <span class="mit-text">{{ risk.mitigation }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Log Risk Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>Log New Risk</h2>
          <button class="close-btn" @click="showForm = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>Risk Title *</label>
              <input v-model="form.title" type="text" placeholder="e.g. Foundation subsidence risk" />
            </div>
            <div class="form-group">
              <label>Category *</label>
              <select v-model="form.category">
                <option value="">Select category...</option>
                <option>Structural</option>
                <option>Electrical</option>
                <option>Financial</option>
                <option>Schedule</option>
                <option>Environmental</option>
                <option>Worker Safety</option>
                <option>Procurement</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Site *</label>
              <select v-model="form.site">
                <option value="">Select site...</option>
                <option v-for="s in siteOptions" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Risk Owner *</label>
              <select v-model="form.owner">
                <option value="">Assign owner...</option>
                <option>Grace Otieno</option>
                <option>James Mutua</option>
                <option>Peter Kamau</option>
                <option>Alice Wanjiku</option>
              </select>
            </div>
          </div>
          <div class="form-group full">
            <label>Description *</label>
            <textarea v-model="form.description" rows="3" placeholder="Describe the risk and potential consequences..."></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Likelihood (1–5)</label>
              <div class="rating-input">
                <button v-for="n in 5" :key="n"
                  :class="['rating-btn', form.likelihood >= n ? 'active' : '']"
                  @click="form.likelihood = n">{{ n }}</button>
              </div>
            </div>
            <div class="form-group">
              <label>Impact (1–5)</label>
              <div class="rating-input">
                <button v-for="n in 5" :key="n"
                  :class="['rating-btn', form.impact >= n ? 'active' : '']"
                  @click="form.impact = n">{{ n }}</button>
              </div>
            </div>
          </div>
          <div class="form-group full" v-if="form.likelihood && form.impact">
            <div class="risk-preview-score" :class="getRiskLevel(form.likelihood, form.impact)">
              Computed Risk Level: <strong>{{ getRiskLevel(form.likelihood, form.impact).toUpperCase() }}</strong>
              &nbsp;(Score: {{ form.likelihood * form.impact }})
            </div>
          </div>
          <div class="form-group full">
            <label>Proposed Mitigation</label>
            <textarea v-model="form.mitigation" rows="2" placeholder="How will this risk be mitigated?"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm = false">Cancel</button>
          <button class="btn-primary" @click="submitRisk">Log Risk</button>
        </div>
      </div>
    </div>

    <!-- Risk Detail Drawer -->
    <div class="drawer-overlay" v-if="activeRisk" @click.self="activeRisk = null">
      <div class="drawer">
        <div class="drawer-header" :class="activeRisk.level + '-border'">
          <div>
            <span class="mono ref-tag">{{ activeRisk.ref }}</span>
            <h2>{{ activeRisk.title }}</h2>
          </div>
          <button class="close-btn" @click="activeRisk = null">✕</button>
        </div>
        <div class="drawer-body">
          <div class="detail-grid">
            <div class="detail-item"><span class="detail-lbl">Level</span><span class="level-badge" :class="activeRisk.level">{{ activeRisk.level }}</span></div>
            <div class="detail-item"><span class="detail-lbl">Score</span><span class="detail-val">{{ activeRisk.likelihood * activeRisk.impact }} / 25</span></div>
            <div class="detail-item"><span class="detail-lbl">Site</span><span class="detail-val">{{ activeRisk.site }}</span></div>
            <div class="detail-item"><span class="detail-lbl">Category</span><span class="detail-val">{{ activeRisk.category }}</span></div>
            <div class="detail-item"><span class="detail-lbl">Owner</span><span class="detail-val">{{ activeRisk.owner }}</span></div>
            <div class="detail-item"><span class="detail-lbl">Status</span><span class="status-badge" :class="activeRisk.status">{{ activeRisk.status }}</span></div>
          </div>

          <div class="detail-section">
            <span class="detail-lbl">Description</span>
            <p class="detail-text">{{ activeRisk.description }}</p>
          </div>

          <div class="detail-section">
            <span class="detail-lbl">Mitigation Plan</span>
            <p class="detail-text">{{ activeRisk.mitigation || 'No mitigation plan defined yet.' }}</p>
          </div>

          <div class="ai-insight" v-if="activeRisk.aiInsight">
            <div class="ai-insight-header">
              <span>🤖</span>
              <span class="ai-insight-title">AI Prediction Insight</span>
            </div>
            <p class="ai-insight-text">{{ activeRisk.aiInsight }}</p>
            <div class="ai-confidence">
              <span class="mono">Confidence:</span>
              <div class="conf-bar">
                <div class="conf-fill" :style="{ width: activeRisk.aiConfidence + '%' }"></div>
              </div>
              <span class="mono">{{ activeRisk.aiConfidence }}%</span>
            </div>
          </div>

          <!-- Update Status -->
          <div class="status-update">
            <span class="detail-lbl">Update Status</span>
            <div class="status-options">
              <button v-for="s in ['open', 'mitigating', 'mitigated', 'accepted']" :key="s"
                :class="['status-opt', activeRisk.status === s ? 'active' : '', s]"
                @click="activeRisk.status = s">{{ s }}</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const showForm = ref(false)
const activeRisk = ref(null)
const filterLevel = ref('')
const filterSite = ref('')
const filterStatus = ref('')
const sortBy = ref('score')
const aiRunning = ref(false)
const aiProgress = ref(0)

const siteOptions = ['Nairobi Housing — Phase 1', 'Mombasa Infrastructure', 'Kisumu Commercial', 'Nakuru Road Project']

const form = ref({ title: '', category: '', site: '', owner: '', description: '', likelihood: 0, impact: 0, mitigation: '' })

const risks = ref([
  {
    id: 1, ref: 'RSK-2025-001',
    title: 'Foundation Subsidence — Block C',
    description: 'Soil investigation indicates potential subsidence risk in Block C due to high water table and inadequate compaction.',
    site: 'Nairobi Housing — Phase 1', category: 'Structural',
    owner: 'James Mutua', dateAdded: '2025-02-10',
    likelihood: 4, impact: 5, level: 'critical', status: 'mitigating',
    mitigation: 'Additional ground investigation commissioned. Raft foundation design under review.',
    aiPredicted: true, aiInsight: 'Based on EVM data showing schedule slippage (SPI: 0.78) and recent soil reports, subsidence risk has increased by 34% over the past 3 weeks.', aiConfidence: 88
  },
  {
    id: 2, ref: 'RSK-2025-002',
    title: 'Electrical Contractor Delay',
    description: 'Main electrical contractor has indicated supply chain issues with switchgear components, potentially delaying Level 3 works by 2–3 weeks.',
    site: 'Kisumu Commercial', category: 'Procurement',
    owner: 'Alice Wanjiku', dateAdded: '2025-02-12',
    likelihood: 4, impact: 4, level: 'high', status: 'open',
    mitigation: 'Alternative supplier being sourced. Contract variation order being prepared.',
    aiPredicted: true, aiInsight: 'Procurement delays of this type have historically caused 2.5× cost overruns in similar projects. Early intervention is recommended.', aiConfidence: 76
  },
  {
    id: 3, ref: 'RSK-2025-003',
    title: 'PPE Non-Compliance — Casual Workers',
    description: 'Casual laborers observed without proper PPE during peak hours. Risk of worker injury significantly elevated.',
    site: 'Mombasa Infrastructure', category: 'Worker Safety',
    owner: 'Grace Otieno', dateAdded: '2025-02-14',
    likelihood: 3, impact: 3, level: 'medium', status: 'mitigating',
    mitigation: 'Daily toolbox talks reinstated. PPE station added at site entrance. Random spot checks scheduled.',
    aiPredicted: false, aiInsight: null, aiConfidence: null
  },
  {
    id: 4, ref: 'RSK-2025-004',
    title: 'Budget Overrun — Materials Cost',
    description: 'Rising steel and cement prices may push project budget above planned value. CPI currently at 0.91.',
    site: 'Nairobi Housing — Phase 1', category: 'Financial',
    owner: 'Peter Kamau', dateAdded: '2025-02-08',
    likelihood: 4, impact: 5, level: 'critical', status: 'open',
    mitigation: 'Value engineering review initiated. Project owner notified of potential budget revision.',
    aiPredicted: true, aiInsight: 'EVM analysis shows CPI of 0.91 and SPI of 0.78. Estimate at Completion (EAC) projects a 12% cost overrun if current trends continue.', aiConfidence: 92
  },
  {
    id: 5, ref: 'RSK-2025-005',
    title: 'Dust Nuisance — Neighbouring Properties',
    description: 'Earthworks are generating significant dust affecting neighbouring properties. Community complaints received.',
    site: 'Nakuru Road Project', category: 'Environmental',
    owner: 'Grace Otieno', dateAdded: '2025-02-16',
    likelihood: 2, impact: 2, level: 'low', status: 'mitigated',
    mitigation: 'Water bowser deployed. Dust suppression schedule implemented. Barriers erected.',
    aiPredicted: false, aiInsight: null, aiConfidence: null
  },
])

const matrixCells = computed(() => {
  const cells = []
  for (let row = 5; row >= 1; row--) {
    for (let col = 1; col <= 5; col++) {
      const score = row * col
      let level = score >= 16 ? 'critical' : score >= 9 ? 'high' : score >= 4 ? 'medium' : 'low'
      cells.push({ row, col, level, label: score })
    }
  }
  return cells
})

function getRisksInCell(row, col) {
  return risks.value.filter(r => r.likelihood === col && r.impact === row)
}

const riskStats = computed(() => [
  { label: 'Total Risks', val: risks.value.length, cls: 'all' },
  { label: 'Critical', val: risks.value.filter(r => r.level === 'critical').length, cls: 'critical' },
  { label: 'High', val: risks.value.filter(r => r.level === 'high').length, cls: 'high' },
  { label: 'Open', val: risks.value.filter(r => r.status === 'open').length, cls: 'open' },
  { label: 'AI Predicted', val: risks.value.filter(r => r.aiPredicted).length, cls: 'ai' },
])

const filteredRisks = computed(() => {
  let list = risks.value.filter(r => {
    return (!filterLevel.value || r.level === filterLevel.value) &&
           (!filterSite.value  || r.site  === filterSite.value)  &&
           (!filterStatus.value|| r.status === filterStatus.value)
  })
  if (sortBy.value === 'score') list = [...list].sort((a, b) => (b.likelihood * b.impact) - (a.likelihood * a.impact))
  return list
})

function getRiskLevel(l, i) {
  const s = l * i
  return s >= 16 ? 'critical' : s >= 9 ? 'high' : s >= 4 ? 'medium' : 'low'
}

function viewRisk(r) { activeRisk.value = { ...r } }

function runAIPrediction() {
  aiRunning.value = true
  aiProgress.value = 0
  const interval = setInterval(() => {
    aiProgress.value += Math.random() * 15
    if (aiProgress.value >= 100) {
      aiProgress.value = 100
      clearInterval(interval)
      setTimeout(() => { aiRunning.value = false }, 800)
    }
  }, 200)
}

function submitRisk() {
  if (!form.value.title || !form.value.site || !form.value.likelihood || !form.value.impact) {
    alert('Please fill in all required fields including likelihood and impact.')
    return
  }
  const level = getRiskLevel(form.value.likelihood, form.value.impact)
  risks.value.unshift({
    id: risks.value.length + 1,
    ref: `RSK-2025-00${risks.value.length + 1}`,
    title: form.value.title, description: form.value.description,
    site: form.value.site, category: form.value.category,
    owner: form.value.owner || 'Unassigned',
    dateAdded: new Date().toISOString().split('T')[0],
    likelihood: form.value.likelihood, impact: form.value.impact,
    level, status: 'open', mitigation: form.value.mitigation,
    aiPredicted: false, aiInsight: null, aiConfidence: null
  })
  showForm.value = false
  form.value = { title: '', category: '', site: '', owner: '', description: '', likelihood: 0, impact: 0, mitigation: '' }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.risk-assessments {
  font-family: 'Syne', sans-serif;
  background: #0d0f14;
  color: #e8e4dc;
  min-height: 100vh;
  padding: 28px 32px;
}

.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.page-tag { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px; color: #f5a623; text-transform: uppercase; display: block; margin-bottom: 6px; }
h1 { font-size: 28px; font-weight: 800; color: #fff; }
.page-sub { font-size: 13px; color: #6b7280; margin-top: 4px; }
.header-actions { display: flex; gap: 10px; }

.btn-primary { background: #f5a623; color: #0d0f14; border: none; padding: 10px 20px; border-radius: 8px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; cursor: pointer; }
.btn-secondary { background: #1a1e2a; border: 1px solid #2a2f3e; color: #e8e4dc; padding: 10px 18px; border-radius: 8px; font-family: 'Syne', sans-serif; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 6px; }
.btn-secondary:hover { border-color: #f5a623; color: #f5a623; }
.btn-ghost { background: none; border: 1px solid #2a2f3e; color: #9ca3af; padding: 10px 20px; border-radius: 8px; font-family: 'Syne', sans-serif; font-size: 13px; cursor: pointer; }
.mono { font-family: 'DM Mono', monospace; }

/* AI Banner */
.ai-banner { background: #0a1520; border: 1px solid #1a3550; border-radius: 10px; padding: 14px 18px; margin-bottom: 20px; display: flex; align-items: center; gap: 12px; }
.ai-pulse { width: 10px; height: 10px; border-radius: 50%; background: #3b82f6; animation: pulse 1s infinite; flex-shrink: 0; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(1.4)} }
.ai-text { font-size: 12px; color: #60a5fa; flex: 1; }
.ai-progress { width: 120px; height: 4px; background: #1e2230; border-radius: 2px; overflow: hidden; }
.ai-fill { height: 100%; background: #3b82f6; border-radius: 2px; transition: width 0.2s ease; }

/* RISK MATRIX */
.matrix-section { background: #13161f; border: 1px solid #1e2230; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
.matrix-header { display: flex; align-items: baseline; gap: 12px; margin-bottom: 16px; }
.matrix-header h2 { font-size: 15px; font-weight: 700; }
.matrix-sub { font-size: 11px; color: #4b5563; font-family: 'DM Mono', monospace; }
.matrix-grid-wrap { display: flex; gap: 8px; align-items: flex-start; }
.matrix-y-label { display: flex; align-items: center; justify-content: center; width: 16px; font-family: 'DM Mono', monospace; font-size: 9px; color: #4b5563; letter-spacing: 2px; writing-mode: vertical-rl; transform: rotate(180deg); text-transform: uppercase; }
.matrix-content { flex: 1; }
.matrix-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 3px; margin-bottom: 4px; }
.matrix-cell { aspect-ratio: 1.5; border-radius: 4px; display: flex; align-items: flex-start; justify-content: flex-end; padding: 4px; position: relative; cursor: default; transition: opacity 0.2s; }
.matrix-cell:hover { opacity: 0.85; }
.matrix-cell.critical { background: rgba(220,38,38,0.3); border: 1px solid rgba(220,38,38,0.4); }
.matrix-cell.high     { background: rgba(239,68,68,0.2); border: 1px solid rgba(239,68,68,0.3); }
.matrix-cell.medium   { background: rgba(245,158,11,0.2); border: 1px solid rgba(245,158,11,0.25); }
.matrix-cell.low      { background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.2); }
.cell-label { font-family: 'DM Mono', monospace; font-size: 9px; color: rgba(255,255,255,0.3); }
.cell-dots { position: absolute; top: 4px; left: 4px; display: flex; flex-wrap: wrap; gap: 2px; }
.risk-dot { width: 8px; height: 8px; border-radius: 50%; background: #fff; opacity: 0.9; }
.matrix-x-labels { display: grid; grid-template-columns: repeat(5, 1fr); margin-top: 4px; }
.matrix-x-labels span { font-family: 'DM Mono', monospace; font-size: 9px; color: #4b5563; text-align: center; }
.matrix-x-title { text-align: center; font-family: 'DM Mono', monospace; font-size: 9px; color: #4b5563; letter-spacing: 2px; text-transform: uppercase; margin-top: 6px; }

/* STATS */
.risk-stats { display: flex; gap: 10px; margin-bottom: 20px; }
.risk-stat { background: #13161f; border: 1px solid #1e2230; border-radius: 8px; padding: 12px 18px; display: flex; flex-direction: column; align-items: center; gap: 4px; min-width: 90px; }
.rs-val { font-size: 28px; font-weight: 800; color: #fff; }
.rs-label { font-size: 10px; color: #6b7280; text-transform: uppercase; font-family: 'DM Mono', monospace; }
.risk-stat.critical { border-left: 3px solid #dc2626; }
.risk-stat.high     { border-left: 3px solid #ef4444; }
.risk-stat.open     { border-left: 3px solid #f59e0b; }
.risk-stat.ai       { border-left: 3px solid #3b82f6; }

/* FILTERS */
.filters-bar { display: flex; gap: 10px; align-items: center; margin-bottom: 20px; }
.filter-select { background: #13161f; border: 1px solid #1e2230; color: #e8e4dc; padding: 8px 12px; border-radius: 7px; font-family: 'Syne', sans-serif; font-size: 13px; cursor: pointer; }
.sort-control { display: flex; align-items: center; gap: 8px; margin-left: auto; }
.sort-control .mono { font-size: 11px; color: #4b5563; }

/* RISK CARDS */
.risk-list { display: flex; flex-direction: column; gap: 12px; }
.risk-card { background: #13161f; border: 1px solid #1e2230; border-radius: 12px; overflow: hidden; display: flex; cursor: pointer; transition: border-color 0.2s; }
.risk-card:hover { border-color: #2a2f3e; }
.risk-level-bar { width: 4px; flex-shrink: 0; }
.risk-level-bar.critical { background: #dc2626; }
.risk-level-bar.high     { background: #ef4444; }
.risk-level-bar.medium   { background: #f59e0b; }
.risk-level-bar.low      { background: #22c55e; }
.risk-body { flex: 1; padding: 16px 20px; }
.risk-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.risk-ref { font-size: 10px; color: #f5a623; display: block; margin-bottom: 2px; }
.risk-title { font-size: 15px; font-weight: 700; color: #fff; }
.risk-badges { display: flex; gap: 6px; align-items: center; flex-shrink: 0; }
.level-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }
.level-badge.critical { background: #2a0808; color: #dc2626; }
.level-badge.high     { background: #200e0e; color: #ef4444; }
.level-badge.medium   { background: #1f1a08; color: #f59e0b; }
.level-badge.low      { background: #0d2818; color: #22c55e; }
.status-badge { font-family: 'DM Mono', monospace; font-size: 9px; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }
.status-badge.open       { background: #200e0e; color: #ef4444; }
.status-badge.mitigating { background: #1f1a08; color: #f59e0b; }
.status-badge.mitigated  { background: #0d2818; color: #22c55e; }
.status-badge.accepted   { background: #1a1e2a; color: #6b7280; }
.ai-badge { background: #0d1a2e; color: #60a5fa; font-family: 'DM Mono', monospace; font-size: 9px; padding: 3px 8px; border-radius: 4px; }
.risk-desc { font-size: 12px; color: #6b7280; margin-bottom: 10px; line-height: 1.5; }
.risk-meta { display: flex; flex-wrap: wrap; gap: 12px; font-size: 11px; color: #4b5563; margin-bottom: 12px; }
.risk-scores { display: flex; gap: 24px; align-items: center; margin-bottom: 10px; }
.score-item { display: flex; align-items: center; gap: 8px; }
.score-lbl { font-size: 10px; color: #6b7280; }
.score-dots { display: flex; gap: 3px; }
.score-dot { width: 10px; height: 10px; border-radius: 50%; }
.score-dot.critical { background: #dc2626; }
.score-dot.high     { background: #ef4444; }
.score-dot.medium   { background: #f59e0b; }
.score-dot.low      { background: #22c55e; }
.score-dot.empty    { background: #1e2230; }
.score-num { font-family: 'DM Mono', monospace; font-size: 11px; color: #6b7280; }
.risk-score-total { display: flex; flex-direction: column; align-items: center; padding: 4px 12px; border-radius: 6px; margin-left: auto; }
.risk-score-total.critical { background: #2a0808; }
.risk-score-total.high     { background: #200e0e; }
.risk-score-total.medium   { background: #1f1a08; }
.risk-score-total.low      { background: #0d2818; }
.total-label { font-family: 'DM Mono', monospace; font-size: 9px; color: #4b5563; }
.total-val { font-size: 22px; font-weight: 800; }
.risk-score-total.critical .total-val { color: #dc2626; }
.risk-score-total.high .total-val     { color: #ef4444; }
.risk-score-total.medium .total-val   { color: #f59e0b; }
.risk-score-total.low .total-val      { color: #22c55e; }
.mitigation-preview { display: flex; gap: 6px; font-size: 11px; padding: 8px 10px; background: #0d0f14; border-radius: 6px; border: 1px solid #1a1e2a; }
.mit-label { color: #4b5563; flex-shrink: 0; }
.mit-text { color: #9ca3af; }

/* MODAL */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 100; display: flex; align-items: center; justify-content: center; }
.modal { background: #13161f; border: 1px solid #2a2f3e; border-radius: 16px; width: 680px; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 22px 28px; border-bottom: 1px solid #1e2230; }
.modal-header h2 { font-size: 18px; font-weight: 700; }
.close-btn { background: none; border: none; color: #6b7280; font-size: 18px; cursor: pointer; }
.modal-body { padding: 24px 28px; display: flex; flex-direction: column; gap: 16px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; padding: 18px 28px; border-top: 1px solid #1e2230; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group.full { grid-column: 1 / -1; }
.form-group label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; font-family: 'DM Mono', monospace; }
.form-group input, .form-group select, .form-group textarea { background: #0d0f14; border: 1px solid #1e2230; color: #e8e4dc; padding: 10px 12px; border-radius: 7px; font-family: 'Syne', sans-serif; font-size: 13px; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: #f5a623; }
.rating-input { display: flex; gap: 6px; }
.rating-btn { width: 36px; height: 36px; border-radius: 6px; border: 1px solid #2a2f3e; background: #0d0f14; color: #6b7280; font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; cursor: pointer; transition: all 0.15s; }
.rating-btn.active { background: #f5a623; border-color: #f5a623; color: #0d0f14; }
.risk-preview-score { padding: 10px 14px; border-radius: 8px; font-size: 13px; }
.risk-preview-score.critical { background: #2a0808; color: #dc2626; }
.risk-preview-score.high     { background: #200e0e; color: #ef4444; }
.risk-preview-score.medium   { background: #1f1a08; color: #f59e0b; }
.risk-preview-score.low      { background: #0d2818; color: #22c55e; }

/* DRAWER */
.drawer-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 100; display: flex; justify-content: flex-end; }
.drawer { background: #13161f; border-left: 1px solid #2a2f3e; width: 500px; height: 100%; overflow-y: auto; }
.drawer-header { padding: 24px; border-bottom: 1px solid #1e2230; display: flex; justify-content: space-between; align-items: flex-start; }
.drawer-header.critical-border { border-left: 4px solid #dc2626; }
.drawer-header.high-border     { border-left: 4px solid #ef4444; }
.drawer-header.medium-border   { border-left: 4px solid #f59e0b; }
.drawer-header.low-border      { border-left: 4px solid #22c55e; }
.ref-tag { font-family: 'DM Mono', monospace; font-size: 11px; color: #f5a623; display: block; margin-bottom: 4px; }
.drawer-header h2 { font-size: 16px; font-weight: 700; max-width: 380px; }
.drawer-body { padding: 24px; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }
.detail-item { display: flex; flex-direction: column; gap: 4px; }
.detail-lbl { font-size: 10px; color: #4b5563; text-transform: uppercase; letter-spacing: 0.5px; font-family: 'DM Mono', monospace; display: block; margin-bottom: 4px; }
.detail-val { font-size: 13px; color: #e8e4dc; }
.detail-section { margin-bottom: 18px; }
.detail-text { font-size: 13px; color: #9ca3af; line-height: 1.6; margin-top: 6px; }

.ai-insight { background: #070e1a; border: 1px solid #1a3550; border-radius: 10px; padding: 16px; margin-bottom: 20px; }
.ai-insight-header { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.ai-insight-title { font-size: 13px; font-weight: 700; color: #60a5fa; }
.ai-insight-text { font-size: 12px; color: #93c5fd; line-height: 1.6; margin-bottom: 12px; }
.ai-confidence { display: flex; align-items: center; gap: 8px; }
.ai-confidence .mono { font-size: 10px; color: #4b5563; }
.conf-bar { flex: 1; height: 4px; background: #1e2230; border-radius: 2px; overflow: hidden; }
.conf-fill { height: 100%; background: #3b82f6; border-radius: 2px; }

.status-update { margin-top: 16px; }
.status-options { display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap; }
.status-opt { padding: 6px 14px; border-radius: 6px; font-size: 11px; font-family: 'DM Mono', monospace; cursor: pointer; border: 1px solid #2a2f3e; background: none; color: #6b7280; text-transform: uppercase; }
.status-opt.open.active       { background: #200e0e; border-color: #ef4444; color: #ef4444; }
.status-opt.mitigating.active { background: #1f1a08; border-color: #f59e0b; color: #f59e0b; }
.status-opt.mitigated.active  { background: #0d2818; border-color: #22c55e; color: #22c55e; }
.status-opt.accepted.active   { background: #1a1e2a; border-color: #9ca3af; color: #9ca3af; }
</style>