# Sistema de Gestão de Hogwarts (CRUD)

Este é um sistema de gerenciamento escolar desenvolvido em Python utilizando banco de dados SQLite.

## Demonstração Online

Clique no botão abaixo para testar o código diretamente no navegador via Replit, sem a necessidade de baixar arquivos:

[![Run on Replit](https://binbashbanana.github.io/deploy-buttons/buttons/remade/replit.svg)](https://replit.com/@mrhiandre/Projetos)

## Contexto do Projeto

Desenvolvi este algoritmo para solucionar um problema de organização durante uma campanha de RPG de mesa baseada no universo de Harry Potter, a qual eu narrava. Na época, enfrentei dificuldades para gerenciar o grande volume de NPCs (personagens não jogáveis) e manter a consistência de suas informações. O sistema foi criado para automatizar e organizar esses dados de forma eficiente.

## Funcionalidades Atuais

O sistema opera via terminal e permite a gestão completa do banco de dados escolar, incluindo:

* **Professores:** Cadastro, demissão e atualização de matéria lecionada.
* **Casas:** Criação de casas e gerenciamento de coordenadores (com restrição `UNIQUE` para garantir um coordenador por casa).
* **Alunos:** Matrícula, promoção de ano letivo e desligamento. Inclui um `TRIGGER` no banco de dados para impedir a troca de casa após a seleção inicial (regra de negócio do universo).
* **Anos Letivos:** Criação e estruturação do currículo escolar.

## Tecnologias Utilizadas

* Python 3
* SQLite3 (Biblioteca nativa do Python)

## Próximos Passos (Roadmap)

Planejo expandir o sistema com as seguintes funcionalidades:

* **Visualização de Dados:** Implementar relatórios em tabelas para listar todos os registros.
* **Sistema de Busca:** Criar filtros para localizar alunos ou professores específicos.
* **Interface Gráfica (GUI):** Desenvolver uma interface visual para substituir o uso do terminal.
* **Análise de Dados:** Gerar gráficos de desempenho e distribuição dos alunos.
* **Gestão Acadêmica:** Adicionar tabelas para controle de notas, frequências e matérias específicas.

## Como Executar

Para rodar o projeto localmente:

1.  Certifique-se de ter o Python 3 instalado.
2.  Clone o repositório.
3.  Execute o arquivo principal:
    ```bash
    python CRUD_HP.py
    ```
4.  O banco de dados `hogwarts.db` será criado automaticamente na primeira execução.


## Disclaimer (Aviso Legal)

Este projeto foi desenvolvido apenas para fins educacionais e de aprendizado.

* **Harry Potter** e todos os nomes, personagens e elementos relacionados são marcas registradas e propriedade intelectual de **J.K. Rowling** e **Warner Bros. Entertainment Inc.**
* Este projeto não possui fins lucrativos e não é afiliado, endossado ou patrocinado pelos detentores dos direitos autorais.


---
**Autor:** [Rhiandre Alcantara Viera Marques]
---
