#!/usr/bin/env python3
"""Apply the method-centered Agent testing review taxonomy.

The title sets are intentionally explicit: classification is a review decision, not a
keyword heuristic. Re-running this script is idempotent and keeps unknown future rows
in the background tier until they are screened.
"""

from __future__ import annotations

import csv
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "research/evidence/evidence-table.csv"
SCREENING = ROOT / "research/evidence/screening-log.csv"


CORE_5 = {
    "Testing and Understanding Erroneous Planning in LLM Agents through Synthesized User Inputs",
    "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents",
    "AI Agents That Matter",
    "Breaking Agents: Compromising Autonomous LLM Agents Through Malfunction Amplification",
    "ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities",
    "Agent-as-a-Judge: Evaluate Agents with Agents",
    "AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents",
    "AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Trajectories",
    "Agent-Testing Agent: A Meta-Agent for Automated Testing and Evaluation of Conversational AI Agents",
    "SIRAJ: Diverse and Efficient Red-Teaming for LLM Agents via Distilled Structured Reasoning",
    "VeriGrey: Greybox Agent Validation",
    "FLARE: Agentic Coverage-Guided Fuzzing for LLM-Based Multi-Agent Systems",
    "LogicHunter: Testing LLM Agent Frameworks with an Agentic Oracle",
    "ReliabilityBench: Evaluating LLM Agent Reliability Under Production-Like Stress Conditions",
    "Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents",
    "Process Evaluation for Agentic Systems",
    "Who Tests the Testers? Systematic Enumeration and Coverage Audit of LLM Agent Tool Call Safety",
    "MUZZLE: Adaptive Agentic Red-Teaming of Web Agents Against Indirect Prompt Injection Attacks",
    "MATE: Policy-Aware Security Auditing for Mobile Agents via Synthesis-Driven Trajectory Learning",
    "AgentChaos: Chaos Engineering for Agent Systems via Programmatic Fault Injection",
    "OrchestraBench: Evaluating Multi-Agent Orchestration Failure Modes, Recovery, and Decomposition Quality",
    "MAS-FIRE: Fault Injection and Reliability Evaluation for LLM-Based Multi-Agent Systems",
    "AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents",
    "REFLECT: Intervention-Supported Error Attribution for Silent Failures in LLM Agent Traces",
    "AgentTelemetry: A Fault Detection Benchmark and Toolkit for LLM Agent Observability",
    "Observability and Fault Injection for LLM-Based Multi-Agent Systems in Software Engineering",
    "AgentTrace: Causal Graph Tracing for Root Cause Analysis in Deployed Multi-Agent Systems",
    "FALAT: Tracing Failures in LLM Agent Trajectories via Dependency-Guided Search",
    "Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures",
    "Agentic CLEAR: Automating Multi-Level Evaluation of LLM Agents",
    "AgentDiagnose: An Open Toolkit for Diagnosing LLM Agent Trajectories",
}

CORE_4 = {
    "AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents",
    "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains",
    "AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents",
    "Why Do Multi-Agent LLM Systems Fail?",
    "AgentLens: Production-Assessed Trajectory Reviews for Coding Agent Evaluation",
    "AJ-Bench: Benchmarking Agent-as-a-Judge for Environment-Aware Evaluation",
    "Who Broke the System? Failure Localization in LLM-Based Multi-Agent Systems",
    "VerifyMAS: Hypothesis Verification for Failure Attribution in LLM Multi-Agent Systems",
    "StepFinder: A Temporal Semantic Framework for Failure Attribution in Multi-Agent Systems",
    "Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-based Multi-Agent Systems",
    "Aligning Agents via Planning: A Benchmark for Trajectory-Level Reward Modeling",
}

