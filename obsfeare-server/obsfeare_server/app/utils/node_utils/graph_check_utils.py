async def check_task_for_done(node, **repositories):
    if not node["taskId"]:
        return 0

    task_id = node["taskId"]
    task = await repositories["task_repository"].get_task_by_id(task_id)

    num_children_done = 0

    for todo_id in task["todos"]:
        todo = await repositories["todo_repository"].get_todo_by_id(todo_id)
        if todo["done"]:
            num_children_done += 1

    if num_children_done == len(task["todos"]) and num_children_done > 0:
        await repositories["task_repository"].update_task_by_id(task_id, {"done": True})
        return 1

    await repositories["task_repository"].update_task_by_id(task_id, {"done": False})
    return 0


async def check_node_for_done(node_id: str, **repositories):
    node = await repositories["node_repository"].get_node_by_id(node_id)

    if not node:
        raise Exception("Node not found")

    # reached leaf node
    if not node["children"]:
        is_task_done = await check_task_for_done(node, **repositories)

        if is_task_done:
            await repositories["node_repository"].update_node_by_id(
                node_id, {"done": True}
            )
            return 1

        await repositories["node_repository"].update_node_by_id(
            node_id, {"done": False}
        )
        return 0

    num_children_done = 0
    tot_children = 0

    for child_id in node["children"]:
        if await repositories["node_repository"].get_node_by_id(child_id):
            tot_children += 1

        is_child_done = await check_node_for_done(child_id, **repositories)
        num_children_done += is_child_done

    if num_children_done == tot_children and num_children_done > 0:
        await repositories["node_repository"].update_node_by_id(node_id, {"done": True})
        return 1

    await repositories["node_repository"].update_node_by_id(node_id, {"done": False})
    return 0


# repositories is a dictionary of repositories consisting of tree_repository, node_repository, task_repository, and todo_repository
async def check_tree_for_done(tree_id: str, **repositories):
    tree = await repositories["tree_repository"].get_tree_by_id(tree_id)
    if not tree:
        raise Exception("Tree not found")

    is_tree_done = await check_node_for_done(tree["nodeId"], **repositories)

    if is_tree_done:
        await repositories["tree_repository"].update_tree_by_id(tree_id, {"done": True})
        return True

    await repositories["tree_repository"].update_tree_by_id(tree_id, {"done": False})
    return False
