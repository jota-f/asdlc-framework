"""
A-SDLC Framework - Dashboard Generator
Gera um dashboard HTML interativo do projeto. Zero dependências externas.
"""

import json
import logging
import re
import webbrowser
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------------


@dataclass
class StoryData:
    ticket: str
    title: str
    status: str
    priority: str
    labels: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    date: Optional[str] = None
    tasks_total: int = 0
    tasks_done: int = 0
    has_tests: bool = False
    file_size: int = 0
    file_path: str = ""

    @property
    def progress(self) -> int:
        if self.tasks_total == 0:
            return 0
        return round(self.tasks_done / self.tasks_total * 100)


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


class DashboardParser:
    """Analisa as stories do projeto e extrai métricas."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.stories_dir = project_root / "stories"

    def parse_stories(self) -> List[StoryData]:
        if not self.stories_dir.exists():
            return []

        files = sorted(
            f
            for f in self.stories_dir.rglob("*.md")
            if f.name != "MEMORY.md" and "templates" not in f.parts and not f.name.endswith("template.md")
        )

        stories = []
        for f in files:
            story = self._parse_file(f)
            if story:
                stories.append(story)
        return stories

    def _parse_file(self, filepath: Path) -> Optional[StoryData]:
        try:
            content = filepath.read_text(encoding="utf-8")
            fm = self._parse_frontmatter(content)
            if not fm:
                return None

            ticket = fm.get("ticket", "")
            tasks_done = len(re.findall(r"- \[x\]", content, re.IGNORECASE))
            tasks_open = len(re.findall(r"- \[ \]", content))
            has_tests = bool(re.search(r"(critérios de aceitação|criteria|aceitação)", content, re.IGNORECASE))
            labels = re.findall(r'"([^"]+)"', fm.get("labels", "[]"))
            depends_on = re.findall(r'"([^"]+)"', fm.get("depends_on", "[]"))

            return StoryData(
                ticket=ticket,
                title=fm.get("title", filepath.stem),
                status=fm.get("status", "PENDENTE"),
                priority=fm.get("priority", "Medium"),
                labels=labels,
                depends_on=depends_on,
                date=self._extract_date(ticket),
                tasks_total=tasks_done + tasks_open,
                tasks_done=tasks_done,
                has_tests=has_tests,
                file_size=filepath.stat().st_size,
                file_path=str(filepath.relative_to(self.project_root)),
            )
        except Exception as e:
            logger.warning(f"Erro ao processar story {filepath}: {e}")
            return None

    @staticmethod
    def _parse_frontmatter(content: str) -> Optional[Dict[str, str]]:
        if not content.startswith("---"):
            return None
        parts = content.split("---", 2)
        if len(parts) < 3:
            return None
        fm: Dict[str, str] = {}
        for line in parts[1].strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                fm[key.strip()] = val.strip().strip('"').strip("'")
        return fm

    @staticmethod
    def _extract_date(ticket: str) -> Optional[str]:
        m = re.match(r"(\d{8})", ticket)
        if m:
            try:
                return datetime.strptime(m.group(1), "%Y%m%d").strftime("%Y-%m-%d")
            except ValueError:
                pass
        return None

    def calc_metrics(self, stories: List[StoryData]) -> Dict[str, Any]:
        total = len(stories)
        done = sum(1 for s in stories if s.status == "CONCLUÍDO")
        pending = sum(1 for s in stories if s.status == "PENDENTE")
        in_progress = total - done - pending
        tasks_total = sum(s.tasks_total for s in stories)
        tasks_done = sum(s.tasks_done for s in stories)
        with_tests = sum(1 for s in stories if s.has_tests)
        return {
            "total": total,
            "done": done,
            "pending": pending,
            "in_progress": in_progress,
            "progress_pct": round(done / total * 100) if total else 0,
            "tasks_total": tasks_total,
            "tasks_done": tasks_done,
            "tasks_pct": round(tasks_done / tasks_total * 100) if tasks_total else 0,
            "quality_pct": round(with_tests / total * 100) if total else 0,
        }

    def calc_burndown(self, stories: List[StoryData]) -> Dict[str, Any]:
        dated = [(s.date, s.status) for s in stories if s.date]
        if not dated:
            return {"labels": [], "remaining": [], "ideal": []}
        dated.sort(key=lambda x: x[0])
        all_dates = sorted({d for d, _ in dated})
        total = len(stories)
        done_by_date: Dict[str, int] = {}
        for date, status in dated:
            if status == "CONCLUÍDO":
                done_by_date[date] = done_by_date.get(date, 0) + 1
        labels, remaining = [], []
        cumulative = 0
        for date in all_dates:
            cumulative += done_by_date.get(date, 0)
            labels.append(date)
            remaining.append(total - cumulative)
        n = len(labels)
        ideal = [round(total * (1 - i / max(n - 1, 1))) for i in range(n)]
        return {"labels": labels, "remaining": remaining, "ideal": ideal}

    def calc_velocity(self, stories: List[StoryData], weeks: int = 8) -> Dict[str, Any]:
        """Fase 2: stories concluídas por semana (últimas N semanas)."""
        from datetime import timedelta

        today = datetime.today().date()
        labels, counts = [], []
        for i in range(weeks - 1, -1, -1):
            week_start = today - timedelta(days=today.weekday() + 7 * i)
            week_end = week_start + timedelta(days=6)
            label = week_start.strftime("%d/%m")
            count = sum(
                1
                for s in stories
                if s.status == "CONCLUÍDO"
                and s.date
                and week_start.strftime("%Y-%m-%d") <= s.date <= week_end.strftime("%Y-%m-%d")
            )
            labels.append(label)
            counts.append(count)
        return {"labels": labels, "counts": counts}

    def calc_blocked(self, stories: List[StoryData]) -> List[Dict[str, str]]:
        """Fase 3: stories bloqueadas por dependências não concluídas."""
        done_tickets = {s.ticket for s in stories if s.status == "CONCLUÍDO"}
        blocked = []
        for s in stories:
            if s.status == "CONCLUÍDO":
                continue
            missing = [d for d in s.depends_on if d not in done_tickets]
            if missing:
                blocked.append({"title": s.title, "ticket": s.ticket, "missing": ", ".join(missing)})
        return blocked

    def calc_no_criteria(self, stories: List[StoryData]) -> List[str]:
        """Fase 3: stories sem critérios de aceitação."""
        return [s.title for s in stories if not s.has_tests and s.status != "CONCLUÍDO"]


# ---------------------------------------------------------------------------
# HTML Renderer
# ---------------------------------------------------------------------------


class DashboardRenderer:
    """Gera o HTML completo do dashboard."""

    def render_html(
        self,
        project_name: str,
        metrics: Dict[str, Any],
        stories: List[StoryData],
        burndown: Dict[str, Any],
        velocity: Optional[Dict[str, Any]] = None,
        blocked: Optional[List[Dict[str, str]]] = None,
        no_criteria: Optional[List[str]] = None,
    ) -> str:
        velocity = velocity or {"labels": [], "counts": []}
        blocked = blocked or []
        no_criteria = no_criteria or []
        generated_at = datetime.now().strftime("%d/%m/%Y %H:%M")
        stories_json = json.dumps([asdict(s) for s in stories], default=str, ensure_ascii=False)
        metrics_json = json.dumps(metrics, ensure_ascii=False)
        burndown_json = json.dumps(burndown, ensure_ascii=False)
        velocity_json = json.dumps(velocity, ensure_ascii=False)
        # Build alerts HTML server-side
        alerts_html = ""
        for b in blocked:
            alerts_html += f'<div class="alert-item alert-red">🔒 <strong>{b["title"]}</strong> — bloqueada por: <code>{b["missing"]}</code></div>\n'
        for nc in no_criteria:
            alerts_html += f'<div class="alert-item alert-yellow">⚠️ <strong>{nc}</strong> — sem critérios de aceitação</div>\n'
        if not alerts_html:
            alerts_html = '<div class="alert-item alert-green">✅ Nenhum problema detectado</div>'
        alerts_count = len(blocked) + len(no_criteria)

        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>A-SDLC Dashboard — {project_name}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --bg:       #0d1117;
    --surface:  rgba(22,27,34,0.85);
    --border:   rgba(255,255,255,0.08);
    --blue:     #58a6ff;
    --green:    #3fb950;
    --yellow:   #d29922;
    --red:      #f85149;
    --purple:   #bc8cff;
    --text:     #e6edf3;
    --muted:    #7d8590;
    --radius:   14px;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    min-height: 100vh;
  }}

  /* ── Header ─────────────────────────────── */
  header {{
    background: linear-gradient(135deg, #0d1117 0%, #161b22 40%, #1a1f2e 100%);
    border-bottom: 1px solid var(--border);
    padding: 28px 40px 24px;
    display: flex; align-items: center; justify-content: space-between;
    position: relative; overflow: hidden;
  }}
  header::before {{
    content: "";
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 60% 80% at 80% 50%, rgba(88,166,255,0.08) 0%, transparent 70%);
    pointer-events: none;
  }}
  .header-left h1 {{
    font-size: 1.6rem; font-weight: 700; letter-spacing: -0.5px;
    background: linear-gradient(90deg, var(--blue), var(--purple));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }}
  .header-left p {{ color: var(--muted); font-size: 0.85rem; margin-top: 4px; }}
  .badge {{
    background: rgba(88,166,255,0.15); border: 1px solid rgba(88,166,255,0.3);
    color: var(--blue); padding: 6px 14px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 600; letter-spacing: 0.5px;
  }}

  /* ── Layout ─────────────────────────────── */
  main {{ padding: 32px 40px; max-width: 1400px; margin: 0 auto; }}

  /* ── KPI Cards ──────────────────────────── */
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px; margin-bottom: 32px;
  }}
  .kpi-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 22px 24px;
    backdrop-filter: blur(12px);
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative; overflow: hidden;
  }}
  .kpi-card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 32px rgba(0,0,0,0.4); }}
  .kpi-card::before {{
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: var(--accent, var(--blue));
  }}
  .kpi-label {{ color: var(--muted); font-size: 0.78rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 10px; }}
  .kpi-value {{ font-size: 2.4rem; font-weight: 800; line-height: 1;
    color: var(--accent, var(--blue)); }}
  .kpi-sub {{ color: var(--muted); font-size: 0.82rem; margin-top: 6px; }}

  /* ── Section Headers ─────────────────────── */
  .section-title {{
    font-size: 1rem; font-weight: 600; color: var(--text);
    margin-bottom: 16px; display: flex; align-items: center; gap: 8px;
  }}
  .section-title::after {{
    content: ""; flex: 1; height: 1px; background: var(--border);
  }}

  /* ── Two-column grid ─────────────────────── */
  .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 32px; }}
  @media (max-width: 900px) {{ .two-col {{ grid-template-columns: 1fr; }} }}

  .chart-card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 24px;
    backdrop-filter: blur(12px);
  }}

  /* ── Kanban ──────────────────────────────── */
  .kanban {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 32px; }}
  @media (max-width: 768px) {{ .kanban {{ grid-template-columns: 1fr; }} }}
  .kanban-col {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 16px;
    backdrop-filter: blur(12px);
  }}
  .kanban-header {{
    font-size: 0.82rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.8px; margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
  }}
  .kanban-header .dot {{ width: 8px; height: 8px; border-radius: 50%; }}
  .story-card {{
    background: rgba(255,255,255,0.04); border: 1px solid var(--border);
    border-radius: 10px; padding: 12px 14px; margin-bottom: 10px;
    transition: transform 0.15s, box-shadow 0.15s; cursor: default;
  }}
  .story-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.3); }}
  .story-card-title {{ font-size: 0.85rem; font-weight: 500; color: var(--text);
    margin-bottom: 8px; line-height: 1.4; }}
  .story-card-meta {{ display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }}
  .pill {{
    padding: 2px 8px; border-radius: 20px; font-size: 0.7rem; font-weight: 600;
  }}
  .pill-high   {{ background: rgba(248,81,73,0.15); color: var(--red); border: 1px solid rgba(248,81,73,0.3); }}
  .pill-medium {{ background: rgba(210,153,34,0.15); color: var(--yellow); border: 1px solid rgba(210,153,34,0.3); }}
  .pill-low    {{ background: rgba(63,185,80,0.15); color: var(--green); border: 1px solid rgba(63,185,80,0.3); }}
  .pill-label  {{ background: rgba(188,140,255,0.12); color: var(--purple); border: 1px solid rgba(188,140,255,0.2); }}
  .progress-bar-wrap {{
    background: rgba(255,255,255,0.06); border-radius: 99px;
    height: 4px; margin-top: 8px; overflow: hidden;
  }}
  .progress-bar-fill {{
    height: 100%; border-radius: 99px;
    background: linear-gradient(90deg, var(--blue), var(--purple));
    transition: width 1s ease;
  }}

  /* ── Alerts ──────────────────────────────── */
  .alerts-panel {{ display: flex; flex-direction: column; gap: 8px; }}
  .alert-item {{
    padding: 10px 16px; border-radius: 8px; font-size: 0.85rem; line-height: 1.5;
  }}
  .alert-red    {{ background: rgba(248,81,73,0.1); border: 1px solid rgba(248,81,73,0.25); color: #ffa198; }}
  .alert-yellow {{ background: rgba(210,153,34,0.1); border: 1px solid rgba(210,153,34,0.25); color: #e3b341; }}
  .alert-green  {{ background: rgba(63,185,80,0.1); border: 1px solid rgba(63,185,80,0.25); color: #56d364; }}
  .alert-item code {{ background: rgba(255,255,255,0.1); padding: 1px 5px; border-radius: 4px; font-size: 0.8rem; }}

  /* ── Footer ──────────────────────────────── */
  footer {{
    text-align: center; color: var(--muted); font-size: 0.78rem;
    padding: 24px 0 40px; border-top: 1px solid var(--border); margin-top: 8px;
  }}
</style>
</head>
<body>

<header>
  <div class="header-left">
    <h1>⚡ A-SDLC Dashboard</h1>
    <p>Projeto: <strong style="color:var(--text)">{project_name}</strong> · Gerado em {generated_at}</p>
  </div>
  <span class="badge">🤖 A-SDLC Framework</span>
</header>

<main>

  <!-- KPI Cards -->
  <div class="kpi-grid" id="kpi-grid">
    <div class="kpi-card" style="--accent:var(--blue)">
      <div class="kpi-label">Total de Stories</div>
      <div class="kpi-value" data-target="{metrics['total']}">0</div>
      <div class="kpi-sub">{metrics['done']} concluídas · {metrics['pending']} pendentes</div>
    </div>
    <div class="kpi-card" style="--accent:var(--green)">
      <div class="kpi-label">Progresso Geral</div>
      <div class="kpi-value" data-target="{metrics['progress_pct']}" data-suffix="%">0%</div>
      <div class="kpi-sub">{metrics['tasks_done']} de {metrics['tasks_total']} tarefas</div>
    </div>
    <div class="kpi-card" style="--accent:var(--purple)">
      <div class="kpi-label">Tasks Concluídas</div>
      <div class="kpi-value" data-target="{metrics['tasks_pct']}" data-suffix="%">0%</div>
      <div class="kpi-sub">{metrics['tasks_done']} checkboxes marcados</div>
    </div>
    <div class="kpi-card" style="--accent:var(--yellow)">
      <div class="kpi-label">Conformidade A-SDLC</div>
      <div class="kpi-value" data-target="{metrics['quality_pct']}" data-suffix="%">0%</div>
      <div class="kpi-sub">stories com critérios de aceitação</div>
    </div>
  </div>

  <!-- Charts row 1: Burndown + Status -->
  <div class="two-col">
    <div class="chart-card">
      <div class="section-title">📉 Burndown Chart</div>
      <canvas id="burndownChart" height="200"></canvas>
    </div>
    <div class="chart-card">
      <div class="section-title">🍩 Status das Stories</div>
      <canvas id="statusChart" height="200"></canvas>
    </div>
  </div>

  <!-- Charts row 2: Velocity -->
  <div class="chart-card" style="margin-bottom:32px">
    <div class="section-title">⚡ Velocity — Stories Concluídas por Semana</div>
    <canvas id="velocityChart" height="100"></canvas>
  </div>

  <!-- Alerts panel -->
  <div class="section-title" style="margin-bottom:16px">🚨 Alertas ({alerts_count})</div>
  <div class="alerts-panel" style="margin-bottom:32px">
    {alerts_html}
  </div>

  <!-- Kanban Board -->
  <div class="section-title" style="margin-bottom:16px">📋 Story Board</div>
  <div class="kanban" id="kanban-board"></div>

</main>

<footer>
  A-SDLC Framework · Dashboard gerado automaticamente · {generated_at}
</footer>

<script>
const STORIES  = {stories_json};
const METRICS  = {metrics_json};
const BURNDOWN = {burndown_json};
const VELOCITY = {velocity_json};

// ── Animated counters ────────────────────────────────────────────────────────
document.querySelectorAll('.kpi-value[data-target]').forEach(el => {{
  const target = parseInt(el.dataset.target, 10);
  const suffix = el.dataset.suffix || '';
  let start = null;
  const duration = 900;
  function step(ts) {{
    if (!start) start = ts;
    const p = Math.min((ts - start) / duration, 1);
    const ease = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(ease * target) + suffix;
    if (p < 1) requestAnimationFrame(step);
  }}
  requestAnimationFrame(step);
}});

// ── Burndown Chart ────────────────────────────────────────────────────────────
if (BURNDOWN.labels.length > 0) {{
  new Chart(document.getElementById('burndownChart'), {{
    type: 'line',
    data: {{
      labels: BURNDOWN.labels,
      datasets: [
        {{
          label: 'Real',
          data: BURNDOWN.remaining,
          borderColor: '#58a6ff',
          backgroundColor: 'rgba(88,166,255,0.1)',
          fill: true, tension: 0.4, pointRadius: 4,
        }},
        {{
          label: 'Ideal',
          data: BURNDOWN.ideal,
          borderColor: 'rgba(63,185,80,0.5)',
          borderDash: [6, 4], pointRadius: 0,
          fill: false, tension: 0,
        }},
      ],
    }},
    options: {{
      responsive: true,
      plugins: {{ legend: {{ labels: {{ color: '#e6edf3', font: {{ size: 12 }} }} }} }},
      scales: {{
        x: {{ ticks: {{ color: '#7d8590', maxTicksLimit: 6 }}, grid: {{ color: 'rgba(255,255,255,0.05)' }} }},
        y: {{ ticks: {{ color: '#7d8590' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }}, beginAtZero: true }},
      }},
    }},
  }});
}} else {{
  document.getElementById('burndownChart').closest('.chart-card').innerHTML =
    '<div class="section-title">📉 Burndown Chart</div><p style="color:var(--muted);font-size:0.85rem;padding-top:8px">Dados insuficientes — adicione datas nas stories.</p>';
}}

// ── Status Donut ──────────────────────────────────────────────────────────────
new Chart(document.getElementById('statusChart'), {{
  type: 'doughnut',
  data: {{
    labels: ['Concluído', 'Pendente', 'Em Progresso'],
    datasets: [{{
      data: [METRICS.done, METRICS.pending, METRICS.in_progress],
      backgroundColor: ['#3fb950', '#58a6ff', '#d29922'],
      borderColor: '#0d1117', borderWidth: 3,
    }}],
  }},
  options: {{
    responsive: true, cutout: '65%',
    plugins: {{
      legend: {{ position: 'bottom', labels: {{ color: '#e6edf3', padding: 16, font: {{ size: 12 }} }} }},
    }},
  }},
}});

// ── Velocity Chart ───────────────────────────────────────────────────────────
new Chart(document.getElementById('velocityChart'), {{
  type: 'bar',
  data: {{
    labels: VELOCITY.labels,
    datasets: [{{
      label: 'Stories concluídas',
      data: VELOCITY.counts,
      backgroundColor: 'rgba(88,166,255,0.5)',
      borderColor: '#58a6ff',
      borderWidth: 1,
      borderRadius: 6,
    }}],
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      x: {{ ticks: {{ color: '#7d8590' }}, grid: {{ color: 'rgba(255,255,255,0.04)' }} }},
      y: {{ ticks: {{ color: '#7d8590', stepSize: 1 }}, grid: {{ color: 'rgba(255,255,255,0.04)' }}, beginAtZero: true }},
    }},
  }},
}});

// ── Kanban Board ──────────────────────────────────────────────────────────────
const COLS = [
  {{ key: 'CONCLUÍDO',  label: 'Concluído',    color: '#3fb950' }},
  {{ key: 'PENDENTE',   label: 'Pendente',      color: '#58a6ff' }},
  {{ key: 'other',      label: 'Em Progresso',  color: '#d29922' }},
];

function pillPriority(p) {{
  const cls = p === 'High' ? 'pill-high' : p === 'Low' ? 'pill-low' : 'pill-medium';
  return `<span class="pill ${{cls}}">${{p || 'Medium'}}</span>`;
}}

const board = document.getElementById('kanban-board');
COLS.forEach(col => {{
  const stories = STORIES.filter(s =>
    col.key === 'other' ? (s.status !== 'CONCLUÍDO' && s.status !== 'PENDENTE') : s.status === col.key
  );
  const cards = stories.map(s => {{
    const pct = s.tasks_total > 0 ? Math.round(s.tasks_done / s.tasks_total * 100) : 0;
    const labels = (s.labels || []).map(l => `<span class="pill pill-label">${{l}}</span>`).join('');
    return `
      <div class="story-card">
        <div class="story-card-title">${{s.title}}</div>
        <div class="story-card-meta">
          ${{pillPriority(s.priority)}}
          ${{labels}}
          ${{s.has_tests ? '<span class="pill pill-label">✓ testes</span>' : ''}}
        </div>
        ${{s.tasks_total > 0 ? `
          <div style="display:flex;justify-content:space-between;margin-top:8px">
            <span style="font-size:0.72rem;color:var(--muted)">${{s.tasks_done}}/${{s.tasks_total}} tasks</span>
            <span style="font-size:0.72rem;color:var(--muted)">${{pct}}%</span>
          </div>
          <div class="progress-bar-wrap">
            <div class="progress-bar-fill" style="width:${{pct}}%"></div>
          </div>` : ''}}
      </div>`;
  }}).join('');

  board.innerHTML += `
    <div class="kanban-col">
      <div class="kanban-header">
        <div class="dot" style="background:${{col.color}}"></div>
        ${{col.label}}
        <span style="margin-left:auto;background:rgba(255,255,255,0.07);border-radius:99px;
          padding:1px 8px;font-size:0.72rem;color:var(--muted)">${{stories.length}}</span>
      </div>
      ${{cards || '<p style="color:var(--muted);font-size:0.82rem">Nenhuma story</p>'}}
    </div>`;
}});
</script>
</body>
</html>"""

    def write_and_open(
        self,
        html: str,
        output_path: Path,
        auto_open: bool = True,
    ) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        logger.info(f"Dashboard gerado em: {output_path}")
        if auto_open:
            webbrowser.open(output_path.as_uri())
        return output_path


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------


def generate_dashboard(
    project_root: Path,
    output_path: Optional[Path] = None,
    auto_open: bool = True,
) -> Path:
    """Gera o dashboard HTML e (opcionalmente) abre no browser."""
    if output_path is None:
        output_path = project_root / ".asdlc" / "dashboard" / "dashboard.html"

    parser = DashboardParser(project_root)
    stories = parser.parse_stories()
    metrics = parser.calc_metrics(stories)
    burndown = parser.calc_burndown(stories)
    velocity = parser.calc_velocity(stories)
    blocked = parser.calc_blocked(stories)
    no_criteria = parser.calc_no_criteria(stories)

    project_name = project_root.name

    renderer = DashboardRenderer()
    html = renderer.render_html(
        project_name,
        metrics,
        stories,
        burndown,
        velocity=velocity,
        blocked=blocked,
        no_criteria=no_criteria,
    )
    return renderer.write_and_open(html, output_path, auto_open)
