# Serverless Home Challenge
### Project Overview

Esse documento descreve o passo a passo para configuração e teste das APIs desenvolvidas para o projeto TODO list. O projeto fornece endpoints para manipulação de itens de uma lista de tarefas. A sessão "anexos" deste documento contém um arquivo de collections do Postman, descrevendo todos os endpoints e conténdo os payloads e demais configurações necessárias para seu uso. Os requisitos referentes ao desenvolvimento deste projeto estão descritos [neste documento].

Diagrama de visão geral da aplicação: [draw io]

**Importante:** Para validação deste projeto poderão ser utilizados os seguintes caminhos:

**1-** Utilizando os endpoints que já estão hospedados em ambiente AWS na conta do desenvolvedor do projeto (André Vinícius). Para seguir com este caminho, nenhum setup adicional é necessário, dado que a API (API Gateway), funções Lambda e banco de dados DynamoDB já estão hospedados e prontos para uso. Essa API somente receberá requisições contendo uma API-key válida, que já está configurada como uma variável de collection do Postman fornecida na sessão "anexos" e é necessária em todos os endpoints. 

**2-** Fazendo deploy do projeto em qualquer conta AWS. A configuração de todos os recursos foi feita via Serverless Framework. O projeto está pronto para ser implantado de forma automatizada e as instruções estão fornecidas na sessão "setup". 

**3-** Testes locais: Neste projeto utilizou-se o plugin serverless-offline, que permite um ciclo de desenvolvimento e testes mais rápidos por meio de endpoints rodando em ambiente local, sem necessidade de publicação em ambiente AWS a todo momento.

**Importante:** Independemente de qual caminho de validação será utilizado, ressalta-se que o projeto também conta um conjunto de testes unitários a fim de validar o comportamento das funções Lambda envolvidas. Para isso utilizou-se a biblioteca "pytest" juntamente com a biblioteca "moto" para simulação do comportamento de serviços AWS. 

> Note: Recomendo fortemente o uso do Software Postman [link] para validação dos endpoints utilizando as collections fornecidas, que já estão configuradas para uso.

### Setup Guide
##### Testes utilizando a API já hospedada
Como mencionado anteriormente, para seguir este caminho de validação basta fazer o download da collection do Postman disponível na sessão "anexo". **Importante:** O caminho raíz da collection (Serverless Home Challenge - TODO List) contém uma descrição geral do serviço e contém um link de conteúdo **"View complete documentation"**, cujo conteúdo descreve detalhadamente cada um dos endpoints disponíveis, campos e formatos exigidos e exemplos de payloads válidos e inválidos.

##### Fazer deploy automatizado em ambiente AWS
Para seguir com a configuração do projeto na sua própria conta AWS, siga o passo-a-passo abaixo:
###### Pré requisitos (por favor não avance para a etapa de setup antes de validar os seguintes itens): 
Conta AWS criada; 
Node JS instalado (necessário para execução dos comandos do Serverless Framework);
Python a partir da versão 3.10 (necessário caso queira rodar os endpoints de API localmente por meio do serverless-offline plugin);
Usuário IAM da AWS configurado para acesso programático via Access Keys. **Caso ainda não tenha esse usuário AWS com acesso programático configurado**, execute os seguintes passos:
 - Dentro de sua conta AWS, acesse o console do serviço IAM
 - Em "users", clique em "create user", forneça um nome de sua preferência e avance
 - Na tela seguinte, selecione "Attach policies directly" e inclua a policy "AdministratorAccess". Essa policy deverá ser utilizada apenar em ambientes de testes para simplificar o processo de validação dos endpoints. Por razões de segurança ela não deverá ser utilizada em ambiente de produção e deverá ser substituida por uma que tenha apenas os acessos necessários. 
 - Avance para a tela de revisão e conclua a criação do usuário.
 - De volta à tela de listagem de usuários, selecione o usuário que você acabou de criar, acesse a aba "Security Credentials" e clique no botão "Create Access Key". Em "use case", Selecione a opção "Command Line Interface (CLI)" e marque a caixa de confirmação. Após confirmar o procedimento, você receberá os valores de "Access Key" e "Secret access key". Eles serão necessários para a configuração do Serverless Framework, permitindo que o mesmo faça deploy de recursos em sua conta AWS. 
    
###### Setup do ambiente: 
 - Realize o download deste projeto utilizando o meio de sua preferência (Git Clone ou download .zip file)
 - Utilizando um terminal, execute o comando `npm i serverless -g`. Isso instalará o serverless framework em sua máquina e o tornará acessível a partir de qualquer diretório.
 - Crie um usuário na AWS e habilite as Access Keys.
 - Acesse o diretório raiz do projeto baixado e execute o comando `serverless config`. 
 - Ainda no diretório raiz do projeto, faça a instalação dos plugins necessários, através dos comandos `npm install serverless-offline --save-dev` e `npm install serverless-python-requirements` 
 - Para seguir com o deploy, execute o comando `serverless deploy` 

###### Ajustes finais: 
Neste ponto sua aplicação já deve estar hospedada em sua conta AWS e pronta para uso. Para consultar seu endpoint de requisições, acesse sua conta AWS e, no serviço Amazon API Gateway, selecione a API que acabou de ser criada (serverless-challenge). No menu lateral, acesse "stages". Nesse tela, copie o valor de "Invoke URL". Essa será a URL de base para todas as chamadas em sua API. 

A partir daqui, basta abrir a Postman collection fornecida e atualizar o valor da variável "serverless_api_challenge_url". Para isso, na raiz da collection, basta acessar a aba "variables" e substituir os campos "initial value" e "current value" com a sua URL de invocação, conforme mostrado abaixo:
[print 1]
[print 2]

> Note: Utilizando o método de deploy em sua própria conta, não será necessário o uso de API keys nas requisições, pois essa configuração não faz parte do template fornecido no projeto e foi configurada separadamente.

##### Testes locais
1) Testes unitários - setup:
 - Dentro do diretório "serverless-home-challenge", executar os comandos `pip install -r requirements.txt`. Isso irá configurar as bibliotecas pytest, moto e boto3.
 - Após a instalação das bibliotecas, basta executar o comando `pytest`, que identificará automaticamente todos os arquivos de teste (localizados no diretório "tests" e executará todos os casos descritos). Em cada um dos casos, há uma descrição da funcionalidade a ser testada.

2) Além dos testes unitários, pode-se usar o serverless-offline para testar suas APIs localmente. Para isso, basta acessar o diretório serverless-home-challenge e executar o comando `serverless offline`. Isso viabilizará testes locais utilizando por padrão o endereço localhost:3000 como url base de suas APIs. 





[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)