SUPPORTING = {
    "WebArena: A Realistic Web Environment for Building Autonomous Agents",
    "AgentBench: Evaluating LLMs as Agents",
    "Identifying the Risks of LM Agents with an LM-Emulated Sandbox",
    "Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models",
    "VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks",
    "InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents",
    "StableToolBench: Towards Stable Large-Scale Benchmarking on Tool Learning of Large Language Models",
    "OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments",
    "AndroidWorld: A Dynamic Benchmarking Environment for Autonomous Agents",
    "WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge Work Tasks",
    "AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases",
    "BadRobot: Jailbreaking Embodied LLM Agents in the Physical World",
    "Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents",
    "AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents",
    "The BrowserGym Ecosystem for Web Agent Research",
    "SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents",
    "Agent-SafetyBench: Evaluating the Safety of LLM Agents",
    "Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents",
    "MultiAgentBench: Evaluating the Collaboration and Competition of LLM agents",
    "Les Dissonances: Cross-Tool Harvesting and Polluting in Pool-of-Tools Empowered LLM Agents",
    "Gaia2: Benchmarking LLM Agents on Dynamic and Asynchronous Environments",
    "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions",
    "Mem2ActBench: A Benchmark for Evaluating Long-Term Memory Utilization in Task-Oriented Autonomous Agents",
    "LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues",
    "Collab-Overcooked: Benchmarking and Evaluating Large Language Models as Collaborative Agents",
    "LLM-Coordination: Evaluating and Analyzing Multi-agent Coordination Abilities in Large Language Models",
    "SILO-BENCH: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems",
    "ETOM: A Five-Level Benchmark for Evaluating Tool Orchestration within the MCP Ecosystem",
    "MASEval: Extending Multi-Agent Evaluation from Models to Systems",
    "Benchmarking LLM Judges for Mobile Agent Evaluation",
    "YC-Bench: Benchmarking AI Agents for Long-Term Planning and Consistent Execution",
    "MAGPIE: A Benchmark for Multi-Agent Contextual Privacy Evaluation",
    "AgentCollabBench: Benchmarking Process-Level Failures in Multi-Agent LLM Systems",
    "Adaptive Adversaries: A Multi-Turn, Multi-LLM Benchmark for LLM Agent Security",
    "STATE-Bench: Stateful Task Agent Evaluation Benchmark",
    "AgentLAB: Benchmarking LLM Agents against Long-Horizon Attacks",
    "Can LLM Agents Stick to the Script? A Benchmark for Long-Horizon Consistency in Interactive Narratives",
}


