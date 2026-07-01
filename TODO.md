# WinOptimizer Pro — Roadmap / TODO

Estado atual: **v1.3.1** (gestão de licença na UI, armazenamento de licença robusto)

## Feito
- [x] v1.2.x — Auditoria completa do tweaks.json para Win11; Free vs Pro
- [x] v1.3.0 — Licenciamento HMAC offline, Undo real por tweak, persistência de estado (state.json), instalador Inno Setup
- [x] v1.3.1 — Badge FREE/PRO clicável (ativar/gerir licença), diálogo "Manage License" (licenciado, chave mascarada, desativar com confirmação), escrita atómica do license.json, load tolerante a corrupção

## Próxima sessão (sugestão, por ordem de valor)
1. **UI polida**: estados hover/pressed consistentes nos cards; scroll suave; indicador visual de tweaks já aplicados (badge "Applied") na lista.
2. **Instalador**: rever WinOptimizer.iss — página de licença, atalho opcional no desktop, verificação de versão instalada/upgrade in-place.
3. **Licenciamento robusto (fase 2)**: formato de chave v2 com payload (edição/expiração) assinado; manter compatibilidade com chaves v1.
4. **Qualidade**: testes unitários para license_manager e para o parsing do tweaks.json (pytest, correm em CI/GitHub Actions).

## Notas
- Não repetir a auditoria de tweaks (concluída em v1.2.1).
- keygen.py é ferramenta do autor — nunca incluir no instalador.
- Mudar `_SECRET` em license_manager.py antes de emitir chaves reais.
