def help():
    print_message = [
        "Welcome to tfmt, a cli tool for summarising terraform plan outputs",
        "usage: tfmt [file]"
    ]
    print("\n".join(print_message))

commands = [
    "help",
    "command1"
]
