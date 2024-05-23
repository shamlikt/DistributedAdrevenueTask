.PHONY: cluster_up run_cluster run_cluster_no_args cluster_down


cluster_up:
	sudo docker-compose up -d --build

run_cluster:
	docker exec -it admarketApp /usr/local/bin/python main.py --ads /data/$(ads) --publisher /data/$(publisher) --date $(date) --output /data/$(output) -c

run_local:
	docker exec -it admarketApp /usr/local/bin/python main.py --ads /data/$(ads) --publisher /data/$(publisher) --date $(date) --output /data/$(output)

cluster_down:
	sudo docker-compose down
