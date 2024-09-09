from bson import ObjectId
from obsfeare_server.app.repositories.node_repository.node_repository import (
    NodeRepository,
)
from obsfeare_server.app.repositories.tree_repository.tree_repository import (
    TreeRepository,
)


async def parse_node_dfs(
    node_repository: NodeRepository, node, depth, tree_id, user_id
):
    if not node["children"]:  # If there are no children
        last_node_id = await node_repository.create_node(
            node_title=node["title"],
            user_id=user_id,
            tree_id=tree_id,
            children=[],
            done=False,
            is_root=True if depth == 0 else False,
            is_leaf=True,
        )

        return last_node_id
    else:
        children = []
        for child in node["children"]:
            child_id = await parse_node_dfs(
                node_repository, child, depth + 1, tree_id, user_id
            )
            children.append(child_id)

        last_node_id = await node_repository.create_node(
            node_title=node["title"],
            user_id=user_id,
            tree_id=tree_id,
            children=children,
            done=False,
            is_root=True if depth == 0 else False,
            is_leaf=False,
        )

        return last_node_id


async def parse_tree(
    tree_repository: TreeRepository, node_repository: NodeRepository, root_node, user_id
):
    tree_object_id = ObjectId()
    tree_id = str(tree_object_id)

    # Start DFS parsing
    root_node_id = await parse_node_dfs(node_repository, root_node, 0, tree_id, user_id)

    last_tree_id = await tree_repository.create_tree(
        user_id, root_node_id, False, _id=ObjectId(tree_id)
    )

    return last_tree_id


async def append_node(
    node_repository: NodeRepository,
    root_node: dict,
    node_id: str,
):

    node = await node_repository.get_node_by_id(node_id)
    node_children = root_node["children"]
    children = []
    for child in node_children:
        node_child = await parse_node_dfs(
            node_repository, child, 1, node["tree_id"], node["user_id"]
        )
        children.append(node_child)

    await node_repository.update_node_by_id(
        node_id, {"children": children, "isLeaf": False, "focus": False}
    )
