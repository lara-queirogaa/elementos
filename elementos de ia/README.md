# Instruções

Para executar o ficheiro é necessário ter instalado o pygame (versão mais atual de preferência).

Execução em Windows executa-se o código diretamente no VS Code, PyCharm, etc: 
Inicialmente, para abrir o programa é necessário, aceder à pasta onde se encontra o ficheiro (elemntos de ia).
De seguida, temos duas opções de jogo, no terminal ou com interface.

..........
## Terminal
Para executar é entrar no ficheiro chamado "main_terminal.py" e corrê-lo.

1. Escolha de nível:
Escolha um nivel (1-3) ou 'q' para desistir:

2. Após escolher o nível vai mostrar uma matriz inicial, e depois o jogador insere a prateleira inicial e depois seguido de uns espaço a prateleira final. Isto vai mover o número mais à direita da prateleira inicial para a prateleira final.

Este passo é repetisdo até o jogo ser ganho.

3. A qualquer ponto é possível desistir se for inserida a letra q. Isto vai retornar ao ponto 1. Se não for desejado jjogar novamente é só voltar a escrever a letra q.

..........
## Interface
Para executar é entar no ficheiro chamado "interface.py", que se encontra dento da pasta "uteis", e corrê-lo.

Inicialmente vai ter um menu principal onde se vai escolher ou jogar ou regras. Dentro de regras vai existir uma nova página com as regras do jogo e algumas indicações sobre como executar os movimentos.

Dentro do jogar vai aparecer uma nova página onde o jogador tem a escolha do tipo de jogador que deseja, bem como um botão para regressar ao menu principal.

....
Jogador

HUMANO
COMPUTADOR
....

Selecionando qualquer uma das opções, vai aparecer uma nova página com os vários níveis e com a opção de "voltar" que o redireciona para o menu principal.

....
Nível

NÍVEL 1
NÍVEL 2
NÍVEL 3
....

Após a seleção do nível, se foi selecionado o jogador "humano" então pode começar a jogar! Se foi selecionado o jogador "computador", então tem uma opção "próximo" que sempre que for clicada mostrará o próximo movimento realizado pelo computador. Este é calculado usando o algoritmo a*.

Depois do jogo ser ganho é só clicar no "voltar" que vai ser redirecionado para o menu com a escolha dos niveis. 

....
Enquanto o jogador joga, a peça selecionada por este, se for permitida mover, vai ficar a rodeada a amarelo, e depois é só escolher a prateleira para onde a quer mover (tem de ser clicado mesmo na parte de madeira, não no espaço em cima desta. Isto encontra-se explicado também no menu das regras). Se for possivel, a bola vai ser movida, se não for aparece uma mensagem com "Destino inválido".

..........
Trabalho realizado por:
- Ana Maria Martins Alves, up202407579
- Lara Vieira Queiroga, up202406713
- Sofia dos Santos Ribeiro, up202403331

Licenciatura em Inteligência Artificial e Ciência de Dados,
2025