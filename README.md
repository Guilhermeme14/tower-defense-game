# 🏰 Tower Defense – Jogo em Python com Pygame

Este é um jogo **Tower Defense** desenvolvido em **Python** utilizando a biblioteca **Pygame**.  
O objetivo é impedir que os inimigos alcancem o final do caminho construindo torres que atacam automaticamente, evoluem e possuem características próprias.

---

## 🎮 Funcionalidades do Jogo

### 🧱 Torres
O jogo possui 3 tipos principais de torres:

| Tipo   | Alcance | Dano | Velocidade de Tiro | Custo |
|--------|---------|------|--------------------|--------|
| Básica | Médio   | Alto | Médio              | 100    |
| Rápida | Baixo   | Médio| Alta               | 150    |
| Sniper | Alto    | Muito Alto | Baixa        | 200    |

- Torres podem ser **evoluídas** (upgrade) aumentando dano e alcance.
- Ao clicar em uma torre, seus detalhes aparecem no painel inferior.
- O alcance da torre selecionada é desenhado visualmente na tela.

---

## 👾 Inimigos

Os inimigos:

- Seguem um caminho pré-definido.
- Têm vida e velocidade diferentes.
- A cada onda ficam mais fortes.
- Eliminá-los concede dinheiro.
- Possuem barras de vida e cores diferentes.

---

## 🌊 Sistema de Ondas

- Cada onda gera inimigos de forma progressiva.
- Tempo de espera entre ondas.
- O número e tipo de inimigos aumenta ao longo do jogo.

---

## 💰 Economia

Você ganha dinheiro ao derrotar inimigos e pode gastar em:

- Construção de torres
- Evolução das torres existentes

Caso um inimigo chegue ao final do caminho, o jogador perde vidas.

---

## 🕹️ Controles

| Ação                | Como Fazer |
|--------------------|------------|
| Selecionar torre   | Clique esquerdo na torre |
| Construir torre    | Clique no botão da torre e depois no mapa |
| Evoluir torre      | Clique direito na torre selecionada |
| Deselecionar torre | Clique esquerdo fora de qualquer torre |

---

## 🎨 Interface do Jogo

- Painel inferior exibindo:
  - Dinheiro
  - Vidas
  - Número da onda
  - Botões de construção das torres
- Detalhes completos da torre selecionada
- Círculo mostrando o alcance da torre

---

## 🚀 Como Executar

### 1. Instale o Python 3.10+


### 2. Instale o pygame
```bash
pip install pygame
```
### 3. Execute o jogo
```bash
python main.py
```

## 🔧 Requisitos

- Python 3.10 ou superior

- Pygame 2.5+

- Windows, Linux ou macOS