-- Small helpers shared across the pack. Returned table becomes the module.
local M = {}

function M.greeting(name)
    return 'Hello, ' .. name .. '!'
end

function M.decorate(text)
    return '[' .. text .. ']'
end

return M
