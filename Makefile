.PHONY: reset-player-data

# プレイヤーデータをリセットする (全てのプレイヤーデータが削除されます)
reset-player-data:
	@echo "プレイヤーデータを削除します..."
	@rm -f minecraft_server/world/playerdata/*.dat
	@rm -f minecraft_server/world/playerdata/*.dat_old
	@echo "完了しました。サーバーに参加し直すと初回参加処理が走ります。"
