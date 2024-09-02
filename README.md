## Demo repository for custom inventory plugins

Please see: https://termlen0.github.io/2019/11/16/observations/ for details

### Commands

```bash
# check inventory list
ansible-inventory -i csv_inventory.yaml --playbook-dir ./ --list

# check inventory graph
ansible-inventory -i csv_inventory.yaml --playbook-dir ./ --graph

# run playbook
ansible-playbook -i csv_inventory.yaml playbook.yaml

ANSIBLE_INVENTORY_ENABLED=my_csv_plugin ansible-inventory -i csv_inventory.yml --list
```

### VScode Extensions...

- https://velog.io/@kshjessica/VSCode-%EC%97%90%EC%84%9C-Prettier-%EB%9E%91-Black-%EB%8F%99%EC%8B%9C%EC%97%90-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0
