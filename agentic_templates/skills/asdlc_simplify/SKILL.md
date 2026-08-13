---
name: asdlc_simplify
description: Skill para realizar refatoração, simplificação e remoção de código morto pós-Green mantendo 100% da suíte de testes passando.
---

# 🧹 A-SDLC Code Simplify Skill

Esta skill atua como o **Code Refactor & Simplicity Agent** do A-SDLC Framework. Ela deve ser invocada após a conclusão bem-sucedida de um ciclo TDD (Green Phase) para refatorar o código, eliminar complexidade desnecessária e garantir que o resultado final seja enxuto, legível e manutenível.

---

## 📐 Diretrizes de Simplificação (Princípio Ponytail / YAGNI)

### 1. Eliminação de Abstrações Prematuras
- Remova interfaces que possuem apenas 1 implementação concreta (a menos que sejam estritamente exigidas por frameworks de DI).
- Elimine padrão Factory/Builder se uma simples instanciação direta for suficiente.
- Remova parâmetros de configuração genéricos que possuem valores fixos e sem perspectiva de variação.

### 2. Controle de Escopo e Tamanho
- **Limite de 300 Linhas**: Se um novo arquivo tiver mais de 300 linhas, divida-o em módulos coesos e menores.
- **Redução de Profundidade de Aninhamento**: Substitua blocos `if/else` profundamente aninhados por **Guard Clauses** (early returns).
- **Lixamento de Código Morto**: Remova imports não utilizados, variáveis não referenciadas e funções de rascunho.

### 3. Clareza e Nomenclatura
- Substitua nomes de variáveis genéricos (`data`, `temp`, `res`, `obj`) por nomes expressivos com significado de domínio.
- Dê preferência a funções pequenas e com responsabilidade única (Single Responsibility Principle).

---

## ⚡ Regra de Ouro da Refatoração
> **NENHUMA REFATORAÇÃO É VÁLIDA SE OS TESTES QUEBRAREM.**

Após aplicar cada alteração de simplificação:
1. Execute a suíte de testes via `run_command`.
2. Se qualquer teste falhar, **reverta imediatamente a alteração** e reavalie a abordagem.
3. Garanta `exit code 0` antes de concluir o workflow.

---

## 💡 Saída para o Usuário
O agente apresenta o diff simplificado e a confirmação:
> `[A-SDLC Simplify] Refatoração concluída! Reduzidas N linhas de código sem quebrar nenhum dos testes da suíte.`
