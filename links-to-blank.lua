-- file: links-to-blank.lua
function Link(el)
  -- Check if the link is external by looking for 'http' in the URL
  if string.find(el.target, "^http") then
    -- Add target="_blank" to external links
    if el.attributes.target == nil then
      el.attributes.target = "_blank"
      -- Optionally, add rel="noopener noreferrer" for security reasons
      el.attributes.rel = "noopener noreferrer"
    end
  end
  return el
end