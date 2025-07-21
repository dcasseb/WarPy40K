# WarPy40K: Funcionalidades e Melhorias Futuras

Este documento acompanha os recursos planejados, correções de bugs e melhorias para a linguagem WarPy40K e interpretador. Contribuições e sugestões são bem-vindas!

---

## Melhorias do Interpretador Central

- **Funcionalidade Correta do vox_cast**
  - Garantir que `vox_cast` imprima argumentos string conforme esperado, incluindo análise adequada e saída de literais string.
  - Adicionar suporte para concatenação de strings e interpolação de variáveis em `vox_cast`.

- **Manipulação Robusta de Literais String**
  - Melhorar a análise de literais string (suporte para sequências de escape, strings multi-linha, etc.).
  - Corrigir problemas restantes com strings vazias ou malformadas.

- **Funcionalidade de Entrada**
  - Garantir que `hear_the_emperors_voice` receba e retorne entrada do usuário de forma confiável.
  - Adicionar validação de entrada e tratamento de erros para tipos numéricos e string.

- **Relatório de Erros e Depuração**
  - Fornecer mensagens de erro mais claras para erros de sintaxe e execução.
  - Adicionar relatório de linha/coluna para erros de análise e execução.
  - Implementar um modo de depuração para rastreamento de execução passo a passo.

- **Melhorias do Sistema de Tipos**
  - Aplicar verificação de tipos para atribuições de variáveis e argumentos de comandos.
  - Adicionar suporte para inferência de tipos e conversão de tipos quando apropriado.

---

## Recursos da Linguagem

- **Funções e Procedimentos**
  - Adicionar funções definidas pelo usuário com parâmetros e valores de retorno.
  - Suporte para chamadas de função e recursão.

- **Estruturas de Dados**
  - Implementar arrays/listas e dicionários/mapas.
  - Adicionar suporte para iteração sobre coleções.

- **Fluxo de Controle Avançado**
  - Adicionar suporte para declarações `break`, `continue` e `return`.
  - Implementar construções switch/case ou correspondência de padrões.

- **Módulos e Importações**
  - Permitir dividir código em múltiplos arquivos e importar módulos.

---

## Ferramentas e Ecossistema

- **Framework de Testes**
  - Criar um executor de testes para scripts `.wp40k` com asserções e verificações de saída.

- **Melhorias do Linter**
  - Expandir análise estática para capturar mais tipos de erro e questões de estilo.
  - Adicionar sugestões de correção automática para problemas comuns.

- **Integração com Editores**
  - Melhorar destaque de sintaxe e autocompletar para extensões VS Code e Sublime Text.
  - Adicionar snippets de código e popups de documentação.

---

## Documentação

- **Referência da Linguagem**
  - Manter a referência de comandos e guia da linguagem atualizados com novos recursos.

- **Tutoriais e Exemplos**
  - Adicionar mais scripts de exemplo demonstrando recursos avançados e melhores práticas.

---

## Problemas Conhecidos

- Literais string podem ser analisados como strings vazias em alguns casos (limitação do parser Earley).
- Mensagens de erro podem carecer de contexto ou números de linha.
- Alguns comandos podem não lidar com argumentos ou tipos de forma robusta.

---

*Última atualização: [15-07-2025]*