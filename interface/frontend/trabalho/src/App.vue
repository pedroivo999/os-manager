<script>
import axios from "axios";

export default {
  data() {
    return {
      // controle de telas
      tela: "login", // login | register | dashboard

      // login
      email: "",
      senha: "",
      carregando: false,
      erro: "",
      msgSucesso: "",

      // cadastro
      cadEmail: "",
      cadSenha: "",
      cadSenha2: "",

      // auth / dados
      token: "",
      osLista: [],
      filtroStatus: "todas",

      // form OS
      novaOS: {
        numero: "",
        equipamento: "",
        descricao: "",
        status: "Aberta",
        responsavel: "",
        prioridade: "Média"
      },

      // edição
      emEdicao: false,
      numeroOriginalEdicao: null
    };
  },
  computed: {
    osFiltradas() {
      if (this.filtroStatus === "todas") return this.osLista;
      return this.osLista.filter(os => os.status === this.filtroStatus);
    },
    totalOS() {
      return this.osLista.length;
    },
    totalAbertas() {
      return this.osLista.filter(os => os.status === "Aberta").length;
    },
    totalConcluidas() {
      return this.osLista.filter(os => os.status === "Concluída").length;
    }
  },
  methods: {
    // ---------- LOGIN ----------
    async login() {
      this.erro = "";
      this.msgSucesso = "";
      this.carregando = true;
      try {
        const r = await axios.post("http://127.0.0.1:5000/login", {
          email: this.email,
          senha: this.senha
        });

        this.token = r.data.token;
        this.tela = "dashboard";
        await this.carregarOS();
      } catch (e) {
        this.erro = "Credenciais inválidas. Tenta de novo.";
      } finally {
        this.carregando = false;
      }
    },

    logout() {
      this.token = "";
      this.tela = "login";
      this.osLista = [];
      this.senha = "";
      this.email = "";
      this.resetFormOS();
    },

    abrirCadastro() {
      this.tela = "register";
      this.erro = "";
      this.msgSucesso = "";
      this.cadEmail = "";
      this.cadSenha = "";
      this.cadSenha2 = "";
    },

    voltarLogin() {
      this.tela = "login";
      this.erro = "";
      this.msgSucesso = "";
    },

    // ---------- CADASTRO ----------
    async registrar() {
      this.erro = "";
      this.msgSucesso = "";

      if (!this.cadEmail || !this.cadSenha || !this.cadSenha2) {
        this.erro = "Preencha todos os campos.";
        return;
      }

      if (this.cadSenha !== this.cadSenha2) {
        this.erro = "As senhas não conferem.";
        return;
      }

      try {
        await axios.post("http://127.0.0.1:5000/criar_usuario", {
          email: this.cadEmail,
          senha: this.cadSenha
        });

        this.msgSucesso = "Usuário criado com sucesso. Agora faça login.";
        this.email = this.cadEmail;
        this.tela = "login";
      } catch (e) {
        if (e.response && e.response.data && e.response.data.error) {
          this.erro = e.response.data.error;
        } else {
          this.erro = "Erro ao criar usuário.";
        }
      }
    },

    // ---------- OS / DASHBOARD ----------
    async carregarOS() {
      const r = await axios.get("http://127.0.0.1:5000/os", {
        headers: { Authorization: this.token }
      });
      this.osLista = r.data;
    },

    resetFormOS() {
      this.novaOS = {
        numero: "",
        equipamento: "",
        descricao: "",
        status: "Aberta",
        responsavel: "",
        prioridade: "Média"
      };
      this.emEdicao = false;
      this.numeroOriginalEdicao = null;
      this.erro = "";
    },

    async salvarOS() {
      this.erro = "";

      if (!this.novaOS.numero || !this.novaOS.equipamento) {
        this.erro = "Número e equipamento são obrigatórios.";
        return;
      }

      if (this.emEdicao) {
        // edição -> PUT
        await axios.put(
          "http://127.0.0.1:5000/os",
          this.novaOS,
          { headers: { Authorization: this.token } }
        );
      } else {
        // criação -> POST
        await axios.post(
          "http://127.0.0.1:5000/os",
          this.novaOS,
          { headers: { Authorization: this.token } }
        );
      }

      this.resetFormOS();
      await this.carregarOS();
    },

    iniciarEdicao(os) {
      // entra em modo edição e preenche o formulário com a OS selecionada
      this.emEdicao = true;
      this.numeroOriginalEdicao = os.numero;
      this.novaOS = {
        numero: os.numero,
        equipamento: os.equipamento,
        descricao: os.descricao || "",
        status: os.status || "Aberta",
        responsavel: os.responsavel || "",
        prioridade: os.prioridade || "Média"
      };

      // rola a página pro topo do formulário (só pra ficar mais amigável)
      const form = document.querySelector(".card-form-os");
      if (form) form.scrollIntoView({ behavior: "smooth", block: "start" });
    },

    cancelarEdicao() {
      this.resetFormOS();
    },

    async deletarOS(numero) {
      if (!confirm(`Excluir OS ${numero}?`)) return;

      await axios.delete(
        `http://127.0.0.1:5000/os?numero=${numero}`,
        { headers: { Authorization: this.token } }
      );

      if (this.emEdicao && this.numeroOriginalEdicao === numero) {
        this.resetFormOS();
      }

      await this.carregarOS();
    },

    classeStatus(status) {
      switch (status) {
        case "Aberta":
          return "badge badge-open";
        case "Em andamento":
          return "badge badge-progress";
        case "Concluída":
          return "badge badge-done";
        default:
          return "badge";
      }
    }
  }
};
</script>

