# MASTER_QA_SUITE
# Project: MASTER_QA_SUITE
# File: task_prioritizer.py
# Purpose: The InnerCouncil's decision engine for task prioritization, governance, and project state management.
# Maintainer: DiegoMendezT / InnerCouncil
# Last updated: 2025-08-10 13:55 UTC
#
# This file is part of the Akashic Records. All changes must be attributed and timestamped.
#
# Agile Voice Attribution (Full Team):
# - Product Owner: Guides product vision and backlog priorities.
# - Scrum Master: Facilitates process, removes impediments, ensures agile adherence.
# - Development Team: Designers, developers, testers, and specialists responsible for delivery.
# - Stakeholders: Provide input and feedback on product direction and features.
# - Subject Matter Experts: Offer specialized technical or domain knowledge.
# - QA Voice: [Diego Alejandro] — Ensures quality, test coverage, and user advocacy.
# - Shadow QA: [Diego's Shadow] — Represents blindspots, risks, and unspoken challenges.
# - Teacher as Copilot, Gatekeeper as Copilot, Release Captain: AI/InnerCouncil voices for governance, traceability, and decision synthesis.
#
# All major decisions, changes, and logic evolutions must be attributed to one or more of these voices in docs/decision_log.md.
#
# Kintsugi Traceability: All major logic changes are snapshotted to tools/history/ before editing. See docs/decision_log.md for decision history.

from __future__ import annotations

import argparse
import datetime as dt
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

BACKLOG = Path("config/backlog.yml")
ROADMAP = Path("config/roadmap_phase2.yml")

# ---------- weights & knobs (safe defaults) ----------
DEFAULT_WEIGHTS = {"roi": 0.5, "complexity": -0.2, "learning": 0.3}
BONUSES = {
    "bonus_due_today": 0.2,   # add to score if due today
    "bonus_due_soon": 0.1,    # add if due within N days
    "soon_days": 3,
}
PENALTIES = {
    "penalty_blocked": -1.0,
    "penalty_has_open_deps": -0.5,
    "cooldown_days": 2,        # reduce score if very recently done
    "penalty_recently_done": -0.2,
}
TIEBREAK = ["roi", "learning", "effort_hrs"]  # descending except effort asc

# ---------- model ----------
@dataclass
class Task:
    id: str
    name: str
    roi: float = 0.0
    complexity: float = 0.0
    learning: float = 0.0
    effort_hrs: float = 0.0
    tags: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    due: Optional[str] = None        # "YYYY-MM-DD"
    status: str = "todo"
    recently_done: bool = False
    blocked: bool = False

    # populated later
    _explain: Dict[str, float] = field(default_factory=dict, repr=False)

# ---------- IO ----------
def _read_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

def _load_tasks() -> List[Task]:
    data = _read_yaml(BACKLOG)
    # accept both simple backlog and richer roadmap_phase2 (labels → tags)
    roadmap_data = _read_yaml(ROADMAP)

    tasks: List[Task] = []
    seen: set[str] = set()
    task_fields = {f.name for f in field(Task) if f.init}

    def add(raw: Dict[str, Any]):
        # normalize keys
        raw = {**raw}
        raw["id"] = raw.get("id") or raw.get("name")
        raw["tags"] = raw.get("tags") or raw.get("labels") or []
        raw["depends_on"] = raw.get("depends_on") or raw.get("deps") or []
        if raw["id"] in seen:
            return
        seen.add(raw["id"])
        
        # Filter out keys that are not in the Task dataclass
        filtered_raw = {k: v for k, v in raw.items() if k in task_fields}
        tasks.append(Task(**filtered_raw))

    for t in data.get("tasks", []):
        add(t)
    for t in roadmap_data.get("tasks", []):
        add(t)

    return tasks

# ---------- scoring ----------
def _due_bonus(today: dt.date, t: Task) -> float:
    if not t.due:
        return 0.0
    try:
        due = dt.date.fromisoformat(t.due)
    except (ValueError, TypeError):
        return 0.0
    if due == today:
        return BONUSES["bonus_due_today"]
    if 0 < (due - today).days <= BONUSES["soon_days"]:
        return BONUSES["bonus_due_soon"]
    return 0.0

def _penalties(t: Task, has_open_deps: bool) -> float:
    p = 0.0
    if t.blocked:
        p += PENALTIES["penalty_blocked"]
    if has_open_deps:
        p += PENALTIES["penalty_has_open_deps"]
    if t.recently_done:
        p += PENALTIES["penalty_recently_done"]
    return p

def _wsjf(t: Task) -> float:
    # WSJF ~ (Business Value + Time Criticality + Risk Reduction/Opportunity) / Job Size
    bv = t.roi
    tc = _due_bonus(dt.date.today(), t) * 10
    rr = t.learning
    size = max(t.effort_hrs, 1.0)
    return (bv + tc + rr) / size

def _rice(t: Task) -> float:
    # RICE ~ (Reach * Impact * Confidence) / Effort
    # map: roi->impact, learning->confidence (rough), effort_hrs->effort, reach from tag?
    reach = 1.0 + (0.2 if "course" in t.tags else 0.0)
    impact = t.roi
    confidence = 0.5 + min(max(t.learning / 10.0, 0), 0.5)
    effort = max(t.effort_hrs, 1.0)
    return (reach * impact * confidence) / effort

