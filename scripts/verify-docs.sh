#!/usr/bin/env bash
set -euo pipefail
for path in README.md README.txt USER-MANUAL.md USER-MANUAL.txt CHANGELOG.md CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md SUPPORT.md LICENSE LICENSE-CODE LICENSE-DOCS AGENTS.md docs/index.html docs/architecture.md docs/architecture-civiclegal.svg docs/IMPLEMENTATION_PLAN.md docs/MILESTONES.md docs/RECONCILIATION.md docs/github-discussions-seed.md; do [[ -s "$path" ]] || { echo "VERIFY-DOCS: FAILED missing $path"; exit 1; }; done
for file in README.md README.txt USER-MANUAL.md USER-MANUAL.txt CHANGELOG.md docs/index.html AGENTS.md MILESTONE_0_7_DONE.md; do for pattern in CivicBudget civicbudget CivicHR civichr HRIS "0.1.1.dev0" "~=0.2" MIT; do if grep -Fq "$pattern" "$file"; then echo "VERIFY-DOCS: FAILED stale marker '$pattern' found in $file"; exit 1; fi; done; done
grep -Fq "civiccore==0.3.0" README.md || { echo "VERIFY-DOCS: FAILED README pin"; exit 1; }
grep -Fq "not legal advice" README.md || { echo "VERIFY-DOCS: FAILED legal-advice boundary"; exit 1; }
echo "VERIFY-DOCS: PASSED"
