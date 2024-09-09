async def populate_tree(root_node, **repositories):
    root_node["children"] = await repositories["node_repository"].get_nodes_by_query(
        {"_id": {"$in": root_node["children"] or []}}
    )

    if root_node.get("isLeaf"):
        # Populating the "taskId" field if it exists
        if root_node.get("taskId"):
            root_node["taskId"] = await repositories["task_repository"].get_task_by_id(
                root_node["taskId"]
            )

            root_node["taskId"]["todos"] = await repositories[
                "todo_repository"
            ].get_todos_by_query({"taskId": root_node["taskId"]["_id"]})

    # Recursively populate children
    for child in root_node["children"]:
        await populate_tree(child, **repositories)

    return root_node
