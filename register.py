from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport
import websockets
import asyncio
import aiohttp
from datetime import datetime, timezone

end_time = None
mode = None
pendingTimer = None

def disable():
    print('disabling robots')
    if pendingTimer is not None:
        pendingTimer.cancel()

async def process_field_control(set_mode, set_end_time):
    global end_time, mode

    if set_mode != mode:
        mode = set_mode
        print(f"Mode: {mode}")

    if set_end_time != end_time:
        end_time = set_end_time
        if end_time is None:
            disable()
        else:
            global pendingTimer
            if pendingTimer is not None:
                pendingTimer.cancel()
            pendingTimer = asyncio.create_task(timer(end_time))

async def timer(end_time: str):
    # time is in ISO format
    timeToWait = (datetime.fromisoformat(end_time) - datetime.now(timezone.utc)).total_seconds()
    await asyncio.sleep(timeToWait)
    disable()

async def subscribe(server, serverPort, fieldId: int):
    url = 'ws://' + server + ':' + str(serverPort) + '/graphql'
    transport = WebsocketsTransport(url=url)
    query = gql("""
    subscription FieldControl($fieldId: Int!) {
            fieldControl(fieldId: $fieldId) {
            endTime
            mode
        }
    }
    """)

    variables = {
        "fieldId": fieldId
    }

    async with Client(transport=transport) as session:
        print('Subscribed to field control')
        try:
            async for result in session.subscribe(query, variable_values=variables):
                await process_field_control(result['fieldControl']['mode'], result['fieldControl']['endTime'])
        except websockets.exceptions.ConnectionClosedError:
            print('Connection lost')
            return

async def pollDeviceConfig(server, serverPort, uuid):
    url = 'http://' + server + ':' + str(serverPort) + '/graphql'
    transport = AIOHTTPTransport(url)

    query = gql("""
        query getDisplay($uuid: String!) {
          display(uuid: $uuid) {
            field {
                id
                fieldControl {
                    mode
                    endTime
                }
            }
          }
        }
        """)
    
    variables = {
            "uuid": uuid
        }


    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        lastValue = None
        current_subscription = None
        while True:
            await asyncio.sleep(0.25)
            try:
                result = await session.execute(query, variables)
                field = result['display']['field']
            except aiohttp.client_exceptions.ClientConnectorError:
                if lastValue is not None:
                    print("Connection lost")
                    current_subscription.cancel()
                    lastValue = None
                continue
        
            if field is None:
                if lastValue is not None:
                    lastValue = None
                    current_subscription.cancel()
                    print("Unassigned")
                continue
        
            fieldId = int(field['id'])
            if fieldId is not lastValue:
                if current_subscription is not None:
                    current_subscription.cancel()
                lastValue = fieldId
                print(f"Assigned to field with id {fieldId}")
                current_subscription = asyncio.create_task(subscribe(server, serverPort, fieldId))

            fieldControl = field['fieldControl']

            if fieldControl is not None:
                await process_field_control(fieldControl['mode'], fieldControl['endTime'])

def subscribe(server, serverPort, uuid):
    while True:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(pollDeviceConfig(server, serverPort, uuid))
            loop.close()
        except aiohttp.client_exceptions.ClientConnectorError:
            continue