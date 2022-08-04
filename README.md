# Trabalho 1 - 2022-1 - FSE

Repositório focado no trabalho 1 da matéria de Fundamentos de Sistemas Embarcados feito utilizando a Raspberry Pi.

## Objetivo

Este trabalho tem como objetivo gerenciar o funcionamento de 4 cruzamentos, controlando a passagem de pedestres e carros, além de monitorar as infrações por velocidade acima do limite permitido e avanço de sinal vermelho. Para um entendimento completo do projeto, sua descrição e requisitos podem ser vistos [aqui](https://gitlab.com/fse_fga/trabalhos-2022_1/trabalho-1-2022-1)


## Descrição

Utilizando a linguagem Python (versão 3) foi criado um Servidor Distribuído, é um Servidor Central.

#### Servidor Distribuído

- Controlar os semáforos
- Controlar o acionamento de botões de passagem de pedestres
- Monitorar o sensor de parada e passagem de carros
- Monitorar a velocidade dos carros na via principal
- Monitorar o número de carros na via principal
- Monitorar as infrações cometidas
- Enviar e receber informações do Servidor Central

#### Servidor Central

- Gerenciar o acionamento dos cruzamentos
- Mostrar as informações, por cruzamento, recebidas do Servidor Distribuído:
    - Número de carros por minuto na via principal
    - Velocidade média da via principal
    - Número de infrações por tipo
- Enviar informações para o Servidor Distribuído para ser acionado o modo noturno, ou o modo de emergência

## Principais bibliotecas utilizadas

- RPi.GPIO (Link da documentação [aqui](https://pypi.org/project/RPi.GPIO/), não vem por padrão no Python 3)
- socket
- threading

# **Requisitos**

Para executar o código necessita-se de um ambiente raspbian, por isso é necessário conectar-se as Raspberry Pi, cujas quais foram utilizadas para desenvolver este projeto.

Além do que precisa-se executar os códigos da **maneira** e na **ordem** que é explicado na seção 'Uso' (abaixo).

## **Uso**

Para executar os comandos abaixo, primeiro precisa-se clonar este repositório e copiá-lo para as duas rasp's, posteriormente acessá-las via conexão 'ssh' e entrar na pasta do projeto transferido.

Trabalhando com duas rasp's, uma delas servirá como servidor central, logo, o IP dessa Rasp terá que ser passado como parâmetro de inicialização nos scripts


- **1°**: Executar o Servidor Central
    - No primeiro terminal, na rasp, execute o comando passando o IP :

```
python3 servidor_central.py numero_IP_da_rasp
```
Exemplo

```
python3 servidor_central.py 164.41.98.26
```

- **2°**: Executar o primeiro Cruzamento como cliente do Servidor Distribuído
    - No segundo terminal, na rasp, execute o comando passado os parâmetros 'cruzamento' e 'IP' de onde está rodando o servidor central:

```
python3 main.py cruzamento_1 numero_IP_servidor_central
```
Exemplo

```
python3 main.py cruzamento_1 164.41.98.26
```

- **3°**: Executar o segundo Cruzamento como cliente do Servidor Distribuído
    - No terceiro terminal, na rasp, execute o comando passado os parâmetros 'cruzamento' e 'IP' de onde está rodando o servidor central:

```
python3 main.py cruzamento_2 numero_IP_servidor_central
```
Exemplo

```
python3 main.py cruzamento_2 164.41.98.26
```

- **4°**: Executar o terceiro Cruzamento como cliente do Servidor Distribuído
    - No quarto terminal, na rasp, execute o comando passado os parâmetros 'cruzamento' e 'IP' de onde está rodando o servidor central:

```
python3 main.py cruzamento_3 numero_IP_servidor_central
```
Exemplo

```
python3 main.py cruzamento_3 164.41.98.26
```

- **5°**: Executar o quarto Cruzamento como cliente do Servidor Distribuído
    - No quinto terminal, na rasp, execute o comando passado os parâmetros 'cruzamento' e 'IP' de onde está rodando o servidor central:

```
python3 main.py cruzamento_4 numero_IP_servidor_central
```
Exemplo

```
python3 main.py cruzamento_4 164.41.98.26
```
No servidor Central, quando ele é executado, uma lista de interações aparece no terminal, mostrando os comandos:

```
1 - Ligar modo de emergencia nos cruzamentos 1 e 2
2 - Desligar modo de emergencia nos cruzamentos 1 e 2
3 - Ligar modo de emergencia nos cruzamentos 3 e 4
4 - Desligar modo de emergencia nos cruzamentos 3 e 4
5 - Ligar modo noturno
6 - Desligar modo noturno
```
**IMPORTANTE** Visualize esses comandos por aqui, pois eles irão aparecer apenas uma vez no terminal.

- **Modo noturno**: Liga o semáforo amarelo em todos os cruzamentos ativos
- **Modo emergência**: Liga o semáforo verde por via principal, ou seja, nos cruzamentos 1 e 2, e/ou, nos cruzamentos 3 e 4.

Feito todos os comandos acima na **ordem**, basta interagir no simulador que se encontra na página de descrição do [Trabalho 1](https://gitlab.com/fse_fga/trabalhos-2022_1/trabalho-1-2022-1)

## Autor

Ian Ferreira.
