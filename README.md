# GameLog-Backend
Backend section for GameLog
rodar: uvicorn app.main:main --reload

- Alembic:
  1. Criar conexão no MySQL:
     1. -> nome: localhost / username: root / senha: admin / porta: 3306
  2. Criar base de dados no script MySQL:
     1. -> create database db_Gamelog;
     2. usar base de dados -> use db_Gamelog;
  3. Scripts para rodar via CMD para criar as tabelas:
     # EXECUTAR NA RAÍZ DO PROJETO (gamelog/)
     1. alembic revision --autogenerate -m "create tables"
     2. aplicar upgrade -> alembic upgrade head
     3. voltar -> alembic downgrade -1