NEW_EVIDENCE = [
    {
        "title": "Agentic CLEAR: Automating Multi-Level Evaluation of LLM Agents",
        "authors": "Asaf Yehudai; Lilach Eden; Michal Shmueli-Scheuer",
        "year": "2026",
        "venue": "ACL System Demonstrations",
        "doi": "10.18653/v1/2026.acl-demo.74",
        "arxiv_id": "",
        "publication_type": "conference system demonstration",
        "version_status": "ACL 2026 formal open-access version",
        "agent_type": "general LLM agents",
        "research_problem": "Automatically diagnose agent behavior at system, trace, and node granularity",
        "testing_method": "dynamic rubric generation; node/trace scoring; cross-trace issue aggregation",
        "metrics": "macro-F1; micro-F1; AUC for task-success prediction",
        "benchmark_or_dataset": "AppWorld; GAIA; SWE-bench Verified Mini; tau-bench",
        "main_findings": "Across the evaluated settings, multi-level diagnostics align with annotated errors and can predict task success, but performance varies by benchmark and agent architecture.",
        "limitations": "LLM-judge dependence, incomplete benchmark-internal metadata, and variable cross-setting performance limit use as a standalone oracle.",
        "code_url": "https://ibm.biz/ACLEAR-Code",
        "paper_url": "https://aclanthology.org/2026.acl-demo.74/",
        "relevance_score": "5",
        "evidence_level": "已阅读全文",
        "full_text_read": "yes",
        "crossref_status": "exact DOI/title verified",
        "openalex_status": "exact DOI/title verified",
        "inclusion_status": "included",
        "notes_file": "research/notes/2026-Yehudai-AgenticCLEAR.md",
        "review_tier": "core-method",
    },
    {
        "title": "AgentDiagnose: An Open Toolkit for Diagnosing LLM Agent Trajectories",
        "authors": "Tianyue Ou; Wanyao Guo; Apurva Gandhi; Graham Neubig; Xiang Yue",
        "year": "2025",
        "venue": "EMNLP System Demonstrations",
        "doi": "10.18653/v1/2025.emnlp-demos.15",
        "arxiv_id": "",
        "publication_type": "conference system demonstration",
        "version_status": "EMNLP 2025 formal open-access version",
        "agent_type": "general and web agents",
        "research_problem": "Expose trajectory quality beyond final success or failure",
        "testing_method": "five extensible trajectory evaluators plus semantic and state-transition visualization",
        "metrics": "Pearson r; Spearman rho; Kendall tau; downstream WebArena success",
        "benchmark_or_dataset": "NNetNav-Live; WebArena",
        "main_findings": "The evaluators positively correlate with human ratings and can filter a smaller training subset, but agreement differs substantially by trajectory property.",
        "limitations": "Human validation uses only 30 trajectories; evaluator prompts and reasoning traces may not generalize to other domains or hidden-reasoning agents.",
        "code_url": "https://github.com/oootttyyy/AgentDiagnose",
        "paper_url": "https://aclanthology.org/2025.emnlp-demos.15/",
        "relevance_score": "5",
        "evidence_level": "已阅读全文",
        "full_text_read": "yes",
        "crossref_status": "exact DOI/title verified",
        "openalex_status": "exact DOI/title verified; author-name variants noted",
        "inclusion_status": "included",
        "notes_file": "research/notes/2025-Ou-AgentDiagnose.md",
        "review_tier": "core-method",
    },
    {
        "title": "Aligning Agents via Planning: A Benchmark for Trajectory-Level Reward Modeling",
        "authors": "Jiaxuan Wang; Yulan Hu; Wenjin Yang; Zheng Pan; Xin Li; Lan-Zhe Guo",
        "year": "2026",
        "venue": "ACL",
        "doi": "10.18653/v1/2026.acl-long.1062",
        "arxiv_id": "",
        "publication_type": "conference paper",
        "version_status": "ACL 2026 formal open-access version",
        "agent_type": "tool-using agents and trajectory evaluators",
        "research_problem": "Meta-evaluate reward models and LLM judges on long-horizon agent trajectories",
        "testing_method": "pairwise trajectory preference benchmark with natural rollouts and controlled hard-negative perturbations",
        "metrics": "pairwise accuracy; macro-accuracy; human agreement; order-swap consistency",
        "benchmark_or_dataset": "Plan-RewardBench",
        "main_findings": "Evaluator families degrade on long trajectories and show complementary strengths across planning, recovery, tool relevance, and safety scenarios.",
        "limitations": "The release is text-only, task-family balance is uneven, and most labels are produced by a model panel with a stratified human audit rather than exhaustive human labeling.",
        "code_url": "https://github.com/wyy-1112/Plan-RewardBench",
        "paper_url": "https://aclanthology.org/2026.acl-long.1062/",
        "relevance_score": "4",
        "evidence_level": "已阅读全文",
        "full_text_read": "yes",
        "crossref_status": "exact DOI/title verified",
        "openalex_status": "exact DOI/title verified",
        "inclusion_status": "included",
        "notes_file": "research/notes/2026-Wang-PlanRewardBench.md",
        "review_tier": "core-method",
    },
]


def tier(title: str) -> str:
    if title in CORE_5 or title in CORE_4:
        return "core-method"
    if title in SUPPORTING:
        return "supporting-benchmark"
    return "background"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    fd, tmp_name = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp_name, path)
    except Exception:
        os.unlink(tmp_name)
        raise


