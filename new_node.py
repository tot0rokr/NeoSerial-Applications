def new_node(api, uuid, name="new_node"):
    addr = api('provision_node', uuid=uuid, name=name)
    api('compose_node', addr)
    return addr

def new_nodes(api, uuids=[], name="new_node"):
    addrs = []
    for i in range(len(uuids)):
        addrs.append(new_node(api, uuids[i], name + str(i)))
    return addrs
