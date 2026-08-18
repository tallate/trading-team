"""Validate the portable AgentTeams committee protocol without external packages."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_role_map(data: dict) -> None:
    require(data.get("protocol_version") == "1.0", "role map protocol_version must be 1.0")
    roles = data.get("roles")
    require(isinstance(roles, list) and roles, "role map must include roles")
    role_ids = {role.get("id") for role in roles if isinstance(role, dict)}
    required = {"team_leader", "fundamental_equity", "market_structure", "macro_sector", "positioning_ownership", "thesis_bull", "thesis_bear", "investment_committee_chair"}
    require(required <= role_ids, "role map is missing a required committee responsibility")
    execution = data.get("execution", {})
    require(execution.get("mode") == "dag", "committee execution mode must be dag")
    require(set(execution.get("parallel_wave", [])) <= role_ids, "parallel wave refers to unknown role")
    require(set(execution.get("review_wave", [])) <= role_ids, "review wave refers to unknown role")
    require(execution.get("final_owner") == "investment_committee_chair", "chair must own final memo")


def validate_research_brief(data: dict) -> None:
    required = {"packet_type", "protocol_version", "security", "horizon", "mandate", "evidence_cutoff", "permitted_sources", "question"}
    require(required <= data.keys(), "research brief is missing a required field")
    require(data["packet_type"] == "research_brief", "example packet_type must be research_brief")
    require(data["protocol_version"] == "1.0", "example protocol_version must be 1.0")
    require(isinstance(data["permitted_sources"], list) and data["permitted_sources"], "research brief needs permitted sources")


def main() -> int:
    validate_role_map(load_json("role-map.json"))
    validate_research_brief(load_json("examples/research-brief.json"))
    print("Protocol validation passed: role map and research brief are structurally valid.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Protocol validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
