# Beonly Studio v6 — modelo para Google Tag Manager

Modelo de tag web para inicializar a integração Beonly Studio v6. A integração requer uma runtime compatível: **o loader atual ainda não lê `window.beonConfig`** e depende de atributos de dados/ID. Confirme a implementação e valide a integração completa em um ambiente controlado antes de ativar em produção. O carregamento bem-sucedido do script chama `gtmOnSuccess`; isso não comprova inicialização nem entrega de rastreamento.

## Configuração

- **Chave de API Beonly:** identificador da conta no formato UUID; não é uma chave secreta.
- **Domínio de cookies:** domínio obrigatório, por exemplo `loja.exemplo.com`.
- **Ambiente:** produção por padrão; staging quando suportado pela operação.
- **Plataforma:** VTEX (`vtex`), VTEXIO (`vtexio`), Shopify (`shopify`), Nuvem Shop (`nuvemshop`), Magento 1.x (`magento1x`), Magento 2.x (`magento2x`) ou WordPress (`wordpress`).

## Instalação e validação

1. No contêiner web do GTM, abra **Modelos**, crie um modelo de tag e importe `template.tpl` no editor.
2. Revise as permissões e execute os cinco testes na aba **Testes**. Crie uma tag com os dados da conta e um acionador apropriado.
3. Use o Preview do GTM em ambiente controlado; confira carregamento, configuração efetivamente recebida pela runtime, inicialização e eventos esperados. Verifique conflitos com integrações existentes e a política de consentimento aplicável. Publique somente após validar a runtime compatível.

O modelo lê e escreve os globais de configuração e fila `beonobject`, `beon`, `beon.q`, `beon.l` e `beonConfig`; lê campos específicos de `beonly` e `beone` para detectar runtimes existentes. Injeta somente `https://c.usebeon.io/v6/loader.js` ou `https://c.staging.usebeon.io/v6/loader.js` e registra logs no modo debug.

## Galeria e versões

Após revisão e validação, publique os arquivos na branch principal de um repositório GitHub público com Issues habilitadas. O responsável deve revisar e aceitar os [termos da galeria](https://developers.google.com/tag-manager/gallery-tos) no editor do GTM e enviar a URL do repositório na [Community Template Gallery](https://tagmanager.google.com/gallery/). Consulte as [instruções oficiais](https://developers.google.com/tag-platform/tag-manager/templates/gallery).

Para atualizar, faça primeiro um commit contendo o novo `template.tpl`, acrescente seu SHA completo no início de `versions` em `metadata.yaml` com notas de mudança e faça outro commit. Preserve o histórico de versões. Execute `python3 scripts/validate.py` e `python3 scripts/scenarios.py | node scripts/scenarios.js` para as verificações locais; elas não substituem os testes e permissões nativos do GTM. Requerem Python 3, PyYAML, Node.js e ImageMagick para validar a imagem.

A licença Apache 2.0 em `LICENSE` foi copiada da distribuição local SPDX (`/usr/share/licenses/spdx/Apache-2.0.txt`).
