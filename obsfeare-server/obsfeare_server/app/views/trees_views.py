import json

from adrf.decorators import api_view
from django.apps import apps
from obsfeare_server.app.utils.auth_utils import IsAuthenticated, JWTAuthentication
from openai import AsyncOpenAI
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.exceptions import status

from ..repositories import (
    history_repository,
    node_repository,
    task_repository,
    todo_repository,
    tree_repository,
)
from ..utils.decorated_response_utils import DecoratedResponse
from ..utils.gpt_utils import extract_tree_json, generate_gpt_content
from ..utils.node_utils.graph_check_utils import check_tree_for_done
from ..utils.node_utils.graph_parser_utils import append_node as append_node_util
from ..utils.node_utils.graph_parser_utils import parse_tree
from ..utils.node_utils.graph_populate import populate_tree

openai: AsyncOpenAI = apps.get_app_config("core").openai


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
async def index(request):
    try:
        trees = await tree_repository.get_trees_by_user_id(request.user.id)

        # print("trees", trees, flush=True)

        populated_trees = []
        for tree in trees:
            print("Current tree", tree, flush=True)
            tree_node = await node_repository.get_node_by_id(tree["nodeId"])

            if not tree_node:
                continue

            print("tree_node", tree_node, flush=True)

            try:
                populated_tree_node = await populate_tree(
                    tree_node,
                    node_repository=node_repository,
                    task_repository=task_repository,
                    todo_repository=todo_repository,
                )
            except Exception as e:
                return DecoratedResponse(
                    {"message": f"Error While Populating Tree: {e}"},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            tree_payload = {
                "treeId": tree["_id"],
                "tree": populated_tree_node,
            }
            populated_trees.append(tree_payload)

        return DecoratedResponse(
            {"trees": populated_trees, "message": "Successfully Pulled All the Trees"},
            status_code=status.HTTP_200_OK,
            safe=False,
        )

    except Exception as e:
        return DecoratedResponse(
            {"message": f"Error While Fetching Trees: {e}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
async def create_tree(request):
    try:
        user_request = request.data.get("request")

        content = generate_gpt_content(user_request)

        completion = await openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": content},
            ],
        )

        # If completion is not successful
        if completion.choices[0].message.content == "":
            return DecoratedResponse(
                {"message": "Error While Generating Tree: OpenAI Completion Failed"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        response_message = extract_tree_json(
            completion.choices[0].message.content, "!RESPONSE START!", "!RESPONSE END!"
        )
        tree_json = extract_tree_json(
            completion.choices[0].message.content, "!START!", "!END!"
        )

        if tree_json == "":
            return DecoratedResponse(
                {"message": "Error While Generating Tree: Tree JSON Not Found"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        root_node = json.loads(tree_json)

        tree_id = await parse_tree(
            tree_repository, node_repository, root_node, request.user.id
        )
        await history_repository.create_history(
            user_request, response_message, request.user.id
        )

        return DecoratedResponse(
            {"treeId": tree_id, "message": "Successfully Generated Tree"},
            status_code=status.HTTP_201_CREATED,
            safe=False,
        )
    except Exception:
        return DecoratedResponse(
            {"message": "Error While Generating Tree"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
async def append_node(request):
    try:
        tree_id = request.headers.get("tree_id")
        node_id = request.headers.get("node_id")

        node = await node_repository.get_node_by_id(node_id)

        content = generate_gpt_content(node["nodeTitle"])

        completion = await openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": content},
            ],
        )

        # If completion is not successful
        if completion.choices[0].message.content == "":
            return DecoratedResponse(
                {"message": "Error While Generating Node: OpenAI Completion Failed"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        response_message = extract_tree_json(
            completion.choices[0].message.content, "!RESPONSE START!", "!RESPONSE END!"
        )
        tree_json = extract_tree_json(
            completion.choices[0].message.content, "!START!", "!END!"
        )

        if tree_json == "":
            return DecoratedResponse(
                {"message": "Error While Generating Node: Tree JSON Not Found"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        root_node = json.loads(tree_json)

        await append_node_util(node_repository, root_node, node_id)

        tree = await tree_repository.get_tree_by_id(tree_id)
        tree_node = await node_repository.get_node_by_id(tree["nodeId"])

        user_request = (
            f'Appending the node: {node["nodeTitle"]} of tree: {tree_node["nodeTitle"]}'
        )
        await history_repository.create_history(
            user_request, response_message, request.user.id
        )

        await check_tree_for_done(
            tree_id,
            tree_repository=tree_repository,
            node_repository=node_repository,
            task_repository=task_repository,
            todo_repository=todo_repository,
        )

        return DecoratedResponse(
            {"message": "Successfully Appended Node"},
            status_code=status.HTTP_201_CREATED,
            safe=False,
        )

    except Exception:
        return DecoratedResponse(
            {"message": "Error While Appending Node"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