def update_evidence() -> dict[str, str]:
    with EVIDENCE.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = list(reader.fieldnames or [])
    if "review_tier" not in fields:
        fields.append("review_tier")

    by_title = {row["title"]: row for row in rows}
    aj = by_title["AJ-Bench: Benchmarking Agent-as-a-Judge for Environment-Aware Evaluation"]
    aj.update(
        authors="Wentao Shi; Yu Wang; Yuyang Zhao; Yuxin Chen; Fuli Feng; Xueyuan Hao; Xi Su; Qi Gu; Hui Su; Xunliang Cai; Xiangnan He",
        venue="Findings of ACL",
        doi="10.18653/v1/2026.findings-acl.1269",
        publication_type="conference paper",
        version_status="Findings of ACL 2026 formal open-access version",
        main_findings="Environment-aware judge agents are evaluated on information acquisition, state verification, and process verification; active tool use improves over text-only judging but leaves substantial error.",
        limitations="The benchmark covers three domains and fixed annotation protocols; judge tool skill is entangled with evaluation reasoning, and measured performance is not sufficient for a standalone gold oracle.",
        code_url="https://aj-bench.github.io/",
        paper_url="https://aclanthology.org/2026.findings-acl.1269/",
        relevance_score="4",
        evidence_level="已阅读全文",
        full_text_read="yes",
        crossref_status="exact DOI/title verified",
        openalex_status="exact DOI/title verified; one author-name variant noted",
        inclusion_status="included",
        notes_file="research/notes/2026-Shi-AJBench.md",
    )

    for record in NEW_EVIDENCE:
        if record["title"] in by_title:
            by_title[record["title"]].update(record)
        else:
            rows.append(record)
            by_title[record["title"]] = record

    for row in rows:
        row["review_tier"] = tier(row["title"])
        if row["review_tier"] == "supporting-benchmark":
            row["relevance_score"] = "3"
        elif row["review_tier"] == "background":
            row["relevance_score"] = "2"
        elif row["title"] in CORE_5:
            row["relevance_score"] = "5"
        else:
            row["relevance_score"] = "4"
        if row["inclusion_status"] == "include":
            row["inclusion_status"] = "included"

    write_csv(EVIDENCE, fields, rows)
    return {row["title"]: row["review_tier"] for row in rows}


def update_screening(tiers: dict[str, str]) -> None:
    with SCREENING.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = list(reader.fieldnames or [])
    if "review_tier" not in fields:
        fields.append("review_tier")

    for row in rows:
        row["decision"] = {"include": "included"}.get(row["decision"], row["decision"])
        if row["decision"] in {"exclude", "excluded"}:
            row["decision"] = "excluded"
            row["review_tier"] = "excluded"
        else:
            row["review_tier"] = tiers.get(row["title"], "background")

    by_title = {row["title"]: row for row in rows}
    aj = by_title["AJ-Bench: Benchmarking Agent-as-a-Judge for Environment-Aware Evaluation"]
    aj.update(
        authors="Shi et al.",
        doi="10.18653/v1/2026.findings-acl.1269",
        source="ACL Anthology; Crossref; OpenAlex",
        screening_stage="full text",
        decision="included",
        reason="Core meta-evaluation benchmark for environment-aware agent judges and process/state verification.",
        version_relationship="Findings of ACL 2026 formal version; DOI verified.",
        evidence_level="已阅读全文",
        screened_date="2026-08-14",
        review_tier="core-method",
    )

    additions = {
        item["title"]: {
            "title": item["title"],
            "authors": item["authors"].split(";")[0] + " et al.",
            "year": item["year"],
            "doi": item["doi"],
            "arxiv_id": item["arxiv_id"],
            "source": "ACL Anthology; Crossref; OpenAlex",
            "screening_stage": "full text",
            "decision": "included",
            "reason": "Direct contribution to agent trajectory diagnosis or evaluator meta-evaluation.",
            "version_relationship": item["version_status"],
            "evidence_level": "已阅读全文",
            "screened_date": "2026-08-14",
            "review_tier": "core-method",
        }
        for item in NEW_EVIDENCE
    }
    for title, row in additions.items():
        if title in by_title:
            by_title[title].update(row)
        else:
            rows.append(row)

    # A later full-text pass can supersede an earlier abstract-level exclusion.
    # Keep one current screening decision per DOI/arXiv/title identity.
    evidence_rank = {"仅核验元数据": 0, "仅阅读摘要": 1, "已阅读全文": 2}

    def identity(row: dict[str, str]) -> tuple[str, str]:
        if row["doi"]:
            return ("doi", row["doi"].lower().removeprefix("https://doi.org/"))
        if row["arxiv_id"]:
            return ("arxiv", row["arxiv_id"].lower())
        normalized = "".join(ch.lower() for ch in row["title"] if ch.isalnum())
        return ("title", normalized)

    deduplicated: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = identity(row)
        previous = deduplicated.get(key)
        current_order = (row["screened_date"], evidence_rank.get(row["evidence_level"], -1))
        previous_order = (
            previous["screened_date"],
            evidence_rank.get(previous["evidence_level"], -1),
        ) if previous else ("", -1)
        if previous is None or current_order >= previous_order:
            deduplicated[key] = row

    write_csv(SCREENING, fields, list(deduplicated.values()))


if __name__ == "__main__":
    update_screening(update_evidence())
