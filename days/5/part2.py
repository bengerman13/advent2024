import sys
from typing import TypeAlias


class PageNumber:
    def __init__(self, number: int) -> None:
        self.number: int = number
        self.must_be_before = set()

    def add(self, number: int) -> None:
        self.must_be_before.add(number)

    def __lt__(self, other) -> bool:
        if other.number in self.must_be_before:
            return True

    def __hash__(self):
        return hash(self.number)


ManualRequest: TypeAlias = list[PageNumber]
RuleSet: TypeAlias = dict[int, PageNumber]


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
                rule = rules.get(first, PageNumber(first))
                rule.add(second)
                rules[first] = rule
            elif "," in line:
                manual = []
                for page_number_str in line.split(","):
                    page_number = int(page_number_str)
                    manual.append(rules.get(page_number, PageNumber(page_number)))
                manuals.append(manual)
    return rules, manuals


def check_manual(manual: ManualRequest, rules: RuleSet) -> bool:
    return sorted(manual) == manual


def sort_manual(manual: ManualRequest, rules: RuleSet) -> ManualRequest:
    return sorted(manual)


def middle_page(manual: ManualRequest) -> int:
    return manual[len(manual) // 2].number


def main():
    rules, requests = load_rules(sys.argv[1])
    wrong_manuals = [manual for manual in requests if not check_manual(manual, rules)]
    total = 0
    for manual in wrong_manuals:
        total += middle_page(sorted(manual))
    print(total)


if __name__ == "__main__":
    main()
