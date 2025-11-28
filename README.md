## Grupo: 
### Pedro Ivo Ribeiro Carluccio - 202310519
### Victor Novaes Apude - 202310526

# OS Manager – Sistema de Ordens de Serviço

Este projeto reúne o desenvolvimento completo de uma aplicação para gerenciamento de Ordens de Serviço (OS). A solução integra frontend em Vue e backend em Flask, conectados ao MongoDB Atlas. A ideia foi construir um sistema funcional, direto e fácil de usar, permitindo registrar, listar, editar e excluir OS, além de ter login e cadastro para controlar quem acessa.

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

OSManager/

├── backend/

│ ├── app.py

│ ├── requirements.txt

│ └── (código do servidor)

│

└── interface/

├── src/

├── package.json

└── vite.config.js

Conforme solicitado:
- no backend não foram incluídas as pastas `venv/` e `__pycache__/`
- no frontend não foi incluída a pasta `node_modules/`

---

## 4. Como Instalar e Rodar

Para rodar o projeto completo, é necessário iniciar tanto o backend quanto o frontend. Cada parte funciona separadamente.

---

### **4.1 Backend (Flask)**

Acessar a pasta:

```bash
cd backend
```

Criar o ambiente virtual (opcional):

```bash
python -m venv venv
```

Ativar no Windows:

```bash
venv\Scripts\activate
```

Instalar as dependências:

```bash
pip install -r requirements.txt
```

Configurar a conexão com o MongoDB dentro do app.py.

Iniciar o servidor:

```bash
python app.py
```

O backend ficará disponível em:

http://127.0.0.1:5000

4.2 Frontend (Vue)

Acessar a pasta:

```bash
cd interface
```

Instalar as dependências:

```bash
npm install
```

Iniciar o projeto:

```bash
npm run dev
```

O frontend abre em:

http://localhost:5173

5. Como Utilizar o Sistema

Abra o frontend pelo navegador.

Faça o cadastro e depois o login.

No painel, você pode:

Criar novas OS

Editar informações

Excluir registros

Filtrar por status

Os contadores são atualizados automaticamente conforme você altera ou cria OS.

Para sair da aplicação, basta clicar em Sair.

6. Conclusão

O projeto entrega exatamente o que foi pedido: um sistema completo de controle de Ordens de Serviço, com autenticação, CRUD funcional, conexão com banco de dados na nuvem e interface organizada. Toda a estrutura foi separada adequadamente e a aplicação está pronta para uso.
