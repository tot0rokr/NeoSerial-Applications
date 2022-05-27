def heartbeat_app(api, addresses):
    import time

    result = dict()
    send_count = 16
    send_period = 1
    receive_period = 4
    ttl = 1

    # Running models
    for i in range(1, len(addresses)):
        for j in range(len(addresses)):
            src = addresses[j]
            dst = addresses[(j + i) % len(addresses)]
            api('hb_pub_set', *(src, dst, send_count, send_period, ttl))
            api('hb_sub_set', *(dst, src, dst, receive_period))

        time.sleep(receive_period)

        for j in range(len(addresses)):
            src = addresses[j]
            dst = addresses[(j + i) % len(addresses)]
            result[(src, dst)] = api('hb_sub_get', *(dst,))

    def log2b(value):
        """Binary log2"""
        log_val = 0
        while value != 0:
            value >>= 1
            log_val += 1
        return log_val

    # Gathering results
    receive_period_log = log2b(receive_period)
    for k, v in result.items():
        if v is None:
            print(k[0], k[1], "disconnected")
            continue
        count_log = v['count_log']
        if count_log >= receive_period_log:
            status = "strong"
        elif count_log >= receive_period_log - 1:
            status = "good"
        else:
            status = "bad"

        print(k[0], k[1], status)
