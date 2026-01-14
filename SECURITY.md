Security & secrets

If you have exposed any API keys, passwords, tokens, or FTP credentials publicly (for example in chat or in files), treat them as compromised and **revoke/regenerate them immediately**.

Recommended actions:
- Revoke any keys you posted publicly (FTP, W&B, Hugging Face, OSF, etc.).
- Replace with fresh keys and store them only in secure places (GitHub Secrets, OS environment variables, or a secrets manager).
- If secrets were committed to git history, consider using `git filter-repo` or BFG Repo-Cleaner to remove them from history and force-push the cleaned history.
- Rotate credentials for any systems that might have been exposed.

If you want, I can run a repository-wide secrets scan and help with history cleaning (this operation rewrites history and requires force-pushing — coordinate with any collaborators).