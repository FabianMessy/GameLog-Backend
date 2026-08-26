# GameLog-Backend
Backend section for GameLog
rodar: uvicorn app.main:main --reload

- Alembic:
  1. Criar conexão no MySQL:
     a. -> nome: localhost / username: root / senha: admin / porta: 3306
  2. Criar base de dados no script MySQL:
     a. -> create database db_Gamelog;
     b. usar base de dados -> use db_Gamelog;
  3. Scripts para rodar via CMD para criar as tabelas:
     a. alembic revision --autogenerate -m "create tables"
     b. aplicar upgrade -> alembic upgrade head
     c. voltar -> alembic downgrade -1
