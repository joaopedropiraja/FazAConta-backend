Fluxogramas para Aplicativo de Compartilhamento de Despesas
Este documento contém fluxogramas modelados em MermaidJS que representam as funcionalidades principais de um aplicativo de compartilhamento de despesas semelhante ao Splitwise e Tricount. Esses fluxogramas cobrem autenticação de usuário, gerenciamento de grupos, adição de despesas, acerto de contas, notificações e configurações de conta.

1. Fluxo de Autenticação de Usuário

```mermaid
flowchart TD
    Inicio[Início] --> UsuarioExistente{Usuário Existente?}
    UsuarioExistente -- Sim --> PaginaLogin[Página de Login]
    UsuarioExistente -- Não --> PaginaCadastro[Página de Cadastro]
    PaginaLogin --> PainelUsuario[Painel do Usuário]
    PaginaCadastro --> CriarConta[Criar Conta]
    CriarConta --> PainelUsuario

```

Explicação:

Os usuários começam decidindo se são usuários existentes.
Usuários existentes vão para a página de login; novos usuários vão para a página de cadastro.
Após a autenticação ou criação da conta, os usuários são direcionados ao seu painel.

2. Fluxo de Criação e Gerenciamento de Grupo

```mermaid
flowchart TD
    PainelUsuario --> OpcaoGrupo{Criar ou Entrar em um Grupo?}
    OpcaoGrupo -- Criar --> CriarGrupo[Criar Novo Grupo]
    OpcaoGrupo -- Entrar --> EntrarGrupo[Entrar em Grupo Existente]
    CriarGrupo --> ConvidarMembros[Convidar Membros]
    ConvidarMembros --> PainelGrupo[Painel do Grupo]
    EntrarGrupo --> InserirCodigo[Inserir Código do Grupo]
    InserirCodigo --> PainelGrupo
```

Explicação:

A partir do painel, os usuários escolhem criar um novo grupo ou entrar em um existente.
Criar um grupo envolve convidar membros; entrar requer inserir um código de grupo.
Ambos os caminhos levam ao painel do grupo.

3. Fluxo de Adição de Despesa

```mermaid
flowchart TD
    PainelGrupo --> AdicionarDespesa[Adicionar Despesa]
    AdicionarDespesa --> DetalhesDespesa[Inserir Detalhes da Despesa]
    DetalhesDespesa --> MetodoDivisao{Dividir Igualmente?}
    MetodoDivisao -- Sim --> ConfirmarDespesa[Confirmar Despesa]
    MetodoDivisao -- Não --> DivisaoPersonalizada[Especificar Partes Individuais]
    DivisaoPersonalizada --> ConfirmarDespesa
    ConfirmarDespesa --> AtualizarSaldos[Atualizar Saldos]
    AtualizarSaldos --> PainelGrupo
```

Explicação:

Os usuários podem adicionar despesas a partir do painel do grupo.
Eles inserem os detalhes da despesa e escolhem como dividir o valor.
O aplicativo atualiza os saldos conforme necessário e retorna ao painel do grupo.

4. Fluxo de Acerto de Contas

```mermaid
flowchart TD
    PainelGrupo --> AcertarContas[Acertar Contas]
    AcertarContas --> EscolherMembro[Selecionar Membro para Pagar]
    EscolherMembro --> MetodoPagamento[Escolher Método de Pagamento]
    MetodoPagamento --> ConfirmarPagamento[Confirmar Pagamento]
    ConfirmarPagamento --> AtualizarSaldos[Atualizar Saldos]
    AtualizarSaldos --> PainelGrupo
```

Explicação:

Os usuários iniciam o acerto de contas a partir do painel do grupo.
Eles selecionam um membro para pagar e escolhem um método de pagamento.
Após a confirmação, o aplicativo atualiza os saldos e retorna ao painel.

5. Fluxo de Notificações e Feed de Atividades

```mermaid
flowchart TD
    QualquerAcao --> AtualizarFeed[Atualizar Feed de Atividades]
    AtualizarFeed --> NotificarMembros[Enviar Notificações]
    NotificarMembros --> AguardarProximaAcao
    AguardarProximaAcao --> QualquerAcao
```

Explicação:

Qualquer ação realizada (como adicionar despesas ou acertar contas) atualiza o feed de atividades.
O aplicativo envia notificações aos membros relevantes.
O sistema aguarda a próxima ação para continuar o ciclo.

6. Fluxo de Configurações de Conta

```mermaid
flowchart TD
    PainelUsuario --> ConfiguracoesConta[Configurações da Conta]
    ConfiguracoesConta --> AlterarDados[Alterar Dados Pessoais]
    ConfiguracoesConta --> AlterarSenha[Alterar Senha]
    ConfiguracoesConta --> GerenciarPagamento[Gerenciar Métodos de Pagamento]
    AlterarDados --> SalvarAlteracoes[Salvar Alterações]
    AlterarSenha --> SalvarAlteracoes
    GerenciarPagamento --> SalvarAlteracoes
    SalvarAlteracoes --> PainelUsuario
```

Explicação:

Os usuários podem acessar as configurações da conta a partir do painel.
Eles podem alterar dados pessoais, senhas ou gerenciar métodos de pagamento.
Após salvar as alterações, são redirecionados de volta ao painel.
