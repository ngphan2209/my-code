
"""Suy luận chính xác và gần đúng trên tập luật chuyên gia."""

from app.knowledge import GROUPS, group_of

NO_RESULT = (
    "Không tìm thấy địa điểm đủ mức phù hợp "
    "trong cơ sở tri thức."
)

MIN_MATCH = 5


def infer(facts, rules, events):
    """
    Giai đoạn 1: Tìm luật khớp chính xác.
    Giai đoạn 2: Nếu không có, tìm luật gần đúng.

    Luôn giữ nguyên tỉnh/thành phố và khoảng cách.
    """

    event_map = {
        event["code"]: event for event in events
    }

    facts = list(facts)
    groups = [group_of(code) for code in facts]

    if (
        len(facts) != 7
        or set(groups) != set(GROUPS)
        or len(set(groups)) != 7
    ):
        raise ValueError(
            "Cần chọn đúng một sự kiện trong mỗi nhóm."
        )

    if any(code not in event_map for code in facts):
        raise ValueError("Mã sự kiện không tồn tại.")

    selected = {
        group_of(code): code for code in facts
    }

    candidates = []

    for rule in rules:
        conditions = {
            group_of(code): code
            for code in rule["conditions"]
        }

        if (
            conditions["R"] != selected["R"]
            or conditions["K"] != selected["K"]
        ):
            continue

        matched = []
        mismatched = []

        for group in GROUPS:
            selected_code = selected[group]
            rule_code = conditions[group]

            if selected_code == rule_code:
                matched.append(group)
            else:
                mismatched.append({
                    "group": group,
                    "selected": selected_code,
                    "expected": rule_code
                })

        score = len(matched)

        candidates.append({
            "code": rule["result"],
            "rule_ids": [rule["id"]],
            "score": score,
            "percentage": round(score / 7 * 100, 2),
            "matched_groups": matched,
            "mismatches": mismatched,
            "exact": score == 7
        })

    exact_results = {}

    for item in candidates:
        if item["exact"]:
            code = item["code"]

            if code not in exact_results:
                exact_results[code] = item
            else:
                exact_results[code]["rule_ids"].extend(
                    item["rule_ids"]
                )

    if exact_results:
        return sorted(
            exact_results.values(),
            key=lambda x: int(x["code"][1:])
        )

    near_results = {}

    for item in candidates:
        if item["score"] < MIN_MATCH:
            continue

        code = item["code"]

        if code not in near_results:
            near_results[code] = item
        else:
            current = near_results[code]

            if item["score"] > current["score"]:
                near_results[code] = item
            elif item["score"] == current["score"]:
                current["rule_ids"].extend(
                    item["rule_ids"]
                )

    results = sorted(
        near_results.values(),
        key=lambda x: (
            -x["score"],
            int(x["code"][1:])
        )
    )

    for item in results:
        item["rule_ids"] = sorted(
            set(item["rule_ids"])
        )

    return results
