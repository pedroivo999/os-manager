## Grupo: 
### Pedro Ivo Ribeiro Carluccio - 202310519
### Victor Novaes Apude - 202310526

# OS Manager – Sistema de Ordens de Serviço

Este projeto reúne o desenvolvimento completo de uma aplicação para gerenciamento de Ordens de Serviço (OS). A solução integra frontend em **Vue** e backend em **Flask**, conectados ao **MongoDB Atlas**. A ideia foi construir um sistema funcional, direto e fácil de usar, permitindo registrar, listar, editar e excluir OS, além de ter login e cadastro para controlar quem acessa.

---

## 1. Funcionalidades da Aplicação

A aplicação foi organizada para que qualquer pessoa consiga usar sem complicação. Entre as principais funções:

### **Autenticação**
- Cadastro de novos usuários  
- Login com verificação dos dados  
- Encerrar sessão com botão *Sair*

### **Ordens de Serviço**
- Criar novas OS informando número, equipamento, responsável, prioridade, descrição e status  
- Editar OS já cadastradas  
- Excluir OS  
- Filtrar por status (todas, abertas, concluídas)  
- Contadores automáticos mostrando:
  - Total de OS
  - Quantas estão abertas
  - Quantas foram concluídas

A interface foi feita em modo escuro, com tela dividida entre formulário e tabela, deixando tudo mais limpo e confortável de visualizar.

---

## 2. Tecnologias Utilizadas

O sistema foi separado em dois projetos independentes:

### **Backend – Flask**
- Python  
- Flask  
- Flask-CORS  
- PyMongo  
- MongoDB Atlas  

### **Frontend – Vue + Vite**
- Vue.js 3  
- Axios  
- CSS customizado em modo dark  

---

## 3. Estrutura do Projeto

A estrutura geral segue o padrão abaixo:
