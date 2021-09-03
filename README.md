<p align="center"><img src="https://media.discordapp.net/attachments/879862259273302016/883364906643120158/RPG.png"></p>
<h1 align="center">Merlin - Alternative Role Playing Game</h1>
<p align="center">Auxiliar de jogadores de RPG interpretativo</p>
<p align="center"> desenvolvido e testado no PyCharm 2021.2 / Python 3.8</p>

<p align="center">
 <a href="#objetivo">Objetivo</a> •
 <a href="#comandos">Comandos</a> • 
 <a href="#requisitos">Requisitos</a> • 
 <a href="#autor">Autor</a>
</p>

### Objetivo
---
<a>Este projeto tem como objetivo auxiliar jogadores de RPG interpretativo, aumentando a imersão através de recursos do discord</a>
<p>Inicialmente baseado no jogo tibia.com, porém pode utilizar a base que achar melhor</p>

* Salva a ficha do usuário, podendo consultar a qualquer momento
* Inventario do personagem
* Equipamentos do personagem
* Combate com monstros
* Entre outros recursos

### Requisitos
---


<p>É necessário a criação das tags "aguardando aprovação", "verificado", "cadastrado" e "em recuperação"</p>

* aguardando aprovação: tag dada automaticamente ao jogador quando entra no grupo
* verificado: dado manualmente por um administrador, após aprovar o membro a utilizar os canais
* cadastrado: tag dada automaticamente após criação do cadastro, necessário para utilizar os comandos do bot
* em recuperação: dado automaticamente após jogador estar com 0 de vida

<p> Criação de um chat específico para utilizar os comandos e respostas do bot, configurado em const/ANUNCIO_ID
<h1 align="center">
  <img src="./how_use/tags_necessarias.png" />
</h1>


### Comandos
---
* !cadastrar Nome, Raca, Classe, Idade, link_foto -> Realizar cadastro da sua ficha
* !consultar cadastro -> Verificar cadastro atual
* !deletar cadastro -> Deleta totalmente seu cadastro
<img src="./how_use/comandos_cadastro.png" />

* !meu status -> Consultar status do personagem
<img src="./how_use/consulta_status.png" />

* !gerar "Nome" -> Gera um monstro conforme nome selecionado, baseado na lista de monstros do arquivo json/monstros.json
<img src="./how_use/respawn.png" />

* !atacar "Nome" -> ataca um monstro que esteja disponível no jogo, irá girar os dados, 1/20, 10+ sucesso | 10- falha
<img src="./how_use/atacar_diceWin.png" />

* caso perca, seu ataque é cancelado e passa a vez ao atacado
<img src="./how_use/atacar_diceLose.png" />

* caso sua vida chegue a 0, é enviado para enfermaria, a partir deste momento jogador fica inápto a jogar
<img src="./how_use/vida_zero.png" />

* caso mate a criatura, irá receber o xp e o loot ficará disponível para pegar
<img src="./how_use/defeat_mob.png" />

* !pegar ID -> para pegar um item e por no inventário, basta informar o ID do item
<img src="./how_use/pegar_item.png" />

* !loot disponivel -> consultar a lista de itens ainda disponível no chão
<img src="./how_use/loot_disponivel.png" />

* !meu inventario -> consultar os itens coletados em seu inventário
<img src="./how_use/inventario.png" />

* !meu set -> consultar os itens no set do personagem
<img src="./how_use/consultar_set.png" />

* !equipar ID -> para trocar seu equipamento, basta informar o ID do item que está em seu inventário
<img src="./how_use/equipar.png" />

### Autor
---
<p><b>Marcos Pacheco</b></p>

Contato:
<p>discord: Marcos#9999</p>
