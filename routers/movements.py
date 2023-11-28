from fastapi import APIRouter, Request, Response, status
from models.movements import Movement
import models.errors as cax_errors


router = APIRouter(prefix='/movements')


@router.post('/', tags=["movements"])
async def create_move(request: Request):

    request_body = await request.json()

    try:
        user_id = request_body['userId']
        origin = request_body['origin']
        dest = request_body['dest']
        route_name = request_body['routeName']

        movement = Movement(user_id, origin, dest, route_name)
        response_body = movement.save()
        status_code = status.HTTP_201_CREATED

    except KeyError as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response_body = {'error': f'Missing key: {e.args[0]}'}

    except cax_errors.DataNotInsertedException as e:
        status_code = status.HTTP_409_CONFLICT
        response_body = {'error': f'{e.args[0]}'}

    except cax_errors.DatabaseNotOnlineException as e:
        status_code = status.HTTP_409_CONFLICT
        response_body = {'error': f'{e.args[0]}'}

    return Response(content=response_body, status_code=status_code, headers={'Content-Type': 'application/json'})


@router.get('/{user_id}', tags=["movements"])
async def get_movements(user_id):

    try:

        response_body = Movement.find(user_id)

        status_code = status.HTTP_200_OK

    except cax_errors.CantParseDataToModel as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response_body = {'error': f'Data not parsed: {e.args[0]}'}

    return Response(content=response_body, status_code=status_code, headers={'Content-Type': 'application/json'})