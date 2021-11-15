# course_grade_system
Microserviço de controle de notas. A aplicação no qual esse  microsserviço se insere é um aplicativo que permite a uma pessoa cadastrar as disciplinas que está  cursando e suas notas por disciplina. 


Para rodar a entrega final, entrar na pasta "Projetofinal" (entrega para o dia 17/11):
1- Criar um arquivo .env com a seguinte estrutura:
  SQL_SERVER=
  SQL_USER=
  SQL_PASSWORD=
  SQL_DB=projetoFinal
  
2- Fazer pip install de:
  2.1- pymysql
  2.2- sqlalchemy_utils
  
3- Entrar na pasta "sql_app" e rodar o comando: ```python uvicorn main:app --reload```  
