"""General API endpoints."""
import os
import pathlib
import mimetypes

from typing import Optional

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse

from app import config, database
from app.dependencies import Sesh
from app.logger import log

router = APIRouter(tags = ["general"])


@router.get("/logo/{make_uid}")
async def request_make_logo(make_uid: str, sesh: Sesh):
    """Query the logo for the given Make UID. This will return a response
    that will invoke X-Accel-Redirect internally toward the resource.
    """
    log.debug("logo with UID %s has been requested" % make_uid)
    # query a vehicle make with the given id
    vehicle_make: Optional[database.VehicleMake] = \
        await database.find_vehicle_make(
            sesh,
            make_uid
        )
    # if the vehicle make can't be found, abort with 404.
    if vehicle_make is None:
        log.error("failed to find logo. returning 404")
        raise HTTPException(
            status_code = 404,
            detail = "the desired vehicle make can't be found!"
        )
    log.debug("found logo, it is %s" % str(vehicle_make.logo_media_uri))
    # otherwise, extract info from the vehicle make. we need the filename
    # and mimetype.
    logo_media_path = pathlib.Path(vehicle_make.logo_media_uri)
    # get filename with the extension.
    filename: str = logo_media_path.name
    # guess mimetype, fail if we can't find anything.
    mimetype, _ = mimetypes.guess_type(vehicle_make.logo_media_uri)
    if mimetype is None:
        raise HTTPException(
            status_code = 500,
            detail = "we found the logo! but could not determine type of "\
                     "resource."
        )
    
    # depending on status of using nginx, serve content either with
    # X-Accel-Redirect or a file response.
    if config.USING_NGINX:
        # build a url to redirect to
        redirect_to: str = "/%s" % str(logo_media_path).strip("/")
        log.debug("using nginx to serve content. X-Accel-Redirect to %s"
                  % redirect_to)
        # build a response with X-Accel-Redirect. this will trigger the internal
        # location block with /import/vehicles/logos/toyota.png or whatever.
        return Response(
            headers = {
                "Content-Type": mimetype,
                "X-Accel-Redirect": redirect_to
            }
        )
    else:
        # serve with file response.
        log.warning("application configured as NOT using nginx, we will use "\
                    " fastapi's fileresponse to serve the content...")
        # build an absolute path with the content directory variable.
        absolute_path: str = os.path.join(
            config.CONTENT_DIRECTORY,
            str(logo_media_path)
        )
        return FileResponse(absolute_path)
