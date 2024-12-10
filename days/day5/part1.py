import sys
from typing import TypeAlias

PageNumber: TypeAlias = int
ManualRequest: TypeAlias = list[PageNumber]
RuleSet: TypeAlias = dict[PageNumber, set[PageNumber]]


def load_rules(filename) -> tuple[RuleSet, list[ManualRequest]]:
    rules: RuleSet = {}
    manuals: list[ManualRequest] = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if "|" in line:

                first_str, _, second_str = line.partition("|")
                first = int(first_str)
                second = int(second_str)
                rule = rules.get(first, set())
                rule.add(second)
                rules[first] = rule
            elif "," in line:
                page_numbers = [int(el) for el in line.split(",")]
                manuals.append(page_numbers)
    return rules, manuals


def check_manual(manual: ManualRequest, rules: RuleSet) -> bool:
    seen: set[PageNumber] = set()
    for page in manual:
        if page in rules:
            page_rules = rules[page]
            intersection = page_rules & seen
            if len(intersection):
                return False
        seen.add(page)
    return True


def middle_page(manual: ManualRequest) -> int:
    return manual[len(manual) // 2]


def main():
    rules, requests = load_rules(sys.argv[1])
    passed_manuals = [manual for manual in requests if check_manual(manual, rules)]
    total = 0
    for manual in passed_manuals:
        total += middle_page(manual)
    print(total)


if __name__ == "__main__":
    main()