def _linear(t: Task, weights: Dict[str, float]) -> float:
    return (
        t.roi * weights["roi"]
        + t.complexity * weights["complexity"]
        + t.learning * weights["learning"]
    )

def _compute(
    t: Task, strategy: str, weights: Dict[str, float], open_deps: bool
) -> float:
    base = {
        "linear": _linear(t, weights),
        "wsjf": _wsjf(t),
        "rice": _rice(t),
    }.get(strategy, _linear(t, weights))

    bonus = _due_bonus(dt.date.today(), t)
    pen = _penalties(t, open_deps)
    score = base + bonus + pen
    t._explain = {"base": base, "bonus": bonus, "penalties": pen, "total": score}
    return score

# ---------- engine ----------
def prioritize(
    tasks: List[Task],
    strategy: str = "linear",
    weights: Dict[str, float] = DEFAULT_WEIGHTS,
    explain: bool = False,
    top: int = 5,
) -> List[Task]:
    id_index = {t.id: t for t in tasks}
    def has_open_deps(t: Task) -> bool:
        return any(id_index.get(dep, Task(id=dep, name=dep)).status != "done" for dep in t.depends_on)

    scored: List[tuple[float, Task]] = []
    for t in tasks:
        if t.status == "done":
            continue
        score = _compute(t, strategy, weights, has_open_deps(t))
        scored.append((score, t))

    # sort by score then tie-breakers
    def tie_key(it: tuple[float, Task]):
        score, t = it
        tb = []
        for k in TIEBREAK:
            v = getattr(t, k, 0.0)
            tb.append(-v if k != "effort_hrs" else v)  # smaller effort better
        return (-score, *tb)

    ordered = [t for _, t in sorted(scored, key=tie_key)]
    return ordered[:top] if top else ordered

# ---------- CLI ----------
def _parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--top", type=int, default=3)
    p.add_argument("--strategy", choices=["linear", "wsjf", "rice"], default="linear")
    p.add_argument("--weights", type=str, help='JSON like {"roi":0.5,"complexity":-0.2,"learning":0.3}')
    p.add_argument("--mark-done", dest="mark_done", type=str)
    p.add_argument("--explain", action="store_true")
    p.add_argument("--next-action", dest="next_action", action="store_true", help="Show the single most critical action to unblock the project.")
    return p.parse_args()

def _persist(tasks: List[Task]) -> None:
    # write back only into backlog.yml to keep roadmap intact
    task_list = []
    for t in tasks:
        task_dict = asdict(t)
        del task_dict['_explain'] # Don't save runtime data
        task_list.append(task_dict)
    BACKLOG.write_text(yaml.safe_dump({"tasks": task_list}, sort_keys=False), encoding="utf-8")

# --- EVOLUTION LOG: 2025-08-10 ---
# [Architect as Copilot] The Council's first decision introduced state-awareness.
# The system now understands not just "what's important" but "what's blocking us NOW."
# This function is the seed of the "Pathfinder" voice. Its logic will grow to become
# the core of the AI-Clocked Governance engine.
def get_next_gated_action(current_stage="CI_VERIFICATION"):
    """
    Determines the single most critical action to unblock the current project stage.
    This represents the voice of the Pathfinder.
    """
    if current_stage == "CI_VERIFICATION":
        return {
            "action": "Push hotfix to remote",
            "intent": "To validate the applied CI fix and get a GREEN pipeline.",
            "blocker": "Local changes not yet validated in the CI environment.",
            "next_stage": "RELEASE_TAGGING",
        }
    # Future stages (e.g., "RELEASE_TAGGING", "CLIENT_ONBOARDING") will be added here.
    return {"action": "No critical action defined for this stage.", "intent": "Observe and report."}

def main():
    args = _parse_args()
    tasks = _load_tasks()

    if args.next_action:
        # This is the new entry point for the Pathfinder voice
        action = get_next_gated_action() # In the future, stage will be determined automatically
        print("Pathfinder recommends the next critical action:")
        for key, value in action.items():
            print(f"- {key.capitalize()}: {value}")
        return

    if args.mark_done:
        found = False
        for t in tasks:
            if t.name == args.mark_done or t.id == args.mark_done:
                t.status = "done"
                t.recently_done = True
                found = True
                break
        _persist(tasks)
        print("Marked as done." if found else "Task not found.")
        return

    weights = DEFAULT_WEIGHTS
    if args.weights:
        weights = {**weights, **json.loads(args.weights)}

    ranked = prioritize(tasks, strategy=args.strategy, weights=weights, explain=args.explain, top=args.top)
    print("TaskPrioritizer recommends:")
    for i, t in enumerate(ranked, 1):
        line = f"{i}. {t.name} — score {t._explain.get('total', 0):.2f}"
        if args.explain:
            line += f" [base={t._explain['base']:.2f}, bonus={t._explain['bonus']:.2f}, pen={t._explain['penalties']:.2f}]"
        print(line)

if __name__ == "__main__":
    main()
