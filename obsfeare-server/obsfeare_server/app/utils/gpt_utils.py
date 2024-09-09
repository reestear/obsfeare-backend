def generate_gpt_content(request: str):
    content = (
        f"""
    I have a description of my goal as: ${request}
    """
        + """
    Summarize the goal as Goal and follow below commands:
    Now, I want to visualize my Goal in view of tree, where my root is the my Goal.
    Therefore, dividing my Goal into different subroots where each subroot represents generalized aspect which should be accomplished in order to complete the main Goal. This process of dividing root and each subroot should continue until reaching the moment when all of the leaves (the nodes which don't have any children) have a capacity to be done in within a week.
    Give me the result in view of object i.e node, where it has its "title" (the title of the nodes including root, sub root, and leaves) and "children" array which also consists of the same objects i.e nodes which also have their own titles and possibly empty children array if they are leaves.
    Also, generate at least 45+ nodes including the root, subroots, and leaves.

    For example, the structure should be similar to this:
    {
    "title": "Some node title",
    "children": [
        {
        "title": String = "Some children node title",
        "children": Array = [other nodes...]
        }
    ]
    }
    Also, remember that "children" should be an array and that root shouldn't have any leaves!

    Wrap the json file which includes tree structure between keywords: !START! and !END!

    Divide the tree into subnodes very, very detailed, remembering that my leaves should be reachable within a week.

    And, finally give your overall feedback or advice in 1 sentence to this goal, also wrapping it inside of keywords !RESPONSE START! and !RESPONSE END!
    """
    )

    return content


def extract_tree_json(string, start_word, end_word) -> str:

    start_index = string.find(start_word)
    if start_index == -1:
        return ""

    end_index = string.find(end_word, start_index + len(start_word))
    if end_index == -1:
        return ""

    return string[start_index + len(start_word) : end_index].strip()
