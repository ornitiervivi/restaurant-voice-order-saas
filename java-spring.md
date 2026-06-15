# Compatibilidade — Java/Spring

## Versões

- Java: definir no projeto derivado.
- Spring Boot: definir no projeto derivado.
- Build tool: Maven ou Gradle, a definir.

## Regras obrigatórias

- Não usar `record`.
- Não adicionar comentários no código.
- Não fazer mudanças não solicitadas.
- Preferir classes completas, explícitas e testáveis.
- Manter nulidade segura.
- Evitar listas longas de parâmetros; usar objetos de comando, request ou configuração.
- Preservar compatibilidade binária e de API pública quando aplicável.
- Aplicar Clean Code, Clean Architecture, SOLID e design patterns apropriados.
- Usar inglês como idioma padrão para todo código, contratos técnicos, schemas, configurações e documentação técnica do projeto derivado.
- Não misturar idiomas no código ou em contratos técnicos.
- Exigir 100% de cobertura de linhas e branches em testes unitários para classes de regras de negócio.

## Bibliotecas

Adicionar dependências somente com justificativa registrada em `DECISIONS.md`. Preferir bibliotecas que reduzam boilerplate e simplifiquem código, como Lombok, utilitários de collections, `StringUtils`, `Objects` e equivalentes, desde que tenham manutenção ativa, compatibilidade com a stack e ganho claro de legibilidade.
