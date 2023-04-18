import uvicorn

from app import ErpigramFastAPI
from src.utils import parse_args


app = ErpigramFastAPI(title="ErpiGRAM")


def main(args):
    uvicorn.run("main:app", reload=args.reload)


if __name__ == "__main__":
    main(parse_args())
