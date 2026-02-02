from fastapi import FastAPI
from contextlib import asynccontextmanager
from expenses.routes import router as expenses_routes
from users.routes import router as users_routes


tags_metadata = [
    {
        "name": "expenses",
        "description": "API for managing expenses with FastAPI",
        "externalDocs": {
            "description": "My GitHub",
            "url": "https://github.com/shahinabbasidev"
        }
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")


app = FastAPI(
    title="Expenses management application",
    description="This is a section of description",
    version="0.0.1",
    contact={
        "name": "Shahin Abbasi",
        "url": "https://github.com/shahinabbasidev",
        "email": "shahin.abbasi.dev@gmail.com",
    },
    license_info={"name": "MIT"},
    lifespan=lifespan,
    openapi_tags=tags_metadata
)

app.include_router(expenses_routes)
app.include_router(users_routes)

