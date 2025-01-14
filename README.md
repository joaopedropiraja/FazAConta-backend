# Projeto desenvolvido para a disciplina Programção Orientada a Objetos (POO)

Abaixo está a descrição da estrutura de pastas do projeto, inspiradas em conceitos de Arquitetura Limpa e DDD (Domain Driven Design)

# Estrutura do Projeto FazAConta-backend

A seguir está a descrição das principais pastas do projeto `fazaconta_backend`, baseada nos princípios de **Arquitetura Limpa** e **Domain-Driven Design (DDD)**.

## **modules**

Essa pasta é o coração do sistema, onde os módulos principais da aplicação estão organizados de forma modular, seguindo o princípio de separação por contexto. Cada módulo (como `group` e `user`) representa um **Bounded Context** dentro do DDD, encapsulando a lógica e os comportamentos específicos do domínio que ele representa. Dentro de cada módulo, temos subpastas que seguem a divisão de responsabilidades:

- **`domain`**: Contém as entidades de domínio, que representam os conceitos principais do módulo, e as interfaces que definem os contratos de comportamento do sistema. É onde reside a lógica de negócio mais essencial.
- **`dtos`**: Define os **Data Transfer Objects**, usados para transportar dados entre camadas da aplicação. Esses objetos facilitam a separação entre as camadas, evitando o acoplamento direto. São utilizados principalmente como interface de comunicação para recebimento de requisições HTTP e envio de respostas.
- **`infra`**: Implementa os detalhes de infraestrutura do módulo, como conexões com bancos de dados, integração com APIs externas ou qualquer outro mecanismo que dependa de tecnologia específica.
- **`mappers`**: Realiza a conversão entre diferentes modelos de dados (como de entidades para DTOs e vice-versa), mantendo a separação clara entre as camadas.
- **`repos`**: Contém a implementação dos repositórios, que abstraem o acesso aos dados no banco. Essa camada é crucial para garantir que a aplicação interaja com os dados sem se preocupar com os detalhes de persistência.
- **`services`** (caso aplicável): Define serviços específicos que encapsulam regras de negócio mais complexas ou orquestram a interação entre entidades.
- **`useCases`**: Representa os **Casos de Uso** ou **Serviços de Aplicação**, encapsulando a lógica de negócio em um nível mais alto e servindo como ponto de entrada para interações com o domínio.

---

## **shared**

Essa pasta contém elementos que são reutilizados por múltiplos módulos, seguindo o princípio DRY (**Don't Repeat Yourself**). Os componentes aqui armazenados são genéricos e independentes de contexto específico.

- **`application`**: Define conceitos da camada de aplicação genéricos que podem ser utilizados em diferentes módulos, como useCases.
- **`domain`**: Define conceitos de domínio genéricos que podem ser utilizados em diferentes módulos, como interfaces base ou entidades comuns.
- **`infra`**: Armazena implementações de infraestrutura que são usadas em todo o sistema, como configuração de bancos de dados, provedores de serviços externos e interações genéricas.

Essa divisão permite centralizar elementos comuns, reduzindo duplicação e promovendo consistência entre os módulos.

---

## **utils**

Essa pasta armazena funções utilitárias e genéricas que são utilizadas em várias partes do sistema. Geralmente, essas funções não pertencem diretamente a um domínio específico, mas são essenciais para o funcionamento da aplicação.

Os utilitários são cuidadosamente projetados para evitar acoplamento com módulos ou domínios específicos, garantindo reusabilidade.

---

## Organização Geral

A organização do projeto segue os princípios de **Arquitetura Limpa** e **DDD**, promovendo:

1. **Separação de responsabilidades**: Cada pasta encapsula uma parte clara e específica da lógica de negócio, infraestrutura ou utilitários.
2. **Baixo acoplamento e alta coesão**: A estrutura facilita a manutenção e evolução do sistema, permitindo que mudanças em um módulo não impactem outros.
3. **Reusabilidade e escalabilidade**: Componentes compartilhados e bem definidos permitem que novos módulos ou funcionalidades sejam adicionados sem retrabalho.

Essa estrutura modular torna o sistema robusto, escalável e fácil de entender para novos desenvolvedores, promovendo boas práticas de engenharia de software.
