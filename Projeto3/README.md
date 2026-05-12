Projeto 3 – Dashboard Grafana

Esse projeto contém o dashboard do Grafana que visualiza os dados do Projeto 2.

Arquivos inclusos:

-> dashboard.json - Arquivo de exportação do dashboard
-> dashboard-print.png - Print da tela do dashboard funcionando

 Pré-requisitos:

-> Grafana instalado e rodando em http://localhost:3000
-> PostgreSQL rodando com o banco monitor populado (Projeto 2)
-> Datasource PostgreSQL já configurado no Grafana apontando para o banco monitor

Como importar o dashboard:

1. Acesse o Grafana no navegador: http://localhost:3000

2. Faca login:
   -> Usuario: admin
   -> Senha: admin (depois redefine se quiser)

3. No menu lateral esquerdo, clique em Dashboards

4. Clique no botao New e depois em Import
   (ou clique diretamente no botao Import se aparecer)

5. No campo Import via dashboard JSON model, faça uma das opções:
   -> Clique em Upload dashboard JSON file e selecione o arquivo dashboard.json
   -> Ou copie o conteudo do arquivo dashboard.json e cole no campo de texto

6. Em seguida, aparecerá a tela de configurações:
   -> Em Name, digite: Monitor de Wallets BSC
   -> Em Folder, pode deixar General
   -> Em Database, selecione o datasource PostgreSQL que você configurou (ex: PostgreSQL Monitor)
   -> Deixe Unique identifier (uid) em branco

7. Clique em Import

O dashboard será carregado e os 4 paineis serão exibidos.

Como configurar o datasource PostgreSQL (se ainda não instalou)

1. No menu lateral, clique no icone de engrenagem (Configuração)
2. Clique em Data sources
3. Clique em Add data source
4. Escolha PostgreSQL
5. Preencha:
   - Name: PostgreSQL Monitor
   - Host: localhost:5433
   - Database: monitor
   - User: meuuser
   - Password: a senha que voce definiu no Projeto 2
   - SSL Mode: disable
   - PostgreSQL Version: 15 (ou a versao do seu)
6. Clique em Save & test
7. Deve aparecer a mensagem Database Connection OK

Ajustar intervalo de tempo após importar

No canto superior direito do dashboard, clique no seletor de tempo e escolha:
- Last 7 days
- Ou Last 14 days

Seus dados devem aparecer nos gráficos.



