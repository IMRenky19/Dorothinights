def decrypt_user_key(key: str, login_time: int) -> str:

    LOG_SECRET_KEY = "12451c15120f1c1b203d421a3b132ecf"

    buf = [int(x, 16) for x in
           [y.replace("f", "") for y in [LOG_SECRET_KEY[z:z + 2] for z in range(0, len(LOG_SECRET_KEY), 2)]]]
    data_bin = "".join([format(ord(x), '08b') for x in key])
    format_data = [data_bin[i:i + 8] for i in range(0, len(data_bin), 8)]
    try:
        decrypt_buf = "".join(['{:08b}'.format(int(format_data[i], 2) - buf[i]) if i in (6, 15) else '{:08b}'.format(
            int(format_data[i], 2) + buf[i]) for i in range(len(format_data))])
        decrypt_data = "".join(map(lambda x: chr(int(str(x), 2)), [decrypt_buf[i:i + 8] for i in
                                                                   range(0, len(decrypt_buf),
                                                                         8)])) if login_time else None
        return decrypt_data

    except Exception as e:
        return None