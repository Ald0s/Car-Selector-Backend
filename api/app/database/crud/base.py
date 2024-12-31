"""Base CRUD generic implementation - supports async"""
import logging

from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy import select, delete, insert, func, exists, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.logger import log as LOG
from .. import errors, compat
from ..basemodel import Model

ModelType = TypeVar("ModelType",
    bound = Model)
CreateSchemaType = TypeVar("CreateSchemaType",
    bound = BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType",
    bound = BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """The base type that provides common functionality for CRUD operations.
    """
    def __init__(self, model_type: Type[ModelType]):
        self._ModelTypeCls = model_type

    async def total_count(self, sesh: AsyncSession) -> int:
        """Return the total number of this model in database."""
        select_stmt = (
            select(func.count("*"))
                .select_from(self._ModelTypeCls)
        )
        select_result = await sesh.execute(select_stmt)
        return select_result.scalar()
    
    async def exists(self, sesh: AsyncSession, id: Any) -> bool:
        """Return True if the model represented by this base has an instance
        stored with the given value.
        """
        try:
            exists_stmt = (
                select(True)
                    .where(
                        select(self._ModelTypeCls)
                            .where(self._ModelTypeCls.id == id)
                            .exists()
                    )
            )
            exists_result = await sesh.execute(exists_stmt)
            return exists_result.scalar()
        except Exception as e:
            raise e
        
    async def get(self, sesh: AsyncSession, id: Any) -> Optional[ModelType]:
        """Get the an instance of the model type with its ID. The model type
        must have an attribute named 'id' that matches the given ID. If this
        is not the case, the subtype must implement a separate get function
        operable on the desired ID(s).
        
        Arguments
        ---------
        :sesh: The database session on which to query the model.
        :id: The ID with which to query the model.
        """
        try:
            select_stmt = (
                select(self._ModelTypeCls)
                    .where(self._ModelTypeCls.id == id)
            )
            result = await sesh.execute(select_stmt)
            return result.scalar()
        except Exception as e:
            raise e
        
    async def upsert(
        self, 
        sesh: AsyncSession, 
        create_obj: Union[ModelType, CreateSchemaType], 
        *,
        commit: bool = False
    ) -> ModelType:
        try:
            """TODO implement a generic upsert that can work across the board,
            perhaps by actually selecting all primary keys.
            """
            raise NotImplementedError
        except Exception as e:
            raise e
    
    async def create(
        self, 
        sesh: AsyncSession,
        create_obj: Union[dict, ModelType, CreateSchemaType], 
        *,
        commit: bool = False
    ) -> ModelType:
        """A base implementation of creating the desired model type from
        a pydantic creation schema type.
        
        Arguments
        ---------
        :sesh: The database session on which to create the new object.
        :create_obj: A pydantic model, or a dict containing data that can be
                     loaded straight into a new instance of model type.
        
        Keyword arguments
        -----------------
        :commit: Whether commit should be used. If False, flush will be used.
                 Default is False.
        """
        try:
            if not create_obj:
                raise ValueError
            
            if isinstance(create_obj, dict):
                create_obj = CreateSchemaType(**create_obj)
            elif not isinstance(create_obj, BaseModel):
                raise TypeError
            
            new_obj = self._ModelTypeCls(**create_obj.model_dump())
            sesh.add(new_obj)
            if commit:
                await sesh.commit()
            else:
                await sesh.flush()
            return new_obj
        except IntegrityError as ie:
            # If this is a unique violation, raise object exists.
            if compat.check_for_unique_violation(ie):
                # Primary key is duplicate. Instead submit an update.
                raise errors.ObjectAlreadyExistsException(create_obj)
            raise ie
        except Exception as e:
            raise e
    
    async def update(
        self, 
        sesh: AsyncSession, 
        existing_obj_id: Any, 
        update_obj: Union[UpdateSchemaType, Dict[str, Any]], 
        *,
        commit: bool = False
    ) -> bool:
        """A base implementation of updating a specific instance of model 
        type, provided either an update schema pydantic type, or a dictionary
        containing elements where the keys map to attributes on model type,
        while their associated values are the desired new state for those 
        attributes.
        
        Arguments
        ---------
        :sesh: The database session on which to perform the update.
        :existing_obj_id: The ID for the existing instance to update.
        :update_obj: Either an update schema or dictionary containing desired 
        values for target attributes.

        Keyword arguments
        -----------------
        :commit: Whether commit should be used. If False, flush will be used.
                 Default is False.
        """
        try:
            # Dump the update object, removing unset keys and also keys set
            # to their given defaults.
            update_obj_data: Dict = update_obj.model_dump(
                exclude_unset = True,
                exclude_defaults = True
            )
            if not len(update_obj_data.items()):
                # No items to update? Just return.
                return True
            # If update object data isn't a dictionary, fail.
            if not isinstance(update_obj_data, Dict):
                raise TypeError
            # Construct an update statement, updating only those values found
            # in the resulting update object dictionary.
            update_stmt = (
                update(self._ModelTypeCls)
                    .where(self._ModelTypeCls.id == existing_obj_id)
                    .values(**update_obj_data)
            )
            # Execute the statement and return True if no issues.
            await sesh.execute(update_stmt)
            if commit:
                await sesh.commit()
            else:
                await sesh.flush()
            return True
        except Exception as e:
            raise e
    
    async def delete(self, sesh: AsyncSession, id: Any, *, 
        commit: bool = False
    ) -> bool:
        """A base implemention of deleting a specific instance of model type,
        provided the ID for the instance. The model type must have an 'id'
        attribute, otherwise, subtype must define a separate delete function
        applicable to the ID(s) configured on model type.
        
        Arguments
        ---------
        :sesh: The database session on which to delete model type.
        :id: The ID for the target to delete.

        Keyword arguments
        -----------------
        :commit: Whether commit should be used. If False, flush will be used.
                 Default is False.
        """
        try:
            delete_stmt = (
                delete(self._ModelTypeCls)
                    .where(self._ModelTypeCls.id == id)
            )
            await sesh.execute(delete_stmt)
            if commit:
                await sesh.commit()
            else:
                await sesh.flush()
            return True
        except Exception as e:
            raise e
