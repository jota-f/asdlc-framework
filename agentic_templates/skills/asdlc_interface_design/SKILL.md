---
name: asdlc_interface_design
description: Skill de engenharia disciplinada para projetar interfaces, contratos de API, tipos de dados e schemas antes de escrever a lógica de implementação.
user_command: /design-interface
invocation_mode: user_and_model
tags: [interface, contracts, typing, api, schema, ddd]
---

# 📐 A-SDLC Interface & Contract Design Skill (`/design-interface`)

Inspirada no princípio do Matt Pocock de "Interfaces First", esta skill orienta o agente a desenhar contratos de tipos, assinaturas de funções e schemas de validação antes de qualquer código de implementação ser gerado.

## 🎯 Por que Interfaces Primeiro?
- Elimina 90% dos erros de integração entre frontend, backend e módulos internos.
- Força a clareza sobre entradas, saídas, erros e nulidade.
- Cria a especificação exata que os testes e a implementação devem seguir.

---

## 🧭 Procedimento

### Passo 1: Mapear Entidades & Fronteiras
- Identifique os dados de entrada (Input / DTO).
- Identifique os dados de saída (Output / View Model).
- Mapeie todos os possíveis estados de erro (Exceptions / Result Types).

### Passo 2: Definir Interfaces Puras
Crie ou apresente as interfaces sem detalhes de implementação:

#### Exemplo em TypeScript:
```typescript
export interface CreateUserInput {
  email: string;
  name: string;
  role: 'admin' | 'member';
}

export type CreateUserResult =
  | { success: true; userId: string; createdAt: Date }
  | { success: false; error: 'EMAIL_ALREADY_EXISTS' | 'INVALID_ROLE' };

export interface IUserRepository {
  create(input: CreateUserInput): Promise<CreateUserResult>;
  findById(id: string): Promise<User | null>;
}
```

#### Exemplo em Python (Pydantic / Protocols):
```python
from typing import Protocol, Literal, Union
from pydantic import BaseModel, EmailStr

class CreateUserDTO(BaseModel):
    email: EmailStr
    name: str
    role: Literal["admin", "member"]

class UserCreatedResult(BaseModel):
    user_id: str
    success: bool = True

class IUserRepository(Protocol):
    async def create(self, dto: CreateUserDTO) -> UserCreatedResult: ...
    async def get_by_id(self, user_id: str) -> dict | None: ...
```

### Passo 3: Validação com o Usuário
Apresente o contrato ao usuário:
1. *Os nomes e propriedades cobrem todos os requisitos?*
2. *Os tipos de erro e edge cases estão contemplados?*

Ao aprovar o contrato, passe para a etapa de testes com `asdlc_tdd` (`/tdd`) ou implementação com `asdlc_implementation`.
