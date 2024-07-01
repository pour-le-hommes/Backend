import os
import logging
from fastapi.middleware import Middleware, cors
from fastapi import FastAPI, Depends, HTTPException
from typing import List

from api_v1.utils.user_logging import setup_logging
from api_v1.utils.database import init_db

from api_v1.endpoints.health import health_router
from api_v1.endpoints.lifeup.lifeup_main import lifeup_router
from api_v1.endpoints.models.cloudflare import cf_router
from api_v1.endpoints.models.gemini import gemini_router
from api_v1.endpoints.models.groq import groq_router

def init_routers(app_:FastAPI)-> None:
    try:
        app_.include_router(health_router)
        app_.include_router(lifeup_router)
        app_.include_router(cf_router)
        app_.include_router(gemini_router)
        app_.include_router(groq_router)
    except Exception as e:
        message = "The initialization of routers isn't working: "+str(e)
        raise HTTPException(status_code=500,detail=message)

def make_middleware() -> List[Middleware]:
    try:
        middleware = [
            Middleware(
                cors.CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"]
            )
        ]
        return middleware
    except Exception as e:
        message = "The initialization of middlewares isn't working:"+str(e)
        raise HTTPException(status_code=500,detail=message)

def create_app() -> FastAPI:
    try:
        init_db()
        setup_logging()
        app_ = FastAPI(
            title="Personal Database and Endpoints",
            description="The database (Supabase) and Backend",
            version="1.23.17066",
            middleware=make_middleware(),
            swagger_ui_parameters ={
                "docExpansion":"none",
                "syntaxHighlight.theme": "obsidian",
            },
        )
        init_routers(app_=app_)
        return app_
    except Exception as e:
        # Log the error and decide how to handle it
        logging.exception("Failed to initialize the application: %s", e)
        # You could raise an HTTPException or return a minimal app
        raise HTTPException(status_code=500, detail="Failed to initialize the application")

try:
    app = create_app()
except Exception as e:
    message = "The initialization of the whole thing isn't working:",e
    print(message)