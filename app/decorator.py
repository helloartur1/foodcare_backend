from functools import wraps
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

def handle_db_exceptions(func):
    """Декоратор для обработки исключений БД в методах DAO"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            # Пробрасываем HTTPException без изменений
            raise
        except SQLAlchemyError as e:
            # Логируем ошибки БД
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            # Обрабатываем все остальные исключения
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return wrapper

def handle_api_exceptions(func):
    """Декоратор для обработки исключений в API endpoints"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return wrapper