from fastapi.openapi.utils import get_openapi


def add_language_header(app):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        for path in openapi_schema["paths"].values():
            for method in path.values():
                parameters = method.setdefault("parameters", [])
                parameters.append(
                    {
                        "name": "accept-language",
                        "in": "header",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "enum": ["en", "fa", "fr", "de"],
                            "default": "en",
                        },
                        "description": "Response language",
                    }
                )

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