<template>
  <div class="app-root">
    <div class="app-container">
      <!-- LOGIN -->
      <div v-if="tela === 'login'" class="center-wrapper">
        <div class="card card-login">
          <h1 class="logo">OS Manager</h1>
          <p class="subtitle">Acesse para gerenciar as ordens de serviço.</p>

          <div class="form-group">
            <label>E-mail</label>
            <input v-model="email" placeholder="ex: admin@facamp.com" />
          </div>

          <div class="form-group">
            <label>Senha</label>
            <input v-model="senha" type="password" placeholder="Sua senha" />
          </div>

          <button class="btn btn-primary" @click="login" :disabled="carregando">
            <span v-if="!carregando">Entrar</span>
            <span v-else>Entrando...</span>
          </button>

          <p v-if="erro" class="msg-erro">{{ erro }}</p>
          <p v-if="msgSucesso" class="msg-sucesso">{{ msgSucesso }}</p>

          <p class="hint">
            Não tem conta?
            <button class="link-btn" @click="abrirCadastro">Criar cadastro</button>
          </p>
        </div>
      </div>

      <!-- CADASTRO -->
      <div v-else-if="tela === 'register'" class="center-wrapper">
        <div class="card card-login">
          <h1 class="logo">Criar conta</h1>
          <p class="subtitle">Cadastro de novo usuário do sistema.</p>

          <div class="form-group">
            <label>E-mail</label>
            <input v-model="cadEmail" placeholder="ex: voce@facamp.com" />
          </div>

          <div class="form-group">
            <label>Senha</label>
            <input v-model="cadSenha" type="password" placeholder="Senha" />
          </div>

          <div class="form-group">
            <label>Confirmar senha</label>
            <input v-model="cadSenha2" type="password" placeholder="Repita a senha" />
          </div>

          <button class="btn btn-primary" @click="registrar">
            Cadastrar
          </button>
          <button class="btn btn-secondary btn-inline" @click="voltarLogin">
            Voltar ao login
          </button>

          <p v-if="erro" class="msg-erro">{{ erro }}</p>
        </div>
      </div>

      <!-- DASHBOARD -->
      <div v-else class="dashboard-wrapper">
        <div class="dashboard">
          <header class="topbar">
            <div>
              <h1>Ordens de Serviço</h1>
              <p class="subtitle">Painel de controle de manutenções.</p>
            </div>
            <button class="btn btn-secondary" @click="logout">Sair</button>
          </header>

          <!-- CARDS RESUMO -->
          <section class="resumo">
            <div class="summary-card">
              <span class="summary-label">Total</span>
              <span class="summary-value">{{ totalOS }}</span>
            </div>
            <div class="summary-card">
              <span class="summary-label">Abertas</span>
              <span class="summary-value">{{ totalAbertas }}</span>
            </div>
            <div class="summary-card">
              <span class="summary-label">Concluídas</span>
              <span class="summary-value">{{ totalConcluidas }}</span>
            </div>
          </section>

          <main class="main-grid">
            <!-- FORM NOVA / EDIÇÃO OS -->
            <section class="card card-form-os">
              <h2>{{ emEdicao ? "Editar OS" : "Nova OS" }}</h2>

              <div class="form-grid">
                <div class="form-group">
                  <label>Número</label>
                  <input
                    v-model="novaOS.numero"
                    placeholder="ex: 001"
                  />
                </div>

                <div class="form-group">
                  <label>Equipamento</label>
                  <input
                    v-model="novaOS.equipamento"
                    placeholder="ex: Ar-condicionado"
                  />
                </div>

                <div class="form-group">
                  <label>Responsável</label>
                  <input
                    v-model="novaOS.responsavel"
                    placeholder="ex: Técnico João"
                  />
                </div>

                <div class="form-group">
                  <label>Prioridade</label>
                  <select v-model="novaOS.prioridade">
                    <option>Baixa</option>
                    <option>Média</option>
                    <option>Alta</option>
                  </select>
                </div>

                <div class="form-group form-full">
                  <label>Descrição</label>
                  <textarea
                    v-model="novaOS.descricao"
                    rows="4"
                    placeholder="Descreva o problema com detalhes..."
                  ></textarea>
                </div>

                <div class="form-group form-full">
                  <label>Status</label>
                  <select v-model="novaOS.status">
                    <option>Aberta</option>
                    <option>Em andamento</option>
                    <option>Concluída</option>
                  </select>
                </div>
              </div>

              <div class="actions-row">
                <button class="btn btn-primary" @click="salvarOS">
                  {{ emEdicao ? "Salvar alterações" : "Salvar OS" }}
                </button>
                <button
                  v-if="emEdicao"
                  class="btn btn-secondary btn-inline"
                  @click="cancelarEdicao"
                >
                  Cancelar edição
                </button>
              </div>

              <p v-if="erro" class="msg-erro">{{ erro }}</p>
            </section>

            <!-- LISTA DE OS -->
            <section class="card">
              <div class="lista-header">
                <h2>Lista de OS</h2>
                <select v-model="filtroStatus" class="select-filtro">
                  <option value="todas">Todas</option>
                  <option value="Aberta">Abertas</option>
                  <option value="Em andamento">Em andamento</option>
                  <option value="Concluída">Concluídas</option>
                </select>
              </div>

              <div class="tabela-wrapper" v-if="osFiltradas.length">
                <table class="tabela-os">
                  <thead>
                    <tr>
                      <th>Nº</th>
                      <th>Equipamento</th>
                      <th>Responsável</th>
                      <th>Prioridade</th>
                      <th>Status</th>
                      <th>Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="os in osFiltradas" :key="os.numero">
                      <td>{{ os.numero }}</td>
                      <td>{{ os.equipamento }}</td>
                      <td>{{ os.responsavel || "-" }}</td>
                      <td>{{ os.prioridade || "-" }}</td>
                      <td>
                        <span :class="classeStatus(os.status || 'Aberta')">
                          {{ os.status || "Aberta" }}
                        </span>
                      </td>
                      <td class="acoes">
                        <button class="btn btn-small" @click="iniciarEdicao(os)">
                          Editar
                        </button>
                        <button
                          class="btn btn-small btn-danger"
                          @click="deletarOS(os.numero)"
                        >
                          Excluir
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <p v-else class="vazio">
                Nenhuma OS cadastrada ainda. Cria uma do lado.
              </p>
            </section>
          </main>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
