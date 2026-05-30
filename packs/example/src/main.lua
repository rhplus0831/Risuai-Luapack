-- Entry module. Risu calls the global handlers defined here.
local utils = require('utils')

-- When a chat starts, greet using the character's name.
function onStart(id)
    addChat(id, 'char', utils.greeting(getName(id)))
end

-- Wrap every model output in brackets.
listenEdit('editOutput', function(id, value, meta)
    return utils.decorate(value)
end)
