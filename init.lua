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
      local player_meta = player:get_meta()
      local last_timestamp = player_meta:get_int("login_bonus:last_timestamp")
      local current_timestamp = os.time(os.date("!*t"))

      local last_date = os.date("%Y%m%d", last_timestamp)
      local current_date = os.date("%Y%m%d", current_timestamp)

      -- 当日付与済みであるため付与しない
      if last_date == current_date then
	 minetest.chat_send_player(name, "Welcome home")
	 do return end
      end

      -- 注意
      -- inventoryがいっぱいの場合、ログインボーナスは付与されない。
      -- その場合であっても、メッセージは同じように表示される。
      inv:add_item("main", login_bonus)
      player_meta:set_int("login_bonus:last_timestamp", current_timestamp)
      minetest.chat_send_player(name, message)
end)
