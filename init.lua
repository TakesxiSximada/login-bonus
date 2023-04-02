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
      local player_meta = player:get_meta()
      local last_timestamp = player_meta:get_int("login_bonus:last_timestamp")
      local current_timestamp = os.time(os.date("!*t"))

      -- UTC to JST
      local last_date = os.date("%Y%m%d", last_timestamp + 32400)
      local current_date = os.date("%Y%m%d", current_timestamp + 32400)

      -- 当日付与済みであるため付与しない
      if last_date == current_date then
         minetest.chat_send_player(name, "Welcome home")
         do return end
      end

      -- 注意
      -- inventoryがいっぱいの場合、ログインボーナスは付与されない。
      -- その場合であっても、メッセージは同じように表示される。
      local today = os.date("%m%d", current_timestamp + 32400)
      local message = string.format("Hi %s, You got a login bonus. (bonus: apple+1)", name)

      -- 設定からスペシャルログインボーナスデーを取得し、スペシャルログインボーナスデーかどうかを判定する。
      -- スペシャルログインボーナスデーはmmdd形式で、複数指定する場合はカンマで区切る。
      local special_days = minetest.settings:get("symdon_special_days") or ""
      if string.match(special_days, today) then
         message = string.format("Hi %s, You got a login special bonus. (special bonus: diamond+1)", name)
         local login_bonus_special = ItemStack("default:diamond 1")
         inv:add_item("main", login_bonus_special)
      else
         local login_bonus = ItemStack("default:apple 1")
         inv:add_item("main", login_bonus)
      end

      player_meta:set_int("login_bonus:last_timestamp", current_timestamp)
      minetest.chat_send_player(name, message)
end)
