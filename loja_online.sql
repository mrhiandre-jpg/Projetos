-- 1. Criar o banco de dados
CREATE DATABASE loja_online;
USE loja_online;

-- 2. Criar tabela de clientes
CREATE TABLE CLIENTES (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    NOME VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) UNIQUE,
    TELEFONE VARCHAR(20),
    DATA_CADASTRO DATE
);

-- 3. Criar tabela de produtos
CREATE TABLE PRODUTOS (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    NOME VARCHAR(100) NOT NULL,
    DESCRICAO TEXT,
    PRECO DECIMAL(10, 2) NOT NULL,
    ESTOQUE INT DEFAULT 0
);

-- 4. Criar tabela de pedidos
CREATE TABLE PEDIDOS (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ID_CLIENTE INT NOT NULL,
    DATA_PEDIDO DATE,
    VALOR_TOTAL DECIMAL(10, 2),
    FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID)
);

-- 5. Inserir dados de clientes
INSERT INTO CLIENTES (NOME, EMAIL, TELEFONE, DATA_CADASTRO)
VALUES 
('João Silva', 'joao@email.com', '11987654321', '2024-01-10'),
('Maria Santos', 'maria@email.com', '11987654322', '2024-01-12'),
('Pedro Oliveira', 'pedro@email.com', '11987654323', '2024-01-15');

-- 6. Inserir dados de produtos
INSERT INTO PRODUTOS (NOME, DESCRICAO, PRECO, ESTOQUE)
VALUES 
('Notebook', 'Notebook Intel i7', 3500.00, 10),
('Mouse', 'Mouse sem fio', 50.00, 50),
('Teclado', 'Teclado mecânico', 150.00, 25);

-- 7. Inserir dados de pedidos
INSERT INTO PEDIDOS (ID_CLIENTE, DATA_PEDIDO, VALOR_TOTAL)
VALUES 
(1, '2024-01-20', 3550.00),
(2, '2024-01-22', 200.00),
(1, '2024-01-25', 150.00);

-- 8. Consultar os dados
SELECT * FROM CLIENTES;
SELECT * FROM PRODUTOS;
SELECT * FROM PEDIDOS;