:root {
  color-scheme: dark;
}

body {
  margin: 0;
  background: #050509;
  color: #f5f5f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.app-root {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: stretch;
}

.app-container {
  flex: 1;
  display: flex;
  justify-content: center;
}

.center-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-login {
  width: 500px;
}

/* Cards / inputs */

.logo {
  margin: 0 0 4px;
}

.subtitle {
  margin: 0 0 16px;
  color: #bbbbbb;
  font-size: 0.9rem;
}

.form-group {
  margin-bottom: 12px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-size: 0.85rem;
  color: #c7c7c7;
}

input,
select,
textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid #343434;
  background: #121218;
  color: #f5f5f5;
  outline: none;
  font-size: 0.9rem;
}

input:focus,
select:focus,
textarea:focus {
  border-color: #4caf50;
}

textarea {
  resize: vertical;
  min-height: 150px;
}

.card {
  background: #111119;
  padding: 18px 20px;
  border-radius: 12px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
}

.btn {
  border: none;
  cursor: pointer;
  border-radius: 999px;
  padding: 8px 18px;
  font-weight: 600;
  font-size: 0.9rem;
}

.btn-primary {
  background: linear-gradient(135deg, #4caf50, #76ff7a);
  color: #020204;
}

.btn-secondary {
  background: #252533;
  color: #f5f5f5;
}

.btn-danger {
  background: #e53935;
  color: #fff;
}

.btn-small {
  padding: 4px 10px;
  font-size: 0.8rem;
}

.btn-inline {
  margin-left: 8px;
}

.btn:disabled {
  opacity: 0.7;
  cursor: default;
}

.actions-row {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.msg-erro {
  margin-top: 8px;
  color: #ff7676;
  font-size: 0.85rem;
}

.msg-sucesso {
  margin-top: 8px;
  color: #76ff7a;
  font-size: 0.85rem;
}

.hint {
  margin-top: 14px;
  font-size: 0.8rem;
  color: #9b9b9b;
}

.link-btn {
  border: none;
  background: none;
  color: #76ff7a;
  font-size: 0.85rem;
  cursor: pointer;
  padding: 0 0 0 2px;
}

/* DASHBOARD */

.dashboard-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.dashboard {
  max-width: 1350px;          /* mais largo */
  width: 100%;
  margin: 40px auto 48px;     /* mais afastado do topo e centralizado */
  padding: 0 32px 40px;       /* mais respiro nas laterais */
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.resumo {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.summary-card {
  background: #151521;
  padding: 10px 14px;
  border-radius: 10px;
  border: 1px solid #262637;
}

.summary-label {
  display: block;
  font-size: 0.75rem;
  color: #a3a3b3;
  margin-bottom: 4px;
}

.summary-value {
  font-size: 1.4rem;
  font-weight: 700;
}

.main-grid {
  display: grid;
  grid-template-columns: 1.9fr 1.6fr;  /* AUMENTA a coluna do form */
  gap: 24px;
  align-items: flex-start;
  justify-content: center;
}

.card-form-os {
  min-width: 500px;  
}


.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

@media (min-width: 1100px) {
  .form-grid {
    grid-template-columns: 1fr 1fr;  /* só em tela grande */
  }

  .form-full {
    grid-column: 1 / -1;
  }
}

.form-full {
  grid-column: 1 / -1;
}

.lista-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.select-filtro {
  max-width: 160px;
}

/* TABELA */

.tabela-wrapper {
  max-height: 360px;
  overflow: auto;
  border-radius: 10px;
  border: 1px solid #262637;
}

.tabela-os {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.tabela-os thead {
  background: #181824;
}

.tabela-os th,
.tabela-os td {
  padding: 8px 10px;
  text-align: left;
}

.tabela-os tbody tr:nth-child(even) {
  background: #101017;
}

.vazio {
  margin-top: 10px;
  font-size: 0.85rem;
  color: #9b9b9b;
}

.acoes {
  display: flex;
  gap: 6px;
}

/* BADGES */

.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 0.75rem;
}

.badge-open {
  background: rgba(255, 193, 7, 0.15);
  color: #ffc107;
}

.badge-progress {
  background: rgba(33, 150, 243, 0.15);
  color: #42a5f5;
}

.badge-done {
  background: rgba(76, 175, 80, 0.15);
  color: #81c784;
}

/* RESPONSIVO */

@media (max-width: 900px) {
  .main-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .resumo {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 600px) {
  .dashboard {
    margin-top: 16px;
  }

  .topbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .resumo {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}


/* ==== CENTRALIZAÇÃO GERAL ==== */

/* garante que o fundo ocupe a tela toda */
body {
  margin: 0;
  background: #050509;
  color: #f5f5f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* o elemento raiz do Vue */
#app {
  min-height: 100vh;
  display: flex;
  justify-content: center;   /* centro horizontal */
  align-items: flex-start;   /* topo da tela, mas alinhado ao centro */
}

/* wrappers que você criou lá no template */
.app-root,
.app-container,
.dashboard-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;   /* joga o conteúdo pro centro SEM DISCUSSÃO */
}

/* o bloco que realmente contém tudo da tela logada */
.dashboard {
  max-width: 1350px;
  width: 100%;
  margin: 40px auto 48px;    /* auto = centraliza */
  padding: 0 32px 40px;
}



</style>
