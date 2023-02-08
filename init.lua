symdon = {}

symdon.modname = minetest.get_current_modname()
symdon.modpath = minetest.get_modpath(symdon.modname)

minetest.register_chatcommand("symdon", {
     params = "",
     description = "Hello minetest",
     func = function (name, param)
       minetest.chat_send_player(name, "Hello minetest!!")
     end
})
