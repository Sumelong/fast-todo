from fastapi import FastAPI
from presentation import TodoApiRouter
from presentation import TodoWebRouter
from configs import EntityBase, DBEngine


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     DBModel.metadata.create_all(DBEngine)
#     yield
#     DBEngine.dispose()


app = FastAPI()
EntityBase.metadata.create_all(DBEngine)

app.include_router(TodoApiRouter)
app.include_router(TodoWebRouter)
