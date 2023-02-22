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

-- Login Bonus
minetest.register_on_joinplayer(function (player)
      local name = player:get_player_name()
      local inv = player:get_inventory()
      local login_bonus = ItemStack("default:apple 1")
      local message = string.format("Hi %s, You got a login bonus. (bonus: apple+1)", name)
      -- 注意
      -- ログインボーナスと言いつつ、ログインしたら必ず林檎を1つ貰える。
      -- inventoryがいっぱいの場合、ログインボーナスは付与されない。
      -- ログインボーナスが貰えても、貰えなくてもメッセージは同じように表示される。
      inv:add_item("main", login_bonus)
      minetest.chat_send_player(name, message)
end)
