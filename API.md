All actions return 200 on success; those referencing an item ID return 404 if
the ID is not found. The response body is empty unless specified otherwise. All
non-empty response bodies are JSON.

<dl>
    <dt>GET /items</dt>

    <dd>Return a list of items on the todo list, in the format {"id":
    &lt;item_id&gt;, "summary": &lt;one-line summary&gt;}</dd>

    <dt>GET /items/&lt;item_id&gt;</dt>

    <dd>Fetch all available information for a specific todo item, in
    the format {"id": &lt;item_id&gt;, "summary": &lt;one-line
    summary&gt;, "description" : &lt;free-form text field&gt;}</dd>

    <dt>POST /items</dt>
    
    <dd>Create a new todo item. The POST body is a JSON object with
    two fields: "summary" (must be under 120 characters, no newline),
    and "description" (free-form text field). The response is an
    object with one field: the id created by the server.</dd>

    <dt>DELETE /items/&lt;item_id&gt;</dt>

    <dd>Mark the item as done. (I.e., strike it off the list, so GET
    /items will not show it.) The response body is empty.</dd>

    <dt>PUT /items/&lt;item_id&gt;</dt>

    <dd>Modify an existing task. The PUT body is a JSON object with
    two fields: "summary" (must be under 120 characters, no newline),
    and "description" (free-form text field).</dd>

</dl>
