# WinOptimizer Pro — Roadmap / TODO

Estado atual: **v1.3.2** (testes unitários + CI no GitHub Actions)

## Feito
- [x] v1.2.x — Auditoria completa do tweaks.json para Win11; Free vs Pro
- [x] v1.3.0 — Licenciamento HMAC offline, Undo real por tweak, persistência de estado (state.json), instalador Inno Setup
- [x] v1.3.2 — Suite pytest (30 testes: license_manager + schema do tweaks.json) e workflow CI (GitHub Actions, Windows, Py 3.11/3.12, py_compile + pytest)
- [x] v1.3.1 — Badge FREE/PRO clicável (ativar/gerir licença), diálogo "Manage License" (licenciado, chave mascarada, desativar com confirmação), escrita atómica do license.json, load tolerante a corrupção

## Próxima sessão (sugestão, por ordem de valor)
1. **Instalador**: rever WinOptimizer.iss — página de licença, atalho opcional no desktop, verificação de versão instalada/upgrade in-place.
2. **UI polida**: estados hover/pressed consistentes nos cards; scroll suave (badge "Applied" já existe desde v1.3.x).
3. **Licenciamento robusto (fase 2)**: formato de chave v2 com payload (edição/expiração) assinado; manter compatibilidade com chaves v1 — adicionar testes à suite existente.

## Notas
- Não repetir a auditoria de tweaks (concluída em v1.2.1).
- keygen.py é ferramenta do autor — nunca incluir no instalador.
- Mudar `_SECRET` em license_manager.py antes de emitir chaves reais.
