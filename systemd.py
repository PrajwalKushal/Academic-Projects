def collect_systemd_data(ssh):
    units_output = ssh.run(
        "systemctl list-units --type=service --all --no-legend"
    )

    services = []

    for line in units_output.splitlines():
        unit = line.split()[0]

        props_output = ssh.run(
            f"systemctl show {unit} "
            "--property=Description,"
            "InactiveExitTimestampMonotonic,"
            "ExecMainStartTimestampMonotonic,"
            "ActiveEnterTimestampMonotonic"
        )

        props = {}
        for p in props_output.splitlines():
            key, value = p.split("=", 1)
            props[key] = value

        try:
            inactive_exit = int(props["InactiveExitTimestampMonotonic"])
            exec_start = int(props["ExecMainStartTimestampMonotonic"])
            active_enter = int(props["ActiveEnterTimestampMonotonic"])
        except (KeyError, ValueError):
            continue

        if inactive_exit == 0 or exec_start == 0:
            continue

        services.append({
            "unit": unit,
            "description": props.get("Description", ""),
            "time_to_execstart_usec": exec_start - inactive_exit,
            "inactive_exit_usec": inactive_exit,
            "execstart_usec": exec_start,
            "active_enter_usec": active_enter,
        })

    return services
