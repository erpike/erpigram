### Quickstart
#### run backend

`python main.py` - start uvicorn app<br/>
`--reload` - reload app on code update<br/>
`--devmode` - clean all db table data and populate by dummy examples<br/>

#### run frontend
`npm start`<br/>

#### docker: 
###### backend
`docker build -t fastapi-backend ./fastapi_backend/`<br/>
`docker run --name erpigram-backend -p 8000:8000 fastapi-backend`<br/>
###### frontend
`docker build -t react-frontend ./react_frontend/`<br/>
`docker run --name erpigram-frontend -p 3000:3000 react-frontend`<br/>
###### docker-compose
`docker-compose up -d --build`