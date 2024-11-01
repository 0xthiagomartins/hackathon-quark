# Quark Code Challenge
Bem-vindo ao Desafio de Programação voltado para o Mercado de Assessoria e Prospecção! Este desafio é direcionado a programadores que desejam demonstrar suas habilidades na criação de sistemas de alta qualidade, focados em eficiência, organização e criatividade para resolver problemas.

Principais Qualidades Avaliadas:
- Criatividade: Capacidade de apresentar soluções inovadoras e funcionais.
- Organização: Estruturação clara e lógica do código e do projeto.
- Performance: Otimização de desempenho para garantir uma experiência rápida e confiável.
- Eficiência: Uso inteligente de recursos para atender aos requisitos com o menor consumo possível e mitigação de erros por meio de testes

## Sprint 01: API
A API pode ser dividida em dois domínios:

### Gerenciamento de Usuário
- Controle de Usuários: Permita que um usuário do tipo ADMIN adicione novos usuários e configure níveis de acesso.
- Autenticação e Níveis de Acesso:
  - Admin: Acesso completo com permissões de leitura, edição, exclusão e aprovação de dados.
  - Trainee: Não possui acesso à visualização de dados.
  - Assessor: Acesso limitado à leitura dos dados de seus próprios clientes.

### Gerenciamento de Operações
Para o gerenciamento de operações considere o seguinte processo:
- Todas as manhãs recebemos uma planilha em excel, ainda em formato XLS, constando o histórico de operações de forma incremental, a essa denominaremos PLANILHA DE OPERAÇÕES
- Todas as segunda-feiras recebemos uma planilha em excel, ainda em formato XLS, constando os a tabela atualizada de clientes, a essa denominaremos PLANILHA DE CLIENTES

Desenvolva um serviço com um banco de dados de sua escolha que possa ser atualizado a partir das planilhas citadas anteriormente, onde cada atualização seja submetida a aprovação de um Administrador do Sistema, antes de atualizar ou adicionar dados.

## Sprint 02: Desenvolvimento das Interfaces
Implemente a interface para o usuário final, garantindo um fluxo intuitivo e alinhado com as funcionalidades descritas na Sprint 01. A interface deve permitir que cada usuário acesse as funcionalidades conforme seu nível de permissão, com uma experiência de navegação organizada e eficiente.

## Sprint 03: Integração com Inteligência Artificial
Integre uma camada de Inteligência Artificial que gere relatórios automatizados, proporcionando insights relevantes ao usuário.
Para essa parte final do desafio utilize a API da Open AI para conectar-se ao serviço de inteligência artificial e gerar os seguintes relatórios:
- Meus Clientes
- Operações Ativas
- Operações com Vencimento Hoje

Essa integração deve ser pensada para fornecer informações práticas e em tempo real ao usuário.

Requisitos Não Funcionais
- Não é permitido o uso de CMSs ou plataformas similares para construção do sistema. Esperamos um código personalizado, construído do zero, que se ajuste totalmente às necessidades do desafio.

Especificações Técnicas
- Arquitetura: O sistema deve seguir uma arquitetura cliente/servidor, composta por um back-end e um front-end. A API deve ser RESTful e fornecer dados no formato JSON (in/out)
- Tecnologias: Para linguagem de programação escolha entre Javascript e Python
