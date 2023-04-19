import uvicorn

from app import ErpigramFastAPI
from src.utils import parse_args
from tests.devmode import refresh_db_data


app = ErpigramFastAPI(title="ErpiGRAM")


def main(args):
    if args.devmode:
        refresh_db_data()
    uvicorn.run("main:app", reload=args.reload)


if __name__ == "__main__":
    main(parse_args())
