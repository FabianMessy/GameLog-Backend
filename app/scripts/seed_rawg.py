import argparse

from sqlmodel import Session

from app.core.database import create_db, engine
from app.services.rawg_import_service import importar_jogos_rawg


def main():
    parser = argparse.ArgumentParser(
        description="importa jogos da api rawg para o banco sqlte do GameLog."
    )
    parser.add_argument(
        "--search",
        default=None,
        help="termo de busca. Exemplo: minecraft, gta, hollow knight.",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="quant de pag da RAWG para importar",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=10,
        help="quant de jogos por pag. max recomendado: 40",
    )

    args = parser.parse_args()

    create_db()

    with Session(engine) as session:
        resultado = importar_jogos_rawg(
            session=session,
            search=args.search,
            pages=args.pages,
            page_size=args.page_size,
        )

    print("importacao rawg suscesdida.")
    print(f"importados: {resultado['importados']}")
    print(f"ignorados: {resultado['ignorados']}")

    if resultado["erros"]:
        print("Erros:")
        for erro in resultado["erros"]:
            print(f"- {erro}")

#ex de codigo do cmd para colar
#python -m app.scripts.seed_rawg --pages 1 --page-size 10

if __name__ == "__main__":
    main()