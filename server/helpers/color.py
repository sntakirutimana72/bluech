def colored(name: str) -> str:
    # ANSI colors
    cli_colors = {
        'red': '91', 'sky': '96', 'cyan': '36', 'gray': '34', 'blue': '94',
        'green': '32', 'black': '97', 'yellow': '93', 'orange': '33',
        'purple': '95', 'magenta': '35', 'di-white': '90', 'di-yellow': '92'
    }
    color_ = cli_colors.get(name)
    return f'\033[{color_ if color_ else 0}m'
