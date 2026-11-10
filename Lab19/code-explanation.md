# Explain Cathie Wood's checks

Open add_checks in panel.py.

1. Read the same annual rows used by Buffett and Burry. For each year, get R&D and revenue from selected SEC facts, with tag and filing provenance preserved.
2. Set R&D/revenue to unknown when either input is missing or revenue is not positive. Otherwise divide, then multiply by one hundred to display a percent. Missing is never zero.
3. Take the first and last revenue values. Require all five annual periods and positive endpoints. Compute the fourth root of last/first, subtract one and express as percent; five annual observations have four intervals.
4. outcome returns not known for an absent derived value; otherwise it tests the stated threshold and returns pass or fail.
5. Compare CAGR with the selected growth threshold and latest R&D/revenue with the fixed reinvestment threshold. Changing the growth slider changes only its predicate, not the source facts or the missing-value rule.

Three personas can disagree because their objectives and predicates differ, even with identical evidence. The script determines numbers and tests; the separate memos interpret their meaning. They are not independent data sources and do not establish a causal or valuation conclusion.
