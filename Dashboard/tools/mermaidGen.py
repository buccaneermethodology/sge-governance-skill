import json
from pathlib import Path

src = Path(".semx/tmp/runtime-exp/extract_p05_tbc/read_model.json")
out = Path(".semx/tmp/runtime-exp/extract_p05_tbc/read_model.mmd")

data = json.loads(src.read_text(encoding="utf-8"))

def esc(value):
    return str(value).replace('"', "'")

node_ids = {}
lines = ["flowchart TB"]

for index, node in enumerate(data.get("nodes", []), start=1):
    original_id = node["node_id"]
    mermaid_id = f"n{index}"
    node_ids[original_id] = mermaid_id

    label = (
        f"{esc(original_id)}<br/>"
        f"{esc(node.get('node_kind', 'unknown'))} / {esc(node.get('phase', 'unknown'))}<br/>"
        f"event: {esc(node.get('introduced_by_event', 'unknown'))}"
    )
    lines.append(f'  {mermaid_id}["{label}"]')

for index, edge in enumerate(data.get("edges", []), start=1):
    src_id = edge["from"]
    dst_id = edge["to"]

    if src_id not in node_ids:
        node_ids[src_id] = f"missing_src_{index}"
        lines.append(f'  {node_ids[src_id]}["{esc(src_id)}"]')

    if dst_id not in node_ids:
        node_ids[dst_id] = f"missing_dst_{index}"
        lines.append(f'  {node_ids[dst_id]}["{esc(dst_id)}"]')

    label = (
        f"{esc(edge.get('edge_type', 'edge'))}<br/>"
        f"{esc(edge.get('edge_category', 'unknown'))}<br/>"
        f"state_effect={esc(edge.get('state_effect', 'unknown'))}"
    )
    lines.append(f'  {node_ids[src_id]} -->|"{label}"| {node_ids[dst_id]}')

out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(out)
