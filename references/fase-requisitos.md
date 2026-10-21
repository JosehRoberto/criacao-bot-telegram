# Fase de requisitos e decisões

Como transformar uma ideia de bot em um `docs/requisitos.md` sem ambiguidade, antes de escrever
código.

## 1. Por que esta fase existe

A maior fonte de retrabalho em bots Telegram é descobrir, no meio da implementação, que o **modelo de
dados** ou o **alvo das alterações** estava indefinido. Cada pergunta respondida tarde custa refazer
serviços, handlers, testes e preview. Fechar isso agora é barato; refazer depois é caro.

## 2. O que precisa estar fechado antes de codar

1. **Objetivo** em uma frase.
2. **Modelo de dados**: quais campos cada entidade tem e **onde** são persistidos.
3. **Alvo das alterações**: qual arquivo/API/recurso o bot manipula e qual é o formato exato.
4. **Regras de negócio invariantes**: ordenação, formatação, marcadores, unicidade.
5. **Fonte de verdade**: qual cópia/clone é autoritativo (evitar duas cópias divergentes).
6. **Autenticação e segredos**: quais variáveis de ambiente existem.
7. **Fluxo conversacional**: menu, campos coletados, preview, aprovação.
8. **Publicação/escrita**: quando e como o bot grava (e o que exige confirmação).

## 3. Como conduzir

- Comece pelo template `assets/templates/requisitos.template.md`.
- Para cada item do prompt inicial, formule **uma decisão**. Se houver conflito (ex.: um campo pedido
  que o formato alvo não suporta), **pare e apresente a divergência** — não decida sozinho por algo
  que muda o escopo.
- Registre as decisões numeradas em `## 2. Decisões confirmadas` e as dúvidas em
  `## 3. Pendências / conflitos`.
- Quando o usuário responder a uma pendência, **mova a resposta** para as decisões confirmadas.
- Mantenha o documento enxuto: ele é a fonte canônica do escopo, não um diário.

## 4. Sinais de que ainda não pode avançar

- Não se sabe **onde** os dados são gravados.
- O modelo de dados não bate com o formato real do arquivo/API de destino.
- Há duas cópias do mesmo recurso sem definição de qual é a fonte da verdade.
- A regra de formatação (ordenação, template, marcador) não está escrita.

## 5. Estrutura recomendada do `docs/requisitos.md`

```markdown
# Requisitos — <Nome do Projeto>

## 1. Visão geral
## 2. Decisões confirmadas
### 2.1 <escopo/dados>
### 2.2 Repositórios e pastas
### 2.3 Localização do código
### 2.4 <formato/regras de negócio>
...
## 3. Pendências / conflitos
## 4. Estrutura de pastas proposta
## 5. Variáveis de ambiente (.env)
## 6. Próximos passos
```

## 6. Transição para a implementação

Só depois de `## 3. Pendências` estar vazio (ou explicitamente aceito) siga para a Fase 2
(estrutura + repositório) e a Fase 3 (`AGENTS.md`). O `AGENTS.md` deve refletir as decisões desta
fase nas seções de regras de negócio e regiões protegidas.
