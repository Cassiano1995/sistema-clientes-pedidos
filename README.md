# Sistema de Clientes e Pedidos

Sistema CRUD desenvolvido em Python com MySQL, para gerenciamento de clientes, produtos e pedidos, com relacionamento entre tabelas e cálculo automático de valores.

## 📋 Funcionalidades

- Cadastro, listagem, atualização e exclusão de clientes
- Cadastro, listagem, atualização e exclusão de produtos
- Criação de pedidos vinculados a um cliente e um produto
- Cálculo automático do valor total do pedido
- Atualização de status do pedido (pendente, enviado, entregue, cancelado)
- Exclusão de pedidos com remoção em cascata dos itens vinculados

## 🛠 Tecnologias utilizadas

- Python 3.14
- MySQL
- Biblioteca `mysql-connector-python`

## 🗄 Modelagem do banco de dados

O banco possui 4 tabelas relacionadas:

- **clientes**: dados dos clientes
- **produtos**: catálogo de produtos disponíveis
- **pedidos**: pedidos feitos por clientes, com status e valor total
- **itens_pedido**: tabela de ligação entre pedidos e produtos, permitindo relacionamento N:N

## 📁 Estrutura do projeto