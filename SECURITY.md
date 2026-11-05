<!--
Project: Secure Image Generation with ASIC Signature
Author: Francisco Angulo de Lafuente
ORCID: https://orcid.org/0009-0001-1634-7063
Copyright: 2026 Francisco Angulo de Lafuente
Recorded on: 2026-11-05
SPDX-License-Identifier: MIT
-->

Security & secrets

**Author:** [Francisco Angulo de Lafuente](https://orcid.org/0009-0001-1634-7063)

If you have exposed any API keys, passwords, tokens, or FTP credentials publicly (for example in chat or in files), treat them as compromised and **revoke/regenerate them immediately**.

Recommended actions:
- Revoke any keys you posted publicly (FTP, W&B, Hugging Face, OSF, etc.).
- Replace with fresh keys and store them only in secure places (GitHub Secrets, OS environment variables, or a secrets manager).
- If secrets were committed to git history, consider using `git filter-repo` or BFG Repo-Cleaner to remove them from history and force-push the cleaned history.
- Rotate credentials for any systems that might have been exposed.

If you want, I can run a repository-wide secrets scan and help with history cleaning (this operation rewrites history and requires force-pushing — coordinate with any collaborators).
**Citation and reuse:** Cite the project through CITATION.cff; see LICENSE and provenance.json for the applicable scope.
